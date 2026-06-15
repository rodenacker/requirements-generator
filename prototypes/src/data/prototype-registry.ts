/**
 * The list of generated prototypes, regenerated additively by prototype-landing-updater
 * from prototypes/.registry.json. Imported by the landing (src/app/page.tsx) and the
 * prototype chrome (PrototypeChrome.tsx). Empty until the first prototype is generated.
 */
export interface PrototypeEntry {
  name: string
  slug: string
  route: string
  scope_slug: string
  scope_label: string
  posture_label: string
  position_labels: string[]
  roles: string[]
  smoke_skipped?: boolean
}

export const PROTOTYPES: PrototypeEntry[] = [
  {
    name: 'Approval Queue — Dense',
    slug: 'approval-queue-dense',
    route: '/approval-queue-dense',
    scope_slug: 'approval-queue',
    scope_label: 'The approval queue with bulk-decision actions',
    posture_label: 'Analytical / Information-Dense',
    position_labels: ['Maximally dense'],
    roles: ['Importer', 'Approver'],
    smoke_skipped: false,
  },
]
