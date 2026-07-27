/**
 * Suscripción Rutas — precio estándar USD 25 / mes.
 * Por geolocalización (país) se ofrece moneda local cuando hay Price ID en Stripe;
 * si no, se cobra en USD 25 (inscripción disponible desde cualquier país).
 */
window.MF_CHECKOUT = {
  rutasSuscripcion: {
    id: 'rutas-fisiologia',
    nombre: 'Suscripción Rutas de Aprendizaje',
    periodo: 'mensual',
    /** Precio estándar mundial */
    precioUsd: 25,
    /**
     * Ofertas por país (ISO 3166-1 alpha-2).
     * amount: unidades menores Stripe (cents) EXCEPTO monedas de cero decimales (CLP, COP…).
     * amountMajor: valor “humano” para mostrar en UI.
     * stripeMoneda: clave que usa /crear-checkout-session (clp|usd|brl|mxn|…)
     */
    porPais: {
      CL: { currency: 'CLP', stripeMoneda: 'clp', amountMajor: 24000, label: 'Chile', nota: 'Precio local en pesos chilenos (equiv. ~USD 25).' },
      BR: { currency: 'BRL', stripeMoneda: 'brl', amountMajor: 140, label: 'Brasil', nota: 'Precio local en reales (equiv. ~USD 25).' },
      MX: { currency: 'MXN', stripeMoneda: 'mxn', amountMajor: 460, label: 'México', nota: 'Precio local en pesos mexicanos (equiv. ~USD 25).' },
      PE: { currency: 'PEN', stripeMoneda: 'pen', amountMajor: 95, label: 'Perú', nota: 'Precio local en soles (equiv. ~USD 25).' },
      CO: { currency: 'COP', stripeMoneda: 'cop', amountMajor: 105000, label: 'Colombia', nota: 'Precio local en pesos colombianos (equiv. ~USD 25).' },
      AR: { currency: 'USD', stripeMoneda: 'usd', amountMajor: 25, label: 'Argentina', nota: 'En Argentina cobramos en USD 25 por estabilidad cambiaria.' },
      US: { currency: 'USD', stripeMoneda: 'usd', amountMajor: 25, label: 'Estados Unidos', nota: 'Precio estándar USD 25 / mes.' },
      ES: { currency: 'EUR', stripeMoneda: 'eur', amountMajor: 23, label: 'España', nota: 'Precio local en euros (equiv. ~USD 25).' }
    },
    /** Fallback si el país no está en la lista */
    defaultOffer: { currency: 'USD', stripeMoneda: 'usd', amountMajor: 25, label: 'Internacional', nota: 'Precio estándar mundial: USD 25 / mes.' },
    lemon: { clp: '', usd: '', brl: '', mxn: '' },
    whatsapp:
      'https://wa.me/56910111167?text=' +
      encodeURIComponent(
        'Hola, quiero suscribirme a las Rutas de Aprendizaje de Metabolic Fitness (USD 25 / mes o precio local según mi país).'
      )
  }
};
