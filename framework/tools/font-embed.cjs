#!/usr/bin/env node
/**
 * font-embed.cjs — deterministic brand-font handling for /design-system
 *
 * Purpose: make the brand specimens in the design-system HTML (and in the
 * prototypes built from it) render in a real brand or stand-in face without a
 * network connection, without an LLM probing URLs or transcribing base64.
 *   candidates  — font-availability-rules §2 as code: the ordered Google-name
 *                 candidate list for a CSS font-family, plus the weight a
 *                 per-weight family name carries (`SourceSansPro-SemiBold`).
 *   file-family — the family an `@font-face` src file name names (E1 evidence).
 *   resolve     — §1 E3: one Google Fonts probe per candidate, with a control.
 *   embed       — fetch the latin + latin-ext woff2 faces of each family as
 *                 data URIs, within a byte budget.
 *   inject      — fill the `brand-font-faces` marker block of a written HTML.
 *   vendor      — turn that block into woff2 files + a CSS file for /prototype.
 * The prompt files decide *which* family a slot needs; this file decides how a
 * name is spelled for Google and how its faces reach the file.
 *
 * Callers: framework/agents/design-system-styler/steps/step-05-brand-extraction.md
 * (candidates, file-family, resolve in §4b), step-05b-fill-and-derive.md (embed
 * in §G), step-06-artifact-generation.md (inject), step-07-handback.md (embed on
 * revise), framework/agents/prototype-app-scaffolder.md (vendor). Policy prose:
 * framework/agents/design-system-styler/data/font-availability-rules.md.
 * Never restate the constants or word lists below in prose — point here.
 *
 * Contract (CLI), JSON on stdout unless noted:
 *   node framework/tools/font-embed.cjs candidates  --name <raw>
 *   node framework/tools/font-embed.cjs file-family --url <url>
 *   node framework/tools/font-embed.cjs resolve     --name <raw> [--name <raw> …]
 *   node framework/tools/font-embed.cjs embed       --params "<A>,<B>" --out <css>
 *        writes the CSS (possibly empty); prints { embedded, failed, bytes }
 *   node framework/tools/font-embed.cjs inject      --html <path> --css <path>
 *        rewrites the HTML in place; prints { sha256, bytes } of the new file
 *   node framework/tools/font-embed.cjs vendor      --html <path> --fonts-dir <dir> --css-out <path>
 *        writes the woff2 files and the CSS; prints { files, css_bytes }
 *   exit 0 → result printed / file written; exit 2 → one-line stderr message.
 *   Never throws an uncaught error. As a module, bad input throws a TypeError.
 *
 * Self-contained: Node >= 18 (global fetch), no dependencies.
 * Unit tests: font-embed.test.cjs.
 */
'use strict';

const GOOGLE_CSS = 'https://fonts.googleapis.com/css2?family=';
const WEIGHTS = ':wght@400;500;600;700&display=swap';
// A desktop Chrome UA makes Google answer with woff2 faces split by subset.
const UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36';
const SUBSETS = ['latin', 'latin-ext'];
const MAX_EMBED_BYTES = 600000; // raw woff2 bytes per design-system file
const MARKER = '/* BRAND_FONT_FACES */';
const CONTROL = 'Inter';
const MAX_PROBES = 5; // requests per resolve call, control included

// Weight words a per-weight family or file name may end in (design D3).
const WEIGHT_WORDS = {
  thin: 100, hairline: 100,
  extralight: 200, ultralight: 200,
  light: 300,
  regular: 400, normal: 400, book: 400, roman: 400,
  medium: 500,
  semibold: 600, demibold: 600,
  bold: 700,
  extrabold: 800, ultrabold: 800,
  black: 900, heavy: 900,
};
const STYLE_WORDS = ['italic', 'oblique'];
// §2 step 4: names whose capitalisation is not plain Title Case.
const VERBATIM = ['DM Sans', 'DM Serif Display', 'EB Garamond', 'IBM Plex Sans', 'IBM Plex Serif', 'PT Sans', 'PT Serif', 'Wix Madefor Display'];
// §2 step 6: one trailing classification/style word, trimmed into the LAST candidate.
const TRIM_WORDS = ['Sans', 'Serif', 'Mono', 'Grotesk', 'Text', 'Display', 'Std', 'LT', 'Pro', 'Regular', 'Book'];

