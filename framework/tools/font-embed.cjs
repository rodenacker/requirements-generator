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

module.exports = {
  candidates, familyFromFontFile, InputError,
  WEIGHT_WORDS,
};
