<!-- ROLE: skill. STATUS: stub — author during phase-1 build-order step 2. -->

# flag-gaps-ambiguities.md

**Purpose:** Surface gaps, ambiguities, and inconsistencies in categorised facts before drafting begins; mark items for AI-suggested enrichment vs Q&A vs reconciliation.

**Inputs:** categorised fact list from `categorise-by-topic.md`.

**Outputs:** list of flagged items with category (AI-suggested / vague / contradictory) + recommended resolution path.

**Used by:** `framework/agents/requirements-drafter/agent.md`.

**Used how:** Called after categorisation. Pre-feeds the completeness-report finding categories so the drafter knows which fields to mark `[AI-SUGGESTED]` and which to leave for Q&A.

> Content TBD per `plan/v7b-Brief.md > §Approach > skills`.
