'use client'

import { Search } from 'lucide-react'

import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'

/**
 * Compact filter row for the transaction queue: free-text search + status select + clear.
 * UI-only controls — they filter the collection but bind to no data Property, so they
 * carry no data-prop attribute.
 */
export function SearchFilterBar({
  query,
  onQuery,
  status,
  onStatus,
  onClear,
}: {
  query: string
  onQuery: (v: string) => void
  status: string
  onStatus: (v: string) => void
  onClear: () => void
}) {
  return (
    <div className="flex flex-wrap items-center gap-2">
      <div className="relative min-w-[16rem] flex-1">
        <Search
          aria-hidden="true"
          className="pointer-events-none absolute top-1/2 left-2.5 size-4 -translate-y-1/2 text-muted-foreground"
        />
        <Input
          type="search"
          value={query}
          onChange={(e) => onQuery(e.target.value)}
          placeholder="Search reference, account, description…"
          aria-label="Search transactions"
          className="h-8 pl-8 text-sm"
        />
      </div>
      <Select value={status} onValueChange={onStatus}>
        <SelectTrigger size="sm" aria-label="Filter by status" className="w-40">
          <SelectValue placeholder="All statuses" />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="all">All statuses</SelectItem>
          <SelectItem value="Imported">Imported</SelectItem>
          <SelectItem value="Approved">Approved</SelectItem>
          <SelectItem value="Rejected">Rejected</SelectItem>
        </SelectContent>
      </Select>
      <Button variant="outline" size="sm" onClick={onClear}>
        Clear
      </Button>
    </div>
  )
}
