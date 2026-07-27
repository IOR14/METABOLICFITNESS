/**
 * Base URL del backend Flask (checkout + webhooks).
 * Producción (GitHub Pages): API en Vercel.
 * Local: mismo origen (Flask en :5000).
 */
(function () {
  var host = (window.location && window.location.hostname) || '';
  var isLocal = host === '127.0.0.1' || host === 'localhost';
  var PROD_API = 'https://metabolicfitness.vercel.app';

  if (typeof window.MF_API_BASE_OVERRIDE === 'string' && window.MF_API_BASE_OVERRIDE) {
    window.MF_API_BASE = window.MF_API_BASE_OVERRIDE.replace(/\/$/, '');
  } else if (isLocal) {
    window.MF_API_BASE = '';
  } else if (host.indexOf('metabolicfitness.cl') !== -1 || host.indexOf('github.io') !== -1) {
    window.MF_API_BASE = PROD_API;
  } else if (host.indexOf('vercel.app') !== -1) {
    window.MF_API_BASE = '';
  } else {
    window.MF_API_BASE = PROD_API;
  }

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

  window.mfBindCheckoutForms = function () {
    var action = window.mfCheckoutAction();
    document.querySelectorAll('form[data-mf-checkout]').forEach(function (f) {
      f.setAttribute('action', action);
    });
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', window.mfBindCheckoutForms);
  } else {
    window.mfBindCheckoutForms();
  }
})();
