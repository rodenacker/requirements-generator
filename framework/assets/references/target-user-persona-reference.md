<!-- ROLE: asset (reference). Reference shape only — actual target-user personas live in `requirements/requirements.md > §Target users`, never as a standalone asset. -->

# Target-user persona reference

> **Disambiguation:** A *target-user persona* is an end user of the application being designed (e.g. loan officer, customer, team lead). **Not** the Unicorn (LLM identity) and **not** the Consultant (audience). Target-user personas live in `requirements.md > §Target users` — they are spec content, not framework assets.
>
> This reference describes the *shape* a target-user persona should take when authored into a requirements spec.

---

## Required fields (canonical, from `topics-requirements.md`)

| Field | Description |
|---|---|
| **Role / job title** | The target-user identity preserved from inputs (e.g. *loan-officer*, *team-lead*). Drives role-gated UI in the design spec. |
| **Expertise level** | Domain expertise + tool-familiarity. Influences trade-off ratings (Power ↔ Simplicity, Memorability ↔ Density). |
| **Stakes / error-cost** | Consequence of getting it wrong. Influences trade-off ratings (Speed ↔ Accuracy). |

---

## Optional fields (lifted from v7a; useful when inputs warrant)

| Field | Description |
|---|---|
| **Frequency of use** | How often this persona uses the application. High frequency → Power-leaning; rare/high-stakes → Accuracy-leaning. |
| **Context** | Where, when, on what device. Drives layout/viewport decisions. |
| **Driving forces — wants** | Top 3 positive drivers. What they're hoping to achieve. Each pairs with a product affordance the design must surface. |
| **Driving forces — fears** | Top 3 negative drivers. What they're afraid of. Each pairs with a guardrail the design must include. |
| **Quality signals** | Natural-language phrases ("must not contain errors", "50 times a day", "occasional", "scared of getting it wrong"). Mapped via `taxonomy-goals.md` to the trade-off dimensions. |
| **Pain points with current tooling** | Sourced from §Source UI references in the inputs. Surfaces opportunity gaps. |

---

## Shape (markdown skeleton for use inside `requirements.md > §Target users`)

```markdown
### {{Persona name}} — {{Role}}

**One-line summary:** {{Sentence capturing who they are and what they do in this application's context}}

| Field | Value |
|---|---|
| Role | {{role}} |
| Expertise | {{novice / intermediate / expert}} in {{domain}} + {{novice / intermediate / expert}} in {{tool category}} |
| Stakes | {{description of consequence of error}} |
| Frequency | {{daily / weekly / occasional / rare}} |
| Context | {{where / when / on what device}} |

**Wants (positive drivers):**
1. {{want}} — {{why it matters}}
2. {{want}} — {{why it matters}}
3. {{want}} — {{why it matters}}

**Fears (negative drivers):**
1. {{fear}} — {{why it terrifies them}}
2. {{fear}} — {{why it terrifies them}}
3. {{fear}} — {{why it terrifies them}}

**Quality signals (verbatim phrases from inputs or consultant):**
- "{{phrase}}" → maps to {{trade-off dimension position}}

**Pain points with current tooling:**
- {{pain}} (source: §Source UI references > {{ref}})
```

---

## Authoring guidance

- **Preserve role exactly** as named in inputs. The role is the identity that drives role-gated UI in the design spec — losing the original term loses the link.
- **Use natural language for quality signals**, then map them to trade-off dimensions via `taxonomy-goals.md`. Don't invent a new ratings vocabulary.
- **Provenance markers apply.** Personas inferred from domain knowledge (no inputs name them) are marked `[AI-SUGGESTED]` at the heading level.
- **Multiple target-user personas are normal.** Record them all. Roles drive role-conditional CTAs, per-role views, and permission-gated affordances downstream.
- **Avoid pipeline-persona contamination.** Do not describe the consultant or the LLM here — those have their own asset files.

---

## What v7a had that v7b deliberately drops

- **Image-generation prompt sections** — out of scope for v7b (no asset generation).
- **Priority emojis (🎓 / 💼 / 🏠) and PRIMARY / SECONDARY / TERTIARY rankings** — v7b records all named target-user personas without ranking; goal-level prioritisation lives in §User goals + the JTBD analysis (P2).
- **Strategic-triangle / flywheel diagrams** — marketing-flywheel framing; not how v7b connects personas to UI. Personas connect to UI via §User goals (which name the actor) and per-role gating in the design spec.
- **Long Before/After transformation arcs** — narrative bloat; v7b favours dense, structured fields over storytelling.
