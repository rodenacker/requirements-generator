# analysis-selector.md

**Purpose:** Read a methodology registry, filter the methodologies whose `status` is `mvp`, present them to the consultant as a printed numbered list — **clustered by lens group, with the next un-run methodology flagged `★ suggested next` and already-produced ones marked `✓ already run`** — parse the consultant's typed reply, and return the consultant's selection as a structured row (the row's `name`, `output_path`, `reference_asset`, `character`, `template_asset`, `map_skill`, plus the caller-specific agent-pointer field — `analyser_agent` in analyses registries or `reviewer_agent` in reviews registries).

The ordering and flags are derived **purely from the options** — the registry's curated order, each row's declared `group`, and whether each row's `output_path` already resolves on disk. The skill reads **no** target document (not `requirements/requirements.md`, not `input/` material), so its recommendation costs only one registry read plus one cheap `Glob` per row and can never assert a stale claim about document content.

The skill is **read-only**: one registry read plus a cheap on-disk presence probe (one `Glob` per MVP row, existence only), one printed list (plus up to two re-prompts on invalid input), one return. It does not invoke the chosen agent, does not touch state, and does not write any file.

The skill is pipeline-neutral: it works against any registry that follows the field-shape contract documented in `framework/assets/analyses/registry.md`. The caller supplies the registry path; the skill does not hardcode it.

The skill's printed prompt nouns ("Available analyses:" and "Enter the number of the analysis to run") are also caller-parameterisable via the optional `list_label` and `verb_label` inputs below. Callers that select reviews rather than analyses (e.g. `/review-inputs`) pass `list_label: "reviews"` and `verb_label: "review"` so the prompt reads naturally; callers that omit these inputs get the analysis-flavoured defaults unchanged.

## Inputs

- `registry_path` — repo-relative path to the methodology registry file. Required. Examples in current use: `framework/assets/analyses/registry.md` (for `/analyse-requirement`), `framework/assets/analyses-inputs/registry.md` (for `/analyse-inputs`), `framework/assets/reviews-inputs/registry.md` (for `/review-inputs`). The file must carry a YAML frontmatter `methodologies:` list whose rows match the field-shape contract documented in the requirements-analyses registry.
- `list_label` — optional string used in the printed list heading `Available <list_label>:`. Default: `"analyses"`. Callers selecting reviews pass `"reviews"`.
- `verb_label` — optional string used in the printed prompt `Enter the number of the <verb_label> to run (or 0 to cancel):`. Default: `"analysis"`. Callers selecting reviews pass `"review"`.

## Outputs

Exactly one of:

- **`selected`** — a structured row with every registry field populated, returned verbatim from the YAML row. The orchestrator consumes `name`, `output_path`, and the per-pipeline agent-pointer field — `analyser_agent` for analyses pipelines, `reviewer_agent` for reviews pipelines — directly; the chosen agent reads `reference_asset`, `character`, and `template_asset` at activation. The selector does not rename or normalise the agent-pointer field; it returns whatever the row carries.
- **`cancelled`** — the consultant chose to cancel out of the selection prompt. The orchestrator exits cleanly without invoking any analyser or reviewer.
- **`empty-registry`** — defensive: zero `mvp` rows were found in the registry. The orchestrator surfaces a configuration error and exits.

## Used by

- `framework/orchestrators/analyse-requirement-orch.md` — step 1, with `registry_path: "framework/assets/analyses/registry.md"` (default labels).
- `framework/orchestrators/analyse-inputs-orch.md` — step 0, with `registry_path: "framework/assets/analyses-inputs/registry.md"` (default labels).
- `framework/orchestrators/review-inputs-orch.md` — step 0, with `registry_path: "framework/assets/reviews-inputs/registry.md"`, `list_label: "reviews"`, `verb_label: "review"`.
- `framework/orchestrators/review-requirement-orch.md` — step 1, with `registry_path: "framework/assets/reviews/registry.md"`, `list_label: "reviews"`, `verb_label: "review"`. (Migrated from the retired `review-selector.md`; `/review-requirement` is the skill's fourth caller.)

## Procedure

1. **Read the registry.** `Read` the file at `registry_path`. Parse the YAML frontmatter (the block between the opening `---` and the next `---`). Locate the `methodologies:` list.
2. **Filter to MVP.** Retain only rows whose `status` field equals the literal string `mvp`. Discard `status: future` rows and any row whose `status` field is absent.
3. **Defensive guard.** If the filtered list is empty, return `empty-registry`. Do not surface an `AskUserQuestion` with no options.
3a. **History probe (on-disk presence).** For each retained MVP row, `Glob` its `output_path` to determine whether that artefact already exists on disk. Mark the row `already_run = true` when the file resolves, `false` otherwise. This is an **existence check only** — never read the file's contents. (Precedent: `framework/skills/select-supporting-analyses.md` performs the same `Glob`-of-`output_path` probe.)

3b. **Presentation order, groups, and suggested-next.** Establish the presentation order: walk the MVP rows in registry order and cluster them by their `group` field — each distinct `group` value forms a group, groups appear in the order their first member is encountered, and rows keep registry order within their group. A row with no `group` field joins a trailing group labelled `Other`. Then compute **suggested-next** = the first row in this presentation order whose `already_run` is `false`. If every row is `already_run`, there is no suggested-next (see the all-run note in step 4).

4. **Build the grouped numbered list.** Number the rows starting at **1** in **presentation order** (the clustered order from step 3b); numbering is continuous across groups. For each row, format a two-line block:

    `{{n}}. {{name}}{{mark}}`
    `{{description}}`

    where `{{n}}` is the 1-based index, `{{name}}` is the row's `name` field verbatim (no `/` prefix), `{{description}}` is the row's `description` field verbatim on the next line, and `{{mark}}` is:
    - ` ★ suggested next` when the row is the suggested-next row,
    - ` — ✓ already run` when `already_run` is `true` (mutually exclusive with `★`, since suggested-next is by definition un-run),
    - empty otherwise.

    No leading indent. Rows are separated from each other by a single blank line. Immediately before the first row of each group, emit a blank line and a **group header line** — the group's label verbatim (e.g. `Objects, data & lifecycle`). `✓ already run` rows keep their number and remain selectable (the consultant may re-run them).

    After the methodology lines, append a blank line and a trailing cancel line:

    `0. Cancel — exit without running a {{verb_label}}`

    (With the default `verb_label: "analysis"` this renders as `0. Cancel — exit without running an analysis`. Callers passing `verb_label: "review"` render `0. Cancel — exit without running a review`.)

    Let `N` be the count of MVP rows (and therefore the highest valid selection number).

5. **Surface the prompt and parse the reply.** Print the assembled block to the consultant as plain text in this shape (substituting `{{list_label}}` and `{{verb_label}}` from the inputs; defaults `"analyses"` and `"analysis"` preserve historical wording):

    ```
    Available {{list_label}}:

    Suggested next: <suggested-next name> — <its group>

    <Group A label>

    1. <name> ★ suggested next
    <description>

    2. <name> — ✓ already run
    <description>

    <Group B label>

    3. <name>
    <description>

    …

    N. <name>
    <description>

    0. Cancel — exit without running a {{verb_label}}

    Enter the number of the {{verb_label}} to run (or 0 to cancel):
    ```

    (When every MVP row is already run, replace the `Suggested next:` line with `All {{list_label}} have been run — pick any to re-run and refresh it.` and render no `★`. The `Suggested next:` line always names the same row that carries the inline `★`. A row with no `group` field appears under a trailing `Other` header.)

    Then end the turn. The consultant's next chat message is the reply. On that turn:

    1. **Normalize** the reply — trim leading/trailing whitespace, lowercase.
    2. **Cancel keywords** — if the normalized reply equals `0`, `cancel`, `q`, or `exit`, return `cancelled` (skip to step 6).
    3. **Numeric parse** — if the reply parses cleanly as an integer `k` with `1 ≤ k ≤ N`, advance to step 6 with the row occupying position `k` in the **presentation order** (the numbered list printed in step 4) as the selection. The number maps to the printed position, not to registry order.
    4. **Invalid** — anything else (non-numeric text, out-of-range number, empty reply, mixed text+number) is invalid. Print one line:

        *"Invalid selection. Enter a number from 1–{{N}}, or 0 / cancel / q / exit to cancel."*

        Then re-print the full numbered list + prompt line (same shape as above), end the turn, and parse the next reply through the same loop.

    5. **Retry budget** — keep an in-memory counter of invalid replies for this skill invocation. The budget is **2 re-prompts**: on the **third** consecutive invalid reply (counter would become 3), stop re-prompting, print one final line *"Too many invalid selections. Cancelling."*, and return `cancelled`. Do not persist the counter — it resets on every fresh invocation.

6. **Return the consultant's choice.**
    - If a valid numeric selection was parsed at step 5.3: return `selected` with the full row payload (all eight registry fields).
    - If a cancel keyword was parsed at step 5.2, or the retry budget was exhausted at step 5.5: return `cancelled`.

## Self-validation

- The numbered list was printed at most three times in total (initial print plus up to two re-prompts on invalid input). The skill never loops indefinitely.
- Methodologies were presented clustered by their declared `group` (groups in first-appearance order, registry order preserved within each group); no row was sorted by `name`, `description`, or any key other than this stable grouping.
- Each MVP row's `output_path` was probed once via `Glob`; rows whose output exists were marked `✓ already run`, and the first un-run row in presentation order was flagged `★ suggested next` (or, when every row is already run, the "all run — re-run any to refresh" note was shown instead, with no `★`).
- The history probe was `Glob`-only (existence); no target document (`requirements/requirements.md` or `input/`) was read.
- `0` and `cancel` / `q` / `exit` (case-insensitive, with whitespace trimmed) were honoured as cancel signals at every prompt.
- The `0. Cancel — …` line was the last line above the prompt at every print, and the prompt line was *"Enter the number of the {{verb_label}} to run (or 0 to cancel):"* (with `{{verb_label}}` substituted from the input; default `"analysis"`).
- The returned row (when `selected`) has every required field populated (`name`, `output_path`, `reference_asset`, `character`, and the caller-specific agent-pointer field — `analyser_agent` for analyses-pipeline registries or `reviewer_agent` for reviews-pipeline registries). The `template_asset` and `map_skill` fields may be `null` for methodologies that don't require them.
- The retry budget was respected — exactly **2** re-prompts are permitted; the third invalid reply returns `cancelled` with the *"Too many invalid selections."* line.

## Anti-Patterns

- Do not call `AskUserQuestion` from this skill. The selector renders a numbered list as plain text and parses the consultant's typed reply on the next turn. `AskUserQuestion` would re-introduce structured radio UI and defeat the consultant's chosen terminal-style UX.
- Do not re-prompt more than twice. The retry budget is two re-prompts; the third invalid reply must return `cancelled`. Looping further turns a typo into a stuck conversation.
- Do not sort the methodologies by `name`, `description`, or any key other than the stable `group` clustering. Registry order is the curated recommended sequence; the selector clusters rows by their declared `group` (groups in first-appearance order, registry order preserved within each group) and annotates them with `★`/`✓` marks, but never reorders within a group and never sorts alphabetically. Adding, removing, or promoting a row must not change the relative order of the others.
- Do not read the target document to compute the ordering. Ordering and flags come only from the registry (curated order + `group`) and the `Glob` presence probe of each `output_path`. Reading `requirements/requirements.md` or `input/` material here would add cost and risk a recommendation that goes stale when the consultant edits those documents — the selector deliberately asserts nothing about document content.
- Do not hide, drop, or auto-select any MVP row based on the `★`/`✓` marks. The marks are advisory; every MVP methodology stays visible, numbered, and selectable (including already-run ones, which are re-runnable).
- Do not hardcode methodology names. The registry is the source of truth; the selector must work unchanged when a new MVP row is added.
- Do not hardcode the registry path. `registry_path` is a required input parameter; the skill must work unchanged against any registry that follows the documented field-shape contract.
- Do not hardcode the printed prompt nouns. `list_label` and `verb_label` are optional input parameters with backwards-compatible defaults; the skill must substitute them into the printed list heading, the cancel-line tail, and the prompt line so callers selecting reviews (rather than analyses) read naturally.
- Do not invoke the chosen agent (analyser or reviewer) from this skill. Selection and invocation are separate concerns — the orchestrator owns invocation.
- Do not write to disk. This skill has no side effects beyond the printed list and any re-prompts.
- Do not silently skip rows with malformed frontmatter (missing required fields on an `mvp` row). Surface `empty-registry` and let the orchestrator report a configuration error rather than printing a half-populated line that would crash on selection.
- Do not present `status: future` rows even with a "coming soon" suffix. Future rows do not have analyser agents on disk — selecting them would crash the orchestrator.
- Do not accept partial-match or fuzzy-keyword cancel inputs (e.g. `c`, `quit`, `nope`, `n`). Only the exact normalized tokens `0`, `cancel`, `q`, `exit` are cancel signals; everything else is invalid and re-prompts (until the retry budget is exhausted).
