import Link from 'next/link'

import { PROTOTYPES, type PrototypeEntry } from '@/data/prototype-registry'

export default function Home() {
  if (PROTOTYPES.length === 0) {
    return (
      <div className="mx-auto max-w-2xl p-8 text-center">
        <h1 className="text-2xl font-semibold tracking-tight">No prototypes yet</h1>
        <p className="mt-2 text-muted-foreground">
          Run <code className="rounded bg-secondary px-1">/prototype</code> to generate one.
          Prototypes appear here, grouped by the part of the requirement they explore.
        </p>
      </div>
    )
  }

  const byScope = new Map<string, PrototypeEntry[]>()
  for (const p of PROTOTYPES) {
    const list = byScope.get(p.scope_slug) ?? []
    list.push(p)
    byScope.set(p.scope_slug, list)
  }

  return (
    <div className="mx-auto max-w-5xl p-8">
      <h1 className="text-2xl font-semibold tracking-tight">Prototypes</h1>
      {[...byScope.entries()].map(([scope, list]) => (
        <section key={scope} className="mt-8">
          <h2 className="text-lg font-medium">{list[0]?.scope_label ?? scope}</h2>
          <ul className="mt-4 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {list.map((p) => (
              <li key={p.slug} className="rounded-lg border p-4">
                <div className="font-semibold">{p.name}</div>
                <div className="text-sm text-muted-foreground">{p.posture_label}</div>
                <div className="mt-2 flex flex-wrap gap-1">
                  {p.position_labels.map((label) => (
                    <span key={label} className="rounded bg-secondary px-2 py-0.5 text-xs">
                      {label}
                    </span>
                  ))}
                </div>
                <Link
                  href={p.route}
                  className="mt-3 inline-block text-sm font-medium text-primary underline-offset-4 hover:underline"
                >
                  Open →
                </Link>
              </li>
            ))}
          </ul>
        </section>
      ))}
    </div>
  )
}
