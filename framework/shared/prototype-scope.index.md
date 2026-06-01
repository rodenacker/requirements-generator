# Prototype Scope — index

Slim index of `framework/shared/prototype-scope.md`. Loaded by the requirements-resolver in place of the full body so the scope predicate does not sit in context for the entire run. When the follow-up filter (`framework/skills/flag-gaps-ambiguities.md` step 3) needs the full bullet wording — e.g. to phrase a `follow_ups[*].scope_reason` precisely — Read the matching bullet from `framework/shared/prototype-scope.md` on demand.

The "Not Prototypable (Filter Out)" list below is the strict predicate for `defer-out-of-scope` decisions. The "Prototypable (In Scope)" list is informational for orientation; falling through to step 4 (`ask`) is the default for any territory not unambiguously matched here.

## Not Prototypable (Filter Out) — defer-out-of-scope categories

- Backend internals (FE consumes contracts via §6.10 only)
- Database schema and migration specifics
- Authentication/authorization implementation (UI auth surfaces remain in scope behaviourally via §6.4 / §5; the §6.6.1 session-policy table is application-target-only, omitted under prototype)
- DevOps, CI/CD, infrastructure
- Performance optimization techniques (backend-side; §6.6.2 FE perf budgets are application-target-only, omitted under prototype — review harness, PI-08)
- Data migration strategies
- Security implementation details
- Third-party service integration internals
- Server-side business logic implementation (UI surfaces of derivations remain in scope via §7.X)

## Prototypable (In Scope) — orientation only

- Screens and page layouts
- Navigation flows and routing
- Form fields, inputs, and validation feedback
- Data display (tables, charts, cards, lists, detail views, KPI widgets)
- Status indicators and visual states
- Modals, dialogs, sheets, popovers
- Loading and empty states
- Responsive layout adaptations (1280px+, 768px+)
- Design tokens
- Icon usage and placement
- Validation rules — as visual feedback only
- State transitions — as visual state changes only
- Business logic — only when it affects what the user sees
- Data relationships — as navigation between related screens
- Data model elements — as entity names, typed fields displayed in UI, enums, relationships
- Permissions and roles — as different screen states per role
- Notifications — as UI elements only
- Search and filtering — as controls and result displays
- Projected volumes — as drivers of UI pattern selection
