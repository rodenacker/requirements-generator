'use strict';
// Unit tests for enumerate-inputs.cjs. Run: node --test framework/tools/enumerate-inputs.test.cjs
const test = require('node:test');
const assert = require('node:assert/strict');

const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');

const { enumerate } = require('./enumerate-inputs.cjs');

function tree(files) {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'enum-inputs-'));
  for (const [rel, body] of Object.entries(files)) {
    const p = path.join(root, ...rel.split('/'));
    fs.mkdirSync(path.dirname(p), { recursive: true });
    if (body !== null) fs.writeFileSync(p, body);
  }
  return root;
}
const rels = (r) => r.files.map((f) => f.relpath);

test('walks every depth, forward slashes, ordinal relpath order', () => {
  const root = tree({ 'b.md': 'b', 'pricing/deep/rules.md': 'r', 'pricing/workshop-notes.md': 'w', 'A.md': 'a' });
  assert.deepEqual(rels(enumerate(root)), ['A.md', 'b.md', 'pricing/deep/rules.md', 'pricing/workshop-notes.md']);
});

test('IX-01: dotfiles and every path under a dot-directory are absent', () => {
  const root = tree({ 'keep.md': 'k', '.secret.md': 's', '.scratch/x.md': 'x', 'topic/.obsidian/cfg.md': 'c' });
  assert.deepEqual(rels(enumerate(root)), ['keep.md']);
});

test('IX-02: *.converted.md siblings are absent at any depth', () => {
  const root = tree({ 'a.png': 'p', 'a.png.converted.md': 'd', 'x/b.docx': 'o', 'x/b.converted.md': 'd' });
  assert.deepEqual(rels(enumerate(root)), ['a.png', 'x/b.docx']);
});

test('IX-03: each signature leg makes a pruned unit at any depth', () => {
  const root = tree({
    'apps/One/administration.db': '',
    'apps/One/ClientApp/x.js': 'js',
    'deep/er/Two/App_Data/Updates/v1.sapz': 'z',
    'deep/er/Two/notes.md': 'n',
    'Three/ClientApp/y.js': 'js',
    'ptr.stadium': 'C:/apps/Four',
    'topic/ptr2.stadium': 'C:/apps/Five',
    'brief.md': 'b',
  });
  const r = enumerate(root);
  assert.deepEqual(rels(r), ['brief.md']);
  assert.deepEqual(r.stadium_units, [
    { relpath: 'Three', kind: 'folder' },
    { relpath: 'apps/One', kind: 'folder' },
    { relpath: 'deep/er/Two', kind: 'folder' },
    { relpath: 'ptr.stadium', kind: 'pointer' },
    { relpath: 'topic/ptr2.stadium', kind: 'pointer' },
  ]);
});

test('IX-04: only top-level *.stadium-assets/embedded/** is absent', () => {
  const root = tree({
    'App.stadium-assets/App.stadium.overview.md': 'o',
    'App.stadium-assets/embedded/logo.png': 'l',
    'topic/embedded/photo.png': 'p',
  });
  assert.deepEqual(rels(enumerate(root)), ['App.stadium-assets/App.stadium.overview.md', 'topic/embedded/photo.png']);
});

test('media directories are enumerated; their marker and descriptions are not', () => {
  const root = tree({
    'decks/review.docx': 'd',
    'decks/review.docx.media/img-ab12cd34.png': 'i',
    'decks/review.docx.media/img-ab12cd34.png.converted.md': 'x',
    'decks/review.docx.media/.extracted-by-framework': 'm',
  });
  assert.deepEqual(rels(enumerate(root)), ['decks/review.docx', 'decks/review.docx.media/img-ab12cd34.png']);
});

test('each file carries its sha256 and an ISO mtime', () => {
  const root = tree({ 'a.md': 'hello' });
  const [f] = enumerate(root).files;
  assert.equal(f.sha256, '2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824');
  assert.match(f.mtime, /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z$/);
});

test('no result cap: 250 nested files are all listed', () => {
  const files = {};
  for (let i = 0; i < 250; i++) files[`t${i % 5}/f${String(i).padStart(3, '0')}.md`] = String(i);
  assert.equal(enumerate(tree(files)).files.length, 250);
});
