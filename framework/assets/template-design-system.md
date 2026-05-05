<!-- ROLE: asset (template). Populated by `framework/agents/design-system-styler.md` step-06. Final output written to `design-system/design-system.md`. Section order is contractual — do not reorder. -->

---
reference_url: "{{reference_url}}"
extraction_date: "{{extraction_date}}"
extraction_status: "{{extraction_status}}"
domain: "{{domain}}"
css_source_type: "{{css_source_type}}"
css_source_url: "{{css_source_url}}"
---

# Design System: {{domain}}

> {{attribution_paragraph}}
>
> Every token below carries a provenance marker — `extracted-from-url` if the value was found in the fetched CSS, `inferred-from-domain` if it was inferred per-run from the `{{domain}}` string. Review before consuming.

---

## Extraction Summary

Human-readable view with source context per token. The machine-readable Brand sections below contain the same values without context.

### Colours

| Token        | Hex       | Source Context              | Provenance              |
| ------------ | --------- | --------------------------- | ----------------------- |
| primary      | `{{c_primary_hex}}`      | {{c_primary_source}}      | {{c_primary_prov}}      |
| secondary    | `{{c_secondary_hex}}`    | {{c_secondary_source}}    | {{c_secondary_prov}}    |
| accent       | `{{c_accent_hex}}`       | {{c_accent_source}}       | {{c_accent_prov}}       |
| background   | `{{c_background_hex}}`   | {{c_background_source}}   | {{c_background_prov}}   |
| surface      | `{{c_surface_hex}}`      | {{c_surface_source}}      | {{c_surface_prov}}      |
| text         | `{{c_text_hex}}`         | {{c_text_source}}         | {{c_text_prov}}         |
| text-muted   | `{{c_text_muted_hex}}`   | {{c_text_muted_source}}   | {{c_text_muted_prov}}   |
| success      | `{{c_success_hex}}`      | {{c_success_source}}      | {{c_success_prov}}      |
| warning      | `{{c_warning_hex}}`      | {{c_warning_source}}      | {{c_warning_prov}}      |
| error        | `{{c_error_hex}}`        | {{c_error_source}}        | {{c_error_prov}}        |
| info         | `{{c_info_hex}}`         | {{c_info_source}}         | {{c_info_prov}}         |

### Typography

| Token              | Value                          | Source Context              | Provenance              |
| ------------------ | ------------------------------ | --------------------------- | ----------------------- |
| heading-family     | {{t_heading_family}}           | {{t_heading_family_source}} | {{t_heading_family_prov}} |
| heading-weight     | {{t_heading_weight}}           | {{t_heading_weight_source}} | {{t_heading_weight_prov}} |
| body-family        | {{t_body_family}}              | {{t_body_family_source}}    | {{t_body_family_prov}}    |
| body-weight        | {{t_body_weight}}              | {{t_body_weight_source}}    | {{t_body_weight_prov}}    |
| text-xs            | {{t_size_xs}}                  | {{t_size_xs_source}}        | {{t_size_xs_prov}}        |
| text-sm            | {{t_size_sm}}                  | {{t_size_sm_source}}        | {{t_size_sm_prov}}        |
| text-base          | {{t_size_base}}                | {{t_size_base_source}}      | {{t_size_base_prov}}      |
| text-lg            | {{t_size_lg}}                  | {{t_size_lg_source}}        | {{t_size_lg_prov}}        |
| text-xl            | {{t_size_xl}}                  | {{t_size_xl_source}}        | {{t_size_xl_prov}}        |
| text-2xl           | {{t_size_2xl}}                 | {{t_size_2xl_source}}       | {{t_size_2xl_prov}}       |
| text-3xl           | {{t_size_3xl}}                 | {{t_size_3xl_source}}       | {{t_size_3xl_prov}}       |
| text-4xl           | {{t_size_4xl}}                 | {{t_size_4xl_source}}       | {{t_size_4xl_prov}}       |
| line-height-tight  | {{t_lh_tight}}                 | {{t_lh_tight_source}}       | {{t_lh_tight_prov}}       |
| line-height-base   | {{t_lh_base}}                  | {{t_lh_base_source}}        | {{t_lh_base_prov}}        |
| line-height-loose  | {{t_lh_loose}}                 | {{t_lh_loose_source}}       | {{t_lh_loose_prov}}       |

