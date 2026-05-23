# Pattern-binding guidance (wireframe-private)

**Role:** asset (wireframe-private).

**Purpose:** Help the variant-generator pick the right *primary* pattern category for each screen in the blueprint, given the screen's requirement IDs and the variant's dimension positions. This is composition guidance, not enforcement — the catalogue at `framework/assets/pattern-catalogue/` remains the source of truth for what each pattern can do.

**Used by:**
- `framework/agents/wireframe-variant-generator.md` — at its per-screen primary-pattern selection step. Consulted in conjunction with `framework/assets/wireframes/tradeoff-dimensions-registry.md` (the latter governs which *variant* of the chosen pattern to compose).
- `framework/skills/check-pattern-coverage.md` — uses the same intent → category heuristics in its preflight matching.

**Living doc.** Append rows as new requirement-type → pattern-category patterns emerge. Never remove rows — the catalogue is open; this guidance is shaped by usage.

---

## Section 1 — Requirement-type → pattern-category mapping (primary slot)

Use this table to derive the *category* shortlist for a screen. Within the category, the variant-generator picks the specific pattern + pattern variant per the trade-off positions.

| Requirement type (verb / noun shape) | Primary pattern category | Common picks |
|---|---|---|
| `F-NN` with verbs {create, add, capture, enter, register} | `forms/` | `single-form`, `multi-step-wizard`, `modal-form` |
| `F-NN` with verbs {edit, update, modify, configure} | `forms/` | `single-form`, `inline-edit`, `drawer-form` |
| `F-NN` with verbs {browse, list, search, filter, find} | `collections/` + `forms/search-and-filter` | `table`, `data-list`, `card-grid`, `master-detail-list` |
| `F-NN` with verbs {approve, reject, sign-off, decide} | `forms/` + `surfaces/modal-confirmation` | `single-form` for the decision payload + modal-confirmation gating |
| `F-NN` with verbs {delete, remove, archive, cancel, destroy} | `surfaces/modal-confirmation` | always `modal-confirmation` per `GR-04` |
| `F-NN` with verbs {upload, import, attach} | `forms/file-upload` (T3) + composing parent | `file-upload` inside `single-form` or `multi-step-wizard` |
| `F-NN` with verbs {export, download, generate report} | `forms/search-and-filter` + export action | typically a filtered `table` + an export CTA |
| `F-NN` with verbs {view, see, inspect, drill, examine} | `collections/detail-page`, `surfaces/drawer-detail` | `detail-page` for primary surface, `drawer-detail` for inline drill |
| `F-NN` with verbs {authenticate, log in, sign in} | `auth/` + `layouts/centered-form` | `login-form` inside `centered-form` |
| `UI-NN` with collection nouns | `collections/` | `table`, `card-grid`, `data-list`, `dashboard` |
| `UI-NN` with summary / KPI nouns | `collections/dashboard`, `collections/kpi-tile` | `dashboard` of `kpi-tile`s |
| `UI-NN` with status / lifecycle nouns | `feedback/notification-banner`, badge per `GR-16` | `notification-banner` for state-requiring-acknowledgement |
| `BR-NN` with validation / constraint shape | `feedback/inline-validation` (secondary slot) | composed inside `single-form` per `GR-05` |
| `BR-NN` with permission / RBAC shape | hidden in chrome per `GR-01` / `GR-02` | no separate screen; affects chrome of the underlying screen |
| `G-NN` (top-level goal) | maps to a flow, not a single screen | the goal drives which screens get composed; not a direct pick |
| `§5` Task flow | sequence of screens | each step of the flow becomes its own `S-NN` row |
| `§7` Data shape | informs slots inside `single-form` / `detail-page` | the data shape's fields populate the form's `sections` / `fields` slots |

---

## Section 2 — Secondary slot composition (within a screen)

A screen's primary pattern fills the dominant region; secondary patterns fill auxiliary slots (validation messages, tooltips, modals, banners). The variant-generator composes these per screen.

