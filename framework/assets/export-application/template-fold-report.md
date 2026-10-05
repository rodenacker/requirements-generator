<!--
role: asset
kind: template

Populate-top-to-bottom skeleton for generated-docs/export-application/fold-report.md,
written by framework/agents/export-application-folder.md (which reads this file) and
pointed to from the /export-application accept/reject gate.

This file is the CANONICAL DEFINITION of:
  - the fold report's shape
  - the four per-amendment fold statuses:
      folded                 — the amendment's end state was applied at its resolved anchor
      quote-mismatch-folded  — applied at the anchor ID, but its verbatim quote was not found
                               in that unit; the consultant must confirm the placement
      absorbed-by-chain      — a later amendment amends this one; its content reaches the
                               export only through the later amendment's end state
      collision-loser        — another, higher-numbered amendment supersedes the same base
                               bytes; this one was not applied
  - the three classifications: contradict (removes or replaces base bytes), refine (adds
    to a unit and removes nothing), net-new (the Amends line carries the net-new sentinel)

Population rules:
  - Replace every {{PLACEHOLDER}}; the finished report contains zero {{…}} tokens.
  - Alternatives inside a placeholder are written {{a | b}} — emit exactly one.
  - One "### AMD-NN — …" block per amendment in the source's Amendments section, in
    AMD-number order. EVERY amendment gets a block, whatever its status.
  - Removed and inserted text are quoted VERBATIM, [SRC: …] tags included, as blockquotes.
    Never summarise an edit. A partial-line contradict quotes the WHOLE original line as
    removed text.
  - Inside the spread-edits table, escape every literal "|" in a verbatim cell as "\|" so
    a quoted table row cannot break the table.
  - The "Limits of this report" blockquote is a fixed literal — emit it verbatim.
  - The report follows framework/shared/output-readability.md (summary first, one idea
    per sentence, no hedges). Verbatim quotes are exempt from the sentence cap.
  - HTML comments in this skeleton are authoring guidance and are NOT emitted.
-->
# Amendment fold report

## In plain terms

**What we found**
- {{N}} amendment(s) from {{k}} amendment document(s) were folded into the export: {{f}} applied, {{q}} applied with a quote mismatch, {{c}} absorbed by a later amendment, {{l}} superseded by a colliding amendment.
- The fold made {{s}} spread edit(s) to keep other mentions consistent, and minted {{m}} new requirement ID(s).

**What it means for you**
- Read each amendment block below before you accept the export — every edit the fold made is listed there.
- {{Check the quote-mismatch placements first: AMD-NN, AMD-NN. | No placement needs a special check.}}
- To change an amendment, run `/amend-requirements`, then re-export. `generated-docs/requirements/requirements.md` was not changed.

## Provenance

| Field | Value |
| --- | --- |
| Source document | `generated-docs/requirements/requirements.md` |
| Source sha256 | {{64-character lower-case hex}} |
| Folded at | {{ISO-8601 UTC}} |
| Amendments in source | {{N}} across {{R}} run(s) |
| Amendment documents | {{`documentation/<file>`, `documentation/<file>`, …}} |
| Outcome counts | folded {{f}}; quote-mismatch-folded {{q}}; absorbed-by-chain {{c}}; collision-loser {{l}} |
| Minted IDs | {{F-NN (AMD-NN), BR-NN (AMD-NN), … | none}} |
| Spread edits | {{s}} |
| Headings added or removed | {{`### Shape: X` added (AMD-NN), … | none}} |
| Folded intermediate | `generated-docs/export-application/.folded-source.md` — transient; deleted when the export run ends |

## Limits of this report

> **The fold is a judgement, and you are its check.** Every fact in a folded unit must come from the base text or from the amendment itself. No machine check proves that; reading the blocks below does. Spread edits are found by meaning, not by text match, so a missed mention is possible. Minted IDs exist only in the export. `requirements.md`, its blueprints and its prototypes do not carry them. The next `/requirements` run numbers the same requirements independently, so its IDs may differ.

## Amendments

### AMD-{{NN}} — {{one-liner, verbatim from the AMD heading}}

| Field | Value |
| --- | --- |
| Status | {{folded | quote-mismatch-folded | absorbed-by-chain | collision-loser}} |
| Amendment document | `documentation/{{filename}}` — cited in the export as `[SRC: {{filename}}]` |
| Origin | {{`[CONSULTANT-STATED]` | `[AI-INFERRED, CONSULTANT-CONFIRMED]`}} |
| Grounding | {{the AMD's Grounding line, verbatim | (none)}} |
| Classification | {{contradict | refine | net-new}} |
| Anchor | {{<anchor> — quote confirmed | <anchor> — quote NOT found in that unit; placed by ID | net-new — placed in <section> after <last unit> | AMD-NN (chain)}} |
| Chain / collision | {{absorbs AMD-NN | absorbed by AMD-NN | lost to AMD-NN on <anchor> | (none)}} |
| Minted ID | {{F-NN | (none)}} |
| Cells left empty | {{Priority, Acceptance criteria — the amendment does not state them | (none)}} |

**Removed text:**

> {{verbatim superseded bytes, [SRC: C-NNN] tags included | (none)}}

**Inserted text:**

> {{verbatim folded unit exactly as it appears in the folded source (`.folded-source.md`) — the exporter may still delete a scope span or swap a §6.10 cell inside it | (none — see AMD-NN)}}

**Spread edits:**

| Location | Before | After |
| --- | --- | --- |
| {{§N.N / ID / Shape.Field}} | {{verbatim before}} | {{verbatim after}} |

<!-- When there are no spread edits, replace the table with the single line: (none)
     Mentions considered and deliberately not edited go in a second table under the
     heading "Considered, not edited" with columns Location | Text | Why not edited;
     omit that table when there are none. -->

<!-- repeat the AMD block per amendment, in AMD-number order -->
