<!-- ROLE: skill. STATUS: stub — author during phase-1 build-order step 2. -->

# categorise-by-topic.md

**Purpose:** Bucket extracted facts under the canonical topic list in `assets/topics-requirements.md`.

**Inputs:** fact list from `extract-facts.md`, `assets/topics-requirements.md`.

**Outputs:** facts grouped under topics 1–10 (Application context / Domain model / Target users / User goals / Task flows / Requirements / Data entities / Source UI references / Key terminology / Volumes). Within §6 Requirements, sub-buckets are §6.1 Functional, §6.2 Business rules (BR-NN rows; statements of the form "when X then Y"), §6.3 Data, §6.4 User-facing, §6.5 Access control (role-permission statements; RBAC matrix cells), §6.6 Non-functional (security & session — including session timeout, lockout, MFA — performance, availability, compliance & audit, accessibility).

**Used by:** `framework/agents/requirements-drafter/agent.md`.

**Used how:** Called after `extract-facts.md` and before drafting. Surfaces empty topics for the drafter's fill-every-field pass.

> Content TBD per `plan/v7b-Brief.md > §Approach > skills`.
