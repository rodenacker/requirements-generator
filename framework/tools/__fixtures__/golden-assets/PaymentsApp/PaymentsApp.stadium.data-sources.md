---
stadium_asset: data-sources
app: PaymentsApp
file_guid: be54c8c9-dc03-43d5-bc2b-fba14e07f360
designer_version: 6.14.3378.13771
selected_package: 2211275f-1cb9-495c-91cf-4ff48dc4c142.sapz
deployment_count: 1
last_published: 2026-06-30 12:29:25.6302212
extracted_from: C:\Stadium 6 Web Apps\be54c8c9-dc03-43d5-bc2b-fba14e07f360
provenance: deterministic extraction from the Stadium 6 design model + administration.db
marker_legend: Tier-A lines are authoritative facts ([SRC]-quotable); Tier-B lines are advisory design signals.
---
# Data sources — PaymentsApp

> **Internal data-source contract — handoff-only.** The SQL / stored procedures / API endpoints below name the client's internal databases and services. Treat as backend-contract material, not prototype design input (only the payload *field names* in `data-model` are §7 shapes).

## Tier-A — connectors & operations

### FileSystem — FileSystem
- Connection (redacted): `{"Path": "C:\\DigiataRepos\\DigiataApps\\PaymentsApp\\Tests\\", "User": "", "Password": ""}` [from administration.db / design model]
- **DeleteFile** (DeleteFile) — params: FileName:Parameter [from connector: FileSystem]
- **FileExists** (FileExists) — params: FileName:Parameter [from connector: FileSystem]
- **ReadFile** (ReadFile) — params: FileName:Parameter [from connector: FileSystem]
- **WriteFile** (WriteFile) — params: FileName:Parameter, FileContents:Parameter [from connector: FileSystem]

### PaymentsApiSetup — REST / HTTP  ·  ⚠ mock / non-prod host `[AI-SUGGESTED]`
- Connection (redacted): `{"URL": "http://localhost:10009/PaymentsApp/", "Auth": "ApiKey", "KeyLocation": "Header", "KeyName": "X-API-Key", "KeyValue": "Test123", "Timeout": 90}` [from administration.db / design model]
- **BeneficiaryGetList** (WebServiceFunction) — params: RaiseExceptions:RaiseExceptionsParameter [from connector: PaymentsApiSetup]
  - endpoint: `GET /v1/beneficiaries` — response: BeneficiaryReadList
- **BeneficiaryCreate** (WebServiceFunction) — params: RaiseExceptions:RaiseExceptionsParameter, Body:WebServiceParameter, LastChangedUser:WebServiceParameter [from connector: PaymentsApiSetup]
  - endpoint: `POST /v1/beneficiaries` — body: BeneficiaryWrite, response: DefaultResponse
- **BeneficiaryGetById** (WebServiceFunction) — params: RaiseExceptions:RaiseExceptionsParameter, Id:WebServiceParameter [from connector: PaymentsApiSetup]
  - endpoint: `GET /v1/beneficiaries/{Id}` — response: BeneficiaryRead
- **BeneficiaryUpdate** (WebServiceFunction) — params: RaiseExceptions:RaiseExceptionsParameter, Body:WebServiceParameter, Id:WebServiceParameter, LastChangedUser:WebServiceParameter [from connector: PaymentsApiSetup]
  - endpoint: `PUT /v1/beneficiaries/{Id}` — body: BeneficiaryWrite, response: DefaultResponse
- **BeneficiaryDelete** (WebServiceFunction) — params: RaiseExceptions:RaiseExceptionsParameter, Id:WebServiceParameter, LastChangedUser:WebServiceParameter [from connector: PaymentsApiSetup]
  - endpoint: `DELETE /v1/beneficiaries/{Id}` — response: DefaultResponse
- **BusinessUnitGetList** (WebServiceFunction) — params: RaiseExceptions:RaiseExceptionsParameter [from connector: PaymentsApiSetup]
  - endpoint: `GET /v1/business-units` — response: BusinessUnitReadList
