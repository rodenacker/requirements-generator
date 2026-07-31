# Prototype UX baseline checklist (`ux-baseline-checklist.md`)

**Role:** asset (prototype-private).

**Purpose:** The non-negotiable UX floor **every** generated prototype must satisfy, regardless of the chosen posture (`design-philosophies.md`). Each item is a crisp, **self-validatable** statement the `prototype-generator` (and its per-surface sub-agents) check each rendered screen against; the `prototype-spec-merger` appends the relevant subset into each design spec's §9. A baseline miss is **fail-closed** — the generator fixes it before the verify gate, or the verify gate (`verify-prototype-build.md`) and self-validation surface it.

A posture *emphasizes* some of these harder (recorded per-posture in `design-philosophies.md`), but a posture **never licenses violating** the floor.

**Used by:** `framework/agents/prototype-generator.md` + `prototype-generator/steps/{step-04-dispatch-surface-subagents, step-sub-render-surface, step-05-compose-route, step-07-handback}.md` (dispatch payload, render-time self-check, mechanical sweep), `framework/agents/prototype-spec-merger.md` (appends §9), `framework/skills/verify-prototype-build.md` (Playwright smoke asserts the runtime-checkable subset).

---

## Nielsen's 10 usability heuristics
Source: https://www.nngroup.com/articles/ten-usability-heuristics/

- [ ] **N1 Visibility of system status** — every state change (loading, saving, success, active filter) shows visible feedback within ~1s.
- [ ] **N2 Match system ↔ real world** — use the client's domain language (from `requirements.md` / `glossary`); no system/dev jargon in labels.
- [ ] **N3 User control & freedom** — every action offers a clear escape: Cancel, Close, Undo, or Back; no dead-ends.
- [ ] **N4 Consistency & standards** — the same word/control/pattern means the same thing everywhere; follow platform conventions and the shared component set.
- [ ] **N5 Error prevention** — constrain inputs, disable invalid actions, and confirm/guard destructive ones before they can happen.
- [ ] **N6 Recognition over recall** — make options, actions, and prior choices visible; don't force memory across screens.
- [ ] **N7 Flexibility & efficiency** — provide accelerators (shortcuts, saved views) that don't burden novices.
- [ ] **N8 Aesthetic & minimalist design** — show only relevant content; every on-screen element earns its place.
- [ ] **N9 Help users recover from errors** — errors in plain language, state the problem, suggest a fix; no codes alone.
- [ ] **N10 Help & documentation** — provide in-context, task-focused help where users get stuck.

## Shneiderman's 8 golden rules
Source: https://ixdf.org/literature/article/shneiderman-s-eight-golden-rules-will-help-you-design-better-interfaces

- [ ] **S1 Consistency** — identical sequences, terminology, and layout for analogous situations.
- [ ] **S2 Shortcuts for frequent users** — keyboard accelerators / abbreviations as usage frequency grows.
- [ ] **S3 Informative feedback** — every user action yields a system response, scaled to its significance.
- [ ] **S4 Closure** — group actions into begin/middle/end; signal task completion.
- [ ] **S5 Prevent errors / simple handling** — design so serious errors can't occur; recovery is simple when they do.
- [ ] **S6 Easy reversal** — Undo is available; relieves anxiety, encourages exploration.
- [ ] **S7 Keep users in control** — users initiate; the system responds, not the reverse.
- [ ] **S8 Reduce short-term memory load** — keep displays simple; don't require recalling info across screens.

## Gestalt principles (layout legibility)
Sources: https://www.nngroup.com/articles/gestalt-proximity/ · https://ixdf.org/literature/topics/gestalt-principles

- [ ] **G1 Proximity** — related elements grouped close; unrelated ones spaced apart (whitespace groups).
- [ ] **G2 Similarity** — elements sharing colour/shape/size read as one group; use for status/categories.
- [ ] **G3 Common region** — a shared border/background binds elements into a unit (cards, panels, fieldsets).
- [ ] **G4 Closure / continuity** — aligned elements and partial reveals read as continuous wholes; use alignment grids.

## Single-principle laws

