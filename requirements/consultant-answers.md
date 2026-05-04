# Consultant Answers — AugmentRisk Payments Workflow POC

**Generated:** 2026-05-04
**Source draft:** `requirements/requirements-draft.md`
**Source manifest:** `framework/state/resolver-manifest.json`
**Run summary:** 16 blocking items (5 confirmed individually, 11 accepted via `accept-all-remaining-blocking`); 49 non-blocking items (all accepted via `accept-all-remaining-non-blocking`).

---

### AI-001
- **Source location:** §1 Business goal
- **Original suggestion:** Validate the proposed workflow design with the client by walking the prototype through scripted demo scenarios that exercise each control (CFO threshold, dual auth, anomaly flag, escalation, CoP failure paths), and produce a clickable prototype the client can use to converge on the production specification.
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Validate the proposed workflow design with the client by walking the prototype through scripted demo scenarios that exercise each control (CFO threshold, dual auth, anomaly flag, escalation, CoP failure paths), and produce a clickable prototype the client can use to converge on the production specification.

### AI-002
- **Source location:** §3 Super User · Expertise level
- **Original suggestion:** High — comfortable across every screen and configuration setting
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** High — comfortable across every screen and configuration setting

### AI-003
- **Source location:** §3 Super User · Stakes
- **Original suggestion:** Demo integrity: ability to drive any scenario from a single login; mid stakes — the Super User exists to support demos rather than represent a real production role.
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Demo integrity: ability to drive any scenario from a single login; mid stakes — the Super User exists to support demos rather than represent a real production role.

### AI-004
- **Source location:** §3 Super User · Frequency of use
- **Original suggestion:** Daily during the POC build/demo phase.
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Daily during the POC build/demo phase.

### AI-005
- **Source location:** §3 Super User · Driving forces — wants
- **Original suggestion:** Single-login access to every screen and action; ability to walk a demo without re-authenticating.
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Single-login access to every screen and action; ability to walk a demo without re-authenticating.

### AI-006
- **Source location:** §3 Super User · Driving forces — fears
- **Original suggestion:** Being unable to exercise a control mid-demo because of a missing permission.
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Being unable to exercise a control mid-demo because of a missing permission.

### AI-007
- **Source location:** §3 Payments Initiator · Expertise level
- **Original suggestion:** Mid — familiar with payment forms, beneficiaries, ERP exports; not deeply familiar with bank protocols.
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Mid — familiar with payment forms, beneficiaries, ERP exports; not deeply familiar with bank protocols.

### AI-008
- **Source location:** §3 Payments Initiator · Stakes
- **Original suggestion:** High — a mistyped account number or sort code routes funds to the wrong recipient.
- **Initial classification:** blocking
- **Revised classification:** unchanged
- **Status:** confirmed
- **Consultant answer:** confirm
- **Follow-ups:** none
- **Resolved value:** High — a mistyped account number or sort code routes funds to the wrong recipient.

### AI-009
- **Source location:** §3 Payments Initiator · Frequency of use
- **Original suggestion:** Multiple times a day; primary screen for this user.
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Multiple times a day; primary screen for this user.

### AI-010
- **Source location:** §3 Payments Initiator · Driving forces — wants
- **Original suggestion:** Fast, low-friction capture; clear validation feedback before submit; clear status of what they have submitted.
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Fast, low-friction capture; clear validation feedback before submit; clear status of what they have submitted.

### AI-011
- **Source location:** §3 Payments Initiator · Driving forces — fears
- **Original suggestion:** Submitting a duplicate; entering wrong beneficiary details that pass validation but route incorrectly.
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Submitting a duplicate; entering wrong beneficiary details that pass validation but route incorrectly.

### AI-012
- **Source location:** §3 Approver 1 · Expertise level
- **Original suggestion:** Mid-high — understands the duplicate, verification, and out-of-range signals on a payment.
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Mid-high — understands the duplicate, verification, and out-of-range signals on a payment.

