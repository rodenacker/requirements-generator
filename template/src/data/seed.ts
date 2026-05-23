import { useExampleStore } from '@/stores'

/**
 * Seeds all stores from fixture data if not already loaded.
 * Call on app startup (e.g., in root layout useEffect).
 */
export function seedAllStores(): void {
  useExampleStore.persist.rehydrate()
  const { isLoaded, seedFromFixtures } = useExampleStore.getState()
  if (!isLoaded) {
    seedFromFixtures()
  }
}

/**
 * Resets all stores to fixture data.
 * Clears store state and re-seeds from fixtures.
 */
export function resetAllStores(): void {
  useExampleStore.getState().reset()
}
