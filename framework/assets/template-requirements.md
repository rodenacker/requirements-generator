<!-- ROLE: asset. Section order matches `framework/assets/topics-requirements.md` one-to-one. Audience is LLM-only (no human stakeholder consumption). -->

# Requirements: {{application_name}}

**Domain:** {{domain}} <!-- inferred from inputs; flag [AI-SUGGESTED] if not stated explicitly --> **Target:** prototype | application <!-- from `requirements/source-manifest.json > target`; controls §6.10 sub-block and PI-append --> **Created:** {{date}} **Status:** draft | final **Last finalised at:** {{last_finalised_at}}

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

> The `target` field on the source manifest is `prototype` or `application`. The drafter picks the matching variant for the rows below at fill-time; the merger does not see both.

| Section | `prototype` | `application` | Mode-conditional? |
| --- | --- | --- | --- |
| §6.10 Consumed backend contracts | fixture references | pointers into the sibling backend requirements document | yes — sub-block content differs |
| §7 Data shapes consumed by FE | shape sourced from fixtures | shape sourced from backend contracts | provenance label only |
| `## Prototype invariants` appendix | appended (PI-01..PI-07) | omitted | yes — merger conditional |
| (all other sections) | identical | identical | no |

---

## 1. Application context

**Name:** {{application_name}}

**Purpose / business value:** {{purpose}}

**Domain:** {{domain}}

**Business goal:** {{business_goal}}

<!-- rev: run-N YYYY-MM-DD -->

---

## 1.5 Scope

> §1.5 is in-scope-only — unsupplied buckets emit `[AI-SUGGESTED]` under both targets. `[OUT-OF-SCOPE: domain-default]` is **not** valid in this section (the section *defines* scope; OOS would be self-referential).

| Bucket | Items |
| --- | --- |
| In | {{in_scope_capabilities}} <!-- capability categories this FE must deliver --> |
| Out | {{out_of_scope_capabilities}} <!-- explicitly excluded; capability-level only; no product/vendor names per GR-20 --> |
| Deferred | {{deferred_capabilities}} <!-- known future scope; not in this build --> |

<!-- rev: run-N YYYY-MM-DD -->

---

## 1.6 Assumptions & dependencies

> Abstract services, persona prerequisites, environment assumptions. Cells naming a product or vendor fail `GR-20`.

| Kind | Statement | Source |
| --- | --- | --- |
| Abstract service dependency | {{capability_category}} <!-- e.g. "an identity provider", "a binary blob storage tier" --> | stated / inferred |
| Persona prerequisite | {{prerequisite}} <!-- e.g. "users have an existing account in the identity provider" --> | stated / inferred |
| Environment assumption | {{assumption}} <!-- e.g. "users on modern evergreen browser", "stable broadband connection" --> | stated / inferred |

<!-- repeat per row; one row per assumption / dependency -->

<!-- rev: run-N YYYY-MM-DD -->

---

## 1.7 Architectural implications

> Capability categories derived by the drafter from §6 functional requirements + §10 volumes + §6.7 reporting needs, against an inline catalogue of ≤15 categories (see `framework/agents/requirements-drafter.md > derive-architectural-implications`). Drafter seeds every row as `[AI-SUGGESTED: AI-NNN | non-blocking]`; resolver Q&A refines. Recommendation column is **optional** and **non-deterministic** — a stack choice belongs in the code-generation step, not here.

| Capability category | Driving requirement(s) | Recommendation (optional) |
| --- | --- | --- |
| {{capability}} <!-- e.g. "Client-side full-text search at ≤10⁴ records" --> | → §6.1 F-{{nn}} / §10 row / §6.7 RPT-{{nn}} | {{soft_recommendation}} <!-- e.g. "in-memory index acceptable given volume"; blank when no deterministic guidance --> |

<!-- repeat per active category -->

<!-- rev: run-N YYYY-MM-DD -->

---

## 2. Domain model

> The BA's framing of the business domain in **ubiquitous language**, implementation-free.