### AI-013
- **Source location:** §3 Approver 1 · Stakes
- **Original suggestion:** High — wrongful approval results in funds leaving the business; controls compliance posture.
- **Initial classification:** blocking
- **Revised classification:** unchanged
- **Status:** confirmed
- **Consultant answer:** confirm
- **Follow-ups:** none
- **Resolved value:** High — wrongful approval results in funds leaving the business; controls compliance posture.

### AI-014
- **Source location:** §3 Approver 1 · Frequency of use
- **Original suggestion:** Several times a day in batches.
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Several times a day in batches.

### AI-015
- **Source location:** §3 Approver 1 · Driving forces — wants
- **Original suggestion:** At-a-glance visibility of out-of-range and duplicate flags; bulk approve where safe.
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** At-a-glance visibility of out-of-range and duplicate flags; bulk approve where safe.

### AI-016
- **Source location:** §3 Approver 1 · Driving forces — fears
- **Original suggestion:** Approving a payment that breaches the CFO threshold or that has a failing verification.
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Approving a payment that breaches the CFO threshold or that has a failing verification.

### AI-017
- **Source location:** §3 Approver 2 · Expertise level
- **Original suggestion:** Mid-high — sees only payments escalated past SLA.
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Mid-high — sees only payments escalated past SLA.

### AI-018
- **Source location:** §3 Approver 2 · Stakes
- **Original suggestion:** High — same as Approver 1 with the additional pressure of overdue items.
- **Initial classification:** blocking
- **Revised classification:** unchanged
- **Status:** confirmed
- **Consultant answer:** confirm
- **Follow-ups:** none
- **Resolved value:** High — same as Approver 1 with the additional pressure of overdue items.

### AI-019
- **Source location:** §3 Approver 2 · Frequency of use
- **Original suggestion:** Daily during POC, sporadic outside SLA-breach windows.
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Daily during POC, sporadic outside SLA-breach windows.

### AI-020
- **Source location:** §3 Approver 2 · Driving forces — wants
- **Original suggestion:** Clear view of overdue items and how they got escalated.
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Clear view of overdue items and how they got escalated.

### AI-021
- **Source location:** §3 Approver 2 · Driving forces — fears
- **Original suggestion:** Missing a payment that has aged past secondary-approval SLA.
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Missing a payment that has aged past secondary-approval SLA.

### AI-022
- **Source location:** §3 CFO · Expertise level
- **Original suggestion:** High — domain expertise; uses the system selectively for high-value sign-off.
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** High — domain expertise; uses the system selectively for high-value sign-off.

### AI-023
- **Source location:** §3 CFO · Stakes
- **Original suggestion:** Very high — all payments above the CFO threshold (£500,000) and all anomalies (£1,000,000+) require their personal approval.
- **Initial classification:** blocking
- **Revised classification:** unchanged
- **Status:** confirmed
- **Consultant answer:** confirm
- **Follow-ups:** none
- **Resolved value:** Very high — all payments above the CFO threshold (£500,000) and all anomalies (£1,000,000+) require their personal approval.

### AI-024
- **Source location:** §3 CFO · Frequency of use
- **Original suggestion:** Daily but in short, focused sessions.
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Daily but in short, focused sessions.

### AI-025
- **Source location:** §3 CFO · Driving forces — wants
- **Original suggestion:** Filtered view of high-value items only; clear at-a-glance attestation that the verification, duplicate, and out-of-range checks have run.
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Filtered view of high-value items only; clear at-a-glance attestation that the verification, duplicate, and out-of-range checks have run.

### AI-026
- **Source location:** §3 CFO · Driving forces — fears
- **Original suggestion:** Approving a £1M+ payment without seeing the anomaly indicator; missing a foreign payment that needs dual auth.
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Approving a £1M+ payment without seeing the anomaly indicator; missing a foreign payment that needs dual auth.

### AI-027
- **Source location:** §3 Configurator · Expertise level
- **Original suggestion:** High — owns thresholds and toggles.
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** High — owns thresholds and toggles.

