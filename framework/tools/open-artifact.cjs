#!/usr/bin/env node
/**
 * open-artifact.cjs — PostToolUse hook (matcher: Write)
 *
 * Purpose: the moment a pipeline writes a final HTML artefact, open it in the
 * consultant's default browser so it is already on screen when the accept gate
 * appears. Removes the alt-tab-and-navigate round trip from every gate in
 * /analyse-requirement, /analyse-inputs, /review-requirement, /review-inputs,
 * /design-system and /wireframe.
 *
 * Canonical policy (which paths, why, opt-out, failure semantics):
 *   framework/shared/artifact-preview.md
 *
 * This is a harness-level affordance. It is NOT invoked by any orchestrator,
 * agent, or skill — do not add a call site for it, and do not look for one.
 *
 * Self-contained: no dependencies, reads the hook payload as JSON on stdin.
 * Fails open: every error path exits 0 so it can never wedge a session or a
 * pipeline. A viewer that did not launch is not a refusal and has no RF-NN.
 *
 * Writes nothing to stdout — on a PostToolUse hook stdout is a control channel,
 * and a stray {"decision":"block"} would break the calling pipeline. Progress
 * goes to stderr.
 *
 * Dry-run (allowlist testing, no browser):
 *   node framework/tools/open-artifact.cjs --dry-run <repo-relative-path> [...]
 *   → prints "OPEN <path>" or "SKIP <path> (<reason>)" per argument.
 */

'use strict';

const fs = require('fs');
const os = require('os');
const path = require('path');
const crypto = require('crypto');
const { spawn } = require('child_process');
const { pathToFileURL } = require('url');

// ── Path allowlist ─────────────────────────────────────────────────────────
// Repo-relative, forward-slashed. Allowlist-only: anything unmatched is
// skipped, so there is no deny list to keep in sync. Canonical rationale for
// each inclusion/exclusion lives in framework/shared/artifact-preview.md.
//
// Deliberately NOT matched:
//   wireframes/<slug>/<variant>/screen-NN-*.html  (3 segments — index.html is
//     the comparator's entry point and links to these on click)
//   design-system/.workspace/**                   (transient styler scratch)
//   design-system/design-system.html              (legacy, no longer authored)
//   prototypes/** framework/** template/** input/**
const ALLOW = [
  /^analyse-requirements\/[^/]+\/[^/]+\.html$/,
  /^analyse-inputs\/[^/]+\/[^/]+\.html$/,
  /^review-requirements\/[^/]+\/[^/]+\.html$/,
  /^review-inputs\/[^/]+\/[^/]+\.html$/,
  /^design-system\/design-system-(light|dark)\.html$/,
  /^wireframes\/[^/]+\/index\.html$/,
];

// Below every opened artefact's own verify-artifact-write `expected_min_bytes`
// floor (lowest is 1024). Catches a clearly-truncated write before it opens.
const MIN_BYTES = 512;

function isAllowed(relPath) {
  return ALLOW.some((re) => re.test(relPath));
}

function toRel(absPath, cwd) {
  return path.relative(cwd, absPath).replace(/\\/g, '/');
}

function optedOut() {
  const v = process.env.REQGEN_NO_AUTO_OPEN;
  return typeof v === 'string' && v !== '' && v !== '0' && v.toLowerCase() !== 'false';
}

// ── Dedupe state ───────────────────────────────────────────────────────────
// { "<relpath>": "<sha256>" } in the OS temp dir, keyed by session.
//
// Temp dir, not framework/state/ — that tree is orchestrator/agent-owned and
// git-tracked; a hook writing there would breach ownership.
//
// Session-keyed so a fresh session always opens, even for byte-identical
// content. Within a session an unchanged hash means this is
// verify-artifact-write's silent re-Write, not new work → no second tab. A
// genuine re-render (a Revise branch) has different bytes and does re-open.
function statePath(sessionId) {
  const safe = String(sessionId || 'nosession').replace(/[^A-Za-z0-9._-]/g, '_').slice(0, 80);
  return path.join(os.tmpdir(), `reqgen-open-${safe}.json`);
}

