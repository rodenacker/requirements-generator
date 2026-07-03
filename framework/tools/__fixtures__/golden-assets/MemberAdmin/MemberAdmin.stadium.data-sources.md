---
stadium_asset: data-sources
app: MemberAdmin
file_guid: 785d3104-7f1a-4d0d-9689-566e0c21295b
designer_version: 6.14.3378.13771
selected_package: 9edc4a95-3fde-45b4-899a-2a59d1c23452.sapz
extracted_from: C:\Stadium 6 Web Apps\785d3104-7f1a-4d0d-9689-566e0c21295b
provenance: deterministic extraction from the Stadium 6 design model + administration.db
marker_legend: Tier-A lines are authoritative facts ([SRC]-quotable); Tier-B lines are advisory design signals.
---
# Data sources — MemberAdmin

> **Internal data-source contract — handoff-only.** The SQL / stored procedures / API endpoints below name the client's internal databases and services. Treat as backend-contract material, not prototype design input (only the payload *field names* in `data-model` are §7 shapes).

## Tier-A — connectors & operations

### Members (Database)
- Connection (redacted): `Data Source=.;Initial Catalog=Members;Integrated Security=False;User ID=sa;Password=<redacted>;Trust Server Certificate=True` [from administration.db / design model]
- **MembersSelect** (SqlQuery) — params: none [from connector: Members]
  ```sql
  SELECT m.ID ,FirstName ,LastName ,Email ,DOB ,CityID ,Subscribed ,City FROM dbo.Members m inner join Cities c on m.CityID = c.ID
  ```
- **MemberInsert** (SqlQuery) — params: FirstName:String, LastName:String, Email:String, Password:String, DOB:String, CityID:String, Subscribed:String [from connector: Members]
  ```sql
  INSERT INTO dbo.Members (FirstName ,LastName ,Email ,Password ,DOB ,CityID ,Subscribed ,UpdateDateTime) VALUES (@FirstName ,@LastName ,@Email ,@Password ,@DOB ,@CityID ,@Subscribed ,getDate() );
  ```
- **CitiesSelect** (SqlQuery) — params: none [from connector: Members]
  ```sql
  SELECT ID ,City FROM dbo.Cities order by City
  ```
- **MemberSelect** (SqlQuery) — params: ID:String [from connector: Members]
  ```sql
  SELECT ID ,FirstName ,LastName ,Email ,Password ,DOB ,CityID ,Subscribed FROM dbo.Members WHERE ID = @ID;
  ```
- **MemberUpdate** (SqlQuery) — params: FirstName:String, LastName:String, Email:String, Password:String, DOB:String, CityID:String, Subscribed:String, ID:String [from connector: Members]
  ```sql
  UPDATE dbo.Members SET FirstName = @FirstName ,LastName = @LastName ,Email = @Email ,Password = @Password ,DOB = @DOB ,CityID = @CityID ,Subscribed = @Subscribed ,UpdateDateTime = getDate() WHERE ID = @ID;
  ```
- **MemberDelete** (SqlQuery) — params: ID:String [from connector: Members]
  ```sql
  DELETE FROM dbo.Members WHERE ID = @ID;
  ```
