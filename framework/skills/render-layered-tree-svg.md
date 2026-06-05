# render-layered-tree-svg.md

**Purpose:** Compute and emit one self-contained inline `<svg>` for a **layered tree** — nodes arranged in ordered top→bottom rows, edges as vertical-S cubic Béziers between adjacent-row node centres. Nodes and edges share a single `viewBox` coordinate space, so an edge is derived from the same node centres it connects and **always meets its node regardless of node count or viewport width**. This is the canonical definition of the layered-tree SVG layout; callers supply rows/nodes/edges and a colour palette, never the layout arithmetic. Replaces ad-hoc per-methodology geometry (e.g. hub-and-spoke fans with straight radial edges, or absolute-positioned SVG overlays on CSS-flowed cards) whose hand-authored coordinates cannot stay aligned.

**Inputs:**
- `rows` — ordered list (top→bottom) of layers. Each layer = `{ class, nodes[] }` where `class` is the per-layer node class (e.g. `node-outcome`, `node-theme`). Each node = `{ id?, label_lines[], shape, rx?, flagged? }`:
  - `id` — optional stable id shown as a `node-id` line (omit when `node_text.show_id` is false for the layer).
  - `label_lines[]` — caller pre-splits/truncates the label into the lines to render; the skill emits one `<tspan>` per line (does **not** truncate).
  - `shape` — `"rect"` (default) or `"circle"`.
  - `rx` — corner radius for `rect` (default `6`).
  - `flagged` — when true, append `flagged` to the node `<g>` class (caller styles it).
- `parent_child_edges` — `[{ parent_id, child_id, edge_class }]`. One vertical-S cubic per edge; `parent` must sit in a row above `child` (normally the adjacent row).
- `same_row_edges` *(optional)* — `[{ a_id, b_id, edge_class, dashed }]`. Rendered as a shallow dashed arc bulging out of the row band (used for peer/proximity links, e.g. thematic cross-theme proximity). Empty/absent in the common case.
- `row_labels` *(optional)* — `[{ row_index, text }]`. Left-margin `<text class="layer-label">` per present row.
- `node_text` — per-layer (keyed by layer `class`, or a single default) `{ show_id: bool, anchor: "start"|"middle" }`. `start` → left-aligned id+label (OST style); `middle` → centred multi-line label (theme-map style). The skill emits the matching `x`; the **template CSS** must set the matching `text-anchor`.
- `constants` *(optional, overridable)* — defaults `boxW=170 boxH=52 hGap=18 vGap=72 marginX=24 marginY=20`. Override `boxW`/`boxH` for wider or taller node boxes (e.g. two-line theme labels). `arc_dip` (default `28`) governs `same_row_edges` arc depth.
- `aria_label` — the `<svg>` accessible name (caller composes, naming the counts).

**Outputs:** a structured return:
- `svg_markup` — the full `<svg …>…</svg>` string (edges, then row labels, then node `<g>` groups), ready to drop inside the caller's wrapper element.
- `W`, `H` — the computed natural pixel dimensions (also stamped on the `<svg>` as `width`/`height`/`viewBox`).

**Used by:**
- `framework/agents/analyses-inputs/opportunity-solution-trees-analyser.md` — Step 10B Sub-step B (rows: Outcome / Opportunities[+sentinel] / Solutions / Assumption Tests; `node_text` start; layer-4-absent → 3 rows).
- `framework/agents/analyses-inputs/thematic-analysis-analyser.md` — Step 10B Sub-step B (rows: Root / Themes / Codes-when-toggled; `node_text` middle; `same_row_edges` = cross-theme proximity).

## Procedure

The analyser does this arithmetic in-memory; exact pixels may vary slightly run-to-run, but **alignment cannot break** because edges are derived from the node centres.

### 1. Layout geometry

Let `numRows` = number of present rows. With constants `boxW boxH hGap vGap marginX marginY`:

- For each row `k` with `n_k` nodes: `rowW_k = n_k*boxW + (n_k-1)*hGap`.
- `inner = max(rowW_k over all rows)`.
- `W = inner + 2*marginX`.
- `H = numRows*boxH + (numRows-1)*vGap + 2*marginY` (then `H += arc_dip` when `same_row_edges` is non-empty, to reserve the arc band).
- Row `k` start x = `marginX + (inner - rowW_k)/2` (centre each row).
- Node `i` in row `k`: `nx = rowStartX + i*(boxW+hGap)`, `ny = marginY + k*(boxH+vGap)`.
- Node centre `cx = nx + boxW/2`; `top = ny`; `bottom = ny + boxH`; vertical centre `cy = ny + boxH/2`.

The `<svg>` carries `role="img" width="{W}" height="{H}" viewBox="0 0 {W} {H}"` (natural pixels, **default** `preserveAspectRatio`) plus the `aria_label`, so wide trees scroll inside the wrapper rather than distorting. Never emit `preserveAspectRatio="none"` or an absolute-positioned overlay.

