#!/usr/bin/env node
/**
 * colour-tokens.cjs — deterministic colour maths for /design-system
 *
 * Purpose: turn the colours the styler extracted from a reference site into a
 * token set, without an LLM doing colour arithmetic. Two operations:
 *   assign — reserved-zone check, primary cascade, secondary/accent fallbacks,
 *            the two-option trigger, the `brand` identity colour and the house
 *            status set (with `error` moved away from a reserved brand hue).
 *   derive — the other colour mode from the hue-source set: minimum-change
 *            OKLCH lightness for fills, the neutral flip, the neutral ladder,
 *            measured on-colours and the contrast numbers.
 * The prompt files decide *what* the site uses (picks, area weights, the
 * site's own other scheme); this file decides *how* those become tokens.
 *
 * Callers: framework/agents/design-system-styler/steps/step-05b-domain-inference.md
 * (assign at the start of §C; derive + onColours in §D / §F). Policy prose:
 * framework/agents/design-system-styler/data/cross-mode-derivation-rules.md.
 * Never restate the constants below in prose — point here.
 *
 * Contract (CLI):
 *   node framework/tools/colour-tokens.cjs <assign|derive> --in <json> --out <json>
 *   exit 0 → output JSON written; exit 2 → one-line stderr message (bad input).
 *   Never throws an uncaught error.
 *
 * Self-contained: Node >= 18, no dependencies. Unit tests: colour-tokens.test.cjs.
 */
'use strict';

const fs = require('node:fs');

const RESERVED = { hueFrom: 345, hueTo: 95, minC: 0.07 };
const NEUTRAL_C = 0.04;
const USAGE_SHARE_MIN = 0.03;
const FILL_TARGET = 3.0;
const LABEL_TARGET = 4.5;
const TEXT_TARGET = 4.5;
// The fixed light-mode status set for internal data-management apps. Nothing
// infers status any more; this constant is its only definition.
const HOUSE_STATUS = { success: '#15803D', warning: '#B45309', error: '#B91C1C', info: '#0369A1' };

const COLOUR_KEYS = ['background', 'surface', 'text', 'text_muted', 'primary', 'secondary', 'accent', 'brand', 'success', 'warning', 'error', 'info'];
const FILL_KEYS = ['primary', 'secondary', 'accent', 'success', 'warning', 'error', 'info'];
const ON_KEYS = ['primary', 'secondary', 'accent', 'brand', 'success', 'warning', 'error', 'info'];
const STEP = 0.005;

// ---------- conversions (Björn Ottosson's OKLab) ----------

const HEX_RE = /^#[0-9A-Fa-f]{6}$/;
const isHex = (s) => typeof s === 'string' && HEX_RE.test(s);
const clamp01 = (x) => Math.min(1, Math.max(0, x));
const toLinear = (c) => (c <= 0.04045 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4));
const toGamma = (c) => (c <= 0.0031308 ? 12.92 * c : 1.055 * Math.pow(c, 1 / 2.4) - 0.055);

function hexToRgb(hex) {
  const n = parseInt(hex.slice(1), 16);
  return [(n >> 16) & 255, (n >> 8) & 255, n & 255].map((v) => v / 255);
}

function linearToOklab([r, g, b]) {
  const l = Math.cbrt(0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b);
  const m = Math.cbrt(0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b);
  const s = Math.cbrt(0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b);
  return [
    0.2104542553 * l + 0.793617785 * m - 0.0040720468 * s,
    1.9779984951 * l - 2.428592205 * m + 0.4505937099 * s,
    0.0259040371 * l + 0.7827717662 * m - 0.808675766 * s,
  ];
}

function oklabToLinear([L, a, b]) {
  const l = Math.pow(L + 0.3963377774 * a + 0.2158037573 * b, 3);
  const m = Math.pow(L - 0.1055613458 * a - 0.0638541728 * b, 3);
  const s = Math.pow(L - 0.0894841775 * a - 1.291485548 * b, 3);
  return [
    4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
    -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
    -0.0041960863 * l - 0.7034186147 * m + 1.707614701 * s,
  ];
}

