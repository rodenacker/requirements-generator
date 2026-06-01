'use client'

import { useEffect, type ReactNode } from 'react'

import './globals.css'
import { ErrorBoundary } from '@/components/ErrorBoundary'
import { PrototypeChrome } from '@/components/organisms/PrototypeChrome'
import { seedAllStores } from '@/data/seed'

export default function RootLayout({ children }: { children: ReactNode }) {
  useEffect(() => {
    seedAllStores()
  }, [])

  return (
    <html lang="en">
      <head>
        <title>Prototype</title>
        <meta name="description" content="Client prototypes" />
      </head>
      <body className="antialiased">
        <ErrorBoundary>
          <PrototypeChrome>{children}</PrototypeChrome>
        </ErrorBoundary>
      </body>
    </html>
  )
}
