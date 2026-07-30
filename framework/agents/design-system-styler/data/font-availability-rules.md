# Font Availability & Substitution Rules — Design-System-Styler Data File

**Role:** Pure reference knowledge consumed by step-05 (§4b Availability & substitution), step-05b (§B gap-fill, §G bookkeeping), step-06 (§B link rendering, §C assertions) and step-07 (§A disclosure, §B revise). It is the **canonical source of the availability axis** — the `google-native | substituted | unverified` enum in §1, the canonicalisation rules in §2, the proprietary→substitute table in §3, the verified-Google lists in §4, the non-brand→allowed map in §5, and the emitted-value/link shapes in §6. No other file restates any of them.

Sibling of `font-rules.md`, which owns the **brand-ness** axis. The two are disjoint; §0 is the contract between them.

---

## 0. Scope — two axes, never confused

A brand family token passes through two independent questions, in this order:

| # | Axis | Question | Canonical file | Outcome when it fails |
|---|------|----------|----------------|-----------------------|
| 1 | **Brand-ness** | Is this a deliberate brand typeface at all? | `font-rules.md` §1 | Token left **unset** → step-05b infers from the domain. **Never substituted.** |
| 2 | **Availability** | Can that brand typeface be loaded from Google Fonts? | **this file** | Brand name **kept**, a loadable substitute added behind it. **Never unset.** |

**A family reaches axis 2 only after passing axis 1.** `Arial`, `Helvetica`, `Segoe UI`, `SF Pro`, `system-ui` and every other member of `font-rules.md` §1 are rejected before this file is consulted, so they never appear in §3's table. Their handling — reject, leave unset, infer — is unchanged by this file, and `font-rules.md` §4's *"Never repair a non-brand family in place"* remains in full force: it forbids substituting for a **non-brand** family, which is a different operation from substituting for an **unobtainable brand** family.

The distinction matters because the two failures have different correct answers. A site declaring `Arial` has told us nothing about its brand, so there is nothing to preserve and inference is strictly better. A site declaring `Gotham` has told us exactly what its brand is; discarding that would destroy real evidence, so the name is preserved and a loadable stand-in is added behind it.

**Not governed by this file:**

- **Monospace.** The design-system emits no mono family token (`framework/skills/extract-brand-theme.md` — `--font-mono` keeps the template default), so there is nothing to substitute.
- **The artefact's documentation chrome**, which stays `system-ui` — see the `DOC CHROME` comment in `framework/assets/template-design-system.html`.
- **`/wireframe`**, which uses system fonts by design.

---

## 1. Availability classification

Every brand family token that survives `font-rules.md` §1 gets exactly one status:

| Status | Meaning | Token value | Emits a `<link>`? |
|--------|---------|-------------|-------------------|
| `google-native` | The family itself is Google-hosted. | `'<Family>', <generic>` — unchanged | Yes, for `<Family>` |
| `substituted` | The family is real and branded but **not** Google-hosted, on positive evidence. | `'<Brand>', '<Loadable>', <generic>` | Yes, for `<Loadable>` |
| `unverified` | Availability could not be established either way. | `'<Brand>', <generic>` — unchanged | **No** |

`status` is an **availability status, not a provenance marker.** The `prov` enum stays exactly two values — `extracted-from-url` and `inferred-from-domain` — per the locked decision in `framework/agents/design-system-styler.md`. A substituted token keeps whichever `prov` it already had; the substitution is a delivery concern, not a re-sourcing. `meta.extraction_status` is the precedent for a non-provenance status enum living in `meta`.

### The evidence ladder

Run in order per family; stop at the first tier that resolves. A typical run resolves at E1 or E2 and makes **zero** network calls.

**E1 — the site's own font delivery.** Free: the evidence is already on disk from step-04. Read `design-system/.workspace/computed-tokens.json` → `sources` (every stylesheet href the page loaded) and `design-system/.workspace/css-content.txt` (the aggregated CSS, including cross-origin sheets that step-04 §4.A.3 re-fetched).

