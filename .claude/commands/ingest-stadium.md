---
description: Extract a Stadium 6 application dropped in input/ into lean, citation-ready requirement assets the pipelines consume as ordinary inputs.
---

Launch the ingest-stadium orchestrator at `framework/orchestrators/ingest-stadium-orch.md`.

Follow the orchestrator exactly — run the single agent in the prescribed foreground:

1. `framework/agents/stadium-ingestor.md` — wait for the ingestor to report every detected Stadium application either extracted (or skipped / cancelled per the per-app re-ingest gate), and to hand control back.

Honour the per-app **re-ingest gate** (re-ingest / skip / cancel) and the handback gate defined in the orchestrator. Do not perform any task that is not listed in the orchestrator. The agent is stand-alone — it does not read or write `requirements/` state; it produces the per-app assets under `input/<AppName>.stadium-assets/` (plus the forensic `model.json` under `framework/state/stadium/<app-id>/` and the processed-ledger `framework/state/.stadium-processed.json`). Those assets are picked up as ordinary `Native-text` inputs by the next `/requirements` (or `/generate-prd` / `/analyse-inputs` / `/review-inputs`) run — this command does **not** build the source manifest.
