import { Badge } from '@/components/ui/badge'
import { cn } from '@/lib/utils'

/**
 * Shared status chip. Status is conveyed by a glyph + text label in addition to colour
 * (GR-16 / WCAG 1.4.1 — never colour alone). UI atom: carries no data-prop; the data-prop
 * lives on the cell/element that renders the underlying Property value.
 */
export type StatusTone = 'neutral' | 'success' | 'danger' | 'info'

const toneClass: Record<StatusTone, string> = {
  neutral: 'border-border bg-muted text-foreground',
  success: 'border-green-300 bg-green-100 text-green-900',
  danger: 'border-red-300 bg-red-100 text-red-900',
  info: 'border-blue-300 bg-blue-100 text-blue-900',
}

const toneGlyph: Record<StatusTone, string> = {
  neutral: '•',
  success: '✓',
  danger: '✕',
  info: 'ℹ',
}

export function StatusBadge({
  label,
  tone = 'neutral',
  className,
}: {
  label: string
  tone?: StatusTone
  className?: string
}) {
  return (
    <Badge variant="outline" className={cn('gap-1', toneClass[tone], className)}>
      <span aria-hidden="true">{toneGlyph[tone]}</span>
      <span>{label}</span>
    </Badge>
  )
}