- A `sources` href on `fonts.googleapis.com` whose `family=` segment names this family ⇒ **`google-native`**, and its `family=` segment is the **canonical spelling** — prefer it over §2's derived spelling, because the site has told us what Google calls the face.
- An `@font-face` block in `css-content.txt` whose `font-family` is this family and whose `src: url(...)` points at the site's own origin/CDN, `use.typekit.net`, `p.typekit.net`, `fonts.net`, `fast.fonts.com`, `cloud.typography.com`, `api.fontshare.com` or `cdn.fontshare.com` ⇒ **suspect licensed/self-hosted — continue to E2.**

  **Self-hosting is not proof of unavailability.** Plenty of sites self-host a face that *is* on Google Fonts (`next/font` self-hosts Inter; Vercel self-hosts Geist, which is Google-hosted). E1 may only *raise suspicion* here — it must never conclude `substituted` on its own. Concluding from self-hosting alone is the single most likely way to implement this feature wrongly.

**E2 — the curated table.** Canonicalise per §2, then look up §3 and §4.1.

- In §4.1 (verified Google-hosted) ⇒ **`google-native`**.
- In §3 (known proprietary) ⇒ **`substituted`**, using that row's primary substitute.
- Neither ⇒ continue to E3.

**E3 — live probe with a control.** Only reached when E1 and E2 are both inconclusive. Probe the candidate **and** a known-good control in the same step, using `WebFetch`:

```
WebFetch  url: https://fonts.googleapis.com/css2?family=<Canonical+Family>
          prompt: "Does this response contain @font-face rules? Answer only YES or NO."
```

- **Probe §2's candidate list in order, stopping at the first success.** A single name is not the unit of the test — `GeistSans` fails where its candidate `Geist` succeeds. Cap at the **first two** candidates per family (the full name, then the best-ranked rewrite): beyond two the list is speculative and a wrong hit is worse than an `unverified`.
- **One family per request.** A combined `?family=A&family=B` request returns **200 even when A does not exist** — Google silently drops unknown families — so a combined probe cannot detect anything.
- **No `:wght@…` axis.** Requesting an axis a family lacks still returns 200, so the axis adds nothing; omitting it keeps "family unknown" the only thing a failure can mean.
- **Control family: `Inter`.** Probe it once per run, the first time E3 runs — not once per candidate.
- **Cost ceiling: 5 requests per run** — up to 2 candidates × 2 family slots, plus 1 control. A run that would exceed it stops and takes `unverified` for whatever is unresolved.

| Candidates | Control | Verdict |
|-----------|---------|---------|
| any succeeds | — | `google-native`, under **that** candidate's spelling (which becomes the token value per §6.1) |
| all fail | succeeds | `substituted` — genuinely unavailable; choose the substitute per §3's classification fallback |
| all fail | fails | **`unverified`** — the network, not the font, is the problem |

Read a `WebFetch` error (400, network failure, timeout) as "did not succeed" — the point of the control is that we never have to distinguish *why* a request failed, only whether requests are working at all.

**E4 — `unverified`.** Nothing established the answer. Keep the brand family alone, emit no `<link>` for it, and disclose it at step-07. This is the fail-safe direction: **a real brand font is never silently replaced on weak evidence.**

### Inferred families skip the ladder

A family filled by step-05b's domain inference is `google-native` by construction — `prompt-templates/domain-inference.md` §C.1 draws only from §4.1. Assert membership; do not probe.

---

## 2. Canonicalisation

Google Fonts family names are **case-sensitive and space-sensitive**: `?family=inter` returns 400 while `?family=Inter` returns 200. And a CSS `font-family` rarely holds the Google name — it holds whatever the site's build called the face. Canonicalisation is therefore where most of this file's accuracy lives; skipping it produces confident wrong answers.

Produce an **ordered candidate list** from the raw name, then test candidates in order. The first candidate that resolves is the answer.