class InputError extends TypeError {}

// ---------- names (font-availability-rules §2 + design D3) ----------

function camelSplit(token) {
  return token
    .replace(/([a-z])([A-Z])/g, '$1 $2')
    .replace(/([A-Z]+)([A-Z][a-z])/g, '$1 $2')
    .replace(/([A-Za-z])(\d)/g, '$1 $2')
    .split(' ')
    .filter(Boolean);
}

// Words → { words, weight, italic }: drop one trailing style word, then one
// trailing weight word (single, or camel-split pair such as `Semi Bold`).
function stripWeight(words) {
  let italic = false;
  let weight = null;
  const out = words.slice();
  if (out.length > 1 && STYLE_WORDS.includes(out[out.length - 1].toLowerCase())) {
    italic = true;
    out.pop();
  }
  const pair = out.length > 2 ? (out[out.length - 2] + out[out.length - 1]).toLowerCase() : null;
  if (pair && Object.hasOwn(WEIGHT_WORDS, pair)) {
    weight = WEIGHT_WORDS[pair];
    out.splice(-2, 2);
  } else if (out.length > 1 && Object.hasOwn(WEIGHT_WORDS, out[out.length - 1].toLowerCase())) {
    weight = WEIGHT_WORDS[out[out.length - 1].toLowerCase()];
    out.pop();
  }
  return { words: out, weight, italic };
}

function titleCase(words) {
  const name = words.map((w) => (w === w.toLowerCase() ? w.charAt(0).toUpperCase() + w.slice(1) : w)).join(' ');
  return VERBATIM.find((v) => v.toLowerCase() === name.toLowerCase()) || name;
}

// Delimiter split, per-token camel split, weight strip, Title Case.
function parseWords(tokens) {
  const words = tokens.flatMap(camelSplit);
  const { words: kept, weight, italic } = stripWeight(words);
  return { name: titleCase(kept), weight, italic };
}

