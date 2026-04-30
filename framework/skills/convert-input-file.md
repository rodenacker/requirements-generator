<!-- ROLE: skill. STATUS: stub — author during phase-1 build-order step 2. -->

# convert-input-file.md

**Purpose:** Convert non-native input formats into formats the drafter can extract from: pdf → markdown, image → annotated caption, html → markdown, etc. Leaves originals in place.

**Inputs:** a single file path under `/input/`.

**Outputs:** converted file alongside the original; metadata for the source manifest (file type, conversion applied, original path).

**Used by:** `framework/agents/input-handler/agent.md`.

**Used how:** Called once per supported non-native input. Refuses on unsupported types and reports them in the manifest as "unconverted, manual review".

> Content TBD per `plan/v7b-Brief.md > §Approach > skills` + agent roster row 1.
