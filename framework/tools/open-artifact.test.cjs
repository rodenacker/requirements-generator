'use strict';
// Unit tests for open-artifact.cjs's deferred open. Run: node --test framework/tools/open-artifact.test.cjs
// Every case passes --no-launch, so no browser opens.
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { spawn } = require('node:child_process');

const HELPER = path.join(__dirname, 'open-artifact.cjs');
const MARKER = '/* BRAND_FONT_FACES */';

function waiter(file, timeoutMs) {
  return new Promise((resolve) => {
    const child = spawn(process.execPath, [HELPER, '--open-when-filled', file, '--timeout-ms', String(timeoutMs), '--no-launch'], { stdio: ['ignore', 'ignore', 'pipe'] });
    let err = '';
    child.stderr.on('data', (d) => { err += d; });
    child.on('exit', (code) => resolve({ code, err }));
  });
}

function tmpFile(content) {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'open-artifact-'));
  const file = path.join(dir, 'design-system-light.html');
  fs.writeFileSync(file, content);
  return file;
}

test('test_open_when_filled_waits_for_inject', async () => {
  const file = tmpFile(`<!doctype html><body><style id="brand-font-faces">${MARKER}</style></body>`);
  setTimeout(() => fs.writeFileSync(file, '<!doctype html><body><style id="brand-font-faces">/* latin */</style></body>'), 400);
  const started = Date.now();
  const r = await waiter(file, 10000);
  assert.equal(r.code, 0);
  assert.match(r.err, /filled/);
  assert.ok(Date.now() - started < 8000, 'returned on fill, not on timeout');
});

test('test_open_when_filled_opens_anyway_on_timeout', async () => {
  const file = tmpFile(`<!doctype html><body><style id="brand-font-faces">${MARKER}</style></body>`);
  const r = await waiter(file, 600);
  assert.equal(r.code, 0);
  assert.match(r.err, /timeout/);
});
