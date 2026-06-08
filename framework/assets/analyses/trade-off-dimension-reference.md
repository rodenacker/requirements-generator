<!-- ROLE: asset (P2 analysis reference). Loaded by framework/agents/analyses/trade-off-dimension-analyser.md at activation. -->

# analyses/trade-off-dimension-reference.md

**Purpose:** Methodology reference for Trade-Off Dimension Analysis. The analyser follows this document literally and exhaustively. Trade-off dimensions are A-versus-B axes (Speed vs Accuracy, Simplicity vs Power, Automation vs Control, ...) along which every UX design decision implicitly lands. The analyser surfaces, per user goal, where that goal should lean — anchored to evidence in `requirements/requirements.md`.

**Used by:**

- `framework/agents/analyses/trade-off-dimension-analyser.md` — drives Stage A relevance scoring, Stage B per-goal scoring, post-pass prune, and per-goal design-guidance synthesis.
- `framework/skills/map-trade-off-dimension-to-ui.md` — uses the produced scores to bias downstream wireframing options (stub).

**Output produced by the analyser:** `analyse-requirements/TRADE-OFF-DIMENSIONS/trade-off-matrix.html` — self-contained HTML matrix using `framework/assets/analyses/template-trade-off-dimension.html` as scaffold.

---

## Upstream input contract

The analyser starts from `requirements/requirements.md`. It uses:

- `§1` Application context — domain, business goal.
- `§1.5` Scope buckets — In / Out / Deferred.
- The preamble line `**Target:** application` or `**Target:** prototype` (immediately under the H1) — drives the prototype-deferred set below.
- `§4.1` Goals catalogue — the matrix's rows (one row per `G-NN`).
- `§4.2` Stories by persona — secondary evidence per goal (via the `→ §4.1 G-NN` back-reference).
- `§5` Task flows — secondary evidence per goal (matched by flow name referenced from §4.2 `Linked task flow`).
- `§6` Requirements (functional, business rules, validation, UI features, access control, NFRs, reporting, notifications, audit-trail) — secondary evidence per goal (matched by goal-ID back-reference where present, by topic keyword otherwise).

The analyser does not consult `requirements/source-manifest.json`, `framework/state/`, `framework/shared/`, or any other pipeline-internal artefact. Target is derived from the preamble line in `requirements/requirements.md`, preserving the stand-alone-ish constraint.

---

## Three-stage process

The analyser executes three stages in order. Each stage's output feeds the next.

1. **Stage A — Project-level relevance scoring.** Score every dimension in the reference against (domain, business goal, scope, target). Apply threshold, hard cap (15), and floor (5). Produce a `kept[]` list and a `dropped[]` list with per-dimension reasons. Surface `kept[]` to the consultant via the Stage A gate.
2. **Stage B — Per-(goal × kept-dimension) scoring.** For every (goal G × kept-dimension D) pair, count trigger-phrase matches in G's evidence bundle (§4.1, §4.2, §5, §6 scoped to G). Compute a net −2..+2 lean.
3. **Post-pass prune.** Drop any kept dimension whose every goal cell is 0 — it engages no goal individually.

---

## The trigger-phrase table

Every dimension is an A-vs-B axis. For each axis, pole-A triggers signal lean toward A; pole-B triggers signal lean toward B. Triggers are short word/bigram patterns the analyser substring-matches (case-insensitive) against requirement text. Triggers are deliberately curated and conservative — debate happens in PR review of this file, not at run time.

Stable-ID format: `TD-NN` (Trade-off Dimension). The IDs are appended-only; never renumber.

### Cognitive & interaction

| ID | Dimension (A vs B) | Pole-A triggers | Pole-B triggers |
| --- | --- | --- | --- |
| TD-01 | Speed vs Accuracy | "fast", "quickly", "performance budget", "throughput", "real-time", "without delay", "responsive", "within Nms", "low latency" | "correct", "validate", "no errors", "accurate", "verified", "exact", "must match", "reject invalid", "data integrity" |
| TD-02 | Simplicity vs Power/Flexibility | "simple", "minimal", "straightforward", "one-click", "uncluttered", "easy to use" | "configurable", "advanced", "power user", "flexible", "customisable", "expert", "extensive options" |
| TD-03 | Learnability vs Efficiency for Experts | "beginner", "intuitive", "self-explanatory", "no training", "onboarding", "first-time user", "discoverable" | "expert", "power user", "keyboard shortcut", "bulk", "efficient for", "high-frequency", "daily use" |
| TD-04 | Information Density vs Cognitive Load | "all on one screen", "comprehensive view", "tabular", "compact", "dense", "rich detail" | "uncluttered", "focused", "one thing at a time", "minimal", "easy to scan", "low cognitive" |
| TD-05 | Automation vs User Control | "automatic", "system performs", "auto-generated", "default", "background", "without user intervention" | "user controls", "manual", "explicit choice", "user decides", "override", "transparent", "fine-grained control" |
| TD-06 | Consistency vs Contextual Optimization | "consistent", "uniform", "same pattern", "predictable", "standard", "design-system" | "context-aware", "task-specific", "optimised for", "tailored", "specialised" |
| TD-07 | Guidance vs Freedom | "wizard", "step-by-step", "guided", "prompts user", "checklist", "walkthrough" | "free-form", "exploratory", "open-ended", "user chooses path", "no fixed sequence" |
| TD-08 | Discoverability vs Minimalism | "visible", "discoverable", "surface all", "obvious", "labels visible", "no hidden" | "minimal", "clean", "hide complexity", "progressive", "uncluttered" |
| TD-09 | Security vs Convenience | "secure", "encrypted", "authentication", "authorisation", "audit", "compliance", "POPIA", "GDPR", "HttpOnly", "SameSite", "session cookie", "credentials" | "frictionless", "single sign-on", "remember me", "auto-login", "passwordless", "smooth flow" |
| TD-10 | Accessibility vs Visual Density | "accessible", "WCAG", "screen reader", "keyboard navigation", "ARIA", "contrast", "alt text", "large text" | "dense", "compact", "max screen real-estate", "rich visuals", "minimal whitespace" |
| TD-11 | Personalization vs Predictability | "personalised", "tailored", "user-specific", "preferences", "remembers", "adaptive UI" | "predictable", "same for every user", "consistent across sessions", "shared mental model" |
| TD-12 | Feedback Richness vs Interaction Speed | "feedback", "confirms", "explains", "tooltip", "success/failure", "explicit feedback", "status indicator" | "smooth", "frictionless", "no interruptions", "minimal confirmations", "immediate" |
| TD-13 | Error Prevention vs Workflow Speed | "validation", "confirm before", "mandatory note", "guards", "preconditions", "reject invalid" | "quick action", "single click", "no extra step", "streamlined", "no friction" |
| TD-14 | Transparency vs Cognitive Simplicity | "explain", "show why", "audit", "history", "rationale", "transparent" | "hide details", "abstract away", "simple summary", "minimal explanation" |
| TD-15 | Precision vs Ease of Use | "exact", "precise", "fine-grained", "specific", "tolerance", "decimal" | "easy", "approximate", "rough", "broad", "default values" |

