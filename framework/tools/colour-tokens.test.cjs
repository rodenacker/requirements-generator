'use strict';
// Unit tests for colour-tokens.cjs. Run: node --test framework/tools/colour-tokens.test.cjs
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { spawnSync } = require('node:child_process');

const ct = require('./colour-tokens.cjs');
const { hexToOklch, oklchToHex, contrast, isReserved, assign, derive, NEUTRAL_C, HOUSE_STATUS } = ct;

const hueDist = (a, b) => { const d = Math.abs(a - b) % 360; return d > 180 ? 360 - d : d; };

// Design *Evidence* table (absa.co.za spike, 2026-10-26).
const ABSA = () => ({
  candidates: [
    { hex: '#CA2B3D', weight: 508 },
    { hex: '#95052A', weight: 80 },
    { hex: '#AF144B', weight: 63 },
    { hex: '#77021E', weight: 8 },
    { hex: '#FA551E', weight: 7 },
    { hex: '#0074A6', weight: 7 },
  ],
  picks: { primary: '#FA551E', secondary: '#CA2B3D', accent: '#AF144B' },
  neutrals: { background: '#FFFFFF', surface: '#F4F3F3', text: '#2D2323', text_muted: '#524A4A' },
  mode: 'light',
});

const ORANGE_CTA_BLUE_BRAND = () => ({
  candidates: [{ hex: '#1D4ED8', weight: 400 }, { hex: '#F97316', weight: 30 }],
  picks: { primary: '#F97316', secondary: null, accent: null },
  neutrals: ABSA().neutrals,
  mode: 'light',
});

function absaOption1Light() {
  const out = assign(ABSA());
  return { ...ABSA().neutrals, ...out.roles, brand: out.brand, ...out.status };
}

const CHROMATIC_FILLS = ['primary', 'secondary', 'accent', 'success', 'warning', 'error', 'info'];

test('test_oklch_roundtrip', () => {
  for (const x of ['#CA2B3D', '#0074A6', '#FFFFFF', '#000000']) {
    assert.equal(oklchToHex(hexToOklch(x)), x);
  }
});

test('test_reserved_absa', () => {
  for (const x of ['#CA2B3D', '#95052A', '#AF144B', '#77021E', '#FA551E']) assert.equal(isReserved(x), true, x);
  for (const x of ['#0074A6', '#2D2323', '#524A4A']) assert.equal(isReserved(x), false, x);
});

test('test_contrast_known', () => {
  assert.ok(Math.abs(contrast('#FFFFFF', '#000000') - 21) <= 0.01);
  assert.ok(contrast('#FA551E', '#F4F3F3') < 3.0);
});

test('test_assign_absa', () => {
  const out = assign(ABSA());
  assert.equal(out.brand, '#CA2B3D');
  const p = hexToOklch(out.roles.primary);
  assert.ok(p.C < NEUTRAL_C, `primary C ${p.C}`);
  assert.ok(hueDist(p.H, hexToOklch('#CA2B3D').H) < 3, `primary H ${p.H}`);
  for (const k of ['primary', 'secondary', 'accent']) assert.equal(isReserved(out.roles[k]), false, k);
  assert.ok(out.options);
  assert.equal(out.options.site_colour.primary, '#0074A6');
  assert.ok(out.decisions.some((d) => d.includes('#FA551E')));
});

// absa.co.za re-captured 2026-10-27: the blue is only on hidden menu items, so
// step-04 passes it as a hidden-only candidate with weight 0.
test('test_assign_hidden_only_colour_offers_option', () => {
  const input = ABSA();
  input.candidates.find((c) => c.hex === '#0074A6').weight = 0;
  const out = assign(input);
  assert.ok(out.options);
  assert.equal(out.options.site_colour.primary, '#0074A6');
  assert.notEqual(out.roles.primary, '#0074A6');
});

test('test_assign_orange_cta_blue_brand', () => {
  const out = assign(ORANGE_CTA_BLUE_BRAND());
  assert.equal(out.roles.primary, '#1D4ED8');
  assert.equal(out.brand, '#1D4ED8');
  assert.equal(out.options, null);
});

