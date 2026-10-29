'use strict';
// Guards for the /design-system assets step-06 emits verbatim: no `{{` in an
// emitted comment (step-06 §C fails on any literal `{{...}}`), one doctype
// literal, LF line endings. Run: node --test framework/tools/design-system-assets.test.cjs
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const root = path.join(__dirname, '..', '..');
const TEMPLATE = path.join(root, 'framework/assets/template-design-system.html');
const STANDARDS = path.join(root, 'framework/assets/design-system-standards.html');
const CATALOGUE = path.join(root, 'framework/agents/design-system-styler/data/component-catalogue.md');
const read = (p) => fs.readFileSync(p, 'utf8');

// Every /* … */ and <!-- … --> body in the text.
const comments = (text) => [...text.matchAll(/\/\*[\s\S]*?\*\/|<!--[\s\S]*?-->/g)].map((m) => m[0]);
const withPlaceholder = (text) => comments(text).filter((c) => c.includes('{{'));

test('test_template_has_exactly_one_doctype_literal', () => {
  assert.equal(read(TEMPLATE).match(/<!doctype html>/gi).length, 1);
});

test('test_no_placeholder_in_an_emitted_template_comment', () => {
  const t = read(TEMPLATE);
  const emitted = t.slice(t.search(/^<!doctype html>/im));
  assert.deepEqual(withPlaceholder(emitted), []);
});

test('test_standards_file_has_no_placeholder', () => {
  assert.ok(!read(STANDARDS).includes('{{'));
});

test('test_catalogue_css_block_comments_have_no_placeholder', () => {
  // The emitted block is the one under "## Component CSS"; earlier css fences are prose examples.
  const c = read(CATALOGUE);
  const block = c.slice(c.indexOf('## Component CSS')).match(/```css\r?\n([\s\S]*?)```/);
  assert.ok(block, 'no css block under ## Component CSS');
  assert.deepEqual(withPlaceholder(block[1]), []);
});

test('test_verbatim_emitted_assets_are_lf', () => {
  for (const p of [TEMPLATE, STANDARDS, CATALOGUE]) assert.ok(!read(p).includes('\r'), `${path.basename(p)} has CR`);
});
