# analysis-selector.md

**Purpose:** Read a methodology registry, filter the methodologies whose `status` is `mvp`, present them to the consultant as a printed numbered list, parse the consultant's typed reply, and return the consultant's selection as a structured row (the row's `name`, `analyser_agent`, `output_path`, `reference_asset`, `character`, `template_asset`, `map_skill`).

The skill is **read-only**: one read, one printed list (plus up to two re-prompts on invalid input), one return. It does not invoke the analyser, does not touch state, and does not write any file.

The skill is pipeline-neutral: it works against any registry that follows the field-shape contract documented in `framework/assets/analyses/registry.md`. The caller supplies the registry path; the skill does not hardcode it.

## Inputs

- `registry_path` — repo-relative path to the methodology registry file. Required. Examples in current use: `framework/assets/analyses/registry.md` (for `/analyse-requirement`), `framework/assets/analyses-inputs/registry.md` (for `/analyse-inputs`). The file must carry a YAML frontmatter `methodologies:` list whose rows match the field-shape contract documented in the requirements-analyses registry.

## Outputs

Exactly one of:

- **`selected`** — a structured row with the eight registry fields populated. The orchestrator consumes `name`, `analyser_agent`, and `output_path` directly; the analyser agent reads `reference_asset`, `character`, and `template_asset` at activation.
- **`cancelled`** — the consultant chose to cancel out of the selection prompt. The orchestrator exits cleanly without invoking any analyser.
- **`empty-registry`** — defensive: zero `mvp` rows were found in the registry. The orchestrator surfaces a configuration error and exits.

## Used by

- `framework/orchestrators/analyse-requirement-orch.md` — step 1, with `registry_path: "framework/assets/analyses/registry.md"`.
- `framework/orchestrators/analyse-inputs-orch.md` — step 0, with `registry_path: "framework/assets/analyses-inputs/registry.md"`.

## Procedure

1. **Read the registry.** `Read` the file at `registry_path`. Parse the YAML frontmatter (the block between the opening `---` and the next `---`). Locate the `methodologies:` list.
2. **Filter to MVP.** Retain only rows whose `status` field equals the literal string `mvp`. Discard `status: future` rows and any row whose `status` field is absent.
3. **Defensive guard.** If the filtered list is empty, return `empty-registry`. Do not surface an `AskUserQuestion` with no options.
4. **Build the numbered list.** Number the retained rows starting at **1**, in **registry order** (the order they appear in `registry.md` frontmatter). Do **not** re-sort. For each row, format a two-line block:

    `{{n}}. {{name}}`
    `{{description}}`

    where `{{n}}` is the 1-based index, `{{name}}` is the row's `name` field verbatim (no `/` prefix), and `{{description}}` is the row's `description` field verbatim on the next line. No leading indent. Rows are separated from each other by a single blank line.

    After the methodology lines, append a blank line and a trailing cancel line:

    `0. Cancel — exit without running an analysis`

    Let `N` be the count of MVP rows (and therefore the highest valid selection number).

5. **Surface the prompt and parse the reply.** Print the assembled block to the consultant as plain text in this shape:

    ```
    Available analyses:

    1. <name>
    <description>

    2. <name>
    <description>

    …

    N. <name>
    <description>

    0. Cancel — exit without running an analysis

    Enter the number of the analysis to run (or 0 to cancel):
    ```

    Then end the turn. The consultant's next chat message is the reply. On that turn:

    1. **Normalize** the reply — trim leading/trailing whitespace, lowercase.
    2. **Cancel keywords** — if the normalized reply equals `0`, `cancel`, `q`, or `exit`, return `cancelled` (skip to step 6).
    3. **Numeric parse** — if the reply parses cleanly as an integer `k` with `1 ≤ k ≤ N`, advance to step 6 with the `k`-th MVP row as the selection.
    4. **Invalid** — anything else (non-numeric text, out-of-range number, empty reply, mixed text+number) is invalid. Print one line:

        *"Invalid selection. Enter a number from 1–{{N}}, or 0 / cancel / q / exit to cancel."*

        Then re-print the full numbered list + prompt line (same shape as above), end the turn, and parse the next reply through the same loop.

    5. **Retry budget** — keep an in-memory counter of invalid replies for this skill invocation. The budget is **2 re-prompts**: on the **third** consecutive invalid reply (counter would become 3), stop re-prompting, print one final line *"Too many invalid selections. Cancelling."*, and return `cancelled`. Do not persist the counter — it resets on every fresh invocation.

6. **Return the consultant's choice.**
    - If a valid numeric selection was parsed at step 5.3: return `selected` with the full row payload (all eight registry fields).
    - If a cancel keyword was parsed at step 5.2, or the retry budget was exhausted at step 5.5: return `cancelled`.

## Self-validation

- The numbered list was printed at most three times in total (initial print plus up to two re-prompts on invalid input). The skill never loops indefinitely.
- Methodologies were numbered in registry order; no row was re-sorted alphabetically or otherwise.
- `0` and `cancel` / `q` / `exit` (case-insensitive, with whitespace trimmed) were honoured as cancel signals at every prompt.
- The `0. Cancel — …` line was the last line above the prompt at every print, and the prompt line was *"Enter the number of the analysis to run (or 0 to cancel):"*.
- The returned row (when `selected`) has every required field populated (`name`, `analyser_agent`, `output_path`, `reference_asset`, `character`). The `template_asset` and `map_skill` fields may be `null` for methodologies that don't require them.
- The retry budget was respected — exactly **2** re-prompts are permitted; the third invalid reply returns `cancelled` with the *"Too many invalid selections."* line.

## Anti-Patterns

- Do not call `AskUserQuestion` from this skill. The selector renders a numbered list as plain text and parses the consultant's typed reply on the next turn. `AskUserQuestion` would re-introduce structured radio UI and defeat the consultant's chosen terminal-style UX.
- Do not re-prompt more than twice. The retry budget is two re-prompts; the third invalid reply must return `cancelled`. Looping further turns a typo into a stuck conversation.
- Do not re-sort the methodologies. Registry order is the source of truth — re-sorting alphabetically (or by any other key) would change the numbering whenever a row is added, removed, or promoted from `future` to `mvp`.
- Do not hardcode methodology names. The registry is the source of truth; the selector must work unchanged when a new MVP row is added.
- Do not hardcode the registry path. `registry_path` is a required input parameter; the skill must work unchanged against any registry that follows the documented field-shape contract.
- Do not invoke the analyser from this skill. Selection and invocation are separate concerns — the orchestrator owns invocation.
- Do not write to disk. This skill has no side effects beyond the printed list and any re-prompts.
- Do not silently skip rows with malformed frontmatter (missing required fields on an `mvp` row). Surface `empty-registry` and let the orchestrator report a configuration error rather than printing a half-populated line that would crash on selection.
- Do not present `status: future` rows even with a "coming soon" suffix. Future rows do not have analyser agents on disk — selecting them would crash the orchestrator.
- Do not accept partial-match or fuzzy-keyword cancel inputs (e.g. `c`, `quit`, `nope`, `n`). Only the exact normalized tokens `0`, `cancel`, `q`, `exit` are cancel signals; everything else is invalid and re-prompts (until the retry budget is exhausted).