### 2.1 Concepts

| Concept          | Persistence                   | Definition (ubiquitous language)     |
| ---------------- | ----------------------------- | ------------------------------------ |
| {{concept_name}} | persistent / derived / policy | {{one-sentence business definition}} |

<!-- include non-persistent concepts (e.g. Eligibility, Risk Tier, Underwriting Decision) alongside persistent ones; persistent concepts must also appear in §7. Derived concepts must also appear in §7.X. -->

### 2.2 Relationships

- {{Concept A}} **{{verb-phrase}}** {{Concept B}} [{{cardinality}}]

<!-- verbs come from the business ("Borrower **submits** Application"), not from data ("Borrower hasMany Application"); cardinality optional but recommended -->

### 2.3 Aggregates & lifecycles

#### {{aggregate_root}}

| Field            | Value                                                                                                                              |
| ---------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| Member concepts  | {{member_concept_list}}                                                                                                            |
| Lifecycle states | {{ordered_state_list}} <!-- e.g. Application → Approved → Disbursed → Servicing → Closed; transitions defined in §2.5 when >2 states --> |
| Key invariants   | {{business_invariants}} <!-- e.g. "Loan cannot be Disbursed until KYC is Verified" -->                                             |

<!-- repeat per aggregate -->

### 2.4 Diagram (optional)

```mermaid
classDiagram
    %% Mermaid classDiagram or erDiagram in domain mode; markdown-native, diff-able, tool-agnostic.
    %% Absence of this block is a vague-finding (gap category 2), not a blocker.
```

### 2.5 State-transition matrix

> Emitted only when ≥1 §2.3 aggregate has more than two lifecycle states. One sub-block per qualifying aggregate. Pre-condition cells may reference `→ §6.2 BR-NN`.

#### {{aggregate_root}}

| From → To                       | Trigger                       | Pre-condition                                  | Visible effect                                                          |
| ------------------------------- | ----------------------------- | ---------------------------------------------- | ----------------------------------------------------------------------- |
| {{from_state}} → {{to_state}}   | {{triggering_event}}          | {{precondition_or_BR_ref}}                     | {{ui_observable_change}} <!-- badge change, screen route, action gain --> |

<!-- repeat per transition; rows whose Visible effect is purely server-side become [OUT-OF-SCOPE] under prototype / no marker under application (Tier D3) -->

<!-- rev: run-N YYYY-MM-DD -->

---

## 3. Target users

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

| ID | Goal statement | Quality signals | Goal kind | Layout pref (optional) | UX-pattern pref (optional) |
| --- | --- | --- | --- | --- | --- |
| G-{{nn}} | {{goal_statement}} | {{quality_signals}} <!-- resolve via taxonomy-goals.md --> | top-level / sub-level / interaction-level | {{layout_preference}} | {{ux_pattern_preference}} |

<!-- repeat per goal; IDs are stable and referenced from §4.2 stories and §5 task flows -->

### 4.2 Stories by persona

#### {{persona_name}} <!-- → §3 -->

##### Story: As a {{role}}, I want {{intent}}, so that {{benefit}}

| Field                                    | Value                                                                                      |
| ---------------------------------------- | ------------------------------------------------------------------------------------------ |
| Goal                                     | → §4.1 G-{{nn}}                                                                            |
| Objective                                | {{objective}} <!-- behavioural objective for this story; the outcome lives on the goal --> |
| Context (frequency / expertise / stakes) | {{context}}                                                                                |
| Linked task flow (optional)              | {{flow_ref}} <!-- → §5 -->                                                                 |
| Acceptance criteria                      | {{given_when_then_or_observable_signals}} <!-- ≥1 bullet; behavioural, not visual; see Tier B5 in gap-pass --> |

<!-- repeat per story under each persona; persona heading once per persona, story sub-heading per story. A single goal in §4.1 may be referenced by stories under multiple personas (M:N is expected). -->

---

## 5. Task flows

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

