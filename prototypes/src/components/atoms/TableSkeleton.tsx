/**
 * Loading-state placeholder for a table: a grid of pulsing skeleton cells.
 * Presentational, role-agnostic. The driver decides when to show it.
 */
export function TableSkeleton({
  rows = 8,
  cols = 7,
}: {
  rows?: number
  cols?: number
}) {
  const rowIdx = Array.from({ length: Math.max(rows, 0) })
  const colIdx = Array.from({ length: Math.max(cols, 0) })
  return (
    <div
      className="w-full overflow-hidden rounded-md border"
      role="status"
      aria-live="polite"
      aria-busy="true"
      aria-label="Loading transactions"
    >
      <div className="divide-y">
        {rowIdx.map((_, r) => (
          <div key={r} className="flex items-center gap-3 px-2 py-2">
            {colIdx.map((__, c) => (
              <div
                key={c}
                className="h-4 flex-1 animate-pulse rounded bg-muted"
              />
            ))}
          </div>
        ))}
      </div>
      <span className="sr-only">Loading transactions…</span>
    </div>
  )
}