### AI-028
- **Source location:** §3 Configurator · Stakes
- **Original suggestion:** High — wrong threshold values misclassify CFO routing or anomaly flagging system-wide.
- **Initial classification:** blocking
- **Revised classification:** unchanged
- **Status:** confirmed
- **Consultant answer:** confirm
- **Follow-ups:** none
- **Resolved value:** High — wrong threshold values misclassify CFO routing or anomaly flagging system-wide.

### AI-029
- **Source location:** §3 Configurator · Frequency of use
- **Original suggestion:** Rarely — set-and-forget; revisit when policy changes.
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Rarely — set-and-forget; revisit when policy changes.

### AI-030
- **Source location:** §3 Configurator · Driving forces — wants
- **Original suggestion:** Clear units (currency vs minutes), validated input ranges, audit of who changed what.
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Clear units (currency vs minutes), validated input ranges, audit of who changed what.

### AI-031
- **Source location:** §3 Configurator · Driving forces — fears
- **Original suggestion:** Accidentally setting an SLA in the wrong unit (hours vs minutes) or dropping a threshold by an order of magnitude.
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Accidentally setting an SLA in the wrong unit (hours vs minutes) or dropping a threshold by an order of magnitude.

### AI-032
- **Source location:** §3 Release Officer · Expertise level
- **Original suggestion:** Mid — knows the bank-rail differences (Faster, BACS, CHAPS, SWIFT) at a working level.
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Mid — knows the bank-rail differences (Faster, BACS, CHAPS, SWIFT) at a working level.

### AI-033
- **Source location:** §3 Release Officer · Stakes
- **Original suggestion:** High — once released, a payment cannot be undone.
- **Initial classification:** blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-blocking
- **Follow-ups:** none
- **Resolved value:** High — once released, a payment cannot be undone.

### AI-034
- **Source location:** §3 Release Officer · Frequency of use
- **Original suggestion:** Several times a day in release windows.
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Several times a day in release windows.

### AI-035
- **Source location:** §3 Release Officer · Driving forces — wants
- **Original suggestion:** Confidence in the batch contents before transmission; single confirmation step; quick batch export for audit.
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Confidence in the batch contents before transmission; single confirmation step; quick batch export for audit.

### AI-036
- **Source location:** §3 Release Officer · Driving forces — fears
- **Original suggestion:** Releasing the wrong payment; missing a partial-match receipt during reconciliation.
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Releasing the wrong payment; missing a partial-match receipt during reconciliation.

### AI-037
- **Source location:** §4.1 G-01 quality signals
- **Original suggestion:** Time-to-submit; zero data-entry errors at submit; clear in-line validation feedback.
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Time-to-submit; zero data-entry errors at submit; clear in-line validation feedback.

### AI-038
- **Source location:** §4.1 G-02 quality signals
- **Original suggestion:** Visibility of inbound queue; one-click submit-to-workflow per row.
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Visibility of inbound queue; one-click submit-to-workflow per row.

### AI-039
- **Source location:** §4.1 G-03 quality signals
- **Original suggestion:** Verification result visible before activation; duplicate prevention.
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Verification result visible before activation; duplicate prevention.

### AI-040
- **Source location:** §4.1 G-04 quality signals
- **Original suggestion:** Bulk action efficiency; visibility of out-of-range / duplicate / verification flags; SLA awareness.
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Bulk action efficiency; visibility of out-of-range / duplicate / verification flags; SLA awareness.

### AI-041
- **Source location:** §4.1 G-05 quality signals
- **Original suggestion:** Pre-release confirmation; post-release attestation showing batch contents.
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Pre-release confirmation; post-release attestation showing batch contents.

### AI-042
- **Source location:** §4.1 G-06 quality signals
- **Original suggestion:** Match status visibility (Settled / Partial / Unmatched); one-screen view.
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Match status visibility (Settled / Partial / Unmatched); one-screen view.

