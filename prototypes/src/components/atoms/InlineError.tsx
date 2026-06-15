import * as React from 'react'
import { AlertTriangle } from 'lucide-react'

/**
 * Inline validation message. Announced via role="alert" (GR-16 / WCAG — not colour alone:
 * an AlertTriangle glyph accompanies the destructive text). Renders nothing when empty so
 * callers can mount it unconditionally and toggle by passing children.
 */
export function InlineError({
  children,
  id,
}: {
  children: React.ReactNode
  id?: string
}) {
  if (!children) return null
  return (
    <p
      role="alert"
      id={id}
      className="mt-1 flex items-center gap-1 text-sm text-destructive"
    >
      <AlertTriangle className="size-4 shrink-0" aria-hidden="true" />
      <span>{children}</span>
    </p>
  )
}
