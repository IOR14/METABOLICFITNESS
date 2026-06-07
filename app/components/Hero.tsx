'use client'

import { motion } from 'framer-motion'
import { ArrowRight, Activity, GraduationCap } from 'lucide-react'

export default function Hero() {
  return (
    <section className="relative min-h-screen flex items-center justify-center bg-gradient-to-br from-metabolic-bg via-metabolic-bg-secondary to-metabolic-bg pt-20 overflow-hidden">
      {/* Decorative Elements - Molecular Nodes */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-20 left-10 w-2 h-2 bg-metabolic-cyan rounded-full opacity-30"></div>
        <div className="absolute top-40 right-20 w-3 h-3 bg-metabolic-green rounded-full opacity-20"></div>
        <div className="absolute bottom-40 left-1/4 w-2 h-2 bg-metabolic-cyan rounded-full opacity-25"></div>
        <div className="absolute bottom-20 right-1/3 w-2.5 h-2.5 bg-metabolic-green rounded-full opacity-30"></div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 relative z-10">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          {/* Text Content */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="space-y-8"
          >
            <div className="space-y-4">
              <motion.h1
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8, delay: 0.2 }}
                className="font-heading font-extrabold text-4xl sm:text-5xl lg:text-6xl text-metabolic-charcoal uppercase leading-tight"
              >
                FISIOLOGÍA CLÍNICA
                <span className="block text-metabolic-green">DEL EJERCICIO</span>
              </motion.h1>

              <motion.p
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8, delay: 0.4 }}
                className="font-body text-lg sm:text-xl text-metabolic-charcoal/80 leading-relaxed max-w-2xl"
              >
                La integración rigurosa entre la ciencia médica más avanzada y el movimiento humano.
                Diseñamos intervenciones clínicas basadas en evidencia y formamos profesionales
                bajo los más altos estándares de la Fisiología Clínica del Ejercicio.
              </motion.p>
            </div>

            {/* Dual CTA Buttons */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.6 }}
              className="flex flex-col sm:flex-row gap-4 pt-4"
            >
              <motion.a
                href="#tratamiento"
                whileHover={{ scale: 1.05, y: -2 }}
                whileTap={{ scale: 0.95 }}
                className="group bg-metabolic-green text-white px-8 py-4 rounded-md font-body font-semibold text-lg shadow-lg hover:shadow-xl transition-all duration-300 flex items-center justify-center space-x-2"
              >
                <Activity className="w-5 h-5" />
                <span>Soy Paciente</span>
                <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
              </motion.a>

              <motion.a
                href="#academia"
                whileHover={{ scale: 1.05, y: -2 }}
                whileTap={{ scale: 0.95 }}
                className="group bg-white text-metabolic-charcoal border-2 border-metabolic-charcoal px-8 py-4 rounded-md font-body font-semibold text-lg shadow-md hover:shadow-lg hover:border-metabolic-green hover:text-metabolic-green transition-all duration-300 flex items-center justify-center space-x-2"
              >
                <GraduationCap className="w-5 h-5" />
                <span>Soy Profesional</span>
                <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
              </motion.a>
            </motion.div>
          </motion.div>

          {/* Visual Content */}
          <motion.div
            initial={{ opacity: 0, x: 30 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8, delay: 0.3 }}
            className="relative"
          >
            {/* Placeholder for Hero Image */}
            <div className="relative bg-gradient-to-br from-metabolic-green/10 to-metabolic-cyan/10 rounded-2xl p-8 lg:p-12 backdrop-blur-sm border border-white/50">
              <div className="aspect-square bg-white/60 rounded-xl flex items-center justify-center overflow-hidden shadow-2xl">
                {/* Placeholder - Replace with actual image */}
                <div className="w-full h-full bg-gradient-to-br from-metabolic-green/20 to-metabolic-cyan/20 flex items-center justify-center">
                  <div className="text-center space-y-4 p-8">
                    <Activity className="w-24 h-24 text-metabolic-green mx-auto" />
                    <p className="font-heading font-bold text-metabolic-charcoal text-xl">
                      Imagen Hero
                    </p>
                    <p className="font-body text-metabolic-charcoal/60">
                      Lifestyle deportivo/clínico
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </motion.div>
        </div>
      </div>

      {/* Scroll Indicator */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 1, delay: 1.2 }}
        className="absolute bottom-8 left-1/2 transform -translate-x-1/2"
      >
        <motion.div
          animate={{ y: [0, 10, 0] }}
          transition={{ duration: 1.5, repeat: Infinity }}
          className="w-6 h-10 border-2 border-metabolic-charcoal/30 rounded-full flex justify-center"
        >
          <motion.div
            animate={{ y: [0, 12, 0] }}
            transition={{ duration: 1.5, repeat: Infinity }}
            className="w-1.5 h-3 bg-metabolic-green rounded-full mt-2"
          />
        </motion.div>
      </motion.div>
    </section>
  )
}
