<!-- ROLE: asset. Section order matches `framework/assets/topics-requirements.md` one-to-one. Audience is LLM-only (no human stakeholder consumption). -->

# Requirements: {{application_name}}

**Domain:** {{domain}} <!-- inferred from inputs; flag [AI-SUGGESTED] if not stated explicitly --> **Target:** prototype | application <!-- from `requirements/source-manifest.json > target`; controls §6.10 sub-block, PI-append, and the emit-conditional sections listed in §0.1 --> **Created:** {{date}} **Status:** draft | final **Last finalised at:** {{last_finalised_at}}

> **Authoring guardrails.** Cells across §1–§10 must obey:
> - **`GR-20` No stack specifics.** No framework, library, vendor, product, version, or brand name in any cell. Speak in capability categories ("client-side state management", "binary blob storage tier"). Stack picks happen at code-generation time, not here.
> - **`GR-21` No UI layout.** §6.4 / §6.7 / §6.8 / §6.9 cells describe *what UI elements/behaviours must exist*, never *how they are arranged or styled*. Layout, component choice, and visual design are produced by a later UX design step. Exceptions: §5 may name screen-level navigation; §6.5 may describe role-conditional visibility; §8 may quote consultant-supplied layout observations as input citations.
>
> Inferred content is marked inline with one of three markers per the drafter's decision tree (`framework/agents/requirements-drafter.md > Classification`):
> - `[AI-SUGGESTED: AI-NNN | blocking|non-blocking]` — inferred completeness-gating, in-scope value; resolver asks the consultant.
> - `[STANDARD-RULE: GR-NN]` — deterministic answer from `framework/shared/general-rules.md`; resolver skips.
> - `[OUT-OF-SCOPE: domain-default]` — required by template but outside prototype scope per `framework/shared/prototype-scope.md`; emitted under `target = prototype` only; resolver skips, consultant can scan-review.
>
> Citation: input-grounded cells carry a trailing `[SRC: C-NNN]` tag in the draft, backed by `requirements/draft-claims.ndjson`. The merger **retains** `[SRC:]` tags in the final doc (LLM-only audience) and strips all other markers.
>
> Field-level marking when only some sub-fields are inferred; heading-level marking when the whole item is invented. Fill every field — no blanks.

---

## 0.1 Target-mode applicability

<!-- format: table[4-col: section, prototype, application, mode-conditional?]; one row per mode-conditional section -->

> The `target` field on the source manifest is `prototype` or `application`. The drafter picks the matching variant for the rows below at fill-time; the merger does not see both. Rows marked *emit-conditional on target* are **omitted entirely** under `prototype` (the section heading does not appear) and emitted under `application` — these are the FE-irrelevant sections that the convergent/backend consumers (and a future BFF-API-doc / DB-script generator) need, but that add noise to a client-side prototype. Rows marked *content-conditional* are omitted when they have no content under either target.

| Section | `prototype` | `application` | Mode-conditional? |
| --- | --- | --- | --- |
| §1.6 Assumptions & dependencies | omitted when no assumption/dependency applies | emitted | yes — content-conditional |
| §1.7 Architectural implications | **omitted** | emitted (drafter-derived) | yes — emit-conditional on target |
| §6.1 `Rationale` column | column omitted | column emitted (optional) | yes — column-conditional on target |
| §6.6.1 Session UX | **omitted** | emitted | yes — emit-conditional on target |
| §6.6.2 FE performance budgets | **omitted** | emitted (optional) | yes — emit-conditional on target |
| §6.10 Consumed backend contracts | fixture references | pointers into the sibling backend requirements document | yes — sub-block content differs |
| §7 Data shapes consumed by FE | shape sourced from fixtures | shape sourced from backend contracts | provenance label only |
| §8 Source UI references | omitted when no consultant-supplied reference exists | same | yes — content-conditional |
| §9 Key terminology | omitted unless ≥1 inconsistency flag or alternate-term usage exists (full domain glossary lives in the GLOSSARY analysis, not here) | same | yes — content-conditional |
| `## Prototype invariants` appendix | appended (PI-01..PI-08) | omitted | yes — merger conditional |
| (all other sections) | identical | identical | no |

---

## 1. Application context

<!-- format: narrative[4-field: name, purpose, domain, business_goal]; one short paragraph or phrase per field; no bullets -->

**Name:** {{application_name}}

