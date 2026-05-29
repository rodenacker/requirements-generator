---
description: List available workflow commands and launch the one you pick.
---

You are the dispatcher for `/start`. Your only job is to show the user the available workflow commands as a numbered list and launch the one they choose by number. Do nothing else.

## Steps

1. **Discover commands.**
   - `Glob` pattern `.claude/commands/*.md`.
   - Exclude `.claude/commands/start.md` (this file).
   - Exclude any `.claude/commands/claude-flow-*.md` — these are external claude-flow CLI reference docs, not workspace pipelines, and must never appear in the menu.
   - For each remaining file:
     - The command name is the filename without `.md` (e.g. `requirements.md` → `requirements`).
     - `Read` the file and extract the `description:` value from the YAML frontmatter (the single line beginning with `description:` between the opening and closing `---`).
   - If a file has no `description:` line, skip it.

2. **Order the commands.** Present the discovered commands in this fixed display order:

   1. `requirements`
   2. `generate-prd`
   3. `design-system`
   4. `review-inputs`
   5. `analyse-inputs`
   6. `review-requirement`
   7. `analyse-requirement`
   8. `wireframe`

   Any discovered command **not** in this list (e.g. a newly added command) is appended after the fixed list, in discovery order. Any name in the fixed list that was **not** discovered on disk is silently skipped (do not print a dead entry). This keeps the menu fresh while honouring the consultant's preferred ordering.

3. **Show the list and ask for a number.** Print the menu as plain Markdown text — **do not** use `AskUserQuestion`. Use this shape:

   ```
   Which workflow would you like to start?

   1. **/<name>** — <description>
   2. **/<name>** — <description>
   …
   N. **/<name>** — <description>

   0. Cancel — exit without launching a workflow

   Reply with the number of the pipeline to launch (or 0 to cancel):
   ```

   where each `<name>` is the command name (with a leading `/`) and `<description>` is the `description:` value extracted in step 1. Number the rows starting at **1** in the order from step 2; let `N` be the highest number. Then end the turn — the consultant's next chat message is the reply.

4. **Parse the reply.** On the reply turn:
   - **Normalize** — trim whitespace, lowercase.
   - **Cancel** — if the reply is `0`, `cancel`, `q`, or `exit`, output *"Cancelled. No workflow launched."* and stop.
   - **Valid number** — if the reply parses cleanly as an integer `k` with `1 ≤ k ≤ N`, advance to step 5 with the `k`-th command as the selection.
   - **Invalid** — anything else (non-numeric, out of range, empty, mixed text+number) is invalid. Print *"Invalid selection. Enter a number from 1–N, or 0 / cancel / q / exit to cancel."*, then re-print the full numbered list + prompt line (same shape as step 3) and end the turn. Retry budget is **2 re-prompts**: on the third consecutive invalid reply, print *"Too many invalid selections. Cancelling."* and stop.

5. **Launch the selection.**
   - Take the chosen command's name, strip any leading `/`, and invoke `Skill` with `skill` set to that name.
   - That skill's own instructions take over from here.

6. **Stop.** Do not run any further tools, do not summarise, do not narrate. Once `Skill` is invoked, `/start` is done — the launched workflow owns the rest of the turn.

## Constraints

- Always show the options as a numbered Markdown list and accept a typed number. Never use `AskUserQuestion` for the menu.
- Never include `/start` itself in the option list, and never include `claude-flow-*` commands.
- Never inline or paraphrase the chosen command's body — always dispatch via `Skill`.
- Always re-discover the command set from `.claude/commands/` on each invocation. The fixed order in step 2 governs only display sequence, not membership — newly added commands still appear (appended), and removed commands disappear.
