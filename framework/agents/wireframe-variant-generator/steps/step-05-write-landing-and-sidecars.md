---
name: step-05-write-sidecars
description: 'Write manifest.json (per-screen bindings accumulator) and variant-position.json (immutable mirror of variants.json own-entry + self-authored concise strengths/weaknesses/use-when). Verify each. The per-variant landing page (wireframes.html) is no longer authored — the scope index.html owns all variant navigation and meta surfacing.'
---

# Step 5: Write the two JSON sidecars

The variant-generator authors two artefacts in this step: `manifest.json`
(consumed by the comparator for drift detection) and `variant-position.json`
(the immutable mirror of the architect's `variants.json` entry, augmented with
self-authored strengths/weaknesses/use-when). The `wireframes.html` per-variant
landing page is **no longer authored** — the scope `index.html` lists variant
columns side-by-side with all meta + screen links, eliminating the
intermediate per-variant landing surface and reducing wireframe-depth to two
clicks (open index → click screen link).

## 5.1 Write `manifest.json`

Serialise the in-memory accumulator (built up during step-04's per-screen
loop) into the schema documented in
`framework/agents/wireframe-variant-generator.md > Output`:

```json
{
  "scope_slug": "<scope_slug>",
  "variant_id": "<variant_id>",
  "authored_at": "<ISO-8601 UTC at this moment>",
  "blueprint_sha256": "<blueprint.sha256 captured at step 2.1>",
  "screens": { ... }
}
```

Compute sha256. Write to `<output_dir>/manifest.json` with two-space indentation. Verify with `expected_min_bytes = 256`.

On `pass`, capture `manifest_written = true` and advance.

## 5.2 Write `variant-position.json`

Compose the artefact per the schema in `framework/agents/wireframe-variant-generator.md > Output`. The `dimension_positions`, `persona_binding`, and `design_philosophy` fields are **immutable mirrors** of `own.*` (verbatim — drift here is a structural bug). The `strengths`, `weaknesses`, `tradeoffs`, `use_when` fields are **self-authored** by this sub-agent based on:

- The chosen pattern picks in `manifest.screens` (e.g. compact-table at dense → strength: "Many records visible without scrolling").
- The bound persona's traits from `own.persona_traits` (e.g. daily user → use_when: "Daily users handling high volumes").
- The dimension positions at the poles (e.g. expert-leaning → weakness: "Less guidance for first-time users").

### 5.2.1 Concision contract (consultant-facing)

The strengths/weaknesses/tradeoffs/use-when fields are surfaced verbatim on
consultant-facing pages (the scope `index.html` right rail and
`comparison.html` cells). Consultants skim, not read. Enforce hard limits:

| Field | Limit |
|---|---|
| `strengths` | 3 bullets max; each ≤ 80 chars |
| `weaknesses` | 3 bullets max; each ≤ 80 chars |
| `tradeoffs` | 1 sentence; ≤ 140 chars |
| `use_when` | 1 sentence; ≤ 100 chars |

### 5.2.2 No-jargon contract

These four fields are **strictly plain-English**. The following content is
**banned** in any of `strengths`, `weaknesses`, `tradeoffs`, `use_when`:

- **Dimension notation.** No `D1+`, `D1-`, `D2+`, `D2-`, `D3+`, `D3-`, `D4+`, `D4-`, `D5+`, `D5-`, `D6+`, `D6-`. No `density-focus: +2`-style key:value. No bracketed dimension references.
- **Pattern-catalogue IDs.** No `table.compact`, `single-form.compact`, `single-form.two-column`, `master-detail-list`, `card-grid.spacious`, `inline-edit`, `command-palette`, `multi-step-wizard`, `modal-confirmation`, `notification-banner`, `notification-toast`, or any other catalogue pattern slug. Substitute descriptive nouns ("compact table", "two-column form", "wizard", "modal confirmation").
- **General-rule references.** No `GR-01`, `GR-02`, …, `GR-NN` style markers. The rule's intent (e.g. "destructive actions default focus on Cancel") may be stated in plain English without the GR-ID.
- **Requirement-ID notation.** No `F-NN`, `BR-NN`, `UI-NN`, `G-NN`, `[SRC: C-NNN]` style markers in these fields. (IDs remain in `manifest.screens[*].data_src_targets` and in screen HTML `data-src` attributes — those are audit-trail surfaces, not consultant copy.)
- **Bracketed annotations.** No `[STANDARD-RULE: …]`, `[AI-SUGGESTED: …]`, `[OUT-OF-SCOPE: …]`, `[DRIFT: …]`. These markers belong to the requirements pipeline; never propagate them into wireframe variant copy.

If the sub-agent's drafted text fails the no-jargon contract, re-draft. Do not
escape, hyphenate-around, or insert spaces into banned substrings to evade
detection — the contract is intent-bound, not regex-bound. The goal is text a
busy consultant can skim and act on.

### 5.2.3 Length and concision examples

**Acceptable** `strengths` entries (≤ 80 chars, plain English):

- "Many records visible without scrolling"
- "Keyboard shortcuts on every action"
- "Help text appears only where the field is ambiguous"

**Unacceptable** `strengths` entries (banned content):

- "table.compact composed with inline-edit on D3+2 pole" — banned: pattern ID + dimension notation.
- "Submit-on-Enter from any field (D1+1 → single-form.compact)" — banned: dimension notation + pattern ID.
- "Per GR-04 default focus on Cancel" — banned: GR-NN reference.

**Acceptable** `tradeoffs` (one sentence, ≤ 140 chars):

- "Faster for daily operators; harder to learn for occasional users."
- "Minimal scrolling; less whitespace and breathing room."

**Acceptable** `use_when` (one sentence, ≤ 100 chars):

- "Daily users handling high volumes who already know the product."
- "First-time users or low-frequency tasks where care matters more than speed."

### 5.2.4 Write and verify

Compute sha256. Write to `<output_dir>/variant-position.json` with two-space indentation. Verify with `expected_min_bytes = 384`.

On `pass`, capture `variant_position_written = true` and advance.

### 5.2.5 Self-validation: no-jargon enforcement

After write + verify, re-read the JSON and apply the no-jargon contract as a
post-write check:

```
For each of: strengths[*], weaknesses[*], tradeoffs, use_when:
  Confirm length within the limit (Section 5.2.1).
  Confirm no banned substrings (Section 5.2.2).
```

If any check fails, treat as `failed` per step 6's handback semantics. Do not
return `ok` with jargon-bearing variant-position content; the consultant-facing
surfaces (`index.html`, `comparison.html`) depend on this contract.

---

**Next:** Read fully and follow `step-06-self-validate-and-handback.md`.
