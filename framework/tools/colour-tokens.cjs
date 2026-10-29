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
 *   measure — a set in its own mode (the hue-source set, or an extracted
 *            other mode): text-pair adjustment, on-colours, fill and pair
 *            contrast numbers. Extracted fills are reported, never moved.
 * The prompt files decide *what* the site uses (picks, area weights, the
 * site's own other scheme); this file decides *how* those become tokens.
 *
 * Callers: framework/agents/design-system-styler/steps/step-05b-fill-and-derive.md
 * (assign at the start of §C; measure in §D; derive in §B.1 / §F). Policy prose:
 * framework/agents/design-system-styler/data/cross-mode-derivation-rules.md.
 * Never restate the constants below in prose — point here.
 *
 * Contract (CLI):
 *   node framework/tools/colour-tokens.cjs <assign|derive|measure> --in <json> --out <json>
 *   exit 0 → output JSON written; exit 2 → one-line stderr message (bad input).
 *   Never throws an uncaught error. As a module, bad input throws a TypeError.
 *
 * assign input:  { mode: "light"|"dark" (the hue-source mode, required),
 *                  candidates: [{hex, weight|null}], picks: {primary, secondary,
 *                  accent, brand?} (hex|null; a non-null brand is the brand),
 *                  pick_origins?: {primary, secondary, accent} ("page"|"pdf"|
 *                  "alt-scheme"; absent = exempt),
 *                  neutrals: {background, surface, text, text_muted} (hex|null) }
 *   A "page" pick with no weighted candidate within PICK_MATCH_DE is dropped
 *   (decision "<role> <hex> rejected: not rendered on the page") and the
 *   cascade fills the role. PDF and alt-scheme picks are never rendered here.
 * assign output: { brand, monochrome, roles, options, status, neutrals (all
 *                  filled), filled: [neutral names taken from the ladder],
 *                  decisions }
 *   monochrome = no candidate or pick carries colour; every helper-made tint
 *   is then pure grey. neutralLadder(brand|null, mode) is exported too.
 *
 * Self-contained: Node >= 18, no dependencies. Unit tests: colour-tokens.test.cjs.
 */
'use strict';

const fs = require('node:fs');

const RESERVED = { hueFrom: 345, hueTo: 95, minC: 0.07 };
const NEUTRAL_C = 0.04;
const USAGE_SHARE_MIN = 0.03;
// A page pick counts as rendered when a weighted candidate sits within this
// OKLab distance of it. Separates Bootstrap 4's #007BFF from a rendered #0089FF.
const PICK_MATCH_DE = 0.02;
const PICK_ORIGINS = ['page', 'pdf', 'alt-scheme'];
const FILL_TARGET = 3.0;
const LABEL_TARGET = 4.5;
const TEXT_TARGET = 4.5;
// The fixed light-mode status set for internal data-management apps. Nothing
// infers status any more; this constant is its only definition.
const HOUSE_STATUS = { success: '#15803D', warning: '#B45309', error: '#B91C1C', info: '#0369A1' };

const NEUTRAL_KEYS = ['background', 'surface', 'text', 'text_muted'];
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
function deltaEOk(a, b) {
  const lab = (hex) => { const { L, C, H } = hexToOklch(hex); const r = (H * Math.PI) / 180; return [L, C * Math.cos(r), C * Math.sin(r)]; };
  const [p, q] = [lab(a), lab(b)];
  return Math.hypot(p[0] - q[0], p[1] - q[1], p[2] - q[2]);
}
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

class InputError extends TypeError {}

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
  if (input.mode !== 'light' && input.mode !== 'dark') throw new InputError('mode must be "light" or "dark" (the hue-source mode)');
  requireHexMap(input.picks, ['primary', 'secondary', 'accent', 'brand'], 'picks', true);
  requireHexMap(input.neutrals, NEUTRAL_KEYS, 'neutrals', true);
  if (input.brand !== undefined && input.brand !== null && !isHex(input.brand)) throw new InputError('brand must be a #RRGGBB hex');
  if (input.pick_origins !== undefined && input.pick_origins !== null) {
    if (typeof input.pick_origins !== 'object') throw new InputError('pick_origins must be an object');
    for (const k of ['primary', 'secondary', 'accent']) {
      const o = input.pick_origins[k];
      if (o !== undefined && o !== null && !PICK_ORIGINS.includes(o)) throw new InputError(`pick_origins.${k} must be one of ${PICK_ORIGINS.join(', ')}`);
    }
  }
  if (!input.picks.primary && input.candidates.length === 0) throw new InputError('need picks.primary or at least one candidate');
}

function validateDerive(input) {
  if (!input || typeof input !== 'object') throw new InputError('input must be an object');
  if (input.source_mode !== 'light' && input.source_mode !== 'dark') throw new InputError('source_mode must be "light" or "dark"');
  requireHexMap(input.colours, COLOUR_KEYS, 'colours', false);
}

// ---------- neutral ladder ----------

