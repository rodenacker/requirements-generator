import { create } from 'zustand'
import { persist, createJSONStorage } from 'zustand/middleware'

import type { Transaction } from '@/types'
import fixtures from '@/data/fixtures/transaction.json'

/** Result of an approve/reject attempt; `reason` carries the business-rule that blocked it. */
export interface ActionResult {
  ok: boolean
  reason?: 'not-found' | 'not-imported' | 'note-required'
}

interface TransactionState {
  items: Transaction[]
  isLoaded: boolean
  seedFromFixtures: () => void
  reset: () => void
  /** Approve an Imported transaction (BR-01/BR-02/BR-04: only Imported is actionable). Records the acting user + timestamp (AMD-94). */
  approve: (id: number, actor: string) => ActionResult
  /** Reject an Imported transaction with a mandatory note (BR-03). Records the acting user + timestamp (AMD-94). */
  reject: (id: number, note: string, actor: string) => ActionResult
}

const fresh = (): Transaction[] =>
  (fixtures as unknown as Transaction[]).map((t) => ({ ...t }))

/**
 * Action timestamp in the canonical §7 display format (YYYY-MM-DD HH:mm). Simulated
 * server clock per PI-01 — runtime browser time at the moment of approve/reject (AMD-94).
 */
const actionStamp = (): string => {
  const d = new Date()
  const pad = (n: number) => String(n).padStart(2, '0')
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}`
}

export const useTransactionStore = create<TransactionState>()(
  persist(
    (set, get) => ({
      items: [],
      isLoaded: false,
      seedFromFixtures: () => set({ items: fresh(), isLoaded: true }),
      reset: () => set({ items: fresh(), isLoaded: true }),
      approve: (id, actor) => {
        const txn = get().items.find((t) => t.Id === id)
        if (!txn) return { ok: false, reason: 'not-found' }
        if (txn.Status !== 'Imported') return { ok: false, reason: 'not-imported' }
        set({
          items: get().items.map((t) =>
            t.Id === id
              ? { ...t, Status: 'Approved' as const, ActionedBy: actor, ActionedAt: actionStamp() }
              : t,
          ),
        })
        return { ok: true }
      },
      reject: (id, note, actor) => {
        const txn = get().items.find((t) => t.Id === id)
        if (!txn) return { ok: false, reason: 'not-found' }
        if (txn.Status !== 'Imported') return { ok: false, reason: 'not-imported' }
        if (!note || !note.trim()) return { ok: false, reason: 'note-required' }
        set({
          items: get().items.map((t) =>
            t.Id === id
              ? {
                  ...t,
                  Status: 'Rejected' as const,
                  UserNote: note.trim(),
                  ActionedBy: actor,
                  ActionedAt: actionStamp(),
                }
              : t,
          ),
        })
        return { ok: true }
      },
    }),
    {
      // Entity-scoped (shared across prototypes that use Transaction), not prototype-scoped.
      name: 'transactions',
      storage: createJSONStorage(() => localStorage),
      skipHydration: true,
      partialize: (s) => ({ items: s.items, isLoaded: s.isLoaded }),
    },
  ),
)
