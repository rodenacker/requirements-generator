<!-- ROLE: asset (prototype-private). Populate top-to-bottom in one pass: no {{placeholders}}, no blank fields. -->
<!-- This template is consumed by prototype-spec-drafter.md (populates), prototype-spec-resolver.md (resolves markers), prototype-spec-merger.md (strips markers → final design-spec.md), and prototype-generator.md (reads the final spec to generate React). -->

# Prototype design spec: {{prototype_name}}

<!-- format: front-matter is a fenced ```json block the generator reads mechanically. dimension_positions are instance data (selected values), not definitions. -->
```json
{
  "name_slug": "{{name-slug}}",
  "prototype_name": "{{consultant-given name}}",
  "scope_slug": "{{scope-slug}}",
  "posture": "{{P1|P2|P3|P4|P5|P6}}",
  "posture_label": "{{e.g. Efficiency-First / Power-Operator}}",
  "dimension_positions": { "D1": 0, "D2": 0, "D3": 0, "D4": 0, "D5": 0, "D6": 0 },
  "primary_persona": "{{verbatim §3 persona name}}",
  "route": "/{{name-slug}}",
  "wireframe_basis": "{{variant id from wireframes/<scope-slug>/ or null}}",
  "created_at": "{{ISO-8601}}"
}
```

**Marker legend** (mirrors `requirements-draft.md`; the merger strips resolution markers, retains provenance):
- `[SRC: <id>]` — decision grounded in a requirement ID (`F-NN`/`BR-NN`/`UI-NN`/`§7.Shape`), a blueprint surface (`LS-NN`), or a selected wireframe variant (`WF:<variant>`). **Retained** in the final spec as provenance for the generator.
- `[POSTURE-DEFAULT]` — value taken deterministically from the chosen posture's preset in `design-philosophies.md` (resolver skips; merger strips).
- `[AI-SUGGESTED: AI-NNN | blocking|non-blocking]` — drafter UX inference not dictated by the posture, a requirement, or a wireframe (resolver Q&A; merger strips). **Keep this set tight** — only genuinely build-divergent ambiguities are `blocking`.

---

## 1. Scope

| Field | Value |
|---|---|
| Requirement IDs in scope | {{F-NN, BR-NN, UI-NN, §7 shapes — from scope.json [SRC: …]}} |
| Logical surfaces (from blueprint) | {{LS-01 … — each with one-line intent [SRC: LS-NN]}} |
| Out of scope (explicit) | {{what this prototype deliberately does not cover}} |

<!-- guidance: surfaces and IDs come from blueprints/<scope-slug>/{scope.json, blueprint.md}. Do not widen the scope. -->

## 2. Purpose

<!-- guidance: 1–2 paragraphs. The UX question this prototype lets the consultant experience (e.g. "Can high-volume operators clear the import queue faster with inline-edit + bulk actions than with a modal form?"). Free prose from the consultant's Step-B answer. -->
{{purpose prose}}

## 3. UX posture & rationale

| Field | Value |
|---|---|
| Posture | {{posture_label}} [POSTURE-DEFAULT] |
| Why it fits | {{tie to primary_persona + goals; cite §3/§4 [SRC: …]}} |
| Principles emphasized | {{the posture's load-bearing principles, per design-philosophies.md}} |

## 4. Trade-off positions (design parameters)

<!-- guidance: D1–D5 active; D6 inactive (record 0). Labels from position-vocabulary.md. Each value is [POSTURE-DEFAULT] unless the consultant tuned it (then [SRC: consultant] or [AI-SUGGESTED] if the drafter proposed a tune). Re-check against tradeoff-dimensions-registry.md §4/§5. -->

| Dim | Position | Plain-English label | Basis |
|---|---|---|---|
| D1 speed-accuracy | {{-2..+2}} | {{label}} | {{[POSTURE-DEFAULT] / tuned}} |
| D2 power-simplicity | {{-2..+2}} | {{label}} | {{…}} |
| D3 density-focus | {{-2..+2}} | {{label}} | {{…}} |
| D4 control-automation | {{-2..+2}} | {{label}} | {{…}} |
| D5 flexibility-consistency | {{-2..+2}} | {{label}} | {{…}} |
| D6 memorability-discoverability | 0 | *(inactive)* | stance captured in §6 disclosure prose |

**Structural choices implied** (from the posture's recommendations, tuned by positions): navigation {{…}}; primary data display {{…}}; input philosophy {{…}}; disclosure {{…}}; feedback/confirmation density {{…}}; keyboard/bulk emphasis {{…}}.

## 5. Per-surface realization decisions

<!-- guidance: one block per LS-NN in the blueprint. Realization enum from realization-strategies.md: standalone-screen | inline-drawer | inline-expand | modal | wizard-split. Choice driven by the posture's realization recommendation + positions; cite the basis. Folded surfaces name host_surface + host_state. -->

### {{LS-NN}} — {{surface intent}}

| Field | Value |
|---|---|
| Realization | {{standalone-screen / inline-drawer / …}} {{[POSTURE-DEFAULT] / [SRC: WF:<variant>] / [AI-SUGGESTED: AI-NNN | …]}} |
| Host (if folded) | {{host LS-NN + host_state, else —}} |
| Why | {{tie to posture + positions}} |

<!-- repeat §5 per surface -->

## 6. Interaction & workflow flows

<!-- guidance: the clickable paths a reviewer will walk. One numbered flow per primary task. Each step: trigger → surface/state → CTA(s). Navigation + disclosure reflect §4 positions (e.g. command palette at D2+, wizard at D1−/D2−). This is the heart of what diverges between prototypes. -->

**Flow {{n}}: {{task name}}** [SRC: §5.{{x}} / F-NN]
1. {{step}} → {{surface/state}} → {{CTA}}
2. …

**Navigation model:** {{sidebar / topnav / command-palette / stepper — per §4}}.
**Disclosure model:** {{everything-visible / progressive / staged — carries the D6 stance while D6 is inactive}}.

## 7. Component inventory (shared set)

<!-- guidance: every task component MUST come from the shared set (rule 15). List shared components composed per surface, marking reuse vs new. NEW components are authored into the SHARED library (atoms/molecules/organisms/templates/domain), never private to this prototype. See shared-component-conventions.md. -->

| Surface | Shared components composed | Reuse / New | Atomic tier (if new) |
|---|---|---|---|
| {{LS-NN}} | {{Button, DataTable, …}} | {{reuse / new}} | {{atom/molecule/organism/template/domain}} |

## 8. Data binding (anti-fabrication contract)

<!-- guidance: per surface, every data-bound element binds to a Property in the blueprint's per-surface closed set (§7 data shapes + F-NN params). NO invented fields. Map Property → fixture field → store. Mirrors the wireframe data-prop rule. -->

| Surface | Property (closed set) | Fixture field | Store |
|---|---|---|---|
| {{LS-NN}} | {{Entity.Field / F-NN:Param}} | {{fixtures/<shape>.json field}} | {{useXStore}} |

## 9. Accessibility & UX-principle checklist (from `ux-baseline-checklist.md`)

<!-- guidance: the spec-relevant subset of the baseline floor, with the posture's emphasized items called out. The merger embeds this; the generator self-checks against it; the Playwright smoke asserts the runtime-checkable subset. -->
- [ ] Keyboard: {{operable surfaces, shortcuts if posture leans power}}
- [ ] Focus visible & not obscured
- [ ] Name/role/value on all controls
- [ ] Three states (empty / loading / error) on every collection + async action
- [ ] Not colour-alone for status (GR-16)
- [ ] Role switcher present on multi-role surfaces (PI-05)
- [ ] {{posture-emphasized items}}

## 10. Success criteria

<!-- guidance: how a reviewer judges the prototype delivered its purpose, PLUS the verify-gate acceptance. -->
- {{UX success criteria tied to §2 purpose}}
- [ ] Playwright smoke: route `/{{name-slug}}` loads, no console errors, primary CTA clickable.
- [ ] `npm run lint` + `tsc --noEmit` + `next build` pass.

## 11. Prototype invariants checklist

<!-- guidance: merger appends PI references (PI-01..PI-08) verbatim from framework/shared/prototype-invariants.md as a checklist. Drafter leaves this heading; merger fills it. -->
{{merger fills from prototype-invariants.md}}

---

<!-- Self-validation (drafter): no {{placeholders}} remain; every surface in the blueprint has a §5 block; every §8 Property is in the blueprint closed set; the [AI-SUGGESTED] set is tight; positions pass §4/§5 of tradeoff-dimensions-registry.md. -->