test('test_assign_single_colour_brand_no_rotation', () => {
  const out = assign({
    candidates: [{ hex: '#1D4ED8', weight: 400 }],
    picks: { primary: '#1D4ED8', secondary: null, accent: null },
    neutrals: ABSA().neutrals,
    mode: 'light',
  });
  const bh = hexToOklch('#1D4ED8').H;
  for (const k of ['secondary', 'accent']) {
    const o = hexToOklch(out.roles[k]);
    assert.ok(o.C < 0.07, `${k} C ${o.C}`);
    assert.ok(hueDist(o.H, bh) < 3, `${k} H ${o.H}`);
  }
});

test('test_assign_no_area_data', () => {
  const input = ABSA();
  for (const c of input.candidates) c.weight = null;
  const out = assign(input);
  assert.equal(out.brand, '#FA551E');
  for (const k of ['primary', 'secondary', 'accent']) assert.equal(isReserved(out.roles[k]), false, k);
});

test('test_derive_light_to_dark_absa', () => {
  const out = derive({ source_mode: 'light', colours: absaOption1Light() });
  assert.equal(out.mode, 'dark');
  assert.equal(out.colours.brand, '#CA2B3D');
  assert.ok(hexToOklch(out.colours.primary).L >= 0.85);
  for (const [k, v] of Object.entries(out.fills)) assert.ok(v >= 3.0, `fill ${k} ${v}`);
  for (const [k, v] of Object.entries(out.contrast)) assert.ok(v >= 4.5, `pair ${k} ${v}`);
  for (const [k, on] of Object.entries(out.on_colours)) {
    const ok = contrast(on, out.colours[k]) >= 4.5 || out.adjustments.some((a) => a.startsWith(k));
    assert.ok(ok, `on-colour ${k}`);
  }
});

test('test_derive_min_change_keeps_passing_fill', () => {
  const out = derive({ source_mode: 'light', colours: { ...absaOption1Light(), info: '#3B82F6' } });
  assert.equal(out.colours.info, '#3B82F6');
});

test('test_derive_preserves_hue_chroma', () => {
  const src = absaOption1Light();
  const out = derive({ source_mode: 'light', colours: src });
  for (const k of CHROMATIC_FILLS) {
    const a = hexToOklch(src[k]);
    if (a.C < NEUTRAL_C) continue;
    const b = hexToOklch(out.colours[k]);
    assert.ok(hueDist(a.H, b.H) <= 2, `${k} H ${a.H} -> ${b.H}`);
    assert.ok(b.C <= a.C + 0.005, `${k} C ${a.C} -> ${b.C}`);
  }
});

test('test_derive_dark_to_light_neutral_flip', () => {
  const darkSrc = {
    background: oklchToHex({ L: 0.17, C: 0.012, H: 20 }),
    surface: oklchToHex({ L: 0.22, C: 0.014, H: 20 }),
    text: oklchToHex({ L: 0.95, C: 0.008, H: 20 }),
    text_muted: oklchToHex({ L: 0.75, C: 0.01, H: 20 }),
    primary: oklchToHex({ L: 0.90, C: 0.012, H: 20 }),
    secondary: oklchToHex({ L: 0.36, C: 0.012, H: 20 }),
    accent: '#60A5FA',
    brand: '#CA2B3D',
    success: '#4ADE80', warning: '#FBBF24', error: '#F87171', info: '#38BDF8',
  };
  const out = derive({ source_mode: 'dark', colours: darkSrc });
  assert.equal(out.mode, 'light');
  assert.ok(Math.abs(hexToOklch(out.colours.primary).L - 0.30) <= 0.01);
});

test('test_assign_no_candidates', () => {
  const out = assign({
    candidates: [],
    picks: { primary: '#DC2626', secondary: null, accent: null },
    neutrals: ABSA().neutrals,
    mode: 'light',
  });
  assert.equal(out.brand, '#DC2626');
  assert.ok(hexToOklch(out.roles.primary).C < NEUTRAL_C);
  assert.equal(out.options, null);
});

test('test_assign_error_clear_of_brand_and_warning', () => {
  const out = assign(ABSA());
  const e = hexToOklch(out.status.error);
  assert.ok(hueDist(e.H, hexToOklch(out.status.warning).H) >= 15, `error H ${e.H} too close to warning`);
  assert.ok(hueDist(e.H, hexToOklch(out.brand).H) >= 8 || Math.abs(e.L - hexToOklch(out.brand).L) >= 0.08, 'error not distinct from brand');
});