- **BusinessUnitCreate** (WebServiceFunction) — params: RaiseExceptions:RaiseExceptionsParameter, Body:WebServiceParameter, LastChangedUser:WebServiceParameter [from connector: PaymentsApiSetup]
  - endpoint: `POST /v1/business-units` — body: BusinessUnitWrite, response: DefaultResponse
- **BusinessUnitGetById** (WebServiceFunction) — params: RaiseExceptions:RaiseExceptionsParameter, Id:WebServiceParameter [from connector: PaymentsApiSetup]
  - endpoint: `GET /v1/business-units/{Id}` — response: BusinessUnitRead
- **BusinessUnitUpdate** (WebServiceFunction) — params: RaiseExceptions:RaiseExceptionsParameter, Body:WebServiceParameter, Id:WebServiceParameter, LastChangedUser:WebServiceParameter [from connector: PaymentsApiSetup]
  - endpoint: `PUT /v1/business-units/{Id}` — body: BusinessUnitWrite, response: DefaultResponse
- **BusinessUnitDelete** (WebServiceFunction) — params: RaiseExceptions:RaiseExceptionsParameter, Id:WebServiceParameter, LastChangedUser:WebServiceParameter [from connector: PaymentsApiSetup]
  - endpoint: `DELETE /v1/business-units/{Id}` — response: DefaultResponse
- **BusinessUnitDepartmentGetListById** (WebServiceFunction) — params: RaiseExceptions:RaiseExceptionsParameter, BusinessUnitId:WebServiceParameter [from connector: PaymentsApiSetup]
  - endpoint: `GET /v1/business-unit-departments` — response: BusinessUnitDepartmentReadList
- **CostCentreGetList** (WebServiceFunction) — params: RaiseExceptions:RaiseExceptionsParameter [from connector: PaymentsApiSetup]
  - endpoint: `GET /v1/cost-centres` — response: CostCentreReadList
- **CostCentreCreate** (WebServiceFunction) — params: RaiseExceptions:RaiseExceptionsParameter, Body:WebServiceParameter, LastChangedUser:WebServiceParameter [from connector: PaymentsApiSetup]
  - endpoint: `POST /v1/cost-centres` — body: CostCentreWrite, response: DefaultResponse
- **CostCentreGetById** (WebServiceFunction) — params: RaiseExceptions:RaiseExceptionsParameter, Id:WebServiceParameter [from connector: PaymentsApiSetup]
  - endpoint: `GET /v1/cost-centres/{Id}` — response: CostCentreRead
- **CostCentreUpdate** (WebServiceFunction) — params: RaiseExceptions:RaiseExceptionsParameter, Body:WebServiceParameter, Id:WebServiceParameter, LastChangedUser:WebServiceParameter [from connector: PaymentsApiSetup]
  - endpoint: `PUT /v1/cost-centres/{Id}` — body: CostCentreWrite, response: DefaultResponse
- **CostCentreDelete** (WebServiceFunction) — params: RaiseExceptions:RaiseExceptionsParameter, Id:WebServiceParameter, LastChangedUser:WebServiceParameter [from connector: PaymentsApiSetup]
  - endpoint: `DELETE /v1/cost-centres/{Id}` — response: DefaultResponse
- **BankGetList** (WebServiceFunction) — params: RaiseExceptions:RaiseExceptionsParameter [from connector: PaymentsApiSetup]
  - endpoint: `GET /v1/banks` — response: BankReadList
- **BankCreate** (WebServiceFunction) — params: RaiseExceptions:RaiseExceptionsParameter, Body:WebServiceParameter, LastChangedUser:WebServiceParameter [from connector: PaymentsApiSetup]
  - endpoint: `POST /v1/banks` — body: BankWrite, response: DefaultResponse
- **BankGetById** (WebServiceFunction) — params: RaiseExceptions:RaiseExceptionsParameter, Id:WebServiceParameter [from connector: PaymentsApiSetup]
  - endpoint: `GET /v1/banks/{Id}` — response: BankRead
