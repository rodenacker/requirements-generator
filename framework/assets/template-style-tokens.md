<!-- ROLE: asset. v7a-derived seed (from .claude/skills/wds-7-design-system/templates/design-tokens.template.md). Finalise during phase-2 build-order step 12 per v7b-Brief.md > §template-style-tokens.md. -->

# Style Tokens

Populated by the `styler` agent (P2). Each token carries a value and a provenance marker.

**Provenance values:**
- `extracted-from-url` — pulled from the consultant-supplied reference URL
- `inferred-from-spec` — derived from the finalised `design-spec.md` (e.g. shadow tokens from modal/drawer organism elevation; motion durations from behaviours)
- `inferred-from-domain` — derived from `requirements.md > domain` heuristics
- `consultant-specified` — provided directly by the consultant

Tokens the URL pass didn't supply are flagged `<!-- agent-generate -->` for the styler's second pass.

**Last Updated:** [Date]
**Token Count:** [count]

---

## Colour palette

### Primary

```yaml
primary-50:  { value: '#eff6ff', provenance: 'extracted-from-url' }
primary-100: { value: '#dbeafe', provenance: 'extracted-from-url' }
primary-200: { value: '#bfdbfe', provenance: 'extracted-from-url' }
primary-300: { value: '#93c5fd', provenance: 'extracted-from-url' }
primary-400: { value: '#60a5fa', provenance: 'extracted-from-url' }
primary-500: { value: '#3b82f6', provenance: 'extracted-from-url' }
primary-600: { value: '#2563eb', provenance: 'extracted-from-url' }
primary-700: { value: '#1d4ed8', provenance: 'extracted-from-url' }
primary-800: { value: '#1e40af', provenance: 'extracted-from-url' }
primary-900: { value: '#1e3a8a', provenance: 'extracted-from-url' }
```

### Secondary

```yaml
# <!-- agent-generate --> if not on the reference URL
```

### Semantic

```yaml
success: { value: '#10b981', provenance: 'inferred-from-domain' }
error:   { value: '#ef4444', provenance: 'inferred-from-domain' }
warning: { value: '#f59e0b', provenance: 'inferred-from-domain' }
info:    { value: '#3b82f6', provenance: 'inferred-from-domain' }
```

Semantic-state count derived from the §States column of the design-spec UI inventory.

### Neutral

```yaml
gray-50:  '#f9fafb'
gray-100: '#f3f4f6'
gray-200: '#e5e7eb'
gray-300: '#d1d5db'
gray-400: '#9ca3af'
gray-500: '#6b7280'
gray-600: '#4b5563'
gray-700: '#374151'
gray-800: '#1f2937'
gray-900: '#111827'
```

---

## Typography

### Families

```yaml
font-sans: { value: 'Inter, system-ui, sans-serif', provenance: 'extracted-from-url' }
font-mono: { value: 'JetBrains Mono, monospace',   provenance: 'inferred-from-domain' }
```

### Scale

```yaml
text-xs:   0.75rem
text-sm:   0.875rem
text-base: 1rem
text-lg:   1.125rem
text-xl:   1.25rem
text-2xl:  1.5rem
text-3xl:  1.875rem
text-4xl:  2.25rem
```

### Weights

```yaml
font-normal:   400
font-medium:   500
font-semibold: 600
font-bold:     700
```

### Line height

```yaml
leading-tight:  1.25
leading-normal: 1.5
leading-loose:  1.75
```

---

## Spacing

```yaml
spacing-0:  0
spacing-1:  0.25rem
spacing-2:  0.5rem
spacing-3:  0.75rem
spacing-4:  1rem
spacing-6:  1.5rem
spacing-8:  2rem
spacing-12: 3rem
spacing-16: 4rem
```

---

## Radii

```yaml
radius-sm:   0.125rem
radius-md:   0.375rem
radius-lg:   0.5rem
radius-full: 9999px
```

---

## Shadows

Shadow tokens are inferred from organism elevation needs in the finalised design-spec (modal, drawer, sticky bars).

```yaml
shadow-sm: { value: '0 1px 2px 0 rgb(0 0 0 / 0.05)',   provenance: 'inferred-from-spec' }
shadow-md: { value: '0 4px 6px -1px rgb(0 0 0 / 0.1)', provenance: 'inferred-from-spec' }
shadow-lg: { value: '0 10px 15px -3px rgb(0 0 0 / 0.1)', provenance: 'inferred-from-spec' }
```

---

## Motion durations

Derived from the §Behaviours section of the design-spec.

```yaml
transition-fast: { value: '150ms', provenance: 'inferred-from-spec' }
transition-base: { value: '200ms', provenance: 'inferred-from-spec' }
transition-slow: { value: '300ms', provenance: 'inferred-from-spec' }
```

---

## Breakpoints

```yaml
sm:  640px
md:  768px
lg:  1024px
xl:  1280px
2xl: 1536px
```

---

## Icon suggestions

Default set: **Lucide**. Detectable alternatives on the reference URL override.

```yaml
icon-set: { value: 'lucide', provenance: 'inferred-from-domain' }
icon-semantic-mappings:
  # Derived from §States + §Behaviours of the design-spec
  success: 'check-circle'
  error:   'alert-circle'
  warning: 'alert-triangle'
  info:    'info'
```

---

**Output files:** `artifacts/design/style-tokens.md` (this file, populated) + `artifacts/design/tokens.css` (machine form) + `artifacts/design/brand.md` (rationale).
