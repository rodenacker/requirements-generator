# Review Resolutions — adversarial (review-requirements/ADVERSARIAL)

<!-- Consultant-approved input document produced by /resolve-review.
     Corpus material: the next source-manifest build ingests this file like any
     other input/ file (Native-text tier). Finding IDs below are per-run labels
     from the source review and reset whenever that review is re-run — the
     verbatim finding quotes are the durable anchors. Where a resolution changes
     a fact stated elsewhere in the corpus, its Supersedes line is authoritative:
     treat the superseded statement as replaced, not contradicted. -->

## Provenance

| Field | Value |
|---|---|
| Source review | `review-requirements/ADVERSARIAL/adversarial-review.html` |
| Source review sha256 | `a7606aa0f78a8ca809e413b1242228c64ca18f5fdbb22975d1cf172819cdd51c` |
| Review's source fingerprint | `a8c551059a6affd50c20f2d4de43d7bf4d21e5aea9d81e954c56a96d8f3de214` |
| Fingerprint target (`requirements/requirements.md`) at resolution time | `a8c551059a6affd50c20f2d4de43d7bf4d21e5aea9d81e954c56a96d8f3de214` |
| Source drift | none |
| Methodology | `adversarial` |
| Resolution date | 2026-06-13 |
| Findings resolved | ADV-01, ADV-02, ADV-03, ADV-04, ADV-05, ADV-06, ADV-07, ADV-08, ADV-09, ADV-10, ADV-11, ADV-12, ADV-13, ADV-14, ADV-15, ADV-16, ADV-17, ADV-18, ADV-19, ADV-20, ADV-21, ADV-22, ADV-23, ADV-24, ADV-25, ADV-26, ADV-27, ADV-28, ADV-29, ADV-30, ADV-31, ADV-32, ADV-33, ADV-34, ADV-35, ADV-36, ADV-37, ADV-38, ADV-39, ADV-40, ADV-41, ADV-42, ADV-43, ADV-44, ADV-45, ADV-46, ADV-47, ADV-48, ADV-49, ADV-50, ADV-51, ADV-52, ADV-53 |
| Findings skipped | (none) |

<!-- No addendum row: the Step-9b addendum outcome is decided after this document is
     finalised, and recording transient requirements.md state in a durable corpus file
     would mislead after the next re-merge removes the addendum. The pairing is recorded
     on the addendum side (its Run sub-block names this file). -->

**Origin markers:** `[CONSULTANT-STATED]` — the consultant supplied the resolution
content. `[AI-INFERRED, CONSULTANT-CONFIRMED]` — drafted from the review finding's
own actionable payload and individually confirmed by the consultant. Every
resolution below carries exactly one.

## Resolutions

### ADV-01 — §6.6.1 mandates step-up re-authentication for approve/reject, but no §6.1 functional requirement, §5 flow, or §6.4 UI feature need defines the step-up re-auth surface, so a stated security behaviour has no corresponding requirement.

**Finding (verbatim, from the review):**
> | Re-auth scope | Step-up auth required for approve-class actions (approve/reject) | inferred |

**Problem as stated by the review:** §6.6.1 mandates step-up re-authentication for approve/reject, but no §6.1 functional requirement, §5 flow, or §6.4 UI feature need defines the step-up re-auth surface, so a stated security behaviour has no corresponding requirement.

**Review's actionable payload:** Recommendation — "Either add a functional requirement plus UI feature need (re-auth prompt surface, error state) covering step-up auth on approve/reject, or remove the §6.6.1 re-auth row if it is out of MVP scope." · Disposition — Defer.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
Step-up re-authentication for approve/reject actions is out of scope for the MVP prototype. Approve and reject complete with no secondary authentication challenge; the §6.6.1 "step-up auth required for approve-class actions" entry is advisory application-build guidance only and drives no prototype flow, functional requirement, or UI surface.

**Supersedes:** This supersedes the statement in `requirements/requirements.md` regarding the §6.6.1 step-up re-auth scope row.

---

### ADV-02 — BR-08's acceptance criterion depends on an activity-name-to-status mapping that is never enumerated anywhere in the doc, so the rule has no pass/fail predicate and File Status cannot be derived.

**Finding (verbatim, from the review):**
> When a File Log is shown, the system shall display the Status mapped from LastExecutedActivityName per the activity-name-to-status mapping.

**Problem as stated by the review:** BR-08's acceptance criterion depends on an activity-name-to-status mapping that is never enumerated anywhere in the doc (§9 itself flags "mapping not enumerated in the corpus"), so the rule has no pass/fail predicate and File Status cannot be derived.

**Review's actionable payload:** Recommendation — "Enumerate the activity-name-to-status mapping (each LastExecutedActivityName value → File Status enum) in §2.3 or §7, or mark BR-08 as blocked pending the mapping rather than stating it as an enforceable rule." · Disposition — Defer.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
The activity-name-to-status mapping BR-08 depends on is a backend-owned derivation outside frontend scope. The frontend renders the File Status enum value exactly as supplied by the backend (per the §6.10 fixtures) and does not compute it from LastExecutedActivityName; BR-08 is a backend rule, not a frontend acceptance criterion.

**Supersedes:** This supersedes the statement in `requirements/requirements.md` regarding §6.2 BR-08 (File Status derivation as a frontend acceptance criterion).

---

### ADV-03 — F-12's AC begins "While a file summary is open" but no §5 task flow or §6.4 UI feature need defines how/where a user opens a file summary, so the entry point for the feature is missing.

**Finding (verbatim, from the review):**
> | F-12 | Should | Display a file summary of total records and count by status [SRC: C-043] | While a file summary is open, the system shall show total records and a count of transactions by status. | → §6.7 RPT-01 | Supports → §4.1 G-05 |

**Problem as stated by the review:** F-12's AC begins "While a file summary is open" but no §5 task flow or §6.4 UI feature need defines how/where a user opens a file summary, so the entry point for the feature is missing.

**Review's actionable payload:** Recommendation — "Add a §5 flow or a UI-NN feature need specifying the trigger and surface from which a file summary is opened (e.g. from a file-log row), and link F-12 to it." · Disposition — Patch.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
The application provides an explicit entry point for the file summary: from a row in the File Log list the user opens the summary for that file, which shows total records and a count of transactions by status (per F-12). F-12 is reached from the File Log list surface.

**Supersedes:** (supersedes nothing — net-new information)

---

### ADV-04 — Shape: Transaction defines Description, TransactionType, and UserNote as fields, but F-06 (and no other display requirement) names them, so three data-model properties have no documented read/display behaviour.

**Finding (verbatim, from the review):**
> While the transaction table is loaded, the system shall show reference, date, account, amount, currency, and status for each transaction.

**Problem as stated by the review:** Shape: Transaction defines Description, TransactionType, and UserNote as fields, but F-06 (and no other display requirement) names them, so three data-model properties have no documented read/display behaviour.

**Review's actionable payload:** Recommendation — "State explicitly where Description, TransactionType, and UserNote are surfaced (e.g. detail row, chip) or mark them as not displayed in §7, so every Transaction field has documented read coverage." · Disposition — Patch.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
The Transaction fields Description, TransactionType, and UserNote are surfaced in the per-transaction detail view, not in the main transaction table row. Every Transaction property thus has a defined read location: reference, date, account, amount, currency, and status in the table; Description, TransactionType, and UserNote in the detail view.

**Supersedes:** (supersedes nothing — net-new information)

