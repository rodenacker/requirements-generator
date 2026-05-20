# Prototype Brief: Transaction Import & Approval System

## 1. Objective

Design a prototype for a dual-role system that enables:

- Importers to upload and review transaction files
- Approvers to review, approve/reject, and export transactions

The prototype must reflect:

- File-driven ingestion (via File Logs)
- Transaction lifecycle states
- Role-based interaction constraints

---

## 2. Core Domain Model (from API)

The system revolves around three primary objects:

### 1. File Log

Represents an uploaded file and its processing state Key attributes:

- `Id`
- `FileName`
- `RecordCount`
- `CurrentStatus`
- `ProcessDate`
- `HasBulkErrorFile`

### 2. Transaction

Represents individual records extracted from a file Key attributes:

- `Id`
- `FileLogId`
- `Reference`
- `TransactionDate`
- `AccountNumber`
- `Amount`
- `Currency`
- `Status` (Imported / Approved / Rejected)
- `UserNote`

### 3. User

Authenticated via:

- `POST /v1/users/login`

---

## 3. Key System Relationships

- One **File Log → many Transactions**
- Transactions inherit context from FileLog (file name, source)
- Actions on transactions affect **status only**, not structure

---

## 4. Roles & Permissions

### Importer

- Upload files
- View transactions
- Search/filter
- View file summaries
- ❌ Cannot approve/reject

### Approver

- View transactions
- Search/filter
- Approve/reject
- Export data
- View file summaries
- ❌ Cannot upload

---

## 5. Key User Flows

---

### 5.1 Authentication

**Endpoint**

- `POST /v1/users/login`

**Flow**

1. User enters email + password
2. On success → route to role-specific landing
3. On failure → error state

---

### 5.2 File Upload (Importer only)

**Endpoint**

- `POST /v1/files/upload`

**Flow**

1. Select file
2. Provide:
    - FileSettingId
    - FileSettingName
    - FileName

3. Upload
4. System creates FileLog
5. Status shown in UI

**Prototype screens**

- Upload panel (drag & drop)
- Upload progress state
- Success / failure feedback

---

### 5.3 File Log Overview (Shared)

**Endpoint**

- `GET /v1/file-logs`

**Purpose** Anchor object for the system

**UI Requirements**

- Table of uploaded files
- Columns:
    - File Name
    - Process Date
    - Record Count
    - Status

- Row click → drill into transactions

---

### 5.4 Transaction Table (Core Screen)

**Endpoint**

- `GET /v1/transactions`

**This is the primary working surface.**

**UI Requirements**

- Data table with:
    - Reference
    - Date
    - Account
    - Amount
    - Currency
    - Status

- Row-level actions (Approver only):
    - Approve
    - Reject

- Bulk selection (optional but high value)

---

### 5.5 Search & Filtering

**Applied to**

- Transactions table
- File logs

**Filters**

- Status (Imported / Approved / Rejected)
- File (FileLogId)
- Date range
- Amount range
- Text search (Reference, Account)

---

### 5.6 Approve Transaction

**Endpoint**

- `POST /v1/transactions/approve`

**Flow**

1. Select transaction
2. Click approve
3. Confirm action
4. Status updates to Approved

---

### 5.7 Reject Transaction

**Endpoint**

- `POST /v1/transactions/reject`

**Flow**

1. Select transaction
2. Click reject
3. Enter **mandatory note**
4. Submit
5. Status updates to Rejected

---

### 5.8 Export Transactions (Approver)

**Endpoint**

- Uses filtered dataset (no explicit endpoint provided → simulate)

**UI Requirements**

- Export button
- Applies current filters
- Formats:
    - CSV (default)

---

### 5.9 File Summary View

**Derived from FileLog + Transactions**

**UI Requirements**

- Total records
- Count by status:
    - Imported
    - Approved
    - Rejected

- Error indicator (HasBulkErrorFile)

---

## 6. Critical States (Do NOT skip this)

This is where most prototypes fail.

### Transaction States

- Imported
- Approved
- Rejected

### File States (inferred)

- Uploaded
- Processing
- Completed
- Failed

### UI Implications

- Disable approve/reject if not “Imported”
- Show counts per state
- Reflect status changes instantly

---

## 7. Information Architecture

**Top-level navigation**

- Dashboard (File Logs)
- Transactions
- Upload (Importer only)

---

## 8. Key Screens to Prototype

1. Login
2. File Log List (Dashboard)
3. File Upload (Importer)
4. Transaction Table (Shared core)
5. Transaction Detail / Action modal
6. File Summary view
7. Export interaction

---

## 9. Regulatory & Data Scope (Prototype)

This section addresses two blocking findings from the inputs-side adversarial review (ADV-55 POPIA-scope, ADV-56 PCI-DSS-scope) by enumerating the prototype's regulatory boundary in-corpus.

### 9.1 PCI-DSS — does NOT apply

