# Prototype Scope Boundary

This document defines which topics are relevant for UI prototype generation and which should be filtered out during gap analysis. Agents use this boundary to focus discovery and design efforts on prototypable concerns.

## Prototypable (In Scope)

Topics that directly affect what the user sees and interacts with in a prototype:

- **Screens and page layouts** — page structure, content zones, responsive breakpoints
- **Navigation flows and routing** — menu structure, breadcrumbs, page transitions, deep linking
- **Form fields, inputs, and validation feedback** — field types, labels, placeholders, inline error messages, required indicators
- **Data display** — tables, charts, cards, lists, detail views, KPI widgets
- **Status indicators and visual states** — badges, progress bars, status chips, enabled/disabled states
- **Modals, dialogs, sheets, popovers** — overlay patterns, confirmation dialogs, action sheets
- **Loading and empty states** — skeleton screens, spinners, zero-data placeholders, error states
- **Responsive layout adaptations** — desktop (1280px+) and tablet (768px+) breakpoints
- **Design tokens** — colors, typography, spacing, borders, shadows
- **Icon usage and placement** — icon selection, sizing, contextual meaning
- **Validation rules** — prototypable as visual error feedback (inline messages, field highlighting), NOT as server-side validation logic
- **State transitions** — prototypable as visual state changes (e.g., status badge from "Pending" to "Approved"), NOT as backend state machines
- **Business logic** — prototypable ONLY when it affects what the user sees (conditional field visibility, calculated display values, dynamic form sections), NOT as server-side computation
- **Data relationships** — prototypable as navigation between related screens (e.g., click customer to see their policies), NOT as database foreign keys or join logic
- **Data model elements** — prototypable as entity names, typed fields displayed in UI (form inputs, table columns, detail views), enum/status values (dropdown options, status badges), and entity relationships (navigation paths). NOT as database table definitions, indexes, foreign key constraints, or storage-layer concerns
- **Permissions and roles** — prototypable as different screen states per role (admin sees extra controls), NOT as authorization middleware
- **Notifications** — prototypable as UI elements (toast messages, badge counts, notification panels), NOT as push notification infrastructure
- **Search and filtering** — prototypable as filter controls, search bars, and result displays, NOT as search engine indexing or query optimization
- **Projected volumes** — data volume, event frequency, concurrent users; drive UI pattern selection (pagination thresholds, virtualization, list-vs-card, layout density, chart type). NOT capacity planning, infrastructure sizing, or load testing

## Not Prototypable (Filter Out)

Topics that belong to backend, infrastructure, or implementation domains and cannot be represented in a UI prototype:

- **Backend internals** — endpoint logic, middleware, request handling, persistence design, queue infrastructure. The FE consumes the backend only as contracts (§6.10), specified in a sibling backend requirements document under the `application` target or replaced by fixtures under the `prototype` target.
- **Database schema and migration specifics** — table definitions, indexes, migration scripts (FE references §7 data shapes only, never storage shape).
- **Authentication/authorization implementation** — OAuth flows, token management, session storage internals. UI surfaces of auth (timeout warnings, re-auth modal trigger, sign-in screens) remain in scope as **behavioural** needs via §6.4 (UI feature needs) and §5 (task flows). The §6.6.1 Session-UX **policy table** (quantified idle/absolute timeouts, MFA scope) is `application`-target-only and is omitted under `prototype` (server/auth is simulated per PI-01/PI-03, so timeout durations are moot).
- **DevOps, CI/CD, infrastructure** — deployment pipelines, container orchestration, monitoring.
- **Performance optimization techniques** (backend-side) — caching strategies, query optimization, CDN configuration. FE perf budgets (§6.6.2: TTI, bundle size, render budget) are `application`-target-only and omitted under `prototype` — the prototype is a review harness (PI-08), not a perf-optimised build.
- **Data migration strategies** — ETL processes, data transformation scripts.
- **Security implementation details** — encryption, input sanitization, CORS policies.
- **Third-party service integration internals** — SDK configuration, webhook handlers, API keys.
- **Server-side business logic implementation** — calculation engines, rule processors, scheduling. UI surfaces of derived values (§7.X Derivations) remain in scope as business-language rules.

## Finding-scope classification

The two lists above answer *"should this topic be discovered / designed for the prototype?"*. A
second, derived question arises when a **review** (e.g. the ADVERSARIAL reviewers) raises a defect:
*"how relevant is this finding to a **frontend** deliverable?"*. This section defines the canonical
**finding-scope classes** that operationalise the in-scope / out-of-scope lists above into a
three-way rating lens. It is a **definition only** — the procedure that consumes it (classify each
finding, then cap the rating of out-of-scope findings) lives in
`framework/skills/recalibrate-scope-severity.md`.

Every review finding is exactly one of three classes:

- **`fe-relevant`** — the finding's subject **and** its corrective action live in the UI layer: any
  item in the **Prototypable (In Scope)** list above — screens, navigation, form fields, validation
  **feedback** (inline messages, field highlighting), data **display**, status indicators, modals,
  loading/empty/error **states**, role-gated **screen states**, and the **UI surface** of a backend
  event (a retry banner, a preserved draft, a "save failed" toast). A finding is `fe-relevant`
  **regardless of how backend the topic sounds**, as long as what would satisfy its recommendation is
  a change to the UI.

- **`fe-facing-contract`** — the finding is about a backend **contract the FE consumes** rather than a
  UI element directly: the §6.10 contract surface ("the FE consumes the backend only as contracts"),
  the **shape/enum/failure-mode** the UI must render against, and **POPIA / PII handling** (which is
  not pure backend — it surfaces as consent banners, on-screen redaction/masking, regional UI
  variants, and retention notices, per §6.6.4). The frontend genuinely depends on these being
  defined *somewhere*, so their severity is preserved; only their disposition is bounded (see the
  skill).

- **`backend-only`** — the finding's subject **and** its corrective action live entirely in the
  backend / infrastructure / server-side-implementation domain: any item in the **Not Prototypable
  (Filter Out)** list above — endpoint logic, persistence / DB schema, server-side computation,
  queues, DevOps / CI-CD, monitoring / alerting / backups / disaster-recovery, caching /
  query-optimisation, at-rest encryption / sanitisation / CORS, ETL / data-migration, and third-party
  SDK / webhook internals. A `backend-only` finding has **no UI surface** — nothing in the prototype
  or the frontend spec would change to resolve it. This is the class whose rating the recalibration
  procedure caps.

**The load-bearing disambiguation (key on the corrective action, not the topic):** classify by *what
would satisfy the finding's recommendation*. If the fix lands in the UI → `fe-relevant`. If the fix
is "define the contract / shape / compliance surface the UI renders against" → `fe-facing-contract`.
Only if the fix can *exclusively* be satisfied by backend/infra work → `backend-only`. When a finding
is **genuinely dual** — its happy-path UI surface is in scope but its mechanism is backend (e.g. a
network-failure finding: the retry **banner** is `fe-relevant` framing, the retry **mechanism** is
backend) — classify it as `fe-facing-contract`, **never** `backend-only`. The bias is always toward
*not* suppressing: when in doubt between `fe-facing-contract` and `backend-only`, choose
`fe-facing-contract`.