- **BankUpdate** (WebServiceFunction) — params: RaiseExceptions:RaiseExceptionsParameter, Body:WebServiceParameter, Id:WebServiceParameter, LastChangedUser:WebServiceParameter [from connector: PaymentsApiSetup]
  - endpoint: `PUT /v1/banks/{Id}` — body: BankWrite, response: DefaultResponse
- **BankDelete** (WebServiceFunction) — params: RaiseExceptions:RaiseExceptionsParameter, Id:WebServiceParameter, LastChangedUser:WebServiceParameter [from connector: PaymentsApiSetup]
  - endpoint: `DELETE /v1/banks/{Id}` — response: DefaultResponse
- **BankAccountTypeGetList** (WebServiceFunction) — params: RaiseExceptions:RaiseExceptionsParameter [from connector: PaymentsApiSetup]
  - endpoint: `GET /v1/bank-account-types` — response: BankAccountTypeReadList
- **BankAccountGetList** (WebServiceFunction) — params: RaiseExceptions:RaiseExceptionsParameter [from connector: PaymentsApiSetup]
  - endpoint: `GET /v1/bank-accounts` — response: BankAccountReadList
- **BankAccountCreate** (WebServiceFunction) — params: RaiseExceptions:RaiseExceptionsParameter, Body:WebServiceParameter, LastChangedUser:WebServiceParameter [from connector: PaymentsApiSetup]
  - endpoint: `POST /v1/bank-accounts` — body: BankAccountWrite, response: DefaultResponse
- **BankAccountGetById** (WebServiceFunction) — params: RaiseExceptions:RaiseExceptionsParameter, Id:WebServiceParameter [from connector: PaymentsApiSetup]
  - endpoint: `GET /v1/bank-accounts/{Id}` — response: BankAccountRead
- **BankAccountUpdate** (WebServiceFunction) — params: RaiseExceptions:RaiseExceptionsParameter, Body:WebServiceParameter, Id:WebServiceParameter, LastChangedUser:WebServiceParameter [from connector: PaymentsApiSetup]
  - endpoint: `PUT /v1/bank-accounts/{Id}` — body: BankAccountWrite, response: DefaultResponse
- **BankAccountDelete** (WebServiceFunction) — params: RaiseExceptions:RaiseExceptionsParameter, Id:WebServiceParameter, LastChangedUser:WebServiceParameter [from connector: PaymentsApiSetup]
  - endpoint: `DELETE /v1/bank-accounts/{Id}` — response: DefaultResponse
- **BankPaymentSetupGetList** (WebServiceFunction) — params: RaiseExceptions:RaiseExceptionsParameter [from connector: PaymentsApiSetup]
  - endpoint: `GET /v1/bank-payment-setups` — response: BankPaymentSetupReadList
- **BankPaymentSetupCreate** (WebServiceFunction) — params: RaiseExceptions:RaiseExceptionsParameter, Body:WebServiceParameter, LastChangedUser:WebServiceParameter [from connector: PaymentsApiSetup]
  - endpoint: `POST /v1/bank-payment-setups` — body: BankPaymentSetupWrite, response: DefaultResponse
- **BankPaymentSetupGetById** (WebServiceFunction) — params: RaiseExceptions:RaiseExceptionsParameter, Id:WebServiceParameter [from connector: PaymentsApiSetup]
  - endpoint: `GET /v1/bank-payment-setups/{Id}` — response: BankPaymentSetupRead
- **BankPaymentSetupUpdate** (WebServiceFunction) — params: RaiseExceptions:RaiseExceptionsParameter, Body:WebServiceParameter, Id:WebServiceParameter, LastChangedUser:WebServiceParameter [from connector: PaymentsApiSetup]
  - endpoint: `PUT /v1/bank-payment-setups/{Id}` — body: BankPaymentSetupWrite, response: DefaultResponse
- **BankPaymentSetupDelete** (WebServiceFunction) — params: RaiseExceptions:RaiseExceptionsParameter, Id:WebServiceParameter, LastChangedUser:WebServiceParameter [from connector: PaymentsApiSetup]
  - endpoint: `DELETE /v1/bank-payment-setups/{Id}` — response: DefaultResponse
