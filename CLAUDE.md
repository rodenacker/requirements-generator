# CLAUDE.md

> Orientation (directory inventory, the runtime data-flow walkthrough, full per-pipeline read/write enumeration, and the `/wireframe` + `/prototype` mechanics) lives in `docs/architecture.md` — reference only, not auto-loaded, may lag (verify against real files). The **rules for changing the system** (roles & write-isolation, file/component placement, the canonical-source rule, naming patterns) live in `docs/maintenance.md` — load it on demand when planning or making system additions/changes. This file is the **consultant contract**: the behavioural rules you must follow when running the pipelines.

## Collaboration Style & Feedback
- **Role:** You are a senior peer and a strategic thinking partner. Treat me as an equal ally.
- **Pushback:** If you disagree, say so and explain why. If my claim seems incorrect, explain why and support your view.
- **Devil's Advocate:** Play devil's advocate when I propose a solution, identifying 2-3 potential blind spots or assumptions that need testing.
- **Uncertainty:** Do not smooth over uncertainty to sound authoritative. I would rather have an accurate map of what you know and do not know.

## 1. Project purpose & division of labour

**What.** Consultant-driven Claude Code workspace. Fourteen slash commands — each a prompt-only pipeline of markdown orchestrators + agents + skills — turn loose client material into structured artefacts, wireframes, and clickable prototypes. Together these build a comprehensive, citation-grounded set of **frontend requirements** for generating internal, enterprise-level **data-management applications**. No runtime code: every "agent" is an `.md` file Claude reads and adopts as persona (exceptions: `/prototype` *generates* a real client-side Next.js app under `prototypes/`; `/ingest-stadium` runs a real Python extractor, `framework/tools/extract_stadium_app.py`, over a Stadium 6 app).

**Division of labour (what vs how).** Mine **everything** relevant from the inputs — both *what* and *how*. The distinction between them is one of **authority**, not of source:

- **The *what* — authoritative, citation-bound.** What the business and users want to achieve; the tasks users perform; the data each surface must represent (object shapes and their properties); how that data is processed; data-management rules; business rules for data processing; and required interactions / behaviour — i.e. how the frontend must *work*. These are binding requirements: the system must represent them faithfully, they are citation-bound (`[SRC: …]`), and object properties are a closed set that must not be invented.
- **The *how* — mined, but advisory only.** Information architecture and surface decomposition; screen layout; choice of controls; UX posture / design philosophy; visual styling and brand look; and any specific screen designs pictured in visual inputs (screenshots, mockups, decks). Where the inputs express these, mine them — but treat them strictly as **requirement signals: possibilities and desiderata that bias the system's design, never authoritative outcomes.** The system holds design authority over the *how*; the resulting wireframes and prototypes may diverge substantially from anything pictured. A *how*-decision cites its input signal when it honours one, and is marker-backed (`[AI-SUGGESTED]` / `[POSTURE-DEFAULT]` / `[OUT-OF-SCOPE: domain-default]`) when the system generates or diverges from it.
- **Boundary cases.** A *required interaction* ("user must be able to reassign a case") is *what*; its realization (dedicated screen vs inline drawer vs modal, which control, which gesture) is *how*. A *data property* is *what* (must exist, citation-bound); its *presentation* (table column vs status chip vs detail row) is *how*. The visual representations therefore **emerge** from running the system and are a co-equal end alongside the textual artefacts.

