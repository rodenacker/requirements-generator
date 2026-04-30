<!-- ROLE: asset (pattern). STATUS: T3 stub — author full entry on first use. -->

# Pattern: file-upload

```yaml
id: file-upload
kind: composite-pattern
purpose: Single or multi-file upload — drag-drop area + browse button + per-file
  progress + per-file states (queued / uploading / complete / error).
status: stub

when-to-use:
  - User attaches files to a record
  - Bulk import via CSV / spreadsheet
  - Profile / asset uploads

when-not-to-use:
  - Pasting text / structured data → use a textarea / paste-handler
  - Image-specific cropping needs → image-cropper (deferred)

variant-clusters: single, multi, drag-drop-zone, browse-only, with-validation
  (size / type / count), with-preview, chunked-upload, paste-from-clipboard

required-slots-baseline: accept (mime / extension), max-count, max-size, on-change
common-states: idle, drag-over, uploading (per-file), complete, error (per-file),
  exceeded-limit

related: single-form, drawer-form, repeater
```

> **Author the full entry when:** the first brief includes file attachment.