- **BankPaymentMethodGetList** (WebServiceFunction) — params: RaiseExceptions:RaiseExceptionsParameter [from connector: PaymentsApiSetup]
  - endpoint: `GET /v1/bank-payment-methods` — response: BankPaymentMethodReadList
- **LookupDataGetList** (WebServiceFunction) — params: RaiseExceptions:RaiseExceptionsParameter, LookupId:WebServiceParameter [from connector: PaymentsApiSetup]
  - endpoint: `GET /v1/lookup-datas/{LookupId}` — response: LookupDataReadList
- **DepartmentGetList** (WebServiceFunction) — params: RaiseExceptions:RaiseExceptionsParameter [from connector: PaymentsApiSetup]
  - endpoint: `GET /v1/departments` — response: DepartmentReadList
- **DepartmentCreate** (WebServiceFunction) — params: RaiseExceptions:RaiseExceptionsParameter, Body:WebServiceParameter, LastChangedUser:WebServiceParameter [from connector: PaymentsApiSetup]
  - endpoint: `POST /v1/departments` — body: DepartmentWrite, response: DefaultResponse
- **DepartmentGetById** (WebServiceFunction) — params: RaiseExceptions:RaiseExceptionsParameter, Id:WebServiceParameter [from connector: PaymentsApiSetup]
  - endpoint: `GET /v1/departments/{Id}` — response: DepartmentRead
- **DepartmentUpdate** (WebServiceFunction) — params: RaiseExceptions:RaiseExceptionsParameter, Body:WebServiceParameter, Id:WebServiceParameter, LastChangedUser:WebServiceParameter [from connector: PaymentsApiSetup]
  - endpoint: `PUT /v1/departments/{Id}` — body: DepartmentWrite, response: DefaultResponse
- **DepartmentDelete** (WebServiceFunction) — params: RaiseExceptions:RaiseExceptionsParameter, Id:WebServiceParameter, LastChangedUser:WebServiceParameter [from connector: PaymentsApiSetup]
  - endpoint: `DELETE /v1/departments/{Id}` — response: DefaultResponse

### PaymentsApiPaymentTransactions — REST / HTTP  ·  ⚠ mock / non-prod host `[AI-SUGGESTED]`
- Connection (redacted): `{"URL": "http://localhost:10010/PaymentsApp/", "Auth": "ApiKey", "KeyLocation": "Header", "KeyName": "X-API-Key", "KeyValue": "Test123", "Timeout": 90}` [from administration.db / design model]
- **TransactionGetList** (WebServiceFunction) — params: RaiseExceptions:RaiseExceptionsParameter [from connector: PaymentsApiPaymentTransactions]
  - endpoint: `GET /v1/transactions` — response: TransactionReadList
- **TransactionCreate** (WebServiceFunction) — params: RaiseExceptions:RaiseExceptionsParameter, Body:WebServiceParameter, LastChangedUser:WebServiceParameter [from connector: PaymentsApiPaymentTransactions]
  - endpoint: `POST /v1/transactions` — body: TransactionWrite, response: DefaultResponse
- **TransactionGetById** (WebServiceFunction) — params: RaiseExceptions:RaiseExceptionsParameter, Id:WebServiceParameter [from connector: PaymentsApiPaymentTransactions]
  - endpoint: `GET /v1/transactions/{Id}` — response: TransactionRead
- **TransactionUpdate** (WebServiceFunction) — params: RaiseExceptions:RaiseExceptionsParameter, Body:WebServiceParameter, Id:WebServiceParameter, LastChangedUser:WebServiceParameter [from connector: PaymentsApiPaymentTransactions]
  - endpoint: `PUT /v1/transactions/{Id}` — body: TransactionWrite, response: DefaultResponse
- **TransactionDelete** (WebServiceFunction) — params: RaiseExceptions:RaiseExceptionsParameter, Id:WebServiceParameter, LastChangedUser:WebServiceParameter [from connector: PaymentsApiPaymentTransactions]
  - endpoint: `DELETE /v1/transactions/{Id}` — response: DefaultResponse