### Navigation & structure

| ID | Dimension (A vs B) | Pole-A triggers | Pole-B triggers |
| --- | --- | --- | --- |
| TD-16 | Flat Navigation vs Deep Navigation | "flat", "top-level", "one click away", "few levels", "broad" | "hierarchical", "nested", "drill down", "deep", "categorised" |
| TD-17 | Broad Menus vs Focused Menus | "all options visible", "broad menu", "exhaustive", "comprehensive list" | "focused", "scoped", "curated", "few options", "task-specific menu" |
| TD-18 | Search-Based Access vs Browsing | "search", "search box", "query", "find by", "typed input" | "browse", "list", "navigate to", "category tree", "scroll to find" |
| TD-19 | Contextual Navigation vs Global Predictability | "context menu", "row action", "inline action", "in-place" | "global navigation", "main menu", "persistent", "predictable navigation" |
| TD-20 | Progressive Disclosure vs Immediate Visibility | "expand", "show more", "drill", "click to reveal", "advanced section", "progressive" | "all visible", "no hidden options", "immediate", "everything on screen" |
| TD-21 | Single Screen Workflows vs Multi-Step Wizards | "single screen", "one page", "all-in-one", "single form" | "wizard", "multi-step", "step 1 of N", "progress indicator", "stepper" |
| TD-22 | Persistent Navigation vs Workspace Focus | "persistent nav", "global menu", "always visible", "sidebar" | "focused workspace", "distraction-free", "fullscreen", "task mode" |
| TD-23 | Modular Screens vs Workflow Continuity | "modular", "reusable", "separate screens", "card-based" | "continuous flow", "stay in context", "in-place", "without leaving" |

### Workflow & data entry

| ID | Dimension (A vs B) | Pole-A triggers | Pole-B triggers |
| --- | --- | --- | --- |
| TD-24 | Workflow Rigidity vs Flexibility | "must follow", "fixed order", "strict workflow", "preconditions", "lifecycle", "state machine", "guards" | "flexible", "any order", "user-defined path", "exceptions handled" |
| TD-25 | Batch Operations vs Granular Control | "bulk", "batch", "select multiple", "apply to all", "mass" | "row-by-row", "individual", "per-record", "granular", "one at a time" |
| TD-26 | Confirmation Dialogs vs Interaction Flow | "confirm", "are you sure", "confirmation dialog", "mandatory confirmation", "double-check" | "immediate", "no confirmation", "single action", "undo available", "smooth" |
| TD-27 | Inline Editing vs Validation Robustness | "inline edit", "edit in place", "click to edit", "in-row editing" | "form-based edit", "modal", "submit and validate", "validation step" |
| TD-28 | Real-Time Validation vs Typing Freedom | "real-time validation", "as you type", "immediate feedback", "live validation" | "validate on submit", "type freely", "no interruptions while typing" |
| TD-29 | Undo Support vs Prevention Mechanisms | "undo", "reversible", "rollback", "revert", "history" | "prevent", "warn before", "guard", "confirm first", "irreversible action" |
| TD-30 | Keyboard Efficiency vs Visual Clarity | "keyboard shortcut", "hotkey", "tab order", "keyboard navigation", "Enter to submit" | "visual buttons", "icon-led", "mouse-first", "discoverable actions" |
| TD-31 | Multi-Tasking Support vs Focus | "multiple tabs", "parallel work", "multi-tasking", "side-by-side" | "single task", "focus mode", "one thing at a time" |
| TD-32 | Stateful Workflows vs Simplicity | "remember state", "resume", "draft", "persist", "save progress" | "stateless", "fresh start", "no persistence", "simple" |

### Data display & analytics

