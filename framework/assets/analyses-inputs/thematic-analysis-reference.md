<!-- ROLE: asset (analysis reference). Methodology definition for the thematic-analysis input-analyser. Modelled on framework/assets/analyses/glossary-reference.md. Industry framing: Braun & Clarke (2006) "Using thematic analysis in psychology" — six-phase reflexive thematic analysis adapted for software-requirements elicitation inputs. Inductive themes are the only theme source; a deductive pass against a fixed 10-area concern frame surfaces coverage gaps as `[GAP-DEDUCTIVE: <concern>]` markers, never as invented themes. -->

# Thematic Analysis reference

> **Method:** Walk every consumable source enumerated in `requirements/source-manifest.json`, generate per-source observations (Phase 1), transform them into codes anchored to verbatim extracts (Phase 2), cluster the codes into candidate themes (Phase 3), refine the themes against their underlying codes (Phase 4), define and name the final themes (Phase 5), then produce the report — including a bridge from each theme to candidate-requirement seeds and a deductive coverage check against a fixed 10-area concern frame (Phase 6). Every code, theme-definition, and candidate-requirement carries one or more `[SRC: <filename>]` markers naming a manifest row. Coverage gaps surface as `[GAP-DEDUCTIVE: <concern>]` markers in a diagnostics section — **never** as invented themes. Across re-runs the artefact is **additive**: prior theme headings, code lists, and candidate-requirements are preserved; new manifest content extends them.

**Output file:** `analyse-inputs/THEMATIC-ANALYSIS/thematic-analysis.html` — a self-contained HTML document rendered via `framework/assets/analyses-inputs/template-thematic-analysis.html`. The theme-map is a **pre-rendered inline SVG** in a `#diagrams` section, with an adjacent collapsed `<details class="mermaid-block">` block carrying the Mermaid source as an export / re-ingestion adjunct (embedded as text, not validated by `mmdc`). A `language-json` `thematic-analysis-body` block carries the structured model (themes + codes) and the candidate-requirement seeds, so the artefact survives a markitdown HTML→Markdown conversion for re-ingestion by `/requirements`.

**Analyser agent:** `framework/agents/analyses-inputs/thematic-analysis-analyser.md`

**Character:** `framework/assets/characters/thematic-analysis-inputs-analysis.md`

---

## Industry framing — Braun & Clarke (2006) adapted for requirements work

A thematic analysis is a venerable qualitative-research artefact:

