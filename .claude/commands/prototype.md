---
description: Generate a hi-fi, clickable, client-side prototype of a scope of requirements.md inside one shared app — selectable UX posture, full traceability, single landing page.
---

Launch the prototype orchestrator at `framework/orchestrators/prototype-orch.md`.

Follow the orchestrator exactly — one run produces **one** prototype, accumulating in the shared `prototypes/` app:

1. Capture scope (`scope-selector`) + the prototype name, detect prior prototypes, select optional inputs (`select-prototype-inputs`), and (if needed) author the blueprint (`blueprint-architect`, blueprint-only mode).
2. Capture purpose + UX posture + trade-off positions.
3. `framework/agents/prototype-spec-drafter.md` — wait for the design-spec draft.
4. `framework/agents/prototype-spec-resolver.md` — resolve the AI-suggestions. **Skipped on the fast path** (zero AI-suggestions — often the case on the posture/wireframe-seeded path).
5. `framework/agents/prototype-spec-merger.md` — wait for the finalised design spec. Standard path: accepted via the merger's accept/edit/reject loop. Fast path: finalised mechanically with **no** spec-accept (you accept the finished prototype once, at the end).
6. Scaffold the shared app once (`framework/agents/prototype-app-scaffolder.md`) if not already scaffolded — this is where the brand **and colour mode** are captured and locked: a `design-system/design-system-light.html` and/or `-dark.html` (surfaced as the Brand source at input selection) themes the app, and if none exists you're recommended to run `/design-system` first. When **both** mode files exist you're asked how users switch between light and dark (a button in the UI / OS setting only / no switching / something else); with only one, that mode is used and nothing is asked.
7. `framework/agents/prototype-generator.md` — generate the prototype (parallel per-surface), then verify (lint + typecheck + build + Playwright smoke).
8. `framework/agents/prototype-landing-updater.md` — list the prototype on the single landing page.

Honour every handback gate and refusal predicate (`RF-04`, `RF-10`..`RF-13`) defined in the orchestrator. Do not perform any task not listed in the orchestrator. Outputs live under `prototypes/` (the Next.js app + landing) and `prototypes/.specs/<name-slug>/` (the design spec); the shared blueprint lives under `blueprints/<scope-slug>/`.
