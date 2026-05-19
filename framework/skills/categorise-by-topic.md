<!-- ROLE: skill. STATUS: stub — author during phase-1 build-order step 2. -->

# categorise-by-topic.md

**Purpose:** Bucket extracted facts under the canonical topic list in `assets/topics-requirements.md`.

**Inputs:** fact list from `extract-facts.md`, `assets/topics-requirements.md`.

**Outputs:** facts grouped under the canonical topic list (Application context / Scope / Assumptions & deps / Architectural implications / Domain model / Target users / User goals / Task flows / Requirements / Data shapes / Source UI references / Key terminology / Volumes). Within §6 Requirements, sub-buckets are §6.1 Functional, §6.2 Business rules (BR-NN rows; statements of the form "when X then Y"), §6.4 UI feature needs, §6.5 Access control (role-permission statements; RBAC matrix cells), §6.6 Non-functional FE (session UX, FE performance budgets, compliance UI behaviour, accessibility), §6.7 Reporting feature needs, §6.8 Notification points, §6.9 Audit-trail UI feature (conditional), §6.10 Consumed backend contracts.

**Used by:** `framework/agents/requirements-drafter/agent.md`.

**Used how:** Called after `extract-facts.md` and before drafting. Surfaces empty topics for the drafter's fill-every-field pass.

> Content TBD per `plan/v7b-Brief.md > §Approach > skills`.
