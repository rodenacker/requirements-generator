# Extractor golden fixtures

Frozen resolutions that prove the source-model shapes the Stadium extractor depends on, so a future
maintainer can re-verify them **without** the out-of-repo corpus (`C:\Stadium 6 Web Apps`). Regenerate
with `python framework/tools/_probe_execpath.py [--app <folder> --script <name> --out <file>]` (the probe
builds its own id-index straight off the `.sapz`, independently of `read_design_model`, so it is an
oracle, not a mirror). These seed the Phase-2c regression harness.

| File | Source app (corpus GUID) | Script | Proves |
|---|---|---|---|
| `execpath-memberadmin-memberupdate-load.json` | MemberAdmin (`785d3104-…`) | `MemberUpdate.Load` | `Script → ExecutionPath → props["Actions"]` = the **10 ordered** root actions (linear, no branches). The Phase-1 `1a` acceptance oracle. |
| `execpath-rmb-onboarding-btnnext-click.json` | RMB_Onboarding (`87ea91de-…`) | `btnNext.Click` | Branch shape: `Decision.Decision → ExecutionPaths → IfPath{Conditions,Actions}` + a trailing `ExecutionPath` else-branch (`ShowElse=True`). The validation-fail `Notification` lives **inside** the else branch (the flat DFS scrambles it after the happy-path navigate). |

`timing-sample.ndjson` is unrelated (a pipeline timing sample).
