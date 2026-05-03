# General Rules for Requirements

Catalogue of standard answers for common gaps in a requirements draft. Consulted by the requirements-drafter **before** producing an `[AI-SUGGESTED]` marker: if a rule below covers the gap, the drafter applies the rule's canonical answer and tags the field `[STANDARD-RULE: GR-NN]`. The resolver skips this marker — these rules are deterministic and require no consultant Q&A.

Each rule has a stable ID `GR-NN`, a scope predicate (template field/element it applies to), and the canonical answer. Add new rules by appending; never renumber.

**Precedence:** Rules stated in input documents (briefs, source UI references, consultant answers) override general rules. The drafter applies a general rule only when the inputs are silent on the field it covers, or when the rule narrows an input that is itself silent on the specific sub-decision.

## GR-01 — Excluded actions on a Viewer role

**Applies to:** §6.5 RBAC matrix cells where the persona's expertise / role description identifies them as a read-only viewer (e.g. "Viewer", "Read-only user", "Auditor with no write access").

**Rule:** All actions excluded from a Viewer's RoleAssignment must be **hidden** in the UI, not rendered as disabled controls.

**Rationale:** disabled controls invite hover and click attempts, leak feature existence, and clutter the viewer's screen with affordances they cannot use. Hiding is the prototype default.

## GR-02 — Permission-denied affordances on direct links

**Applies to:** §6.5 RBAC cells where an action is denied for a persona but the screen is reachable via shared URL, deep link, or notification.

**Rule:** Hide the denied action in navigation, menus, and toolbars. On direct screen access, render an in-page permission-denied banner naming the missing permission and pointing to a contact or request-access path; do not show a generic 403 error page.

**Rationale:** users following a shared link need orientation, not a dead end. Engineers default to 403 unless directed otherwise.

## GR-03 — Archived and read-only entity action suppression

**Applies to:** §7 entities whose lifecycle (§2.3) includes an `Archived`, `Closed`, `Cancelled`, or other read-only terminal state.

**Rule:** On detail screens for entities in a read-only state, hide all mutating actions and show a top-of-page banner naming the state and the action (if any) that restores editability.

**Rationale:** disabled action buttons on archived records are the most common cause of "is the system broken?" support tickets. Hiding plus a banner conveys both why and what to do next.

## GR-04 — Confirmation gate for irreversible actions

**Applies to:** §6.5 cells with `A` (approve), or actions whose name includes Delete, Remove, Send, Publish, Submit-for-approval, Charge, Cancel-order, or Issue, where the action is not reversible by undo.

**Rule:** Gate with a modal-confirmation that names the affected entity (e.g. "Delete invoice INV-2034?") and uses a destructive-styled primary action. Do not pre-focus the destructive button; default focus to Cancel.

**Rationale:** generic "Are you sure?" copy and pre-focused destructive buttons are well-documented prototype anti-patterns.

## GR-05 — Validation timing

**Applies to:** §6.4 user-facing validation feedback on §7 entity fields.

**Rule:** Validate on blur for synchronous rules (format, required, length); validate on submit for cross-field and asynchronous rules (uniqueness, server-side checks); never validate on keystroke.

**Rationale:** keystroke validation is jarring and the most common form anti-pattern in early prototypes.

## GR-06 — Required-field marking

**Applies to:** §6.4 forms where some fields are required and some optional.

**Rule:** Mark required fields with a leading asterisk and a single legend line above the form. If ≥ 80 % of fields are required, mark optional fields with "(optional)" instead and drop the asterisks.

**Rationale:** marking the minority is the WCAG-aligned default; without a rule, drafters oscillate between conventions.

## GR-07 — Autofocus on form open

**Applies to:** create and edit forms in modals, drawers, and full-page form layouts.

**Rule:** Autofocus the first editable field on open. Exception: forms preceded by a destructive or navigational confirmation step, where the primary cancel/back must hold focus.

**Rationale:** keyboard users expect immediate input; mouse users are unaffected by autofocus.

## GR-08 — Empty-state copy specificity

**Applies to:** any list, table, dashboard widget, or detail panel bound to a §7 entity collection.

**Rule:** Empty-state copy must name the entity ("No clients yet") and offer the primary creation CTA. Generic "No data" or "Nothing here" is not acceptable.

**Rationale:** empty states are the user's first impression of a screen; specificity costs nothing and resolves the "what now?" question.

## GR-09 — No-results vs empty distinction

**Applies to:** any collection with search or filter controls.

**Rule:** Distinguish two empty variants. (a) Zero data: show the entity-specific empty-state with a creation CTA. (b) Zero results from a filter or search: display the active filter chips, a Clear-all action, and copy referencing the search/filter; do not show the create CTA.

