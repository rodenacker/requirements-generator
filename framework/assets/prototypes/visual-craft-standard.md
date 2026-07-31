# Prototype visual-craft standard (`visual-craft-standard.md`)

**Role:** asset (prototype-private).

**Purpose:** The **visual and tactile floor** every generated prototype must meet, and the **responsive contract** it must satisfy for its declared device targets. `ux-baseline-checklist.md` governs whether a surface *works*; this file governs whether it looks and feels like something a designer made. The two are complements, not alternatives — a surface can pass every Nielsen heuristic and still read as an unstyled default, which is exactly what the pipeline shipped before this file existed.

It is a **floor, not a style**: it prescribes how to bind the brand tokens and how interaction must feel, never a palette, a per-prototype visual character, or a divergence axis. Brand stays uniform across every prototype in the shared app (D1); visual divergence remains **forbidden** (`characters/prototype-generator.md`). What varies between prototypes is layout and workflow, via posture + D1–D5 (`design-philosophies.md`).

**Consumed by:** `framework/agents/prototype-generator.md` + `prototype-generator/steps/{step-02-read-spec, step-04-dispatch-surface-subagents, step-05-compose-route, step-sub-render-surface, step-07-handback}.md` (render-time application + self-check), `framework/agents/prototype-spec-merger.md` (appends the spec-relevant subset into design-spec §9), `framework/skills/verify-prototype-build.md` (the runtime-checkable subset). Referenced by `framework/assets/prototypes/shared-component-conventions.md §4`.

**Canonical elsewhere — referenced here, never redefined** (`docs/maintenance.md > Canonical-source rule`):

| Concern | Canonical owner |
|---|---|
| Component minimum-feature contracts (tables, date fields, buttons, inputs, navigation, feedback) | `framework/assets/design-system-standards.md §1` — surfaced through `framework/assets/prototypes/ux-baseline-checklist.md > Component minimum-feature contracts` (function, not craft) |
| Animation policy, `prefers-reduced-motion`, duration tiers | `framework/assets/design-system-standards.md §2` |
| The six required interactive states | `framework/assets/design-system-standards.md §3` |
| Touch-target minimum on touch surfaces (44×44) | `framework/assets/design-system-standards.md §4` |
| Content & microcopy (voice, button labels, error messages, capitalisation, empty-state copy) | `framework/assets/design-system-standards.md §5` — **owned there, not yet consumed by this pipeline**; listed so the gap is visible rather than rediscovered |
| Pattern usage rules (modal vs drawer, table vs card grid, toast vs banner, filters vs search) | `framework/assets/design-system-standards.md §6` — **owned there, not yet consumed by this pipeline**; the `pattern-catalogue/` is the pipeline's working source |
| Colour binding through semantic tokens; the no-palette-colour rule | `framework/assets/prototypes/shared-component-conventions.md §4a` |
| Measured on-colours and the enumerated fill-state table | `framework/skills/extract-brand-theme.md > Contrast & on-colours` |
| Table-to-card collapse below 768px | `framework/shared/general-rules.md > GR-18` |
| Accessibility / usability floor, incl. the 24×24 baseline target | `framework/assets/prototypes/ux-baseline-checklist.md` |
| Runtime test-hook vocabulary | `framework/skills/verify-prototype-build.md` |

---

## 1. Token binding — reach for these, never for a literal

Everything below is a Tailwind utility backed by a brand token written at scaffold by `extract-brand-theme.md`. A raw value is a defect even when it looks right, because it does not move when the brand or the colour mode does.