| ID | Dimension (A vs B) | Pole-A triggers | Pole-B triggers |
| --- | --- | --- | --- |
| TD-33 | Data Density vs Readability | "table", "grid", "columns", "many rows", "compact view", "all columns visible" | "card view", "spacious", "readable", "minimal columns", "summary view" |
| TD-34 | Visualization Richness vs Interpretability | "chart", "visualisation", "graph", "trend line", "dashboard widget" | "table", "raw numbers", "simple list", "minimal visual" |
| TD-35 | Real-Time Updates vs Stability | "real-time", "live update", "auto-refresh", "push notification", "streaming" | "snapshot", "manual refresh", "stable view", "consistent during interaction" |
| TD-36 | Drill-Down Depth vs Navigation Complexity | "drill down", "expand row", "open detail", "nested view" | "shallow", "summary only", "no drill", "flat list" |
| TD-37 | Aggregation vs Detail Visibility | "aggregate", "total", "count by", "summary", "rolled up", "counts by status", "file summary" | "individual", "per-record detail", "raw data", "line-item" |
| TD-38 | Customizability vs Shared Understanding | "user-customisable", "configurable columns", "saved views", "personal preferences" | "shared view", "standard layout", "same for everyone", "single source of truth" |
| TD-39 | Contextual Information vs Visual Noise | "tooltip", "help text", "inline context", "supporting detail" | "minimal noise", "uncluttered", "primary data only" |

### Enterprise / governance

| ID | Dimension (A vs B) | Pole-A triggers | Pole-B triggers |
| --- | --- | --- | --- |
| TD-40 | Governance vs User Autonomy | "approval workflow", "policy", "governance", "controlled", "permission-bound" | "user autonomy", "self-service", "no approval needed", "user decides" |
| TD-41 | Auditability vs Workflow Simplicity | "audit", "audit trail", "traceable", "who/when/what", "history", "LastChangedUser", "LastChangedDate", "log every", "non-repudiation" | "frictionless", "minimal steps", "no audit overhead" |
| TD-42 | Role Separation vs Workflow Fluidity | "role-based", "RBAC", "Importer", "Approver", "segregation of duties", "permission" | "any user can", "shared role", "no role split" |
| TD-43 | Standard Processes vs Local Optimization | "standard process", "uniform workflow", "company-wide", "policy-defined" | "team-specific", "local override", "context-specific workflow" |
| TD-44 | Validation Strictness vs Data Entry Speed | "must validate", "strict format", "mandatory field", "rejected if invalid", "format check" | "lenient", "quick entry", "validation later", "soft validation" |
| TD-45 | Configurability vs System Complexity | "configurable", "settings", "admin can configure", "tunable", "FileSetting", "BulkFileSetting" | "fixed behaviour", "no configuration", "convention over configuration" |
| TD-46 | Traceability vs UI Simplicity | "trace", "lineage", "show source", "audit metadata", "evidence" | "minimal metadata", "clean UI", "hide provenance" |
| TD-47 | Compliance vs Productivity | "POPIA", "GDPR", "HIPAA", "PCI", "regulatory", "compliance", "data retention", "consent" | "frictionless", "no regulatory check", "productivity-first" |
| TD-48 | Cross-System Integration vs Reliability | "integrate with", "external system", "API", "SFTP", "third-party", "SSO" | "self-contained", "no external dependency", "isolated" |

### Visual design

| ID | Dimension (A vs B) | Pole-A triggers | Pole-B triggers |
| --- | --- | --- | --- |
| TD-49 | Minimalism vs Affordance Visibility | "minimal", "clean", "uncluttered design", "subtle" | "obvious affordance", "clearly clickable", "labelled button", "visible action" |
| TD-50 | Brand Expression vs Usability Clarity | "brand", "branded", "marketing", "distinctive design" | "clarity", "neutral", "usability-first", "standard pattern" |
| TD-51 | Animation Richness vs Performance | "animation", "transition", "motion", "animated feedback" | "instant", "no animation", "snappy", "performance-critical" |
| TD-52 | White Space vs Information Capacity | "spacious", "white space", "breathable", "generous padding" | "compact", "dense", "more on screen", "max info per pixel" |
| TD-53 | Visual Hierarchy vs Information Equality | "primary action", "emphasis", "prominent", "highlighted", "above the fold" | "equal weight", "no priority", "flat hierarchy" |

### Behaviour & collaboration

| ID | Dimension (A vs B) | Pole-A triggers | Pole-B triggers |
| --- | --- | --- | --- |
| TD-54 | Collaboration vs Ownership Clarity | "collaborative", "shared", "multiple users edit", "team workspace" | "single owner", "exclusive lock", "one editor at a time" |
| TD-55 | Notification Frequency vs Focus | "notify", "alert", "notification", "email on", "in-app message" | "no notification", "minimal interruption", "focus mode" |
| TD-56 | Real-Time Collaboration vs System Complexity | "live cursor", "real-time edit", "concurrent editing", "synchronous" | "single editor", "lock-based", "asynchronous" |

### User psychology

| ID | Dimension (A vs B) | Pole-A triggers | Pole-B triggers |
| --- | --- | --- | --- |
| TD-57 | User Confidence vs Productive Friction | "frictionless", "smooth", "encouraging", "confidence" | "guard", "safety", "confirm dangerous", "prevent accidental" |
| TD-58 | Familiarity vs Innovation | "familiar pattern", "standard", "convention", "expected behaviour" | "novel", "innovative", "new pattern", "experimental UX" |
| TD-59 | Trust Through Simplicity vs Trust Through Transparency | "simple and trustworthy", "minimal exposed mechanics" | "show how it works", "explain the calculation", "open the box" |

### Technical

| ID | Dimension (A vs B) | Pole-A triggers | Pole-B triggers |
| --- | --- | --- | --- |
| TD-60 | Frontend Richness vs Maintainability | "rich UI", "interactive", "dynamic", "client-side rendering" | "simple UI", "server-rendered", "maintainable", "low complexity" |
| TD-61 | Client-Side Processing vs Security | "client-side", "in-browser", "no server round-trip", "offline-capable" | "server-side", "trust boundary", "secure backend", "no client logic for X" |
| TD-62 | Immediate Rendering vs Data Accuracy | "optimistic UI", "render immediately", "instant feedback" | "wait for server", "confirmed data only", "consistent with backend" |

