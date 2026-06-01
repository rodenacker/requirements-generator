# Prototype UX-posture registry (`design-philosophies.md`)

**Role:** asset (prototype-private).

**Purpose:** Provide the consultant a curated, named set of **UX postures** — the selectable "design philosophy" of `/prototype` (rule 9). In a prototype, the **visual brand is fixed and identical across all prototypes** (one `theme.css`, one shared component set); the *only* thing that differs between prototypes is the **UX approach** — how the design reshapes **layout and workflows**. Each posture is a curated **preset** over the active trade-off dimensions plus the concrete structural choices it implies. The chosen posture + tuned positions are the "design parameters" (rule 12) the LLM uses to make layout/workflow decisions during generation (rule 10).

**This file owns only new content** (the same additive pattern `framework/assets/wireframes/domain-defaults.md` uses): the posture → starting-position-vector **presets**, posture characterizations, and posture → structural/realization recommendations.

**Inherits from / references (never redefines):**
- `framework/assets/wireframes/tradeoff-dimensions-registry.md` — canonical owner of the dimensions (D1–D6), their poles, applicability (§2), incoherent-pairs (§4), and persona-position rules (§5). This file references those by name and **must not restate** them. New posture-derived incoherent pairs are appended **there**, not here.
- `framework/assets/wireframes/position-vocabulary.md` — canonical owner of the plain-English `(dimension, position)` labels. This file references those labels; it never invents new ones.
- `framework/assets/prototypes/ux-baseline-checklist.md` — the non-negotiable UX floor every prototype satisfies regardless of posture.

**Used by:**
- `framework/orchestrators/prototype-orch.md` — Step B surfaces the posture list and (after a pick) the posture's default positions for confirm/tune.
- `framework/agents/prototype-spec-drafter.md` — reads the chosen posture's structural/realization recommendations to draft per-surface realization decisions and the workflow design.

---

## Active-dimension constraint (read first)

Per `tradeoff-dimensions-registry.md > Section 1`, **D6 memorability-discoverability is currently inactive** (pending an upstream rename; `position-vocabulary.md` carries no D6 labels). Therefore:

- Posture presets specify **signed positions on D1–D5 only** (`-2 .. +2`, poles per the registry).
- A posture's stance on *recall-vs-discoverability* (terse expert chrome ↔ verbose signposting) is captured in the posture's **structural choices prose** (navigation / disclosure / chrome), **not** as a D6 numeric position. Every preset records `D6 = 0`.
- When the upstream rename lands and D6 activates, the recorded prose stance converts to a numeric D6 default with no other change.

Dimension poles (mirrored from the registry for reading convenience — the registry is canonical):

| ID | Dimension | `-2` pole | `+2` pole |
|---|---|---|---|
| D1 | speed-accuracy | maximally accurate / careful | maximally fast / throughput |
| D2 | power-simplicity | maximally simple / novice-first | maximally powerful / expert-first |
| D3 | density-focus | maximally focused / sparse | maximally dense |
| D4 | control-automation | full manual control | full automation |
| D5 | flexibility-consistency | bespoke per-context | rigidly consistent |
| D6 | memorability-discoverability | *(inactive — neutral only)* | *(inactive — neutral only)* |

---

## Posture → position-preset matrix

Default positions; the consultant confirms or tunes them in Step B. All presets are checked against `tradeoff-dimensions-registry.md` §4 (incoherent pairs) and §5 (persona-position rules) — none violate a hard rule; soft-warn cells are noted per posture.

| # | Posture | D1 speed-accuracy | D2 power-simplicity | D3 density-focus | D4 control-automation | D5 flexibility-consistency | D6 | Default persona trait |
|---|---|---|---|---|---|---|---|---|
| P1 | Efficiency-First / Power-Operator | +2 | +2 | +1 | -1 | -1 | 0 | daily / high-volume |
| P2 | Guided / Novice-Safe | -1 | -2 | -1 | +1 | +1 | 0 | occasional / first-time |
| P3 | Analytical / Information-Dense | -1 | +1 | +2 | -1 | -1 | 0 | daily / high-volume (analyst) |
| P4 | Error-Averse / High-Stakes | -2 | 0 | 0 | -1 | +1 | 0 | audit / compliance |
| P5 | Calm Focus | 0 | -1 | -2 | +1 | +1 | 0 | occasional or daily (single-task) |
| P6 | Adaptive / Progressive Pro | 0 | 0 | 0 | 0 | 0 | 0 | mixed (novice + expert) |