---

### ADV-05 — G-04's search/filter is realized as F-07 (Must) and UI-03 (Must) but the Importer story that closes G-04 is priority "Should", leaving the goal's priority coverage internally inconsistent.

**Finding (verbatim, from the review):**
> | G-04 | Find specific transactions quickly via search and filter [SRC: C-042] | Target transactions located within a few filter actions | sub-level | | |

**Problem as stated by the review:** G-04's search/filter is realized as F-07 (Must) and UI-03 (Must) but the Importer story that closes G-04 is priority "Should", leaving the goal's priority coverage internally inconsistent.

**Review's actionable payload:** Recommendation — "Reconcile the priority: set the §4.2 Importer search/filter story to 'Must' to match F-07/UI-03, or downgrade F-07/UI-03, so the goal-to-requirement priority chain is consistent." · Disposition — Patch.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
The Importer search/filter user story in §4.2 is priority Must, matching its realizing requirements F-07 (Must) and UI-03 (Must). The goal-to-requirement priority chain for G-04 is consistent at Must.

**Supersedes:** This supersedes the statement in `requirements/requirements.md` regarding the §4.2 Importer search/filter story's "Should" priority.

---

### ADV-06 — The non-functional section covers session UX, performance, compliance, and accessibility but states no observability/error-telemetry requirement, so that NFR category is absent rather than implied.

**Finding (verbatim, from the review):**
> ## 6.6 Non-functional (FE-only)

**Problem as stated by the review:** The non-functional section covers session UX, performance, compliance, and accessibility but states no observability/error-telemetry requirement (e.g. client error logging or failure reporting), so that NFR category is absent rather than implied.

**Review's actionable payload:** Recommendation — "Add an explicit observability NFR (even if scoped as backend-only/app-build guidance) or record an explicit decision that client-side observability is out of scope for the prototype." · Disposition — Defer.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
Client-side observability and error telemetry are out of scope for the prototype. No client error-logging or failure-reporting requirement applies; any observability expectation is application-build guidance only.

**Supersedes:** (supersedes nothing — net-new information)

---

### ADV-07 — A File Log can reach the Failed state but the user-facing recovery flow is explicitly unspecified, leaving G-01 with no closed behaviour for the failure branch.

**Finding (verbatim, from the review):**
> | Processing → Failed | backend processing fails (out-of-FE-scope context) | processing encountered an error | File Status reflects Failed on the File Log list; recovery flow unspecified [SRC: C-069] |

**Problem as stated by the review:** A File Log can reach the Failed state but the user-facing recovery flow is explicitly unspecified, leaving G-01 ("track their processing") with no closed behaviour for the failure branch.

**Review's actionable payload:** Recommendation — "Either define the minimal Failed-file UI behaviour (e.g. surfaced error state and a no-op acknowledgement) or confirm in §1.5 Deferred that no Failed-state interaction ships in the MVP." · Disposition — Defer.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
A File Log in the Failed state surfaces a non-actionable error indication on the File Log list — a Failed status chip with an explanatory message — and no recovery interaction ships in the MVP. This closes the G-01 failure branch with a defined read-only behaviour.

**Supersedes:** (supersedes nothing — net-new information)

---

### ADV-08 — §6.10 lists eight consumed operations with fixture references but contracts no failure mode for any of them, so the integration surface's failure behaviour is uncontracted.

**Finding (verbatim, from the review):**
> > FE-facing only. Prototype sub-block (fixtures). Every operation maps to a §6.1 F-NN.

**Problem as stated by the review:** §6.10 lists eight consumed operations with fixture references but contracts no failure mode (error payload shape / FE error-state mapping) for any of them, so the integration surface's failure behaviour is uncontracted.

**Review's actionable payload:** Recommendation — "Add a failure-mode column to §6.10 (or cross-reference §6.4.5 error states per operation) so each consumed operation names its error/empty response and the FE state it drives." · Disposition — Defer.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
Each of the eight consumed operations in §6.10 must declare its failure mode: the error or empty response it can return and the §6.4.5 frontend state that response drives (an error state with retry for list loads; an inline error for mutations). The integration surface's failure behaviour is contracted rather than implicit.

**Supersedes:** (supersedes nothing — net-new information)

---

### ADV-09 — "about one second" is a vague time window — the hedge "about" makes the performance acceptance criterion unverifiable.

**Finding (verbatim, from the review):**
> the system shall set its status to Approved and reflect the change within about one second [SRC: C-040]

**Problem as stated by the review:** "about one second" is a vague time window (the hedge "about" makes the performance acceptance criterion unverifiable — is 1.4s a pass or fail?).

**Review's actionable payload:** Recommendation — "Replace 'within about one second' with a precise bound, e.g. 'the status chip reflects the change within 1 s (p95)', consistent with the §6.6.2 render budget." · Disposition — Patch.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
When a transaction is approved, the status chip must reflect the change within 1 second (p95) of confirmation, consistent with the §6.6.2 render budget. The vague "about one second" qualifier is replaced by this measurable bound.

**Supersedes:** This supersedes the statement in `requirements/requirements.md` regarding the §6.1 F-08 approve-reflect timing ("about one second").

---

### ADV-10 — "a few filter actions" is a vague quantifier, leaving the goal's success threshold undefined.

**Finding (verbatim, from the review):**
> Target transactions located within a few filter actions

**Problem as stated by the review:** "a few filter actions" is a vague quantifier, leaving the goal's success threshold undefined.

**Review's actionable payload:** Recommendation — "Quantify the signal, e.g. 'located within at most 3 filter applications', or restate as a qualitative-only signal that does not imply a measurable count." · Disposition — Patch.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
G-04's success signal is quantified: a target transaction can be located within at most 3 filter applications. The vague "a few filter actions" is replaced by this measurable threshold.

**Supersedes:** This supersedes the statement in `requirements/requirements.md` regarding G-04's success signal ("a few filter actions").

---

### ADV-11 — "last group of digits" is ambiguous because §7 states AccountNumber is "plain digits" with no delimiter, so a UI implementer cannot determine where a "group" begins.

**Finding (verbatim, from the review):**
> Where AccountNumber is displayed, the system shall mask all but the last group of digits [SRC: C-045]

**Problem as stated by the review:** "last group of digits" is ambiguous because §7 states AccountNumber is "plain digits" with no delimiter, so a UI implementer cannot determine where a "group" begins or how many digits it contains.

**Review's actionable payload:** Recommendation — "Define the group precisely, e.g. 'mask all but the last 4 digits', and reconcile with the §7 'plain digits' representation." · Disposition — Patch.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
Where AccountNumber is displayed, the system masks all but the last 4 digits. "Last group of digits" is defined as the final 4 digits, consistent with the §7 "plain digits" representation (no delimiter).

**Supersedes:** This supersedes the statement in `requirements/requirements.md` regarding §6.2 BR-07's AccountNumber mask rule.

---

### ADV-12 — The business rule references an "activity-name-to-status mapping" that is never enumerated, so a reader cannot determine which activity names yield which File status.

**Finding (verbatim, from the review):**
> the system shall display the Status mapped from LastExecutedActivityName per the activity-name-to-status mapping

**Problem as stated by the review:** The business rule references an "activity-name-to-status mapping" that is never enumerated, so a reader cannot determine which activity names yield Uploaded/Processing/Completed/Failed — §9 itself flags "mapping not enumerated in the corpus".

