# stadium/asset-schemas.md — per-app extracted-asset schemas & drafter mapping

The canonical schema-doc for the **per-app** assets the Stadium extractor emits, plus the thin contract the requirements drafter follows when citing them. (For the platform concepts behind these assets see `glossary.md`; for the per-app assets' *origin* see `sapz-spec.md` + `admindb-schema.md`.)

When the extractor runs with `--emit-assets <dir> --stem <Stem>`, it writes one lean markdown file per category as **`<Stem>.stadium.<category>.md>`** into that engagement's `input/` directory. Two tiers of asset exist:

- **Tier-1 (deterministic, Python)** — written by `emit_assets()` in `extract_stadium_app.py`. Ten files: `overview`, `data-model`, `data-sources`, `business-rules`, `access-control`, `surfaces`, `navigation`, `glossary`, `design-signals`, `modules`.
- **Tier-2 (LLM-inferred, advisory)** — added on top by the extraction skill: `task-flows`, `quality-signals`. These are inference, not extraction; they are advisory throughout.

## (a) The YAML provenance header

Every Tier-1 asset opens with the same frontmatter (`_prov_header()`):

```yaml
---
stadium_asset: <category>          # the category slug, e.g. data-model
app: <App name>                    # from design model / admin.db / appsettings
file_guid: <FileGuid>              # app's stable identity = folder name
designer_version: <x.y.z.b>        # Stadium Designer build that published it
selected_package: <GUID>.sapz      # which deployment was read
extracted_from: <abs app folder>   # provenance trail
provenance: deterministic extraction from the Stadium 6 design model + administration.db
marker_legend: Tier-A lines are authoritative facts ([SRC]-quotable); Tier-B lines are advisory design signals.
---
```

The header is forensic provenance: it ties every asset back to a specific app + deployment so a fact can be audited. (Tier-2 assets carry the same header shape, written by the skill.)

## (b) Tier-A vs Tier-B + the inline locators

Inside each asset, content is split by **explicit `## Tier-A —` / `## Tier-B —` headings**:

- **Tier-A** = provably present in source. Authoritative. Quotable as `[SRC: <asset-filename>]`.
- **Tier-B** = advisory design signal (layout, control-choice, inferred domain). Never authoritative.

Tier-A lines carry an **inline locator** in square brackets naming the exact source within the app:
- `[from design model]` / `[from connector: <FnName>]` / `[from stored-procedure: <ProcName>]` / `[from web-service: <METHOD> <path>]` / `[from script, owner: <Page>]` / `[from administration.db]` / `[from admin.db: <Table>]` / `[from appsettings]`.
- The three data-model locators (`connector` = SQL query/view, `stored-procedure`, `web-service`) name which **evidence class** grounds a field, so a reviewer can weight it (SQL columns and proc/endpoint field-names are all Tier-A; web-service field *types* are often weak — see §(e)). They are byte-stable, sanitized renderings and must be quoted **verbatim** (grounding is byte-exact).

Tier-B / gap / inferred lines carry a provenance **marker** instead: `` `[AI-SUGGESTED: domain inference]` ``, `` `[AI-SUGGESTED: blocking]` `` (for gaps), `` `[AI-SUGGESTED]` `` (for implications). These mirror the system's own marker vocabulary (`CLAUDE.md` §2).

### Tier assignment for the behaviour / actor-model enrichment (load-bearing)

The behaviour-enrichment sub-sections (0a–0h, 1a–1e) split fact from interpretation on the **groundedness** axis. What is a fact vs a reading:

- **Tier-A (fact, no marker):** the affordance's control + verbatim **label** + wired script (0e); the **validator** target + rule + verbatim message (0f); the **trigger token** in the script name (`.Click`/`.Load`) and its user-initiated/automatic classification (0g); the ordered actions + **branch tree** structure (1a/1c); the guard **predicate** operands (1b); the notification **message text + `NotificationType`-decoded `success/error/info`** (0a); the **state toggle / error-type / guard predicate** facts (1d); page name + `IsStartPage` + reachability (0b/0c); RBAC roles, grants, counts, matrix, and the single-operator **posture statement** itself (0d); the journey **edges/gestures/page-kinds** (1e); the scaffold **skeleton** (task-clusters + surfaces + notifications per actor, 0h).
- **Tier-B (`[AI-SUGGESTED]`, never `[SRC]`-citable):** the candidate **task** named from a verb (0e); the **goal** a gesture serves (0g); the inferred page **kind** from the suffix taxonomy (0b); the operator **symbol** where the enum was best-guessed (1b — `op<N>` when unmapped); the state **classification** `{loading/empty/error/permission}` (1d); the **capability split** and **actor-candidate** reading — task-cluster→distinct-operator, recipient→second-actor (0d); the journey **narrative** (that a chain *is one* end-to-end task, 1e).
- **The actor / persona scaffold's two-tier shape (0h):** its **skeleton is Tier-A** (the clusters/surfaces/notifications are joined from source facts); its **narrative fields — `name`, `goal`, `motivation`, `pain-points`, `success-metric` — are rendered as empty `` `[AI-SUGGESTED: blocking]` `` gap prompts, never as asserted content.** Authoring those at ingest would fabricate — the `.sapz` cannot ground them. They become resolver questions downstream; persona *narrative synthesis* stays a `/analyse-*` and `/requirements` concern. PII guard: the recipient signal surfaces only *that* an external recipient exists (+ a role-ish label), never an address; actors are named neutrally (`Operator A`, `Role: <name>`).

## (c) Citation discipline for the drafter (load-bearing)

This is the contract the `/requirements` drafter must honour when ingesting these assets:

1. **Tier-A lines are authoritative and `[SRC]`-citable.** Cite them as `[SRC: <Stem>.stadium.<category>.md]` (the manifest-row `filename` payload, per the `[SRC: <filename>]` convention in `CLAUDE.md` §2). **Quote verbatim, including the inline `[from …]` locator**, so the downstream consumer can trace the fact to the exact connector/page/table.
2. **Tier-B, advisory, and `[AI-SUGGESTED]` lines must NEVER be cited as `[SRC]`.** They are mined as *requirement signals* (the *how*, per `CLAUDE.md` §1) — they bias design, they do not bind it. A `how`-decision that honours one cites the *signal*; it does not promote it to an authoritative fact. Gap lines (`[AI-SUGGESTED: blocking]`) become resolver questions, not requirements.
3. **The closed property set comes from Tier-A `data-model`.** Object properties the wireframe pipeline depends on (the `Shape.Field` closed set, `CLAUDE.md` §1) are exactly the Tier-A `data-model` **fields** — never widen them from a Tier-B inference. API/proc-derived fields enter the closed set **by name** (a field's *type* is omitted when it did not resolve concretely — never emitted as `Object`); web-service **endpoints** (method/URL/host) are handoff-only `data-sources` material, **not** §7 properties. Likewise the Cluster A **control enums (`Options`) and DataGrid column labels** in `surfaces` are *surface* facts the drafter maps onto an **existing** §7 data-model property's `ui_display`/`Enums` — they **never mint a new §7 property** (a column carries no `DataField`, and an inline enum is a control setting, not a persisted field).

## (d) Asset → downstream mapping

What each asset contains and where it feeds:

| Asset (`<Stem>.stadium.<cat>.md`) | Contains | Feeds → `requirements.md` § / pipeline |
|---|---|---|
| `overview` | App facts (name, version, auth, theme, counts), Tier-B candidate domain entities, the blocking **gaps** list, an asset index | §1 (purpose/context); gaps → resolver questions |
| `data-model` | Tier-A entities + fields **reconciled across SQL queries/views, stored procedures and web-service calls** (union by name; each field carries its `[from …]` locator + `: Type` only when concretely resolved), the CRUD matrix (with an Evidence column), a Tier-B "unclassified stored procedures" list + status-field lifecycle hint | §7 (data shapes — the closed property set) + §2 |
| `data-sources` | Connectors + ConnectorFunctions: SQL blocks, stored-procedure names, **web-service endpoints (method/path + resolved body/response type)**, redacted connection strings + typed params — **handoff-only backend contract** | §6.10 (fixtures→contract pointers) + §1.7; never a prototype design input |
| `business-rules` | Scripts as **branch-structured** flows (grouped by trigger — user-initiated / automatic-on-open / other — and rendered gesture-first, with `IF <predicate> → […] / ELSE → […]` branch trees + a flat `Sequence:` back-compat line); guard **conditions** (1a/1b); **notification points** (0a — verbatim message + decoded `success/error/info` severity + dialog/toast); **per-control validation (Cluster A #1 — 0f: target field + rule expression + verbatim message + `required`, deduped across pages; the intent label email/numeric/date/length is Tier-B `[AI-SUGGESTED]`)** plus any design-model validators; **trigger classification / gesture-first framing (0g/1c)**; **edge/empty/error/loading state signals (1d)** | §6 (functions, business rules, behaviour); notifications → §6.8; states → §6.4.5; **validation → §6.3** + §6.2/§6.4.5; triggers/gestures → §5 |
| `access-control` | Auth type, roles; a **conditional** matrix/posture (0d — the real Page×Role matrix + capability split when RBAC is configured, else an explicit single-operator posture statement + the full capability surface); the **actor-candidate reading (0d, PII-guarded)** — task-cluster split + external send-recipient *existence*; the **actor / persona scaffold (0h)** — a grounded skeleton per candidate actor; and user/admin **counts only** (individual identities — name/email — are PII and NOT extracted) | §3 (actors/personas) + §6.5 (access rules) |
| `surfaces` | The **view / task / feature inventory (0b)** (page · start? · design-surface? · reachable? · inferred kind); per-page control trees (layout + controls + visible text + **inline field-behaviour constraints — Cluster A #1: help `Hint`/`ToolTip`, editability `ReadOnly`/password, multi-line, static / `dynamic (bound)` enums, grid affordances**); **resolved DataGrid column sets (Cluster A #2 — ordered `"HeaderText"` · `(hidden)` · `(action)`)**; the **action-affordance inventory → candidate tasks (0e)** (control · label · wired script → candidate task); templates; best-effort screen↔entity guesses | §6.4 (surfaces, UI feature needs) + §7 (`ui_display` / Enums, via existing data-model fields) + §5/screen-classification + `/wireframe` (surface decomposition + per-surface closed set) |
| `navigation` | Templates (master pages); `NavigateToPage` edges; **navigation reachability / orphans (0c)** (coverage stat + orphan list + JS-nav caveat); **candidate cross-surface journeys (1e)** (nav edges + gesture + actor, JS-nav gaps shown as explicit breaks); Tier-B affordances | §5 (IA/navigation, journeys) + design-spec §4 (entry/exit) + `/wireframe` IA |
| `glossary` | Verbatim visible terms (labels, headings, buttons, titles) | `/analyse-inputs` GLOSSARY methodology (domain vocabulary) |
| `design-signals` | Theme, styling classification, custom CSS, fonts — entirely Tier-B | `/design-system` (via the manual bridge — `theming-model.md`) |
| `modules` | Tier-A detected `stadium-software` modules + CSS footprint, Tier-B implication | §1.7 (capabilities) + required-interaction behaviours |
| `task-flows` *(Tier-2)* | LLM-inferred task flows **with decision points + exception paths** (mirroring requirements §5 `steps / decision_points / exception_paths`), **per-role variants** where `access-control` shows a configured split, and **actor → gesture → goal** framing seeded by the candidate tasks (0e), gesture/trigger framing (0g/1c), actor candidates + scaffold (0d/0h) and candidate journeys (1e). Advisory throughout — every substantive line `[AI-SUGGESTED]`; candidates stay candidates | §5 + JTBD framing |
| `quality-signals` *(Tier-2)* | LLM-inferred quality/UX observations (advisory) | `/wireframe` variant philosophy |

Tier-2 assets (`task-flows`, `quality-signals`) are inference layered over the deterministic extraction; treat them as advisory throughout — they are never `[SRC]`-citable, regardless of any Tier-A heading the skill may format them with.

## (e) Data-model reconciliation & safety rails

The `data-model` asset is built by `reconcile_entities()` in `extract_stadium_app.py`, which unions entities across **three evidence classes** — SQL connector queries/views (`_sql_shape`), stored procedures (`_sp_shape`: entity+op from the `<prefix>_[Stadium_]<Entity>_<Op>` name, fields from parameters), and web-service calls (`_ws_shape`: entity name from the Body/Response `GuidReference → CustomType.Name`, fields from the function's bound Parameter/DataResult struct). The design intent is the **most complete field set per entity**. The rails that keep this union truthful:

- **Union by normalized name (aggressive).** One entity per normalized name; SQL `Members` + API `member` collapse, but distinct DTO variants (`member` vs `fullmember`) keep separate stems and are cross-listed as advisory `related shapes`, never merged. A field may therefore be broader than any single backend record — that is intentional completeness, not fabrication, because…
- **…every field is real and carries per-source `[from …]` locators.** Nothing is invented; the drafter cites each field to its exact SQL/proc/endpoint source. Multiple sources for one field are recorded (the asset shows the first locator + a `(+N more)` note).
- **Envelope/transport filtering.** `_ENVELOPE_DENY` (`success, message, raiseexceptions, statuscode, responsebody, apiresponse`) drops status/transport wrappers from proc params + web-service payloads; a broader `_ENTITY_DENY` (adds `result, error, response, data`) blocks transport/scratch entity names from **all** sources — this also removes SQL `DECLARE @result TABLE(…)` scratch table-variables. The field denylist is deliberately narrow so real columns (e.g. a multi-tenant `ApplicationID` FK) are **kept**.
- **Weak types omitted.** A field emits `: Type` only when a concrete design-model / SQL / proc type resolved; `System.Object` (common for API shapes) and unresolved types are dropped, leaving the field **name-only**. Type precedence: design-model `SimpleDataType` > SQL/proc `DbType` > web-service > omit.
- **`IsDataField` is NOT a gate.** The flag is uniformly `0` across deployed `.sapz` models in practice, so gating on it would drop every field; the envelope denylist is the real guard (see `sapz-spec.md`).
- **Unclassified stored procedures** (name yields no recognized entity/op) are listed under a Tier-B heading, never fabricated into an entity.

Correctness of this reconciliation (entity separation, no envelope fields, weak-type omission) is the **extractor's** responsibility and is **not** caught by the skill's Phase-A parse-check (which only asserts each asset exists and is non-empty).
