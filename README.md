# v7b-test — Requirements pipeline

A consultant-driven pipeline that turns client inputs into a structured `requirements.md`. The MVP scope is the requirements stage: `requirements-orch` runs `requirements-input-handler` → `requirements-drafter` → `requirements-resolver` → `requirements-merger` in foreground, gating each transition on an explicit handback.

## Prerequisites

- Claude Code (the harness this pipeline runs under).
- Python 3.10+ with `markitdown-mcp` installed for converting `.docx`/`.xlsx`/`.pptx`/`.pdf` inputs.

## Install

```
pip install markitdown-mcp==0.0.1a4
```

After install, restart Claude Code so the MCP server declared in `.mcp.json` is loaded. See `framework/shared/setup-instructions/markitdown.md` for verification and troubleshooting.

If `markitdown-mcp` is not installed, the pipeline still runs on `.md`/`.txt`/`.drawio`/`.yml`/`.yaml`/`.xml` and standalone images — the input-handler's preflight surfaces `RF-01 dependency_missing` only when an Office or PDF input is present.

## Run

1. Drop input documents into `input/`. Supported tiers:
    - **Native-text** — `.md`, `.txt`, `.drawio`, `.yml`, `.yaml`, `.xml`. Read directly.
    - **Native-multimodal** — `.png`, `.jpg`, `.jpeg`, `.gif`, `.webp`. Read directly via Claude's multimodal vision.
    - **Supported-via-MCP** — `.docx`, `.xlsx`, `.pptx`, `.pdf`. Converted to a sibling `*.converted.md` via markitdown.
    - **Unsupported** — everything else. Recorded in the manifest for forensic record; not read.
2. Invoke the pipeline: `/requirements`.
3. The orchestrator runs the four agents in order. The consultant is prompted only at acceptance gates and at refusal pauses (see `framework/shared/refusal-registry.md`).

## Layout

```
v7b-test/
├── .mcp.json                                 # MCP server declarations (markitdown)
├── README.md                                 # this file
├── input/                                    # consultant-dropped client docs
├── requirements/                             # pipeline outputs
│   ├── source-manifest.json                  # written by input-handler
│   ├── requirements-draft.md                 # written by drafter
│   ├── consultant-answers.md                 # written by resolver
│   └── requirements.md                       # written by merger
└── framework/
    ├── agents/                               # foreground agents (input-handler, drafter, resolver, merger)
    ├── orchestrators/                        # requirements-orch
    ├── skills/                               # reusable verbs (preflight, classify, convert, verify, etc.)
    ├── shared/                               # general-rules, prototype-scope, prototype-invariants, refusal-registry, setup-instructions/
    ├── assets/                               # template-requirements, taxonomies, glossary
    └── state/                                # .progress.json + agent working sidecars
```
