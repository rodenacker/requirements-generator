'use strict';
// Unit tests for font-embed.cjs. Run: node --test framework/tools/font-embed.test.cjs
const test = require('node:test');
const assert = require('node:assert/strict');

const fe = require('./font-embed.cjs');
const { candidates, familyFromFontFile } = fe;

// ---------- Task 1: names ----------

test('test_candidates_per_weight_family_name', () => {
  const semi = candidates('SourceSansPro-SemiBold');
  assert.equal(semi.candidates[0], 'Source Sans Pro');
  assert.equal(semi.weight, 600);
  const reg = candidates('SourceSansPro-Regular');
  assert.equal(reg.candidates[0], 'Source Sans Pro');
  assert.equal(reg.weight, 400);
});

test('test_candidates_keeps_section2_behaviour', () => {
  const geist = candidates('GeistSans').candidates;
  assert.equal(geist[0], 'Geist Sans');
  assert.equal(geist[geist.length - 1], 'Geist');
  assert.equal(candidates('Public Sans').candidates[0], 'Public Sans');
  assert.equal(candidates('"Inter"').candidates[0], 'Inter');
  assert.equal(candidates('Inter-Variable').candidates[0], 'Inter');
  assert.equal(candidates('sohne-var').candidates[0], 'Sohne');
  assert.equal(candidates('ibm-plex-sans').candidates[0], 'IBM Plex Sans');
  assert.equal(candidates('Nunito Sans').candidates[0], 'Nunito Sans');
});

test('test_candidates_real_sites', () => {
  const benton = candidates('Benton-Sans-Regular');
  assert.equal(benton.candidates[0], 'Benton Sans');
  assert.equal(benton.weight, 400);
  assert.equal(candidates('72 Brand Variable').candidates[0], '72 Brand');
  assert.deepEqual(candidates('SiemensSans').candidates, ['Siemens Sans', 'Siemens']);
  const gotham = candidates('Gotham-BoldItalic');
  assert.equal(gotham.candidates[0], 'Gotham');
  assert.equal(gotham.weight, 700);
  assert.equal(gotham.italic, true);
});

test('test_family_from_font_file', () => {
  assert.deepEqual(
    familyFromFontFile('https://www.standardbank.co.za/x/LibreFranklin-Regular.ttf'),
    { family: 'Libre Franklin', weight: 400 },
  );
  assert.deepEqual(
    familyFromFontFile('https://www.absa.co.za/x/SourceSansPro-SemiBold.woff?v=2'),
    { family: 'Source Sans Pro', weight: 600 },
  );
  const siemens = familyFromFontFile('https://www.siemens.com/_astro/SiemensSans_Prof_Roman-WMJYQJZL.DBnmR-HK.woff2');
  assert.equal(siemens.family, 'Siemens Sans Prof');
  assert.equal(siemens.weight, 400);
  assert.equal(familyFromFontFile('data:font/woff2;base64,AAAA'), null);
});

test('test_candidates_rejects_bad_input', () => {
  assert.throws(() => candidates(''), TypeError);
  assert.throws(() => candidates(null), TypeError);
});