**Purpose / business value:** {{purpose}}

**Domain:** {{domain}}

**Business goal:** {{business_goal}}

<!-- rev: run-N YYYY-MM-DD -->

---

## 1.5 Scope

<!-- format: table[3-row: In, Out, Deferred; comma-separated capability list per cell]; capability categories only (GR-20) -->
<!-- guidance: ≥1 entry in In bucket (A10); Out/Deferred may be empty -->

> §1.5 is in-scope-only — unsupplied buckets emit `[AI-SUGGESTED]` under both targets. `[OUT-OF-SCOPE: domain-default]` is **not** valid in this section (the section *defines* scope; OOS would be self-referential).

| Bucket | Items |
| --- | --- |
| In | {{in_scope_capabilities}} <!-- capability categories this FE must deliver --> |
| Out | {{out_of_scope_capabilities}} <!-- explicitly excluded; capability-level only; no product/vendor names per GR-20 --> |
| Deferred | {{deferred_capabilities}} <!-- known future scope; not in this build --> |

<!-- rev: run-N YYYY-MM-DD -->

---

## 1.6 Assumptions & dependencies

<!-- format: table[3-col: kind, statement, source]; one row per assumption; kind ∈ {abstract-service-dependency, persona-prerequisite, environment-assumption} -->
<!-- emit: content-conditional — omit the whole section when no assumption / dependency is stated or domain-implied; not read by any design pipeline, so do not fabricate filler rows -->

> Abstract services, persona prerequisites, environment assumptions. Cells naming a product or vendor fail `GR-20`. Omitted entirely when nothing applies (§0.1 content-conditional).

| Kind | Statement | Source |
| --- | --- | --- |
| Abstract service dependency | {{capability_category}} <!-- e.g. "an identity provider", "a binary blob storage tier" --> | stated / inferred |
| Persona prerequisite | {{prerequisite}} <!-- e.g. "users have an existing account in the identity provider" --> | stated / inferred |
| Environment assumption | {{assumption}} <!-- e.g. "users on modern evergreen browser", "stable broadband connection" --> | stated / inferred |

<!-- repeat per row; one row per assumption / dependency -->

<!-- rev: run-N YYYY-MM-DD -->

---

## 1.7 Architectural implications

<!-- format: table[3-col: capability_category, driving_requirements, recommendation]; capability_category from drafter's inline catalogue (≤15 entries); recommendation optional -->
<!-- emit: emit-conditional on target — OMITTED entirely under `target = prototype` (no design pipeline reads it); emitted under `target = application` (backend capability plan, consumed by application-build + a future BFF/DB generator) -->

> **Emitted under `target = application` only** (§0.1). Capability categories derived by the drafter from §6 functional requirements + §10 volumes + §6.7 reporting needs, against an inline catalogue of ≤15 categories (see `framework/agents/requirements-drafter.md > derive-architectural-implications`). Drafter seeds every row as `[AI-SUGGESTED: AI-NNN | non-blocking]`; resolver Q&A refines. Recommendation column is **optional** and **non-deterministic** — a stack choice belongs in the code-generation step, not here.

| Capability category | Driving requirement(s) | Recommendation (optional) |
| --- | --- | --- |
| {{capability}} <!-- e.g. "Client-side full-text search at ≤10⁴ records" --> | → §6.1 F-{{nn}} / §10 row / §6.7 RPT-{{nn}} | {{soft_recommendation}} <!-- e.g. "in-memory index acceptable given volume"; blank when no deterministic guidance --> |

<!-- repeat per active category -->

<!-- rev: run-N YYYY-MM-DD -->

---

## 2. Domain model

> The BA's framing of the business domain in **ubiquitous language**, implementation-free.

### 2.1 Concepts

<!-- format: table[3-col: concept, persistence∈{persistent,derived,policy}, definition]; one ubiquitous-language sentence per definition -->

| Concept          | Persistence                   | Definition (ubiquitous language)     |
| ---------------- | ----------------------------- | ------------------------------------ |
| {{concept_name}} | persistent / derived / policy | {{one-sentence business definition}} |

<!-- include non-persistent concepts (e.g. Eligibility, Risk Tier, Underwriting Decision) alongside persistent ones; persistent concepts must also appear in §7. Derived concepts must also appear in §7.X. -->

### 2.2 Relationships

