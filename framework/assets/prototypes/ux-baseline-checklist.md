# Prototype UX baseline checklist (`ux-baseline-checklist.md`)

**Role:** asset (prototype-private).

**Purpose:** The non-negotiable UX floor **every** generated prototype must satisfy, regardless of the chosen posture (`design-philosophies.md`). Each item is a crisp, **self-validatable** statement the `prototype-generator` (and its per-surface sub-agents) check each rendered screen against; the `prototype-spec-merger` appends the relevant subset into each design spec's §10. A baseline miss is **fail-closed** — the generator fixes it before the verify gate, or the verify gate (`verify-prototype-build.md`) and self-validation surface it.

A posture *emphasizes* some of these harder (recorded per-posture in `design-philosophies.md`), but a posture **never licenses violating** the floor.

**Used by:** `framework/agents/prototype-generator.md` + `prototype-generator/steps/step-sub-render-surface.md` (render-time self-check), `framework/agents/prototype-spec-merger.md` (appends §10), `framework/skills/verify-prototype-build.md` (Playwright smoke asserts the runtime-checkable subset).

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

---

## How the generator uses this

1. While rendering a surface, the per-surface sub-agent self-checks each rendered screen against this list (`step-sub-render-surface.md`).
2. Any miss is fixed before returning the surface manifest — never deferred.
3. `verify-prototype-build.md`'s Playwright smoke asserts the runtime-checkable subset (focus visible, keyboard reach of the primary CTA, no console errors, role switcher present, the three states reachable where applicable).
4. The merger embeds the spec-relevant subset into design-spec §10 so the contract is auditable per prototype.

## Anti-patterns

- Do not treat a posture as a licence to skip a baseline item. Postures emphasize; they never waive the floor.
- Do not relabel a generic spinner as a "loading state". The three states are explicit designs, not placeholders.
- Do not rely on colour alone for status (also a `GR-16` violation).
- Do not duplicate the WCAG/Nielsen/Shneiderman *definitions* elsewhere; reference this file.
