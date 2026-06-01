import { create } from 'zustand'

interface ProtoChromeState {
  /** The role currently selected in the prototype chrome (PI-05). Null = default/first role. */
  activeRole: string | null
  setActiveRole: (role: string | null) => void
}

/** Session-only chrome state (not persisted). Shared by every prototype's multi-role surfaces. */
export const useProtoChromeStore = create<ProtoChromeState>((set) => ({
  activeRole: null,
  setActiveRole: (role) => set({ activeRole: role }),
}))