| Need | Use | Never |
|---|---|---|
| Type size | `text-xs … text-4xl` (brand scale, paired line-heights) | `text-[13px]`, inline `fontSize` |
| Heading face | `font-heading` on headings (already applied to `h1–h6` by the base layer) | naming a family in a component |
| Elevation | `shadow-xs / shadow-sm / shadow-md / shadow-lg` | `shadow-[0_2px_8px_rgba(...)]` |
| Transition timing | a bare `transition` / `transition-colors` (already brand-bound via `--default-transition-duration` + `--default-transition-timing-function`) | `duration-200`, `duration-[200ms]`, `ease-linear` |
| An explicit slower tier | `duration-[var(--duration-base)]`, `duration-[var(--duration-slow)]` | a hardcoded ms value |
| Overlay entrance easing | `ease-[var(--ease-entrance)]` | `ease-out` for entrances you author yourself |
| Colour | semantic tokens per `shared-component-conventions.md §4a` | any Tailwind palette colour, any hex |
| Radius | `rounded-md / rounded-lg / rounded-xl` (brand `--radius` ladder) | `rounded-[10px]` |
| Spacing | Tailwind's 4/8 scale (`p-2 … p-8`, `gap-2 … gap-6`) | `p-[13px]`, `mt-[7px]` |

**`--duration-*` is not a Tailwind namespace**, so `duration-fast` does **not** exist as a utility. Either rely on the bare `transition` (which already resolves to the brand fast tier) or use the `duration-[var(--duration-base)]` arbitrary-value form. Writing `duration-fast` produces no CSS and fails silently.

## 2. Tactility — press must be felt

**Every clickable element scales down slightly, to 98%, when pressed, using the fast duration.** `0.98`, not `0.9`: it must register as a firm press, not a collapse.

The template's `globals.css` applies this **globally** to `button`, `[role="button"]`, `summary`, `[role="tab"]`, `[role="option"]`, `[role="menuitem"]` and anything carrying `data-pressable`, so semantic controls get it for free. Your obligations:

- **Use a real semantic element** (`<button>`, `<a>`, `<summary>`) wherever something is clickable. That earns the press response, the focus ring and keyboard operability in one move.
- **Stamp `data-pressable` on any non-semantic clickable** you author — a clickable card, a swatch, a footer row, a custom segmented-control segment. This is the only way the global layer can reach it.
- **Stamp `data-elevated` alongside it** when the element rests on elevation, so the press also drops it one step (`md` → `sm`). Pressing something that is floating should feel like pushing it toward the page.
- **Never press a disabled control.** `disabled` / `aria-disabled="true"` / `data-disabled` are exempt by the global layer — do not re-enable them with a local `active:` class.

**Press is transform + elevation only — never a colour change.** This is not a style preference, it is a correctness constraint. `extract-brand-theme.md` measures each fill's label colour against an **enumerated** list of fill states; a press that introduces a new composite (`active:bg-primary/95`) creates a state whose on-colour was never derived, and the both-modes contrast sweep would then be asserting against a state that does not exist in the theme. Hover and active may only use fills **already** in that list:

`primary`, `primary/90` · `secondary`, `secondary/80`, `secondary/90` · `destructive`, `destructive/90`, `destructive/60` · `accent`, `accent/50` · `input/30`, `input/50` · `muted/50` · `background`

**Do not author your own press scale.** The global layer owns it. If a large surface genuinely needs a shallower press, override with `active:scale-[0.99]` — never add a scale *on top* of the global one under a different property. Tailwind v4's `scale-*` utilities compile to the standalone **`scale`** property, not to `transform`, and CSS composes `scale` and `transform` multiplicatively: a `transform: scale(0.98)` plus an `active:scale-[0.98]` renders at **0.9604**, the visible over-collapse this whole rule exists to avoid. The global layer therefore uses the `scale` property too, so a component-level override *cascades* instead of compounding. (`hover:-translate-y-px` uses the separate `translate` property and composes cleanly — that pairing is intended.)

**Clickable rows are the one exception to the scale rule** — they press via the `accent` fill instead. `transform` on `display: table-row` is unreliable across engines, and `accent` is already a measured state, so this costs the contrast contract nothing. The template's base layer handles it for `tr[data-pressable]` / `tr[data-clickable]`; give clickable rows one of those attributes.

**But a data table row is never a click target** (`design-system-standards.md §1 > Tables`, canonical). Whole-row click is an invisible affordance, ambiguous against text selection, hostile to keyboard users, and conflicts with checkbox/multi-select. On a data table the row's primary identifier becomes a **link or button in its own cell**, and row-scoped actions live in a **dedicated action column** — so the press response is the cell control's, earned semantically. The attributes above remain correct for row-*like* lists that are not data tables (a `collections/data-list` row, a stacked card row, a footer row); they are not an escape hatch for a `<table>`.

