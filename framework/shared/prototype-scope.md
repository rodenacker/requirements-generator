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
- **Authentication/authorization implementation** — OAuth flows, token management, session storage internals. UI surfaces of auth (timeout warnings, re-auth modal trigger, sign-in screens) remain in scope as **behavioural** needs via §6.4 (UI feature needs) and §5 (task flows). The §6.6.1 Session-UX **policy table** (quantified idle/absolute timeouts, MFA scope) is present in the requirements document as scope-noted **application-build guidance** — not a prototype design input (server/auth is simulated per PI-01/PI-03); its fields are therefore never `[OUT-OF-SCOPE]`-routed by the gap pass (they resolve via `GR-19` or gap-pass rule B7).
- **DevOps, CI/CD, infrastructure** — deployment pipelines, container orchestration, monitoring.
- **Performance optimization techniques** (backend-side) — caching strategies, query optimization, CDN configuration. FE perf budgets (§6.6.2: TTI, bundle size, render budget) are present in the requirements document as scope-noted **application-build guidance** — not a prototype design input (the prototype is a review harness per PI-08, never perf-optimised); their fields are never `[OUT-OF-SCOPE]`-routed by the gap pass (they resolve via gap-pass rule B7).
- **Data migration strategies** — ETL processes, data transformation scripts.
- **Security implementation details** — encryption, input sanitization, CORS policies.
- **Third-party service integration internals** — SDK configuration, webhook handlers, API keys.
- **Server-side business logic implementation** — calculation engines, rule processors, scheduling. UI surfaces of derived values (§7.X Derivations) remain in scope as business-language rules.

## Prototype-only content marking (`[PROTO-ONLY]`) — canonical definition

This section is the **canonical owner** of the `[PROTO-ONLY]` marker per `docs/maintenance.md > Canonical-source rule`. Every other file references it; no other file redefines it.

### Why the marker exists

`requirements/requirements.md` is written for a prototype target but must be re-projectable to an application audience by `/export-application`, whose whole value is being a *mechanical* transform. Without a marker, the export has to identify prototype-specific content **by reading prose** — the only consumer in this framework asked to classify content rather than match a token. That heuristic is measurably fragile: the drafter has produced six different wordings of the §6.10 scope-note across six runs. The marker replaces classification-by-reading with deletion-by-structure.

### Syntax — a paired span

```
[PROTO-ONLY] …prototype-specific text… [/PROTO-ONLY]
```

- **Deletion is one regex:** `\[PROTO-ONLY\][\s\S]*?\[/PROTO-ONLY\]` (non-greedy). No sentence splitting is ever required — sentence-boundary detection over markdown containing inline code and abbreviations is exactly the heuristic this marker exists to remove.
- **A span may contain a `[SRC: C-NNN]` tag.** The paired form makes nesting unambiguous; a prototype-realization note can be input-grounded like any other content.
- **A span must not cross a markdown block boundary.** It may not run from one table row into the next, nor from a blockquote into body prose, nor across a list-item boundary. One span, one block. This is what makes deletion structurally safe.
- **Balance is checkable:** in the draft and the merged document, opener count equals closer count. In the export, both are zero.
- **Never write a bracketed delimiter inside prose that lands in `requirements.md`.** Documentation of the marker is indistinguishable from a use of it: two bracketed delimiters in order form a real span (deleted at export, inflating the span count), and a lone one unbalances the drafter's open-equals-close check. Where the marker must be *described* in the template or the document — the authoring-guardrails legend and §0.1 both do — write the bare word in code ticks (`` `PROTO-ONLY` ``, `` `/PROTO-ONLY` ``) and say "square-bracketed" in prose. Files outside the document — this one, agent files, `docs/` — are exempt and use the real brackets freely.

### It is a *scope* marker, not a provenance marker

The four provenance markers (`[AI-SUGGESTED]`, `[STANDARD-RULE]`, `[OUT-OF-SCOPE]`, `[POSTURE-DEFAULT]` — closed set, see `CLAUDE.md > Markers in content`) all answer **"where did this value come from?"**. `[PROTO-ONLY]` answers **"which build target does this apply to?"** — a different axis.

Two consequences follow, and both are load-bearing:

1. **The mutual-exclusion rule does not apply.** `framework/agents/requirements-drafter.md > Citation scope` forbids a field from carrying both a provenance marker and a `[SRC:]` tag, because both sit on the provenance axis and a field has exactly one provenance. `[PROTO-ONLY]` sits on the scope axis, so it may co-occur freely with `[SRC:]` **and** with any one provenance marker.
2. **The provenance set stays closed at four.** Adding `[PROTO-ONLY]` does not widen it. `framework/assets/glossary.md` lists it as a *scope marker*, separately.

### What gets marked

Prototype-specific content is anything that is **true of the prototype and false (or meaningless) for the application build**:

- The prototype-scoped portion of a pinned scope-note blockquote (§1.7, §6.6.1, §6.6.2, §6.10, §7) — the sentence explaining that the section is not a prototype design input, or that fixtures stand in for the backend.
- A `PI-NN` reference in body prose.
- A realization note inside a cell describing how the prototype fakes a behaviour (fixture-backed, session-scoped, simulated, client-stub, visual-only).

**What is *not* marked:** the `## Prototype invariants` appendix (already deletable by heading→EOF, a contract `/resolve-review` depends on), the §6.10 fixture-reference column and §7 `**Source:**` lines (both owned by dedicated export transforms), and the §0.1 section (replaced wholesale at export).

