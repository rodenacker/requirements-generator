# Project Brief

## Overview

### Objective

Build an interactive prototype for an operations portal web application targeting teams of technically strong business users building and operating custom software. The prototype will be used to demo the concept to stakeholders and gather feedback before committing to full development.

### Target Users

- **Tenant and Project admins** — Create projects, assign users, view operations
- **Operators** — Add applications and environments, add and configure environment resources, investigate issues
- **Viewers** — View dashboards, logs and metrics

## Features & Requirements

see [requirements](requirements-v1.md)

## User Flows

see [user tasks](user-tasks-v1.md)

## Design Direction

### Visual Style

You are designing a clean enterprise SaaS UI.

Design system:

- Use ONLY the provided color tokens
- Do NOT introduce new colors
- Prefer whitespace over complexity
- Use flat design (no heavy shadows or gradients)
- Maximum 2 colors per component
- Cards must be simple with subtle borders
- Typography must be minimal and readable

Style:

- Calm, structured, professional
- No visual noise
- No unnecessary decoration

Colors:

```json
{
  "colors": {
    "primary": "#1F7A6E",
    "primaryHover": "#17675C",
    "primarySoft": "#E6F4F1",

    "accent": "#22C55E",

    "background": "#F8FAF9",
    "surface": "#FFFFFF",

    "textPrimary": "#0F172A",
    "textSecondary": "#64748B",
    "textMuted": "#94A3B8",

    "border": "#E2E8F0",
    "divider": "#F1F5F9",

    "success": "#16A34A",
    "warning": "#F59E0B",
    "danger": "#DC2626"
  }
}
```

Typography:

```json
{
  "typography": {
    "fontFamily": "Inter, system-ui, sans-serif",
    "sizes": {
      "xs": "12px",
      "sm": "14px",
      "base": "16px",
      "lg": "18px",
      "xl": "20px",
      "2xl": "24px"
    },
    "weights": {
      "normal": 400,
      "medium": 500,
      "semibold": 600
    }
  }
}
```

Spacing and layout:

```json
{
  "spacing": {
    "xs": "4px",
    "sm": "8px",
    "md": "16px",
    "lg": "24px",
    "xl": "32px"
  },
  "radius": {
    "sm": "6px",
    "md": "10px",
    "lg": "14px"
  }
}
```

### Layout Preferences

Use an enterprise console layout similar to AWS, Azure, or Vercel. All screens must feel like part of a single application workspace, not separate pages.

Layout:

- Fixed top bar for global actions
- Persistent left sidebar navigation
- Main content area for primary tasks

Design principles:

- The UI is a tool, not a marketing page
- Maintain strict alignment and consistent spacing
- Avoid large decorative elements, gradients, or hero sections
- Keep visual hierarchy subtle using spacing and typography

Density:

- Medium density

Navigation:

- Always visible sidebar
- Clear section grouping

## Data Objects

see [data model](domain-model-v1.md)

## Screens List

There is no screen list. Propose options based on the information provided.

## Constraints & Notes

- Prototype is for demo purposes only; no backend integration required
- All data should be realistic mock data (not lorem ipsum)
- Mobile responsiveness is not required