<!-- format: bullets; pattern "{ConceptA} **{verb-phrase}** {ConceptB} [{cardinality}]"; verbs business-sourced not data-sourced -->

- {{Concept A}} **{{verb-phrase}}** {{Concept B}} [{{cardinality}}]

<!-- verbs come from the business ("Borrower **submits** Application"), not from data ("Borrower hasMany Application"); cardinality optional but recommended -->

### 2.3 Aggregates & lifecycles

<!-- format: per-aggregate table[3-row: member_concepts, lifecycle_states, key_invariants]; lifecycle_states is an ordered arrow chain -->

#### {{aggregate_root}}

| Field            | Value                                                                                                                              |
| ---------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| Member concepts  | {{member_concept_list}}                                                                                                            |
| Lifecycle states | {{ordered_state_list}} <!-- e.g. Application → Approved → Disbursed → Servicing → Closed; transitions defined in §2.5 when >2 states --> |
| Key invariants   | {{business_invariants}} <!-- e.g. "Loan cannot be Disbursed until KYC is Verified" -->                                             |

<!-- repeat per aggregate -->

### 2.4 Diagram (optional)

<!-- format: mermaid[classDiagram|erDiagram]; classDiagram for concept-centric, erDiagram for storage-shape; every §2.1 concept appears ≥1× -->

```mermaid
classDiagram
    %% Mermaid classDiagram or erDiagram in domain mode; markdown-native, diff-able, tool-agnostic.
    %% Absence of this block is a vague-finding (gap category 2), not a blocker.
```

### 2.5 State-transition matrix

<!-- format: per-aggregate table[4-col: from→to, trigger, precondition, visible_effect]; prototype: server-side-only rows carry [OUT-OF-SCOPE]; application: same rows unmarked -->

> Emitted only when ≥1 §2.3 aggregate has more than two lifecycle states. One sub-block per qualifying aggregate. Pre-condition cells may reference `→ §6.2 BR-NN`.

#### {{aggregate_root}}

| From → To                       | Trigger                       | Pre-condition                                  | Visible effect                                                          |
| ------------------------------- | ----------------------------- | ---------------------------------------------- | ----------------------------------------------------------------------- |
| {{from_state}} → {{to_state}}   | {{triggering_event}}          | {{precondition_or_BR_ref}}                     | {{ui_observable_change}} <!-- badge change, screen route, action gain --> |

<!-- repeat per transition; rows whose Visible effect is purely server-side become [OUT-OF-SCOPE] under prototype / no marker under application (Tier D3) -->

<!-- rev: run-N YYYY-MM-DD -->

---

## 3. Target users

<!-- format: per-persona table[6-row: role, expertise, stakes, frequency, positive_drivers, negative_drivers]; ≥1 story in §4.2 required per persona (A1) -->

> Target-user personas — the end users of the application being designed. Not to be confused with the Unicorn (LLM) or the Consultant (audience).

### {{persona_name}}

| Field                  | Value                |
| ---------------------- | -------------------- |
| Role / job title       | {{role}}             |
| Expertise level        | {{expertise}}        |
| Stakes                 | {{stakes}}           |
| Frequency of use       | {{frequency}}        |
| Driving forces — wants | {{positive_drivers}} |
| Driving forces — fears | {{negative_drivers}} |

<!-- repeat per persona; every persona MUST have ≥1 user story in §4 and may be referenced as actor in §5 Task flows -->

<!-- rev: run-N YYYY-MM-DD -->

---

## 4. User goals & stories

> Quality signals live on the goal (outcome-level), not the story (behaviour-level).

### 4.1 Goals catalogue

<!-- format: table[6-col: ID(G-NN), goal_statement, quality_signals, goal_kind∈{top,sub,interaction}, layout_pref?, ux_pattern_pref?]; outcome-level only -->
<!-- quality_signals on top-level goals SHOULD be measurable outcome signals where the inputs support one (e.g. "task completion < 5 min", "≤ 1 support contact per onboarding") — this is the lightweight stand-in for a success-metrics section when no PRD is run; deeper success metrics + baselines/targets stay in the PRD (§5.2). Do not add a separate column. -->

| ID | Goal statement | Quality signals | Goal kind | Layout pref (optional) | UX-pattern pref (optional) |
| --- | --- | --- | --- | --- | --- |
| G-{{nn}} | {{goal_statement}} | {{quality_signals}} <!-- resolve via taxonomy-goals.md; prefer a measurable outcome signal on top-level goals --> | top-level / sub-level / interaction-level | {{layout_preference}} | {{ux_pattern_preference}} |