- **TransactionSupportingDocumentGetList** (WebServiceFunction) — params: RaiseExceptions:RaiseExceptionsParameter, TransactionId:WebServiceParameter [from connector: PaymentsApiPaymentTransactions]
  - endpoint: `GET /v1/transaction-supporting-documents` — response: TransactionSupportingDocumentReadList
- **TransactionSupportingDocumentCreate** (WebServiceFunction) — params: RaiseExceptions:RaiseExceptionsParameter, Body:WebServiceParameter, LastChangedUser:WebServiceParameter [from connector: PaymentsApiPaymentTransactions]
  - endpoint: `POST /v1/transaction-supporting-documents` — body: TransactionSupportingDocumentWrite, response: DefaultResponse
- **TransactionSupportingDocumentDelete** (WebServiceFunction) — params: RaiseExceptions:RaiseExceptionsParameter, Id:WebServiceParameter, LastChangedUser:WebServiceParameter [from connector: PaymentsApiPaymentTransactions]
  - endpoint: `DELETE /v1/transaction-supporting-documents/{Id}` — response: DefaultResponse
- **TransactionNoteGetList** (WebServiceFunction) — params: RaiseExceptions:RaiseExceptionsParameter, TransactionId:WebServiceParameter [from connector: PaymentsApiPaymentTransactions]
  - endpoint: `GET /v1/transaction-notes` — response: TransactionNoteReadList
- **TransactionNoteCreate** (WebServiceFunction) — params: RaiseExceptions:RaiseExceptionsParameter, Body:WebServiceParameter, LastChangedUser:WebServiceParameter [from connector: PaymentsApiPaymentTransactions]
  - endpoint: `POST /v1/transaction-notes` — body: TransactionNoteWrite, response: DefaultResponse
- **TransactionNoteUpdate** (WebServiceFunction) — params: RaiseExceptions:RaiseExceptionsParameter, Body:WebServiceParameter, Id:WebServiceParameter, LastChangedUser:WebServiceParameter [from connector: PaymentsApiPaymentTransactions]
  - endpoint: `PUT /v1/transaction-notes/{Id}` — body: TransactionNoteWrite, response: DefaultResponse
- **TransactionNoteDelete** (WebServiceFunction) — params: RaiseExceptions:RaiseExceptionsParameter, Id:WebServiceParameter, LastChangedUser:WebServiceParameter [from connector: PaymentsApiPaymentTransactions]
  - endpoint: `DELETE /v1/transaction-notes/{Id}` — response: DefaultResponse
- **PaymentDetailAuditLogGetList** (WebServiceFunction) — params: RaiseExceptions:RaiseExceptionsParameter [from connector: PaymentsApiPaymentTransactions]
  - endpoint: `GET /v1/payment-detail-audit-logs` — response: PaymentDetailAuditLogReadList
- **PaymentReasonGetList** (WebServiceFunction) — params: RaiseExceptions:RaiseExceptionsParameter [from connector: PaymentsApiPaymentTransactions]
  - endpoint: `GET /v1/payment-reasons` — response: PaymentReasonReadList
- **PaymentReasonCreate** (WebServiceFunction) — params: RaiseExceptions:RaiseExceptionsParameter, Body:WebServiceParameter, LastChangedUser:WebServiceParameter [from connector: PaymentsApiPaymentTransactions]
  - endpoint: `POST /v1/payment-reasons` — body: PaymentReasonWrite, response: DefaultResponse
- **PaymentReasonGetById** (WebServiceFunction) — params: RaiseExceptions:RaiseExceptionsParameter, Id:WebServiceParameter [from connector: PaymentsApiPaymentTransactions]
  - endpoint: `GET /v1/payment-reasons/{Id}` — response: PaymentReasonRead
- **PaymentReasonUpdate** (WebServiceFunction) — params: RaiseExceptions:RaiseExceptionsParameter, Body:WebServiceParameter, Id:WebServiceParameter, LastChangedUser:WebServiceParameter [from connector: PaymentsApiPaymentTransactions]
  - endpoint: `PUT /v1/payment-reasons/{Id}` — body: PaymentReasonWrite, response: DefaultResponse
