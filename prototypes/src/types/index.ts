// Prototype entity types — shared across prototypes. Added per-generation by prototype-generator.

/** Transaction.Status closed enum — §7 Transaction [SRC: C-014]. */
export type TransactionStatus = 'Imported' | 'Approved' | 'Rejected'

/** Transaction.TransactionType closed enum — §7 Transaction [SRC: C-049]. */
export type TransactionKind = 'Credit' | 'Debit'

/**
 * §7 Transaction data shape (closed set). Store + fixture fields are EXACTLY these
 * properties — no fabricated fields (anti-fabrication contract,
 * blueprints/approval-queue/blueprint.md).
 *
 * AMD-94 extension (consultant-confirmed 2026-06-15): ActionedBy + ActionedAt are the
 * acting-user reference and action timestamp recorded when an Imported transaction is
 * approved/rejected. requirements.md §7 carries these as AMD-94 PROPOSED ADDITIONS; the
 * consultant confirmed the closed-set extension for this prototype. Run /resolve-review to
 * formalise AMD-94 into requirements.md + the blueprint closed set. Both are optional:
 * absent on Imported (un-actioned) rows, present once a row is Approved/Rejected.
 */
export interface Transaction {
  Id: number
  FileLogId: number
  Reference: string
  TransactionDate: string
  AccountNumber: string
  Description?: string
  Amount: number
  TransactionType: TransactionKind
  Currency: string
  Status: TransactionStatus
  UserNote?: string
  /** AMD-94: acting-user reference (the active chrome role that actioned the row). */
  ActionedBy?: string
  /** AMD-94: action timestamp, canonical display format YYYY-MM-DD HH:mm (matches TransactionDate). */
  ActionedAt?: string
}