1. Strip surrounding quotes (`"Inter"` → `Inter`) and collapse internal whitespace runs to one space.
2. **Strip a variable-font build suffix**: a trailing `-var`, `-variable`, `-vf`, `Var`, `VF`, or `Variable` (`sohne-var` → `sohne`, `Inter-Variable` → `Inter`). These name a build artefact, never a family.
3. **Split delimiters and camel case.** If the name contains `-` or `_`, replace them with spaces (`sohne-var` → `sohne`, `founders-grotesk` → `founders grotesk`). If it is a single token in camel/PascalCase, split on the case boundaries (`GeistSans` → `Geist Sans`, `SourceSansPro` → `Source Sans Pro`).
4. Title-Case each word, then restore known all-caps and mixed-case names verbatim: `DM Sans`, `DM Serif Display`, `EB Garamond`, `IBM Plex Sans`, `IBM Plex Serif`, `PT Sans`, `PT Serif`, `Wix Madefor Display`. Numerals stay as digits: `Source Serif 4`, `Source Sans 3`, `Exo 2`.
5. **Fold diacritics into an additional candidate**, both directions — `Söhne` → `Sohne`. §3's *Brand family* column lists the ASCII and build-alias spellings sites actually declare (in parentheses); a match on one of those resolves to that row. A site will never write `Söhne` in CSS; it writes `sohne-var`.
6. **Add a trailing-word-trimmed candidate, ranked LAST.** Drop one trailing classification or style word — `Sans`, `Serif`, `Mono`, `Grotesk`, `Text`, `Display`, `Std`, `LT`, `Pro`, `Regular`, `Book` — to produce a final fallback candidate (`Geist Sans` → `Geist`).

**Step 6 is last for a verified reason, and the ordering is not negotiable.** Trimming is right exactly when the untrimmed name fails and wrong whenever it succeeds:

| Raw name | Untrimmed | Trimmed | Correct answer |
|---|---|---|---|
| `GeistSans` (Vercel) | `Geist Sans` → **400** | `Geist` → **200** | `Geist` — trimming is *essential*; without it a Google-hosted face is misread as proprietary and needlessly substituted |
| `Public Sans` | `Public Sans` → **200** | `Public` → 400 | `Public Sans` — never trim |
| `Instrument Sans` | `Instrument Sans` → **200** | `Instrument` → 400 | `Instrument Sans` — never trim |
| `DM Sans` | `DM Sans` → **200** | `DM` → 400 | `DM Sans` — never trim |
| `Plus Jakarta Sans` | `Plus Jakarta Sans` → **200** | `Plus Jakarta` → 400 | `Plus Jakarta Sans` — never trim |
| `Nunito Sans` | `Nunito Sans` → **200** | `Nunito` → 200 (a *different* real family) | `Nunito Sans` — trimming would silently swap one real family for another |

So: **always test the full name before any trimmed candidate, and stop at the first success.** Trim only to rescue a name that has already failed.

**A failed probe on a non-canonical spelling is never evidence of proprietariness.** A family is `substituted` only when **every** candidate in the list fails against a succeeding control. Exhaust the list first; one 400 on the raw name proves nothing.

---

## 3. Proprietary → Google-Fonts substitution table

Primary substitute first; alternates are for the step-07 revise conversation. Every name in the *Substitute* columns is drawn from §4.1 and honours §4.2's exclusions.

Match on the canonicalised family name; a row's *Brand family* column lists the variants that share a substitute.

### Geometric sans

