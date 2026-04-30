<!-- ROLE: skill. STATUS: stub — author during phase-2 build-order step 12. -->

# generate-brand-tokens-from-domain.md

**Purpose:** Second pass of the styler — fill `<!-- agent-generate -->` token gaps from (a) the finalised `design-spec.md` (shadow-token roles from modal/drawer organism elevation; motion durations from behaviours; semantic-state count from states; icon-semantic-mappings from spec states + behaviours) and (b) `requirements.md > domain` heuristics. Defaults icon set to **Lucide** unless the reference URL declared otherwise.

**Inputs:** partially-populated `template-style-tokens.md`, finalised `design-spec.md`, `requirements.md`.

**Outputs:** fully-populated `style-tokens.md` with provenance markers on every token (`extracted-from-url` / `inferred-from-spec` / `inferred-from-domain` / `consultant-specified`).

**Used by:** `framework/agents/styler/agent.md`.

**Used how:** Always runs as the styler's last pass. Together with `extract-brand-from-url.md` produces the populated `style-tokens.md` + `tokens.css` (machine form) + `brand.md` (rationale).

> Content TBD per `plan/v7b-Brief.md > §/style > step 3` + §template-style-tokens.md.