<!-- repeat per goal; IDs are stable and referenced from §4.2 stories and §5 task flows -->

### 4.2 Stories by persona

<!-- format: per-persona heading then per-story heading "Story: As a {role}, I want {intent}, so that {benefit}", followed by table[6-row: goal_ref, priority, objective, context, linked_flow?, acceptance_criteria]; AC behavioural — given-when-then OR observable-signal bullet (NOT EARS — see GR-23) -->
<!-- guidance: every persona ≥1 story (A1); every story exactly 1 §4.1 goal-id (A2); priority per GR-24 (B6) -->

#### {{persona_name}} <!-- → §3 -->

##### Story: As a {{role}}, I want {{intent}}, so that {{benefit}}

| Field                                    | Value                                                                                      |
| ---------------------------------------- | ------------------------------------------------------------------------------------------ |
| Goal                                     | → §4.1 G-{{nn}}                                                                            |
| Priority                                 | Must / Should / Could / Won't <!-- MoSCoW; default per GR-24 carries [STANDARD-RULE: GR-24]; input-stated carries [SRC] --> |
| Objective                                | {{objective}} <!-- behavioural objective for this story; the outcome lives on the goal --> |
| Context (frequency / expertise / stakes) | {{context}}                                                                                |
| Linked task flow (optional)              | {{flow_ref}} <!-- → §5 -->                                                                 |
| Acceptance criteria                      | {{given_when_then_or_observable_signals}} <!-- ≥1 bullet; behavioural observable-signal / Given-When-Then, not visual; NOT EARS (GR-23 reserves EARS for §6.1/§6.2); see Tier B5 in gap-pass --> |

<!-- repeat per story under each persona; persona heading once per persona, story sub-heading per story. A single goal in §4.1 may be referenced by stories under multiple personas (M:N is expected). -->

---

## 5. Task flows

<!-- format: per-flow table[6-row: actor, trigger, steps, decision_points, exception_paths, role_conditional]; steps as ordered "(action; observable_result)" pairs; exception_paths structured "{trigger → message → recovery_action}" -->
<!-- guidance: every flow's actor names an existing §3 persona (A8); every step carries an observable signal (B5) -->

### Flow: {{flow_name}}

| Field                      | Value                                                        |
| -------------------------- | ------------------------------------------------------------ |
| Actor                      | {{actor_persona_ref}}                                        |
| Trigger                    | {{trigger}}                                                  |
| Steps                      | {{ordered_steps}} <!-- each step: "(action; observable result)" — Tier B5 acceptance signal per step --> |
| Decision points            | {{decision_points}}                                          |
| Exception paths            | {{exception_paths}} <!-- structured: "{trigger → message → recovery action}" --> |
| Role-conditional behaviour | {{role_gating}} <!-- e.g. "only team leads can reassign" --> |

<!-- repeat per flow -->

---

## 6. Requirements

### 6.1 Functional

<!-- format: table[cols: ID(F-NN), priority, statement, acceptance_criteria, source, rationale?]; statement is atomic — single capability per row, no compound "and"; AC in EARS form (GR-23) -->
<!-- guidance: atomic decomposition aids gap-pass mapping to §6.10 ops (A14) and BR refs; priority per GR-24 (B6); AC in EARS keywords per GR-23 -->
<!-- Rationale column: emit-conditional on target — present under `application` (optional), OMITTED under `prototype` (§0.1) -->

| ID       | Priority | Statement              | Acceptance criteria (EARS — GR-23)                                       | Source                   | Rationale (application only, optional) |
| -------- | -------- | ---------------------- | ------------------------------------------------------------------------ | ------------------------ | -------------------------------------- |
| F-{{nn}} | Must / Should / Could / Won't <!-- GR-24 --> | {{functional_requirement}} | {{ears_acceptance_criterion}} <!-- "When <trigger>, the system shall <response>." etc. — GR-23; ≤3 preconditions; Tier B5 auto-fabricates --> | stated / → §X / inferred | {{why_this_requirement}} <!-- the business reason; application target only, omit the column under prototype --> |

<!-- repeat per functional requirement -->

### 6.2 Business rules

