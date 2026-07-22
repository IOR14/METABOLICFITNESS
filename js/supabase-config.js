/**
 * Supabase client — Metabolic Fitness Portal
 * La clave publishable es segura en el navegador (protegida por RLS).
 */
window.MF_SUPABASE = {
  url: 'https://epvakbxseshjksfhoorl.supabase.co',
  anonKey: 'sb_publishable_aEZQwIDgn5blsYmWavBMRQ_nRVtDNE_',
  /** Edge Functions (producción). Fallback local: /api/live/... vía Flask */
  functionsUrl: 'https://epvakbxseshjksfhoorl.supabase.co/functions/v1',
  /**
   * Clases en vivo sin VPS: 'jitsi' usa meet.jit.si (open source, gratis).
   * Cuando tengas servidor propio: 'bbb' + BBB_URL/BBB_SECRET.
   */
  liveProvider: 'jitsi',
  jitsiDomain: 'meet.jit.si'
};

window.createMFClient = function () {
  if (!window.supabase || !window.supabase.createClient) {
    throw new Error('Supabase JS no cargó. Revisa la conexión a internet.');
  }
  return window.supabase.createClient(window.MF_SUPABASE.url, window.MF_SUPABASE.anonKey, {
    auth: {
      persistSession: true,
      autoRefreshToken: true,
      detectSessionInUrl: true
    }
  });
};
