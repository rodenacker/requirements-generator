# svg-overlap-check.md

**Purpose:** Confirm that every inline `<svg>` figure in an analysis artefact is free of visual overlap. Deterministic — no LLM calls. The check is a pure geometry pass over the SVG primitives (`<rect>`, `<circle>`, `<ellipse>`, `<polygon>`, `<polyline>`, `<path>`, `<line>`, `<text>`) that the analysers emit. It catches three failure modes that the analysers' shared-grid layouts do not by themselves prevent:

1. **Node-on-node** — two node primitives whose axis-aligned bounding boxes (AABBs) intersect.
2. **Edge-through-node** — a polyline/line/path segment whose AABB intersects a node AABB the segment is *not* endpoint-anchored to.
3. **Label-on-edge** — a `<text>` element whose AABB intersects an edge segment AABB without an opaque background `<rect>` (a sibling element carrying the `*-bg` class convention used by the analysers) directly underneath.

The skill itself does not surface refusal predicates. The caller (a renderer-stage analyser) consumes the output, either reflows in memory and re-renders, or accepts the overlap and writes a layout-warning line into the artefact's diagnostics block.

**Inputs (caller-supplied):**

- `artefact_path` — **required** — repo-relative path to the rendered HTML artefact (e.g., `analyse-requirements/DATA-MODEL/data-model.html`, `analyse-requirements/TASK-FLOWS/task-flows.html`, `analyse-requirements/STATE-DIAGRAM/state-diagram.html`). The skill parses *only* the `<svg>...</svg>` blocks inside the file.
- `report_path` — **required** — path the skill writes its NDJSON output to (e.g., `framework/state/svg-overlap-<slug>.ndjson`). One line per detected overlap; zero lines on `pass`.
- `node_class_allowlist` — **required** — caller-supplied list of CSS class substrings that identify *node* primitives (not edges, not labels, not backgrounds). Per pipeline:
  - Task-flows: `["hta-goal", "hta-subgoal", "hta-operation", "tfd-start", "tfd-step", "tfd-decision", "tfd-exit-success", "tfd-exit-abort", "tfd-exit-escalate", "tfd-exit-retry", "tfd-exit-compensate", "plan-badge"]`.
  - Data-model: `["entity-box", "entity-header", "chen-diamond"]`.
  - State-diagram: `["state-node", "composite-state", "initial-node", "final-node", "choice-node", "junction-node"]`.
- `edge_class_allowlist` — **required** — class substrings that identify *edge* primitives.
  - Task-flows: `["hta-edge", "tfd-edge"]`.
  - Data-model: `["relationship-line"]`.
  - State-diagram: `["transition-edge"]`.
- `label_bg_class_suffix` — **required** — the convention the analysers use for opaque-background rects under labels. Pass `"-bg"` for all three analysers (matches `relationship-verb-bg`, `transition-label-bg`, `tfd-edge-guard-bg`).
- `tolerance_px` — **optional, default 1** — AABBs are inflated by `-tolerance_px` on every side before intersection. Used to allow a single-pixel shared-stroke touch (an edge that ends exactly on a node border) without firing the check.

**Outputs:** writes `report_path` and prints a single summary line. Exit signal:

- `pass` — `total: 0`. The caller advances.
- `fail` — `total: > 0`. The caller either reflows (preferred) or records a layout warning and proceeds. The skill does **not** decide; it reports.

**Used by:**

- `framework/agents/analyses/task-flows-analyser.md` — Step 10, after composing the HTML and computing sha256, before Step 11 Write.
- `framework/agents/analyses/data-model-analyser.md` — Step 9, after composing the HTML and computing sha256, before Step 10 Write.
- `framework/agents/analyses/state-diagram-analyser.md` — Step 9, after composing the HTML and computing sha256, before Step 10 Write.

Other analysers that emit inline SVG (`activity-diagram`, `sequence-diagram`, `user-journeys`, `use-cases`) MAY adopt the skill by supplying their own `node_class_allowlist` / `edge_class_allowlist`. Adoption is per-analyser; the skill itself is pipeline-agnostic.

## Procedure

### Pass 0 — load and parse

1. `Read` `artefact_path`. Locate every `<svg ...>...</svg>` block. Treat each `<svg>` as an independent figure; the geometry of one figure is unrelated to another's.
2. For each `<svg>`, extract:
   - `viewBox` (`"x y w h"`), used as the figure's coordinate frame.
   - All `<rect>`, `<circle>`, `<ellipse>`, `<polygon>`, `<polyline>`, `<path>`, `<line>`, `<text>` elements with their attributes (`x`, `y`, `width`, `height`, `cx`, `cy`, `r`, `rx`, `ry`, `x1`, `y1`, `x2`, `y2`, `points`, `d`, `class`).
