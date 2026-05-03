<!-- ROLE: asset. v7a-derived seed (sections lifted from .claude/skills/wds-1-project-brief/templates/project-brief.template.md). Finalise during phase-1 build-order step 1 per v7b-Brief.md > §template-requirements.md and §topics-requirements.md. Section order matches topics-requirements.md one-to-one. -->

# Requirements: {{application_name}}

**Domain:** {{domain}} <!-- inferred from inputs; flag [AI-SUGGESTED] if not stated explicitly --> **Created:** {{date}} **Status:** draft | final **Last finalised at:** {{last_finalised_at}}

> Inferred content is marked inline with one of three markers per the drafter's decision tree (`framework/agents/requirements-drafter.md > Classification`):
> - `[AI-SUGGESTED: AI-NNN | blocking|non-blocking]` — inferred completeness-gating, in-scope value; resolver asks the consultant.
> - `[STANDARD-RULE: GR-NN]` — deterministic answer from `framework/shared/general-rules.md`; resolver skips.
> - `[OUT-OF-SCOPE: domain-default]` — required by template but outside prototype scope per `framework/shared/prototype-scope.md`; resolver skips, consultant can scan-review.
>
> Field-level marking when only some sub-fields are inferred; heading-level marking when the whole item is invented. The fill-every-field rule applies — no blanks.

---

## 1. Application context

**Name:** {{application_name}}

**Purpose / business value:** {{purpose}}

**Domain:** {{domain}}

**Business goal:** {{business_goal}}

<!-- rev: run-N YYYY-MM-DD -->

---

## 2. Domain model

> The BA's framing of the business domain in **ubiquitous language**, implementation-free.

### 2.1 Concepts

| Concept          | Persistence                   | Definition (ubiquitous language)     |
| ---------------- | ----------------------------- | ------------------------------------ |
| {{concept_name}} | persistent / derived / policy | {{one-sentence business definition}} |

<!-- include non-persistent concepts (e.g. Eligibility, Risk Tier, Underwriting Decision) alongside persistent ones; persistent concepts must also appear in §7 -->

### 2.2 Relationships

- {{Concept A}} **{{verb-phrase}}** {{Concept B}} [{{cardinality}}]

<!-- verbs come from the business ("Borrower **submits** Application"), not from data ("Borrower hasMany Application"); cardinality optional but recommended -->

### 2.3 Aggregates & lifecycles

#### {{aggregate_root}}

| Field            | Value                                                                                                                              |
| ---------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| Member concepts  | {{member_concept_list}}                                                                                                            |
| Lifecycle states | {{ordered_state_list}} <!-- e.g. Application → Approved → Disbursed → Servicing → Closed; transitions defined in §5 Task flows --> |
| Key invariants   | {{business_invariants}} <!-- e.g. "Loan cannot be Disbursed until KYC is Verified" -->                                             |

<!-- repeat per aggregate -->

### 2.4 Diagram (optional)

```mermaid
classDiagram
    %% Mermaid classDiagram or erDiagram in domain mode; markdown-native, diff-able, tool-agnostic.
    %% Absence of this block is a vague-finding (gap category 2), not a blocker.
```

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

<!-- repeat per story under each persona; persona heading once per persona, story sub-heading per story. A single goal in §4.1 may be referenced by stories under multiple personas (M:N is expected). -->

---

## 5. Task flows

### Flow: {{flow_name}}

| Field                      | Value                                                        |
| -------------------------- | ------------------------------------------------------------ |
| Actor                      | {{actor_persona_ref}}                                        |
| Trigger                    | {{trigger}}                                                  |
| Steps                      | {{ordered_steps}}                                            |
| Decision points            | {{decision_points}}                                          |
| Exception paths            | {{exception_paths}}                                          |
| Role-conditional behaviour | {{role_gating}} <!-- e.g. "only team leads can reassign" --> |

<!-- repeat per flow -->

---

## 6. Requirements

### 6.1 Functional

- {{functional_requirements}}

### 6.2 Business rules

| ID | Statement (when / then) | Enforcement point | Source | Severity |
| --- | --- | --- | --- | --- |
| BR-{{nn}} | When {{condition}}, then {{required_outcome}} | UI / service / data / cross-layer | → §2.3 invariant / → §6.1 F-{{nn}} / consultant input | blocker / major / minor |

<!-- repeat per business rule; IDs are stable and may be referenced from §5 task flows (decision points) and §6.5 access control (action gating) -->

### 6.3 Data