test('test_assign_dark_surface_neutral_roles_visible', () => {
  const out = assign({
    candidates: [{ hex: '#E11D48', weight: 400 }],
    picks: { primary: '#E11D48', secondary: null, accent: null },
    neutrals: { background: '#0E0E12', surface: '#16161C', text: '#F2F2F5', text_muted: '#A0A0AA' },
    mode: 'dark',
  });
  const p = hexToOklch(out.roles.primary);
  assert.ok(p.L >= 0.85, `dark-surface neutral primary L ${p.L}`);
  assert.ok(contrast(out.roles.primary, '#16161C') >= 3.0);
  assert.ok(contrast(out.roles.accent, '#16161C') >= 3.0, `accent ${out.roles.accent}`);
  for (const k of ['primary', 'secondary', 'accent']) assert.equal(isReserved(out.roles[k]), false, k);
});

test('test_assign_brand_ignores_pale_tint', () => {
  const out = assign({
    candidates: [{ hex: '#FFF4E5', weight: 600 }, { hex: '#CA2B3D', weight: 120 }],
    picks: { primary: '#CA2B3D', secondary: null, accent: null },
    neutrals: ABSA().neutrals,
    mode: 'light',
  });
  assert.equal(out.brand, '#CA2B3D');
});

test('test_assign_house_status', () => {
  const out = assign(ORANGE_CTA_BLUE_BRAND());
  assert.deepEqual(out.status, HOUSE_STATUS);
});

test('test_measure_keeps_passing_text', () => {
  const src = absaOption1Light();
  const out = ct.measure({ mode: 'light', colours: src });
  assert.equal(out.mode, 'light');
  assert.deepEqual(out.colours, src);
  assert.deepEqual(Object.keys(out.on_colours).sort(), ['accent', 'brand', 'error', 'info', 'primary', 'secondary', 'success', 'warning']);
  for (const v of Object.values(out.contrast)) assert.ok(v >= 4.5);
  assert.ok(out.fills.primary >= 3.0);
});

test('test_measure_adjusts_failing_text_light', () => {
  const src = { ...absaOption1Light(), text_muted: '#A89A9A' };
  const out = ct.measure({ mode: 'light', colours: src });
  assert.ok(out.contrast.text_muted_background >= 4.5 && out.contrast.text_muted_surface >= 4.5);
  const a = hexToOklch('#A89A9A'), b = hexToOklch(out.colours.text_muted);
  assert.ok(b.L < a.L);
  assert.ok(hueDist(a.H, b.H) <= 3);
  assert.ok(out.adjustments.some((l) => l.startsWith('text_muted')));
});

test('test_measure_adjusts_failing_text_dark', () => {
  const src = { ...absaOption1Light(), background: '#121212', surface: '#1E1E1E', text: '#6A6A6A', text_muted: '#5A5A5A' };
  const out = ct.measure({ mode: 'dark', colours: src });
  for (const v of Object.values(out.contrast)) assert.ok(v >= 4.5);
  assert.ok(hexToOklch(out.colours.text).L > hexToOklch('#6A6A6A').L);
  assert.equal(out.colours.background, '#121212');
});

test('test_cli_measure', () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'colour-tokens-'));
  const inPath = path.join(dir, 'in.json');
  const outPath = path.join(dir, 'out.json');
  fs.writeFileSync(inPath, JSON.stringify({ mode: 'light', colours: absaOption1Light() }));
  const r = spawnSync(process.execPath, [path.join(__dirname, 'colour-tokens.cjs'), 'measure', '--in', inPath, '--out', outPath], { encoding: 'utf8' });
  assert.equal(r.status, 0, r.stderr);
  assert.ok(JSON.parse(fs.readFileSync(outPath, 'utf8')).on_colours.primary);
});

test('test_cli_bad_input', () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'colour-tokens-'));
  const inPath = path.join(dir, 'in.json');
  fs.writeFileSync(inPath, '{}');
  const r = spawnSync(process.execPath, [path.join(__dirname, 'colour-tokens.cjs'), 'assign', '--in', inPath, '--out', path.join(dir, 'out.json')], { encoding: 'utf8' });
  assert.equal(r.status, 2);
  assert.ok(r.stderr.trim().length > 0);
});