function hexToOklch(hex) {
  const [L, a, b] = linearToOklab(hexToRgb(hex).map(toLinear));
  const C = Math.sqrt(a * a + b * b);
  let H = (Math.atan2(b, a) * 180) / Math.PI;
  if (H < 0) H += 360;
  return { L, C, H };
}

function oklchLinear({ L, C, H }) {
  const h = (H * Math.PI) / 180;
  return oklabToLinear([L, C * Math.cos(h), C * Math.sin(h)]);
}

const inGamut = (rgb) => rgb.every((c) => c >= -1e-6 && c <= 1 + 1e-6);

// Quantise to 8-bit: of the 8 floor/ceil neighbours, take the one closest in
// OKLab, with a/b weighted up so low-chroma tints keep their hue.
function linearToHex(rgb) {
  const target = linearToOklab(rgb.map(clamp01));
  const g = rgb.map((c) => clamp01(toGamma(clamp01(c))) * 255);
  let best = null, bestD = Infinity;
  for (let m = 0; m < 8; m++) {
    const q = g.map((v, i) => Math.min(255, (m >> i) & 1 ? Math.ceil(v) : Math.floor(v)));
    const lab = linearToOklab(q.map((v) => toLinear(v / 255)));
    const d = (lab[0] - target[0]) ** 2 + 4 * ((lab[1] - target[1]) ** 2 + (lab[2] - target[2]) ** 2);
    if (d < bestD) { bestD = d; best = q; }
  }
  return '#' + best.map((v) => v.toString(16).padStart(2, '0')).join('').toUpperCase();
}

// Gamut-mapped by reducing C (binary search); L and H are kept.
function oklchToHex(o) {
  const L = clamp01(o.L);
  let C = Math.max(0, o.C);
  if (!inGamut(oklchLinear({ L, C, H: o.H }))) {
    let lo = 0, hi = C;
    for (let i = 0; i < 30; i++) {
      const mid = (lo + hi) / 2;
      if (inGamut(oklchLinear({ L, C: mid, H: o.H }))) lo = mid; else hi = mid;
    }
    C = lo;
  }
  return linearToHex(oklchLinear({ L, C, H: o.H }));
}

function luminance(hex) {
  const [r, g, b] = hexToRgb(hex).map(toLinear);
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
}

function contrast(a, b) {
  const la = luminance(a), lb = luminance(b);
  return (Math.max(la, lb) + 0.05) / (Math.min(la, lb) + 0.05);
}

function isReserved(hex) {
  const { C, H } = hexToOklch(hex);
  return C >= RESERVED.minC && (H >= RESERVED.hueFrom || H < RESERVED.hueTo);
}

const hueDist = (a, b) => { const d = Math.abs(a - b) % 360; return d > 180 ? 360 - d : d; };
const fmt = (hex) => { const o = hexToOklch(hex); return `H${Math.round(o.H)} C${o.C.toFixed(3)}`; };
const same = (a, b) => typeof a === 'string' && typeof b === 'string' && a.toUpperCase() === b.toUpperCase();
const up = (h) => (isHex(h) ? h.toUpperCase() : h);

// Step L (keeping H and C) toward `dir` (+1 lighter, −1 darker) until the
// colour meets `target` against `against`. Returns the start colour if it
// already passes.
function stepUntil(hex, against, target, dir) {
  if (contrast(hex, against) >= target) return hex;
  const o = hexToOklch(hex);
  for (let L = o.L + dir * STEP; L >= 0 && L <= 1; L += dir * STEP) {
    const c = oklchToHex({ L, C: o.C, H: o.H });
    if (contrast(c, against) >= target) return c;
  }
  return oklchToHex({ L: dir > 0 ? 1 : 0, C: o.C, H: o.H });
}

// ---------- validation ----------

class InputError extends Error {}

