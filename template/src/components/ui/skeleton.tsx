import { cn } from "@/lib/utils"

/**
 * Loading placeholder. Use it to mirror the SHAPE of the content that is coming —
 * a skeleton row per table row, a skeleton block per card — never as a lone
 * spinner substitute. `ux-baseline-checklist.md` requires a skeleton matching the
 * data layout, and `GR-10` sets the thresholds (nothing under 300ms, skeleton
 * 300ms–3s, skeleton + message beyond 3s).
 *
 * The pulse is state feedback, not decoration, so it deliberately survives
 * `prefers-reduced-motion` (globals.css exempts in-flight indicators).
 */
function Skeleton({ className, ...props }: React.ComponentProps<"div">) {
  return (
    <div
      data-slot="skeleton"
      aria-hidden="true"
      className={cn("animate-pulse rounded-md bg-muted", className)}
      {...props}
    />
  )
}

export { Skeleton }
