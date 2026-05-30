# Northstar Wealth Client Onboarding & KYC Wizard

## Project Overview

Northstar Wealth is a wealth management firm seeking to modernize its client onboarding process. Today, new clients complete onboarding during a 2–3 hour in-person meeting with a financial advisor. The objective of this project is to shift most information gathering, verification, and risk assessment activities to a self-service digital experience that clients can complete from home.

The solution will reduce advisor meeting time to approximately 20 minutes by allowing clients to submit their personal information, supporting documentation, and investment profile before their appointment.

The application must create a professional, trustworthy, and secure experience that reflects the expectations of financial services clients while complying with Know Your Customer (KYC) and Anti-Money Laundering (AML) onboarding practices.

---

# Business Goals

### Primary Goals

1. Reduce advisor-led onboarding time from 2–3 hours to approximately 20 minutes.
2. Improve client onboarding efficiency through self-service data capture.
3. Increase data accuracy by allowing clients to review and validate their information before submission.
4. Collect all information required for KYC and suitability assessments before advisor review.
5. Improve client experience by reducing paperwork and repetitive data entry.

### Success Measures

* Clients can complete onboarding within approximately 15 minutes.
* Advisor meetings focus on review and advice rather than data capture.
* Users can pause and resume onboarding without losing progress.
* All mandatory KYC documentation is submitted prior to advisor review.
* Risk profile assessments are completed consistently and accurately.

---

# User Goals

As a prospective client, I want to:

* Understand what information I need before starting.
* Complete onboarding from home at my own pace.
* Save my progress and continue later.
* Know why sensitive information is being requested.
* Feel confident that my personal information is handled securely.
* Upload documents easily and verify that they were received correctly.
* Review and correct information before submission.
* Understand my investment risk profile.
* Receive confirmation that my application has been submitted successfully.

---

# Target Users

## Primary User

Prospective Northstar Wealth clients who are:

* Opening a new investment account.
* Completing onboarding independently.
* Comfortable using desktop web applications.
* Required to provide identity and financial information.

## User Characteristics

* Financial knowledge may vary significantly.
* May be unfamiliar with KYC terminology.
* Expect professionalism and clarity.
* May be cautious about sharing personal and financial information online.

---

# Application Scope

The application consists of a six-step onboarding wizard.

### Core Features

* Multi-step workflow
* Progress indicator
* Forward and backward navigation
* Validation and error handling
* Save and resume capability
* File upload and preview
* Risk profile calculation
* Review and edit functionality
* Submission confirmation

---

# Functional Requirements

## Step 1: Get Started

### Purpose

Prepare the client for the onboarding process and establish a resumable session.

### Fields

* Email address

### Content

Display:

* Estimated completion time (15 minutes)
* Required documents:

  * Government-issued ID
  * Proof of address
  * Employment details

### Actions

* Begin onboarding
* Create onboarding session
* Store session locally for resumption

### Validation

* Valid email format
* Email required

---

## Step 2: Personal Details

### Purpose

Collect identity and residency information required for KYC compliance.

### Fields

* Full legal name
* Preferred name
* Date of birth
* Nationality
* Country of residence
* Tax residency
* Mobile number
* Email confirmation

### Validation

* Age must be 18 years or older
* Required fields completed
* Email confirmation matches Step 1 email
* Mobile number valid format
* Nationality selected
* Country of residence selected
* Tax residency selected

### Reference Data

Nationality and tax residency dropdowns must include at least the 20 most common countries.

---

## Step 3: Identity Verification

### Purpose

Collect supporting documentation required for KYC verification.

### Identity Document Types

* Passport
* Driver's License
* National ID

### Upload Requirements

#### Identity Document

Passport:

* Front image only

Driver's License:

* Front image
* Back image

National ID:

* Front image
* Back image

#### Proof of Address

Accepted:

* Utility bill
* Bank statement

Requirements:

* Dated within the last three months

### Supported File Types

* JPG
* PNG
* PDF

### File Size

Maximum 5 MB per file

### UX Requirements

* Upload progress indicator
* Preview thumbnail after upload
* Clear validation feedback

### Validation

* Supported file type
* File size limit
* Required uploads completed

---

## Step 4: Employment & Source of Funds

### Purpose

Collect financial information required for regulatory compliance.

### Employment Status

Options:

* Employed
* Self-employed
* Retired
* Unemployed
* Student

### Conditional Fields

#### Employed

* Employer name
* Job title
* Annual income bracket

#### Self-employed

* Business name
* Occupation
* Annual income bracket

#### Retired

* Previous occupation
* Pension income bracket

#### Student

* Institution name
* Funding source

#### Unemployed

* Source of living expenses

### Annual Income Brackets

* Under $25,000
* $25,000–$50,000
* $50,001–$100,000
* $100,001–$250,000
* Above $250,000

### Source of Funds

Options:

