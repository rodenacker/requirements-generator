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
 *        rewrites the HTML in place, then opens it in the default browser when
 *        open-artifact.cjs allowlists it; prints { sha256, bytes, opened }
 *   node framework/tools/font-embed.cjs vendor      --html <path> --fonts-dir <dir> --css-out <path>
 *        writes the woff2 files and the CSS; prints { files, css_bytes }
 *   exit 0 → result printed / file written; exit 2 → one-line stderr message.
 *   Never throws an uncaught error. As a module, bad input throws a TypeError.
 *
 * Node >= 18 (global fetch), no package dependencies; inject uses the sibling
 * open-artifact.cjs to preview the filled file.
 * Unit tests: font-embed.test.cjs.
 */
'use strict';

const crypto = require('node:crypto');
const fs = require('node:fs');
const path = require('node:path');

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

// An all-lowercase token has no case boundary, so split off a glued class
// word instead (`bentonsans` → `benton sans`); the stem keeps 3+ letters.
function classSplit(token) {
  const m = token === token.toLowerCase() ? /^([a-z]{3,})(sans|serif|mono)$/.exec(token) : null;
  return m ? [m[1], m[2]] : [token];
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
  const words = tokens.flatMap(camelSplit).flatMap(classSplit);
  // A Font Squirrel build suffix (`-webfont`, `WebFont`) names the build, never the family.
  const n = words.length;
  if (n > 1 && words[n - 1].toLowerCase() === 'webfont') words.pop();
  else if (n > 2 && (words[n - 2] + words[n - 1]).toLowerCase() === 'webfont') words.splice(-2, 2);
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
  // A variable family repeats one file per subset in a block per weight: merge
  // those into one block with a weight range so each file is embedded once.
  const groups = new Map();
  for (const f of faces) {
    const style = (f.block.match(/font-style:\s*([a-z]+)/) || [])[1] || 'normal';
    const key = `${f.subset}|${style}|${f.url}`;
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(f);
  }
  const css = [...groups.values()]
    .map((g) => {
      const weights = g.map((f) => Number((f.block.match(/font-weight:\s*(\d+)/) || [])[1])).filter(Number.isFinite);
      let block = g[0].block.replace(SRC_RE, `src: url(data:font/woff2;base64,${data.get(g[0].url).toString('base64')}) format('woff2');`);
      if (g.length > 1 && weights.length === g.length) {
        block = block.replace(/font-weight:\s*\d+;/, `font-weight: ${Math.min(...weights)} ${Math.max(...weights)};`);
      }
      return `/* ${g[0].subset} */\n${block}`;
    })
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

// ---------- the brand-font-faces block ----------

const BLOCK_OPEN = '<style id="brand-font-faces">';
const EMPTY_FACES = '/* no embedded brand fonts */';

// [start, end) of the one block's content; null when there is no block.
function blockRange(html) {
  const first = html.indexOf(BLOCK_OPEN);
  if (first < 0) return null;
  if (html.indexOf(BLOCK_OPEN, first + 1) >= 0) throw new InputError('more than one brand-font-faces block');
  const start = first + BLOCK_OPEN.length;
  const end = html.indexOf('</style>', start);
  if (end < 0) throw new InputError('brand-font-faces block is not closed');
  return [start, end];
}

// Fill the marker block; every other byte is unchanged.
function inject(html, css) {
  if (typeof html !== 'string') throw new InputError('html must be a string');
  if (typeof css !== 'string') throw new InputError('css must be a string');
  const range = blockRange(html);
  if (!range) throw new InputError('no brand-font-faces block');
  const [start, end] = range;
  if (html.slice(start, end) !== MARKER) throw new InputError('brand-font-faces block is already filled');
  return html.slice(0, start) + (css === '' ? EMPTY_FACES : css) + html.slice(end);
}

// The filled block as local woff2 files + a CSS file pointing at /fonts/.
function vendor(html) {
  if (typeof html !== 'string') throw new InputError('html must be a string');
  const range = blockRange(html);
  if (!range) return { css: '', files: [] };
  const content = html.slice(range[0], range[1]);
  const byUri = new Map();
  const parts = [];
  for (const m of content.matchAll(FACE_RE)) {
    const uri = m[2].match(/url\((data:font\/woff2;base64,([A-Za-z0-9+/=]+))\)/);
    const fam = m[2].match(/font-family:\s*['"]?([^'";]+)['"]?\s*;/);
    if (!uri || !fam) continue;
    if (!byUri.has(uri[1])) {
      const bytes = Buffer.from(uri[2], 'base64');
      const hash = crypto.createHash('sha256').update(bytes).digest('hex').slice(0, 8);
      const slug = fam[1].trim().toLowerCase().replace(/\s+/g, '-');
      byUri.set(uri[1], { name: `${slug}-${m[1]}-${hash}.woff2`, bytes });
    }
    parts.push(`/* ${m[1]} */\n${m[2].replace(uri[0], `url(/fonts/${byUri.get(uri[1]).name})`)}`);
  }
  if (parts.length === 0) return { css: '', files: [] };
  return { css: parts.join('\n') + '\n', files: [...byUri.values()] };
}

// ---------- CLI ----------

const USAGE = 'usage: font-embed.cjs <candidates|file-family|resolve|embed|inject|vendor> [options]';

function writeFile(file, data) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, data);
}

