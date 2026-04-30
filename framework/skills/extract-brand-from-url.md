<!-- ROLE: skill. STATUS: stub — author during phase-2 build-order step 12. -->

# extract-brand-from-url.md

**Purpose:** Fetch a consultant-supplied reference URL and extract style tokens — colour palette, typography, spacing scale, radii, shadows, motion durations, breakpoints, icon set — into `template-style-tokens.md`. Tokens not extractable are left as `<!-- agent-generate -->` for the styler's second pass.

**Inputs:** reference URL, `assets/template-style-tokens.md`.

**Outputs:** populated token entries with `provenance: extracted-from-url`; `<!-- agent-generate -->` markers on gaps.

**Used by:** `framework/agents/styler/agent.md`.

**Used how:** First pass of the styler. If no URL supplied, this skill is skipped and `generate-brand-tokens-from-domain.md` produces all tokens with `inferred-from-domain` / `inferred-from-spec` provenance.

> Content TBD per `plan/v7b-Brief.md > §/style > step 3`.