Plain-English labels for each cell come from `position-vocabulary.md` (e.g. D3 `+2` → "Maximally dense", D1 `+2` → "Maximally fast"). Step B renders labels, not signed notation.

---

## P1 — Efficiency-First / Power-Operator

**Positions:** D1 +2 · D2 +2 · D3 +1 · D4 -1 · D5 -1 · D6 0. **Persona:** daily / high-volume (D4 -1 is a *soft-warn* per §5 — deliberate: experts want to drive).

**Characterization.** Optimizes raw task throughput for users who live in the tool all day. Chrome is stripped to the minimum; the screen is dense with actionable data; nearly everything is reachable from the keyboard via a command palette (Cmd/Ctrl-K) and per-action shortcuts. Rewards muscle memory over visual hunting. The feeling is *fast, frictionless, slightly austere* — a cockpit, not a showroom.

**Who/when it fits.** High-frequency expert operators: support agents, ops teams, data-entry specialists, dispatchers. A poor fit for occasional users.

**Structural choices (what the LLM should build).**
- **Navigation:** persistent left sidebar **+ command palette** (Cmd-K) as the primary action surface; shortcuts shown inline so they self-teach. *(Carries the recall-leaning D6 stance while D6 is inactive.)*
- **Primary data display:** dense **table** (`collections/table` + `wf-table--compact`), sticky header, sort/resize/reorder, virtualized scroll.
- **Input philosophy:** **inline-edit** for single fields; **bulk edit** via multi-select + batch action bar; modal only for multi-field create.
- **Disclosure:** mostly everything-visible; advanced filters one keystroke away.
- **Feedback/confirmation:** low — optimistic updates + undo toasts; confirm only irreversible deletes.
- **Keyboard/bulk:** maximal (the defining trait).
- **Empty/loading/error:** terse; skeleton rows; one-line inline errors; empty state offers a create shortcut.

**Realization recommendation (per `framework/assets/wireframes/realization-strategies.md`):** prefer `inline-drawer` / `inline-expand` for detail (keep table context); avoid `wizard-split`.

**Principles leaned on hardest (see `ux-baseline-checklist.md`):** Nielsen #7 flexibility/efficiency; Shneiderman "shortcuts for frequent users"; Fitts's Law; recognition-vs-recall deliberately tilted to recall.

**Citations:** Superhuman command palette — https://blog.superhuman.com/how-to-build-a-remarkable-command-palette/ · Mobbin command palette — https://mobbin.com/glossary/command-palette · NN/g 10 heuristics — https://www.nngroup.com/articles/ten-usability-heuristics/ · IxDF Shneiderman — https://ixdf.org/literature/article/shneiderman-s-eight-golden-rules-will-help-you-design-better-interfaces · IxDF Fitts — https://ixdf.org/literature/topics/fitts-law

---

## P2 — Guided / Novice-Safe

**Positions:** D1 -1 · D2 -2 · D3 -1 · D4 +1 · D5 +1 · D6 0. **Persona:** occasional / first-time (all positions §5-compatible).

**Characterization.** Treats every user as a first-timer and walks them through tasks in clearly bounded steps. Complexity is rationed via staged disclosure (wizards/back-next); each step asks only what it needs; the path to "done" is unambiguous; dangerous options are kept out of reach. The feeling is *reassuring, paced, never lost* — a guided tour, not an open sandbox.

**Who/when it fits.** Occasional, untrained, or anxious users; high-turnover roles; rarely-performed tasks (quarterly compliance entry, one-off setup). Poor fit for high-frequency operators.

**Structural choices.**
- **Navigation:** simple top-nav or a stepper; minimal lateral navigation during a task (a wizard owns the screen).
- **Primary data display:** **cards** or generously-spaced list; summaries over raw grids.
- **Input philosophy:** **wizard / staged disclosure** (back-next) for create and multi-field edit; one logical group per step; inline validation per field.
- **Disclosure:** progressive/staged (defining trait) — advanced settings behind "More options".
- **Feedback/confirmation:** high — explicit success states, "step 2 of 4", review-before-submit summary.
- **Keyboard/bulk:** low; pointer-first; bulk de-emphasized.
- **Empty/loading/error:** rich — empty states explain what to do + a CTA; errors plain-language with a fix suggestion.

**Realization recommendation:** prefer `wizard-split` for create/multi-field edit; `standalone-screen` for list/detail; avoid dense `inline-drawer` editing.