### AI-043
- **Source location:** §4.1 G-07 quality signals
- **Original suggestion:** Single-screen authoritative source; clear units; change auditability.
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Single-screen authoritative source; clear units; change auditability.

### AI-044
- **Source location:** §4.1 G-08 quality signals
- **Original suggestion:** Filterable history; CSV/PDF download.
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Filterable history; CSV/PDF download.

### AI-045
- **Source location:** §4.1 G-09 quality signals
- **Original suggestion:** At-a-glance KPIs; period filter affects all widgets; click-through to detail screens.
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** At-a-glance KPIs; period filter affects all widgets; click-through to detail screens.

### AI-046
- **Source location:** §4.1 G-10 quality signals
- **Original suggestion:** One-click reset; predictable post-reset data set.
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** One-click reset; predictable post-reset data set.

### AI-047
- **Source location:** §4.1 G-11 quality signals
- **Original suggestion:** Clear "overdue" filter and visual indicator.
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Clear "overdue" filter and visual indicator.

### AI-048
- **Source location:** §4.1 G-12 quality signals
- **Original suggestion:** Confirmation modal that names the amount and beneficiary.
- **Initial classification:** blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-blocking
- **Follow-ups:** none
- **Resolved value:** Confirmation modal that names the amount and beneficiary.

### AI-049
- **Source location:** §4.2 Super User story · Objective
- **Original suggestion:** Surface a navigation menu where every screen is reachable in one click.
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Surface a navigation menu where every screen is reachable in one click.

### AI-050
- **Source location:** §5 Configure thresholds · Decision points DP-1
- **Original suggestion:** Numeric inputs validated against min/max bands.
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Numeric inputs validated against min/max bands.

### AI-051
- **Source location:** §5 Audit batch download · Role-conditional behaviour
- **Original suggestion:** Any persona with audit-read may download; default include Release Officer + CFO + Configurator + Super User.
- **Initial classification:** blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-blocking
- **Follow-ups:** none
- **Resolved value:** Any persona with audit-read may download; default include Release Officer + CFO + Configurator + Super User.

### AI-052
- **Source location:** §5 Reset demo · Role-conditional behaviour
- **Original suggestion:** Super User only (and any persona with reset permission — POC limited to Super User).
- **Initial classification:** blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-blocking
- **Follow-ups:** none
- **Resolved value:** Super User only (and any persona with reset permission — POC limited to Super User).

### AI-053
- **Source location:** §6.4 UF-13 mobile breakpoint scope
- **Original suggestion:** Mobile breakpoint table-to-card collapse per [STANDARD-RULE: GR-18] (below 768 px). Note: dashboard and approval queues are desktop-primary; mobile is best-effort.
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Mobile breakpoint table-to-card collapse per [STANDARD-RULE: GR-18] (below 768 px). Note: dashboard and approval queues are desktop-primary; mobile is best-effort.

### AI-054
- **Source location:** §6.5 RBAC · Release Officer · Reset demo cell
- **Original suggestion:** X (Release Officer may execute Reset demo).
- **Initial classification:** blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-blocking
- **Follow-ups:** none
- **Resolved value:** X (Release Officer may execute Reset demo).

