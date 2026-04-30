<!-- ROLE: asset. v7a-derived seed (metadata + overview + states sections lifted from .claude/skills/wds-4-ux-design/templates/page-specification.template.md). Finalise during phase-1 build-order step 1 per v7b-Brief.md > §template-design-spec.md and §topics-design.md. -->

# Design specification: {{application_name}}

**Tool-agnostic constraint:** UI described via `taxonomy-screens.md` + object mappings + content + states + behaviours + `visual_form`. **No tool-native tokens, no hex codes, no pixel values, no CSS classes** — those belong in `style-tokens.md` (P2 styler output), not here.

**Status:** draft | final
**Last finalised at:** {{last_finalised_at}}

> Inferred content is marked `[AI-SUGGESTED]` — **this stage's own inferences only.** Upstream `[AI-SUGGESTED]` requirements do NOT propagate the marker into this spec; their status is recorded as a citation note in §Provenance instead (e.g. `source-status = AI-SUGGESTED-at-requirements-Accept`). The design-spec completeness report generates findings only from markers this drafter added. Fill-every-field rule applies.

---

## 1. Overview

| Count | Kind |
|---|---|
| {{n_screens}} (≥1) | screens |
| {{n_views}} | views |
| {{n_organisms}} | organisms |
| {{n_molecules}} | molecules |
| {{n_atoms}} | atoms |

**Narrative summary:** {{summary}}

<!-- rev: run-N YYYY-MM-DD -->

---

## 2. Screen classification

| Screen | Tier | Rationale |
|---|---|---|
| {{screen_id}} | core / pattern-inheriting / CRUD | {{why}} |

Pattern-inheriting screens reuse the layout shell of a core screen; CRUD screens follow the template-CRUD pattern. The classification is a structural signal for downstream renderers; this spec carries the classification, not the shells themselves.

---

## 3. Global design decisions

| Topic | Decision | Trade-off rationale |
|---|---|---|
| Page layout | {{decision}} | {{trade_off_axis_and_position}} |
| Main navigation | {{decision}} | {{rationale}} |
| Notification / feedback | {{decision}} | {{rationale}} |
| Messaging / dialog | {{decision}} | {{rationale}} |
| Data table pattern | {{decision}} | {{rationale}} |
| Search & filter pattern | {{decision}} | {{rationale}} |
| Loading / empty / error states | {{decision}} | {{rationale}} |

---

## 4. Per-screen design decisions

### Screen: {{screen_id}}

| Property | Value |
|---|---|
| Route | {{route}} |
| Primary task | {{task_ref}} |
| Primary actor | {{actor_persona_ref}} |
| Page type | full / modal / drawer / popup |
| Viewport | mobile-first / desktop-first / responsive |
| Interaction | touch-first / mouse+keyboard |
| Visibility | public / authenticated / role-gated |
| Entry points | {{how_users_arrive}} |
| Exit points | {{where_users_go_next}} |

**Trade-off ratings (per `trade-off-dimensions.md`):**

| Dimension | Rating (−2 … +2) | Rationale |
|---|---|---|
| Speed ↔ Accuracy | {{rating}} | {{why}} |
| Power ↔ Simplicity | {{rating}} | {{why}} |
| Density ↔ Focus | {{rating}} | {{why}} |
| Control ↔ Automation | {{rating}} | {{why}} |
| Flexibility ↔ Consistency | {{rating}} | {{why}} |
| Memorability ↔ Density | {{rating}} | {{why}} |

### UI inventory

| taxonomy_id | taxonomy_kind | taxonomy_modifier | parent_id | object_refs | role | visual_form | states | behaviours |
|---|---|---|---|---|---|---|---|---|
| screen-{{slug}} | screen | — | — | {{ooux_object_refs}} | {{role_gating}} | — | default / loading / empty / error / success | {{onLoad / onSubmit / etc.}} |
| view-{{slug}} | view | tab? | screen-{{parent}} | {{refs}} | {{role}} | — | {{states}} | {{behaviours}} |
| org-{{slug}} | organism | modal / drawer / list / — | {{parent}} | {{refs}} | {{role}} | {{shape}} | {{states}} | {{behaviours}} |
| mol-{{slug}} | molecule | — | {{parent}} | {{refs}} | — | {{shape}} | {{states}} | {{behaviours}} |
| atom-{{slug}} | atom | — | {{parent}} | — | — | {{shape}} | {{states}} | {{behaviours}} |

**`visual_form` vocabulary (tool-agnostic):** indicator, chip, card, panel, button, link, tab, accordion, list-row, progress, field, etc. Describes _kind of surface_; concrete colour, icon, and pixel-level appearance come from the styler.

### Page states

| State | When | Appearance | Available actions |
|---|---|---|---|
| Default | {{condition}} | {{description}} | {{actions}} |
| Loading | {{condition}} | {{description}} | {{actions}} |
| Empty | {{condition}} | {{description}} | {{actions}} |
| Error | {{condition}} | {{description}} | {{recovery_actions}} |
| Success | {{condition}} | {{description}} | {{next_steps}} |

<!-- repeat §4 per screen -->

---

## 5. Behaviours

AI-enriched behaviour items are flagged `[AI-SUGGESTED]`.

| Behaviour | Trigger | Effect | Affects (taxonomy_ids) | Notes |
|---|---|---|---|---|
| {{name}} | {{trigger}} | {{effect}} | {{ids}} | {{notes}} |

---

## 6. Provenance

Every decision links back to its source.

| Decision | Source | Type |
|---|---|---|
| {{decision}} | requirements §{{section}} / user goal {{ref}} / analysis {{file}} / research {{ref}} | extracted / derived / [AI-SUGGESTED] |

---

_Re-finalised on rerun via `design-spec-finaliser` agent; touched sections carry `<!-- rev: run-N YYYY-MM-DD -->` markers. Brand tokens are produced separately by `/style` (P2) and live in `artifacts/design/style-tokens.md` — never in this spec._
