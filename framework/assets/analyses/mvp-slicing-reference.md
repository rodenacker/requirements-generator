<!-- ROLE: asset (P2 analysis reference). Loaded by framework/agents/analyses/mvp-slicing-analyser.md at activation. -->

# analyses/mvp-slicing-reference.md

**Purpose:** Methodology reference for **MVP slicing** — Jeff Patton's User-Story Mapping (backbone + a walking-skeleton release-slice line) crossed with the DSDM **MoSCoW** prioritisation board. The analyser follows this document literally and exhaustively.

**The defining constraint of this lens: it reads the cut, it never makes it.** Priorities already exist in `requirements/requirements.md` (the `Priority` field on §6.1 / §6.4 / §4.2, set by `GR-24` at merge time). This methodology *visualises* them as a release slice and a board — it does not re-prioritise, score, or infer. There is no effort axis and no value axis to compute; every value on the artefact is read verbatim or routed deterministically. **This methodology emits zero `[AI-SUGGESTED]` markers** because it performs zero content inference: a card that cannot be sourced or linked is *routed* (to a Supporting column or an Unprioritised band), never invented.

**Used by:**

- `framework/agents/analyses/mvp-slicing-analyser.md` — drives the agent's five-round process plus the quality-check sweep.
- `framework/skills/map-mvp-slicing-to-ui.md` — downstream consumer (stub).

**Output produced by the analyser:** `analyse-requirements/MVP-SLICING/mvp-slicing.html` — a self-contained HTML artefact (story map + MoSCoW board) using `framework/assets/analyses/template-mvp-slicing.html` as scaffold, plus the structured sidecar `analyse-requirements/MVP-SLICING/mvp-slicing.sidecar.json`.

---

## Upstream input contract

MVP slicing is a **prioritisation lens onto the requirements the BA already prioritised** — never a re-prioritisation. The analyser reads the **clean merged** `requirements/requirements.md`: the `Priority` cell on each §6.1 F-NN row, §6.4 UI-NN row, and §4.2 story is a plain `Must` / `Should` / `Could` / `Won't` token (the `[STANDARD-RULE: GR-24]` / `[SRC: C-NNN]` markers were stripped at merge). The analyser takes that token as-authored.

`GR-24` is referenced **only** to (a) sanity-check whether each `Must` card is GR-24-consistent (a *soft* flag — the consultant may have hand-edited a priority, which GR-24 explicitly permits) and (b) phrase the human-readable rationale line. The analyser never recomputes a priority from the §1.5 buckets or §4 goal links.

**Source-of-truth hierarchy (priority order):**

1. **§5 Task flows** — the backbone activities and their left-to-right order (the spine). Each `### Flow:` is one backbone activity.
2. **§4.1 Goals** — the backbone *fallback* when §5 is absent (top-level goals become columns); also a cross-link target for placing cards.
3. **§4.2 Stories / §6.1 F-NN / §6.4 UI-NN** — the cards. Their `Priority` field is canonical and read verbatim.
4. **GR-24** (`framework/shared/general-rules.md`) — the *definition* of the four buckets, used for the Must-consistency soft check and the rationale line only.

If §5 is absent the backbone falls back to §4.1 top-level goals; if §4.1 is also absent the map degrades to a single "All requirements" column. The chosen path is recorded in the artefact's `Backbone source` meta field so the consultant can see how anchored the backbone is.

---

## The MVP-slicing process

Five rounds, executed in order. The analyser does not skip or collapse rounds — each round's output feeds the next, and round-by-round structure is what makes the slice auditable.

### Round 1 — Backbone discovery

Build the ordered set of **backbone activities** (the columns of the story map):

- **Primary path — §5 present.** Walk `§5 Task flows` in document order. Each `### Flow: <name>` becomes one backbone activity `{backbone_id, activity_label: <flow name>, source: "§5:Flow «<name>»", order: <document order>, provenance: from-§5}`. The flow's ordered *Steps* are captured as a short narrative caption on the backbone cell (context only — steps are **not** themselves columns, because cards link to flows, not to individual steps; making steps the columns would force step-level placement inference, which this lens forbids).
- **Fallback 1 — no §5, §4.1 present.** Use **top-level** §4.1 goals (`goal_kind = top-level`) as backbone activities, in §4.1 document order. `provenance: derived-from-§4.1`. Sub/interaction goals are not columns.
- **Fallback 2 — no §5 and no §4.1.** A single backbone activity "All requirements" (`provenance: single-column`). The map degrades to a pure priority stack with a slice line — still valid.

A trailing **"Supporting"** column is appended later (Round 3) iff any card cannot be linked to a backbone activity.

### Round 2 — Card extraction (priority read verbatim)

