import { create } from 'zustand'
import { persist, createJSONStorage } from 'zustand/middleware'

import type { ExampleItem } from '@/types'

import exampleData from '@/data/fixtures/_example-data.json'

interface ExampleStoreState {
  items: ExampleItem[]
  isLoaded: boolean
}

interface ExampleStoreActions {
  addItem: (item: Omit<ExampleItem, 'id'>) => void
  updateItem: (id: string, updates: Partial<ExampleItem>) => void
  deleteItem: (id: string) => void
  seedFromFixtures: () => void
  reset: () => void
}

export const useExampleStore = create<ExampleStoreState & ExampleStoreActions>()(
  persist(
    (set, get) => ({
      items: [],
      isLoaded: false,

      /** Adds a new item with an auto-generated UUID. */
      addItem: (item) =>
        set((s) => ({
          items: [...s.items, { ...item, id: crypto.randomUUID() }],
        })),

      /** Updates an existing item by ID with partial field overrides. */
      updateItem: (id, updates) =>
        set((s) => ({
          items: s.items.map((i) => (i.id === id ? { ...i, ...updates } : i)),
        })),

      /** Removes an item by ID. */
      deleteItem: (id) =>
        set((s) => ({
          items: s.items.filter((i) => i.id !== id),
        })),

      /** Seeds store from fixture data if not already loaded. Idempotent. */
      seedFromFixtures: () => {
        if (!get().isLoaded) {
          set({ items: exampleData.items, isLoaded: true })
        }
      },

      /** Resets store to fixture data, overwriting any user changes. */
      reset: () => {
        set({ items: exampleData.items, isLoaded: true })
      },
    }),
    {
      name: 'example-store',
      storage: createJSONStorage(() => localStorage),
      skipHydration: true,
    },
  ),
)
