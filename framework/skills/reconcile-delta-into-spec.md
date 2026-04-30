<!-- ROLE: skill. STATUS: stub — author during phase-1 build-order step 6. -->

# reconcile-delta-into-spec.md

**Purpose:** On rerun, fold the new/changed information from updated inputs into the main spec — updating existing sections in place, adding new sections, removing obsolete sections — and stamp every touched section with a `<!-- rev: run-N YYYY-MM-DD -->` marker.

**Inputs:** updated inputs / analyses / research, current spec, current `.progress.json > last_finalised_at`.

**Outputs:** updated spec with revision markers on touched sections; downstream stages use these markers to scope rerun work.

**Used by:**
- `framework/agents/requirements-finaliser/agent.md` — on rerun branches.
- `framework/agents/design-spec-finaliser/agent.md` — on rerun branches.

**Used how:** Called by finalisers during rerun. Distinct from `reconcile.md` (which handles in-cycle Q&A reconciliation); this skill handles cross-cycle / brownfield deltas.

> Content TBD per `plan/v7b-Brief.md > §Reconciliation model` + §Rerun detection > "rerun branches".
