#!/usr/bin/env node
// timing-report.mjs — offline reader for framework/state/timing.ndjson.
//
// Turns the append-only timing log into per-run summaries: per-stage durations,
// the three optimization buckets (human / compute / llm_gen), retry counts, and
// halt/incomplete flags. Read-only — never writes, never gates pipeline control
// flow (the "observability only" invariant holds). Dependency-free Node ESM.
//
// Usage:
//   node framework/tools/timing-report.mjs [--last|--all|--run <run_id>] [--json] [--file <path>] [--pipeline <name>]
//     (default)        same as --last
//     --last           most recent matching run
//     --run <run_id>   a specific run by its run_id (== its run_start timestamp)
//     --all            every matching run + an aggregate (median per stage/bucket)
//     --json           machine-readable output (for feeding later optimization work)
//     --file <path>    read a different ndjson file (default: ../state/timing.ndjson)
//     --pipeline <n>   filter to a pipeline (default: prototype; "*" for all)

import { readFileSync } from 'node:fs'
import { fileURLToPath } from 'node:url'
import { dirname, join, resolve } from 'node:path'

const SCRIPT_DIR = dirname(fileURLToPath(import.meta.url))
const DEFAULT_LOG = join(SCRIPT_DIR, '..', 'state', 'timing.ndjson')

// ── CLI ────────────────────────────────────────────────────────────────────
function parseArgs(argv) {
  const o = { mode: 'last', json: false, file: DEFAULT_LOG, pipeline: 'prototype', runId: null }
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i]
    if (a === '--last') o.mode = 'last'
    else if (a === '--all') o.mode = 'all'
    else if (a === '--run') { o.mode = 'run'; o.runId = argv[++i] }
    else if (a === '--json') o.json = true
    else if (a === '--file') o.file = resolve(argv[++i])
    else if (a === '--pipeline') o.pipeline = argv[++i]
    else if (a === '--help' || a === '-h') o.mode = 'help'
    else throw new Error(`unknown argument: ${a}`)
  }
  return o
}

// ── parse + segment ──────────────────────────────────────────────────────────
function parseEvents(text) {
  const events = []
  for (const raw of text.split(/\r?\n/)) {
    const line = raw.trim()
    if (!line) continue
    let ev
    try { ev = JSON.parse(line) } catch { continue } // tolerate malformed lines
    if (!ev || typeof ev.t !== 'string') continue
    const ms = Date.parse(ev.t)
    if (Number.isNaN(ms)) continue
    ev._ms = ms
    events.push(ev)
  }
  // append order ≈ chronological; sort defensively (stable on _ms)
  return events.map((e, i) => ({ e, i })).sort((a, b) => a.e._ms - b.e._ms || a.i - b.i).map(x => x.e)
}

// A run = the events from a run_start up to its run_end (or the next run_start /
// end-of-file if run_end is missing). Stage/consultant events carry no run_id in
// the canonical schema, so chronological segmentation — not run_id grouping — is
// the reliable association (runs never overlap: pipelines are foreground/in-thread).
function segmentRuns(events) {
  const runs = []
  let cur = null
  for (const ev of events) {
    if (ev.type === 'run_start') {
      if (cur) runs.push(cur) // prior run had no run_end → closed by this start
      cur = {
        run_id: ev.run_id || ev.t,
        pipeline: ev.pipeline || null,
        start: ev,
        end: null,
        events: [],
      }
      continue
    }
    if (!cur) continue // stray events before any run_start
    if (ev.type === 'run_end') { cur.end = ev; cur.events.push(ev); runs.push(cur); cur = null; continue }
    cur.events.push(ev)
  }
  if (cur) runs.push(cur)
  return runs
}

// ── per-run analysis ──────────────────────────────────────────────────────────
const START_TYPES = { stage_start: 'stage', substep_start: 'substep', consultant_prompted: 'consultant' }
const END_TYPES = { stage_end: 'stage', substep_end: 'substep', consultant_responded: 'consultant' }

function keyOf(ev, kind) {
  if (kind === 'stage') return `s|${ev.stage || ''}`
  if (kind === 'substep') return `ss|${ev.stage || ''}|${ev.substep || ''}|${ev.surface || ''}`
  return `c|${ev.stage || ''}|${ev.label || ''}` // consultant
}