- **PaymentReasonDelete** (WebServiceFunction) — params: RaiseExceptions:RaiseExceptionsParameter, Id:WebServiceParameter, LastChangedUser:WebServiceParameter [from connector: PaymentsApiPaymentTransactions]
  - endpoint: `DELETE /v1/payment-reasons/{Id}` — response: DefaultResponse
- **PaymentSetupGetList** (WebServiceFunction) — params: RaiseExceptions:RaiseExceptionsParameter [from connector: PaymentsApiPaymentTransactions]
  - endpoint: `GET /v1/payment-setups` — response: PaymentSetupReadList
- **PaymentSetupCreate** (WebServiceFunction) — params: RaiseExceptions:RaiseExceptionsParameter, Body:WebServiceParameter, LastChangedUser:WebServiceParameter [from connector: PaymentsApiPaymentTransactions]
  - endpoint: `POST /v1/payment-setups` — body: PaymentSetupWrite, response: DefaultResponse
- **PaymentSetupGetById** (WebServiceFunction) — params: RaiseExceptions:RaiseExceptionsParameter, Id:WebServiceParameter [from connector: PaymentsApiPaymentTransactions]
  - endpoint: `GET /v1/payment-setups/{Id}` — response: PaymentSetupRead
- **PaymentSetupUpdate** (WebServiceFunction) — params: RaiseExceptions:RaiseExceptionsParameter, Body:WebServiceParameter, Id:WebServiceParameter, LastChangedUser:WebServiceParameter [from connector: PaymentsApiPaymentTransactions]
  - endpoint: `PUT /v1/payment-setups/{Id}` — body: PaymentSetupWrite, response: DefaultResponse
- **PaymentSetupDelete** (WebServiceFunction) — params: RaiseExceptions:RaiseExceptionsParameter, Id:WebServiceParameter, LastChangedUser:WebServiceParameter [from connector: PaymentsApiPaymentTransactions]
  - endpoint: `DELETE /v1/payment-setups/{Id}` — response: DefaultResponse
- **PaymentSetupTransactionCodingGetList** (WebServiceFunction) — params: RaiseExceptions:RaiseExceptionsParameter, BusinessUnitId:WebServiceParameter, BusinessUnitDepartmentId:WebServiceParameter, TransactionTypeId:WebServiceParameter, BankAccountId:WebServiceParameter, BankPaymentMethodId:WebServiceParameter, PaymentReasonId:WebServiceParameter [from connector: PaymentsApiPaymentTransactions]
  - endpoint: `GET /v1/payment-setups/transaction-codings` — response: PaymentSetupReadList
- **TransactionTypeGetList** (WebServiceFunction) — params: RaiseExceptions:RaiseExceptionsParameter [from connector: PaymentsApiPaymentTransactions]
  - endpoint: `GET /v1/transaction-types` — response: TransactionTypeReadList
- **DuplicateTransactionGetList** (WebServiceFunction) — params: RaiseExceptions:RaiseExceptionsParameter, Id:WebServiceParameter [from connector: PaymentsApiPaymentTransactions]
  - endpoint: `GET /v1/transactions-duplicate/{Id}` — response: TransactionReadList
- **DraftTransactionGetList** (WebServiceFunction) — params: RaiseExceptions:RaiseExceptionsParameter [from connector: PaymentsApiPaymentTransactions]
  - endpoint: `GET /v1/transaction-drafts` — response: TransactionReadList

### PaymentsApiUsers — REST / HTTP  ·  ⚠ mock / non-prod host `[AI-SUGGESTED]`
- Connection (redacted): `{"URL": "http://localhost:10008/PaymentsApp/", "Auth": "ApiKey", "KeyLocation": "Header", "KeyName": "X-API-Key", "KeyValue": "Test123", "Timeout": 90}` [from administration.db / design model]
- **UserGetList** (WebServiceFunction) — params: RaiseExceptions:RaiseExceptionsParameter [from connector: PaymentsApiUsers]
  - endpoint: `GET /v1/users` — response: UserReadList
