# v7b-test — Requirements + Design-System pipelines

Two consultant-driven pipelines, each invoked by its own slash command:

- **`/requirements`** — turns client inputs into a structured `requirements.md`. `requirements-orch` runs `requirements-input-handler` → `requirements-drafter` → `requirements-resolver` → `requirements-merger` in foreground, gating each transition on an explicit handback.
- **`/design-system`** — stand-alone styler. Asks the consultant for a domain (curated list + free-text) and an optional reference URL, extracts brand tokens from the URL's CSS where possible, and fills the rest from `framework/assets/domain-defaults/{{domain}}.md`. Writes `design-system/design-system.md` with provenance markers per token. Does not read `requirements/` or any other agent's output — the two pipelines are isolated.

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

### `/requirements`

1. Drop input documents into `input/`. Supported tiers:
    - **Native-text** — `.md`, `.txt`, `.drawio`, `.yml`, `.yaml`, `.xml`. Read directly.
    - **Native-multimodal** — `.png`, `.jpg`, `.jpeg`, `.gif`, `.webp`. Read directly via Claude's multimodal vision.
    - **Supported-via-MCP** — `.docx`, `.xlsx`, `.pptx`, `.pdf`. Converted to a sibling `*.converted.md` via markitdown.
    - **Unsupported** — everything else. Recorded in the manifest for forensic record; not read.
2. Invoke the pipeline: `/requirements`.
3. The orchestrator runs the four agents in order. The consultant is prompted only at acceptance gates and at refusal pauses (see `framework/shared/refusal-registry.md`).

### `/design-system`

Stand-alone — no `input/` files needed.

1. Invoke the styler: `/design-system`.
2. The orchestrator detects any prior `design-system/design-system.md` and prompts overwrite / keep / cancel.
3. The styler agent asks for a **domain** (pick from the seven curated values — `retail-banking`, `education-saas`, `healthcare-booking`, `internal-tooling`, `ecommerce`, `fintech-consumer`, `government-services` — or type your own as free-text) and an **optional reference URL**.
4. With a URL: WebFetch two-pass (homepage → primary stylesheet, framework-exclusion rules applied), extract colours/typography/effects from the CSS, fill any unset tokens from the domain defaults.
5. Without a URL: every token is filled from the domain defaults.
6. Output: `design-system/design-system.md` with frontmatter (provenance metadata), human-readable Extraction Summary tables (Source Context + Provenance per token), and machine-readable Brand sections.

## Layout

```
v7b-test/
├── .mcp.json                                 # MCP server declarations (markitdown)
├── README.md                                 # this file
├── input/                                    # consultant-dropped client docs (used by /requirements only)
├── requirements/                             # /requirements outputs
│   ├── source-manifest.json                  # written by input-handler
│   ├── requirements-draft.md                 # written by drafter
│   ├── consultant-answers.md                 # written by resolver
│   └── requirements.md                       # written by merger
├── design-system/                            # /design-system output
│   └── design-system.md                      # written by design-system-styler
└── framework/
    ├── agents/                               # foreground agents (requirements-* + design-system-styler/)
    ├── orchestrators/                        # requirements-orch, design-system-orch
    ├── skills/                               # reusable verbs (preflight, classify, convert, verify, etc.)
    ├── shared/                               # general-rules, prototype-scope, prototype-invariants, refusal-registry, setup-instructions/
    ├── assets/                               # template-requirements, template-design-system, characters/, domain-defaults/, taxonomies, glossary
    └── state/                                # .progress.json + agent working sidecars (requirements pipeline only)
```
