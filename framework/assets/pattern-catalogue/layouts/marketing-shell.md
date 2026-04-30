<!-- ROLE: asset (pattern). v7b-specific. -->

# Pattern: marketing-shell

```yaml
id: marketing-shell
kind: layout-primitive
purpose: Public-facing landing-page layout — hero + content sections + footer —
  optimised for narrative, conversion, and brand expression rather than tool use.

when-to-use:
  - Unauthenticated public surface: home, feature, pricing, about, contact
  - Conversion-driven page (signup, contact, demo request as the page goal)
  - Content / story-led page where vertical reading order matters
  - SEO-relevant page

when-not-to-use:
  - Inside the authenticated app (use app-shell-with-sidebar or topnav)
  - Documentation-style content with deep navigation (use sidebar variant for docs)
  - Single-action surfaces (use centered-form)

variants:
  - default: hero + sections + footer, top marketing nav
  - long-scroll: many narrative sections, anchored sub-nav appears on scroll
  - minimal: hero only + single CTA + footer
  - with-docs-sidebar: marketing-style header but sidebar nav on the body (documentation)

default-trade-offs:
  speed-accuracy: -1
  power-simplicity: -1
  density-focus: -1
  control-automation: 0
  flexibility-consistency: 0
  memorability-density: -1

required-slots:
  - marketing-nav: brand + a small set of marketing destinations + primary CTA
  - hero: top-of-page narrative + primary CTA
  - sections: ordered list of content blocks
  - footer: legal / sitemap / social

optional-slots:
  - announcement-bar: thin banner above the nav
  - sub-nav: anchor links to in-page sections (long-scroll variant)
  - testimonials, logos, faq, comparison: section types
  - secondary-cta: repeated CTA row near the page bottom

states:
  default: full page renders
  loading: skeleton sections (rare — most marketing pages are SSR / static)
  error: 404 / 500 falls through to error-shell instead

behaviours-built-in:
  - smooth-scroll for in-page anchors
  - sub-nav highlights the section currently in view (long-scroll variant)
  - sticky-on-scroll behaviour for marketing-nav
  - keyboard: anchored skip-links to each major section
  - mobile menu: focus trap, aria-modal

composition-rules:
  may-contain: hero, content section, image, video (if media patterns are added),
    cta-strip, testimonial, logo-cloud, faq, footer
  must-not-contain: app-shell internals (table, dashboard, multi-step-wizard);
    these belong in the authenticated product
  parent-restrictions: top-level

token-roles-consumed:
  - surface-default, surface-elevated, surface-inverse
  - text-default, text-muted, text-inverse
  - state-success              # for primary CTA
  - elevation-card             # for floating elements
  - motion-emphasised          # for hero / scroll animations
  - radius-lg                  # marketing prefers larger radii
  - breakpoint-sm/md/lg

accessibility:
  - landmark: nav + main + footer (and aside for sub-nav)
  - skip-link to main hero
  - reduced-motion: hero / parallax / scroll-tied animations disabled
  - all interactive elements reachable by keyboard
  - sufficient contrast on hero overlay text against background imagery

spec-author-cues:
  - if the brief includes a public marketing site, this is the shell
  - if the brief is internal-tool-only, this pattern likely does not appear
  - hero variant choice (full-bleed image, video, illustration, plain) follows brand —
    decided at /style time, not here
  - long-scroll variant matters when sections >5; below that, plain section stack is fine

mapping-helpers:
  ooux-signal: not a primary signal
  user-stories-signal: "as a prospect I want to learn / decide / sign up"
  jtbd-signal: "evaluate-product" job
  journeys-signal: journey-stage = "awareness" or "consideration"
```
