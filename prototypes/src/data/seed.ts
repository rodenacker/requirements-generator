// Stores are registered here per-generation by prototype-generator (step-03).
// Mutations persist in-session only (PI-02); rehydrate is manual because stores use skipHydration.

import { useTransactionStore } from '@/stores/transaction-store'

/** Rehydrates + seeds (if empty) every registered store. Idempotent. */
export function seedAllStores(): void {
  void useTransactionStore.persist.rehydrate()
  const txns = useTransactionStore.getState()
  if (!txns.isLoaded || txns.items.length === 0) txns.seedFromFixtures()
}

/** Resets every registered store to fixture data (PI-02 data-reset in the chrome). */
export function resetAllStores(): void {
  useTransactionStore.getState().reset()
}
