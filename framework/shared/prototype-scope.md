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
- **Authentication/authorization implementation** — OAuth flows, token management, session storage internals. UI surfaces of auth (timeout warnings, re-auth modal trigger, sign-in screens) remain in scope via §6.6.1.
- **DevOps, CI/CD, infrastructure** — deployment pipelines, container orchestration, monitoring.
- **Performance optimization techniques** (backend-side) — caching strategies, query optimization, CDN configuration. FE perf budgets (TTI, bundle size, render budget) remain in scope via §6.6.2.
- **Data migration strategies** — ETL processes, data transformation scripts.
- **Security implementation details** — encryption, input sanitization, CORS policies.
- **Third-party service integration internals** — SDK configuration, webhook handlers, API keys.
- **Server-side business logic implementation** — calculation engines, rule processors, scheduling. UI surfaces of derived values (§7.X Derivations) remain in scope as business-language rules.
