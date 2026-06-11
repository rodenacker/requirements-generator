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
# v1 scope: /review-inputs artefacts only (the orchestrator globs review-inputs/*/*.html).
# Future /review-requirement support = append rows keyed by review-requirements/<METHOD>
# dirs + widen the orchestrator's step-0 glob. The lookup key is `method_dir` (the
# artefact's parent directory name).
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
    resolution_semantics: ratify-candidate
    ask_shape: >-
      Ratification ask. Present the candidate_requirement (shall-form) + MoSCoW +
      Impact × Confidence; options: Ratify-as-is / Edit (Other free text) / Reject-skip.
      Ratify → [AI-INFERRED, CONSULTANT-CONFIRMED]; Edit → [CONSULTANT-STATED]. Won't
      rows carrying the deferred sentinel degrade to: State a resolution (Other) / Skip.
---

# resolve-review/methodology-map.md

**Purpose:** Machine-readable per-methodology contract for `framework/agents/resolve-review-drafter.md`. The frontmatter above is the **only** place methodology-specific parse anchors and resolution semantics are defined for the `/resolve-review` pipeline; the drafter and `framework/orchestrators/resolve-review-orch.md` resolve every methodology-specific value from the row whose `method_dir` matches the chosen artefact's parent directory. The selectors and field labels in each row were transcribed from the methodology's template asset (`framework/assets/reviews-inputs/template-<method>.html`) — that template remains the canonical definition of the artefact's structure; this map only *points at* it for parsing.

**Used by:**

- `framework/orchestrators/resolve-review-orch.md` — step 0 checks that the chosen artefact's parent directory has a row here (no row → friendly exit naming this file as the fix location).
- `framework/agents/resolve-review-drafter.md` — resolves its row at Step 1 and drives parsing (Steps 2–3), the findings list (Step 4), the per-finding asks (Step 5), and the output filename (Step 9) from the row's fields.

**Field semantics:**

- `method_dir` — the artefact's parent directory name under `review-inputs/` (uppercase). **The lookup key.** Future `/review-requirement` rows would use `review-requirements/<METHOD>` dir names; key collisions are impossible because the orchestrator passes the dir name as found on disk.
- `method_slug` — lowercase methodology slug, matching the source registry's `name` field. Recorded in the resolutions document's provenance table.
- `filename_stem` — the output filename stem: the final document is `input/<filename_stem>-<YYYY-MM-DD>.md` (same-day collision → `-2`, `-3`, …). Explicit per row so slugs already ending in `-review` don't produce `…-review-review-resolutions…`.
- `id_prefix` — the finding-ID prefix (`ADV`, `COMP`, `AMB`, `GAP`). **Finding IDs are per-run labels** — the source review resets them on every fresh run — so the resolutions document anchors on verbatim content (`verbatim_anchor`) and treats IDs as convenience labels only.
- `parse_source` — `embedded-json` (parse the `<script type="application/json" id="{json_block_id}">` block; on parse failure fall back to the HTML articles and say so in-thread) or `html-articles` (walk the finding articles directly).
- `json_block_id` — the embedded JSON block's element id; `null` for `html-articles` rows.
- `finding_selector` / `heading_shape` / `one_liner_source` / `evidence_shape` / `payload_fields` — prose parse anchors describing where a finding's id, severity, one-line problem, verbatim evidence, and actionable payload live. Transcribed from the template asset; if a template's block schema changes, re-verify this row (co-edit rule).
- `verbatim_anchor` — which extracted content serves as the durable verbatim anchor in the resolutions document (gap-analysis differs: its evidence is citations or a sentinel, so the payload itself anchors).
- `severity_vocab` — the ranking vocabulary, **highest first** (gap-analysis ranks by MoSCoW, not Blocker/Major/Minor). Drives the findings-list display and `severity_keyword_map`.
- `severity_keyword_map` — free-text selection keywords accepted at the drafter's Step 4 multi-pick (e.g. `all blockers`), each mapping to a single vocab value meaning "every finding at that value".
- `fingerprint_label` — the header `<dt>` label carrying the review's manifest fingerprint (`Manifest SHA-256` for three methodologies, `Manifest fingerprint` for gap-analysis). Used by the drafter's Step-2 drift check.
- `resolution_semantics` — closed enum naming the resolution flow: `apply-recommendation` | `answer-elicitation` | `pick-interpretation` | `ratify-candidate`. New methodologies may reuse an existing value or append a new one **here** (with its `ask_shape` describing the flow); the drafter's Step 5 executes whatever the row describes.
- `ask_shape` — one short paragraph specifying the per-finding `AskUserQuestion`: what is presented, the option set, and which option maps to which origin marker (`[CONSULTANT-STATED]` / `[AI-INFERRED, CONSULTANT-CONFIRMED]` — canonical definitions in `framework/assets/resolve-review/template-resolutions.md`). Every flow must include a Skip option, and every flow in which the drafted content originates from the review (not the consultant) must confirm **per finding** — never in bulk.

**Adding a new methodology (per-PR steps):**

1. Read the methodology's template asset and transcribe its finding-block anatomy into a new row (verify the selectors against the real template — do not copy a sibling row blind).
2. Choose `resolution_semantics` (reuse or append) and write the `ask_shape` honouring the per-item-confirmation rule.
3. Set `filename_stem` so the output filename reads naturally.
4. No agent, orchestrator, or command edits. The artefact picker discovers artefacts from disk; this map only gates whether a discovered `method_dir` is consumable.
