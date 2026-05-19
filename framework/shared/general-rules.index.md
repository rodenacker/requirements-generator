# General Rules — index

Slim index of `framework/shared/general-rules.md`. Loaded by the requirements-resolver in place of the full body so the catalogue does not sit in context for the entire run. When the resolver's follow-up filter (`framework/skills/flag-gaps-ambiguities.md` step 2) needs a rule's full **Rule** + **Rationale** text — e.g. to render the canonical answer into a `follow_ups[*].a` — Read the matching `## GR-NN` section from `framework/shared/general-rules.md` on demand.

Format: one line per rule — `GR-NN | <Applies to predicate, condensed> | <one-line headline of the canonical answer>`.

Add a row here when a new rule is appended to `general-rules.md`; never renumber.

| ID | Applies to | Headline |
|---|---|---|
| GR-01 | §6.5 RBAC cells where the persona is read-only / Viewer / Auditor | Hide excluded actions in the UI; do not render disabled controls. |
| GR-02 | §6.5 RBAC cells where an action is denied but the screen is reachable via shared/deep link | Hide denied actions in chrome; on direct access show in-page permission-denied banner naming the missing permission, not a 403. |
| GR-03 | §7 entities whose §2.3 lifecycle includes Archived/Closed/Cancelled or other read-only terminal state | On detail screens in a read-only state, hide all mutating actions and show a top-of-page banner naming the state and the path back to editability. |
| GR-04 | §6.5 cells with `A` (approve), or actions named Delete/Remove/Send/Publish/Submit-for-approval/Charge/Cancel-order/Issue without undo | Modal-confirm naming the affected entity, destructive-styled primary action, default focus on Cancel. |
| GR-05 | §6.4 user-facing validation feedback on §7 entity fields | Validate on blur for sync rules; on submit for cross-field/async; never on keystroke. |
| GR-06 | §6.4 forms mixing required and optional fields | Mark required with leading asterisk + single legend; if ≥80% required, mark optional with "(optional)" instead. |
| GR-07 | Create/edit forms in modals, drawers, full-page layouts | Autofocus the first editable field; exception when preceded by a destructive/navigational confirmation step. |
| GR-08 | Lists, tables, dashboard widgets, detail panels bound to a §7 entity collection | Empty-state copy must name the entity and offer the primary creation CTA; "No data" / "Nothing here" not acceptable. |
| GR-09 | Collections with search or filter controls | Distinguish zero-data (entity-specific empty + create CTA) from zero-results (active filter chips, Clear-all, no create CTA). |
| GR-10 | Any data-bound region (table, detail page, chart, async section) | No indicator <300ms; skeleton 300ms–3s; skeleton + "still loading…" >3s. |
| GR-11 | §6 collections rendered as table/data-list/card grid | Always render pagination chrome (rows-per-page **5/10/20/50**, default **20**); disable controls for small datasets but keep them visible. |
| GR-12 | §6 collections rendered as a table | All columns sortable by default; single-column sort, asc on first click then desc; active sort persists for the session. |
| GR-13 | Create/edit forms for any §7 entity | ≤8 fields → single form; 9–20 → single form with section headers; >20 → multi-step wizard or settings-shell with tabs. |
| GR-14 | §6.4 feedback on user-initiated actions and system events | Toasts (4–8s, top-right) for transient confirmations; banners (persistent) for state requiring acknowledgement or affecting subsequent actions. |
| GR-15 | Badge counts on icons/tabs/nav items | Exact counts up to 99; `99+` above; hide badge when count is 0. |
| GR-16 | §7 enum/status fields rendered as badges/chips/pills | Map by intent — success→green, error→red, warning→amber, in-progress/info→blue, draft/archived→grey. Always pair colour with icon or text. |
| GR-17 | Icon-only controls (toolbars, table-row actions, compact toolbars) | Tooltip on hover/focus + matching `aria-label`; never icon-only for primary destructive actions. |
| GR-18 | §6 tables rendered on screens with <768px coverage per §6.6.5 | Collapse to vertical card list with primary identifier + 2–3 key columns + row-action overflow; do not horizontally scroll a desktop table. |
| GR-19 | §6.6.1 session policy when input is silent on idle/absolute timeout | Apply by §1 domain — financial/healthcare/regulated 15min/8h with T-1min warning + step-up auth; internal tools 30min/12h with T-1min warning; marketing/public 60min/24h, no warning. |
| GR-20 | Every template cell value across §1–§10 | No framework / library / vendor / product / version name. Speak in capability categories (e.g. "search index tier"). Drafter Grep blocklist; hard FAIL on first hit. |
| GR-21 | §6.4, §6.7, §6.8, §6.9 cells (with §5/§6.5/§8 exceptions) | No layout vocabulary (column/grid/sidebar/Card/Modal/...). Describe what must exist, not how it is arranged. Drafter Grep blocklist; hard FAIL on first hit. |
| GR-22 | `[AI-SUGGESTED]` marker count in the written draft | Cap at 50. Keep all blocking; non-blocking kept by `priority_score desc, AI-NNN asc` until cap; surplus demoted to value-only fills. Applied uniformly under both `target` values by `completeness-gap-pass.md`. |
