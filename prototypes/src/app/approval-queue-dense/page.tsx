'use client'

import { useEffect, useMemo, useState } from 'react'

import { TableSkeleton } from '@/components/atoms/TableSkeleton'
import { EmptyState } from '@/components/molecules/EmptyState'
import { Pagination } from '@/components/molecules/Pagination'
import { SearchFilterBar } from '@/components/molecules/SearchFilterBar'
import { ApproveRejectDialog } from '@/components/organisms/ApproveRejectDialog'
import { TransactionDetailDialog } from '@/components/organisms/TransactionDetailDialog'
import { TransactionTable } from '@/components/organisms/TransactionTable'
import { Button } from '@/components/ui/button'
import { useProtoChromeStore } from '@/stores/proto-chrome-store'
import { useTransactionStore } from '@/stores/transaction-store'
import type { Transaction } from '@/types'

const PAGE_SIZE = 8

type Notice = { tone: 'success' | 'error'; text: string } | null

/**
 * Approval Queue — Dense (LS-01 host). Dense scannable transaction table (DENSE-LEAN basis,
 * posture P3) hosting the read-only transaction-detail modal (LS-02, consultant-directed) and
 * the approve/reject confirmation modal (LS-03). Role-gated approve/reject (BR-05) via the
 * prototype chrome's activeRole (PI-05). Fixture-backed, in-session mutations only (PI-01/PI-02).
 */
export default function ApprovalQueueDensePage() {
  const items = useTransactionStore((s) => s.items)
  const isLoaded = useTransactionStore((s) => s.isLoaded)
  const approve = useTransactionStore((s) => s.approve)
  const reject = useTransactionStore((s) => s.reject)

  const activeRole = useProtoChromeStore((s) => s.activeRole)
  // BR-05: only the Approver may approve/reject; default view is the Importer (read-only).
  const canAction = (activeRole ?? 'Importer') === 'Approver'

  const [query, setQuery] = useState('')
  const [status, setStatus] = useState('all')
  const [page, setPage] = useState(1)
  const [notice, setNotice] = useState<Notice>(null)

  const [detailTxn, setDetailTxn] = useState<Transaction | null>(null)
  const [detailOpen, setDetailOpen] = useState(false)

  const [actionTxn, setActionTxn] = useState<Transaction | null>(null)
  const [actionMode, setActionMode] = useState<'approve' | 'reject'>('approve')
  const [actionOpen, setActionOpen] = useState(false)

  useEffect(() => {
    document.title = 'Approval Queue — Dense'
  }, [])

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase()
    return items.filter((t) => {
      const matchesStatus = status === 'all' || t.Status === status
      const matchesQuery =
        !q ||
        t.Reference.toLowerCase().includes(q) ||
        t.AccountNumber.toLowerCase().includes(q) ||
        (t.Description ?? '').toLowerCase().includes(q)
      return matchesStatus && matchesQuery
    })
  }, [items, query, status])

  const pageCount = Math.max(1, Math.ceil(filtered.length / PAGE_SIZE))
  const currentPage = Math.min(page, pageCount)
  const pageRows = filtered.slice((currentPage - 1) * PAGE_SIZE, currentPage * PAGE_SIZE)

  function clearFilters() {
    setQuery('')
    setStatus('all')
    setPage(1)
  }

  function openDetail(t: Transaction) {
    setDetailTxn(t)
    setDetailOpen(true)
  }

  function openAction(t: Transaction, mode: 'approve' | 'reject') {
    setActionTxn(t)
    setActionMode(mode)
    setActionOpen(true)
  }

  function confirmAction(note?: string) {
    if (!actionTxn) return
    // AMD-94: record the acting user. Only the Approver may action (BR-05/canAction guard),
    // so the actor is the active chrome role (PI-05).
    const actor = activeRole ?? 'Approver'
    const result =
      actionMode === 'approve'
        ? approve(actionTxn.Id, actor)
        : reject(actionTxn.Id, note ?? '', actor)
    if (result.ok) {
      setNotice({
        tone: 'success',
        text: `${actionTxn.Reference} ${actionMode === 'approve' ? 'approved' : 'rejected'}.`,
      })
      setActionOpen(false)
    } else if (result.reason === 'not-imported') {
      // F-10 / BR-04 stale-action guard: the row was already actioned.
      setNotice({
        tone: 'error',
        text: `${actionTxn.Reference} was already actioned and can no longer be changed.`,
      })
      setActionOpen(false)
    }
    // note-required is handled inside the dialog (it blocks and shows an inline error).
  }

  return (
    <div className="mx-auto max-w-6xl p-6">
      <header className="mb-4">
        <h1 className="text-xl font-semibold tracking-tight">Approval queue</h1>
        <p className="mt-1 text-sm text-muted-foreground">
          {filtered.length} of {items.length} transactions ·{' '}
          {canAction
            ? 'Approver — approve/reject available on Imported rows'
            : 'Importer — read-only (switch role to action)'}
        </p>
      </header>

      {notice ? (
        <div
          role={notice.tone === 'error' ? 'alert' : 'status'}
          className={
            notice.tone === 'error'
              ? 'mb-3 flex items-center justify-between rounded-md border border-red-300 bg-red-50 px-3 py-2 text-sm text-red-900'
              : 'mb-3 flex items-center justify-between rounded-md border border-green-300 bg-green-50 px-3 py-2 text-sm text-green-900'
          }
        >
          <span>{notice.text}</span>
          <Button variant="ghost" size="xs" onClick={() => setNotice(null)} aria-label="Dismiss notice">
            Dismiss
          </Button>
        </div>
      ) : null}

      <div className="mb-3">
        <SearchFilterBar
          query={query}
          onQuery={(v) => {
            setQuery(v)
            setPage(1)
          }}
          status={status}
          onStatus={(v) => {
            setStatus(v)
            setPage(1)
          }}
          onClear={clearFilters}
        />
      </div>

      {!isLoaded ? (
        <TableSkeleton rows={8} cols={7} />
      ) : filtered.length === 0 ? (
        <EmptyState
          title="No transactions match"
          message="No transactions match the active filters. Clear them to see the full queue."
          action={
            <Button variant="outline" size="sm" onClick={clearFilters}>
              Clear filters
            </Button>
          }
        />
      ) : (
        <>
          <TransactionTable
            rows={pageRows}
            canAction={canAction}
            onView={openDetail}
            onApprove={(t) => openAction(t, 'approve')}
            onReject={(t) => openAction(t, 'reject')}
          />
          <div className="mt-3">
            <Pagination page={currentPage} pageCount={pageCount} onPage={setPage} />
          </div>
        </>
      )}

      <TransactionDetailDialog
        transaction={detailTxn}
        open={detailOpen}
        onOpenChange={setDetailOpen}
      />
      <ApproveRejectDialog
        transaction={actionTxn}
        mode={actionMode}
        open={actionOpen}
        onOpenChange={setActionOpen}
        onConfirm={confirmAction}
      />
    </div>
  )
}
