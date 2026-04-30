<!-- ROLE: skill. STATUS: stub — author during phase-1 build-order step 2 or 6. -->

# commit-and-clear.md

**Purpose:** Checkpoint subroutine — commit artifacts under `artifacts/<stage>/` with the convention `[stage] sub-step: summary` and prompt the consultant to `/clear` before proceeding to the next stage. Non-blocking git wrapper.

**Inputs:** stage name, sub-step name, files to include in the commit.

**Outputs:** git commit; consultant-facing message naming the next command.

**Used by:**
- `framework/orchestrators/requirements-orch.md` — after Accept + finalise.
- `framework/orchestrators/design-orch.md` — after Accept + finalise.
- `framework/orchestrators/style-orch.md` — after style artifacts produced.
- `framework/workflows/checkpoint.flow.md` — primary subroutine.

**Used how:** Never auto-`/clear`s the conversation; prompts the consultant to do it. Never auto-chains the next stage.

> Content TBD per `plan/v7b-Brief.md > §Approach > skills` + §Risks #3.
