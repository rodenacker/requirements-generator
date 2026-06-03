<!-- ROLE: asset (review reference). Loaded by framework/agents/reviews/requirements-traceability-reviewer.md at activation. -->

# reviews/requirements-traceability-reference.md

**Purpose:** Methodology reference for the **Requirements Traceability** review of `requirements/requirements.md`. The reviewer audits the **provenance integrity** of the merged spec: every substantive fact and every ID-bearing requirement should trace back to one of the system's legitimate provenance classes — a **real input source** (`[SRC: C-NNN]`, backed by a verbatim quote in `draft-claims.ndjson` and re-verified against the actual input file), an **accepted AI-suggestion** (a draft `[AI-SUGGESTED: AI-NNN]` the consultant confirmed/corrected in `resolver-answers.ndjson`), a **standard rule** (`[STANDARD-RULE: GR-NN]`), or an **out-of-scope domain default** (`[OUT-OF-SCOPE]`). Anything that traces to **nothing** — an **orphan**, a **broken citation**, or content that should have been **dropped** — is the headline result. The reviewer follows this document literally and exhaustively.

**Used by:**

- `framework/agents/reviews/requirements-traceability-reviewer.md` — drives capability-tier detection, the citation-integrity band, the draft↔final alignment band, the Untraceable Set, coverage metrics, verdict, validate, render, and write workflow.

**Output produced by the reviewer:** `review-requirements/REQUIREMENTS-TRACEABILITY/requirements-traceability.html` — a self-contained HTML document that **leads with the untraceable result** — (a) a capability banner + verdict, (b) a **provenance-class distribution diagram** (the untraceable slice highlighted), (c) the **Untraceable Requirements block** (every orphan / broken-citation / dropped-but-present item, the main result), then (d) a **requirement × trace-target heatmap**, (e) the full **provenance ledger** (every traced fact + its class + its evidence), (f) a **drift & dead-provenance** fix list, and (g) a diagnostics block recording the capability tier, the citation-verification run, and the alignment confidence.

The scaffold for the artefact is `framework/assets/reviews/template-requirements-traceability.html`.

---

## What "Requirements Traceability Review" means

Requirements traceability is the property that every requirement can be **followed back to its origin** — the stakeholder need, source document, or rationale that justifies it (Gotel & Finkelstein, 1994). The literature distinguishes two directions:

- **Pre-RS (backward) traceability** — from a requirement *back* to the source/rationale that produced it. Gotel & Finkelstein show this is the dominant, most-neglected traceability problem: requirements that enter the spec with no defensible origin.
- **Post-RS (forward) traceability** — from a requirement *forward* to design, code, and test artefacts.

**This lens audits backward/pre-RS traceability only.** Forward/post-RS traceability (requirement → design → code → test) is **not applicable here**: at review time there is no design/code/test artefact set to trace into (wireframes and prototypes are optional, separate pipelines and are out of scope for this review). The trace targets are the system's own **upstream provenance sources**: the input documents and the consultant's answers.

The lens is uniquely positioned for *this* system because the spec is assembled by an LLM pipeline (**draft → resolve → merge**) and is then hand-editable. Every step is a place where a fact could lose its origin: the drafter could cite a source it cannot quote; the merger could drop or alter a citation; a post-merge hand-edit could insert an unsourced claim or drift a value off the quote that justifies it. A traceability review re-establishes provenance integrity on the **final artefact that downstream pipelines actually consume**.

The lens's load-bearing honesty — mirroring the requirements-quality lens — is a **decidability split**. The citation half ("does this trace to a real input source?") is **mechanically decidable**: a `[SRC: C-NNN]` tag either resolves to a ledger entry whose quote is a verbatim substring of a real source file, or it does not. The AI-suggestion half ("does this trace to an accepted suggestion?") is **mostly decidable** because the marker-bearing draft survives as a baseline — but where the merger reworded content heavily or a hand-edit obscured the antecedent, attribution becomes a **judgment call that is fenced, never asserted as fabrication**.

### How this differs from the other `/review-requirement` lenses