| Brand family | Substitute | Alternates | Why |
|---|---|---|---|
| Gotham, Gotham Narrow, Gotham Book | **Montserrat** | Jost, Figtree | Tall caps, closed apertures, near-circular bowls. Montserrat is the closest widely-available match to Gotham's cap-driven geometry. |
| Gotham Rounded | **Nunito** | Quicksand | Same geometry with rounded terminals. |
| Futura, Futura PT, Futura Now | **Jost** | Josefin Sans | Jost is an explicit open Futura revival — single-storey `a`, pointed `A` apex. |
| Avenir, Avenir Next, Avenir Next LT | **Nunito Sans** | Jost, Montserrat | Humanist-tempered geometry; Nunito Sans keeps the warmth Jost loses. |
| Circular, Circular Std (`circular-std`, `CircularStd`) | **Figtree** | Poppins, Manrope | Circular's uniform stroke and wide bowls; Figtree matches the x-height better than Poppins. |
| Brandon Grotesque, Brandon Text | **Josefin Sans** | Montserrat | Small x-height, geometric caps, art-deco flavour. |
| Sofia Pro, Cera Pro, Larsseit, Objektiv | **Poppins** | Outfit | Monolinear geometric sans with a large x-height. |
| Proxima Nova, Proxima Sans | **Montserrat** | Mulish, Figtree | Sits between geometric and humanist. Montserrat for display use, Mulish when the site used it as body text. |
| Museo Sans | **Rubik** | Cabin | Slightly slabbed geometric sans. |
| Century Gothic, Brown, Questrial-likes | **Jost** | Poppins | Wide circular geometry. |
| Halyard, Camphor | **Mulish** | Figtree | Neutral geometric text sans. |

### Neo-grotesque & grotesque sans

| Brand family | Substitute | Alternates | Why |
|---|---|---|---|
| Söhne (`sohne`, `sohne-var`, `Sohne`), Söhne Breit, Neue Haas Grotesk (`neue-haas-grotesk`), Helvetica Now, Akzidenz-Grotesk, Aktiv Grotesk, Suisse Int'l (`suisse-intl`), Untitled Sans, Maison Neue, Colfax, Calibre, Metric, ABC Diatype, Sharp Grotesk | **Inter** | Archivo, Public Sans | The de-facto open neo-grotesque: horizontal terminals, tight apertures, drawn for UI text sizes. The default answer for any Helvetica-lineage licensed face. `sohne-var` is the spelling Stripe actually ships — verified live, and the reason §2 folds diacritics and strips `-var`. |
| Graphik, Apercu, GT America, Basis Grotesque, Styrene | **Archivo** | Public Sans, Inter | Slightly more character than Inter in the `a`/`g`, matching Graphik's warmth. |
| Founders Grotesk, Neue Montreal, Aeonik, TT Norms, Sequel Sans | **Space Grotesk** | Familjen Grotesk, Schibsted Grotesk | Quirkier grotesques with distinctive `R` and `g`. |
| Whitney, Interstate, Benton Sans | **Public Sans** | Archivo, Asap | Signage-lineage grotesques; Public Sans shares the Interstate-adjacent ancestry. |
| National, Founders Grotesk Text | **Archivo** | Golos Text | |
| Klavika, Eurostile, Bank Gothic | **Rajdhani** | Saira, Michroma | Squarish technical letterforms. |

### Humanist sans

| Brand family | Substitute | Alternates | Why |
|---|---|---|---|
| Gill Sans, Gill Sans Nova | **Lato** | Cabin | Humanist proportions, calligraphic skeleton. |
| Myriad, Myriad Pro | **Source Sans 3** | Assistant | Adobe's own open humanist sans — the nearest thing to a licensed-free Myriad. |
| Frutiger, Univers | **Archivo** | Encode Sans, Titillium Web | Open apertures, signage clarity. Deliberately **not** Roboto Condensed — see §4.2. |
| FF Meta, Officina Sans | **Chivo** | Assistant | |
| Effra | **Cabin** | Karla | |

### Condensed, display & compressed

| Brand family | Substitute | Alternates | Why |
|---|---|---|---|
| DIN, DIN Next, DIN Pro | **Barlow** | Barlow Condensed, Archivo Narrow | Use Barlow at normal width, Barlow Condensed when the site used condensed. |
| Trade Gothic, Trade Gothic Condensed | **Barlow Condensed** | Archivo Narrow, Oswald | |
| Knockout, Druk, Monument Extended | **Anton** | Bebas Neue, Unbounded | Compressed display weight. |
| Tungsten | **Bebas Neue** | Oswald | Condensed all-caps display. |

### Serif — text