**The marker never wraps a normative requirement.** A `[PROTO-ONLY]` span inside a §6.1/§6.2/§6.3 statement would mean "this requirement only applies to the prototype", which is not a thing a requirement can be — the realization *note* is markable, the requirement itself is not. See **Normative-section prototype-vocabulary ban** below.

### Lifecycle

| Stage | Behaviour |
|---|---|
| `requirements-drafter` | **Emits** spans at populate time (Workflow step 3), alongside `[SRC:]`. Not a gap-pass concern — prototype scope is a property of content already present, not a gap. |
| `requirements-resolver` | **Ignores.** Not enumerated into the manifest; no Q&A. |
| `requirements-merger` | **Retains verbatim**, exactly as it retains `[SRC:]`. Resolution markers are stripped because their job ends at merge; reference and scope markers survive because downstream consumers need them. |
| `/export-application` | **Deletes** every span, then drops any blockquote left empty. |
| `/wireframe`, `/prototype` | May read spans as prototype-realization guidance. Neither is required to. |

### Unmarked documents

Documents produced before this marker existed carry no spans. They are **out of scope** — there is no fallback branch, no migration, and no gate. An unmarked document simply yields zero span deletions, and the export's residue sweep (which is retained precisely for this) reports the surviving prototype framing at the gate. Absence of the marker is indistinguishable from absence of prototype framing, so **the residue sweep is the only check that can catch a drafter that under-marks** — it must never be removed on the grounds that the marker made it redundant.

## Normative-section prototype-vocabulary ban — canonical definition

This section is the **canonical owner** of the normative-section set and the realization-vocabulary detector. Consumers: `framework/skills/completeness-gap-pass.md` rule **B8** (raises a consultant question at draft time) and `framework/agents/export-application-exporter.md` step 1.5 (halts the export as a backstop). Neither restates it.

### The defect this prevents

A real run produced `§6.2 BR-08 — "When a list is requested, then the system shall serve session-scoped fixture data"`, enforcement point **`data`**, carrying `[SRC: C-018]`. Two other rows in the same document said comparable things: a §1.6 environment assumption and a §6.6.4 compliance bullet. None carried a `PI-NN` token.

That row is not a formatting problem. `enforcement point = data` is the column a backend generator consumes, so the exported document instructs a downstream system to build a production application with **no persistence**. The citation freezes the bytes, so `/export-application` cannot repair it — it can only disclose it, and a provenance row hundreds of lines away does not stop anyone. The only place this is fixable is where it is written.

### Normative sections (closed set)

A cell, row, or bullet in any of these is **normative** — it states what the application must do, and a downstream generator may act on it:

| Section | Normative unit |
|---|---|
| §1.6 Assumptions & dependencies | `Statement` cell |
| §6.1 Functional | `Statement` and `Acceptance criteria` cells |
| §6.2 Business rules | `Statement`, `Acceptance criteria`, `Enforcement point` cells |
| §6.3 Validation rules | `Rule` and `Error message` cells |
| §6.4 UI feature needs (incl. §6.4.5) | `Feature need` / `Expected UI behaviour` / `Recovery action` cells |
| §6.6.4 Compliance UI behaviour | each bullet |
| §7 Data shapes (incl. §7.X) | `Notes` cells and derivation `Rule` cells |
| §6.10 Consumed backend contracts | `Notes` cell only (the fixture column is transform-owned) |

Everything else — narrative prose, scope-note blockquotes, §1.7, §6.6.1, §6.6.2, §8, the PI appendix — is **outside** this set. Prototype framing there is ordinary markable content.

### Realization vocabulary (the detector)

A normative unit trips the detector when it contains any of:

```
PI-\d{2} | fixture | (?i)session-scoped | does not persist | client-stub
simulat | review harness | visual[- ]only | no backend endpoint | in-memory only
```

**The detector raises a question. It never rewrites, and it never auto-marks.** This distinction is the whole design: a heuristic that asks a human costs one question when it is wrong; a heuristic that silently edits content is the failure mode that corrupted a citation-bound cell in a real run. The detector is deliberately broad for the same reason — a false positive is cheap.

### Disposition

1. **At draft time** — gap-pass rule `B8` emits `[AI-SUGGESTED: AI-NNN | blocking]` on the offending unit with a `draft_context` asking the consultant to choose. This reuses the existing Q&A channel; no new resolver or merger machinery exists for it.
   - **Confirmed** — the behaviour is genuinely part of the domain (some real systems *are* session-scoped, and "fixture" is legitimate vocabulary in test-data domains). The value stays, unmarked, and never trips again.
   - **Corrected** — the consultant supplies application-correct wording. If the prototype realization is worth recording, they include it inside a scope span, which moves it out of the normative unit.
2. **At export time** — `export-application-exporter.md` step 1.5 re-runs the detector over the normative set. A surviving hit **halts before any write**. This is the one place the exporter's disclose-don't-block policy is deliberately reversed: disclosure is the right answer for prose, and the wrong answer for a rule a code generator will act on.

**A `[PROTO-ONLY]` span does not launder a normative unit.** Wrapping a requirement statement in a span would assert "this requirement applies only to the prototype", which is not a thing a requirement can be. Mark the realization *note*; never the requirement.

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
