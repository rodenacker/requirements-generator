'use client'

import { ChevronLeft, ChevronRight } from 'lucide-react'

import { Button } from '@/components/ui/button'

/**
 * UI-only page navigation: Prev / Next (disabled at bounds) + "Page X of Y".
 * Carries no data-prop (it is a UI control, not a data binding).
 */
export function Pagination({
  page,
  pageCount,
  onPage,
}: {
  page: number
  pageCount: number
  onPage: (p: number) => void
}) {
  const total = Math.max(pageCount, 1)
  const current = Math.min(Math.max(page, 1), total)
  const atStart = current <= 1
  const atEnd = current >= total

  return (
    <nav
      className="flex items-center justify-end gap-2"
      aria-label="Transaction pages"
    >
      <Button
        variant="outline"
        size="sm"
        onClick={() => onPage(current - 1)}
        disabled={atStart}
        aria-label="Previous page"
      >
        <ChevronLeft aria-hidden="true" />
        Prev
      </Button>
      <span
        className="px-1 text-xs text-muted-foreground tabular-nums"
        aria-live="polite"
      >
        Page {current} of {total}
      </span>
      <Button
        variant="outline"
        size="sm"
        onClick={() => onPage(current + 1)}
        disabled={atEnd}
        aria-label="Next page"
      >
        Next
        <ChevronRight aria-hidden="true" />
      </Button>
    </nav>
  )
}