function requireHexMap(obj, keys, label, allowNull) {
  if (!obj || typeof obj !== 'object') throw new InputError(`${label} must be an object`);
  for (const k of keys) {
    const v = obj[k];
    if (allowNull && (v === null || v === undefined)) continue;
    if (!isHex(v)) throw new InputError(`${label}.${k} must be a #RRGGBB hex`);
  }
}

function validateAssign(input) {
  if (!input || typeof input !== 'object') throw new InputError('input must be an object');
  if (!Array.isArray(input.candidates)) throw new InputError('candidates must be an array');
  for (const c of input.candidates) {
    if (!c || !isHex(c.hex)) throw new InputError('every candidate needs a #RRGGBB hex');
    if (c.weight !== null && c.weight !== undefined && typeof c.weight !== 'number') throw new InputError('candidate weight must be a number or null');
  }
  requireHexMap(input.picks, ['primary', 'secondary', 'accent'], 'picks', true);
  requireHexMap(input.neutrals, ['background', 'surface', 'text', 'text_muted'], 'neutrals', false);
  if (input.brand !== undefined && input.brand !== null && !isHex(input.brand)) throw new InputError('brand must be a #RRGGBB hex');
  if (!input.picks.primary && input.candidates.length === 0) throw new InputError('need picks.primary or at least one candidate');
}

function validateDerive(input) {
  if (!input || typeof input !== 'object') throw new InputError('input must be an object');
  if (input.source_mode !== 'light' && input.source_mode !== 'dark') throw new InputError('source_mode must be "light" or "dark"');
  requireHexMap(input.colours, COLOUR_KEYS, 'colours', false);
}

// ---------- assign ----------

