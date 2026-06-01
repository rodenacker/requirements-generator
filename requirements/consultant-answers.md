# Consultant Answers — Northstar Wealth Client Onboarding & KYC Wizard

Resolved entries for every `[AI-SUGGESTED]` marker in `requirements/requirements-draft.md`. One blocking item (AI-010) resolved individually in Phase 1; the 15 non-blocking items accepted in bulk via `accept-all-remaining-non-blocking` in Phase 2.

---

### AI-001
- **Source location:** §1.5 Deferred bucket
- **Original suggestion:** Joint-account and multi-applicant onboarding; advisor-side review and approval surfaces
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Joint-account and multi-applicant onboarding; advisor-side review and approval surfaces

### AI-002
- **Source location:** §1.7 row [Client-side state management] recommendation
- **Original suggestion:** Client-side state management (driving F-01/F-05/F-31)
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Client-side state management (driving F-01/F-05/F-31); no specific recommendation

### AI-003
- **Source location:** §1.7 row [Offline cache / local persistence] recommendation
- **Original suggestion:** Offline cache / local persistence (driving F-05/F-30/F-31)
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Offline cache / local persistence (driving F-05/F-30/F-31); no specific recommendation

### AI-004
- **Source location:** §1.7 row [File upload / binary blob handling] recommendation
- **Original suggestion:** binary blob storage tier required
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** File upload / binary blob handling; binary blob storage tier required

### AI-005
- **Source location:** §1.7 row [Notification delivery surface] recommendation
- **Original suggestion:** in-app channel only
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Notification delivery surface; in-app channel only

### AI-006
- **Source location:** §2.5 row [In Progress → Submitted] visible effect
- **Original suggestion:** The success screen replaces the flow and a confirmation number is shown
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** The success screen replaces the flow and a confirmation number is shown

### AI-007
- **Source location:** §2.5 row [Submitted → Confirmed] visible effect
- **Original suggestion:** The confirmation number, follow-up message, and contact email are shown and local storage is cleared
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** The confirmation number, follow-up message, and contact email are shown and local storage is cleared

### AI-008
- **Source location:** §6.1 F-01 acceptance criteria
- **Original suggestion:** Given a started session, the client moves through exactly six ordered steps to a submission state
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Given a started session, the client moves through exactly six ordered steps to a submission state

### AI-009
- **Source location:** §6.4.5 edge state [no saved progress]
- **Original suggestion:** When no saved progress exists for a returning client, the flow starts fresh from the first step
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** When no saved progress exists for a returning client, the flow starts fresh from the first step

### AI-010
- **Source location:** §6.5 Access control (RBAC) — Delete access
- **Original suggestion:** Discarding an in-progress application and restarting (Delete access) is not specified by the brief
- **Initial classification:** blocking
- **Revised classification:** unchanged
- **Status:** corrected
- **Consultant answer:** Correct — add discard
- **Follow-ups:** Q: Should the discard-and-restart action be confirmation-gated? — A: Gate with a modal-confirmation naming the affected entity, destructive-styled primary action, default focus on Cancel. (apply-rule: GR-04)
- **Resolved value:** Grant the Prospective Client Delete access to their own in-progress Onboarding Session/Application via a discard-and-restart action, gated by a modal confirmation per GR-04.

### AI-011
- **Source location:** §6.6.2 Frontend performance budgets — Time to interactive (p95)
- **Original suggestion:** p95 <= 2.5 s on a desktop viewport
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Time to interactive p95 <= 2.5 s on a desktop viewport

### AI-012
- **Source location:** §6.6.2 Frontend performance budgets — Initial bundle size budget
- **Original suggestion:** <= 300 KB gzipped
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Initial bundle size budget <= 300 KB gzipped

### AI-013
- **Source location:** §6.6.5 Accessibility — target conformance
- **Original suggestion:** Target conformance: WCAG 2.2 AA
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Target conformance: WCAG 2.2 AA

### AI-014
- **Source location:** §10 Volumes — Data volume
- **Original suggestion:** One onboarding application per client; a handful of uploaded documents per application
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** One onboarding application per client; a handful of uploaded documents per application

### AI-015
- **Source location:** §10 Volumes — Frequency
- **Original suggestion:** Low; onboarding is a one-time event per client, occasionally resumed across sessions
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Low frequency; onboarding is a one-time event per client, occasionally resumed across sessions

### AI-016
- **Source location:** §10 Volumes — Concurrency
- **Original suggestion:** A single client per session; no shared or concurrent editing
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** A single client per session; no shared or concurrent editing