- **Braun & Clarke (2006) "Using thematic analysis in psychology"** is the canonical framing. Six phases — Familiarisation → Generating initial codes → Searching for themes → Reviewing themes → Defining and naming themes → Producing the report. Themes are **constructed by clustering codes**, not "emergent" in the data (the phrase *"emerging themes"* misleads about the analyst's active role).
- **Inductive vs deductive.** Pure inductive TA lets codes and themes arise from the data; pure deductive TA (framework analysis) applies a fixed code-frame to every source. This analyser runs **inductive Phases 1–5** and adds a **deductive coverage check** at Phase 6 that only flags gaps — it never creates a theme. Inductive themes remain the only theme source; the deductive pass is a safety net for software-domain concerns (NFRs, integration, security, compliance, operations) that may be under-represented in raw inputs.
- **Common failure modes.** Inventing themes from analyst world-knowledge that the data does not support; conflating different topics under a single generic theme (*Other*, *Misc*); padding with low-conviction codes to fill a deductive frame; calling a single-source pattern a "theme" without cross-source corroboration; using *"emerging themes"* language that hides the analyst's clustering choices.

This analyser sits firmly in the extraction camp. The subject of every code is an extract that **appears verbatim in a manifest-enumerated source**; every theme is supported by ≥ 2 codes; every candidate-requirement line cites the parent theme's source set; coverage gaps surface as `[GAP-DEDUCTIVE: <concern>]` markers, never as themes.

### Why apply a thematic-analysis pass to raw inputs?

Consultants drop briefs, decks, screenshots, interview notes, and meeting transcripts into `input/`. Reading those documents builds an intuitive sense of what matters — but the intuition is unreviewable and the patterns are forgotten by the time `/requirements` runs. A thematic analysis surfaces those patterns explicitly:

| Lens | Methodology | Question answered | Operates on |
|---|---|---|---|
| Domain vocabulary × definitions | glossary (input variant) | Which terms appear in the raw material? | raw `input/` |
| Jobs-to-be-done × situations | jtbd (input variant) | What jobs are users trying to get done? | raw `input/` |
| Causal chain × root drivers | five-whys (input variant) | Why does this concern exist in the inputs? | raw `input/` |
| **Pattern recognition × cross-source themes** | **thematic-analysis** | **What recurring patterns do the inputs carry, and what candidate requirements do they imply?** | **raw `input/`** |

Thematic analysis is the **right first methodology** for `/analyse-inputs` because qualitative-research TA was designed for transcripts, interview notes, and source documents — exactly the shape of raw consultant material. By contrast, the merged `requirements/requirements.md` that `/analyse-requirement` lenses has already normalised the consultant's phrasing into *"the system shall …"* statements; TA on that document would surface themes about the normaliser, not about the consultant's inputs.

### Why HTML with embedded Mermaid source + JSON body

- **Self-contained, diagram-first.** The artefact is a single HTML file the consultant can open in a browser with the theme-map at the top as a pre-rendered inline SVG — no Mermaid runtime, no external assets. This matches the framework's HTML-output, diagrams-first convention shared by the other analysers.
- **Re-ingestibility via embedded fenced blocks.** The artefact must still be droppable back into `input/` as a fresh source for a later `/requirements` run. The embedded `language-json` `thematic-analysis-body` block (themes + codes + candidate-requirement seeds) and the collapsed `mermaid-source` block survive a markitdown HTML→Markdown conversion, so the structured model round-trips cleanly; the drafter reads the candidate-requirement seeds without having to parse presentational HTML.
- **Diagram as inline SVG.** The theme-map is a pre-rendered inline `<svg>`; the Mermaid source is kept in an adjacent collapsed `<details class="mermaid-block">` block as an export / re-ingestion adjunct, embedded as text and **not** validated by `mmdc` (the inline SVG is the visible diagram — matching the other inline-SVG analyses; no `mmdc` dependency).

---

## Output structure

The artefact has a fixed top-to-bottom shape:

0. **In plain terms** (`<section id="plain-terms">` with `{{PLAIN_SUMMARY}}`) — a 2–5 sentence plain-English lead: what this thematic analysis is, what it found, what the consultant should do with it. The **first** section, above the meta-grid. A faithful condensation of the content below — it introduces no fact, count, or citation not already present, and carries no `[SRC]` of its own. Methodology jargon (theme, code, inductive/deductive coding, code frequency, saturation) is glossed at first use here; client domain terms are not glossed (the GLOSSARY methodology owns those). Per `framework/shared/output-readability.md`. The theme-map remains the first **visual** after this lead.
1. **Header.** Title, generation timestamp, manifest fingerprint (sha256 of `requirements/source-manifest.json`), run count.
2. **Thematic-meta** HTML comment carrying the additive-merge cursor (`manifest_fingerprint`, `run_count`).
3. **Summary.** Counts: observations, codes, candidate themes, final themes, candidate-requirements, coverage-frame results (covered / gap-deductive / silent), sources consumed / skipped.
4. **Themes.** One block per final theme, alphabetical by theme label. Each block:
   - `### {theme label}` (3–6 words, names the pattern).
   - 1–2-sentence definition.
   - Supporting codes: bulleted list of `{code_label}` — *"{verbatim extract ≤ 200 chars}"* `[SRC: <filename>]` — one bullet per code.
   - Cross-source: `Cross-source: yes (3 sources)` or `Cross-source: no (single source)`.
5. **Theme-map** (a `graph TD` diagram). Rendered as a **pre-rendered inline SVG** in the `#diagrams` section, with the Mermaid source kept in an adjacent collapsed `<details class="mermaid-block">` block as an export / re-ingestion adjunct (embedded as text, not validated by `mmdc`).
6. **Theme-to-requirement-candidates.** One sub-section per final theme; each sub-section is a bullet list of candidate-requirement lines of shape *"The system should `<verb> <object>` so that `<outcome>`"*, citing the parent theme's `[SRC: <filename>]` set.
7. **Coverage gaps and silent areas.** Three sub-lists:
   - **Covered** (no markers; just the concern name + the theme(s) covering it).
   - **Gap-deductive** (one `[GAP-DEDUCTIVE: <concern>]` marker per concern that has source mentions but no theme; for each, list the source filenames that mention it).
   - **Silent** (concerns with no source mentions; no marker — just the concern name and a one-line "no source mention" note).
8. **Source roster.** Two tables:
   - **Consumed**: one row per manifest entry whose `tier != "Unsupported"`: `filename`, `tier`, `sha256[:8]`, code-count.
   - **Skipped**: one row per manifest entry whose `tier == "Unsupported"`: `filename`, `reason` (from manifest's `conversions_applied` field).
9. **Run history.** Append-only bullet list of prior runs (one bullet per run, timestamped, with code-count delta, theme-count delta, and Override notes if applicable).

---

## Phase 1 — Familiarisation

Read every consumable manifest row in full. The manifest's `tier` field drives the read mechanism:

- `Native-text` → `Read original_path` directly as text.
- `Native-multimodal` → `Read original_path`; the Read tool surfaces image bytes automatically; the analyser transcribes visible text and structurally significant observations to memory.
- `Supported-via-MCP` → `Read converted_sibling` (the `.converted.md`) — the input-handler has already converted the source via markitdown; the analyser does not re-invoke conversion.
- `Unsupported` → skipped; record the row in `skipped_rows` with the manifest's `conversions_applied` value as the reason.

For each consumed row, produce a list of **first-pass observations** — short factual notes pinned to a verbatim site:

```
{
  observation_id,
  source_filename,
  excerpt: verbatim ≤ 200 chars or visual description for multimodal,
  position_hint: "para 3" | "line 47" | "image top-left",
  note: "the brief lists approvals as a manual hand-off"
}
```

No codes yet. State per-source observation counts aloud so the consultant can audit.

---

## Phase 2 — Generating initial codes

Transform each observation into one or more codes. Each code carries:

```
{
  code_id,
  label,                          // short noun-phrase, 2–5 words, e.g., "Approval-token expiry"
  extract,                        // verbatim ≤ 200 chars from the cited source
  source_filenames: [<filename>], // one or more manifest filenames
  category_hint: null | string    // optional, free-form (e.g., "data-quality", "permission")
}
```

A code's `extract` is **verbatim** — paraphrasing is not allowed. If the source phrasing is unclear, the `label` can be a cleaner restatement but the `extract` remains a direct lift. Every code carries at least one `[SRC: <filename>]` matching a manifest row's `filename` field.

State per-source code counts and the aggregate code count aloud:

> *"Phase 2 generated 47 codes across 4 sources (brief.docx: 18, whiteboard-photo.png: 9, interview-notes.md: 14, slack-export.md: 6)."*

---

## Phase 3 — Searching for themes

Cluster codes into candidate themes by conceptual proximity. Each candidate theme is:

```
{
  theme_id,
  label,                          // working title, may be revised in Phase 4–5
  code_ids: [...],                // ≥ 2
  cross_source: bool              // True if code_ids draw from ≥ 2 source files
}
```

**Drop any candidate cluster with fewer than 2 codes.** Either collapse it into the nearest neighbour or discard it — never elevate a single code to a theme without explicit consultant Override. State the candidate-cluster shape aloud:

> *"Phase 3 clustered 47 codes into 6 candidate themes: `Approval-bottleneck` (8 codes, 3 sources), `Audit-trail-completeness` (6 codes, 2 sources), `Permission-clarity` (5 codes, 3 sources), `Manual-data-entry` (12 codes, 4 sources), `Status-disambiguation` (3 codes, 2 sources), `Reporting-needs` (2 codes, 1 source). 11 codes did not cluster and remain unthemed (recorded in Diagnostics)."*

Unclustered codes are recorded in Diagnostics as `Unthemed codes (N)` but do not become themes.

---

## Phase 4 — Reviewing themes

Validate each candidate against its underlying codes and extracts. Apply three operations:

- **Split.** If a candidate's codes splinter into two distinct concepts (e.g., approval-time-delay vs approval-token-design coexist under one label), split into two candidates.
- **Merge.** If two candidates share > 50% of codes, merge them into one and pick the more accurate label.
- **Drop.** If after splitting a candidate falls below 2 codes, drop it (the codes become unthemed).

Generic labels are rejected at this phase:

- Forbidden labels: *Other*, *Misc*, *Miscellaneous*, *General*, *Various*, *Additional*, *Etc.* — they hide structural deficits. Either find a concrete pattern in the codes that justifies a real label, or drop the cluster and let its codes go unthemed.

State the reviewed-theme shape aloud:

> *"Phase 4 reviewed 6 candidate themes: kept 5 (Approval-bottleneck, Audit-trail-completeness, Permission-clarity, Manual-data-entry, Status-disambiguation), dropped 1 (Reporting-needs — only 2 codes from a single source; insufficient cross-source support; merged into Manual-data-entry where one of its codes fit, dropped the other)."*

---

## Phase 5 — Defining and naming themes

For each surviving theme, write:

- A **3–6-word title** that names the **pattern**, not the topic. *"Approval bottleneck under one named role"* names a pattern; *"Approvals"* names a topic.
- A **1–2-sentence definition** stating what the pattern is in the data. Definitions cite at least one extract verbatim per supporting source via `[SRC: <filename>]`.

After Phase 5, `final_themes` is **closed**. Phase 6 must not add themes; the deductive coverage check produces markers, not themes.

State the final theme shape aloud:

> *"Phase 5 named the final 5 themes:*
> - *Approval bottleneck under one named role (3 sources)*
> - *Audit trail completeness gaps (2 sources)*
> - *Permission clarity at role boundaries (3 sources)*
> - *Manual data entry burden across screens (4 sources)*
> - *Status value disambiguation across screens (2 sources)*"

---

## Phase 6 — Producing the report + theme-to-requirement-candidates bridge + deductive coverage check

Two sub-steps in order.

### Sub-step A — Bridge

For each theme in `final_themes`, derive one or more candidate-requirement lines:

- Shape: *"The system should `<verb> <object>` so that `<outcome>`"*.
- Solution-agnostic: prefer outcome-language (*"so that approvers can act within their permission scope"*) over implementation-language (*"using OAuth scopes"*).
- Citations: each line carries the parent theme's `[SRC: <filename>]` set.

These are **seeds for `/requirements`**, not authored requirements. The drafter will normalise them into `§6` clauses; the merger will strip `[SRC: …]` markers.

Output: a `Theme-to-requirement-candidates` table or grouped bullet list (one group per theme).

### Sub-step B — Deductive coverage check

Walk the fixed 10-area concern frame. For each concern, classify into one of three states:

| Concern | Keyword cues (lexical scan against consumed sources) |
|---|---|
| **Functional** | feature, capability, action, do, perform, support, allow, enable |
| **Data** | data, entity, record, field, attribute, schema, table, model, store |
| **NFR** (non-functional) | performance, latency, throughput, scalability, availability, reliability, uptime, response time |
| **Integration** | integration, API, webhook, SSO, third-party, external, sync, connector, ETL |
| **Security** | security, auth, authentication, authorisation, permission, role, access control, RBAC, encrypt, password, MFA, 2FA, audit, GDPR, PCI, HIPAA |
| **Workflow** | workflow, approval, process, hand-off, flow, sequence, stage, gate, queue, pipeline |
| **UX** | UX, UI, screen, page, form, button, click, navigation, accessibility, mobile, responsive, layout |
| **Reporting** | report, dashboard, KPI, metric, chart, graph, export, visualisation, summary, drill-down |
| **Compliance** | compliance, regulatory, legal, policy, retention, audit log, four-eyes, segregation of duties, SOX, GDPR, HIPAA, PCI-DSS, MiFID |
| **Operations** | deploy, monitor, alert, runbook, incident, on-call, observability, log, trace, metric, SLO, SLA |

For each concern:

- If at least one theme in `final_themes` touches the concern (its codes or definition lexically match) → record `covered: yes` and list the touching theme labels.
- Else if at least one consumed source mentions any of the concern's keyword cues → record `[GAP-DEDUCTIVE: <concern>]` and list the source filenames where the cue was found.
- Else → record `silent` (no source mention).

**Critical rule:** Sub-step B emits markers, **not** themes. The `final_themes` set is closed. A `[GAP-DEDUCTIVE: <concern>]` marker tells the consultant *"your inputs hint at this concern but no theme was supported — add more material covering it and re-run, or accept that the concern is out of scope for this run."*

### `[GAP-DEDUCTIVE: <concern>]` marker rules

- The marker payload is the concern name from the 10-area frame, written in the case shown above (`Functional`, `Data`, `NFR`, `Integration`, `Security`, `Workflow`, `UX`, `Reporting`, `Compliance`, `Operations`).
- The marker appears **only** in the `Coverage gaps and silent areas` section of the artefact. It must not appear in `Themes`, `Theme-to-requirement-candidates`, or the Mermaid diagram.
- The marker is **never** an invitation to invent a theme. The remedy is consultant action (enrich `input/` and re-run, or accept the gap).

---

## Theme-map diagram

The theme-map has two parts: the **visible** pre-rendered inline SVG and an embedded **Mermaid export** source beneath it. Keep them in agreement — every theme is a node in both.

### Visible diagram — layered-tree SVG

The visible diagram is a layered tree rendered by `framework/skills/render-layered-tree-svg.md` (the canonical layered-tree layout: deterministic centred rows, a single `viewBox`, vertical-S cubic edges). It reads top→bottom as **Root → Themes → (Codes)**:

- **Rows:** row 0 = a single Root node (`<rect rx="16">`, label "Themes from Inputs"); row 1 = one Theme node (`<rect rx="6">`, centred up-to-2-line label) per entry in `final_themes`, in a single centred row; row 2 = Code circles, **off by default** (the consultant opts in via the Step 12 Revise toggle *"include codes in the theme-map"*, which adds the codes row + theme→code edges).
- **Edges:** a solid vertical-S `edge-root-theme` per root→theme link (and `edge-theme-code` per theme→code link when codes are on). Each edge leaves its parent and meets its child straight-down, so the line→block correspondence is unambiguous even with many themes.
- **Cross-theme proximity:** when two themes shared ≥ 30% of codes at Phase 7 but were kept distinct (the analyst's clustering judgement), a dashed `edge-theme-theme` arc links them within the Themes row. The 30% threshold is the Jaccard overlap of the two themes' code sets.
- **Width:** wide maps scroll horizontally inside `figure.theme-map` (natural pixel width, never squashed to fit). Why layered rather than hub-and-spoke: a single root fanning straight radial lines into a 2-D grid forces many long diagonals to cross near the root, so lines cannot be traced to their blocks; one centred row + vertical-S edges removes the crossings.
- **Sources:** never drawn — `[SRC: <filename>]` markers in the body carry that provenance; surfacing sources in the diagram clutters the layout without adding information the body cannot.
- **Placement in the artefact:** after `## Themes`, before `## Theme-to-requirement-candidates`. Readers build the picture from the body's theme definitions, anchor it visually via the diagram, then see how each theme bridges to candidate requirements.

### Mermaid export source

- **Graph type:** `graph TD` (top-down).
- **Nodes:** Root `root([Themes from Inputs])` (stadium); Theme `T1["<theme label>"]` (rectangle), one per entry in `final_themes`; Code `c1((<code label>))` (circle), only when codes are toggled on.
- **Edges:** `root --> T1` for every theme; `T1 --> c1` per theme-code link when codes are on; `T1 -.-> T2` (dashed) per cross-theme proximity pair.
- **No Mermaid validation:** the visible diagram is the pre-rendered inline SVG; the Mermaid source beneath it is embedded as an unvalidated export adjunct (no `mmdc` dependency), surviving markitdown HTML→MD as a fenced ```mermaid block for re-ingestion.

---

## Source-of-truth hierarchy

The analyser reads exactly the files the manifest enumerates, plus the prior artefact (for additive merge) and its own three asset files. The manifest's `tier` field dictates the read path:

| Tier | Source location | Read mechanism |
|---|---|---|
| `Native-text` | `original_path` | `Read` directly as text |
| `Native-multimodal` | `original_path` | `Read` — Claude's vision surfaces image bytes; transcribe visible text/structure |
| `Supported-via-MCP` | `converted_sibling` | `Read` the `.converted.md` (markitdown's output, produced by input-handler) |
| `Unsupported` | — | Skipped; recorded in `Source roster > Skipped` |

The analyser **never** reads:

- Any path under `requirements/` other than `requirements/source-manifest.json`.
- Any path under `framework/state/`.
- Any path under `framework/shared/` (textual references to `RF-NN` / `GR-NN` in this file and in the analyser are links for the reader, not file loads).
- Other analyses' artefacts (`analyse-requirements/<OTHER-METHOD>/...`, `analyse-inputs/<OTHER-METHOD>/...`).
- Any pattern-catalogue or design-system file.

---

## Provenance markers

| Marker | Used in section | Payload | Meaning |
|---|---|---|---|
| `[SRC: <filename>]` | Themes, Theme-to-requirement-candidates, code extracts | basename including extension, matching a manifest row's `filename` field | The cited code / theme-definition / candidate-requirement is anchored to this manifest source; its extract is verbatim from the row's content |
| `[GAP-DEDUCTIVE: <concern>]` | Coverage gaps and silent areas (gap-deductive sub-list only) | concern name from the 10-area frame | The concern has at least one lexical mention in consumed sources but no inductive theme touches it |

**No third marker.** **No `[AI-SUGGESTED]` markers anywhere in the artefact** — thematic analysis is extraction, not inference.

---

## Quality gates (6 hard gates)

Run at Phase 6 close, before render. Each check operates on the in-memory state.

1. **Citation completeness.** Every code, every theme-definition, every candidate-requirement carries at least one `[SRC: <filename>]` marker, and every marker payload matches a manifest row's `filename` field exactly. Mismatch fails.
2. **Theme support.** Every theme in `final_themes` is supported by ≥ 2 codes. If the manifest contains ≥ 2 consumable sources, every theme has codes drawn from ≥ 1 source — but single-source themes are permitted because a manifest may have only one source. A theme with < 2 codes fails (the Phase 3 / Phase 4 discipline should have dropped it; this gate is a structural safety net).
3. **No generic theme names.** No theme or sub-theme label is *Other*, *Misc*, *Miscellaneous*, *General*, *Various*, *Additional*, or *Etc.* — unless the consultant explicitly chose `Override` at a prior fail of this gate (recorded in Diagnostics).
4. **Diagram completeness.** Every theme in `final_themes` appears as a node in **both** the pre-rendered inline SVG theme-map **and** the `graph TD` Mermaid export source; neither references theme IDs that no longer exist. (The Mermaid source is an unvalidated export adjunct — no `mmdc`.)
5. **Deductive coverage gaps recorded.** Every `coverage_results` entry with status `gap-deductive` appears in the `Coverage gaps and silent areas > Gap-deductive` sub-list as a `[GAP-DEDUCTIVE: <concern>]` line; every `silent` entry appears in the `Silent` sub-list; every `covered` entry appears in the `Covered` sub-list. No coverage result is dropped from the artefact.
6. **Manifest fingerprint + source roster.** The artefact carries exactly one `<!-- thematic-meta: ... -->` line; its `manifest_fingerprint` value equals the Phase 1 sha256; the `Source roster > Consumed` table enumerates every manifest row whose `tier != "Unsupported"` (with `filename`, `tier`, `sha256[:8]`, code-count); the `Source roster > Skipped` table enumerates every manifest row whose `tier == "Unsupported"` (with `filename`, reason).

(Six gates, not seven. The framework-wide *"no `[AI-SUGGESTED]` markers"* invariant is enforced by the analyser's anti-pattern of never emitting the marker — it has zero failure modes by construction and does not need a redundant gate.)

### Failure handling (Revise / Override / Restart)

On any hard-check failure: do **not** write the artefact. Surface `AskUserQuestion` with three options:

1. `Revise — exit so the consultant can enrich input/ and re-invoke /analyse-inputs (Recommended)`
2. `Override — proceed and write a known-defective artefact (Run-history bullet records every violation)`
3. `Restart — re-run from Phase 1 with a fresh manifest pass`

On **Revise**: hand back to the orchestrator with a `failed-handback` state.
On **Override**: record each failing check in the Run-history bullet for this run; proceed to render.
On **Restart**: re-enter Phase 1. Cap at three fail-Restart cycles; on the fourth, force the Revise path.

---

## Stop-condition

The analysis is complete when:

- `final_themes` is non-empty (or the consultant Override'd a zero-theme run with a recorded reason).
- All 6 hard gates pass, or the consultant chose Override and the failures are recorded in Diagnostics.
- Every theme is a node in both the pre-rendered inline SVG theme-map and the Mermaid export source (embedded as unvalidated text).
- `analyse-inputs/THEMATIC-ANALYSIS/thematic-analysis.html` has been written and `verify-artifact-write` returned `pass`.
- The consultant chose Accept in the handback loop.

---

## Re-run semantics

- The cursor (`manifest_fingerprint`, `run_count`) lives in the artefact's HTML-comment header. No state file under `framework/state/`.
- On re-run, the analyser compares the current manifest fingerprint to the prior cursor's value:
  - **No change** → pure additive widening; only new codes from new manifest rows extend the prior themes (if they cluster with an existing theme) or seed new ≥ 2-code themes.
  - **Change** → the analyser surfaces a drift prompt: `append-new-codes-only` (default, preserves prior theme bodies; appends new codes), `re-extract-everything` (re-runs Phases 1–5 from scratch; headings preserved where re-clustering produces equivalent themes), or `abort` (exit without writing).
- The artefact is monotonically growing across runs unless the consultant explicitly chose `re-extract-everything` or manually edited the file.

---

## Downstream consumption (handled by `framework/skills/map-thematic-analysis-to-ui.md`)

The analyser does not author UI primitives, so the downstream mapping is **signal-based**, not affordance-based:

- **Theme catalogue** → routed to feature-cluster entries for the design-spec consumer. Each theme is a potential cluster of related capabilities; theme labels seed cluster names; theme definitions seed cluster descriptions.
- **Theme-to-requirement-candidates** → routed to acceptance-criteria seeds for the `/requirements` drafter. Each candidate-requirement line is a starting point for a `§6` clause; the drafter normalises voice and assigns IDs.
- **Coverage gaps (`[GAP-DEDUCTIVE: <concern>]`)** → routed to consultant-interview prompts. Each gap-deductive marker is a question the consultant should answer before `/requirements` runs (or before sign-off).
- **Silent concerns** → recorded but not routed. A silent concern means no source mentions it — the consultant either accepts the silence as out-of-scope or adds material covering it.

`framework/skills/map-thematic-analysis-to-ui.md` is a stub at MVP — the mapping is documented here for the analyser's character file and for future downstream design-spec authors.

---

## Voice and stance

The analyser's stance is defined in `framework/assets/characters/thematic-analysis-inputs-analysis.md` — extraction-only, citation-bound, inductive-first-deductive-checked, gap-honest, additive. The reference here defines **what** to do; the character file defines **how** the agent talks while doing it.

The artefact is human-read (and re-ingested by `/requirements`), so the analyser also follows `framework/shared/output-readability.md`: it writes the "In plain terms" lead (2–5 plain-English sentences, faithful condensation, no new fact or citation), glosses methodology jargon at first use in human-readable prose — theme (a recurring pattern across the inputs), code (a tag on a piece of text anchored to a verbatim extract), inductive/deductive coding (letting codes arise from the data vs checking against a fixed frame), code frequency (how many codes support a theme), saturation (the point at which new sources add no new codes) — leaves client domain vocabulary unglossed (GLOSSARY territory), and keeps every `[SRC: <filename>]` marker. The plain-language layer is confined to the lead and first-use glosses; the thematic map, theme cards, JSON body, and diagnostics keep their concrete, citation-grounded discipline.