<!-- format: table[6-col: ID(BR-NN), statement(when/then), enforcement_point∈{ui,service,data,cross-layer}, acceptance_criteria, source, severity∈{blocker,major,minor}]; statement form "When {condition}, then {required_outcome}"; AC in EARS form (GR-23) -->
<!-- guidance: enforcement_point ∈ {ui, service, data, cross-layer} — `service`/`data`/`cross-layer` rows are the server-side enforcement that a future BFF/DB generator consumes; AC in EARS keywords per GR-23 -->

| ID | Statement (when / then) | Enforcement point | Acceptance criteria (EARS — GR-23) | Source | Severity |
| --- | --- | --- | --- | --- | --- |
| BR-{{nn}} | When {{condition}}, then {{required_outcome}} | UI / service / data / cross-layer | {{ears_acceptance_criterion}} <!-- "If <unwanted condition>, then the system shall <response>." / "When <trigger>, the system shall <response>." — GR-23; Tier B5 --> | → §2.3 invariant / → §6.1 F-{{nn}} / consultant input | blocker / major / minor |

<!-- repeat per business rule; IDs are stable and may be referenced from §5 task flows (decision points), §6.5 access control (action gating), and §2.5 state transitions (pre-conditions) -->

### 6.3 Validation rules

<!-- format: table[4-col: field→§7, validation_type∈{required,format,range,length,enum,cross-field,business-rule-ref}, rule, error_message]; references §7 fields; business-rule-ref points to §6.2 BR-NN -->
<!-- guidance: prototypable inline error feedback only; backend validation logic is OOS per `framework/shared/prototype-scope.md` -->

> Field-level validation surfaced to the user as inline UI feedback (required-field markers, format hints, range/length errors). Validation timing follows `GR-05`. Backend enforcement of business invariants belongs to §6.2 BR-NN and the sibling backend doc; this section captures the *visible* validation surface only. The `Rule → Error message` pairing is **already** in EARS event-driven form by construction ("When the field violates {rule}, the system shall show {error message}"), so `GR-23` does not re-phrase this section — its tabular shape is retained.

| Field (→ §7)              | Validation type                                                                | Rule                          | Error message              |
| ------------------------- | ------------------------------------------------------------------------------ | ----------------------------- | -------------------------- |
| {{shape}}.{{field}}       | required / format / range / length / enum / cross-field / business-rule-ref    | {{rule_or_BR_ref}}            | {{user_facing_message}}    |

<!-- repeat per validation rule; field cell references a §7 shape field; cross-field rule may reference ≥1 sibling field; business-rule-ref cites a §6.2 BR-NN -->

### 6.4 UI feature needs

<!-- format: table[5-col: ID(UI-NN), priority, feature_need, linked(G/story/BR), acceptance_criteria]; behavioural phrasing only — "user can …", "system shows …"; GR-21 forbids layout vocabulary; AC observable-signal NOT EARS (GR-23) -->
<!-- guidance: rows deterministically resolved by GR-05..GR-18 carry [STANDARD-RULE: GR-NN]; priority per GR-24 (B6) -->

> *What UI elements and behaviours the FE must provide.* Never layout, position, framework, component name, or visual design (`GR-21`). Phrase behaviourally ("user can filter by status", "save action is available"); do not phrase visually ("filter chips in the toolbar"). UI feature rows resolved deterministically by `GR-05..GR-18` carry `[STANDARD-RULE: GR-NN]`. Acceptance criteria stay observable-signal phrasing (`GR-23` reserves EARS for §6.1/§6.2).

| ID | Priority | Feature need | Linked (G / story / BR) | Acceptance criteria |
| --- | --- | --- | --- | --- |
| UI-{{nn}} | Must / Should / Could / Won't <!-- GR-24 --> | {{behavioural_need}} <!-- e.g. "user can bulk-delete selected rows with confirmation" --> | → §4.1 G-{{nn}} / → §4.2 / → §6.2 BR-{{nn}} | {{observable_signal}} |

<!-- repeat per feature need -->

#### 6.4.5 Edge, empty & error states

<!-- format: table[4-col: surface→(§4.2 story | §5 flow | UI-NN), condition∈{empty,partial,error,offline,loading,permission-denied}, expected_ui_behaviour, recovery_action]; behavioural phrasing only (GR-21) -->
<!-- guidance: emit when §5 flow has exception_paths OR §6.4 row implies state branching; prototypable per `framework/shared/prototype-scope.md` -->