* Salary
* Savings
* Inheritance
* Sale of property
* Business proceeds
* Other

If "Other":

* Explanation required
* Minimum 20 characters

---

## Step 5: Risk Profile Assessment

### Purpose

Determine the client's investment risk tolerance.

### Question 1

How would you react if your investment portfolio declined by 15% over six months?

* Sell immediately (1)
* Reduce investments (2)
* Hold and wait (3)
* Invest more while prices are lower (4)

### Question 2

What is your investment time horizon?

* Less than 2 years (1)
* 2–5 years (2)
* 5–10 years (3)
* More than 10 years (4)

### Question 3

Which investment would you choose?

* Guaranteed return (1)
* Mostly stable with modest growth (2)
* Balanced growth and risk (3)
* Highest growth potential despite volatility (4)

### Question 4

How familiar are you with investment markets?

* No experience (1)
* Limited experience (2)
* Moderate experience (3)
* Extensive experience (4)

### Question 5

What is your primary investment objective?

* Preserve capital (1)
* Generate income (2)
* Long-term growth (3)
* Maximise growth (4)

### Scoring

Minimum Score: 5

Maximum Score: 20

### Risk Categories

| Score | Category     |
| ----- | ------------ |
| 5–8   | Conservative |
| 9–12  | Balanced     |
| 13–16 | Growth       |
| 17–20 | Aggressive   |

### Output

Display:

* Risk category
* One-sentence description

Example:

**Balanced** — You are comfortable accepting moderate fluctuations in pursuit of long-term investment growth.

---

## Step 6: Review & Submit

### Purpose

Allow users to verify information before submission.

### Display

Read-only summary grouped by:

* Personal Details
* Identity Verification
* Employment & Source of Funds
* Risk Profile

### Edit Functionality

Each section includes an Edit action.

### Declarations

Required checkboxes:

* Information provided is accurate.
* Terms and conditions accepted.
* Consent to identity verification checks.

### Submission

Submit onboarding application to mock endpoint.

### Success State

Display:

* Confirmation number
* Submission confirmation message
* Advisor follow-up process
* Contact email address

---

# User Experience Requirements

## Progress Tracking

Display:

* Current step
* Total steps
* Completion percentage

---

## Save & Resume

### Storage

Use localStorage.

### Resume Behaviour

If existing progress is detected:

"Welcome back. Continue from Step X."

### Security Requirement

To resume an application, the user must re-enter the email address used to start onboarding.

This provides a minimum identity check without requiring a full authentication system.

---

## Review Editing Behaviour

Decision:

When editing from the Review step, users return directly to Review after saving changes.

### Rationale

Users are performing targeted corrections rather than re-completing the workflow. Requiring them to navigate Steps 4–5 again would create unnecessary friction and increase abandonment risk.

---

# Trust & Tone Strategy

The experience should communicate professionalism, transparency, and care.

### Principles

#### Explain Why

Each step includes a short explanation describing why the information is required.

Example:

"We collect your tax residency information to meet international regulatory requirements."

#### Reassure Without Overpromising

Use plain language:

"Your documents are securely transmitted and only used to verify your identity."

Avoid vague claims such as:

* Bank-grade security
* Military-grade encryption
* Completely secure

#### Helpful Errors

User mistakes:

* Specific and corrective

Example:

"Your proof of address must be dated within the last three months."

System issues:

* Apologetic and actionable

Example:

"We couldn't upload your document right now. Please try again."

#### Professional Tone

Avoid:

* Emojis
* Casual social-media language
* Excessive legal terminology

Focus on clarity, confidence, and respect.

---

# Technical Requirements

## Technology Stack

* React
* TypeScript
* Tailwind CSS

## Data Management

* Local component state
* Persistent localStorage state

## Upload Handling

* Base64 encoded files stored in state
* Mock upload endpoint

## Submission Handling

* Mock submission endpoint
* Generate confirmation number
* Clear localStorage after successful submission

## Browser Support

Desktop viewport only

Target width:

* 1280px and above

---

# Non-Functional Requirements

## Performance

* Step transitions under 300ms
* Upload simulation under 2 seconds

## Reliability

* No data loss during refresh
* Validation consistent across steps

## Accessibility

* Keyboard accessible navigation
* Visible focus states
* Associated labels for all fields
* Screen-reader friendly error messages

---

# Deliverables

1. React application
2. TypeScript source code
3. Tailwind styling implementation
4. DECISIONS.md documenting:

   * Risk profile design
   * Review editing behaviour
   * Save-and-resume identity approach
   * Trust and tone strategy
5. Basic test coverage
6. README with setup instructions

---

# Acceptance Criteria

The onboarding journey can be completed from start to finish, resumed after refresh, validated correctly, edited from review, submitted successfully, and leaves the client feeling confident that Northstar Wealth is handling their personal information professionally and responsibly.
