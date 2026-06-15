import * as React from 'react'

import { cn } from '@/lib/utils'

/**
 * Styled multiline text input mirroring the shared Input look (border-input, shadow-xs,
 * focus ring, aria-invalid destructive state). Presentational atom: forwards all props,
 * carries no data-prop itself — the data-prop lives on the consuming element.
 */
export function Textarea({ className, ...props }: React.ComponentProps<'textarea'>) {
  return (
    <textarea
      data-slot="textarea"
      className={cn(
        'flex min-h-20 w-full rounded-md border border-input bg-transparent px-3 py-2 text-sm shadow-xs outline-none focus-visible:border-ring focus-visible:ring-[3px] focus-visible:ring-ring/50 aria-invalid:border-destructive aria-invalid:ring-destructive/20 disabled:opacity-50',
        className
      )}
      {...props}
    />
  )
}
