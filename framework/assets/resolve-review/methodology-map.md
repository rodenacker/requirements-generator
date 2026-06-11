---
role: asset
kind: methodology-map
# Per-methodology parse + resolution schemas for /resolve-review. One row per review
# methodology whose artefacts the resolve-review-drafter can consume. The drafter
# resolves every methodology-specific value from its row — nothing methodology-specific
# is hardcoded in the agent or the orchestrator. Adding support for a new review
# methodology = append a row here (verifying the selectors against that methodology's
# template asset); zero agent edits, zero orchestrator edits.
#
# Scope: /review-inputs AND /review-requirement artefacts (the orchestrator globs both
# review-inputs/*/*.html and review-requirements/*/*.html). The lookup key is `method_dir`:
# the bare parent directory name for review-inputs artefacts (legacy v1 keying), the
# root-qualified `review-requirements/<METHOD>` for review-requirements artefacts —
# qualified because the same method dir name can exist under both roots (e.g. ADVERSARIAL).
methodologies:
  - method_dir: ADVERSARIAL
    method_slug: adversarial
    filename_stem: adversarial-review-resolutions
    id_prefix: ADV
    parse_source: html-articles
    json_block_id: null
    finding_selector: 'article whose class list contains "finding", id attribute = finding ID'
    heading_shape: '<h4><code>{ID}</code> — severity chip · disposition chip · scope chip · {one-line-problem}</h4>'
    one_liner_source: trailing text of the finding <h4> after the chips
    evidence_shape: '<blockquote class="evidence"><pre>{verbatim quote}</pre></blockquote> under dt "Evidence" (Dimension-1 skipped-placeholder variant: <em>(file skipped — tier: Unsupported; reason: …)</em>)'
    payload_fields: 'dt "Problem", dt "Recommendation" (one of five sanctioned corpus-handling forms), Disposition chip (Patch | Defer | Reject), scope-class chip'
    verbatim_anchor: evidence quote + Problem text
    severity_vocab: [Blocker, Major, Minor]
    severity_keyword_map: { "all blockers": Blocker }
    fingerprint_label: "Manifest SHA-256"
    fingerprint_compares_to: source-manifest
    resolution_semantics: apply-recommendation
    ask_shape: >-
      Confirmation ask. Draft the resolution from the finding's Recommendation +
      Disposition (declarative corpus-handling outcome, not the recommendation verb);
      options: Confirm-as-drafted / Edit (Other free text) / Skip. Confirm →
      [AI-INFERRED, CONSULTANT-CONFIRMED]; Edit → [CONSULTANT-STATED].
  - method_dir: COMPLETENESS-REVIEW
    method_slug: completeness-review
    filename_stem: completeness-review-resolutions
    id_prefix: COMP
    parse_source: html-articles
    json_block_id: null
    finding_selector: 'article whose class list contains "finding", id attribute = finding ID'
    heading_shape: '<h4><code>{ID}</code> — severity chip · disposition chip · {one-line-problem}</h4>'
    one_liner_source: trailing text of the finding <h4> after the chips
    evidence_shape: '<blockquote class="evidence"><pre>{verbatim quote}</pre></blockquote> under dt "Evidence" (ABSENT-finding variant: <blockquote class="evidence sentinel"><em>(no mention in consumed corpus)</em></blockquote>)'
    payload_fields: 'dt "Problem", dt "Authority", dt "Elicitation question" (or one of two not-applicable sentinels), Disposition chip (Needs-Clarification | Standard-Rule-Applies | Out-of-Scope)'
    verbatim_anchor: evidence quote (or its sentinel) + Problem text
    severity_vocab: [Blocker, Major, Minor]
    severity_keyword_map: { "all blockers": Blocker }
    fingerprint_label: "Manifest SHA-256"
    fingerprint_compares_to: source-manifest
    resolution_semantics: answer-elicitation
    ask_shape: >-
      Elicitation ask. Put the finding's Elicitation question to the consultant
      verbatim; the answer IS the resolution → [CONSULTANT-STATED]. Options: Answer
      (Other free text) / Mark out-of-scope / Skip. Findings whose Elicitation question
      is a not-applicable sentinel are presented flagged "review says no elicitation
      needed" and degrade to: State a resolution (Other) / Skip.
  - method_dir: AMBIGUITY-REVIEW
    method_slug: ambiguity-review
    filename_stem: ambiguity-review-resolutions
    id_prefix: AMB
    parse_source: html-articles
    json_block_id: null
    finding_selector: 'article whose class list contains "finding", id attribute = finding ID'
    heading_shape: '<h4><code>{ID}</code> — severity chip · type chip · {one-line-problem}</h4>'
    one_liner_source: trailing text of the finding <h4> after the chips
    evidence_shape: '<blockquote class="evidence"><pre>{verbatim quote}</pre></blockquote> under dt "Evidence"'
    payload_fields: 'dt "Problem", dt "Interpretations" (<ol class="interpretations">, ≥2 items), dt "Elicitation question"'
    verbatim_anchor: evidence quote + Problem text
    severity_vocab: [Blocker, Major, Minor]
    severity_keyword_map: { "all blockers": Blocker }
    fingerprint_label: "Manifest SHA-256"
    fingerprint_compares_to: source-manifest
    resolution_semantics: pick-interpretation
    ask_shape: >-
      Interpretation pick. Options = the finding's interpretations verbatim (up to 3)
      + Other ("state the intended meaning") / Skip. A picked interpretation →
      [AI-INFERRED, CONSULTANT-CONFIRMED] (the wording is review-drafted; the pick is
      the confirmation); Other → [CONSULTANT-STATED]. The resolution prose restates the
      chosen meaning declaratively — never as "option (b) was chosen".
  - method_dir: GAP-ANALYSIS
    method_slug: gap-analysis
    filename_stem: gap-analysis-resolutions
    id_prefix: GAP
    parse_source: embedded-json
    json_block_id: gap-analysis-meta
    finding_selector: '<script type="application/json" id="gap-analysis-meta"> → gaps[] array (fields: id, topic_ref, dimension, coverage, impact, confidence, moscow, recommendation, candidate_requirement, evidence, also_see). Fallback on JSON parse failure: article whose class list contains "finding", id attribute = gap ID, dt fields Recommendation / Candidate Requirement / Impact × Confidence / Evidence / Also see'
    heading_shape: '<h4><code>{ID}</code> · <code>{topic_ref}</code> · moscow chip · coverage chip</h4> — no one-line problem in the heading'
    one_liner_source: 'compose as "{topic_ref} ({dimension}) — {recommendation}"'
    evidence_shape: 'gaps[].evidence — [SRC: <filename>] citation list, or the sentinel "(no mention in consumed corpus)" for Missing-coverage gaps'
    payload_fields: 'recommendation, candidate_requirement (shall-form, or the sentinel "(deferred — no candidate requirement issued)"), moscow, impact, confidence, coverage'
    verbatim_anchor: 'recommendation + candidate_requirement verbatim (evidence is citations or a sentinel, not a quote — the payload itself is the durable anchor)'
    severity_vocab: [Must, Should, Could, "Won't"]
    severity_keyword_map: { "all musts": Must, "all blockers": Must }
    fingerprint_label: "Manifest fingerprint"
    fingerprint_compares_to: source-manifest
    resolution_semantics: ratify-candidate
    ask_shape: >-
      Ratification ask. Present the candidate_requirement (shall-form) + MoSCoW +
      Impact × Confidence; options: Ratify-as-is / Edit (Other free text) / Reject-skip.
      Ratify → [AI-INFERRED, CONSULTANT-CONFIRMED]; Edit → [CONSULTANT-STATED]. Won't
      rows carrying the deferred sentinel degrade to: State a resolution (Other) / Skip.
  # ---- /review-requirement rows (root-qualified keys; fingerprint = requirements.md sha) ----
  - method_dir: review-requirements/ADVERSARIAL
    method_slug: adversarial
    filename_stem: adversarial-requirements-review-resolutions
    id_prefix: ADV
    parse_source: html-articles
    json_block_id: null
    finding_selector: 'article whose class list contains "finding" inside the per-dimension findings-list divs, id attribute = finding ID (ADV-NN)'
    heading_shape: '<h4><code>{ID}</code> — severity chip · disposition chip · scope-class chip (fe-relevant | fe-facing-contract | backend-only) · {one-line-problem}</h4>'
    one_liner_source: trailing text of the finding <h4> after the chips
    evidence_shape: '<blockquote class="evidence"><pre>{verbatim quote ≤5 lines from requirements.md}</pre></blockquote> under dt "Evidence"; dt "Location" carries the requirements.md anchor (§N.N, BR-NN, G-NN, FR-NN, line-N)'
    payload_fields: 'dt "Problem", dt "Recommendation" (one-sentence concrete corrective action), Disposition chip (Patch | Defer | Reject), scope-class chip'
    verbatim_anchor: evidence quote + Problem text
    severity_vocab: [Blocker, Major, Minor]
    severity_keyword_map: { "all blockers": Blocker }
    fingerprint_label: "Source SHA-256"
    fingerprint_compares_to: requirements-doc
    resolution_semantics: apply-recommendation
    ask_shape: >-
      Confirmation ask. Draft the resolution from the finding's Recommendation +
      Disposition as a declarative statement about the desired requirement (what the
      requirement must state or cover — never an edit instruction against the doc);
      options: Confirm-as-drafted / Edit (Other free text) / Skip. Confirm →
      [AI-INFERRED, CONSULTANT-CONFIRMED]; Edit → [CONSULTANT-STATED]. Supersession
      names `requirements/requirements.md` + the finding's Location anchor (the
      reviewed document is the only file these findings cite).
  - method_dir: review-requirements/FIRST-PRINCIPLES
    method_slug: first-principles
    filename_stem: first-principles-review-resolutions
    id_prefix: 'mixed — subject IDs (G-NN | US-NN | BR-NN | FR-NN | EN-NN) for Top-10 items; composed labels ORPHAN:{anchor} and CS:{row-n} for the id-less orphan articles and cross-subject rows'
    parse_source: html-articles
    json_block_id: null
    finding_selector: 'three finding kinds, in document order: (a) <article class="ttitem"> Top-10 low-defensibility deep-dives, id attribute = subject ID; (b) <article class="orphan"> coverage findings (no id attribute — label as ORPHAN:{anchor}); (c) <tbody> rows of <table class="cs-table"> cross-subject findings (no id attribute — label as CS:{1-based row index})'
    heading_shape: 'ttitem: <h3>{RANK}. <code>{SUBJECT_ID}</code> — score badge {SCORE}/6 — weakest: {Qn}</h3>; orphan: <h3>{ORPHAN_KIND} — <code>{ANCHOR}</code></h3>; cs-row: no heading — use the Headline cell'
    one_liner_source: 'ttitem: compose as "score {SCORE}/6, weakest {Qn} — {recommended action}"; orphan: compose as "{ORPHAN_KIND} at {ANCHOR} — missing {expected counterpart}"; cs-row: the Headline cell'
    evidence_shape: 'ttitem: dt "Statement" <blockquote class="evidence"><pre>{subject statement verbatim}</pre></blockquote> (+ per-question evidence blockquotes); orphan: dt "Expected counterpart" + dt "Consequence" (absence finding — no doc quote); cs-row: the Evidence cell blockquote ({anchor}: {verbatim quote} per line)'
    payload_fields: 'ttitem: <p class="rec-action"> Recommended action ∈ {re-anchor | re-scope | remove | merge | clarify} + rationale; orphan: Expected counterpart + Consequence; cs-row: Relation + Consequence sentences (observational — no recommendation)'
    verbatim_anchor: 'ttitem: the Statement quote; orphan: the anchor + expected-counterpart text; cs-row: the Evidence cell quotes'
    severity_vocab: [blocking, major, minor]
    severity_keyword_map: { "all blockers": blocking }
    fingerprint_label: "Source SHA-256"
    fingerprint_compares_to: requirements-doc
    resolution_semantics: kind-dispatched
    ask_shape: >-
      Kind-dispatched ask. ttitem findings → confirmation: draft the resolution from the
      Recommended action + rationale as a declarative statement of the subject's intended
      purpose/scope; options: Confirm-as-drafted / Edit (Other free text) / Skip; Confirm →
      [AI-INFERRED, CONSULTANT-CONFIRMED]; Edit → [CONSULTANT-STATED]. orphan and cs-row
      findings carry no recommendation → elicitation: present the finding (expected
      counterpart / relation + consequence) and ask the consultant to state the resolving
      fact or descope; the answer IS the resolution → [CONSULTANT-STATED]; options: Answer
      (Other free text) / Mark out-of-scope / Skip. Findings-list display: ttitem entries
      show "score N/6" in place of a severity word (orphans are all blocking). Supersession
      names `requirements/requirements.md` + the finding's anchor.
  - method_dir: review-requirements/TEN-BA-QUESTIONS
    method_slug: ten-ba-questions
    filename_stem: ten-ba-questions-review-resolutions
    id_prefix: BAQ
    parse_source: html-articles
    json_block_id: null
    finding_selector: 'article whose class list contains "qcard", id attribute = question ID (BAQ-NN, rank order BAQ-01..BAQ-10)'
    heading_shape: '<h3><code>{ID}</code> — priority chip · {category-id} {category-label} · <code>{anchor-or-missing}</code></h3>'
    one_liner_source: 'first line of the question text (<blockquote class="question">), truncated as in the triage table'
    evidence_shape: 'no source quote — the finding IS a question: <blockquote class="question"><p>{question text verbatim}</p></blockquote>; the heading anchor is §N.N or "missing-section: {slug}"'
    payload_fields: '<blockquote class="question"> question text + <p class="why"> rationale ("Why this matters")'
    verbatim_anchor: question text + rationale (absence-type findings carry no doc quote — the question itself is the durable anchor)
    severity_vocab: [blocking, major, minor]
    severity_keyword_map: { "all blockers": blocking }
    fingerprint_label: "Source SHA-256"
    fingerprint_compares_to: requirements-doc
    resolution_semantics: answer-elicitation
    ask_shape: >-
      Elicitation ask. Put the question card's question to the consultant verbatim (with
      category + rationale as context); the answer IS the resolution → [CONSULTANT-STATED].
      Options: Answer (Other free text) / Mark out-of-scope / Skip. Supersession names
      `requirements/requirements.md` + the card's anchor when the answer changes a stated
      fact; "missing-section" anchors are net-new by construction.
  - method_dir: review-requirements/TEN-UX-QUESTIONS
    method_slug: ten-ux-questions
    filename_stem: ten-ux-questions-review-resolutions
    id_prefix: UXQ
    parse_source: html-articles
    json_block_id: null
    finding_selector: 'article whose class list contains "qcard", id attribute = question ID (UXQ-NN, rank order UXQ-01..UXQ-10)'
    heading_shape: '<h3><code>{ID}</code> — priority chip · {category-id} {category-label} · <code>{anchor-or-missing}</code></h3>'
    one_liner_source: 'first line of the question text (<blockquote class="question">), truncated as in the triage table'
    evidence_shape: 'no source quote — the finding IS a question: <blockquote class="question"><p>{question text verbatim}</p></blockquote>; the heading anchor is §N.N or "missing-section: {slug}"'
    payload_fields: '<blockquote class="question"> question text + <p class="why"> rationale ("Why this matters")'
    verbatim_anchor: question text + rationale (absence-type findings carry no doc quote — the question itself is the durable anchor)
    severity_vocab: [blocking, major, minor]
    severity_keyword_map: { "all blockers": blocking }
    fingerprint_label: "Source SHA-256"
    fingerprint_compares_to: requirements-doc
    resolution_semantics: answer-elicitation
    ask_shape: >-
      Elicitation ask. Put the question card's question to the consultant verbatim (with
      category + rationale as context); the answer IS the resolution → [CONSULTANT-STATED].
      Options: Answer (Other free text) / Mark out-of-scope / Skip. Supersession names
      `requirements/requirements.md` + the card's anchor when the answer changes a stated
      fact; "missing-section" anchors are net-new by construction.
  - method_dir: review-requirements/USER-STORIES
    method_slug: user-stories
    filename_stem: user-stories-review-resolutions
    id_prefix: US
    parse_source: html-articles
    json_block_id: null
    finding_selector: 'article whose class list contains "finding" under the blocking/major/minor priority sections, id attribute = story ID (US-NN); one finding = one not-ready story together with its nested <ul class="issues">'
    heading_shape: '<h3><code>{STORY_ID}</code> — priority chip · {persona}</h3>'
    one_liner_source: 'compose as "{persona} story — fails {criteria-violated comma list}"'
    evidence_shape: '<blockquote class="connextra"><p>{story text verbatim}</p></blockquote> + the per-issue reasons in <ul class="issues">'
    payload_fields: 'the issues list — per issue: criterion (Meaningful | Implementable | Testable | Coherent | Scoped | Outcome-aligned) + severity chip + reason + Fix hint; plus the anchor line (§4.2 / {persona} / story #{N})'
    verbatim_anchor: the Connextra story text + the issue reasons
    severity_vocab: [blocking, major, minor]
    severity_keyword_map: { "all blockers": blocking }
    fingerprint_label: "Source SHA-256"
    fingerprint_compares_to: requirements-doc
    resolution_semantics: apply-recommendation
    ask_shape: >-
      Confirmation ask, one per story finding (its issues are resolved together in one
      drafted resolution). Draft the resolution from the issues' Fix hints as a declarative
      statement of what the story must specify (persona, action, outcome, scope, acceptance
      conditions — as the issues demand); options: Confirm-as-drafted / Edit (Other free
      text) / Skip. Confirm → [AI-INFERRED, CONSULTANT-CONFIRMED]; Edit →
      [CONSULTANT-STATED]. Supersession names `requirements/requirements.md` + the story's
      §4.2 anchor.
  - method_dir: review-requirements/REQUIREMENTS-QUALITY
    method_slug: requirements-quality
    filename_stem: requirements-quality-review-resolutions
    id_prefix: 'mixed — fix-{req_id} for per-requirement fix cards; {characteristic}-{n} for set-level findings'
    parse_source: html-articles
    json_block_id: null
    finding_selector: 'two finding kinds, in document order: (a) <article class="fix-card"> per Red/Yellow requirement, id attribute = fix-{req_id}; (b) <article class="setlevel-finding">, id attribute = {characteristic}-{n}. (The trailing <script type="application/json" id="requirements-quality-meta"> carrier exists but its field schema is not documented in the template — the articles are the canonical parse surface.)'
    heading_shape: 'fix-card: <h3><code>{req_id}</code> · <code>{anchor}</code> · tier chip (Red | Yellow)</h3>; setlevel: <h3>characteristic chip + severity chip</h3>'
    one_liner_source: 'fix-card: compose as "{req_id} fails {failing characteristics + rule codes}"; setlevel: compose as "{characteristic} — {relation, truncated}"'
    evidence_shape: 'fix-card: dt "Offending text" <blockquote class="evidence"><pre>{verbatim quote}</pre></blockquote>; setlevel: dt "Evidence" blockquote ({anchor}: {quote} per line)'
    payload_fields: 'fix-card: dt "Failing characteristics" (chips + rule codes) and dt "Proposed (EARS)" — the rewrite / split lines, possibly a "meaning-change: confirm" chip, or the no-automatic-rewrite sentinel; setlevel: dt "Relation" + dt "Consequence" (observational — no recommendation)'
    verbatim_anchor: 'fix-card: the Offending-text quote + the Proposed (EARS) text; setlevel: the Evidence quotes'
    severity_vocab: [Red, Yellow, blocking, major, minor]
    severity_keyword_map: { "all reds": Red, "all blockers": blocking }
    fingerprint_label: "Requirements fingerprint"
    fingerprint_compares_to: requirements-doc
    resolution_semantics: kind-dispatched
    ask_shape: >-
      Kind-dispatched ask. fix-card findings → confirmation: draft the resolution from the
      Proposed (EARS) rewrite as the declarative intended requirement statement (a
      "meaning-change: confirm" chip or the no-automatic-rewrite sentinel degrades the ask
      to elicitation — the consultant states the measurable value / intended meaning);
      options: Confirm-as-drafted / Edit (Other free text) / Skip; Confirm → [AI-INFERRED,
      CONSULTANT-CONFIRMED]; Edit or stated value → [CONSULTANT-STATED]. setlevel findings
      carry no rewrite → elicitation: present Relation + Consequence; the consultant states
      the resolving fact or descopes → [CONSULTANT-STATED]; options: Answer (Other free
      text) / Mark out-of-scope / Skip. Findings-list display: fix-cards show their tier
      (Red | Yellow), setlevel findings their severity word. Supersession names
      `requirements/requirements.md` + the finding's anchor(s).
  - method_dir: review-requirements/REQUIREMENTS-TRACEABILITY
    method_slug: requirements-traceability
    filename_stem: requirements-traceability-review-resolutions
    id_prefix: untraced
    parse_source: html-articles
    json_block_id: null
    finding_selector: '<article class="untraced-card">, id attribute = untraced-{unit_id} — the headline Untraceable Set (verdicts Orphan | Broken-citation | Dropped-but-present | Not-alignable | Unattributed). The warn-level drift/dead-provenance fix cards and the provenance ledger are pipeline-hygiene records, not consultant-resolvable findings — excluded. (The trailing <script type="application/json" id="requirements-traceability-meta"> carrier exists but its field schema is not documented in the template — the articles are the canonical parse surface.)'
    heading_shape: '<h3><code>{unit_id}</code> · <code>{anchor}</code> · provenance-verdict chip</h3>'
    one_liner_source: 'compose as "{verdict}: {why-it-fails-to-trace reason, truncated}"'
    evidence_shape: 'dt "What it says" <blockquote class="evidence"><pre>{offending text verbatim}</pre></blockquote> + dt "Why it fails to trace"'
    payload_fields: 'dt "Recommended action" (e.g. "supply the source quote or remove the citation", "re-confirm with the consultant or remove")'
    verbatim_anchor: the What-it-says quote + the why-it-fails reason
    severity_vocab: [Broken-citation, Dropped-but-present, Orphan, Not-alignable, Unattributed]
    severity_keyword_map: { "all orphans": Orphan, "all broken": Broken-citation }
    fingerprint_label: "Requirements fingerprint"
    fingerprint_compares_to: requirements-doc
    resolution_semantics: answer-elicitation
    ask_shape: >-
      Grounding elicitation. Present the unit's text, verdict, and the review's Recommended
      action; the consultant states the grounding outcome as a declarative fact — ratify the
      statement's content as consultant-stated fact, name the input file that grounds it, or
      remove it from scope. Options: Ratify as stated fact / Name the source or state the
      fact (Other free text) / Remove from scope / Skip. A bare Ratify confirms
      review-presented content → [AI-INFERRED, CONSULTANT-CONFIRMED]; typed content →
      [CONSULTANT-STATED]. Supersession names `requirements/requirements.md` + the unit's
      anchor.