- {{data_requirements}}

### 6.4 User-facing

- {{user_facing_requirements}}

### 6.5 Access control (RBAC)

> Roles-×-resources matrix. Cell values use the action vocabulary below; blanks mean "no access".

**Action vocabulary:** `C` create · `R` read · `U` update · `D` delete · `X` execute / invoke · `A` approve · `—` no access. Suffix with a BR ref for conditional access (e.g. `U†BR-07` = update gated by BR-07).

| Role (→ §3)      | {{resource_or_flow_1}} | {{resource_or_flow_2}} | …   |
| ---------------- | ---------------------- | ---------------------- | --- |
| {{persona_name}} | C R U D                | R                      | —   |

<!-- one row per persona in §3; one column per §7 entity and per §5 flow. Conditional access cells reference a BR-NN from §6.2. -->

### 6.6 Non-functional

> NFRs are first-class and **must be filled even when inferred** — domain heuristics drive defaults (financial services ≠ marketing site). Inferred values carry `[AI-SUGGESTED]`.

#### 6.6.1 Security & session

| Field                    | Value                                                                             | Source            |
| ------------------------ | --------------------------------------------------------------------------------- | ----------------- |
| Idle session timeout     | {{minutes}}                                                                       | stated / inferred |
| Absolute session timeout | {{minutes_or_hours}}                                                              | stated / inferred |
| Idle warning lead-time   | {{seconds}} <!-- "warn the user N seconds before idle logout" -->                 | stated / inferred |
| Re-auth scope            | {{actions_requiring_step_up}} <!-- e.g. "approve loan", "change bank details" --> | stated / inferred |
| Account lockout policy   | {{failed_attempts_threshold_and_cooldown}}                                        | stated / inferred |
| MFA requirement          | {{required_optional_per_role}}                                                    | stated / inferred |

#### 6.6.2 Performance

| Metric                                                 | Target    | Source            |
| ------------------------------------------------------ | --------- | ----------------- |
| {{metric}} <!-- e.g. p95 page TTI, API p99 latency --> | {{value}} | stated / inferred |

#### 6.6.3 Availability

| Field              | Value             | Source            |
| ------------------ | ----------------- | ----------------- |
| Target uptime      | {{percent}}       | stated / inferred |
| Maintenance window | {{window}}        | stated / inferred |
| RTO / RPO          | {{rto}} / {{rpo}} | stated / inferred |

#### 6.6.4 Compliance & audit

- {{compliance_regimes}} <!-- e.g. POPIA, GDPR, PCI-DSS scope; audit-log retention; data residency -->

#### 6.6.5 Accessibility

- {{accessibility_target}} <!-- e.g. WCAG 2.2 AA; assistive-tech scope -->

---

## 7. Data entities

> Implementation-prep view: storage shape, types, validations, FK plumbing.

### Entity: {{entity_name}}

| Field     | Type     | Required | Validation     | Notes     |
| --------- | -------- | -------- | -------------- | --------- |
| {{field}} | {{type}} | yes/no   | {{validation}} | {{notes}} |

**Domain concept:** {{concept_name_from_§2.1}}

**Relationships:** {{relationships}} <!-- entity → entity, with cardinality; should align with §2.2 Relationships (storage view of the same business relationships) -->

**Enums:** {{enums}}

<!-- repeat per entity -->

---

## 8. Source UI references

| Reference | Location        | Notes                                                        |
| --------- | --------------- | ------------------------------------------------------------ |
| {{name}}  | {{path_or_url}} | {{layout / fields / navigation / states / actions observed}} |

<!-- consultant-supplied screenshots, wireframes, existing-tool screens -->

---

## 9. Key terminology

> Domain-concept definitions or non-domain-concept terms (process, role, UI).

| Term     | Definition                                 | Inconsistency flag                              |
| -------- | ------------------------------------------ | ----------------------------------------------- |
| {{term}} | {{domain_specific_definition_or_§2.1_ref}} | {{consultant_uses_alternate / inputs_disagree}} |

---

## 10. Volumes

| Metric      | Value                 | Source                |
| ----------- | --------------------- | --------------------- |
| Data volume | {{records_or_bytes}}  | {{stated / inferred}} |
| Frequency   | {{events_per_period}} | {{stated / inferred}} |
| Concurrency | {{concurrent_users}}  | {{stated / inferred}} |

<!-- volumes are commonly absent in client briefs — flag [AI-SUGGESTED] when inferred from domain heuristics -->

---
