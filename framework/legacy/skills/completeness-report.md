<!-- ROLE: skill. STATUS: stub — author during phase-1 build-order step 3. -->

# completeness-report.md

**Purpose:** Reusable adversarial review skill used by both `/requirements` and `/design`. Produces a structured report with three categories of finding (AI-suggested / vague / contradictory) and three severity levels (blocker / major / minor — informational, not gating). Writes `completeness_hash` into `.progress.json` and persists the report to disk.

**Inputs:** the relevant spec file (`requirements.md` or `design-spec.md`), `assets/topics-*.md`, the stage-specific review character (`characters/requirements-review.md` or `characters/design-review.md`).

**Outputs:**
- Terminal: report surfaced in conversation.
- Disk: `artifacts/<stage>/completeness-reports/completeness-report.md` (single file, overwritten each run).
- `.progress.json`: `completeness_hash = sha256(<spec>)`, increments `completeness_iterations`.

**Used by:**
- `framework/orchestrators/requirements-orch.md` — step 4.
- `framework/orchestrators/design-orch.md` — step 3.

**Used how:** Domain-free skill; loaded with the stage-specific review character. Capped at 3 iterations since last Accept attempt. The Accept gate refuses unless `completeness_hash == sha256(current_spec)`.

**Topic-driven checks (requirements stage):** sourced from `assets/topics-requirements.md > Pre-authoring invariants` and aligned with the Tier A/B/D rules in `framework/skills/completeness-gap-pass.md`. The skill emits a finding when any of the following fails:

- **Tier A (hard bijections):** A1–A9 as previously plus A10 (§1.5 has ≥1 In row), A11 (§2.5 covers state-named invariants when emitted), A12 (§6.7 source concepts resolve), A13 (§6.8 audience resolves), A14 (§6.10 op maps to §6.1 F-NN), A15 (§7.X derived shape resolves) — full text in `framework/skills/completeness-gap-pass.md`.
- **Tier B (soft references):** B1–B3 as previously plus B4 (§1.7 driving-requirement cross-refs) and B5 (acceptance-criteria populated on stories / F / BR / flow steps).
- **Tier D (mixed, in-scope only when visually manifested):** D1 (aggregate invariants → BR projection), D2 (§7 shape field-level UI-display test), D3 (§2.5 server-only effects), D4 (§6.7 audience has §6.5 read).
- **Tier C (out-of-scope, do not gate suggestions):** §6.6.5 Accessibility gating only. The other §6.6 sub-sections (§6.6.1 Session UX, §6.6.2 FE performance, §6.6.4 Compliance UI behaviour) are now FE-relevant and may carry `[AI-SUGGESTED]` when inferred — they no longer gate completeness, but emptiness is uncommon since `GR-19` and domain-inference populate them. (§6.6.3 Availability has been retired entirely from the template.)
- **Marker hygiene:** every `[AI-SUGGESTED]` field passes the precedence check — no `framework/shared/general-rules.md` rule covered the case (else it would be `[STANDARD-RULE]`).

> Content TBD per `plan/v7b-Brief.md > §Completeness report (reusable skill)`. Design-time rubric seed lives in `plan/completeness-report-rubric-seed.md`.
