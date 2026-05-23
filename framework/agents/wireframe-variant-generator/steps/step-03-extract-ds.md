---
name: step-03-extract-ds
description: 'Extract the embedded #wireframe-ds-css <style> block from wireframe-ds.html into <output_dir>/wireframe-ds.css. Verify the write.'
---

# Step 3: Extract the wireframe DS

## 3.1 Ensure output_dir exists

```
Bash tool: mkdir -p <output_dir>
```

## 3.2 Read the wireframe DS source

```
Read tool: framework/assets/design-systems/wireframe-ds.html
```

## 3.3 Extract the CSS block

Locate the `<style id="wireframe-ds-css">` element. Capture its inner content (everything between the opening tag and the closing `</style>`, excluding both tags). This is the per-variant `wireframe-ds.css` body. The token JSON above the style block is **not** part of the extracted CSS — it stays in the source HTML for LLM consumption.

## 3.4 Write the per-variant CSS

Compute the sha256 of the extracted CSS string.

```
Write tool: <output_dir>/wireframe-ds.css  (contents: the extracted CSS)
```

## 3.5 Verify the write

Call `framework/skills/verify-artifact-write.md` with:

- `path = <output_dir>/wireframe-ds.css`
- `expected_sha256 = <hash from 3.4>`
- `expected_min_bytes = 1024` (the extracted CSS is well above 1KB in current shape).

On `pass`, capture `ds_written = true` and advance. On `RF-04 trigger`, return `failed` per the registry's hard-halt semantics; the orchestrator's Stage-3 failure prompt surfaces.

---

**Next:** Read fully and follow `step-04-compose-screens.md`.
