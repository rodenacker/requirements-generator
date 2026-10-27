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
  assert.equal(blocks(r.css), 2); // one per subset: variable weights merged
  assert.ok(!r.css.includes('fonts.gstatic.com'));
  const srcs = r.css.match(/src:.*/g);
  assert.equal(srcs.length, 2);
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

// ---------- Task 3: inject, vendor, CLI ----------

const os = require('node:os');
const crypto = require('node:crypto');
const { spawnSync } = require('node:child_process');
const { inject, vendor } = fe;
const HELPER = path.join(__dirname, 'font-embed.cjs');

const PAGE_HEAD = '<!doctype html>\n<html><head><script type="application/json" id="design-tokens">{"meta":{"brand_fonts":{}}}</script></head>\n<body>\n<section id="standards">x</section>\n<style id="brand-font-faces">';
const PAGE_TAIL = '</style>\n</body>\n</html>\n';
const PAGE = PAGE_HEAD + fe.MARKER + PAGE_TAIL;

test('test_inject_only_touches_marker', () => {
  const css = "/* latin */\n@font-face { font-family: 'Inter'; src: url(data:font/woff2;base64,AAAA) format('woff2'); }";
  const out = inject(PAGE, css);
  assert.ok(out.startsWith(PAGE_HEAD));
  assert.ok(out.endsWith(PAGE_TAIL));
  assert.equal(out, PAGE_HEAD + css + PAGE_TAIL);
  assert.equal(out.split(css).length - 1, 1);
});

test('test_inject_empty_css', () => {
  const out = inject(PAGE, '');
  assert.ok(out.includes('/* no embedded brand fonts */'));
  assert.ok(!out.includes(fe.MARKER));
});

test('test_inject_rejects_filled_block', () => {
  assert.equal(typeof inject, 'function');
  assert.throws(() => inject(inject(PAGE, 'x'), 'y'), TypeError);
  assert.throws(() => inject('<!doctype html><body></body>', 'x'), TypeError);
  const two = PAGE_HEAD + fe.MARKER + '</style>\n<style id="brand-font-faces">' + fe.MARKER + PAGE_TAIL;
  assert.throws(() => inject(two, 'x'), TypeError);
});

test('test_vendor_round_trip', async () => {
  const sources = new Map();
  const fetch = fakeFetch([
    ['fonts.gstatic.com', (url) => {
      if (!sources.has(url)) sources.set(url, Buffer.alloc(1000, sources.size + 1));
      return { status: 200, bytes: sources.get(url) };
    }],
    ['family=Inter', { status: 200, text: INTER_CSS }],
  ]);
  const faces = await buildFaces(['Inter'], { fetch });
  const v = vendor(inject(PAGE, faces.css));
  assert.equal(v.files.length, 2);
  for (const f of v.files) assert.match(f.name, /^inter-(latin|latin-ext)-[0-9a-f]{8}\.woff2$/);
  const src = [...sources.values()].map((b) => b.toString('hex')).sort();
  assert.deepEqual(v.files.map((f) => f.bytes.toString('hex')).sort(), src);
  assert.equal((v.css.match(/url\(\/fonts\//g) || []).length, 2);
  assert.ok(!v.css.includes('data:'));
});

test('test_vendor_without_block', () => {
  assert.deepEqual(vendor('<!doctype html><p>x</p>'), { css: '', files: [] });
  assert.deepEqual(vendor(PAGE), { css: '', files: [] });
});

function tmpDir() {
  return fs.mkdtempSync(path.join(os.tmpdir(), 'font-embed-'));
}

test('test_cli_inject_reports_sha', () => {
  const dir = tmpDir();
  const h = path.join(dir, 'ds.html');
  const c = path.join(dir, 'faces.css');
  fs.writeFileSync(h, PAGE);
  fs.writeFileSync(c, "/* latin */\n@font-face { font-family: 'Inter'; }");
  const r = spawnSync(process.execPath, [HELPER, 'inject', '--html', h, '--css', c], { encoding: 'utf8' });
  assert.equal(r.status, 0, r.stderr);
  const out = JSON.parse(r.stdout);
  const disk = fs.readFileSync(h);
  assert.equal(out.sha256, crypto.createHash('sha256').update(disk).digest('hex'));
  assert.equal(out.bytes, disk.length);
  assert.ok(!disk.toString('utf8').includes(fe.MARKER));
  assert.equal(out.opened, null, 'a file outside the preview allowlist is never opened');
});

test('test_cli_bad_input', () => {
  const dir = tmpDir();
  const c = path.join(dir, 'faces.css');
  fs.writeFileSync(c, '');
  const r = spawnSync(process.execPath, [HELPER, 'inject', '--html', path.join(dir, 'missing.html'), '--css', c], { encoding: 'utf8' });
  assert.equal(r.status, 2);
  assert.equal(r.stderr.trim().split('\n').length, 1);
});

test('test_build_faces_merges_variable_weights', async () => {
  const fetch = fakeFetch([GSTATIC_1000, ['family=Inter', { status: 200, text: INTER_CSS }]]);
  const r = await buildFaces(['Inter'], { fetch });
  // A variable family serves one file per subset for every weight: one block each, a weight range, the data once.
  assert.equal(blocks(r.css), 2);
  assert.equal((r.css.match(/font-weight: 400 700;/g) || []).length, 2);
  assert.equal((r.css.match(/data:font\/woff2/g) || []).length, 2);
  assert.match(r.css, /\/\* latin \*\//);
  assert.match(r.css, /\/\* latin-ext \*\//);
});

test('test_candidates_strips_webfont_suffix', () => {
  // Standard Bank declares a Font Squirrel build name for its heading face.
  const r = candidates('bentonsans-extra-light-webfont');
  assert.equal(r.candidates[0], 'Benton Sans');
  assert.equal(r.weight, 200);
  assert.deepEqual(familyFromFontFile('https://x.example/fonts/gotham-bold-webfont.woff2'), { family: 'Gotham', weight: 700 });
});

test('test_candidates_splits_lowercase_glued_class_word', () => {
  // An all-lowercase name has no case boundary to split on, so a glued class word is split off.
  assert.equal(candidates('bentonsans').candidates[0], 'Benton Sans');
  assert.equal(candidates('opensans-bold').candidates[0], 'Open Sans');
  assert.equal(candidates('sourceserif').candidates[0], 'Source Serif');
  assert.equal(familyFromFontFile('https://x.example/f/robotomono-regular.woff2').family, 'Roboto Mono');
  // Guards: a stem under 3 letters, the bare class word, and mixed case stay as they are.
  assert.equal(candidates('sans').candidates[0], 'Sans');
  assert.equal(candidates('xsans').candidates[0], 'Xsans');
  assert.equal(candidates('Artisans').candidates[0], 'Artisans');
});
