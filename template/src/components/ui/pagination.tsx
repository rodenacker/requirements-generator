import * as React from "react"
import { type VariantProps } from "class-variance-authority"
import {
  ChevronLeftIcon,
  ChevronRightIcon,
  MoreHorizontalIcon,
} from "lucide-react"
import { Slot } from "radix-ui"

import { cn } from "@/lib/utils"
import { buttonVariants } from "@/components/ui/button"

/**
 * Pagination primitive.
 *
 * Why this ships with the template instead of being generated per run:
 * `design-system-standards.md §1 > Tables` requires a pagination footer on every data
 * table — even at one page — and `verify-prototype-build.md`'s per-route smoke asserts
 * the `role="navigation"` landmark below. Shipping the primitive makes that landmark
 * correct BY CONSTRUCTION rather than depending on eight parallel sub-agents each
 * remembering the same `aria-label`. Do not modify (shared-component-conventions.md §1).
 *
 * This is the primitive only: prev/next, numbered links, ellipsis. The page-size
 * selector (5/10/20/50, default 20) and the total record count that §1 also requires
 * are added by `molecules/Pagination`, which wraps this (§7.2 `navigation/pagination`).
 */

function Pagination({ className, ...props }: React.ComponentProps<"nav">) {
  return (
    <nav
      // role is redundant on <nav> for modern AT but is what the smoke queries, and
      // it costs nothing to be explicit. The accessible name is required by
      // design-system-standards.md §1 ("Pagination controls are reachable and labelled").
      role="navigation"
      aria-label="pagination"
      data-slot="pagination"
      className={cn("mx-auto flex w-full justify-center", className)}
      {...props}
    />
  )
}

function PaginationContent({ className, ...props }: React.ComponentProps<"ul">) {
  return (
    <ul
      data-slot="pagination-content"
      className={cn("flex flex-row items-center gap-1", className)}
      {...props}
    />
  )
}

function PaginationItem({ ...props }: React.ComponentProps<"li">) {
  return <li data-slot="pagination-item" {...props} />
}

// `buttonVariants` is a cva() function, not a component — its variant props come from
// VariantProps, NOT React.ComponentProps (which resolves to `never` here and fails tsc).
type PaginationLinkProps = {
  isActive?: boolean
  asChild?: boolean
} & Pick<VariantProps<typeof buttonVariants>, "size"> &
  React.ComponentProps<"a">

/**
 * `data-pressable` is not optional here. The global press layer in globals.css matches
 * `button`, `[role="button"]`, `summary`, the menu/tab/option roles and `[data-pressable]`
 * — it does NOT match a bare `<a>`. Without the attribute these controls would be the
 * one shipped primitive with no press response, failing visual-craft-standard.md §2.
 * `asChild` lets a caller substitute a real `<button>` (the usual choice in a
 * client-side prototype, where a page change is local state and not navigation).
 */
function PaginationLink({
  className,
  isActive,
  size = "icon",
  asChild = false,
  ...props
}: PaginationLinkProps) {
  const Comp = asChild ? Slot.Root : "a"

  return (
    <Comp
      aria-current={isActive ? "page" : undefined}
      data-slot="pagination-link"
      data-active={isActive}
      data-pressable=""
      className={cn(
        buttonVariants({ variant: isActive ? "outline" : "ghost", size }),
        "cursor-pointer",
        className
      )}
      {...props}
    />
  )
}

function PaginationPrevious({
  className,
  size = "default",
  ...props
}: React.ComponentProps<typeof PaginationLink>) {
  return (
    <PaginationLink
      aria-label="Go to previous page"
      size={size}
      className={cn("gap-1 px-2.5 sm:pl-2.5", className)}
      {...props}
    >
      <ChevronLeftIcon />
      {/* "Back", not "Previous": design-system-standards.md §1 names the two controls
          "Next" and "Back", and ux-baseline-checklist.md C2 restates that wording. */}
      <span className="hidden sm:block">Back</span>
    </PaginationLink>
  )
}

function PaginationNext({
  className,
  size = "default",
  ...props
}: React.ComponentProps<typeof PaginationLink>) {
  return (
    <PaginationLink
      aria-label="Go to next page"
      size={size}
      className={cn("gap-1 px-2.5 sm:pr-2.5", className)}
      {...props}
    >
      <span className="hidden sm:block">Next</span>
      <ChevronRightIcon />
    </PaginationLink>
  )
}

function PaginationEllipsis({
  className,
  ...props
}: React.ComponentProps<"span">) {
  return (
    <span
      aria-hidden
      data-slot="pagination-ellipsis"
      className={cn("flex size-9 items-center justify-center", className)}
      {...props}
    >
      {/* A real icon, never the "…" glyph — a text glyph ignores stroke weight and the
          type ramp and differs per platform (step-07 mechanical sweep, pattern 6). */}
      <MoreHorizontalIcon className="size-4" />
      <span className="sr-only">More pages</span>
    </span>
  )
}

export {
  Pagination,
  PaginationContent,
  PaginationLink,
  PaginationItem,
  PaginationPrevious,
  PaginationNext,
  PaginationEllipsis,
}