**Review's actionable payload:** Recommendation — "Enumerate the activity-name-to-status mapping in §2.3 File Log (or a §7 derivation row), or explicitly mark the mapping as a deferred backend-owned input the FE renders verbatim." · Disposition — Defer.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
The activity-name-to-status mapping is a backend-owned input. The frontend renders the File Status enum supplied by the backend verbatim and does not derive it; the mapping is not enumerated in the frontend spec because it is not a frontend concern.

**Supersedes:** This supersedes the statement in `requirements/requirements.md` regarding §6.2 BR-08 (treating the activity-name-to-status mapping as a frontend rule).

---

### ADV-13 — "a baseline accessibility standard" is vague — no named standard or level (e.g. WCAG 2.1 AA) is given, so the requirement is unverifiable.

**Finding (verbatim, from the review):**
> The application targets desktop browsers first and meets a baseline accessibility standard [SRC: C-046]

**Problem as stated by the review:** "a baseline accessibility standard" is vague — no named standard or level (e.g. WCAG 2.1 AA) is given, so the requirement is unverifiable.

**Review's actionable payload:** Recommendation — "Name the target standard and conformance level explicitly, e.g. 'meets WCAG 2.1 AA'." · Disposition — Patch.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
The application meets WCAG 2.1 AA. The vague "baseline accessibility standard" is replaced by this named, testable conformance target.

**Supersedes:** This supersedes the statement in `requirements/requirements.md` regarding §6.6.5's "baseline accessibility standard".

---

### ADV-14 — "render the authenticated user's welcome" uses an undefined noun ("welcome") with no acceptance criterion specifying what content or surface this is.

**Finding (verbatim, from the review):**
> the system shall verify session validity and render the authenticated user's welcome

**Problem as stated by the review:** "render the authenticated user's welcome" uses an undefined noun ("welcome") with no acceptance criterion specifying what content or surface this is.

**Review's actionable payload:** Recommendation — "Define the 'welcome' concretely, e.g. 'render the user's display name and role in the app header', with a testable acceptance criterion." · Disposition — Patch.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
F-16's "welcome" is defined as the authenticated user's display name and role rendered in the application header. On load, after verifying session validity, the system shows the user's name and role in the header.

**Supersedes:** This supersedes the statement in `requirements/requirements.md` regarding §6.1 F-16's undefined "welcome".

---

### ADV-15 — "the required file-setting details" is a vague noun phrase in the story objective; the reader must infer the closed set from F-03 rather than seeing it here.

**Finding (verbatim, from the review):**
> Objective | Select a file, supply the required file-setting details, and upload it [SRC: C-028]

**Problem as stated by the review:** "the required file-setting details" is a vague noun phrase in the story objective; the reader must infer the closed set (FileSettingId, FileSettingName, FileName) from F-03 rather than seeing it here.

**Review's actionable payload:** Recommendation — "Enumerate the required details inline (FileSettingId, FileSettingName, FileName) or add an explicit '→ §6.1 F-03' reference for the field list." · Disposition — Patch.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
The §4.2 Importer upload story names the required file-setting details explicitly: FileSettingId, FileSettingName, and FileName (the closed set defined by F-03). The vague phrase is replaced by this enumeration.

**Supersedes:** (supersedes nothing — net-new information)

---

### ADV-16 — The volume band "10²–10⁴" spans two orders of magnitude, making it a vague quantifier that cannot decisively drive the UI pattern selection §10 claims it governs.

**Finding (verbatim, from the review):**
> no corpus-stated overall cap, so a client-side band of 10²–10⁴ retained transactions is assumed

**Problem as stated by the review:** The volume band "10²–10⁴" spans two orders of magnitude, making it a vague quantifier that cannot decisively drive the UI pattern selection §10 claims it governs (pagination vs virtualization decisions differ across that range).

**Review's actionable payload:** Recommendation — "Narrow the assumed working-set to a single planning figure (e.g. 'assume ~1,000 retained transactions for pattern selection') and note the upper bound separately as a stress case." · Disposition — Defer.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
For UI pattern selection, the planning working-set is ~1,000 retained transactions; the 10⁴ figure is retained only as a separate stress-case ceiling. The two-orders-of-magnitude band is replaced for pattern-selection purposes by this single planning figure.

**Supersedes:** This supersedes the statement in `requirements/requirements.md` regarding §10's "10²–10⁴" retained-transaction band as the pattern-selection basis.

---

### ADV-17 — The qualifier "about one second" has no decidable pass/fail boundary, so a tester cannot determine whether a 1.3s reflection passes or fails.

**Finding (verbatim, from the review):**
> the system shall set its status to Approved and reflect the change within about one second [SRC: C-040]

**Problem as stated by the review:** The qualifier "about one second" has no decidable pass/fail boundary, so a tester cannot determine whether a 1.3s reflection passes or fails.

**Review's actionable payload:** Recommendation — "Replace 'about one second' with a precise predicate such as 'the new status appears within 1000 ms (p95) of confirmation'." · Disposition — Patch.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
When a transaction is approved, the new status must appear within 1000 ms (p95) of confirmation. The vague "about one second" qualifier is replaced by this decidable predicate.

**Supersedes:** This supersedes the statement in `requirements/requirements.md` regarding the §6.1 F-08 approve-reflect timing ("about one second").

---

### ADV-18 — BR-08 and Shape: FileLog.Status both depend on an activity-name-to-status mapping the doc admits is not enumerated, so a tester cannot decide which Status any LastExecutedActivityName must render.

**Finding (verbatim, from the review):**
> | File status | Derived from LastExecutedActivityName via an activity-name-to-status mapping [SRC: C-068] | mapping not enumerated in the corpus |

**Problem as stated by the review:** BR-08 and Shape: FileLog.Status both depend on an activity-name-to-status mapping that the doc itself admits is not enumerated, so a tester cannot decide which Status any given LastExecutedActivityName must render.

**Review's actionable payload:** Recommendation — "Enumerate the activity-name-to-status mapping table (each LastExecutedActivityName value → resulting Status) so BR-08's acceptance criterion becomes decidable from the doc alone." · Disposition — Defer.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
The activity-name-to-status mapping referenced in §9 is a backend-owned derivation; the frontend renders the backend-supplied File Status enum and does not decide Status from LastExecutedActivityName. Testability of the mapping is a backend concern, not a frontend acceptance criterion.

**Supersedes:** This supersedes the statement in `requirements/requirements.md` regarding §9's File-status derivation note (treating it as a frontend testability obligation).

---

### ADV-19 — "last group of digits" is undefined for a field stored as "plain digits" (§7) with no delimiter, so a tester cannot decide how many trailing digits must remain visible.

**Finding (verbatim, from the review):**
> Where AccountNumber is displayed, the system shall mask all but its last group of digits [SRC: C-045].

**Problem as stated by the review:** "last group of digits" is undefined for a field stored as "plain digits" (§7) with no delimiter, so a tester cannot decide how many trailing digits must remain visible.

**Review's actionable payload:** Recommendation — "Specify the exact mask predicate (e.g. 'display only the last 4 digits, mask all preceding digits') in F-13 and BR-07." · Disposition — Patch.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
Where AccountNumber is displayed, the system displays only the last 4 digits and masks all preceding digits. This mask predicate applies to F-13 and BR-07.

**Supersedes:** This supersedes the statement in `requirements/requirements.md` regarding §6.1 F-13's AccountNumber mask rule ("last group of digits").

---