## 3. Hover — every interactive element must shift

A control that looks identical before and after the cursor arrives reads as dead. Pick exactly one shift per element and apply it consistently across the app:

- a token fill from the measured list above (`hover:bg-accent`, `hover:bg-muted/50` for rows) — the default for buttons, rows, menu items;
- elevation +1 step (`hover:shadow-md` on a resting `shadow-sm` card);
- a 1px lift (`hover:-translate-y-px`) for cards that navigate — pair it with the elevation step, never use it alone.

Timing comes from the bare `transition` utility. Do not animate `all`: name the properties (`transition-[transform,box-shadow,background-color]`) so an unrelated layout property never animates by accident.

## 4. Overlay entrances — nothing appears instantly

**Tooltips, popovers, menus, toasts and dialogs fade in, lift 4px, and clear a 2px blur. They never pop in.** Exit is faster and skips the blur — a dismissal should feel immediate, an arrival should feel placed.

The template's `globals.css` drives this off the Radix `data-state` attributes the shadcn primitives already stamp (`proto-overlay-in` at `--duration-base`/`--ease-entrance`, `proto-overlay-out` at `--duration-fast`). So:

- **Compose the shipped primitive** (`ui/tooltip`, `ui/popover`, `ui/dropdown-menu`, `ui/dialog`, `ui/sheet`, `ui/select`) and the entrance is already correct. Hand-rolling an overlay out of a `div` and a boolean forfeits it — and forfeits focus trapping, `Esc`-to-close and portal placement with it.
- **A tooltip is required wherever meaning is carried by an icon alone** — icon-only buttons, status glyphs, truncated cell values. An icon-only control with no accessible name and no tooltip fails both this standard and `ux-baseline-checklist.md`'s name/role/value item.
- Do **not** add a second entrance animation on top (`animate-in` plus a custom keyframe) — they compose into a stutter.

## 5. Elevation ladder — four steps, meaning-bound

| Token | Meaning | Where |
|---|---|---|
| *(none)* | flush content; separation by border or background | table rows, list items, form fields, page sections |
| `shadow-xs` | hairline lift | inputs, outline buttons, sticky table headers |
| `shadow-sm` | resting raised surface | cards, KPI tiles, panels |
| `shadow-md` | hovered / actively raised | card hover, dragged item, raised toolbar |
| `shadow-lg` | floating above the page | dialogs, drawers, popovers, menus, tooltips, toasts |

Two rules: **never skip a rung** on hover (`sm → md`, not `sm → lg`), and **never stack a heavy border on an elevated surface** — pick shadow *or* border as the separator, not both. An elevated card with a 1px border and a shadow reads as a mistake.

## 6. Typography discipline

- **A real hierarchy.** A page title is `text-2xl` or `text-3xl`, a section heading `text-lg`/`text-xl`, body `text-sm`/`text-base`, metadata `text-xs`. Shipping `text-xl` as the only heading size and `text-sm` for everything else is what "looks unstyled" actually means in practice.
- `tracking-tight` at `text-2xl` and above (the base layer already does this for `h1`/`h2`; match it on any non-heading element rendered at display size).
- **Numeric columns get `tabular-nums`** (or `data-numeric="true"`, which the base layer styles) so digits align down the column. Right-align them.
- Weight carries hierarchy alongside size: `font-semibold` for headings and column headers, `font-medium` for emphasis inside body text. Never bold a whole paragraph.
- Prose blocks cap at ~72 characters (`max-w-[72ch]`); unbounded line length in a wide container is unreadable.
- **Muted text is `text-muted-foreground`**, never a lower opacity on the foreground colour — opacity stacks unpredictably over fills and breaks the measured contrast.

## 7. Spacing & rhythm

