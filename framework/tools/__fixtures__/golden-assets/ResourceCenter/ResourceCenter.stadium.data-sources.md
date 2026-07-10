---
stadium_asset: data-sources
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
# Data sources — ResourceCenter

> **Internal data-source contract — handoff-only.** The SQL / stored procedures / API endpoints below name the client's internal databases and services. Treat as backend-contract material, not prototype design input (only the payload *field names* in `data-model` are §7 shapes).

## Tier-A — connectors & operations

### FileSystem — FileSystem
- Connection (redacted): `{"Path": "D:\\Development\\StadiumApps\\ResourceCenter\\docs", "User": "", "Password": ""}` [from administration.db / design model]
- **DeleteFile** (DeleteFile) — params: FileName:Parameter [from connector: FileSystem]
- **FileExists** (FileExists) — params: FileName:Parameter [from connector: FileSystem]
- **ReadFile** (ReadFile) — params: FileName:Parameter [from connector: FileSystem]
- **WriteFile** (WriteFile) — params: FileName:Parameter, FileContents:Parameter [from connector: FileSystem]

## Tier-A — technology stack (NFR baseline)

- Backend framework: **net8.0-windows** [from .csproj]
- Frontend: **Vue ^3.5.22** [from package.json]
- Data providers: `Microsoft.Data.SqlClient`, `Microsoft.EntityFrameworkCore.Sqlite`, `Oracle.ManagedDataAccess.Core`, `System.Data.Odbc` [from .csproj]
- Notable backend capabilities: `EPPlus`, `IdentityModel.AspNetCore.OAuth2Introspection`, `Microsoft.AspNetCore.SignalR.Protocols.NewtonsoftJson`, `Serilog.AspNetCore`, `Serilog.Sinks.EventLog` [from .csproj]