- **UserCreate** (WebServiceFunction) — params: RaiseExceptions:RaiseExceptionsParameter, Body:WebServiceParameter, LastChangedUser:WebServiceParameter [from connector: PaymentsApiUsers]
  - endpoint: `POST /v1/users` — body: UserWrite, response: DefaultResponse
- **UserGetById** (WebServiceFunction) — params: RaiseExceptions:RaiseExceptionsParameter, Id:WebServiceParameter [from connector: PaymentsApiUsers]
  - endpoint: `GET /v1/users/{Id}` — response: UserRead
- **UserUpdate** (WebServiceFunction) — params: RaiseExceptions:RaiseExceptionsParameter, Body:WebServiceParameter, Id:WebServiceParameter, LastChangedUser:WebServiceParameter [from connector: PaymentsApiUsers]
  - endpoint: `PUT /v1/users/{Id}` — body: UserWrite, response: DefaultResponse
- **UserDelete** (WebServiceFunction) — params: RaiseExceptions:RaiseExceptionsParameter, Id:WebServiceParameter, LastChangedUser:WebServiceParameter [from connector: PaymentsApiUsers]
  - endpoint: `DELETE /v1/users/{Id}` — response: DefaultResponse
- **RoleGetList** (WebServiceFunction) — params: RaiseExceptions:RaiseExceptionsParameter [from connector: PaymentsApiUsers]
  - endpoint: `GET /v1/roles` — response: RoleReadList
- **RoleSync** (WebServiceFunction) — params: RaiseExceptions:RaiseExceptionsParameter, Body:WebServiceParameter [from connector: PaymentsApiUsers]
  - endpoint: `POST /v1/roles/sync` — response: DefaultResponse

### PaymentsApiPaymentApprovals — REST / HTTP  ·  ⚠ mock / non-prod host `[AI-SUGGESTED]`
- Connection (redacted): `{"URL": "http://localhost:10011/PaymentsApp/", "Auth": "ApiKey", "KeyLocation": "Header", "KeyName": "X-API-Key", "KeyValue": "Test123", "Timeout": 90}` [from administration.db / design model]
- **DistinctApprovalLevelGetList** (WebServiceFunction) — params: RaiseExceptions:RaiseExceptionsParameter [from connector: PaymentsApiPaymentApprovals]
  - endpoint: `GET /v1/approval-levels` — response: ApprovalLevelReadList
- **ApprovalLevelCreate** (WebServiceFunction) — params: RaiseExceptions:RaiseExceptionsParameter, Body:WebServiceParameter, LastChangedUser:WebServiceParameter [from connector: PaymentsApiPaymentApprovals]
  - endpoint: `POST /v1/approval-levels/` — body: ApprovalLevelWrite, response: DefaultResponse
- **ApprovalLevelUpdate** (WebServiceFunction) — params: RaiseExceptions:RaiseExceptionsParameter, Body:WebServiceParameter, LastChangedUser:WebServiceParameter [from connector: PaymentsApiPaymentApprovals]
  - endpoint: `PUT /v1/approval-levels/` — body: ApprovalLevelWrite, response: DefaultResponse
- **ApprovalLevelDelete** (WebServiceFunction) — params: RaiseExceptions:RaiseExceptionsParameter, LastChangedUser:WebServiceParameter, BusinessUnitId:WebServiceParameter, DepartmentId:WebServiceParameter, TransactionTypeId:WebServiceParameter [from connector: PaymentsApiPaymentApprovals]
  - endpoint: `DELETE /v1/approval-levels/{BusinessUnitId},{DepartmentId},{TransactionTypeId}` — response: DefaultResponse
- **ApprovalLevelAmountGetList** (WebServiceFunction) — params: RaiseExceptions:RaiseExceptionsParameter, BusinessUnitId:WebServiceParameter, DepartmentId:WebServiceParameter, TransactionTypeId:WebServiceParameter [from connector: PaymentsApiPaymentApprovals]
  - endpoint: `GET /v1/approval-levels/{BusinessUnitId},{DepartmentId},{TransactionTypeId}` — response: ApprovalLevelAmountReadList