| Lens | Stance | What gets surfaced | Instrument |
|---|---|---|---|
| **adversarial** | *"What is wrong with what's written?"* | Defects across the whole doc, found freeform. | Eight freeform defect lenses. |
| **first-principles** | *"Does each artefact need to exist given the stated business reality?"* | Weak justification chains; orphans; coherence gaps. | Per-subject defensibility audit. |
| **ten-ba-questions / ten-ux-questions** | *"What's missing for a BA / designer?"* | Stakeholder / designer questions. | Top-ten gap list. |
| **user-stories** | *"Which §4.2 stories are not yet good stories?"* | Story-craft defects. | Six story-quality criteria. |
| **requirements-quality** | *"Is each requirement well-formed against ISO 29148?"* | Per-requirement well-formedness defects + EARS rewrites. | Fixed per-requirement conformance scorecard. |
| **requirements-traceability** | *"Does each fact trace back to a real source or an accepted suggestion — or to nothing?"* | **Orphans, broken citations, dropped-but-present content, and drift.** | **Backward-trace audit of the provenance graph (input source · consultant answer · standard rule · untraced).** |

A doc can be **adversarially clean**, **first-principles defensible**, and **ISO-29148 well-formed** and still be **provenance-poor** — every requirement crisp and testable, yet half of them sourced to nothing the consultant can stand behind. This lens is the only one that audits *where the content came from* rather than *what the content says*. Its overlap with the other lenses is near-zero: it reads the provenance machinery, not the prose quality.

---

## Sources and defensibility

- **Gotel, O. & Finkelstein, A. (1994), "An Analysis of the Requirements Traceability Problem," 1st IEEE ICRE, pp. 94–101.** The canonical definition; establishes pre-RS vs post-RS traceability and that *most* traceability failures are pre-RS (requirements with no defensible origin). The empirical basis for leading with backward traceability and for the ORPHAN verdict.
- **ISO/IEC/IEEE 29148:2018** — lists **"Traceable"** as a required characteristic of a well-formed requirement: *"upward traceable to … documented stakeholder need(s)/source(s)."* This lens operationalises that single characteristic in depth (the requirements-quality lens scores the other eight; it intentionally leaves traceability thin and defers it here).
- **IEEE 830-1998** — names **Traceable** among the eight SRS quality characteristics ("the origin of each requirement is clear"). 29148's predecessor; corroborates the criterion's standing.
- **Orphan / gold-plating detection (RTM practice literature)** — the standard traceability-audit failure modes: a requirement with no upward trace is an *orphan*; coverage analysis classifies each requirement by whether its trace chain is complete. Our **UNTRACED** matrix column + **ORPHAN** verdict are the document-internal analogue.
- **The system's own grounding contract** (`framework/skills/grounding-verifier.md`, `framework/agents/requirements-drafter.md`) — the closed system "verbatim `[SRC: C-NNN]` citation **or** `[AI-SUGGESTED]` marker." This review verifies that contract held all the way into the **final** doc; the citation-integrity band **reuses the grounding-verifier engine** verbatim rather than reinventing a substring matcher.

The synthesis is this reference's contribution: take the pre-RS traceability concept, bind the *decidable* half to the system's deterministic grounding engine (so a "broken citation" is a fact, not an opinion), recover the *AI-suggestion* half through the marker-bearing draft (so an "accepted inference" is mostly decidable too), and **fence the genuinely-ambiguous residue honestly** rather than accuse the consultant of fabrication on a fuzzy alignment.

---

## The provenance asset set (the deliberate departure from stand-alone)

Every other `/review-requirement` lens is **stand-alone** — it reads `requirements/requirements.md` and nothing else under `requirements/`. **This lens cannot be**: provenance cannot be audited without the provenance evidence, and a stand-alone provenance review would be theatre. The reviewer therefore reads the full provenance asset family, **read-only**, as a documented, bounded exception (the drafter and `grounding-verifier.md` already read exactly these files):

