# analysis-selector.md

**Purpose:** Read `framework/assets/analyses/registry.md`, filter the methodologies whose `status` is `mvp`, present them to the consultant via `AskUserQuestion`, and return the consultant's selection as a structured row (the row's `name`, `analyser_agent`, `output_path`, `reference_asset`, `character`, `template_asset`, `map_skill`).

The skill is **read-only and synchronous**: one read, one prompt, one return. It does not invoke the analyser, does not touch state, and does not write any file.

## Inputs

- `framework/assets/analyses/registry.md` — the methodology registry. The frontmatter `methodologies:` list is the source of truth.

## Outputs

Exactly one of:

- **`selected`** — a structured row with the eight registry fields populated. The orchestrator consumes `name`, `analyser_agent`, and `output_path` directly; the analyser agent reads `reference_asset`, `character`, and `template_asset` at activation.
- **`cancelled`** — the consultant chose to cancel out of the selection prompt. The orchestrator exits cleanly without invoking any analyser.
- **`empty-registry`** — defensive: zero `mvp` rows were found in the registry. The orchestrator surfaces a configuration error and exits.

## Used by

- `framework/orchestrators/analyse-orch.md` — step 2.

## Procedure

1. **Read the registry.** `Read framework/assets/analyses/registry.md`. Parse the YAML frontmatter (the block between the opening `---` and the next `---`). Locate the `methodologies:` list.
2. **Filter to MVP.** Retain only rows whose `status` field equals the literal string `mvp`. Discard `status: future` rows and any row whose `status` field is absent.
3. **Defensive guard.** If the filtered list is empty, return `empty-registry`. Do not surface an `AskUserQuestion` with no options.
4. **Build the choice set.** For each retained row, prepare one `AskUserQuestion` option:
    - `label` — the row's `name` field, prefixed with `/` for visual consistency with slash commands (e.g. `ooux` → `/ooux`). If only one MVP row exists, this option is still presented (the consultant must confirm — keeps the UX consistent for when 2+ methodologies arrive).
    - `description` — the row's `description` field, verbatim.
    - Append one additional option at the end: `label: "Cancel"`, `description: "Exit /analyse without running an analysis."`.
5. **Surface the prompt.** Call `AskUserQuestion`:
    - `question`: *"Which analysis methodology would you like to run?"*
    - `header`: `Methodology`
    - `multiSelect`: `false`
    - `options`: the list built in step 4.
6. **Return the consultant's choice.**
    - If the consultant selected a methodology row: return `selected` with the full row payload (all eight registry fields).
    - If the consultant selected `Cancel`: return `cancelled`.
    - If the consultant selected the harness-provided "Other" override with free text: treat as `cancelled` and surface a one-line note that free-text input is not supported here — the orchestrator can re-invoke `/analyse` for a clean retry.

## Self-validation

- Exactly one prompt was surfaced. The skill does not loop.
- The returned row (when `selected`) has every required field populated (`name`, `analyser_agent`, `output_path`, `reference_asset`, `character`). The `template_asset` and `map_skill` fields may be `null` for methodologies that don't require them.
- The `Cancel` option appears last in the list and is always present.

## Anti-Patterns

- Do not hardcode methodology names. The registry is the source of truth; the selector must work unchanged when a new MVP row is added.
- Do not invoke the analyser from this skill. Selection and invocation are separate concerns — the orchestrator owns invocation.
- Do not write to disk. This skill has no side effects beyond the single `AskUserQuestion` surface.
- Do not silently skip rows with malformed frontmatter (missing required fields on an `mvp` row). Surface `empty-registry` and let the orchestrator report a configuration error rather than presenting a half-populated option that would crash on selection.
- Do not present `status: future` rows even with a "coming soon" suffix. Future rows do not have analyser agents on disk — selecting them would crash the orchestrator.