- [ ] **Fitts's Law** — frequent/important targets are large and near the likely cursor path; respect a 24×24 CSS-px minimum. https://ixdf.org/literature/topics/fitts-law
- [ ] **Hick's Law** — reduce simultaneous choices; chunk, default, and stage decisions. https://dovetail.com/ux/hicks-law/
- [ ] **Recognition over recall** — show options rather than requiring memory; surface recent/saved items. (Nielsen #6)
- [ ] **Progressive disclosure** — keep the primary UI to essentials; defer advanced features to secondary/on-demand surfaces. https://www.nngroup.com/articles/progressive-disclosure/

## WCAG 2.2 AA basics (accessibility floor)
Source: https://www.w3.org/TR/WCAG22/ · https://www.w3.org/WAI/standards-guidelines/wcag/new-in-22/

- [ ] **Contrast (1.4.3 / 1.4.11)** — text ≥ 4.5:1 (large ≥ 3:1); UI components & meaningful graphics ≥ 3:1.
- [ ] **Target size (2.5.8)** — interactive targets ≥ 24×24 CSS px (or adequately spaced).
- [ ] **Keyboard accessible (2.1.1)** — all functionality operable by keyboard alone; no traps.
- [ ] **Focus visible + not obscured (2.4.7 / 2.4.11)** — a clearly visible focus indicator (≥3:1 vs adjacent), not hidden behind sticky headers/overlays.
- [ ] **Name, role, value (4.1.2)** — every control has an accessible name/role/state (labels, ARIA where needed).
- [ ] **Error identification & suggestion (3.3.1 / 3.3.3)** — errors identified in text with a correction suggested where known.
- [ ] **Consistent help + redundant entry (3.2.6 / 3.3.7)** — help in a consistent location; don't re-ask info already provided in the same flow.
- [ ] **Not colour alone (1.4.1)** — status conveyed by icon/text/shape in addition to colour (this also reinforces `GR-16`).

## Three states that AI-generated UIs routinely skip

Every collection/data surface and every async action must explicitly design **all three**:

- [ ] **Empty state** — icon/illustration + plain-language explanation + a primary CTA (aligns with `GR-08` / `GR-09`).
- [ ] **Loading state** — skeleton matching the data layout (not a bare spinner) per the `GR-10` threshold (none <300 ms, skeleton 300 ms–3 s, skeleton+message >3 s).
- [ ] **Error state** — plain-language, specific, recovery-oriented (Retry / how to fix), per `GR-14` (toast vs banner) and `N9`.

## Prototype-fidelity floor (invariants)

- [ ] **Client-side only** — no real network calls; data from fixtures (PI-01..PI-04).
- [ ] **Role switcher present** on every multi-role surface, in the prototype chrome (PI-05, PI-08).
- [ ] **Data binding closed** — every data-bound element binds to a Property in the blueprint's per-surface closed set; no invented fields (mirrors the wireframe `data-prop` rule; see `shared-component-conventions.md`).

## Component minimum-feature contracts

**Canonical owner: `framework/assets/design-system-standards.md §1` — the definitions live there and are not redefined here.** The checkboxes below are the self-validatable projection of §1, in the same spirit as the Nielsen / Shneiderman / WCAG restatements above: a sub-agent checks these without a second read, and `step-04` passes the applicable families in its dispatch payload.

**Scope.** §1 is a *minimum-feature* contract, not a required roster (`design-system-standards.md:20`). It binds whichever component families a surface actually composes. A **data table** here means §1's sense — rows of comparable records for scanning, sorting and acting upon — not every use of `ui/table`. A per-prototype exception is recorded in design-spec §9's Exceptions table with a reason (`design-system-standards.md:196`), never taken silently.

**Already structural — do not re-implement, just do not fight it:** numeric right-align + `tabular-nums` comes from `ui/table.tsx`'s `TableHead data-numeric`; the visible-label rule is enforced by `ui/label.tsx`.

- [ ] **C1 Tables — sort.** Every data column is sortable; sort state is visible on the active header (asc/desc/none), carried as `aria-sort`, and persists across pagination.
- [ ] **C2 Tables — pagination.** The table footer **always** carries pagination — explicit Next/Back, "Page N of M", a page-size selector of **5 / 10 / 20 / 50** defaulting to **20**, and the total record count — **even when there is only one page** (consistency over cleverness). Composed from the shipped `ui/pagination` primitive, so the `role="navigation"` landmark and its accessible name come for free.
- [ ] **C3 Tables — three states explicit.** Empty, loading and error are designed, never an absent or silent table (reinforces the three-states section above).
- [ ] **C4 Tables — truncation.** Long cell text truncates with a **tooltip on hover** carrying the full value; row height stays uniform across the page.
- [ ] **C5 Tables — rows are NOT clickable.** No `onClick`, `data-clickable` or `data-pressable` on a data-table `<tr>`. The primary identifier is a link/button in its own cell; row-scoped actions live in a **dedicated action column**. (Whole-row click is an invisible affordance, ambiguous against text selection, hostile to keyboard users, and conflicts with multi-select.) Row-click stays legal for row-*like* lists that are not data tables — see `pattern-catalogue/collections/data-list.md`.
- [ ] **C6 Date fields.** A real picker, never free text as the only input mode; keyboard entry is an accelerator, not the control. Locale-aware format shown in the placeholder. Min/max **disable** out-of-range dates rather than rejecting on submit. No second hand-authored calendar icon beside a native indicator; the indicator's legibility comes from `color-scheme`, never a hardcoded colour/`fill`/`invert()`.
- [ ] **C7 Buttons.** Label is verb-led and action-specific ("Save changes", not "OK"). Loading is visually distinct from disabled. Destructive = colour **and** icon. **One primary per surface.** Navigation uses a link, not a button.
- [ ] **C8 Inputs.** A **suitable placeholder** on every field (format hint or example — complementing, never replacing, the visible label). The focused field is distinguishable by **more than colour**. Required is indicated visibly **and** programmatically. Helper and error text have dedicated slots. Validation runs **on blur** for a field and **on submit** for the form — never aggressively per keystroke.
- [ ] **C9 Navigation.** Current location is indicated (`aria-current`). The URL reflects the current view so it is shareable, bookmarkable and reloadable. No sub-flow trap — there is always a way back. No primary nav hidden behind a hamburger on desktop.
- [ ] **C10 Feedback.** Severity is carried by colour **and** icon. Modals trap focus, close on `Esc`, return focus to the trigger, and carry an elevation shadow **and** a 1px border so the edge survives a same-colour background. Toasts only for ephemeral, non-critical confirmation — errors and warnings persist until acknowledged; never a toast for a critical error.

---

## How the generator uses this

1. `step-04` passes the applicable subset in each sub-agent's dispatch payload (`ux_baseline_subset`, plus `component_contracts` for the §1 families that surface composes) — a compact restatement, not a file path.
2. While rendering a surface, the per-surface sub-agent self-checks each rendered screen against this list (`step-sub-render-surface.md`); `step-05-compose-route.md` binds driver-owned routes to the same floor.
3. Any miss is fixed before returning the surface manifest — never deferred.
4. `step-07-handback.md`'s mechanical sweep fails the build on the grep-decidable items (no clickable data-table row) and on the §7↔code pagination consistency check.
5. `verify-prototype-build.md`'s Playwright smoke asserts the runtime-checkable subset (focus visible, keyboard reach of the primary CTA, no console errors, role switcher present, the three states reachable where applicable, and per table: the pagination landmark, `aria-sort` on data columns, no clickable row).
6. The merger embeds the spec-relevant subset into design-spec §9 so the contract is auditable per prototype, alongside the Exceptions table that records any §1 item a surface legitimately does not meet.

## Anti-patterns

- Do not treat a posture as a licence to skip a baseline item. Postures emphasize; they never waive the floor.
- Do not relabel a generic spinner as a "loading state". The three states are explicit designs, not placeholders.
- Do not rely on colour alone for status (also a `GR-16` violation).
- Do not duplicate the WCAG/Nielsen/Shneiderman *definitions* elsewhere; reference this file.
- Do not redefine a §1 contract here or downstream — `design-system-standards.md §1` owns the definitions; the C1–C10 items above are a projection for self-validation, and a divergence between them is a bug in this file.
- Do not drop pagination because the fixture set fits on one page. §1 requires the footer regardless; a one-page table with no pagination is the most common form of this miss.
- Do not treat an undocumented omission as an exception. An exception is a reasoned row in design-spec §9; anything else is a FAIL.
