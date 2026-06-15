'use client'

import { Check, Eye, X } from 'lucide-react'

import { MaskedAccountNumber } from '@/components/atoms/MaskedAccountNumber'
import { StatusBadge, type StatusTone } from '@/components/atoms/StatusBadge'
import { Button } from '@/components/ui/button'
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'
import type { Transaction } from '@/types'

/**
 * Dense, compact, scannable transaction table (UX posture P3 Analytical / Information-Dense).
 *
 * Anti-fabrication: only LS-01's closed Property set is rendered —
 * { Reference, TransactionDate, AccountNumber, Amount, Currency, Status }. Each data cell's
 * value element carries data-prop="Transaction.<Field>". Search / approve / reject / view are
 * UI controls and carry no data-prop.
 */
export function TransactionTable({
  rows,
  canAction,
  onView,
  onApprove,
  onReject,
}: {
  rows: Transaction[]
  canAction: boolean
  onView: (t: Transaction) => void
  onApprove: (t: Transaction) => void
  onReject: (t: Transaction) => void
}) {
  return (
    <div className="overflow-x-auto rounded-md border">
      <Table className="text-xs">
        <TableHeader>
          <TableRow className="bg-muted">
            <TableHead className="sticky top-0 z-10 h-8 bg-muted px-2 py-1">
              Reference
            </TableHead>
            <TableHead className="sticky top-0 z-10 h-8 bg-muted px-2 py-1">
              Date
            </TableHead>
            <TableHead className="sticky top-0 z-10 h-8 bg-muted px-2 py-1">
              Account
            </TableHead>
            <TableHead className="sticky top-0 z-10 h-8 bg-muted px-2 py-1 text-right">
              Amount
            </TableHead>
            <TableHead className="sticky top-0 z-10 h-8 bg-muted px-2 py-1">
              Status
            </TableHead>
            <TableHead className="sticky top-0 z-10 h-8 bg-muted px-2 py-1 text-right">
              Actions
            </TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {rows.map((t, index) => {
            const tone: StatusTone =
              t.Status === 'Approved'
                ? 'success'
                : t.Status === 'Rejected'
                  ? 'danger'
                  : 'info'
            const showActions = canAction && t.Status === 'Imported'
            return (
              <TableRow key={t.Id}>
                <TableCell className="px-2 py-1 font-medium">
                  <span data-prop="Transaction.Reference">{t.Reference}</span>
                </TableCell>
                <TableCell className="px-2 py-1 tabular-nums">
                  <span data-prop="Transaction.TransactionDate">
                    {t.TransactionDate}
                  </span>
                </TableCell>
                <TableCell className="px-2 py-1">
                  <MaskedAccountNumber value={t.AccountNumber} />
                </TableCell>
                <TableCell className="px-2 py-1 text-right tabular-nums">
                  <span className="text-muted-foreground" data-prop="Transaction.Currency">
                    {t.Currency}
                  </span>{' '}
                  <span data-prop="Transaction.Amount">
                    {t.Amount.toLocaleString('en-ZA', {
                      minimumFractionDigits: 2,
                      maximumFractionDigits: 2,
                    })}
                  </span>
                </TableCell>
                <TableCell className="px-2 py-1" data-prop="Transaction.Status">
                  <StatusBadge label={t.Status} tone={tone} />
                </TableCell>
                <TableCell className="px-2 py-1">
                  <div className="flex items-center justify-end gap-1">
                    <Button
                      variant="ghost"
                      size="xs"
                      onClick={() => onView(t)}
                      aria-label={`View ${t.Reference}`}
                      data-testid={index === 0 ? 'primary-cta' : undefined}
                    >
                      <Eye aria-hidden="true" />
                      View
                    </Button>
                    {showActions ? (
                      <>
                        <Button
                          variant="outline"
                          size="xs"
                          onClick={() => onApprove(t)}
                          aria-label={`Approve ${t.Reference}`}
                        >
                          <Check aria-hidden="true" />
                          Approve
                        </Button>
                        <Button
                          variant="outline"
                          size="xs"
                          onClick={() => onReject(t)}
                          aria-label={`Reject ${t.Reference}`}
                        >
                          <X aria-hidden="true" />
                          Reject
                        </Button>
                      </>
                    ) : null}
                  </div>
                </TableCell>
              </TableRow>
            )
          })}
        </TableBody>
      </Table>
    </div>
  )
}
