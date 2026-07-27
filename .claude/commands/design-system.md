---
description: Run the design-system styler (URL → suggested domain → design tokens) end-to-end.
---

Launch the design-system orchestrator at `framework/orchestrators/design-system-orch.md`.

Follow the orchestrator exactly — run the single agent in the prescribed foreground:

1. `framework/agents/design-system-styler.md` — wait for the design-system document to be accepted.

Honour the startup gate (overwrite / keep / cancel) and the handback gate defined in the orchestrator. Do not perform any task that is not listed in the orchestrator. The agent is stand-alone — it does not read `requirements/`, `framework/state/`, or `framework/shared/`.

**Colour modes.** After extraction, step-05b asks which colour mode(s) to ship — **light only / dark only / both** — and names the scheme it actually found, because a reference URL ships a dark palette as readily as a light one. Whichever scheme was extracted is the **hue source**; the other mode is *derived* from the same brand hues, never separately extracted. The hue-source file is always written (it is the grounded record and the derivation seed) alongside whatever was asked for, and it carries `meta.primary: true` — so asking for one mode against a site in the other scheme legitimately produces two files, and the run says so.

The final artefacts are `design-system/design-system-light.html` and/or `design-system/design-system-dark.html` — one self-contained, single-mode HTML file per mode, each with an embedded `<script type="application/json" id="design-tokens">` block (LLM-readable) and visual sections (swatches, type specimens, shadow / motion / contrast pairs) for consultant review via `file://`. There is no in-document mode switcher and no combined file; the retired unsuffixed `design-system.html` is only recognised for cleanup.