| ID       | Statement              | Acceptance criteria                                                       | Source                                |
| -------- | ---------------------- | ------------------------------------------------------------------------- | ------------------------------------- |
| F-{{nn}} | {{functional_requirement}} | {{given_when_then_or_observable_signal}} <!-- Tier B5 auto-fabricates --> | stated / → §X / inferred              |

<!-- repeat per functional requirement -->

### 6.2 Business rules

| ID | Statement (when / then) | Enforcement point | Acceptance criteria | Source | Severity |
| --- | --- | --- | --- | --- | --- |
| BR-{{nn}} | When {{condition}}, then {{required_outcome}} | UI / service / data / cross-layer | {{observable_signal_or_test}} <!-- Tier B5 --> | → §2.3 invariant / → §6.1 F-{{nn}} / consultant input | blocker / major / minor |

<!-- repeat per business rule; IDs are stable and may be referenced from §5 task flows (decision points), §6.5 access control (action gating), and §2.5 state transitions (pre-conditions) -->

### 6.4 UI feature needs

> *What UI elements and behaviours the FE must provide.* Never layout, position, framework, component name, or visual design (`GR-21`). Phrase behaviourally ("user can filter by status", "save action is available"); do not phrase visually ("filter chips in the toolbar"). UI feature rows resolved deterministically by `GR-05..GR-18` carry `[STANDARD-RULE: GR-NN]`.

| ID | Feature need | Linked (G / story / BR) | Acceptance criteria |
| --- | --- | --- | --- |
| UI-{{nn}} | {{behavioural_need}} <!-- e.g. "user can bulk-delete selected rows with confirmation" --> | → §4.1 G-{{nn}} / → §4.2 / → §6.2 BR-{{nn}} | {{observable_signal}} |

<!-- repeat per feature need -->

### 6.5 Access control (RBAC)

> Roles-×-resources matrix. Cell values use the action vocabulary below; blanks mean "no access".

**Action vocabulary:** `C` create · `R` read · `U` update · `D` delete · `X` execute / invoke · `A` approve · `—` no access. Suffix with a BR ref for conditional access (e.g. `U†BR-07` = update gated by BR-07).

| Role (→ §3)      | {{resource_or_flow_1}} | {{resource_or_flow_2}} | …   |
| ---------------- | ---------------------- | ---------------------- | --- |
| {{persona_name}} | C R U D                | R                      | —   |

<!-- one row per persona in §3; one column per §7 entity and per §5 flow. Conditional access cells reference a BR-NN from §6.2. -->

### 6.6 Non-functional (FE-only)

> Frontend NFRs only. Backend availability / throughput / persistence concerns live in the sibling backend requirements doc. Inferred values carry `[AI-SUGGESTED]`.

#### 6.6.1 Session UX

| Field                    | Value                                                                             | Source            |
| ------------------------ | --------------------------------------------------------------------------------- | ----------------- |
| Idle session timeout     | {{minutes}}                                                                       | stated / inferred |
| Absolute session timeout | {{minutes_or_hours}}                                                              | stated / inferred |
| Idle warning lead-time   | {{seconds}} <!-- "warn the user N seconds before idle logout" -->                 | stated / inferred |
| Re-auth scope            | {{actions_requiring_step_up}} <!-- e.g. "approve loan", "change bank details" --> | stated / inferred |
| Account lockout messaging | {{ui_message_after_N_failed_attempts}}                                            | stated / inferred |
| MFA prompt scope         | {{actions_or_logins_requiring_mfa_prompt}}                                        | stated / inferred |

#### 6.6.2 Frontend performance budgets

| Metric                                                | Target    | Source            |
| ----------------------------------------------------- | --------- | ----------------- |
| Time to interactive (p95)                             | {{value}} | stated / inferred |
| Initial bundle size budget                            | {{value}} | stated / inferred |
| Render budget for largest list/table                  | {{value}} | stated / inferred |
| Time to meaningful content                            | {{value}} | stated / inferred |

#### 6.6.4 Compliance UI behaviour

