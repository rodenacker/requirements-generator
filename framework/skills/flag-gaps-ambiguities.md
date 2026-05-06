# flag-gaps-ambiguities.md

**Purpose:** Decide whether a candidate follow-up question on an answered Q&A item should be asked, short-circuited by a `general-rules.md` answer, or recorded as an out-of-scope domain default. Applies inside the resolver's contradiction-spotting / ambiguity check, after the consultant has answered an `[AI-SUGGESTED]` item but before the resolver phrases a follow-up.

**Inputs:**
- The current Q&A item (manifest entry from `framework/state/resolver-manifest.ndjson`): `id`, `section_heading`, `source_location`, `original_suggestion`, `classification`.
- The consultant's most recent answer for the item, plus any follow-ups already captured for it in `framework/state/resolver-answers.ndjson` (one resolved entry per line).
- The candidate follow-up the resolver is considering.
- `framework/shared/prototype-scope.index.md` — slim heading-only index of out-of-scope categories. Loaded by the resolver at start.
- `framework/shared/general-rules.index.md` — slim one-line-per-rule index of `GR-NN` rules. Loaded by the resolver at start.
- `framework/shared/prototype-scope.md` — full body of the scope predicate. Read on demand only when step 3 fires `defer-out-of-scope` and a precise bullet wording is needed.
- `framework/shared/general-rules.md` — full body of the rules catalogue. Read on demand only when step 2 fires `apply-rule` and the rule's full canonical answer text is needed for `follow_ups[*].a`.

**Outputs:** exactly one action per candidate follow-up, recorded in the item's `follow_ups` array.

| Action | When | Recorded as |
|---|---|---|
| `no-followup-needed` | Answer is already unambiguous, consistent, and complete | nothing — resolver advances to the next item or batch |
| `apply-rule` | A `GR-NN` rule's scope predicate covers the territory the follow-up would probe | `{q, a: "<rule canonical answer>", action: "apply-rule", gr_id: "GR-NN"}` |
| `defer-out-of-scope` | The territory is out-of-scope per `prototype-scope.md` (e.g. backend internals, infra, DB schema, performance optimisation) | `{q, a: "<domain default>", action: "defer-out-of-scope", scope_reason: "<one-line scope category>"}` |
| `ask` | Territory is in-scope and no `GR-NN` covers it | `{q, a: "<consultant answer>", action: "ask"}` after the consultant responds |

**Used by:**
- `framework/agents/requirements-resolver.md` — Phase 1 follow-ups on a single blocking item, and Phase 2 escalations of an unclear non-blocking item out of its batch into a Level 1 follow-up.

## Decision tree (per candidate follow-up)

Walk in order. Stop at the first match.

1. **Ambiguity check.** A follow-up is only justified if the most recent answer is ambiguous, contradictory, or incomplete with respect to (a) the item's `original_suggestion` or (b) the previously captured answers. If the answer is already clear, output `no-followup-needed` — the resolver advances.
2. **General-rules lookup.** Consult the in-context `framework/shared/general-rules.index.md` first — match the candidate follow-up's territory against each rule's *Applies to* line. If a `GR-NN` row matches, output `apply-rule` with that `gr_id`. Read the matching `## GR-NN` section from `framework/shared/general-rules.md` on demand to copy the canonical answer text into `a`. The resolver records the action and does not ask.
3. **Scope check.** Consult the in-context `framework/shared/prototype-scope.index.md` first — match the territory against the "Not Prototypable" categories. If a category matches, output `defer-out-of-scope` with a one-line `scope_reason` quoting the relevant category, and a sensible domain default as the `a` value. Read the full bullet from `framework/shared/prototype-scope.md` on demand only if the precise wording is needed for `scope_reason`. The resolver records the action and does not ask.
4. **Otherwise.** Output `ask`. The resolver phrases and asks the candidate follow-up; the consultant's verbatim response becomes `a`.

The filter is a safety net for **answer-induced expansion** — a follow-up the consultant's response unlocks. It is not a re-check of manifest items, which the drafter has already filtered at gap-pass time via `framework/skills/completeness-gap-pass.md`.

## Match strictness

- **General-rules match** is exact: the candidate follow-up must concern the same template field/element the rule's *Applies to* clause names. Adjacent territory does not match — when in doubt, fall through to step 3.
- **Out-of-scope match** uses `prototype-scope.md`'s "Not Prototypable (Filter Out)" list as the strict predicate. Anything in "Prototypable (In Scope)" — including the conditional clauses that admit a topic only as visual manifestation — is in-scope and falls through to step 4.
- Ambiguity defaults to `ask`. False positives cost a question; false negatives cost a guess shipping unchallenged.

## Recording the action

The resolver appends one entry per candidate follow-up to the item's `follow_ups` array in `framework/state/resolver-answers.ndjson` (one resolved entry per line; the array lives inside that line's JSON object). Schema (additive — `q` and `a` remain primary; the merger reads only those):

```json
{
  "q": "<candidate question text>",
  "a": "<consultant answer | rule canonical answer | domain default>",
  "action": "ask | apply-rule | defer-out-of-scope",
  "gr_id": "<GR-NN, present only when action = apply-rule>",
  "scope_reason": "<one-line category from prototype-scope.md, present only when action = defer-out-of-scope>"
}
```

`no-followup-needed` is not recorded — the absence of an entry is the signal.

## Anti-Patterns

- Do not consult this skill to re-filter the manifest's original `[AI-SUGGESTED]` items; those have already been filtered by the drafter. This skill applies only to follow-ups the answer unlocks.
- Do not output `ask` when an exact `GR-NN` match exists; the rule is canonical and skipping it re-introduces the cycle the rule was added to remove.
- Do not output `defer-out-of-scope` for territory that is in-scope but inconveniently broad. Apply the `prototype-scope.md` predicate strictly.
- Do not silently drop a follow-up. Every candidate produces exactly one of `{no-followup-needed, ask, apply-rule, defer-out-of-scope}`.
- Do not invent a `GR-NN` ID. If no rule covers the territory, fall through.
