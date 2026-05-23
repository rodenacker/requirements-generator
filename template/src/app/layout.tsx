'use client'

import './globals.css'

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en">
      <head>
        <title>Prototype</title>
        <meta name="description" content="Client prototype" />
      </head>
      <body className="antialiased">
        {children}
      </body>
    </html>
  )
}