| Brand family | Substitute | Alternates | Why |
|---|---|---|---|
| Tiempos, Tiempos Text, Publico, Chronicle Text, Freight Text | **Source Serif 4** | Lora, Newsreader | Contemporary transitional text serifs with sturdy, low-contrast strokes. |
| Sabon, Garamond, Adobe Garamond, Granjon | **EB Garamond** | Cormorant Garamond | Old-style; EB Garamond for text, Cormorant only for display (its contrast is far higher). |
| Caslon, Adobe Caslon | **Libre Caslon Text** | Libre Baskerville | |
| Baskerville, Mrs Eaves | **Libre Baskerville** | Petrona | |
| Minion, Minion Pro | **Crimson Pro** | Spectral | |
| Miller, Mercury | **Newsreader** | Spectral | Scotch/news serif. |
| Guardian Egyptian, Chronicle Display | **Petrona** | Domine | |

### Serif — display

| Brand family | Substitute | Alternates | Why |
|---|---|---|---|
| Didot, Bodoni, Bodoni Std | **Libre Bodoni** | Playfair Display, Bodoni Moda | Didone: extreme contrast, hairline serifs. |
| Canela, GT Sectra, Domaine Display | **Fraunces** | Instrument Serif | Contemporary high-contrast display serifs. |
| Trajan, Trajan Pro | **Marcellus** | Cormorant Garamond | Inscribed Roman capitals. |
| Recoleta | **Fraunces** | Petrona | Soft display serif. |

### Slab

| Brand family | Substitute | Alternates | Why |
|---|---|---|---|
| Rockwell, Clarendon, Sentinel | **Zilla Slab** | Bitter, Domine | Deliberately **not** Roboto Slab — see §4.2. |
| Archer | **Bitter** | Aleo | Slab with a geometric skeleton. |

### Free but not Google-hosted

These are widely used on modern product sites and read as "free", so they are easy to assume are Google-hosted. They are not — `Satoshi`, `General Sans` and `Switzer` were each confirmed 400.

| Brand family | Substitute | Alternates | Why |
|---|---|---|---|
| Satoshi (`Satoshi-Variable`) | **Plus Jakarta Sans** | Manrope | Fontshare. Neutral geometric sans with a tall x-height. |
| General Sans (`GeneralSans`, `GeneralSans-Variable`) | **Public Sans** | Inter | Fontshare. Note the trimmed candidate `General` also 400s, so this row is what catches it. |
| Switzer (`Switzer-Variable`) | **Inter** | Archivo | Fontshare. Swiss neo-grotesque. |
| Clash Display, Clash Grotesk | **Familjen Grotesk** | Space Grotesk, Bricolage Grotesque | Fontshare. |
| Cabinet Grotesk | **Schibsted Grotesk** | Space Grotesk | Fontshare. |

### Classification fallback — the unlisted case

A bespoke commissioned face ("Acme Sans") will never be in the table. Classify it from whatever the inputs already say and pick from the ranked defaults below. Signals, in order of reliability: the `@font-face` `src` filename (`AcmeSans-Bold.woff2` names its own weight and family); the generic terminal the site itself declared (`serif` vs `sans-serif`); the family name's own suffix (`Sans`, `Serif`, `Slab`, `Mono`, `Display`, `Condensed`, `Rounded`, `Grotesk`/`Grotesque`); the site's `[SRC]`-cited voice or industry.

| Classification | Ranked defaults |
|---|---|
| Sans — neutral / unknown | **Inter**, Archivo, Public Sans |
| Sans — geometric | **Poppins**, Montserrat, Jost |
| Sans — grotesque / quirky | **Space Grotesk**, Familjen Grotesk |
| Sans — humanist | **Source Sans 3**, Lato, Cabin |
| Sans — rounded | **Nunito**, Quicksand |
| Sans — condensed | **Barlow Condensed**, Archivo Narrow |
| Serif — text | **Source Serif 4**, Lora |
| Serif — display / high contrast | **Playfair Display**, Fraunces |
| Serif — old-style | **EB Garamond**, Crimson Pro |
| Slab | **Zilla Slab**, Bitter |
| Display / compressed | **Anton**, Bebas Neue |