// The brand-tinted neutral set for one mode: the hue-source gap-fill in assign
// and the other mode in derive. No brand, or a monochrome one, gives pure greys.
function neutralLadder(brandHex, mode) {
  if (mode !== 'light' && mode !== 'dark') throw new InputError('mode must be "light" or "dark"');
  const b = isHex(brandHex) ? hexToOklch(brandHex) : null;
  const tint = b && b.C >= NEUTRAL_C ? 1 : 0;
  const H = b ? b.H : 0;
  const dark = mode === 'dark';
  const at = (L, C) => oklchToHex({ L, C: C * tint, H });
  const out = dark
    ? { background: at(0.17, 0.012), surface: at(0.22, 0.014), text: at(0.95, 0.008) }
    : { background: at(0.99, 0.004), surface: at(0.965, 0.006), text: at(0.22, 0.015) };
  const mutedC = dark ? 0.01 : 0.012;
  const far = dark ? 1 : -1;
  let mL = dark ? 0.70 : 0.45;
  out.text_muted = at(mL, mutedC);
  while ((contrast(out.text_muted, out.surface) < TEXT_TARGET || contrast(out.text_muted, out.background) < TEXT_TARGET) && mL > 0 && mL < 1) {
    mL += far * STEP;
    out.text_muted = at(mL, mutedC);
  }
  return out;
}

// ---------- assign ----------