function candidates(raw) {
  if (typeof raw !== 'string' || raw.trim() === '') throw new InputError('name must be a non-empty string');
  let s = raw.trim().replace(/^["']+|["']+$/g, '').replace(/\s+/g, ' ').trim();
  if (s === '') throw new InputError('name must be a non-empty string');
  // §2 step 2: variable-font build suffix.
  s = s.replace(/[\s_-](?:variable|var|vf)$/i, '').replace(/([a-z])(?:Variable|Var|VF)$/, '$1');
  const { name, weight, italic } = parseWords(s.split(/[\s_-]+/).filter(Boolean));
  const list = [name];
  const folded = name.normalize('NFD').replace(/[̀-ͯ]/g, '');
  if (folded !== name) list.push(folded);
  const words = name.split(' ');
  if (words.length > 1 && TRIM_WORDS.includes(words[words.length - 1])) list.push(words.slice(0, -1).join(' '));
  return { candidates: [...new Set(list)], weight, italic };
}

// The family a font file name names, or null when it names none.
function familyFromFontFile(url) {
  if (typeof url !== 'string' || url.trim() === '' || /^data:/i.test(url.trim())) return null;
  let file = url.trim().split(/[?#]/)[0];
  file = file.slice(file.lastIndexOf('/') + 1);
  try { file = decodeURIComponent(file); } catch { return null; }
  file = file.replace(/\.(woff2?|ttf|otf|eot|svg)$/i, '');
  const tokens = [];
  for (const t of file.split(/[-_.]+/).filter(Boolean)) {
    // A build hash ends the name: a digit, or six or more capitals only.
    if (/\d/.test(t) || /^[A-Z]{6,}$/.test(t)) break;
    tokens.push(t);
  }
  if (tokens.length === 0) return null;
  const { name, weight } = parseWords(tokens);
  return name ? { family: name, weight } : null;
}

// ---------- Google Fonts probe (font-availability-rules §1 E3) ----------

const encodeFamily = (name) => encodeURIComponent(name).replace(/%20/g, '+');

async function statusOf(fetch, url, opts) {
  try {
    return (await fetch(url, opts)).status;
  } catch {
    return 'error';
  }
}

// Per name: the first two candidates in order, stopping at the first 200;
// then one shared control. No weight axis: a missing axis still answers 200.
async function resolveAll(names, { fetch }) {
  if (!Array.isArray(names) || names.length === 0) throw new InputError('names must be a non-empty array');
  if (typeof fetch !== 'function') throw new InputError('fetch must be a function');
  const parsed = names.map((n) => ({ name: n, ...candidates(n) }));
  let requests = 0;
  let control;
  const out = [];
  for (const p of parsed) {
    const tried = [];
    let family = null;
    let cut = false;
    for (const c of p.candidates.slice(0, 2)) {
      if (requests >= MAX_PROBES) { cut = true; break; }
      const status = await statusOf(fetch, GOOGLE_CSS + encodeFamily(c));
      requests += 1;
      tried.push({ candidate: c, status });
      if (status === 200) { family = c; break; }
    }
    let verdict;
    if (family) {
      verdict = 'google-native';
    } else {
      if (control === undefined && requests < MAX_PROBES) {
        control = await statusOf(fetch, GOOGLE_CSS + encodeFamily(CONTROL));
        requests += 1;
      }
      verdict = !cut && tried.length > 0 && control === 200 ? 'unavailable' : 'unknown';
    }
    out.push({ name: p.name, verdict, family, weight: p.weight, tried });
  }
  return out;
}

// ---------- embedding ----------

const FACE_RE = /\/\*\s*([a-z0-9-]+)\s*\*\/\s*(@font-face\s*\{[^}]*\})/g;
const SRC_RE = /src:\s*url\(([^)]+)\)\s*format\(['"]woff2['"]\)\s*;/;

// One family: its latin + latin-ext blocks with data-URI sources, or a reason.
async function embedFamily(fetch, param) {
  let res;
  try {
    res = await fetch(GOOGLE_CSS + param.replace(/ /g, '+') + WEIGHTS, { headers: { 'User-Agent': UA } });
  } catch {
    return { reason: 'network' };
  }
  if (res.status !== 200) return { reason: `http ${res.status}` };
  let text;
  try { text = await res.text(); } catch { return { reason: 'network' }; }
  const faces = [];
  for (const m of text.matchAll(FACE_RE)) {
    const src = m[2].match(SRC_RE);
    if (SUBSETS.includes(m[1]) && src) faces.push({ subset: m[1], block: m[2], url: src[1].replace(/^['"]|['"]$/g, '') });
  }
  if (faces.length === 0) return { reason: 'no faces' };
  const data = new Map();
  for (const url of new Set(faces.map((f) => f.url))) {
    let font;
    try {
      font = await fetch(url, { headers: { 'User-Agent': UA } });
    } catch {
      return { reason: 'network' };
    }
    if (font.status !== 200) return { reason: `http ${font.status}` };
    try { data.set(url, Buffer.from(await font.arrayBuffer())); } catch { return { reason: 'network' }; }
  }
  const css = faces
    .map((f) => `/* ${f.subset} */\n${f.block.replace(SRC_RE, `src: url(data:font/woff2;base64,${data.get(f.url).toString('base64')}) format('woff2');`)}`)
    .join('\n');
  const bytes = [...data.values()].reduce((n, b) => n + b.length, 0);
  return { css, bytes };
}

// Each distinct param embedded whole or not at all, within maxBytes.
async function buildFaces(params, { fetch, maxBytes = MAX_EMBED_BYTES }) {
  if (!Array.isArray(params) || !params.every((p) => typeof p === 'string' && p.trim() !== '')) {
    throw new InputError('params must be an array of non-empty strings');
  }
  if (typeof fetch !== 'function') throw new InputError('fetch must be a function');
  const embedded = [];
  const failed = [];
  const parts = [];
  let bytes = 0;
  for (const param of [...new Set(params.map((p) => p.trim()))]) {
    const r = await embedFamily(fetch, param);
    if (r.reason) failed.push({ param, reason: r.reason });
    else if (bytes + r.bytes > maxBytes) failed.push({ param, reason: 'budget' });
    else {
      embedded.push(param);
      parts.push(r.css);
      bytes += r.bytes;
    }
  }
  return { css: parts.join('\n'), embedded, failed, bytes };
}

module.exports = {
  candidates, familyFromFontFile, resolveAll, buildFaces, InputError,
  WEIGHT_WORDS, GOOGLE_CSS, WEIGHTS, UA, SUBSETS, MAX_EMBED_BYTES, MARKER, CONTROL, MAX_PROBES,
};