---

## Trigger-derivation fallback

A dimension not enumerated in the table above is **not** scored automatically. The analyser flags such dimensions in diagnostics as "no triggers defined" and skips them. To add a dimension, extend the table above with curated triggers in a follow-up PR. Triggers are not generated at run time — that would defeat the auditability the methodology depends on.

---

## Stage A — Project-level relevance scoring

For each dimension `D` in the trigger-phrase table:

1. **Compute the raw relevance score** by summing the following signal contributions:

    | Signal | Source section | Contribution |
    | --- | --- | --- |
    | Any pole's trigger phrase appears in **any** `§4.1` quality-signal cell | `§4.1` | **+2** (capped — once per dimension, not per match) |
    | Any pole's trigger phrase appears in **any** `§6.5` NFR row | `§6.5` | **+2** |
    | Any pole's trigger phrase appears in `§1` Domain or Business goal prose | `§1` | **+1** |
    | Any pole's trigger phrase appears in a `§1.5` Scope-In row | `§1.5 In` | **+1** |
    | Any pole's trigger phrase appears in a `§1.5` Scope-Out or Deferred row | `§1.5 Out / Deferred` | **−1** |
    | `Target: prototype` AND `D` is in the prototype-deferred set (below) | preamble + prototype-deferred set | **−2** |
    | A domain-amplifier rule fires for `D` (below) | `§1` + domain-amplifier rules | **+1** |

2. **Apply the threshold:** keep `D` if raw score ≥ **+2**.
3. **Apply the hard cap:** if more than 15 dimensions pass, keep the top 15 by raw score. Ties broken by the dimension's `TD-NN` order in this reference.
4. **Apply the floor:** if fewer than 5 dimensions pass, relax the threshold to ≥ **+1** until 5 pass. If still fewer than 5 even at threshold ≥ **+1**, do not relax further — record the under-floor outcome in diagnostics. Diagnostics also records that the floor relaxation ran when applicable.
5. **Sort kept dimensions by raw score descending.** Render order in the matrix follows this sort.

**Per-kept evidence record (the Stage A audit trail).** For each kept dimension, record:

- `id`: `TD-NN`
- `name`: `"Speed vs Accuracy"`
- `pole_a`, `pole_b`: pole labels
- `raw_score`: integer
- `signal_breakdown`: array of `{signal_name, source_section, quote, weight}` — every contribution that fired, with the verbatim quote that triggered it and the section anchor
- `kept_by`: one of `threshold`, `cap-top-15`, `floor-relaxation`

**Per-dropped evidence record.** For each dropped dimension, record:

- `id`, `name`, `raw_score`
- `dropped_by`: one of `below-threshold`, `cap-overflow`, `prototype-deferred-no-amplifier`, `no-triggers-defined`
- `signal_breakdown`: same shape as kept; included so consultants can audit why something was dropped

---

## Stage A consultant gate

Between Stage A and Stage B, the analyser surfaces the candidate dimension set via `AskUserQuestion` so the consultant can override the trigger-driven selection with domain knowledge the requirements doc may not have captured.

**Prompt template:**

> Stage A produced N kept dimensions and M dropped (threshold +2, cap 15, floor 5). Top kept: TD-NN, TD-NN, TD-NN (...). Accept this set, edit it, or restart the analysis?

**Options:**

1. `Accept — proceed to Stage B with the Stage-A selection (Recommended)`
2. `Edit — add or remove specific dimensions before proceeding`
3. `Restart — re-run Stage A from scratch`

**On Edit:** the analyser accepts free-text instructions ("add TD-30, drop TD-51") in the consultant's next message. Each addition is recorded as `kept_by: consultant-override` with `signal_breakdown` annotated `[CONSULTANT-OVERRIDE: <rationale-if-given>]`. Each removal flips the dimension to `dropped_by: consultant-override`. The cap (15) and floor (5) still apply after edits — if the consultant pushes the count out of range, the analyser surfaces a one-line correction prompt before proceeding.

**On Restart:** the analyser re-enters Stage A. No more than three Restart loops in one invocation; on the fourth, force the `Edit` path.

---

## Stage B — Per-(goal × kept-dimension) scoring

For each `kept` dimension `D` and each goal `G` in `§4.1`:

1. **Build G's evidence bundle** by collecting:
    - G's row in §4.1 (`statement`, `quality_signals`).
    - Every §4.2 story whose `Goal` field back-references G (`→ §4.1 G-NN`).
    - Every §5 task flow named by any of G's stories' `Linked task flow (optional)` field.
    - Every §6 requirement that references G's ID, OR (when no explicit back-reference exists) whose topic matches G by keyword overlap with G's statement (e.g. G-01 *"ingest transaction files"* → §6.1 file-upload requirements).
2. **Count pole hits** by substring-matching D's pole-A and pole-B trigger phrases (case-insensitive) against the evidence bundle. Weighted by source:

    | Source | Pole-A weight per match | Pole-B weight per match |
    | --- | --- | --- |
    | G's `quality_signals` (§4.1) | +2 | +2 |
    | G's `statement` (§4.1) | +1 | +1 |
    | A linked §4.2 story | +1 | +1 |
    | A linked §5 task flow | +1 | +1 |
    | A linked §6 requirement | +1 | +1 |