- {{consent_and_redaction_requirements}} <!-- e.g. cookie / consent banners, PII screen-redaction rules, regional UI variants. Backend audit retention and storage rules are out of scope. -->

#### 6.6.5 Accessibility

- {{accessibility_target}} <!-- e.g. WCAG 2.2 AA; assistive-tech scope -->

### 6.7 Reporting feature needs

> Each row captures *what reporting must exist*, never *how it is visualised*. Chart type, layout, and visualisation choice are determined by the later UX step (`GR-21`).

| ID | Purpose | Audience (→ §3) | Source concept(s) (→ §2.1) | Filter dimensions | Measures / columns | Export formats | Scheduling |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RPT-{{nn}} | {{purpose}} | {{persona}} | {{concept_refs}} | {{filters}} | {{measures}} | csv / pdf / json / none | on-demand / daily / weekly / monthly |

<!-- repeat per reporting need -->

### 6.8 Notification points

> Channel category is capability-level only (`in-app`, `email`, `sms`, `webhook`, `push`); never a vendor name (`GR-20`). Trigger condition may reference a `BR-NN`.

| ID | Event | Audience (→ §3) | Channel category | Trigger condition |
| --- | --- | --- | --- | --- |
| NT-{{nn}} | {{event}} | {{persona}} | in-app / email / sms / webhook / push | {{condition_or_BR_ref}} |

<!-- repeat per notification point -->

### 6.9 Audit-trail UI feature

> Emitted only when §6.6.4 compliance or input documents call for user-visible audit history. Backend audit logging is out of scope; this section specifies the *viewer UI* only.

| Entity (→ §7) | Audited fields | Retention surface         | Viewer access (→ §6.5)    |
| ------------- | -------------- | ------------------------- | ------------------------- |
| {{entity}}    | {{fields}}     | {{ui_retention_window}} <!-- e.g. "last 90 days visible in UI" --> | {{personas_with_view_action}} |

<!-- repeat per audited entity -->

### 6.10 Consumed backend contracts

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

> Emitted only when ≥1 §2.1 concept has `Persistence = derived`. Derivation rule phrased in business language; computation tier is determined at code-generation time (capability category appears in §1.7 if non-trivial).

| Derived concept (→ §2.1) | Derivation rule (business language) | Inputs                          | Refresh trigger                |
| ------------------------ | ----------------------------------- | ------------------------------- | ------------------------------ |
| {{concept}}              | {{rule}}                            | {{concept_or_field_refs}}       | on-load / on-change / scheduled |

<!-- repeat per derived concept -->

---

## 8. Source UI references

| Reference | Location        | Notes                                                        |
| --------- | --------------- | ------------------------------------------------------------ |
| {{name}}  | {{path_or_url}} | {{layout / fields / navigation / states / actions observed}} |

<!-- consultant-supplied screenshots, wireframes, existing-tool screens. These are *input citations*, not normative spec; layout observations quoted here are exempt from `GR-21`. -->

---

## 9. Key terminology

> Domain-concept definitions or non-domain-concept terms (process, role, UI).

| Term     | Definition                                 | Inconsistency flag                              |
| -------- | ------------------------------------------ | ----------------------------------------------- |
| {{term}} | {{domain_specific_definition_or_§2.1_ref}} | {{consultant_uses_alternate / inputs_disagree}} |

---

## 10. Volumes

> Volumes drive UI pattern selection only — pagination thresholds, virtualization choices, list-vs-card density, chart-type suitability. Capacity planning, infrastructure sizing, and load testing belong to the backend doc.

| Metric      | Value                 | Source                |
| ----------- | --------------------- | --------------------- |
| Data volume | {{records_or_bytes}}  | {{stated / inferred}} |
| Frequency   | {{events_per_period}} | {{stated / inferred}} |
| Concurrency | {{concurrent_users}}  | {{stated / inferred}} |

<!-- volumes are commonly absent in client briefs — flag [AI-SUGGESTED] when inferred from domain heuristics -->

---
