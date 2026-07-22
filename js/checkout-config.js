/**
 * Precios y checkouts — Suscripción Rutas de Aprendizaje
 *
 * CLP: $20.000 / mes (precio local Chile)
 * USD: $25 / mes — no es conversión 1:1:
 *   incluye comisión de pasarela internacional (~5% + fee fijo),
 *   spread de conversión y un margen para que el neto se acerque a los $20.000 CLP.
 *
 * Lemon Squeezy: pega el link Share del producto recurrente en checkout.lemon.*
 * Stripe: price IDs vía Flask (.env) cuando esté disponible.
 */
window.MF_CHECKOUT = {
  rutasSuscripcion: {
    id: 'rutas-fisiologia',
    nombre: 'Suscripción Rutas de Aprendizaje',
    periodo: 'mensual',
    precioClp: 20000,
    precioUsd: 25,
    /** Explicación corta para la UI */
    notaUsd:
      'USD 25 incluye costo de pasarela y conversión internacional (en Chile el precio es $20.000 CLP/mes).',
    /** Link Lemon (suscripción mensual). Vacío = se intenta /api/lemon-checkout/... */
    lemon: {
      clp: '',
      usd: ''
    },
    /** WhatsApp de respaldo si el checkout aún no está configurado */
    whatsapp:
      'https://wa.me/56910111167?text=' +
      encodeURIComponent(
        'Hola, quiero suscribirme a las Rutas de Aprendizaje de Metabolic Fitness ($20.000 CLP / mes o USD 25 con pasarela internacional).'
      )
  }
};