function assign(input) {
  validateAssign(input);
  const decisions = [];
  const picks = { primary: up(input.picks.primary || null), secondary: up(input.picks.secondary || null), accent: up(input.picks.accent || null) };
  const declaredBrand = up(input.picks.brand || input.brand || null);
  const cands = input.candidates.map((c, i) => ({ hex: c.hex.toUpperCase(), weight: typeof c.weight === 'number' ? c.weight : null, i }));
  const weighted = cands.some((c) => c.weight !== null);
  const total = cands.reduce((s, c) => s + (c.weight || 0), 0);
  const inUse = (c) => c.weight === null || total === 0 || c.weight / total >= USAGE_SHARE_MIN;
  const byWeight = [...cands].sort((a, b) => (b.weight || 0) - (a.weight || 0) || a.i - b.i);

  // Real-use gate: a pick read from the page (not a PDF, not the site's other
  // scheme) must be rendered there. Unweighted candidates carry no evidence.
  const origins = input.pick_origins || {};
  if (weighted) {
    for (const role of ['primary', 'secondary', 'accent']) {
      const pick = picks[role];
      if (!pick || origins[role] !== 'page') continue;
      if (cands.some((c) => c.weight > 0 && deltaEOk(c.hex, pick) <= PICK_MATCH_DE)) continue;
      decisions.push(`${role} ${pick} rejected: not rendered on the page`);
      picks[role] = null;
    }
  }

  // monochrome: no candidate and no pick carries colour. Every tint the helper
  // makes (neutral roles, neutral ladder, on-colour inks) is then pure grey.
  const monochrome = [...cands.map((c) => c.hex), picks.primary, picks.secondary, picks.accent, declaredBrand]
    .filter(Boolean).every((h) => hexToOklch(h).C < NEUTRAL_C);

  // brand: a declared brand (PDF brand guide) wins outright; otherwise the
  // largest-area chromatic colour (pale tints below the chroma floor never qualify).
  const chromatic = byWeight.find((c) => hexToOklch(c.hex).C >= RESERVED.minC);
  let brand;
  if (declaredBrand) brand = declaredBrand;
  else if (cands.length === 0) brand = picks.primary;
  else if (weighted && chromatic) brand = chromatic.hex;
  else brand = picks.primary || (chromatic || cands[0]).hex;
  const brandO = hexToOklch(brand);
  const brandH = brandO.H;
  // Helper-made tints carry the brand's hue only when the brand has one: an
  // achromatic brand (monochrome palette, or a black / grey declared brand)
  // gives pure greys, as neutralLadder and onColours do.
  const tint = brandO.C >= NEUTRAL_C ? 1 : 0;

  // Neutral gap-fill: every neutral the references did not give comes from the
  // hue-source ladder; given neutrals are kept exactly.
  const ladder = neutralLadder(monochrome ? null : brand, input.mode);
  const neutrals = {};
  const filled = [];
  for (const k of NEUTRAL_KEYS) {
    if (input.neutrals[k]) neutrals[k] = input.neutrals[k].toUpperCase();
    else { neutrals[k] = ladder[k]; filled.push(k); }
  }
  if (filled.length) decisions.push(`neutral ladder filled: ${filled.join(', ')}`);

  // Neutral roles sit at the far end of the hue-source ladder: charcoal on a
  // light surface, near-white on a dark one (a dark charcoal would look disabled).
  const surface = neutrals.surface;
  const darkSurface = hexToOklch(surface).L < 0.5;
  const tinted = (L, C) => oklchToHex({ L, C: C * tint, H: brandH });
  const neutralRoles = darkSurface
    ? {
      primary: tinted(0.90, 0.025),
      secondary: tinted(0.36, 0.02),
      accent: stepUntil(tinted(0.42, 0.065), surface, FILL_TARGET, 1),
    }
    : {
      primary: tinted(0.30, 0.025),
      secondary: tinted(0.45, 0.02),
      accent: tinted(0.42, 0.065),
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
  if (isReserved(brand)) {
    const e = hexToOklch(status.error);
    if (hueDist(e.H, brandH) < 12) {
      // [22°, 32°]: still red, and >= 15° clear of the house warning (H~49).
      const H = hueDist(22, brandH) >= hueDist(32, brandH) ? 22 : 32;
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

  return { brand, monochrome, roles, options, status, neutrals, filled, decisions };
}

// ---------- derive ----------

function onColours(colours, _mode) {
  const b = hexToOklch(colours.brand);
  const tint = b.C >= NEUTRAL_C ? 1 : 0;
  const inkDark = oklchToHex({ L: 0.20, C: 0.01 * tint, H: b.H });
  const inkLight = oklchToHex({ L: 0.98, C: 0.005 * tint, H: b.H });
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

  Object.assign(out, neutralLadder(src.brand, mode));

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

// ---------- measure ----------

// Validate a set in its own mode (the hue-source set, or an extracted other
// mode): text / text_muted step in lightness (H and C kept) away from the
// background until both pairs meet TEXT_TARGET; fills are reported, not moved.
function measure(input) {
  if (!input || typeof input !== 'object') throw new InputError('input must be an object');
  if (input.mode !== 'light' && input.mode !== 'dark') throw new InputError('mode must be "light" or "dark"');
  requireHexMap(input.colours, COLOUR_KEYS, 'colours', false);
  const colours = {};
  for (const k of COLOUR_KEYS) colours[k] = input.colours[k].toUpperCase();
  const far = input.mode === 'dark' ? 1 : -1;
  const adjustments = [];
  const passes = (h) => contrast(h, colours.background) >= TEXT_TARGET && contrast(h, colours.surface) >= TEXT_TARGET;
  for (const k of ['text', 'text_muted']) {
    if (passes(colours[k])) continue;
    const o = hexToOklch(colours[k]);
    let next = colours[k];
    for (let L = o.L + far * STEP; L >= 0 && L <= 1; L += far * STEP) {
      next = oklchToHex({ L, C: o.C, H: o.H });
      if (passes(next)) break;
    }
    adjustments.push(`${k} adjusted from ${colours[k]} to ${next} for ${TEXT_TARGET}:1 vs background and surface`);
    colours[k] = next;
  }
  const fills = {};
  for (const k of FILL_KEYS) {
    fills[k] = contrast(colours[k], colours.surface);
    if (fills[k] < FILL_TARGET) adjustments.push(`${k}: fill ${fills[k].toFixed(2)}:1 vs surface (below ${FILL_TARGET}:1; extracted fills are not moved)`);
  }
  const on = onColours(colours, input.mode);
  for (const k of ON_KEYS) {
    const r = contrast(on[k], colours[k]);
    if (r < LABEL_TARGET) adjustments.push(`${k}: best label ${on[k]} is ${r.toFixed(2)}:1 on ${colours[k]} (below ${LABEL_TARGET}:1)`);
  }
  const pairs = textPairs(colours);
  for (const [k, v] of Object.entries(pairs)) if (v < TEXT_TARGET) adjustments.push(`${k}: ${v.toFixed(2)}:1 (below ${TEXT_TARGET}:1)`);
  return { mode: input.mode, colours, on_colours: on, contrast: pairs, fills, adjustments };
}

// ---------- CLI ----------

function main(argv) {
  const [op, ...rest] = argv;
  const arg = (name) => { const i = rest.indexOf(name); return i >= 0 ? rest[i + 1] : undefined; };
  const inPath = arg('--in');
  const outPath = arg('--out');
  const ops = { assign, derive, measure };
  if (!Object.hasOwn(ops, op) || !inPath || !outPath) {
    process.stderr.write('usage: colour-tokens.cjs <assign|derive|measure> --in <json> --out <json>\n');
    return 2;
  }
  try {
    const input = JSON.parse(fs.readFileSync(inPath, 'utf8'));
    const result = ops[op](input);
    fs.writeFileSync(outPath, JSON.stringify(result, null, 2) + '\n');
    return 0;
  } catch (e) {
    process.stderr.write(`colour-tokens ${op}: ${e && e.message ? e.message : String(e)}\n`);
    return 2;
  }
}

module.exports = {
  hexToOklch, oklchToHex, contrast, isReserved, deltaEOk, assign, derive, measure, onColours, neutralLadder,
  RESERVED, NEUTRAL_C, USAGE_SHARE_MIN, PICK_MATCH_DE, FILL_TARGET, LABEL_TARGET, TEXT_TARGET, HOUSE_STATUS,
};

if (require.main === module) process.exitCode = main(process.argv.slice(2));
