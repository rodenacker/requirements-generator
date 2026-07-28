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
 * On the hook path it writes nothing to stdout — there stdout is a control
 * channel, and a stray {"decision":"block"} would break the calling pipeline.
 * Progress goes to stderr. The CLI modes --dry-run and --selftest are the only
 * stdout writers; neither is ever reached from a hook invocation.
 *
 * Dry-run (allowlist testing, no browser):
 *   node framework/tools/open-artifact.cjs --dry-run <repo-relative-path> [...]
 *   → prints "OPEN <path>" or "SKIP <path> (<reason>)" per argument.
 *
 * Self-test (hook wiring / command form, no browser, no artefact touched):
 *   node framework/tools/open-artifact.cjs --selftest [--command "<string>"]
 *   → runs the registered PostToolUse:Write command(s) under every discoverable
 *     shell with a {"__selftest":true} payload on stdin and prints
 *     "PASS <shell>: <command>" or "FAIL <shell>: <diagnosis>".
 */

'use strict';

const fs = require('fs');
const os = require('os');
const path = require('path');
const crypto = require('crypto');
const { spawn, spawnSync } = require('child_process');
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

// ── Self-test ──────────────────────────────────────────────────────────────
// --dry-run reads argv, so it structurally cannot catch a broken *command
// string*: it never exercises the transport the harness actually uses. This
// mode does — it spawns the registered command the way a shell would and
// asserts the marker comes back on stderr.
//
// Why this exists: the helper fails open (every path exits 0), so a command
// string the shell mangled is indistinguishable from "nothing to open". The
// original bug was `cmd /c "…"`, which MSYS rewrites to `C:/` under Git Bash;
// cmd.exe then started interactively, ate the JSON payload from stdin, and
// exited 0 — recorded by the harness as hook_success with node never running.
const SELFTEST_MARKER = 'open-artifact: selftest ok';

const REPO_ROOT = path.resolve(__dirname, '..', '..');

// The command(s) the harness would actually run for a Write.
function registeredWriteCommands() {
  const settings = path.join(REPO_ROOT, '.claude', 'settings.json');
  let parsed;
  try {
    parsed = JSON.parse(fs.readFileSync(settings, 'utf8'));
  } catch (err) {
    return { error: `cannot read ${settings}: ${err.message}`, commands: [] };
  }
  const groups = (parsed.hooks && parsed.hooks.PostToolUse) || [];
  const commands = [];
  for (const group of groups) {
    if (!group || typeof group.matcher !== 'string' || !group.matcher.includes('Write')) continue;
    for (const hook of group.hooks || []) {
      if (hook && hook.type === 'command' && typeof hook.command === 'string') commands.push(hook.command);
    }
  }
  return { error: null, commands };
}

// Locate a POSIX bash. The harness resolves SHELL to Git Bash on this platform,
// so this is the shell that broke and the one the probe must cover.
//
// WindowsApps\bash.exe is excluded deliberately: it is the WSL App Execution
// Alias, not Git Bash. It applies no MSYS argument translation (so it would not
// reproduce the bug) and launching it can block on distro setup.
function findBash() {
  const fromEnv = process.env.SHELL;
  if (fromEnv && /(^|[\\/])(ba)?sh(\.exe)?$/i.test(fromEnv) && fs.existsSync(fromEnv)) return fromEnv;

  const candidates = [];
  if (process.platform === 'win32') {
    for (const root of [process.env.ProgramFiles, process.env['ProgramFiles(x86)'], process.env.ProgramW6432]) {
      if (root) candidates.push(path.join(root, 'Git', 'bin', 'bash.exe'), path.join(root, 'Git', 'usr', 'bin', 'bash.exe'));
    }
    // `where git` → <git>\cmd\git.exe, whose sibling <git>\bin\bash.exe is Git Bash.
    const git = spawnSync('where', ['git'], { encoding: 'utf8', windowsHide: true });
    for (const line of String(git.stdout || '').split(/\r?\n/)) {
      const exe = line.trim();
      if (exe) candidates.push(path.resolve(path.dirname(exe), '..', 'bin', 'bash.exe'));
    }
  } else {
    candidates.push('/bin/bash', '/usr/bin/bash');
  }

  const probe = spawnSync(process.platform === 'win32' ? 'where' : 'which', ['bash'], {
    encoding: 'utf8',
    windowsHide: true,
  });
  for (const line of String(probe.stdout || '').split(/\r?\n/)) {
    const exe = line.trim();
    if (exe && !/[\\/]WindowsApps[\\/]/i.test(exe)) candidates.push(exe);
  }

  return candidates.find((c) => {
    try {
      return fs.statSync(c).isFile();
    } catch {
      return false;
    }
  }) || null;
}

