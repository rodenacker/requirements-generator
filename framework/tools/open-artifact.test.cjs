'use strict';
// Unit tests for open-artifact.cjs's design-system open path. Run: node --test framework/tools/open-artifact.test.cjs
// No case launches a browser: openIfAllowed takes a stub launcher, and the hook
// case writes a file that still holds the font marker, which the hook skips.
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { spawnSync } = require('node:child_process');

const HELPER = path.join(__dirname, 'open-artifact.cjs');
const REPO_ROOT = path.resolve(__dirname, '..', '..');
const { openIfAllowed, FONT_MARKER } = require('./open-artifact.cjs');

test('test_open_if_allowed_opens_design_system_file', () => {
  const opened = [];
  const abs = path.join(REPO_ROOT, 'generated-docs', 'design-system', 'design-system-light.html');
  assert.equal(openIfAllowed(abs, { launcher: (p) => opened.push(p) }), 'generated-docs/design-system/design-system-light.html');
  assert.deepEqual(opened, [abs]);
});

test('test_open_if_allowed_skips_unlisted_path', () => {
  const opened = [];
  assert.equal(openIfAllowed(path.join(os.tmpdir(), 'ds.html'), { launcher: (p) => opened.push(p) }), null);
  assert.deepEqual(opened, []);
});

test('test_open_if_allowed_honours_opt_out', () => {
  const opened = [];
  process.env.REQGEN_NO_AUTO_OPEN = '1';
  try {
    const abs = path.join(REPO_ROOT, 'generated-docs', 'design-system', 'design-system-dark.html');
    assert.equal(openIfAllowed(abs, { launcher: (p) => opened.push(p) }), null);
  } finally {
    delete process.env.REQGEN_NO_AUTO_OPEN;
  }
  assert.deepEqual(opened, []);
});

test('test_hook_skips_file_with_unfilled_fonts', () => {
  const cwd = fs.mkdtempSync(path.join(os.tmpdir(), 'open-artifact-'));
  const file = path.join(cwd, 'generated-docs', 'design-system', 'design-system-light.html');
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, `<!doctype html><body>${'x'.repeat(600)}<style id="brand-font-faces">${FONT_MARKER}</style></body>`);
  const payload = JSON.stringify({ session_id: `test-${process.pid}`, cwd, tool_name: 'Write', tool_input: { file_path: file } });
  const r = spawnSync(process.execPath, [HELPER], { input: payload, encoding: 'utf8' });
  assert.equal(r.status, 0);
  assert.match(r.stderr, /opens when font-embed\.cjs inject fills/);
  assert.doesNotMatch(r.stderr, /opened/);
});