---

# resolve-review/methodology-map.md

**Purpose:** Machine-readable per-methodology contract for `framework/agents/resolve-review-drafter.md`. The frontmatter above is the **only** place methodology-specific parse anchors and resolution semantics are defined for the `/resolve-review` pipeline; the drafter and `framework/orchestrators/resolve-review-orch.md` resolve every methodology-specific value from the row whose `method_dir` matches the chosen artefact's methodology key. The selectors and field labels in each row were transcribed from the methodology's template asset (`framework/assets/reviews-inputs/template-<method>.html` for review-inputs rows; `framework/assets/reviews/template-<method>.html` for review-requirements rows) — that template remains the canonical definition of the artefact's structure; this map only *points at* it for parsing.

**Used by:**

- `framework/orchestrators/resolve-review-orch.md` — step 0 checks that the chosen artefact's parent directory has a row here (no row → friendly exit naming this file as the fix location).
- `framework/agents/resolve-review-drafter.md` — resolves its row at Step 1 and drives parsing (Steps 2–3), the findings list (Step 4), the per-finding asks (Step 5), and the output filename (Step 9) from the row's fields.

**Field semantics:**

- `method_dir` — **the lookup key.** For review-inputs artefacts: the bare parent directory name under `review-inputs/` (uppercase, legacy v1 keying). For review-requirements artefacts: the root-qualified `review-requirements/<METHOD>` — qualified because the same method dir name can exist under both roots (e.g. `ADVERSARIAL`). The orchestrator derives the key per this rule at its step 0 and passes it as `methodology_key`.
- `method_slug` — lowercase methodology slug, matching the source registry's `name` field. Recorded in the resolutions document's provenance table.
- `filename_stem` — the output filename stem: the final document is `input/<filename_stem>-<YYYY-MM-DD>.md` (same-day collision → `-2`, `-3`, …). Explicit per row so slugs already ending in `-review` don't produce `…-review-review-resolutions…`.
- `id_prefix` — the finding-ID prefix (`ADV`, `COMP`, `AMB`, `GAP`). **Finding IDs are per-run labels** — the source review resets them on every fresh run — so the resolutions document anchors on verbatim content (`verbatim_anchor`) and treats IDs as convenience labels only.
- `parse_source` — `embedded-json` (parse the `<script type="application/json" id="{json_block_id}">` block; on parse failure fall back to the HTML articles and say so in-thread) or `html-articles` (walk the finding articles directly).
- `json_block_id` — the embedded JSON block's element id; `null` for `html-articles` rows.
- `finding_selector` / `heading_shape` / `one_liner_source` / `evidence_shape` / `payload_fields` — prose parse anchors describing where a finding's id, severity, one-line problem, verbatim evidence, and actionable payload live. Transcribed from the template asset; if a template's block schema changes, re-verify this row (co-edit rule).
- `verbatim_anchor` — which extracted content serves as the durable verbatim anchor in the resolutions document (gap-analysis differs: its evidence is citations or a sentinel, so the payload itself anchors).
- `severity_vocab` — the ranking vocabulary, **highest first** (gap-analysis ranks by MoSCoW, not Blocker/Major/Minor). Drives the findings-list display and `severity_keyword_map`.
- `severity_keyword_map` — free-text selection keywords accepted at the drafter's Step 4 multi-pick (e.g. `all blockers`), each mapping to a single vocab value meaning "every finding at that value".
- `fingerprint_label` — the header `<dt>` label carrying the review's source fingerprint (`Manifest SHA-256` / `Manifest fingerprint` for review-inputs rows; `Source SHA-256` / `Requirements fingerprint` for review-requirements rows). Used by the drafter's Step-2 drift check.
- `fingerprint_compares_to` — closed enum naming what the drafter's Step-2 drift check hashes for comparison: `source-manifest` (`requirements/source-manifest.json`, review-inputs rows) or `requirements-doc` (`requirements/requirements.md`, review-requirements rows). For `requirements-doc` rows the drafter also pre-flights that `requirements/requirements.md` exists, and its Step 9b addendum branch is armed (see the drafter).
- `resolution_semantics` — closed enum naming the resolution flow: `apply-recommendation` | `answer-elicitation` | `pick-interpretation` | `ratify-candidate` | `kind-dispatched` (the row's findings come in more than one structural kind; the `ask_shape` names per kind which flow applies — confirmation for kinds with an actionable payload, elicitation for observational kinds). New methodologies may reuse an existing value or append a new one **here** (with its `ask_shape` describing the flow); the drafter's Step 5 executes whatever the row describes.
- `ask_shape` — one short paragraph specifying the per-finding `AskUserQuestion`: what is presented, the option set, and which option maps to which origin marker (`[CONSULTANT-STATED]` / `[AI-INFERRED, CONSULTANT-CONFIRMED]` — canonical definitions in `framework/assets/resolve-review/template-resolutions.md`). Every flow must include a Skip option, and every flow in which the drafted content originates from the review (not the consultant) must confirm **per finding** — never in bulk.

**Adding a new methodology (per-PR steps):**

1. Read the methodology's template asset and transcribe its finding-block anatomy into a new row (verify the selectors against the real template — do not copy a sibling row blind).
2. Choose `resolution_semantics` (reuse or append) and write the `ask_shape` honouring the per-item-confirmation rule.
3. Set `filename_stem` so the output filename reads naturally.
4. No agent, orchestrator, or command edits. The artefact picker discovers artefacts from disk; this map only gates whether a discovered `method_dir` is consumable.
