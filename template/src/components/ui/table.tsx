"use client"

import * as React from "react"

import { cn } from "@/lib/utils"

function Table({ className, ...props }: React.ComponentProps<"table">) {
  return (
    // `overflow-x-auto` here is a desktop affordance for genuinely wide tables. It is
    // NOT permission to horizontally scroll a table at a narrow breakpoint: when a
    // prototype's device_targets include tablet/mobile, GR-18 requires the *generated*
    // component to render a card list below 768px instead of relying on this scroll.
    // See framework/assets/prototypes/visual-craft-standard.md §11.
    <div
      data-slot="table-container"
      className="relative w-full overflow-x-auto"
    >
      <table
        data-slot="table"
        className={cn("w-full caption-bottom text-sm", className)}
        {...props}
      />
    </div>
  )
}

function TableHeader({ className, ...props }: React.ComponentProps<"thead">) {
  return (
    <thead
      data-slot="table-header"
      className={cn("[&_tr]:border-b", className)}
      {...props}
    />
  )
}

function TableBody({ className, ...props }: React.ComponentProps<"tbody">) {
  return (
    <tbody
      data-slot="table-body"
      className={cn("[&_tr:last-child]:border-0", className)}
      {...props}
    />
  )
}

function TableFooter({ className, ...props }: React.ComponentProps<"tfoot">) {
  return (
    <tfoot
      data-slot="table-footer"
      className={cn(
        "border-t bg-muted/50 font-medium [&>tr]:last:border-b-0",
        className
      )}
      {...props}
    />
  )
}

function TableRow({ className, ...props }: React.ComponentProps<"tr">) {
  return (
    <tr
      data-slot="table-row"
      className={cn(
        // A row marked data-clickable gets the pointer + a firm press. The press is
        // an `accent` fill rather than a scale: scaling a `display: table-row` is
        // unreliable across engines, and `accent` is already one of the fill states
        // extract-brand-theme.md measures an on-colour against, so it costs the
        // contrast contract nothing. Applied in globals.css (visual-craft-standard.md §2).
        "border-b transition-colors hover:bg-muted/50 data-[state=selected]:bg-muted data-clickable:cursor-pointer",
        className
      )}
      {...props}
    />
  )
}

function TableHead({ className, ...props }: React.ComponentProps<"th">) {
  return (
    <th
      data-slot="table-head"
      className={cn(
        // data-numeric="true" right-aligns and (via globals.css) sets tabular-nums, so
        // digits align down the column — visual-craft-standard.md §6.
        "h-10 px-2 text-left align-middle font-medium whitespace-nowrap text-foreground data-[numeric=true]:text-right [&:has([role=checkbox])]:pr-0 [&>[role=checkbox]]:translate-y-[2px]",
        className
      )}
      {...props}
    />
  )
}

function TableCell({ className, ...props }: React.ComponentProps<"td">) {
  return (
    <td
      data-slot="table-cell"
      className={cn(
        "p-2 align-middle whitespace-nowrap data-[numeric=true]:text-right [&:has([role=checkbox])]:pr-0 [&>[role=checkbox]]:translate-y-[2px]",
        className
      )}
      {...props}
    />
  )
}

function TableCaption({
  className,
  ...props
}: React.ComponentProps<"caption">) {
  return (
    <caption
      data-slot="table-caption"
      className={cn("mt-4 text-sm text-muted-foreground", className)}
      {...props}
    />
  )
}

export {
  Table,
  TableHeader,
  TableBody,
  TableFooter,
  TableHead,
  TableRow,
  TableCell,
  TableCaption,
}
