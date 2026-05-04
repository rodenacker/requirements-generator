---
name: mermaid-validator
description: Automatically validate mermaid diagrams after creating or editing them in markdown files
---

# When to Use This Skill

**Proactively use this skill after:**

- Creating new mermaid diagrams in markdown files
- Editing existing mermaid diagrams
- User asks to validate/check mermaid diagrams

**Always validate before completing the task.**

# Instructions

1. Read the markdown file (use the file from context or ask user which file to validate)
2. **Run validation** using: `mmdc -i <file-path> -o /tmp/mermaid-validation.svg 2>&1`
3. **Report validation results**:
    - If valid: Confirm the diagram is valid and exit
    - If invalid because `mmdc` is not installed (e.g., command-not-found, `mmdc: not found`, npx fails with ECOMPROMISED, or any "missing binary" signal): halt and present the failure to the user with at least the option: **"install mmdc manually: `npm i -g @mermaid-js/mermaid-cli` and then try again"**. Do not attempt to auto-install. Do not loop.
    - If invalid for any other reason: Show the errors found and explain what's wrong
4. **Fix the issues** automatically (invalid diagrams have no value) — only for syntax/semantic errors, not for the "mmdc not installed" case above
5. **Re-validate** to confirm the fix worked
6. Repeat steps 4-5 until there are no validation issues