**Principles:** progressive/staged disclosure; Hick's Law; Nielsen #6 recognition, #9 error recovery; Shneiderman reversal + informative feedback + closure.

**Citations:** NN/g Progressive Disclosure — https://www.nngroup.com/articles/progressive-disclosure/ · IxDF Progressive Disclosure — https://ixdf.org/literature/topics/progressive-disclosure · Dovetail Hick's Law — https://dovetail.com/ux/hicks-law/ · NN/g 10 heuristics — https://www.nngroup.com/articles/ten-usability-heuristics/

---

## P3 — Analytical / Information-Dense

**Positions:** D1 -1 · D2 +1 · D3 +2 · D4 -1 · D5 -1 · D6 0. **Persona:** daily / high-volume (analyst). D4 -1 soft-warn per §5.

**Characterization.** Built for users whose primary job is to *read the data*: scan, compare across rows/columns, spot outliers, drill in, and act on a selection. Maximizes meaningful information per pixel while preserving scannability through alignment, grouping, and visual encoding (badges, sparklines, status colour). Unlike P1 (dense to go *fast*), P3 is dense to *see relationships*. The feeling is *a control room* — a lot on screen, but legible.

**Who/when it fits.** Analysts, operations leads, monitoring/triage, reconciliation/audit views, pipeline boards. Poor fit for single-record task flows.

**Structural choices.**
- **Navigation:** left sidebar for dataset switching + a persistent filter/facet rail; table ↔ board toggle.
- **Primary data display:** dense **table** (`wf-table--compact`) with sort/group/aggregate rows, inline mini-charts/sparklines, colour-coded status chips; optional **board** for pipeline comparison.
- **Input philosophy:** **inline-edit** + bulk action bar on selection; editing secondary to reading; detail opens in a side **drawer** (keep context).
- **Disclosure:** everything-visible at summary, drill-on-demand (row expand / detail drawer).
- **Feedback/confirmation:** medium; non-blocking; saved-view confirmations.
- **Keyboard/bulk:** high — multi-select, cell/row keyboard nav, bulk tag/status/export.
- **Empty/loading/error:** skeleton tables; "no results for these filters → clear filters"; never hide an active filter.

**Realization recommendation:** prefer `inline-drawer` / `inline-expand` for detail; `standalone-screen` for the primary collection; avoid `wizard-split`.

**Principles:** Gestalt (proximity/similarity/common-region/alignment make density legible — load-bearing here); Nielsen #1 visibility of status (active filters/sorts shown); #8 reinterpreted as signal density not decoration; recognition-vs-recall (visible facets).

**Citations:** Pencil & Paper enterprise data tables — https://www.pencilandpaper.io/articles/ux-pattern-analysis-enterprise-data-tables · Pencil & Paper dashboards — https://www.pencilandpaper.io/articles/ux-pattern-analysis-data-dashboards · NN/g proximity — https://www.nngroup.com/articles/gestalt-proximity/ · Stéphanie Walter data tables — https://stephaniewalter.design/blog/essential-resources-design-complex-data-tables/

---

## P4 — Error-Averse / High-Stakes

**Positions:** D1 -2 · D2 0 · D3 0 · D4 -1 · D5 +1 · D6 0. **Persona:** audit / compliance (D1 -2 and D4 -1 are §5-compatible — opposite of the forbidden +1).

**Characterization.** Built on the assumption that a wrong action can be expensive, irreversible, or compliance-relevant. Inserts deliberate friction before consequential actions, surfaces exactly what will happen and to what, prefers reversibility, leaves an audit trail. Speed is intentionally sacrificed at decision points where the cost of being wrong dwarfs the cost of being slow. The feeling is *careful, accountable, trustworthy* — a vault door, not a swinging gate.

**Who/when it fits.** Financial back-office, payroll, clinical/records, legal — anything where a mis-click destroys work, moves money, sends to a customer, or breaks compliance. Poor fit for low-stakes high-volume tasks (friction becomes habituation-inducing nagging).

**Structural choices.**
- **Navigation:** conventional sidebar/top-nav; destructive actions physically separated from routine ones (NN/g consequential-options proximity).
- **Primary data display:** **table** with clear record identity; status + lock/approval state always visible.
- **Input philosophy:** **modal form** for create/edit with explicit Save/Cancel (no silent inline commits for high-value fields); review-before-submit for multi-field changes; type-to-confirm ("type DELETE") for irreversible ops.
- **Disclosure:** progressive to reduce slips, but consequences never hidden — the confirm dialog restates request + effect.
- **Feedback/confirmation:** high *but calibrated* — heavy confirmation reserved for genuinely irreversible/expensive actions; reversible actions use undo (over-confirmation defeats prevention via habituation). Persistent audit feedback.
- **Keyboard/bulk:** present but guarded — bulk destructive actions require explicit scope confirmation ("affects 412 records").
- **Empty/loading/error:** plain-language, specific, recovery-oriented; no optimistic updates for consequential writes (show real confirmation).