3. Classify every element by its `class` attribute:
   - **node** — `class` contains any token in `node_class_allowlist`.
   - **edge** — `class` contains any token in `edge_class_allowlist`.
   - **label-bg** — `class` ends with `label_bg_class_suffix` (default `-bg`).
   - **label** — element is a `<text>` and is not classified as node or edge.
   - **other** — anything else (markers, dividers, gridlines, axes). `other` participates only as a no-op; it is never flagged.

   Apply allowlists case-sensitively; the analysers use lowercase kebab-case class names.

4. For each classified element, compute its AABB in the figure's `viewBox` coordinate system:
   - `<rect x y width height>` → `(x, y, x+width, y+height)`.
   - `<circle cx cy r>` → `(cx-r, cy-r, cx+r, cy+r)`.
   - `<ellipse cx cy rx ry>` → `(cx-rx, cy-ry, cx+rx, cy+ry)`.
   - `<polygon points="x1,y1 x2,y2 ...">` → min/max over the listed points.
   - `<polyline points="...">` → split into per-segment AABBs (one AABB per adjacent point pair). The segment list, not a single AABB for the whole polyline, is what enters the edge-through-node check.
   - `<line x1 y1 x2 y2>` → single-segment AABB `(min(x1,x2), min(y1,y2), max(x1,x2), max(y1,y2))`.
   - `<path d="M ... L ... C ...">` — split on `M`/`L`/`H`/`V`/`C`/`Q`/`Z` directives. For straight directives (`M`/`L`/`H`/`V`/`Z`), produce per-segment AABBs as above. For curve directives (`C`/`Q`), produce a single AABB enclosing all listed control points (this is a conservative over-approximation; the actual curve lies inside its control-point hull). Self-loop paths emitted by the state-diagram analyser are straight-segment Manhattan paths and decompose cleanly.
   - `<text x y>` — `(x, y - line_height, x + label_w, y)` where `line_height = 14` (matches the analysers' `<text>` font metric: 11 px body + 3 px baseline drop) and `label_w` is estimated as `len(text_content) * 6.5` (px per char at 11 px font, conservative).

   AABB endpoints carry a back-reference to their source element (id within the figure, class string, segment index for multi-segment primitives) so the report can name what overlaps what.

5. Build, per figure, an index keyed by category:
   - `nodes[]` — list of node AABBs plus `endpoint_ids` (set of element ids the node serves as an endpoint anchor for — populated in Pass 1).
   - `edge_segments[]` — list of (AABB, source_endpoint_xy, target_endpoint_xy) tuples.
   - `labels[]` — list of (AABB, has_bg) tuples; `has_bg = true` iff there exists a `label-bg` element whose AABB *contains* the label's AABB (point-inside-rect check, using the inflated tolerance).

### Pass 1 — node-on-node

For every unordered pair `(node_a, node_b)` in the same figure:

- Compute `intersects = aabb_intersect(node_a.aabb, node_b.aabb, tolerance_px)`. AABB intersection is the standard half-plane test: `a.x_min < b.x_max - tol AND a.x_max > b.x_min + tol AND a.y_min < b.y_max - tol AND a.y_max > b.y_min + tol`.
- Skip the pair when one node fully *contains* the other AND one of them carries the class `composite-state` or `entity-header` — composite states legitimately contain substates, and entity headers legitimately sit inside entity boxes. Containment is `a.x_min <= b.x_min AND a.x_max >= b.x_max AND a.y_min <= b.y_min AND a.y_max >= b.y_max` (or the reverse).
- On a true intersection, emit one NDJSON line:

  ```
  {"figure_id":"<svg n>","kind":"node_on_node","a_class":"...","b_class":"...","a_aabb":[x0,y0,x1,y1],"b_aabb":[x0,y0,x1,y1]}
  ```

### Pass 2 — edge-through-node

For every `edge_segment` in the figure, and every `node` in the figure:

- Resolve endpoint anchorage. The segment's `source_endpoint_xy` and `target_endpoint_xy` are taken from the polyline's first and last points (or the line's `(x1,y1)`/`(x2,y2)`). A node is *anchored* to this segment iff either endpoint lies within `tolerance_px + 2` of any of the node's four AABB edges. Pre-compute the set of anchored nodes per segment in a single pass and cache.
- Test `aabb_intersect(segment.aabb, node.aabb, tolerance_px)`.
- On intersection where `node` is *not* in the segment's anchored-nodes set, emit:

  ```
  {"figure_id":"<svg n>","kind":"edge_through_node","edge_class":"...","segment_index":N,"node_class":"...","node_aabb":[x0,y0,x1,y1],"segment_aabb":[x0,y0,x1,y1]}
  ```

  The marker-only case (`marker-end="url(#...)"`) is irrelevant — markers are attached to the segment, not to a separate node, and so cannot trigger this check.

### Pass 3 — label-on-edge

For every `label` in the figure, and every `edge_segment` in the figure:

- Test `aabb_intersect(label.aabb, segment.aabb, tolerance_px)`.
- On intersection where `label.has_bg = false`, emit:

  ```
  {"figure_id":"<svg n>","kind":"label_on_edge","label_text":"<truncated to 80 chars>","edge_class":"...","segment_index":N,"label_aabb":[x0,y0,x1,y1],"segment_aabb":[x0,y0,x1,y1]}
  ```

- When `label.has_bg = true`, the analysers' convention says the opaque rect occludes the underlying line beneath the label — no overlap is reported.

### Summary line

After all NDJSON lines are written, print exactly one summary line to stdout:

```
svg-overlap-check: figures=<F> total=<T> node_on_node=<N> edge_through_node=<E> label_on_edge=<L>
```

Where `figures` is the count of `<svg>` blocks parsed, `total = N + E + L`, and `N`/`E`/`L` are the per-kind counts. `total: 0` is the only condition under which the caller may advance without recording a layout warning.

## Self-validation

- All five required input paths/lists are supplied by the caller; the skill has no defaults and refuses to run with any missing.
- AABB intersection is computed using inflated tolerance (`-tolerance_px` per side) — a single-pixel shared-stroke touch is *not* a violation.
- Per-segment AABBs are used for polylines and paths, never a single AABB enclosing the whole multi-vertex shape. A wrap-around edge that bows around the figure must not produce a giant AABB that "intersects" every node in the bow — only the actual segments that pass through a node fire the check.
- Composite-state containment and entity-header containment are explicitly excluded from `node_on_node` flagging. These are the only legitimate node-inside-node arrangements the analysers emit.
- Labels with the `*-bg` opaque-background sibling (analyser convention) are exempt from `label_on_edge`. The check would otherwise false-fire on every analyser's standard edge label.
- The skill writes `report_path` even on `total: 0` so the caller and its handback gate can read the file and trust the summary line without re-running the skill.
- The skill performs no transformation of the artefact. Its only side effect is the write to `report_path` and the summary print. The caller decides whether to reflow + re-render or to accept and append a diagnostics line.

## Anti-Patterns

- Do not call any LLM. The check is pure geometry — AABB intersection and a containment exclusion. A model in the loop would re-introduce non-determinism.
- Do not parse arbitrary HTML — only `<svg>` blocks inside the artefact. The skill is not a generic SVG validator.
- Do not exact-curve-bound a `<path>`. The Bézier control-hull AABB is a conservative over-approximation; that's the intentional bias — overreporting curve-vs-node is acceptable because the analysers' curves are confined to short marker-arrow segments and bowed include-arrows (use-cases). Tightening would require Bézier flattening and pays no dividend at MVP fidelity.
- Do not modify the artefact. Remediation is the caller's job; this skill only reports.
- Do not collapse per-segment AABBs to per-polyline AABBs. A long polyline routed around the figure can have a giant bounding box that touches every node, none of which the polyline itself actually crosses. Per-segment is the only correct granularity.
- Do not skip Pass 0's classification. An edge mis-classified as a node, or a node-background mis-classified as a label-bg, produces silent false negatives. The caller-supplied allowlists are mandatory and case-sensitive.
- Do not treat a label without `*-bg` as a soft warning. The analysers' contract is *every* edge-overlapping label carries an opaque background; a label without one is a render bug, not a stylistic choice.
- Do not flag a self-loop's own state as `edge_through_node`. The self-loop's endpoints both anchor to the same state — the anchored-nodes set correctly contains that state and the check correctly skips it.
- Do not run before the artefact is on disk. The skill reads from `artefact_path`; passing it the in-memory composed string is not supported by design (the same on-disk read also guards against the analyser composing one string and writing another).
- Do not loop without bound. The skill is a single linear pass over the figure; quadratic in nodes-times-edges per figure is acceptable because per-figure node and edge counts are bounded by the analysers' caps (≤ 30 nodes / ≤ 30 transitions for state-diagram; similar bounds elsewhere). No nested retry / repair logic lives here — the caller owns the reflow loop.