- One scale: Tailwind's 4/8 steps. No arbitrary pixel padding.
- **Consistent section rhythm** across a surface — pick one vertical gap for major sections (`space-y-6` is a sane default; `space-y-4` at dense D3 positions, `space-y-8` at calm ones) and use it everywhere on that surface. Mixed rhythm is the single most common reason a generated page looks careless.
- **Group by proximity, then separate** (`ux-baseline-checklist.md` G1): related fields tighter (`gap-2`), unrelated groups looser (`gap-6`). Uniform spacing everywhere destroys the grouping signal.
- Give a page a deliberate content width. Full-bleed for data tables; a capped measure for forms and detail views (`max-w-3xl`) — never a form stretched across 1600px.
- Density follows the **D3** position, not taste: dense positions tighten cell padding and row height, calm positions open them. The rhythm rule still applies inside either.

## 8. Focus — never traded away for aesthetics

The shipped `focus-visible:ring-[3px] ring-ring/50 ring-offset-2` stays. It must remain visible **through** the press transform: `ring-offset` puts the indicator outside the scaled box, and the base layer gives `:focus-visible` a stacking context so a neighbouring row cannot paint over it mid-press. Do not replace the ring with a colour change alone, do not set `outline-none` without an equivalent indicator, and do not clip it with `overflow-hidden` on an ancestor.

## 9. Motion policy

Canonical: `design-system-standards.md §2`. It is not restated here. The two things this file adds:

- **The decision rule.** If removing an animation does not make the UI harder to use, it must not exist. Motion answers a usability question — what changed, what caused it, where did it go, what is in flight — or it is decoration on a productivity surface.
- **Motion stays in CSS.** `framer-motion` is installed but must not be used. Beyond YAGNI: the both-modes contrast sweep disables motion with `*{transition:none!important;animation:none!important}` before measuring computed colours. A CSS transition is silenced by that; a JS-driven animation is **not**, so it would leave `getComputedStyle` returning mid-interpolation values and make the colour gate report a pass on a broken mode. `verify-prototype-build.md` calls that "the one failure mode that makes the gate actively misleading rather than merely absent." Keeping motion in CSS keeps the colour gate honest.

## 10. The six interactive states

Canonical: `design-system-standards.md §3` — **default, hover, focus-visible, active, disabled, loading**, all six designed and implemented for every interactive element. Two states this pipeline has historically dropped, called out because they are the ones that get skipped:

- **active** — see §2. It was absent from the entire repo before this standard.
- **loading, distinct from disabled** — disabled means "not allowed"; loading means "working on it". A button mid-action shows a spinner and keeps its label; it does not merely grey out.

## 11. Responsive contract (device targets)

The prototype's `device_targets` come from the design spec (front-matter key + §4b), chosen by the consultant at `prototype-orch.md` Step B. **This section is the canonical definition of the named viewports and what each target obliges.**

| Name | Viewport | Touch | Tailwind floor |
|---|---|---|---|
| `mobile` | 390 × 844 | yes | base (unprefixed) |
| `tablet` | 768 × 1024 | no | `md:` |
| `desktop` | 1280 × 800 | no | `lg:` |

`device_targets` shape: `{ primary: "desktop"|"tablet"|"mobile", breakpoints: [...], touch: <bool> }`. The four consultant choices map to:

| Choice | `breakpoints` | `primary` | `touch` |
|---|---|---|---|
| Desktop only | `["desktop"]` | `desktop` | `false` |
| Desktop + tablet | `["tablet","desktop"]` | `desktop` | `false` |
| Fully responsive | `["mobile","tablet","desktop"]` | `desktop` | `true` |
| Mobile first | `["mobile","tablet","desktop"]` | `mobile` | `true` |

### What every target obliges

