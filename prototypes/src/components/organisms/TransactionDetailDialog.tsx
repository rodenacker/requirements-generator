'use client'

import {
  Dialog,
  DialogClose,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog'
import { Button } from '@/components/ui/button'
import { StatusBadge } from '@/components/atoms/StatusBadge'
import { DescriptionList, type DescriptionListItem } from '@/components/molecules/DescriptionList'
import type { Transaction } from '@/types'

/**
 * LS-02 — read-only centred modal disclosing a transaction's non-column fields, and
 * (AMD-94) the post-hoc action-audit detail for a completed transaction reached from the
 * row "View" link. Controlled by the driver (open / onOpenChange).
 *
 * Closed-set Properties only: Transaction.TransactionType, Transaction.Description,
 * Transaction.UserNote, and — for Approved/Rejected rows — Transaction.ActionedBy +
 * Transaction.ActionedAt (AMD-94 §7 extension, consultant-confirmed). No column fields
 * (Reference/Amount/AccountNumber/Date) and no editing.
 * Radix traps + restores focus; Close/Esc/overlay all dismiss (N3 user control).
 */
export function TransactionDetailDialog({
  transaction,
  open,
  onOpenChange,
}: {
  transaction: Transaction | null
  open: boolean
  onOpenChange: (o: boolean) => void
}) {
  const items: DescriptionListItem[] = transaction
    ? [
        {
          term: 'Type',
          value: (
            <StatusBadge
              label={transaction.TransactionType}
              tone={transaction.TransactionType === 'Credit' ? 'info' : 'neutral'}
            />
          ),
          dataProp: 'Transaction.TransactionType',
        },
        {
          term: 'Description',
          value: transaction.Description ?? '—',
          dataProp: 'Transaction.Description',
        },
        {
          term: 'Note',
          value: transaction.UserNote ?? '—',
          dataProp: 'Transaction.UserNote',
        },
      ]
    : []

  // AMD-94 action-audit block — only for a completed (Approved/Rejected) transaction.
  const isActioned =
    transaction != null && transaction.Status !== 'Imported'
  const auditItems: DescriptionListItem[] = isActioned
    ? [
        {
          term: 'Outcome',
          value: (
            <StatusBadge
              label={transaction!.Status}
              tone={transaction!.Status === 'Approved' ? 'success' : 'danger'}
            />
          ),
          dataProp: 'Transaction.Status',
        },
        {
          term: 'Actioned by',
          value: transaction!.ActionedBy ?? '—',
          dataProp: 'Transaction.ActionedBy',
        },
        {
          term: 'Actioned at',
          value: transaction!.ActionedAt ?? '—',
          dataProp: 'Transaction.ActionedAt',
        },
      ]
    : []

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Transaction detail</DialogTitle>
          <DialogDescription>
            Read-only details for the selected transaction.
          </DialogDescription>
        </DialogHeader>
        {transaction ? <DescriptionList items={items} /> : null}
        {isActioned ? (
          <section aria-label="Action audit" className="mt-4 border-t pt-4">
            <h3 className="mb-3 text-sm font-semibold text-foreground">Action audit</h3>
            <DescriptionList items={auditItems} />
          </section>
        ) : null}
        <DialogFooter>
          <DialogClose asChild>
            <Button variant="outline">Close</Button>
          </DialogClose>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}