> The UI behaviour the user sees in non-happy-path states. Captures empty datasets, partial loads, transient errors, offline degradation, loading affordances, and permission-denied surfaces. Behavioural phrasing only (`GR-21` — describe what the user sees and can do, not where it sits on screen).

| Surface (→ story / flow / UI-NN) | Condition                                                                | Expected UI behaviour                                          | Recovery action                       |
| -------------------------------- | ------------------------------------------------------------------------ | -------------------------------------------------------------- | ------------------------------------- |
| {{surface_ref}}                  | empty / partial / error / offline / loading / permission-denied          | {{behavioural_description}}                                    | {{user_action_or_system_retry}}       |

<!-- repeat per edge state; surface cell references a §4.2 story, a §5 flow, or a §6.4 UI-NN row; condition uses the closed vocabulary -->

### 6.5 Access control (RBAC)

<!-- format: matrix[rows=§3 personas, cols=§7 entities + §5 flows]; cell-vocabulary ∈ {C,R,U,D,X,A,—}; conditional cells "U†BR-NN" -->
<!-- guidance: every §3 persona is a row; every §7 entity & §5 flow is a column (A3/A4/A5) -->

> Roles-×-resources matrix. Cell values use the action vocabulary below; blanks mean "no access".

**Action vocabulary:** `C` create · `R` read · `U` update · `D` delete · `X` execute / invoke · `A` approve · `—` no access. Suffix with a BR ref for conditional access (e.g. `U†BR-07` = update gated by BR-07).

| Role (→ §3)      | {{resource_or_flow_1}} | {{resource_or_flow_2}} | …   |
| ---------------- | ---------------------- | ---------------------- | --- |
| {{persona_name}} | C R U D                | R                      | —   |

<!-- one row per persona in §3; one column per §7 entity and per §5 flow. Conditional access cells reference a BR-NN from §6.2. -->

### 6.6 Non-functional (FE-only)

> Frontend NFRs only. Backend availability / throughput / persistence concerns live in the sibling backend requirements doc. Inferred values carry `[AI-SUGGESTED]`.

#### 6.6.1 Session UX

<!-- format: table[3-col: field, value, source]; quantified — minutes/seconds/hours, never "soon"; GR-19 supplies defaults when input is silent -->
<!-- emit: emit-conditional on target — OMITTED under `target = prototype` (server + auth are simulated per PI-01/PI-03, so session policy is moot); emitted under `target = application` -->

> **Emitted under `target = application` only** (§0.1) — a client-side prototype has no real session/auth surface (PI-01/PI-03).

| Field                    | Value                                                                             | Source            |
| ------------------------ | --------------------------------------------------------------------------------- | ----------------- |
| Idle session timeout     | {{minutes}}                                                                       | stated / inferred |
| Absolute session timeout | {{minutes_or_hours}}                                                              | stated / inferred |
| Idle warning lead-time   | {{seconds}} <!-- "warn the user N seconds before idle logout" -->                 | stated / inferred |
| Re-auth scope            | {{actions_requiring_step_up}} <!-- e.g. "approve loan", "change bank details" --> | stated / inferred |
| Account lockout messaging | {{ui_message_after_N_failed_attempts}}                                            | stated / inferred |
| MFA prompt scope         | {{actions_or_logins_requiring_mfa_prompt}}                                        | stated / inferred |

#### 6.6.2 Frontend performance budgets

<!-- format: table[3-col: metric, target, source]; targets quantified with units & percentile (e.g. "p95 ≤ 2.0s", "≤ 250KB gzipped") — never "fast" or "small" -->
<!-- emit: emit-conditional on target — OMITTED under `target = prototype` (the prototype is a review harness per PI-08, never perf-optimised); emitted under `target = application` (optional) -->

> **Emitted under `target = application` only** (§0.1) — the prototype is a review harness (PI-08), not a perf-optimised build.

| Metric                                                | Target    | Source            |
| ----------------------------------------------------- | --------- | ----------------- |
| Time to interactive (p95)                             | {{value}} | stated / inferred |
| Initial bundle size budget                            | {{value}} | stated / inferred |
| Render budget for largest list/table                  | {{value}} | stated / inferred |
| Time to meaningful content                            | {{value}} | stated / inferred |

