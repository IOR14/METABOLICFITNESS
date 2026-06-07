'use client'

import { useState, useEffect } from 'react'
import { Menu, X } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'

export default function Navbar() {
  const [isScrolled, setIsScrolled] = useState(false)
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false)

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 20)
    }
    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  const navLinks = [
    { name: 'Tratamiento Obesidad', href: '#tratamiento' },
    { name: 'Academia', href: '#academia' },
    { name: 'Blog', href: '#blog' },
  ]

  return (
    <nav
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 bg-nav-purple ${
        isScrolled
          ? 'shadow-lg shadow-purple-900/20'
          : ''
      }`}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-20">
          {/* Logo */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="flex items-center space-x-2"
          >
            <div className="flex items-center space-x-3">
              <img 
                src="/Logo MF.png" 
                alt="Metabolic Fitness Logo" 
                className="h-10 w-auto object-contain"
              />
              <span className="font-heading font-bold text-xl text-white hidden sm:block">
                METABOLIC FITNESS
              </span>
            </div>
          </motion.div>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-8">
            {navLinks.map((link) => (
              <a
                key={link.name}
                href={link.href}
                className="text-white/90 font-body font-medium hover:text-white transition-colors duration-200"
              >
                {link.name}
              </a>
            ))}
            <div className="flex items-center space-x-4">
              <a
                href="#portal"
                className="text-white/90 font-body font-medium hover:text-white transition-colors duration-200"
              >
                Portal Alumnos
              </a>
              <motion.a
                href="#evaluacion"
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="bg-white text-nav-purple px-6 py-2.5 rounded-md font-body font-semibold shadow-lg hover:shadow-xl hover:bg-white/90 transition-all duration-200"
              >
                Agendar Evaluación
              </motion.a>
            </div>
          </div>

          {/* Mobile Menu Button */}
          <button
            onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
            className="md:hidden text-white p-2 hover:bg-white/10 rounded-lg transition-colors"
            aria-label="Toggle menu"
          >
            {isMobileMenuOpen ? (
              <X className="w-6 h-6" />
            ) : (
              <Menu className="w-6 h-6" />
            )}
          </button>
        </div>
      </div>

      {/* Mobile Menu */}
      <AnimatePresence>
        {isMobileMenuOpen && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="md:hidden bg-nav-purple border-t border-white/10"
          >
            <div className="px-4 pt-4 pb-6 space-y-4">
              {navLinks.map((link) => (
                <a
                  key={link.name}
                  href={link.href}
                  onClick={() => setIsMobileMenuOpen(false)}
                  className="block text-white/90 font-body font-medium hover:text-white transition-colors duration-200 py-2"
                >
                  {link.name}
                </a>
              ))}
              <a
                href="#portal"
                onClick={() => setIsMobileMenuOpen(false)}
                className="block text-white/90 font-body font-medium hover:text-white transition-colors duration-200 py-2"
              >
                Portal Alumnos
              </a>
              <a
                href="#evaluacion"
                onClick={() => setIsMobileMenuOpen(false)}
                className="block bg-white text-nav-purple px-6 py-3 rounded-md font-body font-semibold text-center shadow-lg hover:bg-white/90 transition-colors"
              >
                Agendar Evaluación
              </a>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </nav>
  )
}