function assign(input) {
  validateAssign(input);
  const decisions = [];
  const picks = { primary: up(input.picks.primary || null), secondary: up(input.picks.secondary || null), accent: up(input.picks.accent || null) };
  const cands = input.candidates.map((c, i) => ({ hex: c.hex.toUpperCase(), weight: typeof c.weight === 'number' ? c.weight : null, i }));
  const weighted = cands.some((c) => c.weight !== null);
  const total = cands.reduce((s, c) => s + (c.weight || 0), 0);
  const inUse = (c) => c.weight === null || total === 0 || c.weight / total >= USAGE_SHARE_MIN;
  const byWeight = [...cands].sort((a, b) => (b.weight || 0) - (a.weight || 0) || a.i - b.i);

  // brand: largest-area chromatic colour; forced when the caller supplies one.
  let brand;
  if (input.brand) brand = input.brand.toUpperCase();
  else if (cands.length === 0) brand = picks.primary;
  else if (weighted) brand = byWeight[0].hex;
  else brand = picks.primary || cands[0].hex;
  const brandO = hexToOklch(brand);
  const brandH = brandO.H;

  const neutralRoles = {
    primary: oklchToHex({ L: 0.30, C: 0.025, H: brandH }),
    secondary: oklchToHex({ L: 0.45, C: 0.02, H: brandH }),
    accent: oklchToHex({ L: 0.42, C: 0.065, H: brandH }),
  };
  const usable = (c) => !isReserved(c.hex) && hexToOklch(c.hex).C >= RESERVED.minC;

  // primary cascade
  let primary = null;
  const usageRejected = [];
  if (picks.primary && !isReserved(picks.primary)) {
    primary = picks.primary;
  } else {
    if (picks.primary) decisions.push(`primary ${picks.primary} rejected: reserved zone (${fmt(picks.primary)})`);
    for (const c of byWeight) {
      if (!usable(c)) continue;
      if (!inUse(c)) { usageRejected.push(c); continue; }
      primary = c.hex;
      decisions.push(`primary = ${c.hex}: next non-reserved extracted colour in real use`);
      break;
    }
    if (!primary) {
      primary = neutralRoles.primary;
      decisions.push(`primary = ${primary}: brand-tinted neutral (no non-reserved extracted colour in real use)`);
    }
  }

  const fillRole = (role, prim, log) => {
    const pick = picks[role];
    if (pick && !isReserved(pick) && !same(pick, prim)) return pick;
    if (pick && log) decisions.push(`${role} ${pick} rejected: ${isReserved(pick) ? `reserved zone (${fmt(pick)})` : 'same as primary'}`);
    return null;
  };
  const completeRoles = (prim, log) => {
    const roles = { primary: prim, secondary: fillRole('secondary', prim, log), accent: fillRole('accent', prim, log) };
    for (const role of ['secondary', 'accent']) {
      if (roles[role]) continue;
      const taken = [roles.primary, roles.secondary, roles.accent];
      const next = byWeight.find((c) => usable(c) && inUse(c) && !taken.some((t) => same(t, c.hex)));
      roles[role] = next ? next.hex : neutralRoles[role];
      if (log) decisions.push(`${role} = ${roles[role]}: ${next ? 'next non-reserved extracted colour in real use' : 'brand-tinted neutral'}`);
    }
    return roles;
  };

  const roles = completeRoles(primary, true);
  let options = null;
  if (same(primary, neutralRoles.primary) && usageRejected.length > 0) {
    const site = usageRejected[0].hex;
    options = { neutral: roles, site_colour: completeRoles(site, false) };
    decisions.push(`two options offered: neutral ${roles.primary} or site colour ${site} (rejected only for low usage)`);
  } else if (same(primary, neutralRoles.primary)) {
    decisions.push('no second option: no non-reserved site colour was rejected only for low usage');
  }

  // status: the house set; error moved away from a reserved brand hue.
  const status = { ...HOUSE_STATUS };
  const surface = input.neutrals.surface.toUpperCase();
  const darkSurface = hexToOklch(surface).L < 0.5;
  if (isReserved(brand)) {
    const e = hexToOklch(status.error);
    if (hueDist(e.H, brandH) < 12) {
      const H = hueDist(22, brandH) >= hueDist(40, brandH) ? 22 : 40;
      const dir = e.L <= brandO.L ? -1 : 1;
      let L = e.L + dir * 0.08;
      let hex = oklchToHex({ L, C: e.C, H });
      // clamp: error still meets the fill target on the surface
      while (contrast(hex, surface) < FILL_TARGET && L > 0 && L < 1) {
        L += darkSurface ? STEP : -STEP;
        hex = oklchToHex({ L, C: e.C, H });
      }
      status.error = hex;
      decisions.push(`error moved to ${hex} (H${H}) away from brand ${brand} (${fmt(brand)})`);
    }
  }
  // A dark hue-source surface: status keeps H and C, lightness only as far as the fill target needs.
  for (const k of Object.keys(status)) status[k] = stepUntil(status[k], surface, FILL_TARGET, darkSurface ? 1 : -1);

  return { brand, roles, options, status, decisions };
}

// ---------- derive ----------

function onColours(colours, _mode) {
  const H = hexToOklch(colours.brand).H;
  const inkDark = oklchToHex({ L: 0.20, C: 0.01, H });
  const inkLight = oklchToHex({ L: 0.98, C: 0.005, H });
  const out = {};
  for (const k of ON_KEYS) out[k] = contrast(inkDark, colours[k]) >= contrast(inkLight, colours[k]) ? inkDark : inkLight;
  return out;
}

function textPairs(c) {
  return {
    text_background: contrast(c.text, c.background),
    text_surface: contrast(c.text, c.surface),
    text_muted_background: contrast(c.text_muted, c.background),
    text_muted_surface: contrast(c.text_muted, c.surface),
  };
}

