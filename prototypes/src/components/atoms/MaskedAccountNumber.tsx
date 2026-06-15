import { cn } from '@/lib/utils'

/**
 * Renders an account number with all but the last four digits masked (F-13 / BR-07).
 * Presentational atom; the data-prop for Transaction.AccountNumber lives here on the
 * rendered value. The full number is never shown.
 *
 * Example: "6011329987654321" -> "•••• •••• •••• 4321".
 */
export function MaskedAccountNumber({
  value,
  className,
}: {
  value: string
  className?: string
}) {
  const masked = maskAccountNumber(value)
  return (
    <span
      className={cn('font-mono tabular-nums', className)}
      data-prop="Transaction.AccountNumber"
      title="Account number (masked)"
    >
      {masked}
    </span>
  )
}

function maskAccountNumber(value: string): string {
  const digits = (value ?? '').replace(/\D/g, '')
  if (digits.length === 0) return '••••'
  const last4 = digits.slice(-4)
  const hiddenCount = Math.max(digits.length - last4.length, 0)
  // Group the masked portion into blocks of four bullets to echo a card-number layout.
  const fullBullets = Math.floor(hiddenCount / 4)
  const remainder = hiddenCount % 4
  const groups: string[] = []
  for (let i = 0; i < fullBullets; i++) groups.push('••••')
  if (remainder > 0) groups.push('•'.repeat(remainder))
  groups.push(last4)
  return groups.join(' ')
}