3. **Compute the lean magnitude** from the pole-A sum `A_sum` and the pole-B sum `B_sum`:

    | Condition | Magnitude |
    | --- | --- |
    | `A_sum == 0 AND B_sum == 0` | `0` (no signal) |
    | `A_sum >= 3 AND B_sum == 0` | `−2` (strong A) |
    | `A_sum >= 1 AND B_sum == 0 AND A_sum < 3` | `−1` (lean A) |
    | `B_sum >= 3 AND A_sum == 0` | `+2` (strong B) |
    | `B_sum >= 1 AND A_sum == 0 AND B_sum < 3` | `+1` (lean B) |
    | `A_sum > B_sum AND (A_sum - B_sum) == 1` | `−1` (lean A, with tension) |
    | `A_sum > B_sum AND (A_sum - B_sum) >= 2` | `−2` (strong A, with tension) |
    | `B_sum > A_sum AND (B_sum - A_sum) == 1` | `+1` (lean B, with tension) |
    | `B_sum > A_sum AND (B_sum - A_sum) >= 2` | `+2` (strong B, with tension) |
    | `A_sum == B_sum AND A_sum > 0` | `0` (balanced — both poles present) |

    Score sign convention: **negative = pole A**, **positive = pole B**, **zero = no signal OR balanced**. The diagnostics block distinguishes the two zero-types (`no-signal` vs `balanced`).

4. **Per-cell evidence record (the Stage B audit trail).** Every non-zero cell stores:

    - `goal_id`: `G-NN`
    - `dimension_id`: `TD-NN`
    - `score`: integer in `[−2, +2]`
    - `lean_label`: human-readable lean (e.g. `"strong A (Speed)"`, `"lean B (Validation Robustness)"`, `"balanced"`)
    - `pole_a_hits`: array of `{quote, anchor, weight}` for every match against pole-A triggers
    - `pole_b_hits`: array of `{quote, anchor, weight}` for every match against pole-B triggers
    - `rationale`: one sentence summarising the dominant pole's evidence

    Zero cells store `score: 0` and `cell_kind: no-signal` or `balanced`. No pole_*_hits array is required when both are empty.

---

## Post-pass prune

After Stage B completes, drop any kept dimension whose every goal cell is 0 (regardless of `no-signal` vs `balanced`). Such a dimension survived Stage A relevance but engages no goal individually — it would render as an all-zero matrix column. Record the prune in diagnostics with the reason.

The post-pass prune **does not** apply the floor (5) — a sparse final matrix is a real outcome, not a methodology failure. The diagnostics surface flags it for consultant attention.

---

## Score scale definition

| Score | Label | Meaning |
| --- | --- | --- |
| `−2` | strong A | Strong evidence the design should lean toward pole A for this goal |
| `−1` | lean A | Evidence the design should lean toward pole A, but not strongly |
| `0` (no-signal) | no signal | No trigger phrase from either pole appeared in this goal's evidence |
| `0` (balanced) | balanced | Triggers from both poles appeared with equal weight; the goal pulls both ways and the decision needs explicit consultant input |
| `+1` | lean B | Evidence the design should lean toward pole B, but not strongly |
| `+2` | strong B | Strong evidence the design should lean toward pole B for this goal |

**No fractional scores.** No `−1.5` or `+0.5`. The clamping rules in Stage B never produce them.

---

## Per-goal design guidance synthesis

After Stage B and the post-pass prune, the analyser produces 2–4 design-guidance bullets per goal. Each bullet picks a non-zero cell (preferring `±2` over `±1`, picking up to 4 strongest cells per goal) and translates the lean into a wireframing implication using the lookup below.

If a goal has zero non-zero cells, its guidance card reads: *"No strong directional evidence in `requirements.md` — design options for this goal can be drawn from any quadrant of the trade-off space. Consultant input recommended before wireframing."*

### Lean → wireframing implication lookup

