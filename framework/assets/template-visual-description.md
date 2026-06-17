<!-- ROLE: asset (template). Populated top-to-bottom in one pass by `framework/skills/describe-visual-input.md`. No {{placeholders}} may remain; no section may be blank (use the empty sentinel). This is the frozen, authoritative textual description of ONE visual input. Downstream input-consumers read it INSTEAD of the image. -->

# Visual description: {{original-filename}}

<!-- guidance: one line a consultant can scan to confirm the describer understood what the visual is. -->
**In plain terms:** {{one-sentence summary of what this visual depicts and its apparent purpose}} [SRC: {{original-filename}}]

| Field | Value |
|---|---|
| Source file | {{original-filename}} |
| Diagram type | {{ui-mockup \| wireframe \| screenshot \| erd \| flowchart \| use-case-diagram \| sequence-diagram \| activity-diagram \| state-diagram \| org-chart \| dashboard \| whiteboard \| other-visual}} |
| Rendered from vector? | {{no \| yes — via <render-tool>}} |

**Marker legend** (canonical set only — never invent a marker):
- `[SRC: <original-filename>]` — an item the visual **shows** (authoritative *what*). Cites the original consultant-dropped filename.
- `[AI-SUGGESTED: AI-NNN | blocking|non-blocking]` — an item the describer **inferred** or that is **uncertain** (e.g. a field that may be placeholder/lorem text, an implied relationship, an unlabelled control). Numbered per-description from `AI-001`. `blocking` only when the uncertainty would materially change a downstream requirement. Routes to the resolver downstream.
- No other marker is permitted. Express all uncertainty through `[AI-SUGGESTED]` — do **not** use `[CONFIDENCE]` or any ad-hoc tag.

<!-- guidance: empty-section sentinel. When a section genuinely does not apply to this diagram type (e.g. an ERD has no controls; a flowchart has no data shapes), write exactly: "_None visible in this visual._" Do not delete the section. -->

---

## Tier A — The *what* (authoritative, citation-bound)

> These describe what the business/users want represented and how the frontend must work. Each item is `[SRC: …]`-cited because the visual shows it — **except** items that are inferred or possibly-placeholder, which carry `[AI-SUGGESTED]`. Object properties are a **closed set**: never assert a field as real unless the visual genuinely shows it as data.

### A1. Data objects / entities
<!-- guidance: every table, card, form, detail pane, ERD box, or use-case subject names a candidate object. -->
{{list each object/entity with a [SRC: …] cite}}

### A2. Object properties / fields (the closed set)
<!-- guidance: form inputs, table columns, detail rows, ERD attributes. THE HIGH-RISK SECTION: a field shown only as placeholder/lorem/sample text is NOT confirmed data — flag it [AI-SUGGESTED: AI-NNN | blocking]. Only fields the visual genuinely presents as real data carry [SRC]. -->
{{per object, list its fields; [SRC: …] for genuine data fields, [AI-SUGGESTED: AI-NNN | blocking] for placeholder/uncertain fields}}

### A3. Relationships & cardinality
<!-- guidance: ERD crow's-feet, master-detail layouts, nested/embedded lists, "belongs to" groupings. -->
{{list relationships with cardinality where shown; mark inferred cardinality [AI-SUGGESTED]}}

### A4. Field types, formats, constraints, enumerations
<!-- guidance: control type implies type (date picker→date; dropdown with fixed options→enum; currency mask→money); required markers (*); max-length hints; visible validation. -->
{{list typed/constrained fields and any visible enumerations}}

### A5. Actors / roles
<!-- guidance: use-case actors, swimlane labels, role-gated screens, "logged in as…" chrome. -->
{{list actors/roles}}

### A6. User tasks / use cases
<!-- guidance: use-case ovals; primary CTAs/action buttons (verbs = tasks). -->
{{list tasks/use-cases}}

### A7. Task flows / sequences / decision branches
<!-- guidance: flow charts, activity/sequence diagrams, multi-step wizards: steps, order, decision points, branches, loops. -->
{{describe the flow(s); name decision points and branch labels}}

### A8. Object states & state transitions
<!-- guidance: status chips/badges, state diagrams, kanban columns, status filters. -->
{{list states and any transitions shown}}

### A9. Business & validation rules implied
<!-- guidance: conditional/disabled UI, error-message text, "if X then Y" in flows, visible required/forbidden combinations. -->
{{list rules; mark inferred rules [AI-SUGGESTED]}}

### A10. System boundary / external integrations
<!-- guidance: use-case system-boundary box; sequence-diagram lifelines for external services; "Export to <system>" actions. -->
{{list external systems/integrations}}

---

## Tier B — The *how* (mined, advisory only — requirement signals)

> These bias the system's design but are **never authoritative**. They are possibilities/desiderata the system may honour or diverge from. Record what the visual shows; downstream design holds authority over the *how*.

### B1. Information architecture / navigation
<!-- nav menus, tabs, breadcrumbs, sitemap structure. -->
{{describe IA/navigation}}

### B2. Required interactions / behaviours
<!-- buttons, drag-drop, inline-edit, bulk-select, gestures. NOTE: the *requirement* ("user must be able to reassign") is Tier-A; its realization (drawer vs modal) is Tier-B. -->
{{describe interactions/affordances}}

### B3. Layout, grouping, control choice
<!-- where fields sit, which control was chosen per field. -->
{{describe layout/grouping/controls}}

### B4. Visual styling / brand / density / posture
<!-- colour, typography, whitespace, information density, apparent UX posture. -->
{{describe styling/density/posture}}

### B5. Reporting / dashboard / aggregation
<!-- charts, KPI tiles, summary widgets. -->
{{describe reporting/aggregation surfaces}}

### B6. Notification points
<!-- toast/badge/bell icons, alert banners. -->
{{describe notifications}}

### B7. Audit-trail surfaces
<!-- "history" / "activity log" panels. -->
{{describe audit-trail surfaces}}

### B8. Volume / scale hints
<!-- "1,247 records", pagination counts, table sizing. -->
{{describe any volume/scale signals}}

---

## Provenance & open questions

### Verbatim text observed
<!-- guidance: a faithful dump of the legible text in the visual (labels, headings, button text, sample values), so downstream consumers and the consultant can audit the description against the source. Mark sample/placeholder values as such. -->
{{verbatim observed text}}

### Ambiguities, placeholders, and unreadable regions
<!-- guidance: every [AI-SUGGESTED: AI-NNN] raised above is itemized here as a resolver-ready question. Blocking items are the ones that would change a downstream requirement. Also note any region too low-resolution/cropped to read. -->
{{numbered list of AI-NNN items with a one-line question each; or the empty sentinel}}

<!-- Self-validation: no {{placeholders}} remain; every section populated or sentinel'd; every Tier-A item cited [SRC: <original-filename>] or flagged [AI-SUGGESTED]; only canonical markers used; every placeholder-suspect property flagged [AI-SUGGESTED | blocking]. -->