Walk §6.1 (F-NN), §6.4 (UI-NN), and §4.2 (stories), in that order. Each becomes a card `{card_id, kind ∈ {functional, ui, story}, text, priority, source}`:

- `card_id` — the requirement ID verbatim: `F-NN`, `UI-NN`, or for a story a stable anchor `story:<persona>/«<intent>»` that is itself a verbatim substring of the doc (stories carry no numeric ID).
- `text` — the §6.1 *Statement* / §6.4 *Feature need* / §4.2 *Objective*, verbatim.
- `priority` — **read verbatim** from the row's `Priority` cell: one of `Must` / `Should` / `Could` / `Won't`. If the cell is blank or absent, `priority = unset` (flagged — never guessed).
- `source` — the section the card came from.

The analyser does **not** apply GR-24 here. The merge step already did.

### Round 3 — Cross-link cards to backbone activities

Place each card under a backbone activity using **only** the explicit cross-references in `requirements.md`:

- **§4.2 story** → its `Linked task flow (→ §5)` field, if set, names the flow column. Else its `Goal (→ §4.1)` — if that goal is a backbone column (fallback path), use it. Else → Supporting.
- **§6.4 UI-NN** → its `Linked (G / story / BR)` field: a linked story resolves to that story's flow column; a linked goal that is a column → that column; a BR link or no resolvable column → Supporting (BR links never create a column).
- **§6.1 F-NN** → follow its `Source (→ §X)` ref-chain: a §5 flow → that column; a §4.1 column-goal → that column; a story that is itself placed → that story's column. Else → Supporting.

Each placement carries exactly one link-provenance marker: `from-link` (a direct field link) or `derived-from-ref-chain` (a followed Source chain). A card that resolves to no column goes to the trailing **"Supporting"** column — it is **never** invented onto an arbitrary activity. Append the Supporting column iff it holds ≥1 card.

### Round 4 — Slice & MoSCoW partition (single structure)

Compute **one** in-memory structure that both rendered sections derive from, so the story map and the MoSCoW board can never disagree:

- **Release bands (the map):** `Must` → MVP band (above the slice line); `Should` → Release-2 band; `Could` → Later band; `unset` → Unprioritised band (below Later, hatched). **`Won't` is not placed on the map** — a release map shows what *will* ship; `Won't` = "not this build". 
- **MoSCoW buckets (the board):** all cards partitioned into the four columns `Must` / `Should` / `Could` / `Won't`, plus an `unset` overflow surfaced as a flagged note. The board shows `Won't` (greyed, collapsed) for completeness — the scope decision stays visible, never silently dropped.
- **The proposed MVP = exactly the `Must` set.** The analyser may not add or remove an item for "balance" or "completeness".
- **Must-consistency soft check:** for each `Must` card, check it is GR-24-consistent (in §1.5 In, linked to a top-level §4.1 goal or a §5 happy-path step). Inconsistent `Must` cards are *flagged* (`.gr24-flag`), not moved — GR-24 lets the consultant adjust priorities.

### Round 5 — Roll-up & coverage

Compute the counts and coverage signals: per-bucket counts; cards mapped vs in Supporting (`N_SUPPORTING`); backbone activities with zero cards (coverage gaps); `unset`-priority count; GR-24-inconsistent `Must` count; and the one-line `MVP_RATIONALE_LINE` (a *factual* statement derivable from the placed data — e.g. "covers every core-flow step of the «Submit claim» backbone end to end" — never a value judgement; falls back to a literal GR-24 restatement when nothing factual can be said).

---

## Output presentation

The artefact renders top-to-bottom, plain-terms lead first:

0. **In plain terms** (`<section id="plain-terms">` with `{{PLAIN_SUMMARY}}`) — a 2–5 sentence plain-English lead: what this MVP-slicing analysis is, what it found, and what the consultant should do with it. The **first** section, above the meta-grid. A faithful condensation of the content below — it introduces no fact, count, or citation not already present, and carries no `[SRC]` of its own. Methodology jargon (MVP, slice, MoSCoW, phase/release, walking skeleton) is glossed at first use here; client domain terms are not glossed (the GLOSSARY methodology owns those). Per `framework/shared/output-readability.md`.
1. **Overview** — meta-grid + the **proposed-MVP callout** banner (the convergence headline: *"Proposed MVP — N Must items; confirm or adjust before client hand-off"*).
2. **Story map** — backbone-activity columns (left-to-right in flow order) × release bands (MVP band above the slice line; Release-2, Later, Unprioritised below). Each card is a tile carrying `data-src` (its requirement ID), `data-priority` (verbatim), `data-activity`, and (where known) `data-goal` / `data-flow`. The slice line is a full-width divider labelled with the Must count.
3. **MoSCoW board** — four columns (Must / Should / Could / Won't). `Won't` is greyed and collapsed.
4. **Diagnostics** — collapsed `<details>`: per-check PASS/FAIL lines, soft warnings, the counts summary, and an embedded `<script type="application/json" id="mvp-slice">` machine dump (every card `{id, kind, priority, activity, goal, flow}`, every backbone activity, and the Must set) so a downstream verifier can re-derive the slice without parsing HTML.

