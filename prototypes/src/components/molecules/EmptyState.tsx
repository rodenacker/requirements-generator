import type * as React from 'react'
import { AlertTriangle, Inbox } from 'lucide-react'

import { cn } from '@/lib/utils'

/**
 * Centered empty / error placeholder: icon + title + plain-language message + optional action.
 * Used for the no-results state (tone="empty") and the load-failure state (tone="error").
 */
export function EmptyState({
  title,
  message,
  action,
  tone = 'empty',
}: {
  title: string
  message: string
  action?: React.ReactNode
  tone?: 'empty' | 'error'
}) {
  const Icon = tone === 'error' ? AlertTriangle : Inbox
  return (
    <div
      className="flex flex-col items-center justify-center gap-3 rounded-md border border-dashed px-6 py-12 text-center"
      role={tone === 'error' ? 'alert' : 'status'}
    >
      <Icon
        aria-hidden="true"
        className={cn(
          'size-10',
          tone === 'error' ? 'text-destructive' : 'text-muted-foreground'
        )}
      />
      <div className="space-y-1">
        <p className="text-sm font-medium text-foreground">{title}</p>
        <p className="max-w-md text-sm text-muted-foreground">{message}</p>
      </div>
      {action ? <div className="mt-1">{action}</div> : null}
    </div>
  )
}
