'use strict';
// Unit tests for font-embed.cjs. Run: node --test framework/tools/font-embed.test.cjs
const test = require('node:test');
const assert = require('node:assert/strict');

const fs = require('node:fs');
const path = require('node:path');

const fe = require('./font-embed.cjs');
const { candidates, familyFromFontFile, resolveAll, buildFaces } = fe;

const FIXTURES = path.join(__dirname, '__fixtures__', 'fonts');
const INTER_CSS = fs.readFileSync(path.join(FIXTURES, 'inter.css'), 'utf8');
const LATO_CSS = fs.readFileSync(path.join(FIXTURES, 'lato.css'), 'utf8');

// routes: [[urlSubstring, response]] — first match wins. A response is
// { status, text } | { status, bytes } | 'throw' | (url) => response.
// Unmatched URLs answer 404. `calls` records every requested URL.
function fakeFetch(routes) {
  const calls = [];
  const fn = async (url, opts) => {
    calls.push({ url, opts });
    const hit = routes.find(([key]) => url.includes(key));
    let res = hit ? hit[1] : { status: 404, text: '' };
    if (typeof res === 'function') res = res(url);
    if (res === 'throw') throw new Error('network down');
    return {
      ok: res.status >= 200 && res.status < 300,
      status: res.status,
      text: async () => res.text ?? '',
      arrayBuffer: async () => {
        const b = res.bytes ?? Buffer.alloc(0);
        return b.buffer.slice(b.byteOffset, b.byteOffset + b.byteLength);
      },
    };
  };
  fn.calls = calls;
  return fn;
}

const blocks = (css) => (css.match(/@font-face/g) || []).length;

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

// ---------- Task 2: probe and embedding ----------

test('test_resolve_first_candidate_200', async () => {
  const fetch = fakeFetch([['family=Source+Sans+Pro', { status: 200 }], ['', { status: 400 }]]);
  const [r] = await resolveAll(['SourceSansPro-SemiBold'], { fetch });
  assert.equal(r.verdict, 'google-native');
  assert.equal(r.family, 'Source Sans Pro');
  assert.equal(r.weight, 600);
  assert.ok(!fetch.calls.some((c) => c.url.endsWith('family=Inter')), 'no control call');
});

test('test_resolve_unavailable', async () => {
  const fetch = fakeFetch([['family=Inter', { status: 200 }], ['', { status: 400 }]]);
  const [r] = await resolveAll(['SiemensSans'], { fetch });
  assert.equal(r.verdict, 'unavailable');
  assert.equal(r.family, null);
  assert.deepEqual(r.tried.map((t) => t.status), [400, 400]);
});

test('test_resolve_unknown_when_control_fails', async () => {
  const fetch = fakeFetch([['', 'throw']]);
  const [r] = await resolveAll(['SiemensSans'], { fetch });
  assert.equal(r.verdict, 'unknown');
  assert.equal(r.family, null);
  assert.ok(r.tried.every((t) => t.status === 'error'));
});

test('test_resolve_request_ceiling', async () => {
  const fetch = fakeFetch([['family=Inter', { status: 200 }], ['', { status: 400 }]]);
  const out = await resolveAll(['SiemensSans', 'BentonSans'], { fetch });
  assert.ok(fetch.calls.length <= 5, `${fetch.calls.length} requests`);
  assert.equal(fetch.calls.filter((c) => c.url.endsWith('family=Inter')).length, 1);
  assert.equal(out.length, 2);
});

const GSTATIC_1000 = ['fonts.gstatic.com', { status: 200, bytes: Buffer.alloc(1000, 7) }];

test('test_build_faces_keeps_latin_subsets', async () => {
  const fetch = fakeFetch([GSTATIC_1000, ['family=Inter', { status: 200, text: INTER_CSS }]]);
  const r = await buildFaces(['Inter'], { fetch });
  assert.deepEqual(r.embedded, ['Inter']);
  assert.deepEqual(r.failed, []);
  assert.equal(blocks(r.css), 8);
  assert.ok(!r.css.includes('fonts.gstatic.com'));
  const srcs = r.css.match(/src:.*/g);
  assert.equal(srcs.length, 8);
  assert.ok(srcs.every((s) => s.startsWith("src: url(data:font/woff2;base64,")));
  assert.equal(fetch.calls.filter((c) => c.url.includes('fonts.gstatic.com')).length, 2);
  assert.equal(r.bytes, 2000);
  const cssCall = fetch.calls.find((c) => c.url.includes('family=Inter'));
  assert.equal(cssCall.url, fe.GOOGLE_CSS + 'Inter' + fe.WEIGHTS);
  assert.equal(cssCall.opts.headers['User-Agent'], fe.UA);
});

test('test_build_faces_static_family_partial_weights', async () => {
  const fetch = fakeFetch([GSTATIC_1000, ['family=Lato', { status: 200, text: LATO_CSS }]]);
  const r = await buildFaces(['Lato'], { fetch });
  assert.equal(blocks(r.css), 4);
  assert.deepEqual(r.failed, []);
  assert.deepEqual(r.embedded, ['Lato']);
});

test('test_build_faces_dedupes_params', async () => {
  const fetch = fakeFetch([GSTATIC_1000, ['family=Inter', { status: 200, text: INTER_CSS }]]);
  const r = await buildFaces(['Inter', 'Inter'], { fetch });
  assert.deepEqual(r.embedded, ['Inter']);
  assert.equal(fetch.calls.filter((c) => c.url.includes('family=Inter')).length, 1);
});

test('test_build_faces_network_failure', async () => {
  const fetch = fakeFetch([['family=Inter', 'throw']]);
  const r = await buildFaces(['Inter'], { fetch });
  assert.deepEqual(r.embedded, []);
  assert.deepEqual(r.failed, [{ param: 'Inter', reason: 'network' }]);
  assert.equal(r.css, '');
  assert.equal(r.bytes, 0);
});

test('test_build_faces_http_error', async () => {
  const fetch = fakeFetch([['family=Inter', { status: 400, text: '' }]]);
  const r = await buildFaces(['Inter'], { fetch });
  assert.deepEqual(r.failed, [{ param: 'Inter', reason: 'http 400' }]);
});

test('test_build_faces_budget', async () => {
  const fetch = fakeFetch([
    GSTATIC_1000,
    ['family=Inter', { status: 200, text: INTER_CSS }],
    ['family=Lato', { status: 200, text: LATO_CSS }],
  ]);
  const r = await buildFaces(['Inter', 'Lato'], { fetch, maxBytes: 3000 });
  assert.deepEqual(r.embedded, ['Inter']);
  assert.deepEqual(r.failed, [{ param: 'Lato', reason: 'budget' }]);
  assert.equal(r.bytes, 2000);
  assert.ok(!r.css.includes("'Lato'"));
});