function derive(input) {
  validateDerive(input);
  const src = {};
  for (const k of COLOUR_KEYS) src[k] = input.colours[k].toUpperCase();
  const mode = input.source_mode === 'light' ? 'dark' : 'light';
  const toDark = mode === 'dark';
  const far = toDark ? 1 : -1;
  const H = hexToOklch(src.brand).H;
  const adjustments = [];
  const out = { brand: src.brand };

  // neutral ladder
  if (toDark) {
    out.background = oklchToHex({ L: 0.17, C: 0.012, H });
    out.surface = oklchToHex({ L: 0.22, C: 0.014, H });
    out.text = oklchToHex({ L: 0.95, C: 0.008, H });
  } else {
    out.background = oklchToHex({ L: 0.99, C: 0.004, H });
    out.surface = oklchToHex({ L: 0.965, C: 0.006, H });
    out.text = oklchToHex({ L: 0.22, C: 0.015, H });
  }
  const mutedC = toDark ? 0.01 : 0.012;
  let mL = toDark ? 0.70 : 0.45;
  out.text_muted = oklchToHex({ L: mL, C: mutedC, H });
  while ((contrast(out.text_muted, out.surface) < TEXT_TARGET || contrast(out.text_muted, out.background) < TEXT_TARGET) && mL > 0 && mL < 1) {
    mL += far * STEP;
    out.text_muted = oklchToHex({ L: mL, C: mutedC, H });
  }

  // fills: neutral flip for primary/secondary, minimum change for the rest
  const fills = {};
  const flipL = toDark ? { primary: 0.90, secondary: 0.36 } : { primary: 0.30, secondary: 0.88 };
  for (const k of FILL_KEYS) {
    const o = hexToOklch(src[k]);
    if ((k === 'primary' || k === 'secondary') && o.C < NEUTRAL_C) {
      out[k] = oklchToHex({ L: flipL[k], C: o.C, H });
      adjustments.push(`${k}: neutral flip to L ${flipL[k]} (${src[k]} -> ${out[k]})`);
      if (k === 'secondary') {
        // A flipped neutral secondary is a tonal button just off the surface (design §4.1 spike):
        // the fill target is not applied; its label is still measured.
        adjustments.push(`secondary: tonal neutral, fill target not applied (${contrast(out[k], out.surface).toFixed(2)}:1 vs surface)`);
        continue;
      }
    } else {
      out[k] = stepUntil(src[k], out.surface, FILL_TARGET, far);
      if (!same(out[k], src[k])) adjustments.push(`${k}: lightness moved for ${FILL_TARGET}:1 vs surface (${src[k]} -> ${out[k]})`);
    }
    fills[k] = contrast(out[k], out.surface);
  }

  const colours = {};
  for (const k of COLOUR_KEYS) colours[k] = out[k];
  const on = onColours(colours, mode);
  for (const k of ON_KEYS) {
    const r = contrast(on[k], colours[k]);
    if (r < LABEL_TARGET) adjustments.push(`${k}: best label ${on[k]} is ${r.toFixed(2)}:1 on ${colours[k]} (below ${LABEL_TARGET}:1)`);
  }
  const pairs = textPairs(colours);
  for (const [k, v] of Object.entries(pairs)) if (v < TEXT_TARGET) adjustments.push(`${k}: ${v.toFixed(2)}:1 (below ${TEXT_TARGET}:1)`);

  return { mode, colours, on_colours: on, contrast: pairs, fills, adjustments };
}

// ---------- CLI ----------

function main(argv) {
  const [op, ...rest] = argv;
  const arg = (name) => { const i = rest.indexOf(name); return i >= 0 ? rest[i + 1] : undefined; };
  const inPath = arg('--in');
  const outPath = arg('--out');
  if ((op !== 'assign' && op !== 'derive') || !inPath || !outPath) {
    process.stderr.write('usage: colour-tokens.cjs <assign|derive> --in <json> --out <json>\n');
    return 2;
  }
  try {
    const input = JSON.parse(fs.readFileSync(inPath, 'utf8'));
    const result = op === 'assign' ? assign(input) : derive(input);
    fs.writeFileSync(outPath, JSON.stringify(result, null, 2) + '\n');
    return 0;
  } catch (e) {
    process.stderr.write(`colour-tokens ${op}: ${e && e.message ? e.message : String(e)}\n`);
    return 2;
  }
}

module.exports = {
  hexToOklch, oklchToHex, contrast, isReserved, assign, derive, onColours,
  RESERVED, NEUTRAL_C, USAGE_SHARE_MIN, FILL_TARGET, LABEL_TARGET, TEXT_TARGET, HOUSE_STATUS,
};

if (require.main === module) process.exitCode = main(process.argv.slice(2));
