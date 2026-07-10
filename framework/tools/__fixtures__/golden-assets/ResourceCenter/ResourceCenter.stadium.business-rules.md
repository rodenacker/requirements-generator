---
stadium_asset: business-rules
app: ResourceCenter
file_guid: 27cac42c-3dc4-44fd-99a0-84d001ccd971
designer_version: 6.14.3378.13771
selected_package: 4dd7964f-aadd-4ba2-ad82-9cf8fa1f9aa7.sapz
deployment_count: 4
last_published: 2026-06-03 11:01:11.2158983
extracted_from: C:\Stadium 6 Web Apps\27cac42c-3dc4-44fd-99a0-84d001ccd971
provenance: deterministic extraction from the Stadium 6 design model + administration.db
marker_legend: Tier-A lines are authoritative facts ([SRC]-quotable); Tier-B lines are advisory design signals.
---
# Business rules & behaviour — ResourceCenter

## Tier-A — event logic (scripts → action sequences)

> Each script is classified by its **trigger** (0g): *user-initiated* (a control event — `.Click/.Change/…`), *automatic-on-open* (a page/template `.Load`), or *other* (a helper invoked via CallScript, or a timer/lifecycle hook). User-initiated scripts are rendered gesture-first; the *goal* a gesture serves is advisory (Tier-B), the gesture itself is fact.

### Automatic — on page / template open

#### FAQ.Load  [from script, surface: FAQ]
- Trigger: **automatic-on-open**  (`.load`)
- Sequence: List → SetValue
  - SetValue: Target=List; Value=List

#### Docs.Load  [from script, surface: Docs]
- Trigger: **automatic-on-open**  (`.load`)
- Sequence: ExecuteConnector → DownloadFile
  - ExecuteConnector: ConnectorFunction=ReadFile

## Tier-A — notification points

_No notification or dialog actions in the design model._

## Tier-A — validation

_No validators, required-field flags, or control validation rules in the design model._

## Tier-A — edge / empty / error / loading state signals

_No explicit spinner/visibility toggles, error notifications, or empty/null guards in the design model._

## Tier-A — bespoke inline-JS rules

_No bespoke (non-library, non-DOM/timing) inline-JS blocks in the design model._
