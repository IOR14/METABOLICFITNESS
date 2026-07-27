/**
 * Base URL del backend Flask (checkout + webhooks).
 * - Local / mismo origen (Vercel Flask): ''
 * - GitHub Pages + API aparte: define window.MF_API_BASE_OVERRIDE antes de este script
 *   o deja el fallback de producción abajo.
 */
(function () {
  if (typeof window.MF_API_BASE === 'string') return;

  var host = (window.location && window.location.hostname) || '';
  var isLocal = host === '127.0.0.1' || host === 'localhost';

  if (isLocal) {
    window.MF_API_BASE = '';
    return;
  }

  if (typeof window.MF_API_BASE_OVERRIDE === 'string') {
    window.MF_API_BASE = window.MF_API_BASE_OVERRIDE.replace(/\/$/, '');
    return;
  }

  // Mismo origen si el sitio ya corre sobre Flask (Vercel/Railway/Render).
  // Si sigues en GitHub Pages puro, pon la URL pública de la API aquí:
  // window.MF_API_BASE_OVERRIDE = 'https://TU-API.vercel.app';
  window.MF_API_BASE = '';
})();

window.mfCheckoutAction = function () {
  var base = (window.MF_API_BASE || '').replace(/\/$/, '');
  return base + '/crear-checkout-session';
};

window.mfApiUrl = function (path) {
  var base = (window.MF_API_BASE || '').replace(/\/$/, '');
  var p = path || '';
  if (p.charAt(0) !== '/') p = '/' + p;
  return base + p;
};
