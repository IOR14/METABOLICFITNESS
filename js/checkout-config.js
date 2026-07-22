/**
 * Precios y checkouts — Suscripción Rutas de Aprendizaje
 * $20.000 CLP / mes  ≈  USD 22 / mes
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
    precioUsd: 22,
    /** Link Lemon (suscripción mensual). Vacío = se intenta /api/lemon-checkout/... */
    lemon: {
      clp: '',
      usd: ''
    },
    /** WhatsApp de respaldo si el checkout aún no está configurado */
    whatsapp:
      'https://wa.me/56910111167?text=' +
      encodeURIComponent(
        'Hola, quiero suscribirme a las Rutas de Aprendizaje de Metabolic Fitness ($20.000 CLP / mes o USD 22).'
      )
  }
};