When nothing distinguishes the face beyond serif-vs-sans, take the first row of the matching class. **Do not** measure glyph metrics, and do not invent a matching procedure — the ranked default is the answer, and the substitution is disclosed at step-07 where the consultant can change it.

---

## 4. Verified Google-hosted families

### 4.1 The verified list

Each name below returned a successful `css2?family=<name>` response when this file was authored. This list has two jobs: it is the pool substitutes are drawn from, and it is what step-06 §C checks every `meta.brand_fonts.families[].param` against.

**Sans:** Albert Sans, Alexandria, Alegreya Sans, Archivo, Archivo Black, Archivo Narrow, Asap, Assistant, Barlow, Barlow Condensed, Be Vietnam Pro, Bricolage Grotesque, Cabin, Chivo, Commissioner, DM Sans, Encode Sans, Epilogue, Exo 2, Familjen Grotesk, Figtree, Fira Sans, Funnel Display, Funnel Sans, Gabarito, Geist, Geologica, Golos Text, Heebo, Hind, Host Grotesk, IBM Plex Sans, Inter, Instrument Sans, Josefin Sans, Jost, Kanit, Karla, Lato, Lexend, Mada, Manrope, Montserrat, Mukta, Mulish, Nunito, Nunito Sans, Onest, Open Sans, Outfit, Overpass, Plus Jakarta Sans, Poppins, PT Sans, Public Sans, Quicksand, Radio Canada, Raleway, Rajdhani, Red Hat Display, Rubik, Saira, Sarabun, Schibsted Grotesk, Sen, Sora, Source Sans 3, Space Grotesk, Syne, Titillium Web, Unbounded, Urbanist, Wix Madefor Display, Wix Madefor Text, Work Sans, Ysabeau

**Serif:** Aleo, Alegreya, Amiri, Andada Pro, Arvo, Bitter, Bodoni Moda, Cormorant, Cormorant Garamond, Crete Round, Crimson Pro, DM Serif Display, Domine, EB Garamond, Faustina, Fraunces, Frank Ruhl Libre, Gelasio, Gentium Book Plus, Gilda Display, IBM Plex Serif, Instrument Serif, Italiana, Josefin Slab, Libre Baskerville, Libre Bodoni, Libre Caslon Text, Literata, Lora, Manuale, Marcellus, Marcellus SC, Merriweather, Newsreader, Noto Serif Display, Petrona, Piazzolla, Playfair Display, Prata, PT Serif, Rokkitt, Rufina, Source Serif 4, Spectral, Trirong, Vollkorn, Yrsa, Zilla Slab

**Display:** Abril Fatface, Anton, Antonio, Bebas Neue, Comfortaa, Michroma, Oswald, Syncopate, Tenor Sans

**Also Google-hosted, but see §4.2 — legal as an *extracted* family, never as a substitute:** Arimo, Cantarell, Cousine, Droid Sans, Noto Sans, Noto Serif Display, Oxygen, Roboto, Roboto Condensed, Roboto Slab, Tinos, Ubuntu

These belong in the assertion pool because a site may legitimately declare one as its brand font (`font-rules.md` §1 group (c) accepts `Roboto` in first position), but §4.2 forbids choosing one as a stand-in.

**Maintenance.** Append only; never remove a row. Adding a family means probing it first — `css2?family=<Name>` must succeed for the exact spelling written here. A family absent from this list is not evidence of anything; it means nobody has checked.

**This list is a cache of past probes, not the definition of what exists.** A family verified this run by E1 (a `fonts.googleapis.com` href on the source page) or E3 (a successful probe) is `google-native` even if it is absent here — first-hand evidence outranks the cache, and step-06 §C's `param` assertion is written to accept it. Legacy names behave this way: `Source Sans Pro` and `Source Serif Pro` both still resolve but are not listed, because §4.1 carries the current names (`Source Sans 3`, `Source Serif 4`). A **substitute**, by contrast, must always come from this list — we are choosing it, so there is no reason to choose an unverified one.