### Effects

| Token              | Value                                 | Source Context           | Provenance               |
| ------------------ | ------------------------------------- | ------------------------ | ------------------------ |
| shadow-sm          | {{e_shadow_sm}}                       | {{e_shadow_sm_source}}   | {{e_shadow_sm_prov}}     |
| shadow-md          | {{e_shadow_md}}                       | {{e_shadow_md_source}}   | {{e_shadow_md_prov}}     |
| shadow-lg          | {{e_shadow_lg}}                       | {{e_shadow_lg_source}}   | {{e_shadow_lg_prov}}     |
| transition-fast    | {{e_dur_fast}}                        | {{e_dur_fast_source}}    | {{e_dur_fast_prov}}      |
| transition-base    | {{e_dur_base}}                        | {{e_dur_base_source}}    | {{e_dur_base_prov}}      |
| transition-slow    | {{e_dur_slow}}                        | {{e_dur_slow_source}}    | {{e_dur_slow_prov}}      |
| easing-standard    | {{e_easing_standard}}                 | {{e_easing_source}}      | {{e_easing_prov}}        |

### Contrast Validation

WCAG AA validation for the four required text/background pairs (minimum 4.5:1 for normal body text). Auto-adjustment runs against the `text` and `text-muted` tokens until each pair passes; adjustments are listed below.

| Pair                            | Ratio                       | Status              |
| ------------------------------- | --------------------------- | ------------------- |
| text on background              | {{cv_text_bg_ratio}}:1      | {{cv_text_bg}}      |
| text on surface                 | {{cv_text_surface_ratio}}:1 | {{cv_text_surface}} |
| text-muted on background        | {{cv_muted_bg_ratio}}:1     | {{cv_muted_bg}}     |
| text-muted on surface           | {{cv_muted_surface_ratio}}:1 | {{cv_muted_surface}} |

Adjustments: {{cv_adjustments}}

---

## Brand Colours

| Token       | Value             |
| ----------- | ----------------- |
| primary     | {{c_primary_hex}}      |
| secondary   | {{c_secondary_hex}}    |
| accent      | {{c_accent_hex}}       |
| background  | {{c_background_hex}}   |
| surface     | {{c_surface_hex}}      |
| text        | {{c_text_hex}}         |
| text-muted  | {{c_text_muted_hex}}   |
| success     | {{c_success_hex}}      |
| warning     | {{c_warning_hex}}      |
| error       | {{c_error_hex}}        |
| info        | {{c_info_hex}}         |

## Brand Typography

### Families

| Role    | Family                    | Weight                    |
| ------- | ------------------------- | ------------------------- |
| Heading | {{t_heading_family}}      | {{t_heading_weight}}      |
| Body    | {{t_body_family}}         | {{t_body_weight}}         |

### Sizes

| Token     | Value             |
| --------- | ----------------- |
| text-xs   | {{t_size_xs}}     |
| text-sm   | {{t_size_sm}}     |
| text-base | {{t_size_base}}   |
| text-lg   | {{t_size_lg}}     |
| text-xl   | {{t_size_xl}}     |
| text-2xl  | {{t_size_2xl}}    |
| text-3xl  | {{t_size_3xl}}    |
| text-4xl  | {{t_size_4xl}}    |

### Line Heights

| Token              | Value             |
| ------------------ | ----------------- |
| line-height-tight  | {{t_lh_tight}}    |
| line-height-base   | {{t_lh_base}}     |
| line-height-loose  | {{t_lh_loose}}    |

## Brand Effects

### Shadows

| Token     | Value                |
| --------- | -------------------- |
| shadow-sm | {{e_shadow_sm}}      |
| shadow-md | {{e_shadow_md}}      |
| shadow-lg | {{e_shadow_lg}}      |

### Motion

| Token             | Value                 |
| ----------------- | --------------------- |
| transition-fast   | {{e_dur_fast}}        |
| transition-base   | {{e_dur_base}}        |
| transition-slow   | {{e_dur_slow}}        |
| easing-standard   | {{e_easing_standard}} |