### ADV-20 — "baseline accessibility standard" names no level or version, so a tester has no enumerated criteria to assert conformance against.

**Finding (verbatim, from the review):**
> The application targets desktop browsers first and meets a baseline accessibility standard [SRC: C-046].

**Problem as stated by the review:** "baseline accessibility standard" names no level or version, so a tester has no enumerated criteria to assert conformance against.

**Review's actionable payload:** Recommendation — "Name the concrete standard and level (e.g. 'WCAG 2.1 AA') so accessibility can be tested against an explicit checklist." · Disposition — Patch.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
The application meets WCAG 2.1 AA; accessibility conformance is asserted and tested against that named level and version.

**Supersedes:** This supersedes the statement in `requirements/requirements.md` regarding §6.6.5's "baseline accessibility standard".

---

### ADV-21 — "the authenticated user's welcome" specifies no concrete UI element or content, so a tester cannot decide what a passing render must contain.

**Finding (verbatim, from the review):**
> When the application loads, the system shall verify session validity and render the authenticated user's welcome.

**Problem as stated by the review:** "the authenticated user's welcome" specifies no concrete UI element or content, so a tester cannot decide what a passing render must contain.

**Review's actionable payload:** Recommendation — "Define the welcome's decidable content (e.g. 'render the user's FirstName and Role in the header')." · Disposition — Patch.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
F-16's welcome renders the user's FirstName and Role in the application header; a passing render contains both.

**Supersedes:** This supersedes the statement in `requirements/requirements.md` regarding §6.1 F-16's undefined "welcome".

---

### ADV-22 — "Skeleton matching the target" gives no decidable predicate for what the loading skeleton must show, so its presence cannot be objectively pass/fail tested.

**Finding (verbatim, from the review):**
> | → §6.1 F-06 | loading | Skeleton matching the target while transactions load | Wait for load to complete |

**Problem as stated by the review:** "Skeleton matching the target" gives no decidable predicate for what the loading skeleton must show (row count, column structure), so its presence cannot be objectively pass/fail tested.

**Review's actionable payload:** Recommendation — "Specify the skeleton's testable shape (e.g. 'render N placeholder rows mirroring the transaction table's column count')." · Disposition — Patch.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
The transaction-table loading skeleton renders placeholder rows mirroring the transaction table's column structure (one placeholder cell per column) over a fixed number of placeholder rows (e.g. 10). "Skeleton matching the target" is defined by this testable shape.

**Supersedes:** This supersedes the statement in `requirements/requirements.md` regarding §6.4.5's "Skeleton matching the target" loading predicate.

---

### ADV-23 — F-16 carries priority "Could" but §1.5 declares the seven key screens as the explicit MVP set with no scope note placing "Could" items in or out, so it straddles the MVP/post-MVP line.

**Finding (verbatim, from the review):**
> | F-16 | Could | Verify session validity and render a welcome on page load

**Problem as stated by the review:** F-16 carries priority "Could" but §1.5 declares the seven key screens as the explicit MVP set with no scope note placing "Could" items in or out of that MVP cut, so it straddles the MVP/post-MVP line.

**Review's actionable payload:** Recommendation — "Add an explicit scope tag to F-16 (e.g. a §1.5 row or a Rationale note) stating whether 'Could'-priority items are in-MVP or deferred." · Disposition — Patch.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
F-16 (priority Could) is included in the MVP prototype as a low-priority item, built after Must/Should items. The §1.5 seven-screen set is the in-scope boundary; Could-priority functional items within those screens are in-MVP unless §1.5 explicitly defers them.

**Supersedes:** (supersedes nothing — net-new information)

---

### ADV-24 — This MVP-scoping claim ("No MFA prompt in the MVP") sits inside an "Application-build guidance — not a prototype design input" block, blurring whether MFA-absence is a binding MVP decision or advisory.

**Finding (verbatim, from the review):**
> | MFA prompt scope | No MFA prompt in the MVP | inferred |

**Problem as stated by the review:** This MVP-scoping claim ("No MFA prompt in the MVP") sits inside a block headed "Application-build guidance — not a prototype design input," blurring whether MFA-absence is a binding MVP scope decision or merely advisory build guidance.

**Review's actionable payload:** Recommendation — "Move MVP in/out scope decisions about MFA into §1.5's In/Out/Deferred buckets and keep §6.6.1 to non-scoping budget values, or annotate the row to say the MVP framing is advisory only." · Disposition — Patch.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
MFA is out of scope for the MVP prototype as a binding scope decision (it belongs in the §1.5 scope buckets, not embedded as advisory §6.6.1 build guidance). The MVP issues no MFA prompt.

**Supersedes:** This supersedes the statement in `requirements/requirements.md` regarding §6.6.1's "No MFA prompt in the MVP" row (reclassifying it from inferred advisory guidance to a binding scope decision).

---

### ADV-25 — The scope note pins the MVP to "seven named key screens" but the In bucket enumerates eight feature items (not screens), so the unit and count of the MVP boundary are inconsistent.

**Finding (verbatim, from the review):**
> > §1.5 is in-scope-only. The brief's seven named key screens are the explicit in-scope MVP set; anything outside that set is out of scope by default [SRC: C-047].

**Problem as stated by the review:** The scope note pins the MVP to "seven named key screens" but the In bucket enumerates eight feature items (not screens), so the unit and count of the MVP boundary are inconsistent and the engineer cannot map features to the asserted seven-screen cut line.

**Review's actionable payload:** Recommendation — "Reconcile the In bucket with the seven-screen claim — either list the seven screens explicitly or restate the MVP boundary in terms of the In-bucket feature items." · Disposition — Patch.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
The §1.5 MVP boundary is expressed consistently in one unit — the seven named key screens. The eight In-bucket feature items are the capabilities delivered across those seven screens; the MVP cut line is the seven screens, not a separate feature count.

**Supersedes:** This supersedes the statement in `requirements/requirements.md` regarding §1.5's mixed screen/feature MVP boundary unit.

---

### ADV-26 — The single Deferred item is explicitly "unspecified," so it is not estimable, yet §2.5's File Log matrix still renders the Failed state inline, mixing undefined deferred work into the active state model.

**Finding (verbatim, from the review):**
> | Deferred | User-facing recovery flow for a Failed file (unspecified, treated as not-yet-defined) [SRC: C-069] |

**Problem as stated by the review:** The single Deferred item is explicitly "unspecified," so it is not estimable and provides no cut-line detail, yet §2.5's File Log matrix still renders the Failed state and notes "recovery flow unspecified" inline, mixing undefined deferred work into the active state model.

**Review's actionable payload:** Recommendation — "Either define a minimal placeholder behaviour for the Failed-file recovery flow or add a note in §2.5 explicitly marking the Failed terminal state as having no in-MVP recovery surface." · Disposition — Defer.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
The §1.5 Deferred Failed-file recovery flow has no in-MVP recovery surface; §2.5's Failed terminal state renders only a read-only Failed indication (per ADV-07) with no actionable recovery in the MVP, separating undefined deferred work from the active state model.

**Supersedes:** (supersedes nothing — net-new information)

---

### ADV-27 — The FileLog data shape derives the user-visible Status chip from a field LastExecutedActivityName that is never declared as a field on the FileLog shape (or any shape) in §7, so a frontend consumer cannot resolve the structure the status chip depends on.

**Finding (verbatim, from the review):**
> | Status | enum | yes | chip | derived from LastExecutedActivityName [SRC: C-068] |

**Problem as stated by the review:** The FileLog data shape derives the user-visible Status chip from a field LastExecutedActivityName that is never declared as a field on the FileLog shape (or any shape) in §7, so a frontend consumer cannot resolve the structure the status chip depends on.

**Review's actionable payload:** Recommendation — "Add LastExecutedActivityName as an explicit field (hidden, source) on the §7 Shape: FileLog so the derivation BR-08 references has a defined input." · Disposition — Patch.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
The §7 FileLog shape declares LastExecutedActivityName as an explicit hidden/source-only field (not displayed), giving the Status chip's derivation a defined input on the shape. The frontend still renders Status from the backend-supplied enum (per ADV-02) and does not compute it.

**Supersedes:** (supersedes nothing — net-new information)

---

### ADV-28 — The File Upload flow and F-03 require the form to capture FileSettingId and FileSettingName, but neither field appears on any §7 data shape, so the upload surface references structure the data model never defines.

**Finding (verbatim, from the review):**
> (Provide FileSettingId, FileSettingName, FileName; required details captured) [SRC: C-028]

**Problem as stated by the review:** The File Upload flow and F-03 require the form to capture FileSettingId and FileSettingName, but neither field appears on any §7 data shape, so the upload surface references structure the data model never defines.

**Review's actionable payload:** Recommendation — "Declare FileSettingId and FileSettingName as captured fields (on the FileLog shape or an upload-input shape) in §7 so the upload form's data-bound inputs have defined properties." · Disposition — Patch.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
The §7 data model declares FileSettingId, FileSettingName, and FileName as captured fields on an upload-input shape (the File Upload form's data-bound inputs), so the upload surface's fields have defined properties.

**Supersedes:** (supersedes nothing — net-new information)

---

### ADV-29 — The activity-name-to-status mapping that drives the File Log Status chip is referenced as load-bearing but is explicitly never enumerated, leaving the status-chip rendering rule undefined for a downstream consumer.

**Finding (verbatim, from the review):**
> | File status | Derived from LastExecutedActivityName via an activity-name-to-status mapping [SRC: C-068] | mapping not enumerated in the corpus |

**Problem as stated by the review:** The activity-name-to-status mapping that drives the File Log Status chip (BR-08, §2.3, §7) is referenced as load-bearing but is explicitly never enumerated anywhere in the doc, leaving the status-chip rendering rule undefined for a downstream consumer.

**Review's actionable payload:** Recommendation — "Enumerate the activity-name-to-status mapping (even as an [AI-SUGGESTED] provisional table) so the FE can deterministically render File Log status, or mark the mapping deferred with an explicit placeholder behaviour." · Disposition — Patch.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
The activity-name-to-status mapping that drives the File Log Status chip is a backend-owned derivation; the frontend deterministically renders the backend-supplied Status enum (per the §6.10 fixtures), and the mapping is not enumerated in the frontend spec. No frontend status-chip rule depends on the unenumerated mapping.

**Supersedes:** This supersedes the statement in `requirements/requirements.md` regarding §9's File-status derivation note (treating the mapping as a frontend rendering rule).

---

### ADV-30 — The goals catalogue never names the implicit dependency that G-02/G-03/G-04/G-05 require an authenticated, role-routed session and populated data, so the buildable order of goals is not discoverable from §4.1.

**Finding (verbatim, from the review):**
> | G-04 | Find specific transactions quickly via search and filter [SRC: C-042] | Target transactions located within a few filter actions | sub-level | | |

**Problem as stated by the review:** The goals catalogue never names the implicit dependency that G-02/G-03/G-04/G-05 all require an authenticated, role-routed session (F-01/F-02) and populated data (G-01), so the buildable order of goals is not discoverable from §4.1.

**Review's actionable payload:** Recommendation — "Add a dependency note to the goals catalogue (or to G-02..G-05) stating they presuppose authentication/role-routing and, for G-04/G-03, a loaded transaction set." · Disposition — Patch.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
The §4.1 goals catalogue records that G-02, G-03, G-04, and G-05 all presuppose an authenticated, role-routed session (F-01/F-02), and that G-03/G-04 additionally require a loaded transaction set (G-01). The buildable order of goals is thereby discoverable.

**Supersedes:** (supersedes nothing — net-new information)

---

### ADV-31 — F-11 operates on "the filtered grid" and depends on F-07 and F-06 existing, but no dependency note records that ordering, so an engineer could schedule export before the grid/filter capability.

**Finding (verbatim, from the review):**
> | F-11 | Must | Export the currently filtered transaction set to CSV, generated client-side [SRC: C-036] |

**Problem as stated by the review:** F-11 operates on "the filtered grid" and is thus dependent on F-07 (client-side filtering) and F-06 (transaction display) existing, but no dependency note records that ordering, so an engineer could schedule export before the grid/filter capability.

**Review's actionable payload:** Recommendation — "Add an explicit dependency note to F-11 (e.g. 'depends on F-06 display and F-07 filtering') so the export build order is discoverable." · Disposition — Patch.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
F-11 (CSV export of the filtered set) records an explicit dependency on F-06 (transaction display) and F-07 (client-side filtering); export is built after the grid and filter capability exist.

**Supersedes:** (supersedes nothing — net-new information)

---

### ADV-32 — The session-UX block inserts a step-up re-auth requirement gating approve/reject, but no task flow or functional requirement defines a step-up auth interaction, so the flows reference a re-auth concept the doc never models.

**Finding (verbatim, from the review):**
> | Re-auth scope | Step-up auth required for approve-class actions (approve/reject) | inferred |

**Problem as stated by the review:** The session-UX block inserts a step-up re-auth requirement gating approve/reject, but no task flow (§5 Approve/Reject) or functional requirement defines a step-up auth interaction, so the approve/reject flows reference a re-auth concept the rest of the doc never models.

**Review's actionable payload:** Recommendation — "Either add a step-up re-auth step/decision point to the Approve and Reject flows (and F-08/F-09) or scope-note this row as application-build-only with no prototype interaction, removing the dangling dependency." · Disposition — Patch.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
The §6.6.1 step-up re-auth row is application-build guidance only with no prototype interaction; the Approve and Reject flows model no step-up auth step, removing the dangling dependency (consistent with ADV-01, which scopes step-up re-auth out of the MVP).

**Supersedes:** This supersedes the statement in `requirements/requirements.md` regarding §6.6.1's step-up re-auth scope as a gate on the approve/reject flows.

---

### ADV-33 — The RBAC matrix grants the Importer Create access on File Log, but §5 Flow: File Upload states "the backend creates a File Log" and §2.3 says the FE does not drive these transitions, so the FE consumer gets contradictory authority over who creates File Logs.

**Finding (verbatim, from the review):**
> | Importer | C R [SRC: C-020] | R [SRC: C-070] | R [SRC: C-071] | — [SRC: C-006] | X [SRC: C-024] | X [SRC: C-020] | X [SRC: C-029] | X [SRC: C-070] | X [SRC: C-042] | — [SRC: C-021] | — [SRC: C-021] | — [SRC: C-005] |

**Problem as stated by the review:** The RBAC matrix grants the Importer Create (`C`) access on File Log, but §5 Flow: File Upload states "the backend creates a File Log" and §2.3 says the FE does not drive these transitions (backend-owned), so the FE consumer gets contradictory authority over who creates File Logs.

**Review's actionable payload:** Recommendation — "Change the Importer's File Log cell from `C R` to `R` (the FE only triggers an upload; the backend creates the File Log), or add a `†` note clarifying that `C` denotes upload-initiated backend creation rather than an FE create capability." · Disposition — Patch.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
The §6.5 RBAC Importer cell for File Log is Read-only (R): the frontend only triggers an upload; the backend creates the File Log. The Importer has no frontend create capability over File Logs, consistent with §2.3 (backend-owned transitions).

**Supersedes:** This supersedes the statement in `requirements/requirements.md` regarding the §6.5 RBAC Importer File Log access ("C R").

---

### ADV-34 — The class diagram models the generic User as actioning Transactions, but §2.2 restricts actioning to Approver and §6.5 RBAC gives the Importer no approve/reject, so the diagram contradicts the prose and the matrix.

**Finding (verbatim, from the review):**
> ```
> User "1" --> "*" Transaction : actions
> ```

**Problem as stated by the review:** The class diagram models the generic `User` as actioning Transactions, but §2.2 restricts actioning to `Approver actions Transaction` and §6.5 RBAC gives the Importer no approve/reject, so the diagram contradicts the prose relationship and the access-control matrix.

**Review's actionable payload:** Recommendation — "Relabel the diagram edge to originate from the Approver role (or annotate the association as Approver-only) so it matches §2.2 and the §6.5 RBAC cells." · Disposition — Patch.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
The §2.4 class-diagram association for actioning Transactions originates from the Approver role, not the generic User: only an Approver actions a Transaction, consistent with §2.2 and the §6.5 RBAC matrix (the Importer has no approve/reject).

**Supersedes:** This supersedes the statement in `requirements/requirements.md` regarding the §2.4 class-diagram "User actions Transaction" association.

---

### ADV-35 — §6.6.1 simultaneously asserts "Step-up auth required for approve-class actions" and "No MFA prompt in the MVP," leaving the two adjacent rows in tension about whether the MVP issues any secondary auth challenge.

**Finding (verbatim, from the review):**
> | Re-auth scope | Step-up auth required for approve-class actions (approve/reject) | inferred |
> | Account lockout messaging | Generic locked-account message after repeated failed logins | inferred |
> | MFA prompt scope | No MFA prompt in the MVP | inferred |

**Problem as stated by the review:** §6.6.1 simultaneously asserts "Step-up auth required for approve-class actions" and "No MFA prompt in the MVP," yet a step-up re-authentication challenge before approve/reject is itself an additional authentication prompt, leaving the two adjacent rows in tension about whether the MVP issues any secondary auth challenge.

**Review's actionable payload:** Recommendation — "Clarify §6.6.1 by either scoping step-up auth out of the MVP to match the no-MFA row, or distinguishing password/session step-up from MFA so the two rows are explicitly non-overlapping." · Disposition — Patch.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
The two §6.6.1 rows are reconciled by scoping step-up re-authentication out of the MVP (consistent with ADV-01/ADV-32): the MVP issues no secondary authentication challenge of any kind — neither MFA nor step-up re-auth.

**Supersedes:** This supersedes the statement in `requirements/requirements.md` regarding §6.6.1's step-up re-auth scope row (resolving its tension with the no-MFA row).

---

### ADV-36 — §7 marks Transaction.UserNote as Required = no, while §6.3 validation and §6.2 BR-03 make the note mandatory on reject, so a consumer reading the data shape sees an optional field that other sections treat as required in the reject path.

**Finding (verbatim, from the review):**
> | UserNote | string | no | detail | note captured on rejection [SRC: C-055] |

**Problem as stated by the review:** §7 marks Transaction.UserNote as Required = no, while §6.3 validation and §6.2 BR-03 make the note mandatory on reject, so a consumer reading the data shape sees an optional field that other sections treat as required in the reject path.

**Review's actionable payload:** Recommendation — "Amend the UserNote Notes cell to state it is conditionally required on reject (per §6.2 BR-03) so the shape-level optionality is qualified." · Disposition — Patch.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
The §7 Transaction.UserNote field is conditionally required: optional in general but mandatory when a transaction is rejected (per §6.3 validation and §6.2 BR-03). The shape-level "Required = no" is qualified by this reject-path condition.

**Supersedes:** This supersedes the statement in `requirements/requirements.md` regarding §7 Transaction.UserNote's unqualified "Required = no".

---

### ADV-37 — §6.6.2 sets a p95 ≤ 500 ms render budget while §10 assumes up to 10⁴ retained transactions filtered/exported client-side, a volume that may exceed the budget — the classic NFR-vs-data-volume conflict.

**Finding (verbatim, from the review):**
> | Render budget for largest list/table | p95 ≤ 500 ms for the transaction table | inferred |

**Problem as stated by the review:** §6.6.2 sets a p95 ≤ 500 ms render budget for the transaction table while §10 assumes a client-side band of up to 10⁴ retained transactions filtered/exported client-side, a volume that may exceed a 500 ms render budget and matches the classic NFR-vs-data-volume conflict.

**Review's actionable payload:** Recommendation — "Either lower the assumed upper volume band, or note that client-side pagination (UI-07) bounds the rendered row count so the 500 ms budget applies per page rather than to the full 10⁴-row set." · Disposition — Defer.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
The §6.6.2 p95 ≤ 500 ms render budget applies per rendered page, not to the full retained set: client-side pagination (UI-07) bounds the rows rendered at once, so the budget is met per page even as the retained set approaches the 10⁴ stress ceiling.

**Supersedes:** This supersedes the statement in `requirements/requirements.md` regarding §6.6.2's render budget scope (clarifying it applies per page).

---

### ADV-38 — The transaction-table list specifies a loading skeleton but no zero-items empty state for when the table genuinely contains no transactions (distinct from the filter-yields-zero 'partial' row).

**Finding (verbatim, from the review):**
> | → §6.1 F-06 | loading | Skeleton matching the target while transactions load | Wait for load to complete |

**Problem as stated by the review:** The transaction-table list specifies a loading skeleton but no zero-items empty state for the case where the table genuinely contains no transactions (distinct from the §6.4.5 filter-yields-zero 'partial' row, which presupposes a non-empty source list).

**Review's actionable payload:** Recommendation — "Add a §6.4.5 row for §6.1 F-06 / Flow: Transaction Table with condition 'empty' specifying an entity-specific empty state for when no transactions exist at all." · Disposition — Patch.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
The transaction table defines a zero-items empty state distinct from the filter-yields-zero state: when the table genuinely contains no transactions, an entity-specific empty state is shown (e.g. "No transactions yet") rather than a skeleton or a filtered-empty message.

**Supersedes:** (supersedes nothing — net-new information)

---

### ADV-39 — Every data-loading surface specifies only a loading skeleton with no error variant, so a failed list load has no defined UI state, leaving the frontend with no behaviour to render on fetch failure.

**Finding (verbatim, from the review):**
> | → §6.1 F-06 | loading | Skeleton matching the target while transactions load | Wait for load to complete |

**Problem as stated by the review:** Every data-loading surface specifies only a loading skeleton with no error variant, so a failed GET /v1/transactions (or file-logs) load has no defined UI state, leaving the frontend consumer with no behaviour to render on fetch failure.

**Review's actionable payload:** Recommendation — "Add a §6.4.5 'error' row for the list-load surfaces specifying a load-failure state with a retry affordance." · Disposition — Patch.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
Every data-loading surface (transaction list, file-log list) defines a load-error state: on a failed GET, the surface shows an error message with a retry affordance rather than an indefinite skeleton.

**Supersedes:** (supersedes nothing — net-new information)

---

### ADV-40 — The file-upload requirement names no maximum file size, no accepted file type/format, and no virus/content check — the canonical 'file upload with no max size, no failure mode' edge gap.

**Finding (verbatim, from the review):**
> | F-03 | Must | Allow an Importer to upload a transaction file with FileSettingId, FileSettingName, and FileName [SRC: C-028] | When an Importer submits a file with the required details, the system shall display upload progress and a success or failure result. | → §5 Flow: File Upload | Supports → §4.1 G-01 |

**Problem as stated by the review:** The file-upload requirement names no maximum file size, no accepted file type/format, and no virus/content check — the canonical 'file upload with no max size, no failure mode' edge gap.

**Review's actionable payload:** Recommendation — "Add a §6.3 validation row (or F-03 acceptance criterion) specifying max file size, accepted extensions/MIME, and the inline error shown when a file is too large or of the wrong type." · Disposition — Patch.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
The file-upload requirement (F-03) specifies validation: a maximum file size, an accepted file type/format (extension and MIME), and an inline error shown when a file exceeds the size limit or is of an unsupported type. Virus/content scanning is a backend concern outside the frontend scope.

**Supersedes:** (supersedes nothing — net-new information)

---

### ADV-41 — A maximum-size state is undefined: the assumed 10⁴ upper band has no specified behaviour when the client-side retained set approaches the band ceiling.

**Finding (verbatim, from the review):**
> | Data volume | ~20 transactions per imported file; no corpus-stated overall cap, so a client-side band of 10²–10⁴ retained transactions is assumed | inferred |

**Problem as stated by the review:** A maximum-size state is undefined: the assumed 10⁴ upper band has no specified behaviour (truncation notice, virtualization, or warning) when the client-side retained set approaches the band ceiling.

**Review's actionable payload:** Recommendation — "Specify the expected UI behaviour at the upper bound of the assumed band (e.g. a 'showing first N' notice or guaranteed virtualized rendering) so the frontend has a defined max-size posture." · Disposition — Defer.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
At the upper bound of the retained-transaction set, the UI guarantees virtualized rendering of the transaction table (only visible rows are rendered) so performance holds; no data is truncated. This defines the max-size posture left open by §10.

**Supersedes:** (supersedes nothing — net-new information)

---

### ADV-42 — The amount-range filter has a format-validation rule but the date-range filter has no validation behaviour specified for a malformed or inverted (start > end) date range.

**Finding (verbatim, from the review):**
> | Transaction.Amount | format | Amount must be a number | "Enter a valid amount." |

**Problem as stated by the review:** The amount-range filter has a format-validation rule but the date-range filter (named in F-07 / UI-03) has no validation behaviour specified for a malformed or inverted (start > end) date range.

**Review's actionable payload:** Recommendation — "Add a §6.3 validation row for the date-range filter covering malformed dates and start-after-end ranges, with an inline error message." · Disposition — Patch.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
The date-range filter (F-07/UI-03) has validation: a malformed date or an inverted range (start date after end date) shows an inline error, and the filter is not applied until corrected.

**Supersedes:** (supersedes nothing — net-new information)

---

### ADV-43 — Re-uploading the same file is not addressed — there is no duplicate-file detection or idempotency surface, so a double submission has undefined UI behaviour (PI-03 excludes idempotency enforcement).

**Finding (verbatim, from the review):**
> | Steps | (Select a file; file is staged for upload); (Provide FileSettingId, FileSettingName, FileName; required details captured) [SRC: C-028]; (Upload; the backend creates a File Log) [SRC: C-027]; (Upload result; success or failure feedback is shown) |

**Problem as stated by the review:** Re-uploading the same file is not addressed — there is no duplicate-file detection or idempotency surface, so an Importer who submits the same file twice has undefined UI behaviour (PI-03 explicitly excludes idempotency enforcement, leaving the gap unaddressed even at the UI layer).

**Review's actionable payload:** Recommendation — "Specify whether a duplicate upload is silently allowed (creating a second File Log) or surfaced with a 'file already uploaded' warning, so the frontend has a defined re-submission behaviour." · Disposition — Defer.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
Re-uploading the same file is allowed and creates a second File Log; before submission the frontend surfaces a non-blocking "this file may already have been uploaded" warning but does not prevent the upload (idempotency enforcement is out of scope per PI-03).

**Supersedes:** (supersedes nothing — net-new information)

---

### ADV-44 — A File Log reaching the Failed terminal state has no recovery path — explicitly deferred — so the only edge for a failed ingestion is a status chip with no actionable next step.

**Finding (verbatim, from the review):**
> | Deferred | User-facing recovery flow for a Failed file (unspecified, treated as not-yet-defined) [SRC: C-069] |

**Problem as stated by the review:** A File Log reaching the Failed terminal state (§2.5) has no recovery path — it is explicitly deferred — so the only edge for a failed ingestion is a status chip with no actionable next step for the Importer.

**Review's actionable payload:** Recommendation — "At minimum specify a placeholder Failed-state UI (e.g. a disabled/explanatory notice naming who to contact) so the Failed status is not a dead end pending the deferred recovery flow." · Disposition — Defer.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
A File Log in the Failed terminal state shows a read-only explanatory notice (the Failed status plus a message that no automated recovery is available, with guidance to contact support); no recovery action ships in the MVP, so the Failed status is not an unexplained dead end.

**Supersedes:** (supersedes nothing — net-new information)

---

### ADV-45 — Authentication specifies only the invalid-credentials path; there is no defined UI for a login network failure/timeout, and password-reset is absent from scope entirely.

**Finding (verbatim, from the review):**
> | Exception paths | {invalid credentials → generic 401 error message → user retries} [SRC: C-065] |

**Problem as stated by the review:** Authentication specifies only the invalid-credentials path; there is no defined UI for a login network failure/timeout, and password-reset (a standard recovery path) is absent from scope entirely.

**Review's actionable payload:** Recommendation — "Add an exception path for login network failure (retry affordance) and explicitly mark password-reset as in/out of scope so its absence is deliberate rather than an omission." · Disposition — Defer.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
The Authentication flow defines a login network-failure/timeout exception path: a network error shows a retry affordance, distinct from the invalid-credentials 401 message. Password reset is explicitly out of scope for the MVP.

**Supersedes:** (supersedes nothing — net-new information)

---

### ADV-46 — "a baseline accessibility standard" is not testable — no WCAG level, version, or conformance target is named, so an FE consumer cannot verify a11y states.

**Finding (verbatim, from the review):**
> - The application targets desktop browsers first and meets a baseline accessibility standard [SRC: C-046].

**Problem as stated by the review:** "a baseline accessibility standard" is not testable — no WCAG level, version, or conformance target is named, so an FE consumer cannot verify a11y states.

**Review's actionable payload:** Recommendation — "Replace 'a baseline accessibility standard' with an explicit, testable target such as 'WCAG 2.1 AA'." · Disposition — Patch.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
The application meets WCAG 2.1 AA; an FE consumer verifies accessibility states against that named target.

**Supersedes:** This supersedes the statement in `requirements/requirements.md` regarding §6.6.5's "baseline accessibility standard".

---

### ADV-47 — "desktop browsers first" names no concrete browser/version targets, so device-specific layout and rendering feasibility cannot be assessed or tested.

**Finding (verbatim, from the review):**
> | Environment assumption | Users operate desktop browsers first; a baseline accessibility standard is met [SRC: C-046] | stated |

**Problem as stated by the review:** "desktop browsers first" names no concrete browser/version targets, so device-specific layout and rendering feasibility cannot be assessed or tested.

**Review's actionable payload:** Recommendation — "Name explicit browser-target floors (e.g. 'Chrome ≥110, Firefox ≥110, Safari ≥16, no IE') and the supported viewport/device baseline." · Disposition — Patch.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
Supported browsers are the current and prior major versions of Chrome, Edge, Firefox, and Safari on desktop; Internet Explorer is not supported. The supported viewport baseline is desktop widths (≥1280px).

**Supersedes:** This supersedes the statement in `requirements/requirements.md` regarding §1.6's "desktop browsers first" environment assumption.

---

### ADV-48 — The document handles POPIA-bearing financial PII but defines no retention window, consent flow, or data-residency treatment beyond on-screen masking, leaving the compliance posture incomplete.

**Finding (verbatim, from the review):**
> - The corpus claims no specific compliance regime; non-functional and compliance signals are stamped from domain defaults [SRC: C-067].

**Problem as stated by the review:** The document handles POPIA-bearing financial PII (AccountNumber, Amount, Currency, Email) but defines no retention window, consent flow, or data-residency treatment beyond on-screen masking, leaving the compliance posture incomplete.

**Review's actionable payload:** Recommendation — "Add explicit POPIA treatment — a retention window, a consent-capture UI requirement, and a data-residency note — even if scoped as application-build guidance." · Disposition — Defer.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
POPIA treatment for the financial PII (AccountNumber, Amount, Currency, Email) is specified: a data-retention window, a consent-capture requirement, and a data-residency note. For the frontend prototype these are application-build guidance (the prototype enforces on-screen masking per BR-07/F-13); retention, consent, and residency are backend/operational concerns recorded so the compliance posture is complete rather than silent.

**Supersedes:** (supersedes nothing — net-new information)

---

### ADV-49 — The client-side retained-transaction band (10²–10⁴) that drives the render budget and in-memory filtering is entirely inferred with no corpus source, so the load model underpinning client-side feasibility is unvalidated.

**Finding (verbatim, from the review):**
> | Data volume | ~20 transactions per imported file; no corpus-stated overall cap, so a client-side band of 10²–10⁴ retained transactions is assumed | inferred |

**Problem as stated by the review:** The client-side retained-transaction band (10²–10⁴) that drives the §6.6.2 render budget and the §6.1 F-07 in-memory filtering is entirely inferred with no corpus source, so the load model underpinning client-side feasibility is unvalidated.

**Review's actionable payload:** Recommendation — "Confirm the upper-bound transaction count with the client (or flag it as a blocking assumption) so the client-side filter/pagination/render budgets rest on a validated load model." · Disposition — Defer.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
The client-side retained-transaction working-set of ~1,000 (per ADV-16), with a 10⁴ stress ceiling, is recorded as an explicit planning assumption to be confirmed with the client — flagged as an assumption rather than a validated figure, so the client-side filter/pagination/render budgets rest on a stated (if provisional) load model.

**Supersedes:** (supersedes nothing — net-new information)

---

### ADV-50 — No cost, timeline, or team-size constraint is stated anywhere in the document, so delivery feasibility cannot be assessed.

**Finding (verbatim, from the review):**
> > Volumes drive UI pattern selection only.

**Problem as stated by the review:** No cost, timeline, or team-size constraint is stated anywhere in the document (concurrency "10¹" describes runtime users, not delivery resourcing), so delivery feasibility cannot be assessed.

**Review's actionable payload:** Recommendation — "Add a brief delivery-constraints note (target timeline, team size, budget envelope) or explicitly record that these are out of scope for this spec." · Disposition — Defer.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
Delivery constraints — cost, timeline, and team size — are out of scope for this frontend specification; the runtime concurrency figure (10¹) describes users, not delivery resourcing. Their absence is a deliberate scope decision, not an omission.

**Supersedes:** (supersedes nothing — net-new information)

---

### ADV-51 — No operational requirements (logging, monitoring, alerting, backups, disaster recovery) are named anywhere, so the system is specified to run in production with an undefined operational posture.

**Finding (verbatim, from the review):**
> | Capability category | Driving requirement(s) | Recommendation (optional) |

**Problem as stated by the review:** No operational requirements (logging, monitoring, alerting, backups, disaster recovery) are named anywhere, so the system is specified to run in production with an undefined operational posture (backend-only, Not Prototypable).

**Review's actionable payload:** Recommendation — "Add an operational-requirements note (logging/monitoring/alerting/backup/DR expectations) under §1.7 application-build guidance, or explicitly scope it out." · Disposition — Defer.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
Operational requirements — logging, monitoring, alerting, backups, and disaster recovery — are backend/operational concerns out of scope for the frontend prototype; they are recorded as application-build guidance under §1.7 so the operational posture is acknowledged rather than silent.

**Supersedes:** (supersedes nothing — net-new information)

---

### ADV-52 — Step-up re-authentication for every approve/reject is asserted as an inferred default but has no supporting latency, UX, or session-mechanism detail, making its feasibility against the ~1s approve budget untested.

**Finding (verbatim, from the review):**
> | Re-auth scope | Step-up auth required for approve-class actions (approve/reject) | inferred |

**Problem as stated by the review:** Step-up re-authentication for every approve/reject is asserted as an inferred default but has no supporting latency, UX, or session-mechanism detail, making its feasibility against the "reflect within about one second" approve budget (F-08) untested.

**Review's actionable payload:** Recommendation — "Either confirm step-up auth is required (and reconcile it with the ~1s approve-reflect budget) or downgrade it to an explicit open question." · Disposition — Defer.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
Step-up re-authentication per approve/reject is not part of the MVP (consistent with ADV-01/ADV-32/ADV-35); there is therefore no step-up latency to reconcile against the F-08 ~1s approve-reflect budget. The §6.6.1 step-up row is advisory application-build guidance only.

**Supersedes:** This supersedes the statement in `requirements/requirements.md` regarding §6.6.1's step-up re-auth scope row (as a feasibility constraint on the approve budget).

---

### ADV-53 — A p95 ≤ 500 ms render budget is asserted with no named stack, rendering strategy, or row-count basis, so the threshold is unanchored and unverifiable.

**Finding (verbatim, from the review):**
> | Render budget for largest list/table | p95 ≤ 500 ms for the transaction table | inferred |

**Problem as stated by the review:** A p95 ≤ 500 ms render budget is asserted with no named stack, rendering strategy, or row-count basis (the 10⁴ upper band is itself inferred), so the threshold is unanchored and unverifiable.

**Review's actionable payload:** Recommendation — "Tie the render budget to a stated row count and rendering approach (e.g. virtualised list at 10⁴ rows) or mark it explicitly provisional pending the validated volume." · Disposition — Defer.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
The §6.6.2 p95 ≤ 500 ms render budget is anchored to a defined basis: it applies to a paginated/virtualized transaction table (per ADV-37/ADV-41) at the ~1,000 planning working-set (per ADV-16/ADV-49). The figure is provisional pending the client-confirmed volume, so the threshold is no longer unanchored.

**Supersedes:** This supersedes the statement in `requirements/requirements.md` regarding §6.6.2's unanchored p95 ≤ 500 ms render budget.

---

## Findings considered but skipped

(none — every selected finding was resolved)