| Asset | Role in the trace | Schema (canonical owner) |
|---|---|---|
| `requirements/requirements.md` | the audited final artefact | `framework/assets/template-requirements.md` |
| `requirements/requirements-draft.md` | **the marker-bearing baseline** (the Rosetta Stone — retains every `[SRC]`, `[AI-SUGGESTED: AI-NNN]`, `[STANDARD-RULE: GR-NN]`, `[OUT-OF-SCOPE]`) | drafter |
| `requirements/draft-claims.ndjson` | the `C-NNN` → verbatim-quote ledger | `{claim_id, draft_locator, claim_text, source_file, source_quote}` (grounding-verifier) |
| `requirements/draft-claims-verification.ndjson` | the **draft-time** grounding result per claim | `{claim_id, status, reason}` (grounding-verifier) |
| `framework/state/resolver-answers.ndjson` | how each `AI-NNN` was resolved (the consultant's answer) | `{id, status, resolved_value, reason}`, `status ∈ {confirmed, accepted-as-is, corrected, dropped}` (requirements-resolver) |
| `requirements/consultant-answers.md` | human-readable corroboration of the resolutions | narrative (drafter/orchestrator) |
| `requirements/source-manifest.json` | the allowlist of valid `source_file` paths + the original input files | input-handler |
| the input files (`original_path` / `converted_sibling`) | **the trace terminus** — the real document a quote must be found in | — |

### The trace chain terminates at the origin, not at an intermediate ledger

- **To the original input document:** final fact → `[SRC: C-NNN]` → `draft-claims.ndjson` (verbatim quote + `source_file`) → the quote must still be a **verbatim substring of the actual input file** named in `source-manifest.json`. The ledger is the index; the verification fires against the real source.
- **To the consultant's actual answer:** final fact → draft `[AI-SUGGESTED: AI-NNN]` → `resolver-answers.ndjson` (`confirmed`/`accepted-as-is`/`corrected` + `resolved_value`), corroborated by `consultant-answers.md`.

---

## Capability tiers (degrade with a banner — never silently fail)

The reviewer detects which provenance assets exist at Step 2 and sets `capability_tier`. A prominent **capability banner** at the top of the artefact states which trace layers were checked and the confidence ceiling. The reviewer **never halts because an asset is missing** (the only hard halts are an empty/unreadable final doc and an `RF-04` write-verify failure); it reports what it could establish.

| Tier | Assets present | What the review establishes | Confidence ceiling |
|---|---|---|---|
| **TIER-2 (full)** | final + draft + `resolver-answers` + `consultant-answers` + `draft-claims` + `draft-claims-verification` + manifest + **source files** | Full taxonomy; `[SRC]` quotes **re-verified live** against the original files; AI-suggestion attribution via draft + resolver ledger. | high (decidable band) |
| **TIER-1b** | as TIER-2 but **source files deleted** (the merger permits deletion of inputs post-generation) | `[SRC]` validity taken from `draft-claims-verification.ndjson` (the draft-time grounding record) — **traced as recorded at draft time, not re-verified live**; AI-suggestion attribution still available. | high (with the live-reverify caveat) |
| **TIER-1** | final + `draft-claims` + manifest + sources, **no draft / resolver ledger** | Citation-integrity only (SOURCED / BROKEN-CITATION / DEAD-PROVENANCE). The AI-suggestion half is `not-decidable` — every uncited substantive fact is reported as **UNATTRIBUTED** (a weaker, honest cousin of ORPHAN), not classified. | partial |
| **TIER-0** | **final doc only** (hand-authored / imported / sidecars gone) | **Syntactic-only**: `[SRC: C-NNN]`-tag well-formedness + an **orphan-surface census** (count of substantive statements carrying any provenance marker vs none). A doc with **zero** `[SRC]` tags gets the honest verdict **"no traceability scaffold present."** | low (banner-stated) |

The tier is recorded in diagnostics and the JSON block. A reader must never mistake a TIER-0 census for a TIER-2 audit; the banner is gate-enforced (gate 8).

---

## The provenance verdict taxonomy

Each **traced unit** (an ID-bearing requirement, or a `[SRC]`/`AI-NNN` ledger entry) is assigned exactly one verdict. The **headline result is the untraceable set** — the defect verdicts lead the report; the rest classify what *does* trace.

### Decidable (deterministic — high confidence)

- ✅ **SOURCED** — the unit carries (or its draft antecedent carries) `[SRC: C-NNN]`; `C-NNN` ∈ `draft-claims.ndjson` keys; **and** (TIER-2) `source_quote` is a verbatim substring of `source_file ∈ manifest allowlist`, **or** (TIER-1b) `draft-claims-verification.ndjson` records `C-NNN` as `status:"pass"`. *Traces to a real input document.*
- ✅ **STANDARD-RULE** — aligns to a draft `[STANDARD-RULE: GR-NN]` marker; the value is retained in the final doc. *Traces to a deterministic framework rule.*
- ✅ **OUT-OF-SCOPE-DEFAULT** — aligns to a draft `[OUT-OF-SCOPE]` marker; value retained (prototype-target docs only). *Traces to a declared domain default.*
- ❌ **BROKEN-CITATION** *(headline / defect)* — `[SRC: C-NNN]` present but `C-NNN ∉ draft-claims.ndjson` (`tag_without_sidecar`), **or** `source_quote` not found in `source_file` (`quote_not_found`), **or** `source_file ∉ manifest` (`source_not_in_manifest`). These are exactly grounding-verifier's three fail reasons. *Claims a source it cannot stand behind.*
- ❌ **DROPPED-BUT-PRESENT** *(headline / defect)* — content aligns to an `AI-NNN` whose `resolver-answers.ndjson` status is `dropped`, yet it survived into the final doc. *A merge defect — the consultant rejected this and it leaked through.*
- ⚠️ **DEAD-PROVENANCE** *(warn / info)* — a `draft-claims.ndjson` entry (or draft marker) with **no** presence in the final doc (grounding-verifier's `sidecar_without_tag`, re-interpreted: the merger may have **legitimately** dropped a cited field, so this is a warn, not a hard fail). *Provenance pointing at content that is gone.*

### Mostly-decidable (conditional on confident draft↔final alignment)

- ✅ **ACCEPTED-INFERENCE** — the final-doc unit aligns to a draft `[AI-SUGGESTED: AI-NNN]` whose resolver status ∈ {`confirmed`, `accepted-as-is`, `corrected`}, **and** the final value equals the retained drafter value (confirmed/accepted) or the `resolved_value` (corrected). *Traces to a suggestion the consultant accepted.* If alignment is **not** confident, the unit degrades to **NOT-ALIGNABLE** (fenced) — never asserted as accepted on a guess.

### Fenced (judgment — moderate confidence; never a fabrication accusation)

- ⚠️ **DRIFTED** *(fenced)* — the unit aligns to a draft antecedent but its **value changed** post-merge in a way **not** explained by a `corrected` resolution (a hand-edit that moved the value off its cited quote / accepted answer). Rendered with both the antecedent and the current value; the consultant adjudicates whether the edit is intentional.
- ⚠️ **ORPHAN / NOT-ALIGNABLE** *(headline / fenced)* — substantive final-doc content with **no** confident draft antecedent and **no** provenance class. Two sub-bands, both fenced at moderate confidence:
  - **NOT-ALIGNABLE** — a draft antecedent may exist but the merge reworded it past confident matching. *"No confident antecedent found"* — flagged for the consultant, not accused.
  - **ORPHAN** — confidently no draft antecedent (the content appeared after drafting — a hand-edit or a merger insertion). The strongest claim the lens makes is *"no antecedent found in the draft or any ledger"* — **never "fabricated."**
- ⚠️ **UNATTRIBUTED** *(TIER-1 only)* — an uncited substantive fact when no draft/resolver ledger is available to attribute it. The honest TIER-1 cousin of ORPHAN: *"cannot be attributed — the AI-suggestion ledger is absent."*

---

## The unit of traceability (two complementary views)

1. **Per-requirement provenance verdict** (the heatmap rows). For each ID-bearing requirement — **G-NN** §4.1, **F-NN** §6.1, **BR-NN** §6.2, **UI-NN** §6.4, **RPT-NN** §6.7, **NT-NN** §6.8 — assign its dominant verdict and light its **trace target** in the matrix: *Input source* (SOURCED), *Consultant answer* (ACCEPTED-INFERENCE), *Standard rule / scope default* (STANDARD-RULE / OUT-OF-SCOPE-DEFAULT), or **UNTRACED** (BROKEN-CITATION / DROPPED-BUT-PRESENT / ORPHAN / NOT-ALIGNABLE / UNATTRIBUTED). A requirement with several citations takes the **worst** verdict among them (one BROKEN citation makes the requirement UNTRACED for the matrix, even if its other citations are SOURCED — and the broken one is listed individually in the ledger). Use the document's own IDs.

2. **Document-level provenance ledger** (the exhaustive audit). One row per `[SRC: C-NNN]` tag found anywhere in the final doc (**including prose** §1/§2/§3/§7), plus one row per draft `AI-NNN`/`GR-NN`/`OUT-OF-SCOPE` marker, plus the DEAD-PROVENANCE entries. Each row carries `{unit, location/anchor, provenance_class, evidence, tier_note}`. This is where prose citations and dropped/dead provenance are accounted for — the heatmap only shows ID-bearing requirements.

Sections §1 context, §2 domain, §3 personas, §5 task flows, §7 data shapes are read for their `[SRC]` tags and for orphan-surface detection, but are **not** scored as heatmap rows (mirrors the requirements-quality §-scope discipline). The exclusion is disclosed in diagnostics as `id_scope_excluded`.

---

## Band A — citation-integrity (reuse the grounding-verifier engine)

The decidable citation half **is** the grounding-verifier engine, pointed at the final doc. Do not reinvent the substring matcher. Invoke `framework/skills/grounding-verifier.md` with:

- `draft_path = requirements/requirements.md` (the **final** doc — its retained `[SRC: C-NNN]` tags are the body under audit),
- `claims_path = requirements/draft-claims.ndjson`,
- `manifest_path = requirements/source-manifest.json`,
- `verification_path = review-requirements/REQUIREMENTS-TRACEABILITY/.workspace/citation-verification.ndjson`.

Consume its NDJSON output and the summary line. Map its reasons to verdicts, **re-interpreting Pass 2 for the final-doc context**:

| grounding-verifier signal | final-doc verdict |
|---|---|
| `status:"pass"` | **SOURCED** |
| `source_not_in_manifest` / `quote_not_found` / `tag_without_sidecar_entry` | **BROKEN-CITATION** |
| `sidecar_entry_without_tag` | **DEAD-PROVENANCE** (warn — *not* a hard fail; the merger may legitimately drop a cited field) |

**TIER-1b fallback** (source files deleted): the skill's Pass-1 `quote_found` cannot run. Do **not** invoke Pass-1; instead read `draft-claims-verification.ndjson` and treat its `status:"pass"` as SOURCED-as-of-draft-time, and still run the Pass-2 tag↔sidecar cross-check (which needs only the final doc + the sidecar). Banner the live-reverify caveat.

**TIER-0** (no `draft-claims.ndjson`): do not invoke the skill. Extract `[SRC: C-NNN]` tags by Grep for the well-formedness/orphan-surface census only.

The skill is **deterministic, no LLM** — the citation band is reproducible: the same inputs yield the same SOURCED/BROKEN set every run.

---

## Band B — draft↔final alignment (recover the stripped half)

The merger **strips** `[AI-SUGGESTED]`, `[STANDARD-RULE]`, `[OUT-OF-SCOPE]` from the final doc but **preserves the draft's structure** (same section order, same field set; it seeds the final by copying the draft, then edits markers/resolutions in place). The marker-bearing draft is therefore the **alignment baseline**.

**Procedure (per final-doc field / requirement):**

1. **Anchor by surviving citation.** If the unit (or its row) carries a `[SRC: C-NNN]` tag, that tag exists in both draft and final — it is a deterministic anchor. Align on it.
2. **Anchor by structure.** Otherwise align on the unit's `§`-anchor + ID + column position. The merger preserves these, so a draft `F-12` Statement aligns to the final `F-12` Statement deterministically in the common case.
3. **Read the draft antecedent's marker.** If the aligned draft cell carried `[AI-SUGGESTED: AI-NNN]` → look up `resolver-answers.ndjson[AI-NNN]`:
   - `confirmed` / `accepted-as-is` → final value should equal the drafter value → **ACCEPTED-INFERENCE** (else **DRIFTED**).
   - `corrected` → final value should equal `resolved_value` → **ACCEPTED-INFERENCE** (else **DRIFTED**).
   - `dropped` → the unit should be **absent** from the final → if present, **DROPPED-BUT-PRESENT**.
   - `[STANDARD-RULE: GR-NN]` → **STANDARD-RULE**; `[OUT-OF-SCOPE]` → **OUT-OF-SCOPE-DEFAULT** (value retained).
4. **No marker, no citation, but a clean structural antecedent with an identical value** → the value passed through unmarked (an `application`-mode out-of-scope field, or a structural field). Classify **ACCEPTED-INFERENCE** only if a draft marker backs it; otherwise treat as **NOT-ALIGNABLE → leans-traced** with an observation, never a hard ORPHAN (a structurally-identical antecedent is weak-but-real provenance).
5. **No confident antecedent at all** → **ORPHAN** (confidently absent from draft + ledgers) or **NOT-ALIGNABLE** (antecedent may exist but reworded past matching). Both fenced; quote the offending final-doc text.

**Anti-fabrication (load-bearing, gate-enforced):**

- **Never invent an antecedent.** If alignment is uncertain, render NOT-ALIGNABLE — do not manufacture a draft locator to claim a trace.
- **Never assert "fabricated."** The strongest ORPHAN claim is *"no antecedent found in the draft or any ledger."* Fabrication is a judgment about intent the lens cannot make.
- **Quote, don't paraphrase.** Every defect (ORPHAN/BROKEN/DROPPED/DRIFT) carries the verbatim offending text, present in the Step-2 quote index.

---

## The Untraceable Set (the headline result)

Assemble, **before** the scorecard and ledger, the **Untraceable Set**: every unit with a defect verdict — **ORPHAN**, **NOT-ALIGNABLE**, **BROKEN-CITATION**, **DROPPED-BUT-PRESENT** (and, at TIER-1, **UNATTRIBUTED**). Each entry carries `{unit_id_or_anchor, verdict, verbatim_offending_text, reason (why it fails to trace), recommended_action}`. This block leads the artefact (it is the main result) and every member must also appear in the per-requirement matrix and/or the ledger (gate: untraceable-set-completeness).

DRIFTED and DEAD-PROVENANCE are **warn-level**, not untraceable — they go in the **drift & dead-provenance** fix list lower down, not the headline block.

---

## Coverage metrics (untraceable count leads — no vanity %)

The exec summary renders, in this order:

- **Untraceable count** — `Orphan: N · Broken-citation: N · Dropped-but-present: N` (+ `Not-alignable: N` fenced; + `Unattributed: N` at TIER-1). **The lead metric.**
- **Trace coverage** — `Sourced: N · Accepted-inference: N · Standard-rule: N · Out-of-scope: N` (of `M` units), expressed as counts. A single **trace coverage %** = `traced / total` MAY be shown as a secondary line, but the lead is always the **untraceable count** — a 95%-traced doc with 3 orphans is reported as "3 untraceable," not "95% good."
- **Warn tally** — `Drifted: N · Dead-provenance: N`.
- **Capability tier** — restated.

---

## Verdict mapping

Reuse the three cross-reviewer verdict strings (kept consistent with the sibling lenses). Derive deterministically:

| Verdict | Trigger |
|---|---|
| **BLOCKED** | ≥1 **BROKEN-CITATION** or **DROPPED-BUT-PRESENT** (a citation that cannot be stood behind, or rejected content that leaked through, poisons downstream code-gen) **OR** ≥3 **ORPHAN** units. |
| **NEEDS-REVISION** | ≥1 ORPHAN/NOT-ALIGNABLE/UNATTRIBUTED or ≥1 DRIFTED, but no BLOCKED trigger. |
| **ACCEPTED-WITH-CONCERNS** | every unit traces (SOURCED / ACCEPTED-INFERENCE / STANDARD-RULE / OUT-OF-SCOPE-DEFAULT); at most DEAD-PROVENANCE warns remain. The lens never returns an unconditional ACCEPTED — at minimum the capability tier and any warns merit a look. |

At **TIER-0**, the verdict is capped at **NEEDS-REVISION** with the banner note *"syntactic-only — provenance ledger absent; trace integrity not established."* (A TIER-0 run cannot certify ACCEPTED-WITH-CONCERNS — absence of evidence is not evidence of trace.)

The verdict is information, not a hard gate: the reviewer writes the artefact regardless and hands back via Accept/Revise/Restart.

---

## Quality gates (hard gates)

Run before writing. Each is `pass | fail` (gate 8 has a `warn` variant). On any hard-gate fail the reviewer does **not** write — it surfaces the failure via `AskUserQuestion {Revise | Override | Restart}` (max 3 restart loops, then force Revise).

1. **Schema** — every traced unit carries a verdict from the closed taxonomy; every matrix row lights exactly one trace target (or UNTRACED).
2. **Enumeration** — every ID-bearing requirement found at Step 3 has a matrix row (`matrix_count == enumerated_count`); every `[SRC: C-NNN]` tag in the final doc has a ledger row.
3. **Untraceable-set-completeness** — every ORPHAN / NOT-ALIGNABLE / BROKEN-CITATION / DROPPED-BUT-PRESENT (/ UNATTRIBUTED) verdict appears in the headline Untraceable block; nothing untraceable is buried below the diagrams.
4. **Evidence-quote-exists (anti-fabrication)** — every defect's verbatim offending text is a substring in the Step-2 quote index; every BROKEN-CITATION carries its grounding-verifier reason; every SOURCED carries its `C-NNN` + (TIER-2) `source_file` or (TIER-1b) the draft-time verification note.
5. **Citation-determinism** — every SOURCED / BROKEN-CITATION / DEAD-PROVENANCE verdict is backed by a line in the citation-verification NDJSON (or, at TIER-1b, the draft-time verification file). No citation verdict is asserted without a ledger basis.
6. **Alignment-anti-fabrication** — no ACCEPTED-INFERENCE / STANDARD-RULE / OUT-OF-SCOPE-DEFAULT verdict without a named draft antecedent (a `[SRC]` anchor or a `§`-anchor + draft marker + resolver `id`); uncertain alignments are NOT-ALIGNABLE, never a manufactured antecedent; no verdict text uses the word "fabricated" of any unit.
7. **Capability-banner-present** — the artefact states the `capability_tier` and its confidence ceiling; the verdict respects the TIER-0 cap.
8. **Fenced-judgment** — ORPHAN / NOT-ALIGNABLE / DRIFTED / UNATTRIBUTED render as moderate-confidence bands with an observation, never a hard "this is fabricated/wrong." *(warn variant: a trace layer is `not-applicable` at this tier — documented in diagnostics.)*
9. **SHA match** — `REQUIREMENTS_SHA256` equals the Step-2 SHA-256 of `requirements/requirements.md`.
10. **Verdict consistency** — recompute the verdict from the untraceable counts + the TIER-0 cap; assert it equals the rendered value.

---

## Worked examples (the build-time decidability fixture)

A by-hand fixture (there is no live `requirements/requirements.md` in this generator repo). Real ID shapes; a mix of clean traces and seeded defects. Reference material, never a runtime input. Assume TIER-2.

| Unit | Final-doc value (abridged) | Draft antecedent | Ledger lookup | Verdict |
|---|---|---|---|---|
| F-01 | "…persist the invoice… [SRC: C-014]" | `[SRC: C-014]` | C-014 quote is a substring of `input/brief.md` | **SOURCED** |
| F-02 | "…export to PDF [SRC: C-031]" | `[SRC: C-031]` | C-031 **absent** from `draft-claims.ndjson` | **BROKEN-CITATION** (`tag_without_sidecar`) |
| F-03 | "…retain records for 7 years [SRC: C-009]" | `[SRC: C-009]` | C-009 quote = "kept for seven years" — **not a substring** of the cited file (value hand-edited from 5→7) | **BROKEN-CITATION** (`quote_not_found`) → also flagged **DRIFTED** in the drift list |
| BR-04 | "…manager approval over £10,000" | draft `[AI-SUGGESTED: AI-007]` | resolver AI-007 `status:"corrected"`, `resolved_value:"£10,000"` → final matches | **ACCEPTED-INFERENCE** |
| F-08 | "…confirm before delete" | draft `[STANDARD-RULE: GR-04]` | retained | **STANDARD-RULE** |
| UI-05 | "…session times out after 15 min" | draft `[AI-SUGGESTED: AI-012]` | resolver AI-012 `status:"dropped"` — yet present in final | **DROPPED-BUT-PRESENT** (merge defect) |
| F-11 | "…integrate with the billing gateway in real time" | **no** draft antecedent (inserted post-merge) | — | **ORPHAN** (no antecedent found; fenced) |
| NT-02 | "…notify the approver" | draft text "…alert the reviewer" (reworded by merge coherence sweep) | structural antecedent exists but reworded | **NOT-ALIGNABLE** (fenced; flagged for confirmation) |
| C-022 (prose, §2.1) | sidecar entry, no tag in final | — | `sidecar_entry_without_tag` (the domain note was dropped by merge) | **DEAD-PROVENANCE** (warn) |

**Untraceable Set (headline):** F-02 (broken), F-03 (broken), UI-05 (dropped-but-present), F-11 (orphan), NT-02 (not-alignable). **Drift & dead-provenance:** F-03 (drift), C-022 (dead). **Coverage:** Sourced 1 · Accepted-inference 1 · Standard-rule 1 (of 9 units). **Verdict: BLOCKED** (broken citations + dropped-but-present present).

This fixture exercises every verdict class and proves the decidable/fenced split: the citation verdicts (SOURCED/BROKEN/DEAD) come straight from the grounding-verifier engine; ACCEPTED-INFERENCE/STANDARD-RULE/DROPPED come from deterministic draft+resolver alignment; only F-11/NT-02 land in the fenced band, each quoted and flagged for the consultant rather than accused.

---

## Anti-patterns (binding on the reviewer)

- **Do not accuse fabrication.** The strongest orphan claim is *"no antecedent found in the draft or any ledger."* Never write "the consultant fabricated this."
- **Do not invent an antecedent or a trace.** Uncertain alignment is NOT-ALIGNABLE; a missing source is BROKEN-CITATION. Never manufacture a draft locator or a `C-NNN` to claim a trace (gate 6).
- **Do not assert a citation verdict without the ledger.** SOURCED / BROKEN / DEAD come from the grounding-verifier run (or the draft-time verification at TIER-1b), never from eyeballing (gate 5).
- **Do not silently certify on missing evidence.** A missing ledger lowers the capability tier and the verdict cap — it never becomes a clean pass (gate 7; TIER-0 cap).
- **Do not bury the untraceable result.** ORPHAN / BROKEN / DROPPED lead the artefact (gate 3); DRIFT / DEAD-PROVENANCE are warns lower down.
- **Do not re-grade content quality.** Ambiguity, testability, well-formedness are other lenses. This lens decides *where the content came from*, not *whether it is good*.
- **Do not write `[SRC: …]` / `[AI-SUGGESTED: AI-NN]` markers into the artefact.** The artefact *reports on* those markers; it does not carry its own. Reference units by requirement ID / `§`-anchor / `C-NNN` / `AI-NNN` as data, inside escaped evidence blocks.
- **Do not paraphrase the offending text.** Every defect quotes verbatim (gate 4).
- **Do not run as a background/sub-agent.** Foreground, same thread as the orchestrator (the citation band invokes the grounding-verifier *skill*, not an Agent).
- **Do not paste the artefact body into the conversation.** The file lands on disk; the consultant opens it.

## Stance summary

Requirements Traceability audits the provenance integrity of the merged spec: every fact should trace back to a real input source (decidable, via the grounding-verifier engine re-run against the final doc), an accepted AI-suggestion (mostly decidable, recovered through the marker-bearing draft + the resolver ledger), a standard rule, or a declared scope default. It leads with what traces to **nothing** — orphans, broken citations, and dropped-but-present content — because those are the actionable result and the real risk in an LLM-assembled, hand-editable spec. It degrades honestly across capability tiers when provenance assets are missing, fences ambiguous alignments rather than accusing fabrication, and never certifies a clean trace on absent evidence. A reviewer that invents an antecedent, asserts a citation verdict without the ledger, accuses fabrication on a fuzzy alignment, or buries the orphans below the diagrams has bent the methodology beyond its contract.
