# General Rules for Requirements

Catalogue of standard answers for common gaps in a requirements draft. Consulted by the requirements-drafter **before** producing an `[AI-SUGGESTED]` marker: if a rule below covers the gap, the drafter applies the rule's canonical answer and tags the field `[STANDARD-RULE: GR-NN]`. The resolver skips this marker — these rules are deterministic and require no consultant Q&A.

Each rule has a stable ID `GR-NN`, a scope predicate (template field/element it applies to), and the canonical answer. Add new rules by appending; never renumber.

## GR-01 — Excluded actions on a Viewer role

**Applies to:** §6.5 RBAC matrix cells where the persona's expertise / role description identifies them as a read-only viewer (e.g. "Viewer", "Read-only user", "Auditor with no write access").

**Rule:** All actions excluded from a Viewer's RoleAssignment must be **hidden** in the UI, not rendered as disabled controls.

**Rationale:** disabled controls invite hover and click attempts, leak feature existence, and clutter the viewer's screen with affordances they cannot use. Hiding is the prototype default.