- **Design for the narrowest listed breakpoint first**, then add `md:`/`lg:` to widen. Mobile-first is the Tailwind grain; writing desktop-first and then trying to claw back with `max-*` variants produces the specificity tangles that make responsive layouts break.
- **No horizontal page scroll at any listed breakpoint.** The document must never exceed its viewport width. This is the gate's primary assertion.
- **Tables never horizontally scroll below the narrowest target** — collapse to a card list showing the primary identifier, 2–3 key columns and a row-action overflow (`GR-18`, canonical in `general-rules.md`). `overflow-x-auto` on a desktop table is the specific failure `GR-18` exists to prevent, and the last real generated prototype did exactly that.
- **Sidebar shells collapse to a drawer below `md:`** — canonical in `pattern-catalogue/layouts/app-shell-with-sidebar.md`. Nav must stay reachable; a sidebar that simply vanishes strands the user.
- **Multi-column forms become single-column below `md:`.** Two-column field grids at 390px are unusable.
- **Dialogs become bottom sheets below `sm:`** when `mobile` is a listed breakpoint — a centred modal at 390px with a fixed width overflows.
- **Touch targets ≥ 44 × 44 px when `touch: true`** (`design-system-standards.md §4`), otherwise the 24 × 24 baseline (`ux-baseline-checklist.md`). Compact button sizes (`size="xs"`) are **not** available on a touch target; use `size="default"` or add padding.
- **A desktop-only prototype still must not break.** It is not obliged to be *good* below 1280px, but it must degrade to a readable single column rather than overlap, clip or scroll horizontally. Reviewers open prototypes in half-width windows.

### Reusing a component at a narrower target

Components are **shared** across every prototype in the app, so a component authored for a desktop-only prototype may be reused by a fully-responsive one. It is then **widened**, not forked — additive breakpoint classes only. The protocol (driver assigns `widen` instead of `reuse`; sub-agent reports `components_widened`) is canonical in `shared-component-conventions.md §3` rule 6.

---

## How the generator uses this

1. `step-02` reads `device_targets` from the design spec into the render plan; `step-04` passes the craft subset + `device_targets` into every per-surface dispatch.
2. While rendering, the per-surface sub-agent applies §1–§11 and self-checks before returning its manifest (`step-sub-render-surface.md` rules 2b/2c). Driver-owned routes and shells obey the same rules (`step-05`).
3. `step-07` runs the static sweeps: no palette colour, no raw hex, no hardcoded duration/shadow/type literal, responsive utilities present when a narrow breakpoint is targeted.
4. `verify-prototype-build.md` asserts the runtime-checkable subset — press response and token resolution once at scaffold, layout integrity per additional device target.
5. The merger embeds the spec-relevant subset into design-spec §9 so the contract is auditable per prototype.

## Anti-patterns

- **Do not use a Tailwind palette colour or a raw hex** — canonical in `shared-component-conventions.md §4a`. They do not flip with the colour mode. The last real generated prototype shipped 15 of them (`bg-green-100 text-green-900` and friends) past every gate; `step-07` now greps for them.
- **Do not introduce a colour change on press**, or any hover fill outside the measured state list (§2). It creates a state whose on-colour was never derived.
- **Do not hardcode a duration, easing, shadow, type size or radius.** If a token does not exist for what you need, you are reaching for a value the brand does not define — use the nearest rung.
- **Do not write `duration-fast`** and assume it works. It is not a generated utility (§1).
- **Do not use `framer-motion`**, and do not animate with JS. It defeats the contrast gate (§9).
- **Do not hand-roll an overlay.** Compose the primitive, or lose the entrance, the focus trap and `Esc`-to-close (§4).
- **Do not use an emoji or a text glyph as an icon.** `'✓'`, `'✕'`, `'ℹ'`, `'•'` do not inherit stroke weight, do not scale with the type ramp, and render differently per platform. Use `lucide-react` with `currentColor`.
- **Do not add decorative motion, gradients, glassmorphism or scroll-driven effects** to a data-management surface. "Modern" here means precise, legible and responsive to touch — not ornamental.
- **Do not skip `active:`** because a design looked fine without it. Six states, not five (§10).
- **Do not treat a posture or a device target as a licence to drop a floor item.** Postures vary layout and workflow; a narrower device changes the layout, not the standard.
- **Do not add a per-prototype theme, palette, type scale or visual character** (D1; `shared-component-conventions.md §4`). This standard raises the shared floor — it is not a divergence axis.
- Do not duplicate the *definitions* owned elsewhere (animation policy, six states, colour binding, `GR-18`, the fill-state table). Reference them — see the canonical-owner table above.