**Rationale:** drafters routinely conflate the two and produce empty states that hide the user's own filter as the cause of the emptiness.

## GR-10 — Loading indicator threshold

**Applies to:** any data-bound region (table, detail page, chart, async section).

**Rule:** Show no indicator for operations expected under 300 ms. Show a skeleton matching the target layout for 300 ms – 3 s. Show a skeleton plus a "still loading…" message for operations exceeding 3 s.

**Rationale:** spinners under 300 ms cause flicker; skeletons over 3 s without context cause abandonment.

## GR-11 — Pagination and rows-per-page

**Applies to:** any §6 collection rendered as a table, data-list, or card grid.

**Rule:** Always render the pagination control, including the rows-per-page selector. For datasets smaller than the current page size, render the page-navigation controls in a disabled state but keep them visible. The rows-per-page selector must offer **5, 10, 20, 50** with **20** as the default.

**Rationale:** consistent pagination chrome avoids layout shifts as datasets grow and trains users where to find page controls. The 5/10/20/50 ladder covers density preferences without overwhelming choice.

## GR-12 — Sortable table columns

**Applies to:** any §6 collection rendered as a table.

**Rule:** All columns must be sortable by default. Sorting is single-column, ascending on first click and descending on second; the active sort column is indicated in the header and persists for the session.

**Rationale:** unsorted-only columns are a recurring annoyance for power users and the sortability decision is rarely worth a per-column question.

## GR-13 — Form-length escalation

**Applies to:** create and edit forms for any §7 entity.

**Rule:** Apply by field count. ≤ 8 fields — single-form pattern. 9 – 20 fields — single-form with section headers. > 20 fields — escalate to a multi-step wizard or a settings-shell with tabs.

**Rationale:** field count is a deterministic pattern-selection signal; codifying it avoids ad-hoc choices per entity.

## GR-14 — Toast vs banner placement

**Applies to:** §6.4 feedback on user-initiated actions and system events.

**Rule:** Use toasts (auto-dismiss 4 – 8 s, top-right) for transient confirmations of completed actions. Use banners (persistent, top of page or section) for state the user must acknowledge or that affects subsequent actions — offline, archived, permission-denied, validation summaries.

**Rationale:** the toast/banner choice is rarely stated in inputs but always matters for read-flow and accessibility.

## GR-15 — Notification badge cap

**Applies to:** badge counts on icons, tabs, and navigation items.

**Rule:** Display exact counts up to 99; show `99+` for higher counts; hide the badge entirely for counts of 0.

**Rationale:** every prototype reproduces this convention; codifying it removes a recurring `[AI-SUGGESTED]` cycle.

## GR-16 — Status colour mapping

**Applies to:** §7 enum and status fields rendered as badges, chips, or status pills.

**Rule:** Map by intent — success/active → green; error/failed/blocked → red; warning/pending → amber; in-progress/info → blue; draft/archived/neutral → grey. Always pair colour with an icon or text label; never rely on colour alone.

**Rationale:** WCAG-required redundancy plus a standardised mapping; reduces a recurring decision per enum.

## GR-17 — Icon-only control labelling

**Applies to:** any control rendered as icon-only (toolbar buttons, table-row actions, compact toolbars).

**Rule:** Provide a tooltip on hover and focus, plus an `aria-label` matching the tooltip text. Never use icon-only for primary destructive actions.

**Rationale:** icon-only destructive controls are the highest-cost accessibility regression in prototypes.

## GR-18 — Table-to-card collapse on mobile

**Applies to:** any §6 table rendered on screens with mobile-breakpoint coverage (< 768 px) per §6.6.5.

**Rule:** Below 768 px, collapse tables into a vertical card list showing the primary identifier, 2 – 3 key columns, and a row-action overflow. Do not horizontally scroll a desktop table.

**Rationale:** horizontal-scroll tables on mobile are the most common responsive failure mode in prototypes.

## GR-19 — Session timeout defaults by domain

**Applies to:** §6.6.1 session policy when the input does not specify an idle or absolute timeout.

**Rule:** Apply by §1 domain. Financial / healthcare / regulated → idle 15 min, absolute 8 h, warning at T-1 min, step-up auth required for approve-class actions. Internal tools → idle 30 min, absolute 12 h, warning at T-1 min. Marketing / public-facing → idle 60 min, absolute 24 h, no warning.

**Rationale:** §6.6.1 is otherwise the most-flagged `[AI-SUGGESTED: blocking]` row across requirements drafts; codified domain defaults remove the cycle.