function analyzeRun(run) {
  const open = new Map() // key -> [startEvent,...]
  const spans = []
  const orphanEnds = []
  for (const ev of run.events) {
    const startKind = START_TYPES[ev.type]
    const endKind = END_TYPES[ev.type]
    if (startKind) {
      const k = keyOf(ev, startKind)
      if (!open.has(k)) open.set(k, [])
      open.get(k).push(ev)
    } else if (endKind) {
      const k = keyOf(ev, endKind)
      const arr = open.get(k)
      if (arr && arr.length) {
        const s = arr.pop()
        spans.push({
          kind: endKind,
          stage: ev.stage ?? s.stage ?? null,
          substep: ev.substep ?? s.substep ?? null,
          surface: ev.surface ?? s.surface ?? null,
          label: ev.label ?? s.label ?? null,
          attempt: ev.attempt ?? s.attempt ?? null,
          outcome: ev.outcome ?? s.outcome ?? null,
          startMs: s._ms,
          endMs: ev._ms,
          durMs: Math.max(0, ev._ms - s._ms),
          concurrent: Boolean(ev.concurrent || s.concurrent),
        })
      } else {
        orphanEnds.push(ev) // end with no matching start (rare; flag, don't crash)
      }
    }
  }
  // leftover opens = orphan starts = halt signal
  const orphans = []
  for (const [, arr] of open) for (const s of arr) orphans.push(s)
  orphans.sort((a, b) => a._ms - b._ms)

  const lastMs = run.events.length ? run.events[run.events.length - 1]._ms : run.start._ms
  const total = (run.end ? run.end._ms : lastMs) - run.start._ms

  const stageSpans = spans.filter(s => s.kind === 'stage')
  const substepSpans = spans.filter(s => s.kind === 'substep')
  const consultantSpans = spans.filter(s => s.kind === 'consultant')

  const human = sum(consultantSpans.map(s => s.durMs))
  const verifyCompute = sum(substepSpans.filter(s => s.stage === 'verify').map(s => s.durMs))
  const scaffoldNpm = sum(substepSpans.filter(s => s.stage === 'scaffold' && s.substep === 'npm-install').map(s => s.durMs))
  const scaffoldStage = stageSpans.find(s => s.stage === 'scaffold')
  const scaffoldOverlapped = Boolean(scaffoldStage && scaffoldStage.concurrent)
  const compute = verifyCompute + (scaffoldOverlapped ? 0 : scaffoldNpm)
  const llmGen = Math.max(0, total - human - compute)

  const verifyAttempts = substepSpans
    .filter(s => s.stage === 'verify' && typeof s.attempt === 'number')
    .reduce((m, s) => Math.max(m, s.attempt), 0)
  const retrySurfaces = substepSpans.filter(s => s.substep === 'retry-surface').length

  const incomplete = !run.end || orphans.length > 0
  const haltAt = orphans.length
    ? `${orphans[0].type} ${orphans[0].stage || ''}${orphans[0].substep ? '/' + orphans[0].substep : ''}`.trim()
    : (!run.end ? 'no run_end' : null)

  return {
    run_id: run.run_id,
    pipeline: run.pipeline,
    startT: run.start.t,
    endT: run.end ? run.end.t : null,
    total,
    buckets: { human, compute, llm_gen: llmGen },
    breakdown: { verifyCompute, scaffoldNpm, scaffoldOverlapped },
    stages: stageSpans.map(s => ({ stage: s.stage, durMs: s.durMs, concurrent: s.concurrent })),
    substeps: substepSpans.map(s => ({ stage: s.stage, substep: s.substep, surface: s.surface, attempt: s.attempt, outcome: s.outcome, durMs: s.durMs })),
    consultant: consultantSpans.map(s => ({ stage: s.stage, label: s.label, durMs: s.durMs })),
    retries: { verifyAttempts, retrySurfaces },
    incomplete,
    haltAt,
    orphanEndCount: orphanEnds.length,
  }
}

const sum = xs => xs.reduce((a, b) => a + b, 0)
function median(xs) {
  if (!xs.length) return 0
  const s = [...xs].sort((a, b) => a - b)
  const m = Math.floor(s.length / 2)
  return s.length % 2 ? s[m] : Math.round((s[m - 1] + s[m]) / 2)
}

// ── formatting ────────────────────────────────────────────────────────────────
function fmt(ms) {
  if (ms == null) return '—'
  const s = ms / 1000
  if (s < 1) return `${ms}ms`
  if (s < 60) return `${s.toFixed(1)}s`
  const m = Math.floor(s / 60)
  const r = Math.round(s % 60)
  return `${m}m ${r}s`
}
const pct = (part, whole) => (whole > 0 ? `${Math.round((part / whole) * 100)}%` : '—')
const pad = (str, n) => String(str).padEnd(n)
const padL = (str, n) => String(str).padStart(n)

