<!-- ROLE: skill. STATUS: stub — author during phase-1 build-order step 2. -->

# extract-facts.md

**Purpose:** Pull literal statements from converted input files: business purpose, problem, domain, application goal, **domain concepts (incl. non-persistent: derived metrics, policies, decisions) + relationship verbs + aggregate hints + lifecycle states**, user goals, tasks, task flows, quality signals, design instructions, business rules, technical constraints, volumes, user behaviours, target users, roles. No interpretation; flag interpretable items.

**Inputs:** `requirements/source-manifest.json`, converted input files, `assets/topics-requirements.md`.

**Outputs:** structured fact list keyed by topic, ready for `categorise-by-topic.md`.

**Used by:** `framework/agents/requirements-drafter/agent.md`.

**Used how:** Called early in the drafter workflow before topic categorisation. Domain-free verb; references no agents.

> Content TBD per `plan/v7b-Brief.md > §Approach > skills` + agent roster row 2.
