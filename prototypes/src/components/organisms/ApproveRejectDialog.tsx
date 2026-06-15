'use client'

import * as React from 'react'
import { AlertTriangle } from 'lucide-react'

import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog'
import { Button } from '@/components/ui/button'
import { StatusBadge } from '@/components/atoms/StatusBadge'
import { Textarea } from '@/components/atoms/Textarea'
import { InlineError } from '@/components/atoms/InlineError'
import type { Transaction } from '@/types'

/**
 * LS-03 — Approve/reject confirmation modal.
 *
 * Confirms a consequential, terminal approve/reject decision. The decision is restated using
 * EXACTLY LS-03's closed property set {Reference, Amount, Status, UserNote} — no Currency, Date,
 * AccountNumber or TransactionType is rendered (those are not in this surface's closed set).
 * Reject requires a mandatory note (BR-02 terminal/irreversible action; N5 error prevention).
 *
 * Controlled by the driver, which owns open state, the host route, and the onConfirm handler.
 */
export function ApproveRejectDialog({
  transaction,
  mode,
  open,
  onOpenChange,
  onConfirm,
}: {
  transaction: Transaction | null
  mode: 'approve' | 'reject'
  open: boolean
  onOpenChange: (o: boolean) => void
  onConfirm: (note?: string) => void
}) {
  const [note, setNote] = React.useState('')
  const [error, setError] = React.useState<string | null>(null)

  // Reset note + error whenever the dialog opens or the target/mode changes, so a prior
  // note never leaks between transactions or between approve/reject.
  React.useEffect(() => {
    setNote('')
    setError(null)
  }, [open, transaction?.Id, mode])

  // Guard a null transaction: render a safe, empty dialog body.
  if (!transaction) {
    return (
      <Dialog open={open} onOpenChange={onOpenChange}>
        <DialogContent />
      </Dialog>
    )
  }

  const isReject = mode === 'reject'
  const title = isReject ? 'Reject transaction' : 'Approve transaction'
  const confirmLabel = isReject ? 'Reject' : 'Approve'
  const confirmVariant = isReject ? 'destructive' : 'default'

  const handleConfirm = () => {
    if (isReject) {
      const trimmed = note.trim()
      if (trimmed.length === 0) {
        setError('A note is required to reject this transaction.')
        return
      }
      onConfirm(trimmed)
      return
    }
    onConfirm()
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>{title}</DialogTitle>
          <DialogDescription>
            Confirm this decision for the transaction below.
          </DialogDescription>
        </DialogHeader>

        {/* Decision restatement — closed set {Reference, Amount, Status, UserNote} only */}
        <dl className="grid grid-cols-[auto_1fr] gap-x-4 gap-y-2 text-sm">
          <dt className="text-muted-foreground">Reference</dt>
          <dd>
            <span data-prop="Transaction.Reference">{transaction.Reference}</span>
          </dd>

          <dt className="text-muted-foreground">Amount</dt>
          <dd>
            <span data-prop="Transaction.Amount">
              {transaction.Amount.toLocaleString('en-ZA', {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2,
              })}
            </span>
          </dd>

          <dt className="text-muted-foreground">Status</dt>
          <dd>
            <span data-prop="Transaction.Status">
              <StatusBadge label={transaction.Status} tone="info" />
            </span>
          </dd>
        </dl>

        {/* BR-02 terminal/irreversible warning */}
        <p className="flex items-center gap-1.5 text-sm text-muted-foreground">
          <AlertTriangle className="size-4 shrink-0" aria-hidden="true" />
          <span>This action is final and cannot be changed.</span>
        </p>

        {isReject && (
          <div>
            <label
              htmlFor="approve-reject-note"
              className="mb-1 block text-sm font-medium"
            >
              Reason for rejection (required)
            </label>
            <Textarea
              id="approve-reject-note"
              data-prop="Transaction.UserNote"
              value={note}
              onChange={(e) => {
                setNote(e.target.value)
                if (error) setError(null)
              }}
              aria-required="true"
              aria-invalid={error ? true : undefined}
              aria-describedby={error ? 'approve-reject-note-error' : undefined}
              placeholder="Explain why this transaction is being rejected"
            />
            <InlineError id="approve-reject-note-error">{error}</InlineError>
          </div>
        )}

        <DialogFooter>
          <Button variant="outline" onClick={() => onOpenChange(false)}>
            Cancel
          </Button>
          <Button variant={confirmVariant} onClick={handleConfirm}>
            {confirmLabel}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}
