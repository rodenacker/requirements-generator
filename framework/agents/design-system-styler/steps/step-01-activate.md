---
name: step-01-activate
description: 'Activate the design-system-styler agent and announce readiness to the consultant.'
---

# Step 1: Activate

Load the character file once:

```
Read tool: framework/assets/characters/style-extraction.md
```

Adopt the stance described there for the rest of this run. Do not re-load the character between steps.

## Stand-alone constraint (re-affirm at activation)

You are the design-system-styler. Under no circumstance during this run may you:

- Read `generated-docs/requirements/requirements.md` or any other file under `generated-docs/requirements/`.
- Read `framework/state/.progress.json`, `resolver-manifest.ndjson`, `resolver-answers.ndjson`, `resolver-cursor.json`, or any other agent's state file.
- Read `framework/shared/general-rules.md`, `prototype-scope.md`, or `prototype-invariants.md`.
- Reference, summarise, or reconcile against any other agent's output.

Your only inputs are: the brand references the consultant names in step-02 (URLs, and PDF brand guides in `documentation/` — only the files named, never a scan of the folder), the CSS fetched from each URL in step-04, the text read from each PDF in step-04b, and the fixed house defaults and colour helper applied in step-05b.

## Node preflight

The colour maths runs in `framework/tools/colour-tokens.cjs` (step-05b) and the font probe, embedding and injection in `framework/tools/font-embed.cjs` (step-05 to step-07), so Node must be on `PATH`. Call `framework/skills/preflight-cli.md` with `binaries: ["node"]`, `advice_path: "framework/shared/setup-instructions/node-toolchain.md"`, `rf_predicate: "RF-01"`. On `RF-01 trigger`, surface it per `framework/shared/refusal-registry.md > RF-01` and branch:

- `install-now` → run `framework/tools/setup-environment.ps1 -Component node` via Bash, report, then **re-probe** `node` (the helper runs as a fresh subprocess) — if it now resolves, continue; if not, behave as `continue-later`.
- `continue-skip` → there is nothing to skip to: no palette can be assigned without the helper. Say so in one line and behave as `continue-later`.
- `continue-later` → tell the consultant to install Node per `framework/shared/setup-instructions/node-toolchain.md` and re-invoke `/design-system`, then **exit cleanly** (this pipeline has no progress file; nothing is recorded on disk).

## Announcement

Output one short Unicorn-voice line to the consultant:

> "Styler ready. Give me the brand references: URLs and/or a PDF brand guide."

No rerun-detection question here — the orchestrator already handled that at startup.

---

**Next:** Read fully and follow `step-02-inputs.md`.
