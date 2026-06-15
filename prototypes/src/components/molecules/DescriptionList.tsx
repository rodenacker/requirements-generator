import * as React from 'react'

import { cn } from '@/lib/utils'

/**
 * Presentational two-column description list. The caller passes already-formatted
 * value nodes; this component does no data lookup. When an item carries `dataProp`,
 * it is stamped on that item's <dd> so the rendered Property value is traceable to
 * the §7 data shape (anti-fabrication contract). UI molecule: no client hooks.
 */
export interface DescriptionListItem {
  term: string
  value: React.ReactNode
  dataProp?: string
}

export function DescriptionList({ items }: { items: DescriptionListItem[] }) {
  return (
    <dl className={cn('grid grid-cols-[8rem_1fr] gap-x-4 gap-y-3 text-sm')}>
      {items.map((item, i) => (
        <React.Fragment key={`${item.term}-${i}`}>
          <dt className="text-muted-foreground">{item.term}</dt>
          <dd className="text-foreground" data-prop={item.dataProp}>
            {item.value}
          </dd>
        </React.Fragment>
      ))}
    </dl>
  )
}
