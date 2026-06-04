# map-faceted-classification-to-ui.md

**Purpose:** Translate a `faceted-classification` analysis artefact into UI-inventory entries (filter chips, facet rails, range controls, sort axes, search-box field sets) for downstream design consumption. **Stub at MVP** — like the other analyses' map-skills, this is registry metadata read by a future design-spec-drafter, **not** invoked by `/analyse-requirement`. Faceted-classification exposes only the `upstream-only` sidecar role at MVP, so the blueprint-architect does not consume the facet model directly; this file documents the wider mapping for human design authors and for the day a dedicated `per-surface-facets` architect role is added (see `framework/assets/analyses/faceted-classification-reference.md > Sidecar projection`).

## Inputs

- `analyse-requirements/FACETED-CLASSIFICATION/facet-map.html` — the faceted-classification artefact (or its embedded `<pre><code class="language-json" id="faceted-classification-body">` model for the structured subset).

## Mapping

### Facet kind → UI control

| Facet kind | UI realisation |
|---|---|
| `enum` (single-select) | **filter chips** (or a dropdown) on the owning collection surface — one chip per value, single active. |
| `multi-enum` (multi-select) | a checkbox **facet rail** — several values active at once. |
| `date-range` | a **date-range picker** scoped to the backing timestamp property. |
| `range` (numeric, **stated bands**) | a **range control** (slider / min-max) bounded by the named bands. |
| `range` **un-banded** (flagged `needs-a-threshold`) | **not** a range control yet — a design unknown to settle before the surface is built; may serve as a `text-search` / sort axis only. |
| `boolean` | a **toggle chip**. |
| `text-search` | the **search box**'s covered field set (the fields the query matches). |

### Facet attribute → surface affordance

- **sort-eligible facet** → a **sort axis** (column-sort header per `GR-12`, or a sort control). Pagination is always present for a collection per `GR-11`.
- **value set** → the chip options / facet-rail checkboxes / range bounds. Sourced from the spec; never widened.
- **backing property** → provenance only. The facet *control* is UI-only chrome (exempt from the wireframe `data-prop` closed set); the backing `Shape.Property` is what justifies the control's existence, not a `data-prop` binding. A facet does **not** introduce a bindable property.

### Register → design signal

- **non-orthogonal pair** → not two filters; a contradiction to resolve before design — collapse to the determining dimension (the dependent one is derivable), or re-derive the facets.
- **`no-slice-dimension` collection** → a list surface with no meaningful filter — render the table + search/pagination chrome only; do not manufacture a filter rail.
- **`needs-a-threshold` facet** → an `[AI-SUGGESTED]` resolver question (the band must be named) before the range control is built.

## Note

No widening. Every control this mapping proposes must trace to a facet that traces to a §7 `Shape.Property` / `F-NN` / `§6.4` source. The mapping never introduces a facet, a value, a backing property, or a slicing dimension the analysis did not carry. Facets scaffold the **UI-only controls the wireframe anti-fabrication rule exempts** (search / sort / filter chips / pagination); they are not bindable `data-prop` properties.
