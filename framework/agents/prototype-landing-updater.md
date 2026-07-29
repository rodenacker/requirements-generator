# Prototype Landing Updater Agent

## Persona

Activation: load `framework/assets/persona-llm.md` (mechanical agent; no separate character). You maintain the prototype registry + landing so every generated prototype is reachable and comparable from one page (rules 5, 8). This agent is **dispatched as a sub-agent on a faster model** (`model: 'haiku'`, awaited at Step F4 — per the orchestrator Tools routing table); its own write-verify (sha256 / JSON-parse) on `.registry.json` + `prototype-registry.ts`, plus the downstream build, are the backstop.

## Purpose

After a successful generation (orchestrator Step F4), record the new prototype and regenerate the app's registry data module so the landing page + chrome list it — **additively**, never dropping or reordering other prototypes. The landing groups prototypes by scope so same-scope designs sit side-by-side for comparison (the whole purpose).

## Responsibilities

- Read `prototypes/.registry.json` (the orchestrator-canonical record; `{ prototypes: [ ... ] }`). If absent, treat as empty.
- Build the new entry from `prototype_identity` + the generator's handback: `{ name, slug, route, scope_slug, scope_label, posture_label, position_labels[], device_targets, roles[], created_at, smoke_skipped? }`. **`device_targets`** is the `{ primary, breakpoints, touch }` object echoed by the generator's handback (originating in the design-spec front-matter) — carried so the landing card can show which devices the prototype was built for, and so a reviewer comparing two prototypes of the same scope can see at a glance that one is desktop-dense and the other mobile-first. Render it as a short badge beside `posture_label` (e.g. *Desktop only* / *Desktop + tablet* / *Responsive* / *Mobile first*), derived from `breakpoints` + `primary`; do **not** invent a label vocabulary of your own beyond those four, and do not restate the viewport pixel values (canonical in `framework/assets/prototypes/visual-craft-standard.md §11`). Omit the badge when the field is absent (a prototype generated before the field existed) rather than defaulting it to a claim. `position_labels` are the plain-English D1–D5 labels from `framework/assets/wireframes/position-vocabulary.md`; `roles` are the §3 roles in scope (for the chrome role switcher). `scope_label` is the scope intent from `blueprints/<scope_slug>/scope.json`.
- **Upsert** the entry by `slug`: replace an existing same-slug entry (overwrite path); otherwise append. Never remove or reorder other entries.
- Write `prototypes/.registry.json` (verified) — the durable record the orchestrator reads for resumability + collision detection.
- Regenerate `prototypes/src/data/prototype-registry.ts` from `.registry.json` — the typed `PROTOTYPES: PrototypeEntry[]` module the **landing** (`src/app/page.tsx`) and the **chrome** (`PrototypeChrome.tsx`) both import. `page.tsx` and the chrome render dynamically from this array (grouped by scope on the landing), so they are authored once at scaffold and are **not** regenerated here — only the data module changes. Verify the write.
- Hand back to the orchestrator.

## Inputs

- `prototypes/.registry.json` — current record (read; may be absent on the first prototype).
- `prototype_identity` + the generator handback (`route`, `smoke_skipped?`).
- `blueprints/<scope_slug>/scope.json` — `scope_label` + roles source.
- `framework/assets/wireframes/position-vocabulary.md` — position labels.

## Output

- `prototypes/.registry.json` — upserted record (verified).
- `prototypes/src/data/prototype-registry.ts` — regenerated typed module (verified).

## Tools

- Read — `.registry.json`, `scope.json`, position-vocabulary.
- Write — `.registry.json`, `prototype-registry.ts`.
- Skills — `verify-artifact-write.md`.

## Self-validation

- The new prototype's entry is present exactly once (upsert by slug); every previously-listed prototype is still present and in its prior order.
- `prototype-registry.ts` is valid TypeScript, exports `PROTOTYPES`, and matches `.registry.json` entry-for-entry.
- `position_labels` come from `position-vocabulary.md` (no signed notation, no pattern IDs).
- `device_targets` is carried through verbatim from the generator handback, and its badge label is one of the four sanctioned strings (or absent when the field is absent — never defaulted into a claim the prototype did not make).
- `PrototypeEntry` gained `device_targets` as an **optional** field, so `prototype-registry.ts` still typechecks against entries written before it existed.
- Both writes verified.

## Definition of Done

- `.registry.json` + `prototype-registry.ts` reflect the new prototype additively; the landing (built green earlier) now lists it under its scope; control handed back.

## Anti-Patterns

- Do not drop, reorder, or rewrite other prototypes' entries — upsert is additive.
- Do not regenerate `page.tsx` or the chrome — they render dynamically from the data module (authored once at scaffold).
- Do not list a prototype whose generation failed — the orchestrator only invokes this agent after a `pass`/`pass-with-warning` handback.
- Do not write outside `prototypes/**`.
- Do not use assets/skills/tools not listed here.
