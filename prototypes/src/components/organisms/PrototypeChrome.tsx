'use client'

import type { ReactNode } from 'react'

import Link from 'next/link'
import { usePathname } from 'next/navigation'

import { Button } from '@/components/ui/button'
import { PROTOTYPES } from '@/data/prototype-registry'
import { resetAllStores } from '@/data/seed'
import { useProtoChromeStore } from '@/stores/proto-chrome-store'

/**
 * The prototype review harness (PI-05, PI-08) — rendered OUTSIDE the app-under-design.
 * Carries no requirement bindings. Lets a reviewer navigate between prototypes, switch
 * the active role on multi-role surfaces, and reset fixture data.
 */
export function PrototypeChrome({ children }: { children: ReactNode }) {
  const pathname = usePathname()
  const active = PROTOTYPES.find(
    (p) => pathname === p.route || pathname.startsWith(`${p.route}/`),
  )
  const activeRole = useProtoChromeStore((s) => s.activeRole)
  const setActiveRole = useProtoChromeStore((s) => s.setActiveRole)

  return (
    <div className="min-h-screen">
      <header
        data-testid="proto-chrome"
        className="flex items-center gap-4 border-b bg-secondary px-4 py-2 text-sm"
      >
        <span className="rounded bg-primary px-2 py-0.5 text-xs font-semibold text-primary-foreground">
          PROTOTYPE
        </span>
        <Link href="/" className="font-medium hover:underline">
          Prototypes
        </Link>
        {active ? (
          <span className="text-muted-foreground">
            {active.name} · {active.posture_label}
          </span>
        ) : null}
        <div className="ml-auto flex items-center gap-2">
          {active && active.roles.length > 1 ? (
            <label className="flex items-center gap-1">
              <span className="text-muted-foreground">Role</span>
              <select
                className="rounded border bg-background px-2 py-1"
                value={activeRole ?? active.roles[0]}
                onChange={(e) => setActiveRole(e.target.value)}
              >
                {active.roles.map((r) => (
                  <option key={r} value={r}>
                    {r}
                  </option>
                ))}
              </select>
            </label>
          ) : null}
          <Button variant="outline" size="sm" onClick={() => resetAllStores()}>
            Reset data
          </Button>
        </div>
      </header>
      <main>{children}</main>
    </div>
  )
}