// ---------- domain removal: declared brand, monochrome brands, neutral gap-fill ----------

const NULL_NEUTRALS = () => ({ background: null, surface: null, text: null, text_muted: null });
const BLUE_BRAND_NO_NEUTRALS = () => ({
  candidates: [{ hex: '#1D4ED8', weight: 400 }],
  picks: { primary: '#1D4ED8', secondary: null, accent: null },
  neutrals: NULL_NEUTRALS(),
  mode: 'light',
});

test('test_assign_declared_brand_wins', () => {
  const input = ABSA();
  input.picks.brand = '#95052A';
  const out = assign(input);
  assert.equal(out.brand, '#95052A');
  for (const k of ['primary', 'secondary', 'accent']) assert.equal(isReserved(out.roles[k]), false, k);
});

test('test_assign_monochrome', () => {
  const out = assign({
    candidates: [{ hex: '#111111', weight: 300 }, { hex: '#777777', weight: 20 }],
    picks: { primary: '#111111', secondary: null, accent: null },
    neutrals: NULL_NEUTRALS(),
    mode: 'light',
  });
  assert.equal(out.monochrome, true);
  assert.equal(out.brand, '#111111');
  for (const k of ['primary', 'secondary', 'accent']) assert.ok(hexToOklch(out.roles[k]).C < 0.005, `${k} ${out.roles[k]}`);
  for (const [k, v] of Object.entries(out.neutrals)) assert.ok(hexToOklch(v).C < 0.005, `${k} ${v}`);
});

test('test_on_colours_monochrome_brand_pure_grey', () => {
  const on = ct.onColours({ ...absaOption1Light(), brand: '#111111' }, 'light');
  for (const [k, v] of Object.entries(on)) assert.ok(hexToOklch(v).C < 0.005, `${k} ${v}`);
});

test('test_assign_neutral_gapfill_light', () => {
  const out = assign(BLUE_BRAND_NO_NEUTRALS());
  assert.deepEqual([...out.filled].sort(), ['background', 'surface', 'text', 'text_muted']);
  assert.ok(hexToOklch(out.neutrals.background).L >= 0.98);
  assert.ok(contrast(out.neutrals.text, out.neutrals.surface) >= 4.5);
  assert.ok(contrast(out.neutrals.text_muted, out.neutrals.surface) >= 4.5);
});

test('test_assign_neutral_gapfill_keeps_given', () => {
  const input = BLUE_BRAND_NO_NEUTRALS();
  input.neutrals.background = '#0D1117';
  input.neutrals.text = '#E6EDF3';
  input.mode = 'dark';
  const out = assign(input);
  assert.equal(out.neutrals.background, '#0D1117');
  assert.equal(out.neutrals.text, '#E6EDF3');
  assert.deepEqual(out.filled, ['surface', 'text_muted']);
  assert.ok(hexToOklch(out.neutrals.surface).L < 0.5);
  assert.ok(contrast(out.neutrals.text_muted, out.neutrals.surface) >= 4.5);
});

test('test_neutral_ladder_matches_derive', () => {
  const ladder = ct.neutralLadder('#CA2B3D', 'dark');
  const d = derive({ source_mode: 'light', colours: absaOption1Light() }).colours;
  for (const k of ['background', 'surface', 'text']) assert.equal(ladder[k], d[k], k);
});

test('test_assign_requires_mode', () => {
  const input = ABSA();
  delete input.mode;
  assert.throws(() => assign(input), TypeError);
});

test('test_assign_achromatic_brand_chromatic_palette_no_invented_hue', () => {
  for (const mode of ['light', 'dark']) {
    const dark = mode === 'dark';
    const out = assign({
      candidates: [{ hex: '#1D4ED8', weight: 400 }],
      picks: { primary: '#1D4ED8', secondary: null, accent: null, brand: '#000000' },
      neutrals: dark
        ? { background: '#0E0E12', surface: '#16161C', text: '#F2F2F5', text_muted: '#A0A0AA' }
        : ABSA().neutrals,
      mode,
    });
    assert.equal(out.monochrome, false);
    for (const k of ['secondary', 'accent']) assert.ok(hexToOklch(out.roles[k]).C < 0.005, `${mode} ${k} ${out.roles[k]}`);
  }
});