Card markup is **shared** between the map and the board so a reader recognises the same card in both; both views derive from the single Round-4 structure.

---

## Quality checks (run after Round 5, before write)

Each hard check is a gate. On any hard failure the analyser does **not** write the artefact — it surfaces a structured error and halts per `framework/agents/analyses/mvp-slicing-analyser.md > Step 8`.

1. **Every card is sourced.** Every card's `data-src` (the `F-NN` / `UI-NN` token, or the `story:<persona>/«intent»` anchor) is a verbatim substring of `requirements/requirements.md`. No fabricated IDs. *(Most load-bearing.)*
2. **Every card has a priority read verbatim.** `data-priority` ∈ {Must, Should, Could, Won't} equals the row's `Priority` cell byte-for-byte, or is `(unset)`. `unset` cards fail this check (forcing the prompt) — the analyser never guesses a priority.
3. **Proposed MVP == Must set.** `MVP_ITEM_COUNT == MUST_COUNT`, and the set of cards in the MVP band equals the set of `data-priority="Must"` cards, equals the Must board column.
4. **Every backbone activity is sourced.** Each backbone column's `data-src` resolves to a real §5 flow, a real §4.1 goal, or the `single-column` sentinel. No invented activities.
5. **Card conservation.** `CARD_COUNT == count(§4.2 stories) + count(§6.1 F-NN) + count(§6.4 UI-NN)`. Unmapped cards are in the Supporting column, never deleted.
6. **Counts reconcile.** `MUST + SHOULD + COULD + WONT + unprioritised == CARD_COUNT`.
7. **No literal placeholders.** Zero `{{...}}` tokens remain in the rendered output.

**Soft checks (warnings — non-blocking, surfaced in diagnostics + handback):**

- **all-Must** — every card is `Must`; MoSCoW provides no prioritisation signal. Recommend the consultant re-examine §1.5 scope buckets.
- **coverage-gap** — a backbone activity has zero cards (a user action with no feature/story).
- **high-Supporting** — `N_SUPPORTING / CARD_COUNT > 0.40`; the backbone is under-specified (many requirements carry no §5/§4 link).
- **gr24-inconsistent-Must** — a `Must` card is not GR-24-consistent; surfaced for the consultant to confirm the hand-edit.

---

## Anti-patterns

- **Re-prioritising.** Never invent, score, or recompute a priority. The `Priority` field is read verbatim; GR-24 is for validation + rationale only.
- **Inventing a backbone activity.** Every column is a real §5 flow, a real §4.1 goal, or the single-column sentinel.
- **Inventing a card-to-activity link.** Unlinkable cards go to the Supporting column — never hung on an arbitrary activity for tidiness.
- **Putting `Won't` on the map.** `Won't` is board-only (shown greyed). The release map carries only what ships.
- **Letting the two sections disagree.** Both render from the single Round-4 structure.
- **Emitting `[AI-SUGGESTED]`.** This lens performs no inference; there is nothing to mark. Content that cannot be sourced is routed, not flagged.
- **Editorialising.** The rationale line is factual, derived from placed data — not a product opinion. The lens surfaces the cut the BA already made; it does not argue for a different one.

---

## Voice and stance

The analyser's stance is defined in `framework/assets/characters/mvp-slicing-analysis.md` — literal, slice-decisive, completeness-over-omission, provenance-honest, converging. The reference here defines **what** to do; the character file defines **how** the agent talks while doing it.

## Readability standard

This artefact is read by a human (the consultant, sometimes a client stakeholder) as well as consumed downstream by `/wireframe`'s `blueprint-architect` (optionally, via the per-analysis sidecar). The operative rules are restated in the character's *Reader & plain language* block; the canonical definition is `framework/shared/output-readability.md`. In brief:

- The "In plain terms" lead (`{{PLAIN_SUMMARY}}`) is 2–5 sentences: a faithful condensation of what the analysis is, what it found, and what the consultant should do — no new fact, no `[SRC]`.
- Methodology jargon is glossed at first use in the lead (e.g. "MVP (the smallest releasable version)", "slice (a thin end-to-end increment)", "MoSCoW (must / should / could / won't)", "walking skeleton (the lightest end-to-end thread)"). Client domain terms are **not** glossed here.
- The plain-English layer is confined to the lead and first-use glosses. The structured body (story map, MoSCoW board, diagnostics) keeps its concrete, telegraphic discipline.
- Every `[SRC: C-NNN]` marker is kept. Never demote or drop them.
