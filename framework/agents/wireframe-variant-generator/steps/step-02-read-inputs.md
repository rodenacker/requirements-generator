---
name: step-02-read-inputs
description: 'Read the blueprint, the variants.json (own entry only), the templates, and the trade-off-dimensions registry + pattern-bindings guidance.'
---

# Step 2: Read inputs

## 2.1 Read the blueprint

```
Read tool: <blueprint_path>
```

Compute the sha256 of the bytes read; capture into in-memory `blueprint.sha256` for later cross-validation. Parse:

- The `## Sources` section's comma-separated source list (for cross-reference at self-validation).
- The `## Available personas` bulleted list.
- The `## Screen inventory` table — for every row, capture `{ screen_id: "S-NN", intent: "<text>", sources: ["<id1>", ...], secondary_intent: "<text or null>" }` into in-memory `screens[]` (preserving inventory order).
- The `## Flow` section's flow notation (for composing cross-screen prev/next nav).

Set `N = screens.length`. Output one short line: *"Variant {{variant_id}} ready. Composing {{N}} screens for scope `{{scope_slug}}`."* (matches the placeholder from step 1's announcement.)

## 2.2 Read the variants.json own-entry

```
Read tool: <variants_path>
```

JSON-parse. Locate the entry where `variants[i].variant_id == <variant_id>`. **Read only that entry; ignore others.** Capture into in-memory:

- `own.variant_id`
- `own.persona_binding`
- `own.design_philosophy`
- `own.dimension_positions` (all six canonical dimensions)
- `own.persona_traits` — derived from the persona binding text by the same heuristic used in `framework/agents/blueprint-architect/steps/step-02-read-inputs.md > 2.4` (frequency, expertise, role).

Cross-check `variants.json > blueprint_sha256` against `blueprint.sha256` from step 2.1. Mismatch indicates the blueprint was edited between the architect's run and Stage 3 dispatch — return `failed` with structured plain-text *"Blueprint sha256 drift: variants.json declares <hash1>, blueprint.md is <hash2>. Re-run architect first."*. Do not proceed.

## 2.3 Read the screen template

```
Read tool: framework/assets/templates/template-screen.html
```

Capture into in-memory `template_screen` (reused for every screen render at step 4).

## 2.4 Read the trade-off-dimensions registry + pattern-bindings guidance

```
Read tool: framework/assets/wireframes/tradeoff-dimensions-registry.md
Read tool: framework/assets/wireframes/pattern-bindings.md
```

Capture Section 3 (per-dimension HTML effects per pattern category) from the registry; this is the per-screen lookup table at step 4. Capture Sections 1, 2, 4 from pattern-bindings.md; these are the primary-slot + secondary-slot + slot-budget guidance.

## 2.5 Read the catalogue index

```
Read tool: framework/assets/pattern-catalogue/_index.md
```

Capture the full list of `{ id, category, tier, file_path }` rows; used at step 4 to validate pattern IDs and to look up file paths for selective per-pattern reads.

## 2.6 Compute pre-render plan (in-memory)

For each screen in `screens`:

- Derive the screen's `primary_pattern` candidate via `pattern-bindings.md > Section 1` matching its intent against requirement-type → pattern-category rows. Pick the most direct-match pattern (cross-check against `_index.md` for the catalogue ID; skip T3 stubs which lack bodies — fall back to T1/T2 closest).
- Derive the screen's `primary_pattern_variant` via `tradeoff-dimensions-registry.md > Section 3` using `own.dimension_positions` (e.g. `density-focus: +2` + pattern category `collections/table` → `table.compact`).
- Derive the screen's `secondary_patterns` shortlist via `pattern-bindings.md > Section 2` (e.g. screen contains a form → add `feedback/inline-validation` per `GR-05`; screen contains a destructive action → add `surfaces/modal-confirmation` per `GR-04`).
- Derive the screen's `states_rendered` list — at minimum `default`; add `loading` if the pattern category typically loads (collections); add `error-*` states per the screen's `BR-NN` sources; add `empty` for any collection screen.
- Derive the screen's `screen_slug` from its intent (kebab-case, max ~30 chars).

The per-screen plan is the input to step 4. Each plan row also names which catalogue files step 4 will need to selectively read (the primary pattern's file + each secondary pattern's file).

---

**Next:** Read fully and follow `step-03-extract-ds.md`.
