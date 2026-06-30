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
- `[from design model]` / `[from connector: <FnName>]` / `[from script, owner: <Page>]` / `[from administration.db]` / `[from admin.db: <Table>]` / `[from appsettings]`.

Tier-B / gap / inferred lines carry a provenance **marker** instead: `` `[AI-SUGGESTED: domain inference]` ``, `` `[AI-SUGGESTED: blocking]` `` (for gaps), `` `[AI-SUGGESTED]` `` (for implications). These mirror the system's own marker vocabulary (`CLAUDE.md` §2).

## (c) Citation discipline for the drafter (load-bearing)

This is the contract the `/requirements` drafter must honour when ingesting these assets:

1. **Tier-A lines are authoritative and `[SRC]`-citable.** Cite them as `[SRC: <Stem>.stadium.<category>.md]` (the manifest-row `filename` payload, per the `[SRC: <filename>]` convention in `CLAUDE.md` §2). **Quote verbatim, including the inline `[from …]` locator**, so the downstream consumer can trace the fact to the exact connector/page/table.
2. **Tier-B, advisory, and `[AI-SUGGESTED]` lines must NEVER be cited as `[SRC]`.** They are mined as *requirement signals* (the *how*, per `CLAUDE.md` §1) — they bias design, they do not bind it. A `how`-decision that honours one cites the *signal*; it does not promote it to an authoritative fact. Gap lines (`[AI-SUGGESTED: blocking]`) become resolver questions, not requirements.
3. **The closed property set comes from Tier-A `data-model`.** Object properties the wireframe pipeline depends on (the `Shape.Field` closed set, `CLAUDE.md` §1) are exactly the Tier-A `data-model` columns — never widen them from a Tier-B inference.

## (d) Asset → downstream mapping

What each asset contains and where it feeds:

| Asset (`<Stem>.stadium.<cat>.md`) | Contains | Feeds → `requirements.md` § / pipeline |
|---|---|---|
| `overview` | App facts (name, version, auth, theme, counts), Tier-B candidate domain entities, the blocking **gaps** list, an asset index | §1 (purpose/context); gaps → resolver questions |
| `data-model` | Tier-A entities + typed fields (`Entity.Field : Type [from connector: …]`), the CRUD matrix, Tier-B status-field lifecycle hint | §7 (data shapes — the closed property set) + §2 |
| `data-sources` | Connectors, ConnectorFunctions, redacted connection strings, SQL + typed params — **handoff-only backend contract** | §6.10 (fixtures→contract pointers) + §1.7; never a prototype design input |
| `business-rules` | Scripts → ordered action sequences (ExecuteConnector/SetValue/Navigate/…), validators + required fields | §6 (functions, business rules, behaviour) |
| `access-control` | Auth type, roles, the Page×Role matrix, and user/admin **counts only** (individual user identities — name/email — are PII and are NOT extracted) | §3 (actors/personas) + §6.5 (access rules) |
| `surfaces` | Per-page control trees (layout + controls + visible text), templates, best-effort screen↔entity guesses | §6.4 (surfaces) + `/wireframe` (surface decomposition) |
| `navigation` | Templates (master pages), `NavigateToPage` edges, Tier-B affordances | §5 (IA/navigation) + `/wireframe` IA |
| `glossary` | Verbatim visible terms (labels, headings, buttons, titles) | `/analyse-inputs` GLOSSARY methodology (domain vocabulary) |
| `design-signals` | Theme, styling classification, custom CSS, fonts — entirely Tier-B | `/design-system` (via the manual bridge — `theming-model.md`) |
| `modules` | Tier-A detected `stadium-software` modules + CSS footprint, Tier-B implication | §1.7 (capabilities) + required-interaction behaviours |
| `task-flows` *(Tier-2)* | LLM-inferred ordered task paths through the app (advisory) | §5 + JTBD framing |
| `quality-signals` *(Tier-2)* | LLM-inferred quality/UX observations (advisory) | `/wireframe` variant philosophy |

Tier-2 assets (`task-flows`, `quality-signals`) are inference layered over the deterministic extraction; treat them as advisory throughout — they are never `[SRC]`-citable, regardless of any Tier-A heading the skill may format them with.