- `AccountNumber` in this prototype is a **bank account number** (South African retail-banking format, e.g. `1001-2034-5567`).
- It is **not** a payment-card Primary Account Number (PAN). The system processes EFT-style ledger transactions, not card transactions.
- PCI-DSS is therefore **out of scope** for this prototype: no card data is stored, transmitted, or processed; no tokenisation, encryption-at-rest of cardholder data, or PCI-scoped audit logging is required.
- If the system is later extended to handle card transactions, PCI-DSS scope must be re-evaluated and this section re-issued.

### 9.2 POPIA — applies in a narrowed prototype mode

POPIA (Protection of Personal Information Act 4 of 2013) applies because the system processes personal information of natural persons. The prototype operates under the **narrowed scope** below.

**9.2.1 Personal Information inventory (the only PI fields stored).**

| Field | Source schema | Lawful processing basis |
|---|---|---|
| `Email`, `FirstName`, `LastName` | `UserInfoRead`, `UserRead`, `UserWrite` | Contract — required to operate the user's account |
| `AccountNumber` | `TransactionRead` | Contract — required to display the user's own transactions |
| `Description` (transaction narrative) | `TransactionRead`, CSV column | Contract — required to identify the transaction in the approval workflow |
| `UserNote` (reject reasons; may contain PI written by the approver) | `TransactionRead`, `TransactionRejectWrite` | Contract — required to record the approval decision |
| `LastChangedUser` (audit-trail name) | All write-endpoint headers + read schemas | Legal obligation — financial-records audit trail |

No other PI is collected. The prototype does **not** store: ID numbers, addresses, phone numbers, dates of birth, biometric data, or special personal information per POPIA s26.

**9.2.2 Prototype data mode.**

- The prototype is operated with **synthetic / illustrative data only** (e.g. the sample `transactions_2026-04-15.csv` is fabricated for demo purposes; account number `1001-2034-5567` is illustrative, not a real account).
- No real client PI is loaded into the prototype.
- This places the prototype outside the operational POPIA enforcement perimeter for the duration of the prototype phase; production POPIA controls are deferred to the application-phase requirements.

**9.2.3 Retention (applies even on synthetic data so the prototype rehearses production behaviour).**

- `FileLog`, `Transaction`, `UserNote`: retained for **7 years** from creation (aligned with the SA Income Tax Act and FICA financial-record retention obligations).
- `User` records (Email, FirstName, LastName): retained while the account is active; deleted within 30 days of account closure.
- Session cookies: cleared on logout; idle timeout 15 minutes; absolute timeout 8 hours.
- Audit-trail rows (`LastChangedUser`, `LastChangedDate`): append-only, retained with the parent record's 7-year window.

**9.2.4 Consent flow.**

- Prototype-phase only: login screen displays a one-line acknowledgement *"This is a prototype; do not enter real personal or financial information."* Acceptance is implicit on login.
- Production consent (POPIA s11 conditions for lawful processing) is **out of scope for the prototype** and will be designed in the application-phase requirements.

**9.2.5 Data-subject rights.**

- POPIA s23–s25 rights (access, correction, deletion) are **out of scope for the prototype**: no real PI is held, so no data-subject can be a subject.
- The application phase will design: a user-facing "Download my data" affordance, a "Delete my account" affordance bound to the 30-day retention rule, and a complaints route to the Information Regulator.

**9.2.6 Cross-border transfer.**

- The prototype is hosted in South Africa (localhost in development); no cross-border transfer occurs.
- Cross-border posture (POPIA s72) is **out of scope for the prototype**.

### 9.3 Other South African financial-services regulation

- **FICA** (Financial Intelligence Centre Act): in scope for retention only (7-year rule applied in 9.2.3); KYC / customer-due-diligence flows are **out of scope for the prototype** (no client onboarding is performed by this system).
- **FAIS** (Financial Advisory and Intermediary Services Act): does not apply — this system records transactions, it does not give advice.
- **NCA** (National Credit Act): does not apply — this system does not extend credit.

### 9.4 Out of scope (prototype phase)

Explicitly out of scope for this prototype so downstream `/requirements` does not infer otherwise:

- SSO, OIDC, external identity providers (already named out-of-scope in `auth-api.yaml`).
- Multi-currency: prototype is ZAR-only. Currency is displayed but not converted.
- Card transactions / PCI scope (per 9.1).
- Real PI loading (per 9.2.2).
- POPIA data-subject-rights UI, consent UX, complaints route (per 9.2.5).
- Notifications (email / in-app / push) for status changes.
- Multi-source ingestion (SFTP / scheduled / API-pull) — browser upload only.
- Process-automation engine UI (`/v1/process-definitions` is read-only and not surfaced in the prototype).
- Admin UI for `/v1/users`, `/v1/roles`, `/v1/pages` CRUD — admin operations performed out-of-band for the prototype.
- Dual-control / escalation / delegation approval flows — single-step approve/reject only.
- Bulk approve / bulk reject / bulk export — only single-row actions in the prototype.
- Mobile / tablet device targets — desktop evergreen browser only.
- Accessibility conformance claim — prototype-tier visual accessibility only; WCAG 2.1 AA is an application-phase target.

---