- **ApprovalLevelAmountDelete** (WebServiceFunction) — params: RaiseExceptions:RaiseExceptionsParameter, Id:WebServiceParameter, LastChangedUser:WebServiceParameter [from connector: PaymentsApiPaymentApprovals]
  - endpoint: `DELETE /v1/approval-levels/{Id}` — response: DefaultResponse
- **UserApprovalLevelAmountGetList** (WebServiceFunction) — params: RaiseExceptions:RaiseExceptionsParameter, BusinessUnitId:WebServiceParameter, DepartmentId:WebServiceParameter, TransactionTypeId:WebServiceParameter [from connector: PaymentsApiPaymentApprovals]
  - endpoint: `GET /v1/user-approval-levels/{BusinessUnitId},{DepartmentId},{TransactionTypeId}` — response: UserApprovalLevelAmountReadList
- **UserApprovalLevelCreate** (WebServiceFunction) — params: RaiseExceptions:RaiseExceptionsParameter, Body:WebServiceParameter, LastChangedUser:WebServiceParameter [from connector: PaymentsApiPaymentApprovals]
  - endpoint: `POST /v1/user-approval-levels` — body: UserApprovalLevelWrite, response: DefaultResponse
- **UserApprovalLevelDelete** (WebServiceFunction) — params: RaiseExceptions:RaiseExceptionsParameter, ApprovalLevelId:WebServiceParameter, UserId:WebServiceParameter, LastChangedUser:WebServiceParameter [from connector: PaymentsApiPaymentApprovals]
  - endpoint: `DELETE /v1/user-approval-levels/{ApprovalLevelId},{UserId}` — response: DefaultResponse
- **UserApprovalLevelGetListByBusinessUnitIdUserId** (WebServiceFunction) — params: RaiseExceptions:RaiseExceptionsParameter, BusinessUnitId:WebServiceParameter, UserId:WebServiceParameter [from connector: PaymentsApiPaymentApprovals]
  - endpoint: `GET /v1/user-approval-levels/{BusinessUnitId},{UserId}` — response: ApprovalLevelReadList
- **UserApprovalLevelGetListByUserId** (WebServiceFunction) — params: RaiseExceptions:RaiseExceptionsParameter, UserId:WebServiceParameter [from connector: PaymentsApiPaymentApprovals]
  - endpoint: `GET /v1/user-approval-levels/{UserId}` — response: UserApprovalLevelReadList
- **ApprovalLevelRuleGetList** (WebServiceFunction) — params: RaiseExceptions:RaiseExceptionsParameter, BusinessUnitId:WebServiceParameter, DepartmentId:WebServiceParameter, TransactionTypeId:WebServiceParameter [from connector: PaymentsApiPaymentApprovals]
  - endpoint: `GET /v1/approval-level-rules/{BusinessUnitId},{DepartmentId},{TransactionTypeId}` — response: ApprovalLevelRuleReadList
- **ApprovalLevelRulesUpdate** (WebServiceFunction) — params: RaiseExceptions:RaiseExceptionsParameter, Body:WebServiceParameter, LastChangedUser:WebServiceParameter [from connector: PaymentsApiPaymentApprovals]
  - endpoint: `PUT /v1/approval-level-rules` — body: ApprovalLevelRuleRead, response: DefaultResponse

## Tier-A — app settings / integration

- Filesystem path referenced: `C:\DigiataRepos\DigiataApps\PaymentApp\Tests\` [from design model: Setting]

## Tier-A — technology stack (NFR baseline)

- Backend framework: **net8.0-windows** [from .csproj]
- Frontend: **Vue ^3.5.22** [from package.json]
- Data providers: `Microsoft.Data.SqlClient`, `Microsoft.EntityFrameworkCore.Sqlite`, `Oracle.ManagedDataAccess.Core`, `System.Data.Odbc` [from .csproj]
- Notable backend capabilities: `EPPlus`, `IdentityModel.AspNetCore.OAuth2Introspection`, `Microsoft.AspNetCore.SignalR.Protocols.NewtonsoftJson`, `Serilog.AspNetCore`, `Serilog.Sinks.EventLog` [from .csproj]