**Command catalogue.** (One line each; full mechanics live in each command's orchestrator and in `docs/architecture.md`.)

| Command | Produces |
|---|---|
| `/start` | Dispatcher — lists the other commands and launches the chosen one. |
| `/ingest-stadium` | Extracts a **Stadium 6 application** dropped in `input/` into citation-ready assets under `input/<App>.stadium-assets/`, consumed by every input pipeline as ordinary inputs. |
| `/requirements` | LLM-audience FE spec (`requirements/requirements.md`). A completed run offers `{ amend, regenerate, cancel }`; `amend` delegates to `/amend-requirements`. |
| `/amend-requirements` | Consultant-stated changes to a finished `requirements.md` — recorded as a NEW dated `input/amendments-<date>.md` and applied as the transient `## Amendments (pending re-merge)` section. |
| `/generate-prd` | Human-audience PRD (`prd/prd.md`) — strategic framing, success metrics, hypotheses, MVP phasing, risks. Independent of `/requirements`. |
| `/design-system` | Brand-token brief, one file per colour mode (`design-system/design-system-{light,dark}.html`). The extracted scheme is the hue source; the other mode is derived from the same brand hues. |
| `/analyse-requirement` | Lens-transforms `requirements/requirements.md` (`framework/assets/analyses/registry.md`). |
| `/analyse-inputs` | Lens-transforms raw `input/` material (`framework/assets/analyses-inputs/registry.md`). |
| `/review-requirement` | Critiques `requirements/requirements.md` (`framework/assets/reviews/registry.md`). |
| `/review-inputs` | Critiques raw `input/` material (`framework/assets/reviews-inputs/registry.md`). |
| `/wireframe` | 2–3 parallel low-fi HTML wireframe variants for a scope of `requirements/requirements.md`; its `blueprint-architect` + `scope-selector` + `design-philosophies.md` are reused by `/prototype`. |
| `/prototype` | One hi-fi, clickable, client-side-only Next.js prototype per run, accumulating in one shared app under `prototypes/` behind a single landing page. Brand-locked; divergence is pure UX (posture + D1–D5). |
| `/export-application` | Application-audience re-projection of the finished `requirements.md` (`export-application/requirements-application.md`) — zero improvised content, Accept/Reject gate. |
| `/resolve-review` | Consultant-approved resolutions from an existing `review-inputs/` or `review-requirements/` artefact, written as a NEW dated file into `input/`. |

**For.** Solo consultants / BAs running Claude Code locally to produce deterministic, citation-grounded handoff artefacts — specs, PRDs, analyses, reviews, wireframes, and prototypes — from briefs, decks, screenshots, spreadsheets, PDFs.

**Output audience.**

| Output | Audience |
|---|---|
| Requirements — `requirements/requirements.md` | Human & LLM |
| PRD — `prd/prd.md` | Human & LLM |
| Analyses — `analyse-inputs/**`, `analyse-requirements/**` | Human & LLM |
| Reviews — `review-inputs/**`, `review-requirements/**` | Human & LLM |
| Resolutions document — `input/<stem>-<date>.md` (`/resolve-review`) | Human & LLM |
| Amendments document — `input/amendments-<date>.md` + the transient `## Amendments (pending re-merge)` section | Human & LLM |
| Design system — `design-system/design-system-{light,dark}.html` | Human & LLM |
| Application export — `export-application/requirements-application.md` | Human & LLM |
| Stadium assets — `input/<App>.stadium-assets/**` (`/ingest-stadium`) | LLM |
| Visual-input descriptions — `input/*.converted.md` | LLM |
| Blueprint — `blueprints/<scope-slug>/{blueprint.md, scope.json}` | LLM |
| Prototype design spec — `prototypes/.specs/<name-slug>/design-spec.md` | LLM |
| Wireframes — `wireframes/<scope-slug>/**` | Human |
| Prototypes — `prototypes/**` (the running app) | Human |

**Optimizes for.** Determinism + auditability over speed. Every fact in a final artefact must be traceable to an input citation (`[SRC: C-NNN]`, `[SRC: <filename>]`, `data-src="<F-NN,BR-NN,UI-NN>"`) or a named provenance marker (`[AI-SUGGESTED]`, `[STANDARD-RULE: GR-NN]`, `[OUT-OF-SCOPE]`). Resumability: every pipeline checkpoints to disk so `/clear` + re-invoke continues at the first incomplete agent.

**Constraints.**
- Target domain = **data-management productivity apps** (CRUD-heavy). Prototype defaults assume that, not marketing/content.
- Output target = **prototype** for every pipeline run (client-stub simulated server, fixture data — `framework/shared/prototype-invariants.md` PI-01..PI-08). The application-audience document is an export-time concern (`/export-application`).
- Every consultant interaction = foreground in-thread via `AskUserQuestion`. **No background/sub/async agents** for interactive surfaces — handback gates depend on same-thread acceptance.
- Every artefact write = `Write` then `framework/skills/verify-artifact-write.md` (sha256 + min-bytes). Mismatch → RF-04 hard halt. The `/prototype` generator narrows the call sites on compile-covered files — canonical in `framework/agents/prototype-generator.md`; the RF-04 predicate itself is unchanged.
- **Visual inputs are interpreted once.** Images and vectors are converted at ingestion to a single frozen, `[SRC: <filename>]`-cited description sibling; downstream consumers (drafters, analysers, reviewers) read that description, **never the pixels**. Canonical read-path rule in `framework/skills/build-source-manifest.md`; conversion in `framework/skills/describe-visual-input.md`.
- Refusal predicates are canonical in `framework/shared/refusal-registry.md` — never paraphrase or redefine.
- **Input files are consultant-owned — the framework never deletes them.** Canonical in `framework/shared/input-safety.md` (`IS-01..IS-03`) — never paraphrase or redefine.
- **Prototype visual quality, device targets and colour are canonical elsewhere.** Every prototype meets the shared visual-craft floor and honours its per-prototype device targets (`framework/assets/prototypes/visual-craft-standard.md`; §11 for the named viewports and per-target obligations); colour binds through the semantic tokens only, with on-colours **measured** per mode by `framework/skills/extract-brand-theme.md`. The floor raises quality uniformly — it is **not** a divergence axis; divergence stays pure UX (posture + D1–D5). It complements `ux-baseline-checklist.md` (whether a surface *works*); a posture emphasises items but waives neither. Never paraphrase or redefine.
- **The wireframe and prototype pipelines never invent object properties.** Every data-bound element carries a `data-prop` drawn from the blueprint's per-surface closed set; anything outside it is a fabrication and an `RF-04`-class self-validation FAIL. Canonical in `framework/agents/blueprint-architect/steps/step-03-author-blueprint.md` and the variant-generator's self-validation step.
- **Final HTML artefacts auto-open in the consultant's browser at write time**, before the accept gate — the four analysis/review methodology artefacts, each `/design-system` mode file, and `/wireframe`'s `index.html` (screens excluded; they open from its links). This is **harness-level**: a `PostToolUse` hook running `framework/tools/open-artifact.cjs`, invoked by no orchestrator, agent, or skill — never add a call site. Canonical (path allowlist, idempotence, opt-out, non-fatal semantics): `framework/shared/artifact-preview.md` — never paraphrase or redefine. A failed preview is **not** a refusal and has no `RF-NN`; consultant-facing prose must never assert a tab exists, only name the path as a fallback.

## 2. Terminology & markers

### System terminology (use the glossary)

When extending, changing, or describing this system — writing plans, editing orchestrators/agents/skills/assets, or phrasing consultant-facing prompts — use the system's own terms exactly as defined in `framework/assets/glossary.md`. Consult the slim lookup `framework/assets/glossary.index.md` for the canonical term + one-line gloss, and Read the full `### Term` entry on demand only when you need the definition or a disambiguation. Do **not** coin synonyms for defined concepts (e.g. "page"/"view" for *surface*/*screen*, "styling" for *Design*, "stance" for *position*). The glossary defines **system** vocabulary only — the client application's domain vocabulary is produced separately by the GLOSSARY methodologies (`analyse-requirements/GLOSSARY/`, `analyse-inputs/GLOSSARY/`).

### Markers in content

**Provenance markers** answer *"where did this value come from?"* — the set is **closed** at these six:

| Marker | Means | Canonical in |
|---|---|---|
| `[SRC: C-NNN]` | Input-cited fact in the `/requirements` draft **and** final doc. Sidecar-backed by `requirements/draft-claims.ndjson`, the authoritative store of the verbatim source quotes (joined on the `C-NNN` tag). **Retained** by the merger as downstream provenance. | `framework/agents/requirements-merger.md` |
| `[SRC: <filename>]` | Filename-cited fact in `/analyse-inputs` and `/review-inputs` artefacts — the manifest row's `filename` payload. | `framework/skills/build-source-manifest.md` |
| `[AI-SUGGESTED: AI-NNN \| blocking\|non-blocking]` | Drafter inference; resolver Q&A. Reserved for facts not traceable to inputs **and** not covered by `GR-NN` — never widen this set. | `framework/shared/refusal-registry.md` |
| `[STANDARD-RULE: GR-NN]` | Deterministic; resolver skips. | `framework/shared/general-rules.md` |
| `[OUT-OF-SCOPE: domain-default]` | Prototype-only; resolver skips. | `framework/shared/prototype-scope.md` |
| `[POSTURE-DEFAULT]` | `/prototype` design spec — value follows deterministically from the chosen UX posture; resolver skips, merger strips. | `framework/assets/prototypes/template-design-spec.md` |

The merger strips `[AI-SUGGESTED]` / `[STANDARD-RULE]` / `[OUT-OF-SCOPE]` and retains `[SRC: …]`.

**Other marker axes:**

| Marker | Axis | Canonical in |
|---|---|---|
| `[PROTO-ONLY] … [/PROTO-ONLY]` | **Scope**, not provenance — *which build target does this apply to?* May co-occur with `[SRC:]` and one provenance marker; the merger retains it; `/export-application` deletes each span whole. | `framework/shared/prototype-scope.md > Prototype-only content marking` |
| `[CONSULTANT-STATED]` / `[AI-INFERRED, CONSULTANT-CONFIRMED]` | **Origin** — shared by the `/resolve-review` resolutions document, the `/amend-requirements` amendments document, and `AMD-NN` entries in the transient section. Deliberately not requirement-ID-shaped. | `framework/assets/resolve-review/template-resolutions.md`, `framework/assets/resolve-review/template-addendum.md` |

**Stable-ID prefixes:** `C-` claims · `AI-` suggestions · `PC-` / `PAI-` PRD equivalents · `GR-` general rules · `RF-` refusals · `PI-` prototype invariants · `AMD-` amendment entries in the transient section (per-section numbering, continuous across runs) · `AM-` amendment entries in an `/amend-requirements` input document (document-local, always from `AM-01`; independent of `AMD-NN` by design).