### 4.2 Never usable as a substitute

These are Google-hosted, so they belong in §4.1's assertion pool, but they must **never** be chosen as a substitute:

- **`font-rules.md` §1 group (c) — position-dependent:** `Roboto`, `Noto Sans`, `Ubuntu`, `Cantarell`, `Oxygen`, `Droid Sans`. A substitute always lands in **second** position, which is exactly where group (c) classifies these as platform fallbacks rather than brand choices. Choosing one would make the emitted stack self-contradictory.
- **`font-rules.md` §1 group (b) — metric clones:** `Arimo` (Arial), `Tinos` (Times New Roman), `Cousine` (Courier New). Substituting `Arimo` for `Helvetica` would smuggle an Arial clone into a brand token — precisely the defect `font-rules.md` §1 exists to prevent.
- **Any family whose name *contains* a group-(c) name:** `Roboto Condensed`, `Roboto Slab`, `Noto Serif Display`. These are not literally group-(c) members, so `font-rules.md` §1 would permit them — but step-06's brand-family assertion scans the token value for prohibited names, and `'Rockwell', 'Roboto Slab', serif` contains the substring `Roboto`. Excluding them keeps the assertion safe to implement as a plain scan.

**The §1 membership test itself is on the whole family name, not a substring.** `Roboto Slab` is not `Roboto`. §4.2's third bullet avoids relying on that distinction rather than contradicting it; a substitute is never a family this rule has to adjudicate.

---

## 5. Non-brand → allowed alternative

The **other** axis, kept here so the pairs live in one place. These families fail `font-rules.md` §1, so their outcome is *unset + domain inference* — **not** substitution. This map exists only so step-07 §B can name a concrete alternative when a consultant asks for one of them by hand, and so the decline is helpful rather than bare.

| Consultant asked for | Name this instead |
|---|---|
| Arial, Arial Nova | Inter |
| Helvetica, Helvetica Neue | Inter or Manrope |
| Segoe UI, SF Pro, system-ui | Inter |
| Georgia, Times New Roman, Times | Source Serif 4 |
| Verdana, Tahoma | Source Sans 3 |
| Trebuchet MS | Cabin |
| Calibri, Candara | Lato |
| Courier New, Consolas | *n/a — the design-system emits no mono token* |

Do not read this table as a substitution table. Nothing here produces a two-name stack; the requested family is never written into a token in any position.

---

## 6. Emitted values & link building

### 6.1 Token value shapes

| Status | Shape | Example |
|---|---|---|
| `google-native` | `'<Family>', <generic>` | `'Inter', sans-serif` |
| `unverified` | `'<Brand>', <generic>` | `'Acme Sans', sans-serif` |
| `substituted` | `'<Brand>', '<Loadable>', <generic>` | `'Gotham', 'Montserrat', sans-serif` |

**The token carries the resolved name, not the raw declaration.** When §2 resolves a candidate that differs from what the CSS declared, the resolved spelling is what goes into the token and into `param`; the raw alias goes into `evidence` only. `GeistSans` becomes `'Geist', sans-serif`, and `sohne-var` becomes `'Söhne', 'Inter', sans-serif` using §3's row name. The raw form is a build artefact that means nothing outside that site — the same reason `font-rules.md` §1 group (d) rejects `__Inter_abc123` outright. Shipping `'GeistSans', sans-serif` would name a family no one else can resolve *and* fail to load, which is the worst of both.

The three-name shape is the **only** permitted extension to `font-rules.md` §4's emitted stack shape, and only when a matching `substituted` record exists in `meta.brand_fonts.families` for that slot, with `brand` and `loadable` appearing in that order. Both named families are single-quoted; the generic terminal is required exactly as `font-rules.md` §4 requires it, and matches the *brand* family's classification (a serif brand keeps `serif` even if its substitute is listed under a different heading — they are the same classification by construction).

