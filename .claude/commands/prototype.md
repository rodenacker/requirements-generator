---
description: Generate a hi-fi, clickable, client-side prototype of a scope of requirements.md inside one shared app — selectable UX posture, full traceability, single landing page.
---

Launch the prototype orchestrator at `framework/orchestrators/prototype-orch.md`.

Follow the orchestrator exactly — one run produces **one** prototype, accumulating in the shared `prototypes/` app:

1. Capture scope (`scope-selector`) + the prototype name, detect prior prototypes, select optional inputs (`select-prototype-inputs`), and (if needed) author the blueprint (`blueprint-architect`, blueprint-only mode).
2. Capture purpose + UX posture + trade-off positions.
3. `framework/agents/prototype-spec-drafter.md` — wait for the design-spec draft.
4. `framework/agents/prototype-spec-resolver.md` — resolve the AI-suggestions (often none on the posture/wireframe-seeded path).
5. `framework/agents/prototype-spec-merger.md` — wait for the finalised design spec to be accepted.
6. Scaffold the shared app once (`framework/agents/prototype-app-scaffolder.md`) if not already scaffolded.
7. `framework/agents/prototype-generator.md` — generate the prototype (parallel per-surface), then verify (lint + typecheck + build + Playwright smoke).
8. `framework/agents/prototype-landing-updater.md` — list the prototype on the single landing page.

Honour every handback gate and refusal predicate (`RF-04`, `RF-10`..`RF-13`) defined in the orchestrator. Do not perform any task not listed in the orchestrator. Outputs live under `prototypes/` (the Next.js app + landing) and `prototypes/.specs/<name-slug>/` (the design spec); the shared blueprint lives under `blueprints/<scope-slug>/`.