| Secondary need | Pattern |
|---|---|
| Per-field validation | `feedback/inline-validation` (in form), respecting `GR-05` (on-blur / on-submit) |
| Cross-field validation summary | `feedback/notification-banner` at top of form |
| Destructive action confirmation | `surfaces/modal-confirmation` (gates the destructive action; default focus on Cancel per `GR-04`) |
| Transient success / error | `feedback/notification-toast` per `GR-14` |
| Persistent state requiring acknowledgement | `feedback/notification-banner` per `GR-14` |
| Empty state | `feedback/empty-state` with entity-named copy per `GR-08` |
| Zero-results state (after filtering) | `feedback/empty-state` distinguishing from zero-data per `GR-09` |
| Loading state | `loading-skeleton` per `GR-10`; no indicator <300ms, skeleton 300ms–3s, skeleton+"still loading…" >3s |
| Pagination chrome (always for collections) | `navigation/pagination` per `GR-11`; 5/10/20/50 with default 20 |
| Sort chrome (always for tables) | column headers per `GR-12`; single-column sort, asc→desc |
| Inline help / tooltip | tooltip per `GR-17` for icon-only controls (also matching `aria-label`) |
| Multi-screen progress | `navigation/stepper-indicator` (inside `multi-step-wizard`) |
| Tabbed sub-navigation within a screen | `navigation/tabs` |
| Side-by-side comparison or detail (inline drill) | `surfaces/drawer-detail` |
| Read-only mode banner (entity in terminal state) | `feedback/notification-banner` per `GR-03` |
| Permission-denied (direct-access) | per-page banner naming missing permission per `GR-02` |

---

## Section 3 — Slot-budget hints

Soft per-screen budgets the variant-generator uses to avoid composing visually-overloaded screens. Exceeding a budget is allowed only when the variant's `dimension_positions` justify it (e.g. `density-focus: +2` raises the per-screen pattern budget by 1).

| Slot class | Default budget per screen | Density-+2 budget |
|---|---|---|
| Primary patterns | 1 | 1 (the primary slot is always exactly one pattern) |
| Secondary patterns | 3 | 5 |
| Modal / drawer overlays simultaneously rendered as state | 1 | 2 |
| Distinct feedback regions (banner / toast / inline) | 2 | 3 |

When a screen's blueprint `intent` + `secondary_intent` would require exceeding the budget even at `density-focus: +2`, the variant-generator splits the responsibility across screens (subject to the blueprint's screen inventory) or surfaces a structured warning to the comparator's drift detection.

---

## Section 4 — `GR-NN` integration points

The variant-generator must compose secondary patterns to honour the active general rules. The most relevant on the wireframe layer:

| GR | Pattern impact |
|---|---|
| `GR-01`, `GR-02` | Hide unauthorised actions in chrome; do not render disabled. RBAC-affected variants need to render the persona's *visible* chrome only. |
| `GR-03` | On terminal state, hide mutating actions; show top banner. Read-only state of a detail page is a state worth rendering visually per the variant's `states_rendered`. |
| `GR-04` | Destructive primary action → modal-confirmation, destructive-styled CTA, default focus on Cancel. |
| `GR-05` | Validation on-blur sync / on-submit cross-field. No on-keystroke validation in rendered states. |
| `GR-07` | Autofocus first editable field in create/edit modes. |
| `GR-08`, `GR-09` | Distinguish empty-data (entity-named create CTA) from zero-results (filter chips, clear-all). |
| `GR-10` | Loading state visualisation: no indicator <300ms; skeleton 300ms-3s; skeleton + "still loading…" >3s. |
| `GR-11` | Always render pagination chrome on collections; 5/10/20/50 default 20. |
| `GR-12` | All collection columns sortable by default; single-column sort; asc → desc. |
| `GR-13` | Field-count drives variant: ≤8 single form, 9-20 sectioned, >20 wizard/settings-shell. |
| `GR-14` | Toast for transient, banner for persistent. |
| `GR-15` | Badge counts: exact ≤99, `99+` above, hide at 0. |
| `GR-16` | Status badge colour mapping (success/error/warning/info/draft) — always pair colour with icon or text. |
| `GR-17` | Icon-only controls require tooltip + aria-label. Never icon-only for destructive primary. |
| `GR-18` | Tables collapse to vertical card list on <768px (per `§6.6.5` mobile coverage). |

---

## Anti-patterns

- Do not bind a pattern by category alone when the catalogue entry's `when-not-to-use` explicitly forecloses the screen's intent. Section 1 is a shortlist; `when-not-to-use` is the hard gate.
- Do not compose patterns that violate `composition-rules > must-not-contain`. A `single-form` cannot contain another `single-form`; a `multi-step-wizard` cannot contain a `single-form`; a `table` cannot live inside a `single-form`. Each catalogue entry's `composition-rules` is the source of truth.
- Do not silently downgrade a `GR-NN` integration point in pursuit of a particular dimension position. The `GR-NN` rules are deterministic defaults; variants choose composition style, not rule compliance.
- Do not add a new pattern category in Section 1 without first authoring a corresponding catalogue entry. Section 1 names categories that exist; "guidance for patterns we plan to author" pollutes the matcher.
- Do not exceed slot budgets without a `dimension_positions` justification recorded in `variant-position.json`. The comparator's drift detection cross-checks budget overruns against declared positions.