function renderRun(a) {
  const L = []
  L.push(`── ${a.pipeline || '?'} run ${a.run_id}`)
  L.push(`   ${a.startT}  →  ${a.endT || '(no run_end)'}`)
  L.push(`   total wall-clock: ${fmt(a.total)}${a.incomplete ? `   ⚠ INCOMPLETE (halt: ${a.haltAt})` : ''}`)
  L.push('')
  L.push('   buckets (of total):')
  L.push(`     human round-trips   ${padL(fmt(a.buckets.human), 9)}  ${padL(pct(a.buckets.human, a.total), 4)}`)
  L.push(`     real compute        ${padL(fmt(a.buckets.compute), 9)}  ${padL(pct(a.buckets.compute, a.total), 4)}   (verify ${fmt(a.breakdown.verifyCompute)}${a.breakdown.scaffoldNpm ? `; scaffold npm ${fmt(a.breakdown.scaffoldNpm)}${a.breakdown.scaffoldOverlapped ? ' — concurrent, off critical path' : ''}` : ''})`)
  L.push(`     llm generation      ${padL(fmt(a.buckets.llm_gen), 9)}  ${padL(pct(a.buckets.llm_gen, a.total), 4)}   (residual: total − human − compute)`)
  if (a.retries.verifyAttempts > 1 || a.retries.retrySurfaces > 0)
    L.push(`   retries: ${a.retries.verifyAttempts} verify attempt(s), ${a.retries.retrySurfaces} surface re-render(s)`)
  L.push('')
  L.push('   per-stage:')
  for (const s of a.stages)
    L.push(`     ${pad(s.stage, 16)} ${padL(fmt(s.durMs), 9)}  ${padL(pct(s.durMs, a.total), 4)}${s.concurrent ? '   [concurrent — overlaps, not summed into buckets]' : ''}`)
  const genSubs = a.substeps.filter(s => s.stage === 'generator')
  if (genSubs.length) {
    L.push('')
    L.push('   generator substeps:')
    for (const s of genSubs)
      L.push(`     ${pad((s.substep || '') + (s.surface ? ` ${s.surface}` : ''), 24)} ${padL(fmt(s.durMs), 9)}${s.attempt ? `  attempt ${s.attempt}` : ''}`)
  }
  const verSubs = a.substeps.filter(s => s.stage === 'verify')
  if (verSubs.length) {
    L.push('')
    L.push('   verify phases:')
    for (const s of verSubs)
      L.push(`     ${pad(s.substep || '', 16)} ${padL(fmt(s.durMs), 9)}${s.attempt ? `  attempt ${s.attempt}` : ''}${s.outcome ? `  ${s.outcome}` : ''}`)
  }
  if (a.consultant.length) {
    L.push('')
    L.push('   consultant prompts (human time):')
    for (const s of a.consultant)
      L.push(`     ${pad(`${s.stage}/${s.label || ''}`, 28)} ${padL(fmt(s.durMs), 9)}`)
  }
  return L.join('\n')
}

function renderAggregate(analyses) {
  const L = []
  L.push(`── aggregate over ${analyses.length} run(s) (median)`)
  L.push(`   total            ${padL(fmt(median(analyses.map(a => a.total))), 9)}`)
  L.push(`   human            ${padL(fmt(median(analyses.map(a => a.buckets.human))), 9)}`)
  L.push(`   compute          ${padL(fmt(median(analyses.map(a => a.buckets.compute))), 9)}`)
  L.push(`   llm generation   ${padL(fmt(median(analyses.map(a => a.buckets.llm_gen))), 9)}`)
  const stageNames = [...new Set(analyses.flatMap(a => a.stages.map(s => s.stage)))]
  L.push('   per-stage median:')
  for (const name of stageNames) {
    const durs = analyses.flatMap(a => a.stages.filter(s => s.stage === name).map(s => s.durMs))
    L.push(`     ${pad(name, 16)} ${padL(fmt(median(durs)), 9)}`)
  }
  const incomplete = analyses.filter(a => a.incomplete).length
  if (incomplete) L.push(`   ⚠ ${incomplete} incomplete run(s) included`)
  return L.join('\n')
}

const HELP = `timing-report.mjs — summarize framework/state/timing.ndjson
  --last (default) | --all | --run <run_id> | --json | --file <path> | --pipeline <name|*>`

// ── main ──────────────────────────────────────────────────────────────────────
function main() {
  let opts
  try { opts = parseArgs(process.argv.slice(2)) } catch (e) { console.error(e.message); console.error(HELP); process.exit(2) }
  if (opts.mode === 'help') { console.log(HELP); return }

  let text
  try { text = readFileSync(opts.file, 'utf8') } catch {
    console.error(`no timing log at ${opts.file} (run /prototype once to populate it, or pass --file)`)
    process.exit(1)
  }

  const runs = segmentRuns(parseEvents(text))
  let analyses = runs.map(analyzeRun)
  if (opts.pipeline !== '*') analyses = analyses.filter(a => a.pipeline === opts.pipeline)

  if (!analyses.length) {
    console.error(`no ${opts.pipeline === '*' ? '' : opts.pipeline + ' '}runs found in ${opts.file}`)
    process.exit(1)
  }

  let selected
  if (opts.mode === 'run') {
    selected = analyses.filter(a => a.run_id === opts.runId)
    if (!selected.length) { console.error(`run_id not found: ${opts.runId}`); process.exit(1) }
  } else if (opts.mode === 'all') {
    selected = analyses
  } else { // last
    selected = [analyses[analyses.length - 1]]
  }

  if (opts.json) {
    const out = opts.mode === 'all' ? { runs: selected } : selected[0] // --last/--run → one object; --all → {runs:[...]}
    console.log(JSON.stringify(out, null, 2))
    return
  }

  console.log(selected.map(renderRun).join('\n\n'))
  if (opts.mode === 'all' && selected.length > 1) { console.log(''); console.log(renderAggregate(selected)) }
}

main()