| Dimension | If `−1` / `−2` (lean A) | If `+1` / `+2` (lean B) |
| --- | --- | --- |
| TD-01 Speed vs Accuracy | Optimistic UI; inline async actions; minimal pre-action validation; keyboard-first for frequent actions. | Synchronous validation; confirmation step on high-cost actions; show outcome only after backend confirms; visible status of in-flight operations. |
| TD-02 Simplicity vs Power | Single primary path per screen; hide advanced options behind a disclosure; sensible defaults; small command surface. | Surface advanced options near primary path; provide a settings/configuration affordance per object; admit a learning curve. |
| TD-03 Learnability vs Efficiency | Inline hints; first-time empty states with examples; longer/explicit button labels; one-action-per-screen. | Keyboard shortcuts; multi-select; bulk operations; minimal hand-holding once learned. |
| TD-04 Information Density vs Cognitive Load | Wide tables; compact rows; rich column count; minimal whitespace. | Card layouts; one record per screen at a time; generous spacing; summary-first patterns. |
| TD-05 Automation vs User Control | System-default values pre-filled; auto-save; background processing with status indicator. | User selects every step; explicit confirmations; transparent system state; undoable defaults. |
| TD-06 Consistency vs Contextual | Reuse the standard table/form pattern across screens; resist per-screen exceptions. | Per-context layout variants; admit a "this screen is different" affordance. |
| TD-07 Guidance vs Freedom | Multi-step wizard; progress indicator; locked sequence with back/next. | Single screen with free order; user-chosen entry points; no fixed sequence. |
| TD-08 Discoverability vs Minimalism | All actions visible as buttons/icons with labels; no hidden menus. | Progressive disclosure; overflow menus; minimal default surface. |
| TD-09 Security vs Convenience | Visible session state; logout affordance; re-authentication on sensitive actions; CSRF/SameSite-Strict cookies. | Persistent sessions; "remember me"; passwordless flows; reduced re-authentication friction. |
| TD-10 Accessibility vs Density | Larger hit targets; high contrast; ARIA labels; keyboard navigation; visible focus rings. | Tighter spacing; smaller hit targets where information density is the priority. |
| TD-11 Personalization vs Predictability | User-saveable views/filters; per-user defaults; remembered state. | Single shared layout per role; no per-user adaptation. |
| TD-12 Feedback Richness vs Speed | Visible status pills; toast confirmations on action; tooltips on metadata fields. | Suppress micro-confirmations; rely on absence-of-error as confirmation; minimal toasts. |
| TD-13 Error Prevention vs Speed | Mandatory fields validated before submit; confirmation modals on destructive actions; pre-flight checks. | Single-click submit; soft validation; undo over confirm. |
| TD-14 Transparency vs Cognitive Simplicity | Audit-trail viewer; "show why" affordances; rationale fields visible. | Hide system reasoning; present results without exposing logic. |
| TD-15 Precision vs Ease | Numeric inputs with decimal precision; explicit unit pickers; fine-grained filters. | Approximate/qualitative inputs; ranges over exact values; rounded display. |
| TD-16 Flat vs Deep Navigation | Top-level tabs; few hierarchy levels; broad navigation. | Hierarchical breadcrumbs; nested sections; drill-down paths. |
| TD-17 Broad vs Focused Menus | All options visible in a single menu surface. | Scoped menus per task; few options in any one menu. |
| TD-18 Search vs Browsing | Prominent search bar; search-first patterns; faceted search. | Browseable lists; category trees; recent/recommended sections. |
| TD-19 Contextual vs Global Navigation | Row actions; in-grid affordances; right-click menus. | Persistent main navigation; predictable global menu. |
| TD-20 Progressive Disclosure vs Immediate | Collapsible sections; "show advanced"; tabbed details. | All fields visible at once; no hidden controls. |
| TD-21 Single Screen vs Wizard | Single-page form with all fields; inline navigation between sections. | Stepper wizard; one step per screen; progress indicator. |
| TD-22 Persistent vs Workspace Focus | Always-visible sidebar/topbar; persistent navigation rail. | Hide navigation in task mode; full-bleed workspace. |
| TD-23 Modular Screens vs Continuity | Reusable card components; modal launch points. | Stay-in-context inline expansions; avoid screen transitions. |
| TD-24 Workflow Rigidity vs Flexibility | Locked state-machine; disabled actions outside legal transitions; status-driven UI. | Allow non-standard transitions with audit; admin override affordance. |
| TD-25 Batch vs Granular | Select-all + bulk action bar; multi-select on lists. | Row-level actions; one action at a time; no multi-select. |
| TD-26 Confirmation vs Flow | Modal confirmation on destructive/financial actions; "Are you sure?" pattern. | Suppress confirmations; rely on undo; single-click destructive only with toast-confirm. |
| TD-27 Inline Edit vs Validation | Click-to-edit cells; in-place editing of grid rows. | Modal/dedicated form for edits; submit-then-validate. |
| TD-28 Real-Time vs Typing Freedom | Live validation as user types; immediate error markers. | Validate only on blur or submit; no in-typing interruption. |
| TD-29 Undo vs Prevention | Toast-with-undo on every destructive action; reversible by default. | Confirm-first patterns; guards that block dangerous transitions. |
| TD-30 Keyboard vs Visual | Visible focus states; Enter to submit; Tab order designed; shortcut hints. | Mouse-led affordances; large buttons; icon-led navigation. |
| TD-31 Multi-Tasking vs Focus | Multiple-tab support; side-by-side panes; resizable split views. | Single-task surface; modal dialogs that block other interaction. |
| TD-32 Stateful vs Stateless | Draft auto-save; resume-where-you-left-off; persistent filter state. | Fresh start on every visit; URL-driven state only. |
| TD-33 Data Density vs Readability | Spreadsheet-style grids; dense column count. | Card layout; one record per row block; few columns. |
| TD-34 Visualization vs Interpretability | Charts and dashboards; trend lines; sparklines. | Plain numeric summaries; counts and totals only. |
| TD-35 Real-Time Updates vs Stability | Live-refresh table rows; auto-update on backend push. | Manual refresh button; stable view during interaction. |
| TD-36 Drill-Down vs Complexity | Expandable rows; nested drill paths; detail-on-demand. | Summary-only views; no drill; flat list. |
| TD-37 Aggregation vs Detail | Summary tiles; counts by status; rolled-up totals first. | Line-item lists; raw record table first. |
| TD-38 Customizability vs Shared | Column-customisable tables; saved-view affordance. | Standard layout enforced; no per-user customisation. |
| TD-39 Contextual Info vs Noise | Inline help icons; tooltips on every field; supporting metadata cells. | Strip secondary information; show primary data only. |
| TD-40 Governance vs Autonomy | Approval queues; permission-bound actions; explicit roles. | Self-service patterns; no approval gate; user-completes-task. |
| TD-41 Auditability vs Simplicity | Audit-trail panels; LastChangedUser/Date columns visible; history view per record. | No audit metadata in UI; trust system without visible trail. |
| TD-42 Role Separation vs Fluidity | Role-conditional surfaces; Importer-only vs Approver-only affordances; segregation of duties enforced in UI. | Common surface regardless of role; collaborative editing. |
| TD-43 Standard Process vs Local | Single canonical workflow; no per-team variations. | Per-team workflow override; configurable per business unit. |
| TD-44 Validation Strictness vs Speed | Format-validated inputs; rejected-on-invalid; structured error display. | Lenient input; warnings over errors; quick entry. |
| TD-45 Configurability vs Complexity | Settings panel; admin-configurable defaults; FileSetting/BulkFileSetting parameterisation surfaces. | Fixed behaviour; no settings; convention over configuration. |
| TD-46 Traceability vs Simplicity | Source/lineage metadata visible; provenance markers in UI. | Clean UI free of metadata clutter. |
| TD-47 Compliance vs Productivity | Consent gates; retention notices; data-subject-rights affordances; POPIA notices. | Frictionless flows free of compliance overhead. |
| TD-48 Integration vs Reliability | External-system status; integration health indicators; degraded-mode UX. | Self-contained operation; no external dependency visible. |
| TD-49 Minimalism vs Affordance | Subtle, refined controls. | Obvious labelled buttons; clearly clickable affordances. |
| TD-50 Brand vs Clarity | Branded chrome; distinctive design language. | Neutral, clarity-first design; standard patterns. |
| TD-51 Animation vs Performance | Animated transitions; motion design. | No animation; instant state changes; performance-first. |
| TD-52 White Space vs Capacity | Generous padding; airy layouts. | Compact, dense layouts. |
| TD-53 Hierarchy vs Equality | Strong primary CTA; visual emphasis on key actions. | Equal-weight controls; no visual priority. |
| TD-54 Collaboration vs Ownership | Shared workspaces; co-editing affordances. | Single-owner records; explicit handoff. |
| TD-55 Notification vs Focus | In-app notifications; email triggers on events. | Quiet mode; minimal notifications. |
| TD-56 Real-Time Collab vs Complexity | Live cursors; concurrent edit visibility. | Single editor; lock-and-edit pattern. |
| TD-57 Confidence vs Friction | Smooth, encouraging flows. | Safety friction; confirm-before-destructive. |
| TD-58 Familiarity vs Innovation | Standard patterns; familiar UI library components. | Novel UX; experimental interaction patterns. |
| TD-59 Trust by Simplicity vs Transparency | Simple, opaque interfaces. | Visible mechanics; explainable computations. |
| TD-60 Frontend Richness vs Maintainability | Rich interactive UI; client-state-heavy. | Simple server-rendered UI; minimal client state. |
| TD-61 Client-Side vs Security | Browser-side computation; offline capability. | Server-side trust boundary; no client logic for sensitive operations. |
| TD-62 Immediate vs Accurate Rendering | Optimistic UI updates; instant local state change. | Wait-for-backend-confirm patterns; show only confirmed state. |