#### 6.6.4 Compliance UI behaviour

<!-- format: bullets; one consent / redaction / regional-variant per bullet; backend retention is OOS -->

- {{consent_and_redaction_requirements}} <!-- e.g. cookie / consent banners, PII screen-redaction rules, regional UI variants. Backend audit retention and storage rules are out of scope. -->

#### 6.6.5 Accessibility

<!-- format: bullets; one accessibility target per bullet (e.g. WCAG 2.2 AA, assistive-tech scope, keyboard-only path) -->

- {{accessibility_target}} <!-- e.g. WCAG 2.2 AA; assistive-tech scope -->

### 6.7 Reporting feature needs

<!-- format: table[8-col: ID(RPT-NN), purpose, audience→§3, source_concepts→§2.1, filters, measures, export_formats∈{csv,pdf,json,none}, scheduling∈{on-demand,daily,weekly,monthly}]; chart-type/layout forbidden (GR-21) -->

> Each row captures *what reporting must exist*, never *how it is visualised*. Chart type, layout, and visualisation choice are determined by the later UX step (`GR-21`).

| ID | Purpose | Audience (→ §3) | Source concept(s) (→ §2.1) | Filter dimensions | Measures / columns | Export formats | Scheduling |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RPT-{{nn}} | {{purpose}} | {{persona}} | {{concept_refs}} | {{filters}} | {{measures}} | csv / pdf / json / none | on-demand / daily / weekly / monthly |

<!-- repeat per reporting need -->

### 6.8 Notification points

<!-- format: table[5-col: ID(NT-NN), event, audience→§3, channel_category∈{in-app,email,sms,webhook,push}, trigger_condition_or_BR_ref]; capability-level channel only (GR-20) -->

> Channel category is capability-level only (`in-app`, `email`, `sms`, `webhook`, `push`); never a vendor name (`GR-20`). Trigger condition may reference a `BR-NN`.

| ID | Event | Audience (→ §3) | Channel category | Trigger condition |
| --- | --- | --- | --- | --- |
| NT-{{nn}} | {{event}} | {{persona}} | in-app / email / sms / webhook / push | {{condition_or_BR_ref}} |

<!-- repeat per notification point -->

### 6.9 Audit-trail UI feature

<!-- format: table[4-col: entity→§7, audited_fields, retention_surface, viewer_access→§6.5]; viewer UI only; backend audit logging is OOS -->

> Emitted only when §6.6.4 compliance or input documents call for user-visible audit history. Backend audit logging is out of scope; this section specifies the *viewer UI* only.

| Entity (→ §7) | Audited fields | Retention surface         | Viewer access (→ §6.5)    |
| ------------- | -------------- | ------------------------- | ------------------------- |
| {{entity}}    | {{fields}}     | {{ui_retention_window}} <!-- e.g. "last 90 days visible in UI" --> | {{personas_with_view_action}} |

<!-- repeat per audited entity -->

### 6.10 Consumed backend contracts

<!-- format: prototype: table[3-col: operation, fixture_reference, notes]; application: table[3-col: operation, backend_contract_pointer, notes]; emit only the sub-block matching manifest.target -->
<!-- guidance: every operation maps to §6.1 F-NN (A14); application-mode pointer never restates the contract -->

> FE-facing only. The drafter emits one sub-block matching `manifest.target`; the merger does not see both.

#### Under `target = prototype`

| Operation | Fixture reference                          | Notes        |
| --------- | ------------------------------------------ | ------------ |
| {{op}}    | {{fixture_path}} <!-- e.g. `fixtures/customers.json` --> | {{notes}}    |

#### Under `target = application`

| Operation | Backend contract pointer                                            | Notes     |
| --------- | ------------------------------------------------------------------- | --------- |
| {{op}}    | → {{path_in_backend_doc}} <!-- e.g. `../backend/requirements.md#operation-list-orders` — pointer only, FE doc never restates the contract --> | {{notes}} |

<!-- repeat per consumed operation -->

---

## 7. Data shapes consumed by the FE

<!-- format: per-shape table[5-col: field, type, required∈{yes,no}, ui_display∈{form-input,table-col,detail,chip,enum,hidden}, notes]; followed by trailing meta lines: domain_concept→§2.1, source∈{prototype-fixture,backend-contract}, enums -->
<!-- guidance: every persistent §2.1 concept appears here (A6); ui_display=hidden gates D2 marker behaviour -->