Brand-first is deliberate: the brief's headline stays the client's actual typeface, the cascade performs the substitution at render time, and a machine that has the licensed face installed renders the real thing with no further change.

### 6.2 The `meta.brand_fonts` record

Assembled once, in step-05b §G, and consumed verbatim by step-06 and by `/prototype` downstream. No consumer may re-derive which name is fetchable.

```json
"brand_fonts": {
  "families": [
    { "role": "heading", "brand": "Gotham", "loadable": "Montserrat", "param": "Montserrat",
      "status": "substituted",
      "evidence": "self-hosted @font-face (cdn.example.com); probe 400, control 200" },
    { "role": "body", "brand": "Inter", "loadable": "Inter", "param": "Inter",
      "status": "google-native",
      "evidence": "site loads it via fonts.googleapis.com" }
  ],
  "links": [
    "https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap",
    "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap"
  ]
}
```

- `families` always has exactly two entries, `role: "heading"` then `role: "body"`, even when both resolve to the same face.
- `loadable` equals `brand` when `status` is `google-native`. When `status` is `unverified`, `loadable` and `param` are both `null`.
- `param` is `loadable` with spaces replaced by `+` (`Source Serif 4` → `Source+Serif+4`). No other escaping is needed for any name in §4.1.
- `evidence` is a short free-text record of which ladder tier decided it. It is read by step-07 for the disclosure line and by a human auditing the run; nothing branches on its text.

### 6.3 Link building

One `<link>` per **distinct** `param`, in `families` order, deduped when heading and body share a face:

```
https://fonts.googleapis.com/css2?family=<param>:wght@400;500;600;700&display=swap
```

- **One family per link, never a combined `family=A&family=B` request.** A combined request returns 200 even when one family does not exist, so a mistake becomes invisible; separate links keep each face's success or failure its own.
- Weights are always `400;500;600;700`. Over-requesting is harmless — a family with fewer weights still returns 200 and serves what it has — and this axis covers both weight tokens plus the `font-medium`/`font-semibold` utilities the prototype primitives use. Do not compute a narrower list.
- `display=swap` is required, so text paints immediately in the fallback rather than blocking on the fetch.
- A family with `status: "unverified"` contributes **no** link. If neither family is loadable, `links` is `[]`.

---

## 7. Anti-patterns

- **Do not substitute on `unverified`.** An offline run must leave the brand family untouched. Substituting on absence-of-evidence is how a client's real typeface gets silently replaced by a lookalike — the worst outcome this whole file exists to prevent, and worse than the problem it would be trying to solve.
- **Do not conclude from self-hosting alone.** Many Google-hosted faces are self-hosted (`next/font`, Geist). E1 raises suspicion; E2 or E3 decides.
- **Do not substitute for a `font-rules.md` §1 family.** That axis's answer is *unset + infer*, and it has not changed. §5 is a naming aid for a conversation, not a substitution path.
- **Do not combine families** in a probe or in a `<link>`. Both mask a missing family behind a 200.
- **Do not add a provenance marker.** `prov` has exactly two values. Availability lives in `meta.brand_fonts[].status`.
- **Do not treat a probe failure on a non-canonical spelling as evidence.** Canonicalise per §2 and exhaust the whole candidate list first; `?family=inter` returns 400 for a family that plainly exists.
- **Do not conclude `substituted` from the raw CSS name.** The worked example, verified live: Vercel's `font-family` is `GeistSans, "GeistSans Fallback"`. `GeistSans` → 400. `Geist Sans` → 400. `Geist` → **200**, and `Geist` is a real Google family. Substituting Inter here would replace a perfectly loadable brand font with a lookalike on the strength of a build-time alias — the exact false positive §2's candidate list exists to prevent. Sites name faces after their build artefacts, not after Google's catalogue.
- **Do not unset a family because it is unavailable.** Availability never destroys extracted evidence — that is the whole distinction in §0.
- **Do not measure glyph metrics** to rank substitutes. §3's table and its classification fallback are the answer; the consultant revises at step-07 if they disagree.
