# Requirements Generator

## Contents

- [1. Overview](#1-overview)
- [2. How to use this repo](#2-how-to-use-this-repo)
- [3. When to use which command](#3-when-to-use-which-command)
- [4. Commands](#4-commands)
    - [`/start`](#41-start)
    - [`/ingest-stadium`](#42-ingest-stadium)
    - [`/design-system`](#43-design-system)
    - [`/generate-prd`](#44-generate-prd)
    - [`/requirements`](#45-requirements)
    - [`/analyse-inputs`](#46-analyse-inputs)
    - [`/review-inputs`](#47-review-inputs)
    - [`/analyse-requirement`](#48-analyse-requirement)
    - [`/review-requirement`](#49-review-requirement)
    - [`/resolve-review`](#410-resolve-review)
    - [`/wireframe`](#411-wireframe)
    - [`/prototype`](#412-prototype)
    - [`/export-application`](#413-export-application)
- [5. Setup](#5-setup)
    - [5.1 First-time install](#51-first-time-install-one-off)
    - [5.2 Office & PDF inputs](#52-to-handle-word-excel-powerpoint-and-pdf-inputs)
    - [5.3 Tokens from a URL](#53-to-extract-design-tokens-from-a-reference-url)
    - [5.4 Prototypes](#54-to-generate-clickable-prototypes)
    - [5.5 Stadium apps](#55-to-ingest-stadium-6-apps)

## 1. Overview

Drop the client material you've been given into `input/`, run a slash command, and get back handoff-ready artefacts:

- Structured Requirements Document
- Product Requirement Document (PRD)
- Business or UX Design Analyses
- Business or UX Design Reviews
- Low-fi wireframes
- Clickable prototypes

Also generate a complete design system for brand-accurate prototype- and application-styling from a URL.

Used together, the commands turn a loose pile of client material into a comprehensive, traceable set of **frontend requirements** for building internal, enterprise-level **data-management applications**. The thirteen commands:

Here is a visual map of how the commands connect:<br>
**[system flowchart](https://rodenacker.github.io/requirements-generator/docs/requirements-generator-flow.html)**

## 2. How to use this repo

This repository is a **template**. You don't work in the shared copy — you create your own private copy from it, do your engagement work there, and take the generated assets onward. The framework itself (the `framework/`, `.claude/`, and `docs/` folders, plus the slash commands) is the product; you consume it, you don't edit it.

**It's proprietary** — company-internal only. Keep every copy you make **private**: never public, never shared outside the company.

**Start a new engagement**

1. **Create your own copy.** On the repository's GitHub page, click **Use this template → Create a new repository**. Name it for the engagement (e.g. `acme-loan-portal`) and set its visibility to **Private** (or **Internal**, per company policy). Make **one copy per client engagement** — don't reuse a copy across clients, so each client's material stays isolated and you start from a clean `input/`.
2. **Clone it to your machine** with `git clone <your-new-repo-url>`, then open the folder in VS Code.
3. **Install the tools** (first time on your workstation only). The fastest way is the bundled **setup script** — open a **PowerShell 7** terminal (`pwsh`) in the repo root and run it:

   ```powershell
   & framework/tools/setup-core.ps1           # check for, and install, the core dependencies
   & framework/tools/setup-core.ps1 -Probe    # only check what's present — installs nothing
   ```

   Run it **right after cloning**, before your first command; re-run it any time to check your setup. Unlike `/setup` (below), it runs in a plain terminal, so it also bootstraps a brand-new machine *before* Claude Code is fully configured. It installs the core dependencies every engagement needs — Python, Node.js, markitdown (Office/PDF conversion + its MCP server), the Mermaid CLI, and the Playwright MCP — and installs the npm-based tools **machine-globally**, so they're available to all your future engagements. After a fresh install, **restart Claude Code** so the new tools and MCP servers are picked up.

   The core script deliberately skips the optional diagram renderers (draw.io, Inkscape, LibreOffice) and the prototype's own packages. For those — and for the same setup driven from *inside* Claude Code via **`/setup`** — see [§5 Setup](#5-setup).

**Do the work**

4. **Add the client material** to the `input/` folder — briefs, decks, screenshots, spreadsheets, PDFs.
5. **Open Claude Code** in the VS Code side panel and run a command. Start with **`/start`** to pick from a menu, or run one directly. What each command does and when to reach for it is in [§3](#3-when-to-use-which-command) and [§4](#4-commands).
6. **Stay in the loop.** The commands are interactive — they draft, ask you to accept, and resolve anything they couldn't confidently fill in. Your answers shape the final artefacts.

**Take the assets onward**

7. **The outputs are your deliverables.** Each command writes to its own folder — `requirements/`, `prd/`, `analyse-requirements/`, `design-system/`, `wireframes/`, `prototypes/`, and the rest. Hand them to a client, a designer, or the next stage (e.g. an application-build framework). Use **`/export-application`** for a clean, dependency-free handoff of the finished spec.
8. **Leave the framework alone.** `framework/`, `.claude/`, `docs/`, and `CLAUDE.md` are the engine — your work belongs only in `input/` and the output folders. You're a consumer of the framework, not an editor of it.

**Getting a newer version.** Your copy is a point-in-time snapshot of the framework. Updates aren't applied in place — when you start your **next** engagement, take a fresh copy (step 1 again) and you'll have the current version. There's nothing to upgrade mid-engagement.

## 3. When to use which command

| Run                                                                       | When                                          | Result                                                                              |
| ------------------------------------------------------------------------------ | --------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| `/requirements`                                                                | Client just sent a pile of attachments                       | Turns inputs into a structured doc you can use for prototyping. Export with `/export-application` for Stadium 8.                          |
| `/ingest-stadium`                                                              | Client handed you a Stadium 6 low-code app, not just documents | Extracts the app into citation-ready assets under `input/` that `/requirements` and the other input commands then read like any other material. Run it before `/requirements`. |
| `/design-system`                                                               | Designer is waiting on a brand brief                                              | One run produces a complete colour + typography + effects brief for prototyping or Stadium 8.                 |
| `/generate-prd`                                                                | A stakeholder is asking for the *why* — problem, metrics, MVP phasing, risks      | Strategic PRD from the inputs.                               |
| `/review-inputs` → `adversarial`                                               | You want a tough critique of the raw inputs before drafting                       | Six-dimension critique of the raw input set — coverage, ambiguity, cross-source conflict, costly silences. |
| `/review-inputs` → `ten-ba-questions` or `ten-ux-questions`                    | You sense the raw inputs leave key BA or UX questions unanswered                  | Ranks the ten most consequential unanswered BA or UX questions, each sourced to a file. |
| `/review-requirement` → `adversarial`                                          | You need to defend the spec to a sceptical stakeholder                            | Strict critique with a Patch / Defer / Reject decision per finding.              |
| `/review-requirement` → `ten-ba-questions` or `ten-ux-questions`               | You sense something is missing in the spec but can't articulate it                | Surfaces the unasked questions in the consultant's blind spot.                   |
| `/analyse-inputs` → e.g. `thematic-analysis`, `journey-mapping`, `jtbd`        | You want to dig into the raw material before drafting                             | Pattern, journey, or motivation lens on the raw inputs. Re-feedable to `/requirements`. |
| `/review-inputs` → `completeness-review` or `gap-analysis`                     | You sense the raw inputs are thin, ambiguous, or contradictory                    | Authority-grounded or template-aligned punch-list before drafting.               |
| `/analyse-requirement` → `data-model`                                          | About to brief a developer on data structure                                      | Surfaces the entities, fields, and relationships the spec implies.       |
| `/analyse-requirement` → `crud-coverage`                                       | Worried a CRUD-heavy spec has forgotten operations or ungranted rights            | Matrix flagging missing create/read/update/delete paths and lifecycle holes.     |
| `/analyse-requirement` → `ooux` or `use-cases`                                 | About to brief a designer on screens and navigation                               | Surfaces the objects + CTAs, or the actor goals + flows.                         |
| `/resolve-review`                                                              | You've run a review and want its findings *acted on*, not just listed             | Walks the findings with you and writes your approved resolutions into `input/`.  |
| `/wireframe`                                                                   | You want to show 2–3 divergent screen options before committing to a high-fi mock | Low-fi HTML variants tied to requirement IDs; compare side-by-side via tabs.     |
| `/prototype`                                                                   | You want something the client can actually click through, not just look at        | Hi-fi client-side React app on fixture data; brand-locked, UX diverges by posture. |
| `/export-application`                                                    | The spec is settled and a dev team outside this workspace needs the build-ready version | Strips the prototype scaffolding and stamps provenance — a clean handoff document. |

## 4. Commands

Every command runs interactively inside Claude Code and keeps you in the loop. A few behaviours are shared, so they're stated once here rather than repeated per command:

- **Two interaction patterns.** The *document* pipelines (`/requirements`, `/generate-prd`, and `/prototype`'s design spec) follow **draft → you accept → Q&A on anything the system couldn't confidently fill in → merge → you accept**. The *lens* pipelines (`/analyse-inputs`, `/analyse-requirement`, `/review-inputs`, `/review-requirement`) follow **pick a methodology → it runs → you accept → saved under its own folder**. (`/export-application` is simpler still: **one transform → you accept** — no Q&A, nothing generated. `/resolve-review` is its own shape: **pick a review → pick findings → resolve each with you → you accept**.)
- **Read-only.** Analyses and reviews only *read* your inputs or spec — they never modify or delete them. Files you drop in `input/` are removed only by you, manually.
- **Re-runs are safe.** Each pipeline detects a prior run and offers to **continue**, **start fresh**, or **overwrite** — the prior work is committed to git first, so nothing is lost. Run a lens pipeline again to add another artefact alongside the first.
- **Input file types** (for the commands that read `input/` — `/requirements`, `/generate-prd`, `/analyse-inputs`, `/review-inputs`): text (`.md`, `.txt`, `.drawio`, `.yml`, `.yaml`, `.xml`) and images (`.png`, `.jpg`, `.jpeg`, `.gif`, `.webp`) are read directly; Office and PDF (`.docx`, `.xlsx`, `.pptx`, `.pdf`) are converted first (needs markitdown — see §5.2); anything else is logged so it doesn't slip through silently.

The [system flowchart](https://rodenacker.github.io/requirements-generator/docs/requirements-generator-flow.html) linked above gives the visual map and a deeper per-methodology description.

### 4.1 `/start`

Run it inside Claude Code to pick from a menu instead of remembering command names — it lists the commands with their one-liners and launches the one you select.

### 4.2 `/ingest-stadium`

Turn a **Stadium 6 application** into inputs the other commands can read. When a client hands you a deployed Stadium low-code app instead of (or alongside) documents, drop it into `input/` — either the deployed app folder or a one-line `*.stadium` pointer file naming its path — and run this first. It extracts the app **once** into a set of lean, citation-ready requirement assets that `/requirements`, `/generate-prd`, `/analyse-inputs`, and `/review-inputs` then consume like any other input material.

Each app is processed once — a ledger records what's already been ingested, and re-ingesting is a deliberate, prompted choice — so your hand-edits to the extracted assets are never silently overwritten. The raw app folder itself is left out of every other command's input set; only the extracted assets are read (the other input commands nudge you to run this if they spot an un-ingested app). Runs a bundled Python extractor — see §5.5.

**You get** `input/<AppName>.stadium-assets/` — thirteen per-app assets (eleven deterministic category files covering the data model, sources, business rules, access control, surfaces, per-view user tasks, navigation, and more, plus two advisory ones), ready to be picked up on the next `/requirements` (or `/generate-prd` / `/analyse-inputs` / `/review-inputs`) run.

### 4.3 `/design-system`

A brand-token brief for a designer in one run — useful when the designer is blocked on visual direction and you need to send something concrete today. Two questions on launch: a required **Domain** (free text, e.g. `loan-origination-portal` — the token set is inferred per-run, no fixed lookup table) and an optional **Reference URL** (a real browser opens at desktop size and extracts the actual colours, typography, and effects from the live CSS; without one, every token is inferred from the domain string alone).

**You get** `design-system/design-system.html` — a self-contained document you open via `file://`: colour swatches, type specimens at their actual sizes, shadow/motion samples, and contrast-validation pairs, each token annotated with its provenance (*extracted from the URL* vs *inferred from the domain*). It also embeds a machine-readable token JSON block, so a downstream tool (Figma plugin, CSS generator, LLM pipeline) can consume the values directly.

### 4.4 `/generate-prd`

A strategic, human-audience PRD from the same client inputs — problem framing, success metrics, hypotheses, MVP phasing, risks, stakeholders. Run it when a sponsor needs the *why* (not the *what-the-FE-must-do* that `/requirements` produces). Fully independent of `/requirements` — run it before, after, or alongside, with no state collision.

**You get** `prd/prd.md`. Citation IDs are namespaced (`PC-NNN` / `PAI-NNN`) so the PRD never visually collides with a requirements doc you run alongside it.

### 4.5 `/requirements`

Turn the loose pile of client material into a clean, structured requirements spec. Drop the files into `input/` first, then run it.

**You get** `requirements/requirements.md` — a structured spec where every item is traceable either to something you provided or to a domain-default rule the framework applies (e.g. accessibility, security, error-handling). Anything the system can't confidently fill in is resolved through the Q&A, so the final doc reads as a clean, signed-off spec.

### 4.6 `/analyse-inputs`

Go deeper into the raw inputs *before* drafting: pick an analytical lens and the framework re-expresses your `input/` material through it as a stand-alone artefact. Each one is designed to be **copied back into `input/`** so `/requirements` consumes it on the next run. Requires a non-empty `input/`; shares the source manifest with `/requirements`.

| If you want to see…                                                                                                                | Pick                          | What it's called                  |
| ---------------------------------------------------------------------------------------------------------------------------------- | ----------------------------- | --------------------------------- |
| The **themes and patterns** the raw inputs already carry, with a coverage check against ten concern areas                          | `thematic-analysis`           | _Braun & Clarke thematic analysis_ |
| The **current-state user journey** described in the inputs, per persona, with sentiment curve and pain points                      | `journey-mapping`             | _NN/G journey map_                |
| What **users are actually trying to get done** in the inputs — jobs, outcomes, forces of progress (push / pull / anxiety / habit)  | `jtbd`                        | _Jobs-to-be-done (JTBD-X)_        |
| The **canonical objects, attributes, relationships, and CTAs** across all sources, with synonym-merge and an ERD                   | `ooux`                        | _Sophia Prater's ORCA process_    |
| The **cross-functional process** with swim-lanes per actor and a Disconnect Register flagging the white-space gaps                 | `swim-lane-process-mapping`   | _Rummler-Brache swim-lane map_    |
| A **hierarchical task decomposition** of user goals — sub-goals, operations, Plans, and per-terminal data nouns                    | `task-analysis`               | _Hierarchical Task Analysis (HTA)_ |
| An **outcome → opportunity → solution → assumption-test tree** seeded with candidate-requirement bridges                           | `opportunity-solution-trees`  | _Teresa Torres OST_               |
| A **bottom-up affinity map** — atomic notes clustered into super-themes via a two-pass re-cluster with drift detection             | `affinity-mapping`            | _KJ-method affinity diagram_      |
| One **agreed vocabulary** for the engagement — terms classified domain vs application, defined from the inputs, maturity-rated, with proposed definitions for the loose ones | `glossary`                    | _ubiquitous-language glossary_    |
| The **actor and end-user goals** behind the request — stated and inferred — as a goal register with an AND/OR refinement tree, an actor map, and a conflicts table | `user-goal-analysis`          | _Goal-Oriented Requirements (GORE)_ |
| The **enterprise motivation** behind the request — business problem → need → goal → problem-statement in one causal chain (the strategic *why*, not actor-level goals) | `business-context-definition` | _OMG BMM / BABOK business context_ |

**You get** one artefact per run under `analyse-inputs/<METHOD>/`, mostly self-contained HTML that survives a markitdown HTML→MD round-trip (the embedded JSON / YAML / Mermaid bodies are the load-bearing re-ingestion contract).

### 4.7 `/review-inputs`

Find what's missing or wrong in the raw inputs *before* you draft — a punch-list you act on before `/requirements` runs. Use it when the inputs feel thin, ambiguous, or contradictory.

| If you want to see…                                                                                                                                                                  | Pick                  |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------- |
| A **six-dimension critique** of the raw input set — stakeholder & role coverage, ambiguity, cross-source conflict, silence-with-downstream-impact, quantitative and scope signals     | `adversarial`         |
| An **authority-grounded completeness sweep** (IEEE 29148 / Volere / BABOK / Wiegers / ISO 25010) across ten dimensions, with stakeholder elicitation questions per finding           | `completeness-review` |
| The **lexical, syntactic, referential, vague, subjective, weak-verb, and optionality ambiguities** (Berry/Kamsties + Femmer) with ready-to-paste elicitation questions per finding   | `ambiguity-review`    |
| A **template-bijection gap delta** measured against the drafter's own template, with a shall-form Candidate Requirement per Must/Should gap ready for `/requirements` re-ingestion   | `gap-analysis`        |
| The **ten most consequential business-analysis questions** the raw inputs leave unanswered, ranked by business impact across eight BA gap categories, each sourced to a file or marked absent-from-corpus | `ten-ba-questions`    |
| The **ten most consequential UX-discovery questions** the raw inputs leave unanswered, ranked by design impact across eight UX gap categories (users, context, goals, task flows, supporting data, errors, collaboration, trust) | `ten-ux-questions`    |

**You get** one self-contained HTML artefact per run under `review-inputs/<METHOD>/`; `gap-analysis.html` additionally carries an inline-SVG coverage heatmap and is designed to be copied back into `input/` so `/requirements` picks up its shall-form Candidate Requirements on the next run.

### 4.8 `/analyse-requirement`

Go deeper into what your requirements doc already contains: pick a lens and the framework re-expresses `requirements.md` through it as a stand-alone artefact you can share with a designer or developer.

| Pick                            | What it's called                | If you want to see…                                                                                                            |
| ------------------------------- | ------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| `ooux`                          | _object map_                    | The **things** in your spec (customers, accounts, applications) and what users can do with each                                |
| `jtbd`                          | _jobs-to-be-done_               | What **users are actually trying to get done** — their jobs and the outcomes they want                                         |
| `use-cases`                     | _use cases_                     | **Each user's goals** and the step-by-step flows they take to reach them                                                       |
| `data-model`                    | _logical data model_            | The **data structure** — what records exist, what fields they have, how they relate, plus optional ERDs                        |
| `crud-coverage`                 | _CRUD coverage matrix_          | Whether **every entity has create / read / update / delete coverage** — a matrix flagging forgotten operations, lifecycle holes, and rights granted but never delivered |
| `sequence-diagram`              | _UML sequence diagram_          | **How the parts of the system talk** to each other across a scenario (front-end ↔ back-end ↔ external services)                |
| `state-diagram`                 | _UML state diagram_             | The **lifecycle of a record** — what statuses it moves through and what triggers each transition                               |
| `activity-diagram`              | _UML activity diagram_          | A **multi-actor process flow** with branches, parallel paths, and who does what                                                |
| `user-journeys`                 | _user journey map_              | The **user's experience phases** with pain-points and opportunities at each step                                               |
| `task-flows`                    | _task flows_                    | The **goal-decomposition and step-by-step paths** users take, ready for wizards / form sequences                               |
| `opportunity-solution-trees`    | _opportunity-solution tree_     | Whether the doc's **features ladder up to its outcomes**, and where unaddressed opportunities or missing assumption-tests sit  |
| `mvp-slicing`                   | _user-story map + MoSCoW board_ | **Where to draw the MVP line** — what ships first and what waits — as a user-story map with a proposed release slice, paired with a MoSCoW priority board |
| `five-whys`                     | _five-whys_                     | Whether each requirement's **rationale chain** drills down to a user goal, business driver, or external mandate                |
| `glossary`                      | _glossary_                      | An alphabetical, **citation-bound vocabulary inventory** before designing copy, labels, status pills, or role surfaces         |
| `trade-off-dimension-analysis`  | _trade-off-dimension matrix_    | Each user goal scored against **UX trade-off dimensions** (Speed vs Accuracy, Simplicity vs Power, Automation vs Control, …)   |

**You get** one HTML artefact per run under `analyse-requirements/<METHOD>/` (e.g. `OOUX/ooux-object-map.html`, `FIVE-WHYS/five-whys.html`) — formatted to share directly with whoever needed the insight.

### 4.9 `/review-requirement`

Find what's missing or wrong in the spec *before* you hand it over — a second pair of eyes before estimation, a design brief, or a sceptical stakeholder.

| Pick                | If you want to see…                                                                                                                |
| ------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| `ten-ba-questions`  | The **stakeholder questions** the spec hasn't yet answered — questions an experienced BA would ask before design or estimation     |
| `ten-ux-questions`  | The **design-blocking gaps** an experienced UX designer would flag before they start designing                                     |
| `adversarial`       | A **strict critique** of what's wrong, with a Patch / Defer / Reject decision per finding so you know what to do about each        |
| `first-principles`  | Whether each requirement is **defensible against business rationale**, so weak items get cut or strengthened before design         |
| `user-stories`      | Which **user stories aren't ready** for design or estimation, so they can be reworked before they enter the backlog                |
| `requirements-quality` | Whether **every requirement is well-formed** against the ISO 29148 standard (singular, unambiguous, verifiable, conforming, complete) — a per-characteristic heatmap with EARS-form rewrites for the ambiguous and compound ones |
| `requirements-traceability` | Which facts **trace to a real source** (or an accepted AI-suggestion) and which **trace to nothing** — orphans, broken citations, and dropped content that leaked through |

**You get** one HTML artefact per run under `review-requirements/<METHOD>/` (e.g. `ADVERSARIAL/adversarial-review.html`). Treat it as a punch-list: fix the findings you accept in `requirements.md`, then re-run for a fresh pass.

### 4.10 `/resolve-review`

Turn the findings of a review you've already run into something the pipeline can consume. A review artefact is a punch-list; this command walks you through acting on it — you pick the review (any `/review-inputs` or `/review-requirement` artefact on disk), pick which findings to address, and resolve each one in turn. Anything the system infers on your behalf is confirmed with you by an explicit affirmative before it's recorded — per finding, or in one go via an explicit *Accept all remaining as drafted* choice — nothing is silently assumed. The approved resolutions are then written as a **new dated document into `input/`** (existing input files are never modified or overwritten), so the next `/requirements` run ingests your decisions like any other client material.

When the review you picked critiques the *spec* (a `/review-requirement` artefact) rather than the raw inputs, the command additionally offers — opt-in — to cache the same resolutions as a transient **Amendments** section inside `requirements.md`, so downstream commands can use them immediately. The cache is temporary by design: the next `/requirements` re-merge regenerates the doc and folds the resolutions in properly from `input/`.

**You get** one new `input/<review-name>-<date>.md` per run — a consultant-approved resolutions document in which every resolution is marked as stated by you or AI-inferred-and-confirmed by you. One run resolves one review; re-run it for another (the output files accumulate side-by-side).

### 4.11 `/wireframe`

2–3 parallel low-fi HTML wireframe variants for a scope of `requirements.md`. Each variant adopts a divergent position on a UX trade-off dimension (density vs focus, speed vs accuracy, automation vs control, …), is bound to a persona, and traces every interactive element back to a requirement ID. You scope the run and optionally pick supporting analyses you've already produced via `/analyse-requirement` (only ones actually on disk are offered); the variants then generate in parallel, so a 2-variant scope takes about the same wall time as one.

**You get** `wireframes/<scope-slug>/` — a metadata-only `index.html` landing (side-by-side variant columns of screen links plus a trade-off matrix that explains *why* the variants differ) and per-screen HTML files carrying `data-src` (requirement ID) and `data-prop` (data-shape) traceability. Open the landing, click a screen link to open it in a new tab, then drag tabs into separate windows to compare directly.

### 4.12 `/prototype`

One clickable, client-side hi-fi prototype of a scope of `requirements.md` per run, accumulating in a **single shared React/Next.js app** under `prototypes/`. The look and feel is **brand-locked and identical across every prototype** (one theme — from `/design-system` if you've run it, otherwise defaults you confirm); what differs is pure UX — a named posture plus trade-off positions reshape the layout and workflows. You scope and name the run, optionally seed it from an analysis or a wireframe variant (a wireframe basis pre-fills the posture and positions), then pick the posture and positions. It runs entirely in the browser against fixture data — there is no backend.

**You get** a shared Next.js app under `prototypes/`: a landing page (`src/app/page.tsx`) listing every prototype grouped by scope, the clickable routes for this one (`src/app/<name-slug>/`), and shared theme / components / fixtures that grow additively across runs. Run `npm run dev` inside `prototypes/` and open the landing — a role switcher and a data-reset control are built into the chrome, so you can hand the running app to a client to click through. (The first run scaffolds the app and runs `npm install` once; later runs reuse it and are much faster.)

### 4.13 `/export-application`

Export the finished spec as an **application-audience document** you can hand to a dev team outside this workspace. Run it once the requirements have settled — after the analyses, reviews, wireframes, and any manual refinements have shaped `requirements.md` into what you actually want built. It's a pure export of the spec **as it exists at that moment**: nothing is generated or invented at export time. The prototype-only scaffolding is removed (the prototype-invariants appendix), fixture references become backend-contract pointers (with a placeholder path to rebind once a backend requirements document exists), and a provenance block is stamped in — including a fingerprint of the exact `requirements.md` version it came from, so a re-run can tell you whether the export is stale. The architectural implications, session-policy, performance-budget, and rationale content is already in the spec (drafted and confirmed during `/requirements`) and carries through untouched.

**You get** `export-application/requirements-application.md` — self-describing for external readers (a citation legend explains every traceability marker). Hand it over together with `requirements/draft-claims.ndjson`, which holds the verbatim source quotes behind the citation tags. Re-running after the spec changes offers a one-click regenerate; the prior export is checkpointed to git first.

## 5. Setup

Install once on your workstation. Versions below are floors — newer is fine.

**Fastest path — run `/setup`.** It detects, installs (user-scoped, so a fresh repo clone never re-installs), configures, and tests everything below in one go, then prints a status table and tells you if a restart is needed. Run `/setup` for the full core set, or target one piece with e.g. `/setup markitdown`. The manual steps in §5.1–§5.4 are the equivalents `/setup` runs for you, and double as troubleshooting.

### 5.1 First-time install (one-off)

The three pieces every command needs:

- **Claude Code** — the runtime everything runs under. Install from <https://claude.com/claude-code> and sign in. The slash commands are picked up automatically from `.claude/commands/` in this repo.
- **VS Code + Claude Code extension** — your editor while a command is running. Install VS Code from <https://code.visualstudio.com/>, then add the **Claude Code** extension from the marketplace. The extension lets you launch Claude Code in a side panel and run slash commands without leaving the editor.
- **git** — used to safely checkpoint a prior run before it gets reset (so nothing is ever lost). Install from <https://git-scm.com/>. Verify with `git --version`.

### 5.2 To handle Word, Excel, PowerPoint, and PDF inputs

Needed for any command that reads `input/` (`/requirements`, `/generate-prd`, `/analyse-inputs`, `/review-inputs`) when your client sends Office or PDF files (typical). Easiest: `/setup markitdown`. Manually: install **Python 3.10+** (<https://www.python.org/>; verify with `python --version`), then install **markitdown with its Office/PDF converters** plus the MCP server:

```
pip install "markitdown[docx,pptx,xlsx,xls,pdf,outlook]"
pip install --no-deps markitdown-mcp==0.0.1a4
pip install "mcp~=1.8.0"
```

The scoped extras are what make `.pptx`/`.xlsx`/`.xls`/`.pdf` convert — bare `markitdown-mcp` handles only `.docx`. The `--no-deps` avoids a dependency conflict on newer Python; see `framework/shared/setup-instructions/markitdown.md` for why. Restart Claude Code afterwards so the converter picks up.

Without it, the input-reading commands still work on plain text, YAML/XML, .drawio diagrams, and images. They only stop if they actually encounter a `.docx`, `.xlsx`, `.pptx`, or `.pdf` in your inputs — and then they tell you exactly what to install and resume after you do.

Setup notes and troubleshooting: `framework/shared/setup-instructions/markitdown.md`.

### 5.3 To extract design tokens from a reference URL

Needed only for `/design-system` when you want it to pull colours/typography from a live website (instead of inferring everything from the domain string). Install **Node.js 20+** (<https://nodejs.org/>; verify with `node --version`), then prime the browser-driver:

```
npx -y @playwright/mcp@0.0.76 --help
```

Restart Claude Code afterwards so the browser driver registers. The server is configured (in `.mcp.json`) to drive your **installed Google Chrome** (`--browser chrome`), so there's no separate browser binary to download.

Without it, `/design-system` still works — you just skip the reference URL when asked, and every token gets inferred from the domain string. If you do supply a URL without Playwright installed, the command offers a lower-fidelity web-fetch fallback or a clean exit while you install.

Setup notes and troubleshooting: `framework/shared/setup-instructions/playwright.md`.

### 5.4 To generate clickable prototypes

Needed only for `/prototype`, which scaffolds and builds a real Next.js app under `prototypes/`. Install **Node.js 20+** (<https://nodejs.org/>; verify with `node --version`) — the prototype app targets Next.js 16 / React 19, which need Node 20 or newer.

```
winget install OpenJS.NodeJS.LTS
```

The first `/prototype` run installs the app's dependencies (`npm install`) once inside `prototypes/`; the cost is amortised across every prototype you generate afterwards. The build-and-verify step also runs a Playwright smoke check, driven by a browser **already installed on your machine** (Chrome by default; set `PLAYWRIGHT_CHANNEL=msedge` to use Windows' preinstalled Edge) — no separate browser download. If no Chrome/Edge can be found, the command offers to skip the smoke check with a warning or tells you how to point it at a browser.

If Node.js is missing when you launch `/prototype`, the command tells you exactly what to install and resumes at the scaffold step after you do.

Setup notes and troubleshooting: `framework/shared/setup-instructions/node-toolchain.md`.

### 5.5 To ingest Stadium 6 apps

Needed only for `/ingest-stadium`, which runs a bundled Python extractor over a Stadium app dropped in `input/`. The extractor is **standard-library only** — there are no packages to install — so if you already installed **Python 3.10+** for Office/PDF inputs (§5.2), you're done. Otherwise install Python (<https://www.python.org/>; verify with `python --version`), or run `/setup python`.

If Python is missing when you launch `/ingest-stadium`, the command tells you exactly what to install and resumes after you do.

Setup notes and troubleshooting: `framework/shared/setup-instructions/stadium.md`.