> Shape of data the FE reads and writes. Under `target = prototype`: the shape of in-memory fixtures (PI-02). Under `target = application`: the shape of payloads exchanged with the backend (authoritative shape lives in the sibling backend requirements doc). Persistence design — indexes, FK constraints, storage layout — is the backend doc's concern, not this section's.

### Shape: {{shape_name}}

| Field     | Type     | Required | UI-display                                                            | Notes     |
| --------- | -------- | -------- | --------------------------------------------------------------------- | --------- |
| {{field}} | {{type}} | yes / no | form-input / table-col / detail / chip / enum / hidden                | {{notes}} |

**Domain concept:** → §2.1 {{concept_name}}
**Source:** prototype-fixture / backend-contract <!-- auto-filled from `manifest.target` -->
**Enums:** {{enums}}

<!-- repeat per shape. Field-level validation timing follows GR-05 and lives in §6.4. -->

### 7.X Derivations

<!-- format: table[4-col: derived_concept→§2.1, derivation_rule, inputs, refresh_trigger∈{on-load,on-change,scheduled}]; emitted iff ≥1 §2.1 concept has persistence=derived -->

> Emitted only when ≥1 §2.1 concept has `Persistence = derived`. Derivation rule phrased in business language; computation tier is determined at code-generation time (capability category appears in §1.7 if non-trivial).

| Derived concept (→ §2.1) | Derivation rule (business language) | Inputs                          | Refresh trigger                |
| ------------------------ | ----------------------------------- | ------------------------------- | ------------------------------ |
| {{concept}}              | {{rule}}                            | {{concept_or_field_refs}}       | on-load / on-change / scheduled |

<!-- repeat per derived concept -->

---

## 8. Source UI references

<!-- format: table[3-col: reference_name, location_path_or_url, notes]; input citations only — exempt from GR-21 -->
<!-- emit: content-conditional — omit the whole section when no consultant supplied a screenshot / wireframe / existing-tool screen (§0.1); never emit an empty table -->

> Omitted entirely when no consultant-supplied UI reference exists (§0.1 content-conditional).

| Reference | Location        | Notes                                                        |
| --------- | --------------- | ------------------------------------------------------------ |
| {{name}}  | {{path_or_url}} | {{layout / fields / navigation / states / actions observed}} |

<!-- consultant-supplied screenshots, wireframes, existing-tool screens. These are *input citations*, not normative spec; layout observations quoted here are exempt from `GR-21`. -->

---

## 9. Key terminology

<!-- format: table[3-col: term, definition_or_§2.1_ref, inconsistency_flag]; domain or non-domain terms -->
<!-- emit: content-conditional — emit a row ONLY for a term that carries an inconsistency flag or an alternate-term usage worth recording; omit the whole section when none apply. The full domain glossary is produced by the GLOSSARY analysis (`analyse-requirements/GLOSSARY/`), not duplicated here. -->

> **Inconsistency register, not a glossary.** Record only terms where the consultant uses an alternate label or the inputs disagree — the canonical, complete domain glossary is produced separately by the GLOSSARY methodology (`analyse-requirements/GLOSSARY/`). Omitted entirely when no inconsistency applies (§0.1 content-conditional).

| Term     | Definition                                 | Inconsistency flag                              |
| -------- | ------------------------------------------ | ----------------------------------------------- |
| {{term}} | {{domain_specific_definition_or_§2.1_ref}} | {{consultant_uses_alternate / inputs_disagree}} |

---

## 10. Volumes

<!-- format: table[3-col: metric, value, source]; three required rows: data_volume, frequency, concurrency — all populated (A9); inferred values [AI-SUGGESTED] -->

> Volumes drive UI pattern selection only — pagination thresholds, virtualization choices, list-vs-card density, chart-type suitability. Capacity planning, infrastructure sizing, and load testing belong to the backend doc.

| Metric      | Value                 | Source                |
| ----------- | --------------------- | --------------------- |
| Data volume | {{records_or_bytes}}  | {{stated / inferred}} |
| Frequency   | {{events_per_period}} | {{stated / inferred}} |
| Concurrency | {{concurrent_users}}  | {{stated / inferred}} |

<!-- volumes are commonly absent in client briefs — flag [AI-SUGGESTED] when inferred from domain heuristics -->

---
