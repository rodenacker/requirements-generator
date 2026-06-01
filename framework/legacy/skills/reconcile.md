<!-- ROLE: skill. STATUS: stub — author during phase-1 build-order step 5. -->

# reconcile.md

**Purpose:** Fold Q&A answers and resolution decisions back into the in-progress spec, in place. Mutates the draft so it always reflects current truth; no parallel change log.

**Inputs:** answers from `run-qa-level1.md` / `run-qa-level2.md`, current spec.

**Outputs:** updated spec; invalidated `completeness_hash` in `.progress.json` (forces a fresh completeness report before next Accept).

**Used by:**
- `framework/agents/requirements-qa/agent.md`.
- `framework/agents/design-qa/agent.md`.

**Used how:** Called after each Q&A pass. Pairs with `reconcile-delta-into-spec.md` (the rerun-flow variant).

> Content TBD per `plan/v7b-Brief.md > §Reconciliation model (in-spec only)`.