async function main(argv) {
  const [op, ...rest] = argv;
  const all = (name) => rest.flatMap((v, i) => (v === name && i + 1 < rest.length ? [rest[i + 1]] : []));
  const arg = (name) => all(name)[0];
  const need = (...names) => {
    for (const n of names) if (!arg(n)) throw new InputError(`${op} needs ${n}`);
  };
  const ops = {
    candidates: async () => { need('--name'); return candidates(arg('--name')); },
    'file-family': async () => { need('--url'); return familyFromFontFile(arg('--url')); },
    resolve: async () => { need('--name'); return resolveAll(all('--name'), { fetch: globalThis.fetch }); },
    embed: async () => {
      need('--params', '--out');
      const params = arg('--params').split(',').map((p) => p.trim()).filter(Boolean);
      const r = await buildFaces(params, { fetch: globalThis.fetch });
      writeFile(arg('--out'), r.css);
      return { embedded: r.embedded, failed: r.failed, bytes: r.bytes };
    },
    inject: async () => {
      need('--html', '--css');
      const file = arg('--html');
      fs.writeFileSync(file, inject(fs.readFileSync(file, 'utf8'), fs.readFileSync(arg('--css'), 'utf8')));
      const disk = fs.readFileSync(file);
      // The filled file is final: open it for the consultant (artifact-preview.md).
      const opened = require('./open-artifact.cjs').openIfAllowed(file);
      return { sha256: crypto.createHash('sha256').update(disk).digest('hex'), bytes: disk.length, opened };
    },
    vendor: async () => {
      need('--html', '--fonts-dir', '--css-out');
      const v = vendor(fs.readFileSync(arg('--html'), 'utf8'));
      for (const f of v.files) writeFile(path.join(arg('--fonts-dir'), f.name), f.bytes);
      writeFile(arg('--css-out'), v.css);
      return { files: v.files.map((f) => f.name), css_bytes: Buffer.byteLength(v.css) };
    },
  };
  if (!Object.hasOwn(ops, op)) {
    process.stderr.write(USAGE + '\n');
    return 2;
  }
  try {
    process.stdout.write(JSON.stringify(await ops[op](), null, 2) + '\n');
    return 0;
  } catch (e) {
    process.stderr.write(`font-embed ${op}: ${String(e && e.message ? e.message : e).split('\n')[0]}\n`);
    return 2;
  }
}

module.exports = {
  candidates, familyFromFontFile, resolveAll, buildFaces, inject, vendor, InputError,
  WEIGHT_WORDS, GOOGLE_CSS, WEIGHTS, UA, SUBSETS, MAX_EMBED_BYTES, MARKER, CONTROL, MAX_PROBES,
};

if (require.main === module) main(process.argv.slice(2)).then((code) => { process.exitCode = code; });
