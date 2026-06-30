# stadium/admindb-schema.md — the `administration.db` reference

`administration.db` is a SQLite database in **every** Stadium app folder (a sibling of the `.csproj`). It holds the deployed app's **security model** (roles, page access, users), its **connection strings**, its **deploy history**, and an **audit log**. The extractor reads it in `read_admin_db()`.

## Schema is stable

The schema is **identical across all apps** — verified across 18 apps carrying an `administration.db`, all returning the same **14-table** signature:

```
AccessLookupEntries, ApplicationUpdates, Applications, AuditLogs,
AuthenticationSettings, Connections, PageRole, Pages, Roles,
Settings, SmtpSettings, UserRole, Users, sqlite_sequence
```

(`sqlite_sequence` is the SQLite-internal autoincrement bookkeeping table — 13 app tables + that internal = 14.)

> Note the **auth type itself** (`Cookie` / `OAuth`) is NOT in `administration.db` — it comes from `appsettings.json > Config.AuthenticationType`. The `AuthenticationSettings` table here is a name/value bag and is empty in practice.

## RBAC — the security model

Role-based. A **Role** grants access to a set of **Pages**; a **User** holds a set of **Roles** (or is a global administrator).

### Page × Role access matrix — `Pages ⋈ PageRole ⋈ Roles`

```sql
SELECT p.Name AS page, r.Name AS role
FROM PageRole pr
JOIN Pages p ON p.Id = pr.PageId
JOIN Roles r ON r.Id = pr.RoleId
ORDER BY p.Name, r.Name;
```

A page absent from `PageRole` has no role grant recorded. `Pages` columns: `Id, Name, IsStartPage`. `Roles` columns: `Id, Name, NormalizedName`.

### User × Role — `Users ⋈ UserRole ⋈ Roles`

```sql
SELECT u.UserName, u.Email, u.IsAdministrator, r.Name AS role
FROM Users u
LEFT JOIN UserRole ur ON ur.UserId = u.Id
LEFT JOIN Roles r ON r.Id = ur.RoleId
ORDER BY u.UserName;
```

`Users` columns: `Id, UserName, Name, Email, PasswordHash, SecurityStamp, IsAdministrator, NormalizedUserName, NormalizedEmail, UniqueId`. **`Users.IsAdministrator`** (bool) = a global admin who bypasses page-role checks. The extractor surfaces only `username / name / email / is_administrator` — never `PasswordHash`/`SecurityStamp`. Users are usually a tiny set (often the developer + a couple of test accounts), not the real user base.

### `Connections` — connection strings (passwords MUST be redacted)

```sql
SELECT Name, ConnectionString FROM Connections;
```

Columns: `Id, Name, DefaultValue, ConnectionString`. These are the **live** connection strings to the client's internal databases — handoff-only, backend-contract material. **Passwords must always be redacted.** The extractor's `sanitize_conn()` masks `Password=…` / `Pwd=…` in SQL-Server strings and the `Password` key in FileSystem-connector JSON, replacing the value with `<redacted>` while keeping host / catalog / user visible. Never emit an unredacted connection string into any asset.

### Tables that are usually empty / unused

- **`Settings`** — name/value/default app settings (`Id, Name, DefaultValue, Value`). Sometimes populated, often sparse.
- **`SmtpSettings`** — outbound email config (`Id, FromAddress, SmtpServer, SmtpUsername, SmtpPassword, SmtpPort, EnableSsl`). Usually **empty**. If populated, `SmtpPassword` is a secret — redact.
- **`AuthenticationSettings`** — name/value bag (`Id, Name, DefaultValue, Value`). Usually **empty** (auth type lives in `appsettings.json`).
- **`AccessLookupEntries`** — (`Id, Description, PageId`). Observed **always empty** across apps — document as unused.

### Deploy history & identity

- **`ApplicationUpdates`** — one row per deployment (`Id, UserId, Username, DesignerVersion, DateTime`). The extractor selects the **latest** `.sapz` by joining each package's GUID filename to this table's `DateTime` (newest wins); it also reports the deploy history and "last published by / when".
- **`AuditLogs`** — change log (`Id, ChangedOn, ChangedBy, Source, Type, Action, OldValue, NewValue`). Forensic; surfaced as a flat list.
- **`Applications`** — one row identifying the app (`FileGuid, Name, WebApiKey`). **`FileGuid`** is the app's stable identity and **equals the app folder name**. `WebApiKey` is a secret — do not emit.