If a dimension is not listed in this lookup (because triggers fired but no implication is curated), the per-goal guidance bullet reads: *"`TD-NN` lean=`<lean_label>` — implication not curated in reference; flag for consultant interpretation."*

---

## Prototype-deferred set

When `Target: prototype` is present in the requirements preamble, the following dimensions receive a `−2` raw-score contribution in Stage A — they are typically out of scope for prototype-mode applications per `framework/shared/prototype-invariants.md` PI-01..PI-05.

- TD-40 Governance vs User Autonomy
- TD-41 Auditability vs Workflow Simplicity
- TD-42 Role Separation vs Workflow Fluidity (kept if §1 explicitly names roles)
- TD-43 Standard Processes vs Local Optimization
- TD-46 Traceability vs UI Simplicity
- TD-47 Compliance vs Productivity
- TD-48 Cross-System Integration vs Reliability
- TD-54 Collaboration vs Ownership Clarity
- TD-55 Notification Frequency vs Focus
- TD-56 Real-Time Collaboration vs System Complexity

The penalty is suppressed if a domain-amplifier rule fires for the same dimension (see below). For `Target: application`, no prototype penalty applies.

---

## Domain-amplifier rules

A domain-amplifier adds `+1` to a dimension's raw score when the requirements doc's `§1` Domain string contains the trigger keyword AND the dimension is in the amplifier's target set. Amplifiers stack: multiple amplifiers can fire for the same dimension (e.g. a "financial banking" domain fires both `financial` and `banking` amplifiers if both are defined).

| Amplifier trigger (case-insensitive in §1) | Amplified dimensions |
| --- | --- |
| `financial`, `bank`, `banking`, `payment`, `transaction` | TD-01 Speed vs Accuracy (pulls B), TD-09 Security vs Convenience, TD-13 Error Prevention vs Speed, TD-26 Confirmation vs Flow, TD-29 Undo vs Prevention, TD-41 Auditability, TD-42 Role Separation, TD-44 Validation Strictness, TD-47 Compliance |
| `health`, `medical`, `clinical`, `patient` | TD-09 Security, TD-10 Accessibility, TD-13 Error Prevention, TD-41 Auditability, TD-44 Validation Strictness, TD-47 Compliance |
| `government`, `public sector`, `regulatory` | TD-41 Auditability, TD-43 Standard Processes, TD-46 Traceability, TD-47 Compliance |
| `consumer`, `retail`, `marketing`, `e-commerce` | TD-08 Discoverability, TD-12 Feedback Richness, TD-50 Brand Expression, TD-58 Familiarity |
| `internal tool`, `productivity`, `back-office`, `admin` | TD-03 Learnability vs Efficiency (pulls B), TD-04 Information Density, TD-25 Batch Operations, TD-30 Keyboard Efficiency, TD-33 Data Density |
| `realtime`, `real-time`, `streaming`, `monitoring`, `dashboard` | TD-12 Feedback Richness, TD-34 Visualization, TD-35 Real-Time Updates, TD-51 Animation, TD-60 Frontend Richness |
| `mobile`, `field`, `on-the-go` | TD-10 Accessibility, TD-32 Stateful Workflows, TD-52 White Space, TD-53 Visual Hierarchy |
| `ai`, `ml`, `machine learning`, `assistant`, `copilot`, `generative` | TD-05 Automation vs Control, TD-14 Transparency, TD-59 Trust by Transparency |

Amplifiers are additive — they cannot push a dimension above `+5` (cap), nor below `−5` (floor). They run after the prototype-deferred subtraction.

---

## Quality checks (run after Stage B and post-pass prune, before write)

Every check is a hard gate. If any check fails, the analyser does **not** write the artefact — it surfaces a structured error to the consultant and halts. (See `framework/agents/analyses/trade-off-dimension-analyser.md > Step 10 — Validate` for the halt contract.)

