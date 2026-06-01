# Prototype Invariants

Behavioural invariants that hold for every prototype produced by this framework. Appended verbatim to the end of every merged `requirements/requirements.md` by the requirements-merger. Read by designers and prototype builders to understand what the requirements assume the prototype is and is not.

Add new invariants by appending; do not renumber.

## PI-01 — Server behaviour is simulated

All server-side behaviour — authentication, API calls, database operations, third-party integrations, scheduled jobs — is simulated by client-side stubs. Backend-shaped requirements describe the user-visible behaviour the simulation must reproduce, not real implementation. Endpoints, middleware, message queues, and infrastructure are out of scope.

## PI-02 — Data is fixture-backed

All data displayed in the prototype is sourced from in-memory fixtures shipped with the build. Mutations persist within a session but do not survive a reload unless an explicit "demo data" mode is specified. There is no real database, no migrations, and no data import / export pipelines.

## PI-03 — Validation is visual only

Form-field validation messages and inline error feedback are rendered as specified by the requirements, but no server-side enforcement is exercised. Constraints that are not visible in the UI — uniqueness checks, referential integrity, rate limiting, idempotency — are not run, even when the requirements name them.

## PI-04 — Third-party integrations are visual

Email, SMS, payment, mapping, file storage, and analytics integrations appear in the UI as visual confirmations or placeholder content. No external network calls are made. Where the requirements describe a third-party flow, the prototype reproduces the user-visible steps and the resulting UI state, not the network exchange.

## PI-05 — Role switcher

Every screen accessible to more than one role displays a role switcher in the prototype's surrounding chrome — outside the application UI under design — so reviewers can inspect each role's view without re-authenticating. The switcher is clearly labelled as a prototype tool, not an in-app control, and is placed in the same position on every screen. It lists every role defined in §3 of the requirements; roles to whom the active screen is not accessible per §6.5 RBAC are rendered in a disabled state. Switching the active role must immediately update the screen's visible components and actions to match the rules captured in the requirements (RBAC entries, conditional visibility, role-gated actions).

## PI-06 — Backend contracts are imaginary

Under the prototype target, the §6.10 fixture references *are* the backend; the §7 data shapes are the contract. There is no sibling backend specification, no live integration, and no contract-compatibility check. When §6.10 lists `Operation → Fixture reference`, the prototype reads and writes that fixture; mutations follow PI-02 (in-session persistence only). Application-target requirements specs replace these fixtures with pointers into a separate backend requirements document — those pointers are out of scope for the prototype build.

## PI-07 — Reporting is fixture-replayed

§6.7 reporting feature needs render from fixture aggregates only. No live computation, no aggregation pipeline, no scheduled materialisation, no export-side rendering. Filter dimensions and measure columns are honoured against the in-memory fixture; export formats produce the file from the same in-memory state. Reports listed with `Scheduling = daily / etc.` are visualised as scheduled in the UI (next-run timestamp, history entries) but do not execute on a clock.

## PI-08 — Prototype chrome is a review harness

The prototype's surrounding chrome — role switching (PI-05), data reset, prototype metadata (scope / purpose / posture), and navigation between generated prototypes — sits **outside** the application UI under design and is **not part of any requirement**. It is clearly marked as a prototype tool, carries no requirement bindings (no `data-src` / `data-prop`), and exists solely so reviewers can inspect and compare the generated designs. Nothing in the chrome should be read as a feature of the product being specified.