// The shells a hook command must survive. `sh` is listed first because it is
// the one that broke.
function discoverShells() {
  const shells = [];
  const bash = findBash();
  if (bash) shells.push({ label: 'sh', run: (cmd, opts) => spawnSync(bash, ['-c', cmd], opts) });
  shells.push({
    label: `default(${process.platform === 'win32' ? 'cmd' : 'sh'})`,
    run: (cmd, opts) => spawnSync(cmd, Object.assign({ shell: true }, opts)),
  });
  return shells;
}

function diagnose(result) {
  if (result.error) return `spawn failed: ${result.error.message}`;
  const err = String(result.stderr || '');
  const out = String(result.stdout || '');
  const both = `${out}\n${err}`;
  if (/Microsoft Windows \[Version/i.test(both)) {
    return 'cmd.exe started interactively and consumed the payload — the command string was mangled by the shell (exit 0, node never ran)';
  }
  if (/MODULE_NOT_FOUND|Cannot find module/i.test(both)) {
    return `node ran but could not resolve the script path — ${(both.match(/Cannot find module.*/) || ['see stderr'])[0]}`;
  }
  const firstLine = both.split(/\r?\n/).map((s) => s.trim()).filter(Boolean)[0] || '(no output)';
  return `marker absent (exit ${result.status}): ${firstLine}`;
}

function selfTest(argv) {
  let commands;
  const flagIndex = argv.indexOf('--command');
  if (flagIndex !== -1) {
    const override = argv[flagIndex + 1];
    if (typeof override !== 'string' || override === '') {
      process.stdout.write('FAIL --command requires a command string\n');
      return 1;
    }
    commands = [override];
  } else {
    const registered = registeredWriteCommands();
    if (registered.error) {
      process.stdout.write(`FAIL ${registered.error}\n`);
      return 1;
    }
    commands = registered.commands;
    if (commands.length === 0) {
      process.stdout.write('FAIL no PostToolUse hook with a Write matcher is registered in .claude/settings.json\n');
      return 1;
    }
  }

  if (optedOut()) {
    process.stdout.write(
      'NOTE REQGEN_NO_AUTO_OPEN is set in this environment; the child inherits it and will exit before the marker.\n'
    );
  }

  const payload = JSON.stringify({
    __selftest: true,
    session_id: 'selftest',
    cwd: REPO_ROOT,
    hook_event_name: 'PostToolUse',
    tool_name: 'Write',
    tool_input: { file_path: path.join(REPO_ROOT, 'analyse-inputs', 'SELFTEST', 'selftest.html') },
  });

  const shells = discoverShells();
  if (!shells.some((s) => s.label === 'sh')) {
    // Announced, never silent: an unprobed shell would make an all-PASS result
    // and a never-tested transport look identical — the same ambiguity the
    // fail-open design created in the first place.
    process.stdout.write('NOTE no bash found — the sh transport was NOT probed; a PASS below covers the platform default only.\n');
  }
  let failures = 0;
  for (const command of commands) {
    for (const shell of shells) {
      const result = shell.run(command, {
        input: payload,
        encoding: 'utf8',
        cwd: REPO_ROOT,
        windowsHide: true,
        timeout: 15000,
      });
      const ok = String(result.stderr || '').includes(SELFTEST_MARKER);
      if (ok) {
        process.stdout.write(`PASS ${shell.label}: ${command}\n`);
      } else {
        failures += 1;
        process.stdout.write(`FAIL ${shell.label}: ${diagnose(result)}\n`);
        process.stdout.write(`     command: ${command}\n`);
      }
    }
  }
  return failures === 0 ? 0 : 1;
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
  if (argv[0] === '--selftest') {
    process.exit(selfTest(argv.slice(1)));
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

  // Wiring probe (see --selftest). Answers "did this script actually receive
  // the payload?" and stops there: before the allowlist, statSync, hash and
  // launch(), so nothing is written, no browser opens, and no pipeline artefact
  // is touched. A real hook payload never carries this key.
  if (payload.__selftest === true) {
    process.stderr.write(`${SELFTEST_MARKER} (stdin bytes=${Buffer.byteLength(raw)}, cwd=${payload.cwd || process.cwd()})\n`);
    process.exit(0);
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