**Realization recommendation:** prefer `modal` for consequential create/edit/confirm; `standalone-screen` for record detail; avoid `inline-edit` for high-value fields.

**Principles:** Nielsen #5 error prevention (headline), #9 recovery; Shneiderman reversal + control + memory-load; NN/g confirmation dialogs (sparingly, restate effect) + consequential-options proximity.

**Citations:** NN/g confirmation dialogs — https://www.nngroup.com/articles/confirmation-dialog/ · NN/g consequential options — https://www.nngroup.com/articles/proximity-consequential-options/ · NN/g 10 heuristics — https://www.nngroup.com/articles/ten-usability-heuristics/ · UIUXMedia error prevention vs recovery — https://uiuxmedia.com/error-prevention-vs-error-recovery/

---

## P5 — Calm Focus

**Positions:** D1 0 · D2 -1 · D3 -2 · D4 +1 · D5 +1 · D6 0. **Persona:** single-task worker (occasional or daily); §5-compatible for occasional (D2 -1, D3 -2 both below the forbidden +1).

**Characterization.** Minimizes the demand the tool makes on the user's attention. One task occupies the foreground; everything else recedes to the periphery or disappears until needed. Generous whitespace, a single clear primary action per screen, quiet/ambient feedback rather than alerts. Distinct from P2 (which *scaffolds* a novice) — P5 doesn't hand-hold, it gets out of the way. The feeling is *quiet, unhurried, low-stress*.

**Who/when it fits.** Focus/knowledge work, single-record deep work, environments where interruption is costly. Poor fit for high-density comparison or high-throughput batch work.

**Structural choices.**
- **Navigation:** minimal — collapsible/hidden sidebar, focus mode; reduced top chrome.
- **Primary data display:** single-record **focus view** or spacious list; one thing centred, large readable type.
- **Input philosophy:** **inline-edit** with auto-save (no modal interruptions); secondary actions in an overflow/peripheral menu.
- **Disclosure:** progressive to keep the foreground minimal — advanced controls on hover/focus or a peripheral panel.
- **Feedback/confirmation:** low / ambient — quiet auto-save indicators, peripheral status, no modal nags.
- **Keyboard/bulk:** modest; shortcuts unobtrusive; bulk not primary.
- **Empty/loading/error:** serene — soft empty states; non-alarming inline errors; subtle loading.

**Realization recommendation:** prefer `standalone-screen` focus views + `inline-expand`; avoid `modal` interruptions and dense tables.

**Principles:** calm technology (smallest possible attention; use the periphery); Nielsen #8 aesthetic & minimalist; Shneiderman reduce memory load; Hick's Law.

**Citations:** Calm Tech principles — https://calmtech.com/ · Mind the Product (Amber Case) — https://www.mindtheproduct.com/calm-technology-can-help-us-human-amber-case/ · NN/g 10 heuristics — https://www.nngroup.com/articles/ten-usability-heuristics/

---

## P6 — Adaptive / Progressive Pro

**Positions:** D1 0 · D2 0 · D3 0 · D4 0 · D5 0 · D6 0 (D5 may tune toward +1). **Persona:** mixed (novice + expert). All-neutral → no §4/§5 conflicts.

**Characterization.** A single interface that serves a *mixed* population — simple and discoverable on the surface for the occasional user, yet revealing power (shortcuts, bulk, advanced config) as the user reaches for it. It refuses the false choice between P1 and P2 by making the *same* UI grow with competence. The feeling is *approachable but not limiting* — low floor, high ceiling.

**Who/when it fits.** Internal tools with heterogeneous users (some daily, some monthly); products that must onboard newcomers **and** retain power users. The most common real-world internal-tool scenario. Poor fit only when the population is uniformly expert (use P1) or uniformly novice (use P2).

> **Selection guard (not the lazy default).** P6 is **not pre-selected** in Step B. Because "all-balanced" is tempting as a non-commitment, choosing P6 **requires a one-line justification** that the population is genuinely mixed. If the consultant cannot name both a novice and an expert audience, Step B nudges them to commit to a primary persona (P1/P2/P3/P4/P5). This preserves the divergence value of generating distinct prototypes.