### AI-055
- **Source location:** §6.5 RBAC · matrix-wide cell-level inferences
- **Original suggestion:** Cell-level inferences across the matrix not directly stated in inputs (Approver tiers' read access to Beneficiaries; Release Officer's update right on Bank Receipts; CFO's broad read across operational entities) — re-confirm the matrix as a whole.
- **Initial classification:** blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-blocking
- **Follow-ups:** none
- **Resolved value:** Cell-level inferences across the matrix not directly stated in inputs (Approver tiers' read access to Beneficiaries; Release Officer's update right on Bank Receipts; CFO's broad read across operational entities) are accepted as drafted.

### AI-056
- **Source location:** §6.6.4 C-02 PCI-DSS scope
- **Original suggestion:** Prototype handles no real PAN data; payment instrument fields are bank account numbers (UK Sort/Account, IBAN/SWIFT) and not card primary account numbers.
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Prototype handles no real PAN data; payment instrument fields are bank account numbers (UK Sort/Account, IBAN/SWIFT) and not card primary account numbers.

### AI-057
- **Source location:** §6.6.4 C-03 UK FCA segregation of duties
- **Original suggestion:** UK FCA-aligned segregation of duties: distinct Initiator / Approver / Release Officer roles; CFO sign-off above £500k; dual-auth on Foreign — already encoded in §6.2 BR-01 / BR-03.
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** UK FCA-aligned segregation of duties: distinct Initiator / Approver / Release Officer roles; CFO sign-off above £500k; dual-auth on Foreign — already encoded in §6.2 BR-01 / BR-03.

### AI-058
- **Source location:** §6.6.4 C-04 GDPR / UK-GDPR PII redaction
- **Original suggestion:** GDPR / UK-GDPR: Beneficiary contact email and personal-name data is stored. PII redaction on screen / consent banner — visual manifestation: redact PII columns for personas without read on Beneficiary.
- **Initial classification:** blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-blocking
- **Follow-ups:** none
- **Resolved value:** GDPR / UK-GDPR: Beneficiary contact email and personal-name data is stored. PII redaction on screen / consent banner — visual manifestation: redact PII columns for personas without read on Beneficiary.

### AI-059
- **Source location:** §6.6.5 A-01 WCAG target
- **Original suggestion:** WCAG 2.2 AA target across all screens (colour-pairing per UF-04, keyboard nav, focus management per GR-07, aria labelling per GR-17).
- **Initial classification:** blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-blocking
- **Follow-ups:** none
- **Resolved value:** WCAG 2.2 AA target across all screens (colour-pairing per UF-04, keyboard nav, focus management per GR-07, aria labelling per GR-17).

### AI-060
- **Source location:** §6.6.5 A-02 assistive-tech scope
- **Original suggestion:** Screen readers (NVDA, JAWS, VoiceOver), keyboard-only operation, high-contrast mode.
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Screen readers (NVDA, JAWS, VoiceOver), keyboard-only operation, high-contrast mode.

### AI-061
- **Source location:** §7 Payment · PaymentDate validation
- **Original suggestion:** DD/MM/YYYY; not in past beyond business days
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** DD/MM/YYYY; not in past beyond business days

### AI-062
- **Source location:** §7 Payment · ReasonCode enum values
- **Original suggestion:** ReasonCode { Supplier invoice, Refund, Payroll, Adhoc }
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** ReasonCode { Supplier invoice, Refund, Payroll, Adhoc }

### AI-063
- **Source location:** §10 Volumes · Data volume
- **Original suggestion:** ~10²–10³ active beneficiaries; ~10³–10⁴ payments per quarter; receipts ≈ 1× payments.
- **Initial classification:** blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-blocking
- **Follow-ups:** none
- **Resolved value:** ~10²–10³ active beneficiaries; ~10³–10⁴ payments per quarter; receipts ≈ 1× payments.

### AI-064
- **Source location:** §10 Volumes · Frequency
- **Original suggestion:** ~10–10² payments captured per business day during demo; ERP feed simulated at 1–10 payments per batch.
- **Initial classification:** blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-blocking
- **Follow-ups:** none
- **Resolved value:** ~10–10² payments captured per business day during demo; ERP feed simulated at 1–10 payments per batch.

### AI-065
- **Source location:** §10 Volumes · Concurrency
- **Original suggestion:** 5–10 concurrent users during demo windows; production assumption ~50–100 concurrent users for medium UK enterprise treasury.
- **Initial classification:** blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-blocking
- **Follow-ups:** none
- **Resolved value:** 5–10 concurrent users during demo windows; production assumption ~50–100 concurrent users for medium UK enterprise treasury.