### 2. Emission order (load-bearing)

Emit children in exactly this order so edges paint **under** the node boxes:

1. **Parent→child edges** — one `<path class="edge {edge_class}">` per `parent_child_edges`, with
   `d="M {p.cx} {p.bottom} C {p.cx} {my} {c.cx} {my} {c.cx} {c.top}"` where `my = (p.bottom + c.top)/2` (a vertical-S cubic; leaves the parent straight down and arrives at the child straight down, so it never crosses sideways into garbage). For a `circle` endpoint, use the circle's top/bottom (`cy ∓ r`) — identical to `top`/`bottom` since `r = boxH/2`.
2. **Same-row arcs** *(if any)* — one `<path class="edge {edge_class}">` (carry the caller's `dashed` modifier class) per `same_row_edges`, bulging below the shared row band:
   `d="M {a.cx} {rowBottom} C {a.cx} {rowBottom+arc_dip} {b.cx} {rowBottom+arc_dip} {b.cx} {rowBottom}"`.
   When a **lower** row is occupied (would collide), flip the arc above the row: replace `rowBottom` with `rowTop` and `+arc_dip` with `-arc_dip`.
3. **Row labels** *(if any)* — `<text class="layer-label" x="4" y="{row.ny + boxH/2}">{text}</text>`, one per `row_labels` entry.
4. **Nodes** — one `<g class="node {layer.class}{ flagged}">` per node, in row then index order:
   - `rect`: `<rect x="{nx}" y="{ny}" width="{boxW}" height="{boxH}" rx="{rx}"/>`.
   - `circle`: `<circle cx="{cx}" cy="{cy}" r="{boxH/2}"/>`.
   - Text — resolve `node_text` for this layer:
     - x-coordinate: `anchor:"start"` → `tx = nx + 8`; `anchor:"middle"` → `tx = cx`. (Matching `text-anchor` comes from template CSS.)
     - If `show_id` and `id` present: `<text class="node-id" x="{tx}" y="{ny+15}">{id}</text>`, then `<text class="node-label" x="{tx}" y="{ny+31}">` with one `<tspan>` per `label_lines` (lines 2+ carry `x="{tx}" dy="14"`).
     - Else (no id): `<text class="node-label" x="{tx}" y="{firstY}">` with one `<tspan>` per `label_lines` (lines 2+ `x="{tx}" dy="16"`), where `firstY = ny + boxH/2 - 7*(L-1)` for `L` label lines (vertically centres the block).
   - **XML-escape** every `<text>`/`<tspan>` payload (`<`, `>`, `&`, `"`).

### 3. CSS contract (template supplies the values; skill fixes the hooks)

The caller's template `<style>` must provide:
- A **wrapper element** (e.g. `.tree-wrap`, `figure.theme-map`) with `overflow-x: auto` so wide diagrams scroll. The `<svg>` must render at **natural width** (`display:block; max-width:none;`) — **never** `width:100%` (which squashes a wide tree).
- `.edge { fill:none; stroke:…; stroke-width:… }` plus one rule per `edge_class` used, and a dashed modifier (`stroke-dasharray`) for any `dashed`/orphan edge class.
- `.node-<layer> rect`/`circle` fills+strokes per layer, and a `.node.flagged` rule if any node is `flagged`.
- `.node-id`, `.node-label` (set `text-anchor: middle` on layers that use `anchor:"middle"`), and `.layer-label` text styles.

## Self-validation

- Every `parent_id`/`child_id`/`a_id`/`b_id` in the edge lists resolves to a node present in `rows`. A dangling reference is a caller bug — fail closed (the caller's diagram-completeness gate, e.g. OST/thematic Gate 4, depends on node↔edge parity).
- Each edge's two endpoints are read from the **same** computed node centres emitted in the SVG; never hand-author an endpoint coordinate independently.
- `parent` sits strictly above `child` (smaller `row_index`). Same-row links go through `same_row_edges`, not `parent_child_edges`.
- `W`/`H` on the `<svg>` equal the computed values; the wrapper, not `preserveAspectRatio`, absorbs overflow.

## Anti-Patterns

- **No straight radial edges from one hub** (`d="M hubX hubY L childX childY"`) and **no 2-D grid of children.** That is the unreadable hub-and-spoke this skill replaces: many long diagonals converge on one point and cross each other. Children go in a single centred row beneath their parent; edges are vertical-S cubics.
- **No `width:100%` on the `<svg>`** and no `preserveAspectRatio="none"`. Wide trees scroll in the wrapper; they are never distorted to fit.
- **No absolute-positioned `<svg>` overlay** on CSS-flowed/auto-fit cards. Nodes and edges live in one `viewBox`.
- Do not truncate labels here — the caller pre-splits `label_lines` so each methodology controls its own label policy.
- Do not bake methodology semantics (themes, opportunities, orphans) into this skill — it sees only generic rows, nodes, and edges; the caller assigns classes and decides which nodes exist.