function readState(file) {
  try {
    const raw = fs.readFileSync(file, 'utf8');
    const obj = JSON.parse(raw);
    return obj && typeof obj === 'object' && !Array.isArray(obj) ? obj : {};
  } catch {
    return {};
  }
}

function writeState(file, state) {
  try {
    fs.writeFileSync(file, JSON.stringify(state), 'utf8');
  } catch {
    // Losing the dedupe record only risks a duplicate tab. Never fatal.
  }
}

function sha256(absPath) {
  return crypto.createHash('sha256').update(fs.readFileSync(absPath)).digest('hex');
}

// ── Launch ─────────────────────────────────────────────────────────────────
// Detached + unref + stdio:'ignore' so this process exits immediately and never
// approaches the hook's 5s budget while the browser starts up.
//
// win32 uses rundll32 rather than `cmd /c start "" "<path>"`: no shell, so no
// quoting or metacharacter hazard, and pathToFileURL percent-encodes spaces.
function launch(absPath) {
  let cmd;
  let args;
  if (process.platform === 'win32') {
    cmd = 'rundll32.exe';
    args = ['url.dll,FileProtocolHandler', pathToFileURL(absPath).href];
  } else if (process.platform === 'darwin') {
    cmd = 'open';
    args = [absPath];
  } else {
    cmd = 'xdg-open';
    args = [absPath];
  }
  const child = spawn(cmd, args, { detached: true, stdio: 'ignore', windowsHide: true });
  child.on('error', () => {}); // no handler → an ENOENT would throw async
  child.unref();
}

// ── Dry-run ────────────────────────────────────────────────────────────────
// Allowlist-only check: reports the routing decision without touching disk or
// launching anything, so the patterns are testable without spawning tabs.
function dryRun(paths) {
  for (const p of paths) {
    const rel = String(p).replace(/\\/g, '/').replace(/^\.\//, '');
    if (isAllowed(rel)) process.stdout.write(`OPEN ${rel}\n`);
    else process.stdout.write(`SKIP ${rel} (not in allowlist)\n`);
  }
}

function readStdin() {
  try {
    return fs.readFileSync(0, 'utf8');
  } catch {
    return '';
  }
}

function main() {
  const argv = process.argv.slice(2);
  if (argv[0] === '--dry-run') {
    dryRun(argv.slice(1));
    process.exit(0);
  }

  if (optedOut()) process.exit(0);

  const raw = readStdin();
  if (!raw.trim()) process.exit(0);

  let payload;
  try {
    payload = JSON.parse(raw);
  } catch {
    process.exit(0); // malformed payload — never break the session
  }

  const input = payload.tool_input || {};
  let filePath = input.file_path;
  if (!filePath || typeof filePath !== 'string') process.exit(0);

  const cwd = payload.cwd || process.cwd();
  if (!path.isAbsolute(filePath)) filePath = path.resolve(cwd, filePath);

  const rel = toRel(filePath, cwd);
  if (!isAllowed(rel)) process.exit(0);

  let stat;
  try {
    stat = fs.statSync(filePath);
  } catch {
    process.exit(0); // Write may have failed — nothing to open
  }
  if (!stat.isFile() || stat.size < MIN_BYTES) process.exit(0);

  let hash;
  try {
    hash = sha256(filePath);
  } catch {
    process.exit(0);
  }

  const stateFile = statePath(payload.session_id);
  const state = readState(stateFile);
  if (state[rel] === hash) process.exit(0); // already opened this exact content
  state[rel] = hash;
  writeState(stateFile, state);

  launch(filePath);
  process.stderr.write(`open-artifact: opened ${rel}\n`);
  process.exit(0);
}

try {
  main();
} catch {
  process.exit(0); // fail open
}