**Structural choices.**
- **Navigation:** left sidebar (discoverable) **+ optional command palette** (accelerator); shortcuts shown beside menu items so novices learn them passively.
- **Primary data display:** **table** with a density toggle + optional board; defaults comfortable, expert can compact.
- **Input philosophy:** **inline-edit** for quick changes **and** a modal/drawer form for full create — novice uses the form, expert uses inline; bulk present but unobtrusive until multi-select.
- **Disclosure:** progressive disclosure as the central mechanism — "More options" / advanced filters one click in, never in the newcomer's face.
- **Feedback/confirmation:** medium, adaptive — confirmations for consequential actions, undo for the rest; first-run coachmarks that don't nag thereafter.
- **Keyboard/bulk:** available and surfaced, not mandatory.
- **Empty/loading/error:** instructive empty states (help newcomers) with a fast path (help experts); plain-language recoverable errors.

**Realization recommendation:** mix — `standalone-screen` collection, `inline-drawer` detail for experts, `modal`/`wizard-split` create for novices.

**Principles:** Nielsen #7 (explicitly "accommodate both novice and expert"); progressive disclosure (the mechanism); Shneiderman shortcuts; recognition-AND-recall.

**Citations:** NN/g 10 heuristics (#7) — https://www.nngroup.com/articles/ten-usability-heuristics/ · NN/g Progressive Disclosure — https://www.nngroup.com/articles/progressive-disclosure/ · Superhuman command palette — https://blog.superhuman.com/how-to-build-a-remarkable-command-palette/

---

## Posture-selection guidance (Step B)

1. Read the scope's persona(s) + goals (from `requirements.md > §3`/`§4`, surfaced via `scope.json`).
2. Pick the posture whose "Who/when it fits" best matches the **primary** persona. Genuinely mixed population → P6 (with justification).
3. Take the posture's D1–D5 defaults as starting positions; the consultant confirms or tunes them (rendered with `position-vocabulary.md` labels).
4. Re-check the tuned positions against `tradeoff-dimensions-registry.md` §4 (incoherent pairs) and §5 (persona rules) — hard conflicts block; soft conflicts warn.
5. Record the final positions + the posture id in the design spec front-matter (instance data, not a definition).

**Wireframe-seeded fast path.** If a wireframe variant for the same scope was selected as the basis (`/prototype` input D), pre-fill steps 2–3 from the variant's `variant-position.json` (`design_philosophy`, `dimension_positions`): map the variant's `design_philosophy` to the nearest posture above and adopt its positions as the defaults. The consultant confirms/tweaks rather than choosing from scratch.

---

## Antagonistic combinations (reference)

The **canonical** incoherent-pair rules live in `tradeoff-dimensions-registry.md > Section 4` and the persona rules in `Section 5`. None of the six presets above violate a hard rule. Two posture-derived contradictions worth appending to the canonical registry (Section 4 / a posture note), referenced here, never restated:

- **Density vs novice-spaciousness** — `density-focus +2` with a posture/persona that also demands novice-spacious signposting is incoherent (a Bloomberg-dense TurboTax-airy screen). Already implied by §4 D2×D3; extend the note to cover persona pairing.
- **Over-confirmation vs speed** — heavy confirmation density on reversible actions while `speed-accuracy ≥ +1` *defeats* error prevention via habituation (NN/g). A soft tension to flag when a consultant tunes P1/P3 toward high confirmation.

---

## Anti-patterns

- Do not restate dimension definitions, poles, position labels, or incoherent-pair/persona rules here — they are owned by `tradeoff-dimensions-registry.md` and `position-vocabulary.md`. This file only adds posture presets + characterizations + structural recommendations.
- Do not emit non-neutral D6 positions while D6 is inactive. Capture the recall-vs-discoverability stance in structural-choices prose; record `D6 = 0`.
- Do not introduce *visual* tokens (color/type/radius/elevation) as posture parameters. The brand is fixed and uniform (see `app-shell-spec.md` + `extract-brand-theme.md`); postures vary **layout and workflow only**.
- Do not pre-select P6 or let it become the default. It requires an explicit mixed-population justification.
- Do not invent a seventh posture without grounding it in the literature and checking it against §4/§5; the six are chosen to span the meaningful space while staying decisive.
- Do not author a preset that violates a §4 incoherent-pair or a §5 hard persona rule. Re-check on every edit.