1. **Every goal in §4.1 appears as a matrix row.** No goal is silently omitted.
2. **Every final dimension carries pole-A and pole-B labels matching this reference.** No invented poles.
3. **Every non-zero cell has at least one `pole_*_hits` entry with quote and anchor.** No bare scores.
4. **Every `quote` is verbatim present in the read `requirements.md`** (substring check, case-insensitive). No fabricated evidence.
5. **No score outside `[−2, +2]`.** No fractional scores.
6. **Final dimension count is between floor (5) and cap (15) inclusive** — OR diagnostics records a consultant-override or under-floor outcome with explicit rationale.
7. **Every goal has a design-guidance card** with either 2–4 bullets (when non-zero cells exist) or the standard no-signal card.

---

## Anti-patterns

- **Run-time trigger generation.** Triggers come from this file, curated and reviewed. Do not synthesise triggers from dimension names at run time — that defeats audit.
- **Soft scoring.** No fractional scores. The Stage B mechanism produces integers `[−2, +2]` only.
- **Free-form rationales without evidence.** Every non-zero cell's `rationale` is derived from concrete hits in `pole_a_hits` / `pole_b_hits`. If no hits, the score is 0.
- **Bypassing the consultant gate.** The Stage A gate is mandatory. Never skip directly from Stage A to Stage B without surfacing the candidate set.
- **Filling the matrix to avoid empty cells.** A `0 (no-signal)` cell is a real outcome — leave it as a 0 rather than inventing a lean.
- **Editorialising on dimension importance.** This file is the contract; do not invent additional dimensions or alter pole labels at run time.

---

## See also

- `framework/assets/analyses/registry.md` — the row for `trade-off-dimension-analysis` references this file as `reference_asset`.
- `framework/shared/prototype-invariants.md` — PI-01..PI-05 inform the prototype-deferred set.
- `framework/shared/general-rules.md` — `GR-NN` deterministic rules; some overlap with TD-09 (security defaults) and TD-13 (error-prevention defaults).
- `framework/assets/analyses/ooux-reference.md` — the OOUX object map names the things this analysis scores trade-offs **for**. Use them together for downstream design.
- `framework/assets/analyses/jtbd-reference.md` — Jobs-to-be-Done complements trade-off dimensions: JTBD answers *why*, this analysis answers *which posture*.
- **Future row:** `decision-matrix` in `registry.md` is a generic options-vs-criteria scoring tool; trade-off dimension analysis is a goal-vs-axis scoring tool with a fixed taxonomy. The two are distinct.

### Relationship to existing Phase-1 stubs

The codebase contains pre-existing (unbuilt) stubs that share the trade-off-dimension vocabulary but operate at a different abstraction layer:

- `framework/assets/trade-off-dimensions.md` — STUB. Planned canonical taxonomy of **6 paired dimensions in 3 tiers** (Tier 1: Speed↔Accuracy, Power↔Simplicity; Tier 2: Density↔Focus, Control↔Automation, Flexibility↔Consistency; Tier 3: Memorability↔Density). Scoped to per-screen/view/component rating by the planned design-spec-drafter agent.
- `framework/skills/rate-against-dimensions.md` — STUB. Planned skill to apply −2..+2 ratings to screens, views, and components using the 6-dimension set above.
- `framework/assets/taxonomy-goals.md` — STUB. Planned user-goal taxonomy with quality-signal phrase → trade-off-position mapping.
- `framework/assets/references/user-goal-trigger-reference.md` — Conceptual seed for the planned taxonomy-goals.md. Contains a small quality-signal phrase → trade-off mapping table that overlaps with this reference's trigger-phrase tables.

**Layer relationship.** This methodology (trade-off-dimension-analysis) operates at **user-goal level** with a broad ~62-dimension taxonomy (`TD-01..TD-62`). The planned Phase-1 stubs operate at **screen / view / component level** with a curated 6-dimension subset (Tier 1/2/3). The two layers are complementary, not duplicative:

- Goal-level posture (this analysis) tells the wireframer *which axes matter and where each goal leans*.
- Screen-level rating (the planned Phase-1 stubs) tells the wireframer *how a specific design variant scores on the project's most relevant axes*.

**Canonical-source policy.** When the Phase-1 stubs are built, their 6-tier curated subset should be defined as `TD-01`, `TD-02`, `TD-04`, `TD-05`, `TD-06`, and (Tier 3) a Memorability-vs-Density axis to be added to this reference as a new `TD-NN` row. At that point, this reference becomes the canonical taxonomy and the screen-level rating files reference its IDs. No re-definition; only reference.

---

## Voice and stance

The analyser's stance is defined in `framework/assets/characters/trade-off-dimension-analysis.md` — analytical, mechanical, evidence-bound. This reference defines **what** to do; the character file defines **how** the agent talks while doing it.

The artefact is human-read (and consumed downstream by `/wireframe`'s `blueprint-architect` via the per-analysis sidecar), so the analyser also follows `framework/shared/output-readability.md`: it opens with an **In plain terms** lead (`<section id="plain-terms">` carrying `{{PLAIN_SUMMARY}}`) as the **first content section**, above the overview — a 2–5 sentence plain-English summary (what this matrix is, what it found, what to do with it) that introduces no goal, dimension, count, or `[SRC]` not already present. It glosses methodology jargon (trade-off dimension, pole, lean/score) at first use in human-readable prose, leaves client domain vocabulary unglossed (GLOSSARY territory), and keeps every `[SRC: C-NNN]` marker. The plain-language layer is confined to the lead + first-use glosses; the matrix, guidance cards, relevance table, JSON, and diagnostics keep their concrete, telegraphic discipline.
