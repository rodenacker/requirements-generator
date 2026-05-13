---
description: List available workflow commands and launch the one you pick.
---

You are the dispatcher for `/start`. Your only job is to show the user the available workflow commands and launch the one they choose. Do nothing else.

## Steps

1. **Discover commands.**
   - `Glob` pattern `.claude/commands/*.md`.
   - Exclude `.claude/commands/start.md` (this file).
   - For each remaining file:
     - The command name is the filename without `.md` (e.g. `requirements.md` → `requirements`).
     - `Read` the file and extract the `description:` value from the YAML frontmatter (the single line beginning with `description:` between the opening and closing `---`).
   - If a file has no `description:` line, skip it.

2. **Ask the user to choose.**
   - Call `AskUserQuestion` with one question: `"Which workflow would you like to start?"`.
   - Set `header` to `"Workflow"`. Set `multiSelect` to `false`.
   - One option per discovered command:
     - `label` = `/<command-name>` (e.g. `/requirements`).
     - `description` = the `description:` value you extracted.
   - If more than 4 commands are discovered, list the first 3 and add a 4th option `label: "More…"`, `description: "Show the remaining commands."`. When the user picks "More…", call `AskUserQuestion` again with the next batch (same rules).

3. **Launch the selection.**
   - Take the user's chosen `label`, strip the leading `/`, and invoke `Skill` with `skill` set to that name.
   - That skill's own instructions take over from here.

4. **Stop.** Do not run any further tools, do not summarise, do not narrate. Once `Skill` is invoked, `/start` is done — the launched workflow owns the rest of the turn.

## Constraints

- Never include `/start` itself in the option list.
- Never inline or paraphrase the chosen command's body — always dispatch via `Skill`.
- Never hard-code the command list; always re-discover from `.claude/commands/` on each invocation.
