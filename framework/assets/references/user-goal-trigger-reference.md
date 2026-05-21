<!-- ROLE: asset (reference). Conceptual scaffolding for `taxonomy-goals.md` and the §User goals authoring pattern in `topics-requirements.md` — not a deliverable. Trigger-mapping is not a discrete stage; the relevant content surfaces through requirements + the JTBD analysis (P2). -->

# User-goal trigger reference

> Conceptual seed. Trigger-mapping as a discrete stage doesn't exist in v7b — the relevant content is captured in `requirements.md > §User goals` (positive drivers, quality signals) and, optionally in P2, via the JTBD analysis (situation → motivation → expected outcome) and user-journeys analysis (emotional arc).

---

## Core idea worth keeping (from Effect Mapping, Balic & Domingues)

A user goal connects four things:

1. **Business objective** — what the business needs to achieve.
2. **Target-user persona** — who the user is.
3. **Driving forces** — what they want (positive) and what they fear (negative).
4. **Affordance** — what the application surfaces to honour the wants and guardrail the fears.

In v7b this collapses into the User-Goal definition in `taxonomy-goals.md`:

> **User Goal:** `{objective, context {frequency, expertise, stakes / error-cost}, quality dimension}`

The "driving forces" layer becomes the **quality signals** field — natural-language phrases like *"must not contain errors"*, *"50 times a day"*, *"scared of getting it wrong"* — which `taxonomy-goals.md` maps to trade-off-dimension positions (Accuracy, Power, Accuracy-emotional respectively).

---

## How v7b uses this conceptually

- **Wants → goal objectives + quality signals.** A persona's positive driver ("I want to settle disputes fast without back-and-forth") shapes the goal's objective and signals Speed-leaning quality.
- **Fears → guardrails + quality signals.** A persona's negative driver ("I'm scared of approving a fraudulent claim") signals Accuracy-leaning quality and drives confirmation/validation patterns in the design spec.
- **Business objective → goal-kind hierarchy.** Top-level business objectives map to top-level goals (which require their own `screen`); supporting objectives map to sub-level goals (which may share affordances with a parent screen).

---

## What v7b deliberately drops from v7a's trigger-mapping

| v7a element | Why dropped in v7b |
|---|---|
| Mermaid flow diagram (Business goals → Platform → Target groups → Driving forces) | Visual artifact, not spec content. v7b's relationships are captured by `taxonomy-goals.md`'s mapping table + cross-references in `requirements.md`. |
| Feature-impact prioritisation matrix | v7b doesn't prioritise features — it prioritises goals. Feature decisions emerge in the design spec's per-screen trade-off ratings. |
| Strategic-triangle / flywheel narrative | Marketing framework, not requirements engineering. |
| "Cross-group patterns" (shared / unique / conflicting drivers across personas) | Useful but informal — surfaces naturally during the requirements completeness report under "contradictory" findings. |
| MoSCoW prioritisation per goal | Replaced by goal-kind hierarchy (top-level / sub-level / interaction-level) in `taxonomy-goals.md`. Priority emerges from where the goal sits in the screen taxonomy, not from a separate ranking. |

---

## Quality-signal mapping (conceptual seed for `taxonomy-goals.md`)

| Phrase pattern | Trade-off position |
|---|---|
| "bulk" / "batch" / "50 times a day" | Power |
| "compliance" / "must not contain errors" | Accuracy |
| "occasional" / "self-service" | Simplicity |
| "quick" / "streamlined" | Speed |
| "dense" / "at a glance" | Density |
| "guided" / "don't overwhelm" | Focus |
| "worried" / "anxious" / "scared of getting it wrong" | Accuracy (emotional) |
| "biggest decision" / "life-changing" / "rare event" | Accuracy (stakes) |
| "clarity" / "one thing at a time" | Focus |

Negative drivers ("fears") are the strongest source of Accuracy-leaning signals. Positive drivers ("wants") are the strongest source of Speed/Power-leaning signals. The mapping is one-way: phrases in the inputs imply trade-off positions; the trade-offs feed into per-screen ratings in the design spec.
