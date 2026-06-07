import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Metabolic Fitness - Fisiología Clínica del Ejercicio',
  description: 'Plataforma líder mundial en Fisiología Clínica del Ejercicio. Tratamiento integral de la obesidad y academia profesional.',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="es">
      <body className="antialiased">{children}</body>
    </html>
  )
}
