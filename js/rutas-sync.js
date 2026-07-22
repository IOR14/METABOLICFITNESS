/**
 * Sync progreso / certificados de rutas → Supabase
 * Fallback: localStorage (MF_RUTAS) si no hay sesión.
 */
(function (w) {
  if (!w.MF_RUTAS) return;

  var client = null;
  var user = null;
  var ready = null;

  function getClient() {
    if (client) return client;
    if (typeof w.createMFClient === 'function') {
      try { client = w.createMFClient(); } catch (e) { client = null; }
    }
    return client;
  }

  MF_RUTAS.authReady = function () {
    if (ready) return ready;
    ready = new Promise(function (resolve) {
      var c = getClient();
      if (!c) {
        resolve(null);
        return;
      }
      c.auth.getSession().then(function (res) {
        user = (res.data && res.data.session && res.data.session.user) || null;
        resolve(user);
      }).catch(function () {
        resolve(null);
      });
    });
    return ready;
  };

  MF_RUTAS.currentUser = function () { return user; };

  function mergeDone(a, b) {
    var set = {};
    (a || []).concat(b || []).forEach(function (id) { set[id] = true; });
    return Object.keys(set);
  }

  /** Carga remoto + une con local; guarda el resultado en localStorage */
  MF_RUTAS.hydrateFromCloud = async function (rutaId) {
    await MF_RUTAS.authReady();
    var local = MF_RUTAS.getProgress(rutaId);
    if (!user || !getClient()) return local;

    var { data, error } = await client
      .from('ruta_progreso')
      .select('done_modulos')
      .eq('user_id', user.id)
      .eq('ruta_id', rutaId)
      .maybeSingle();

    if (error) {
      console.warn('[MF_RUTAS] hydrate progreso:', error.message);
      return local;
    }

    var remoteDone = (data && data.done_modulos) || [];
    if (typeof remoteDone === 'string') {
      try { remoteDone = JSON.parse(remoteDone); } catch (e) { remoteDone = []; }
    }

    var merged = {
      done: mergeDone(local.done, remoteDone),
      certificate: local.certificate || null
    };

    var { data: cert } = await client
      .from('ruta_certificados')
      .select('codigo, nombre_display, titulo_ruta, completed_at')
      .eq('user_id', user.id)
      .eq('ruta_id', rutaId)
      .maybeSingle();

    if (cert) {
      merged.certificate = {
        code: cert.codigo,
        name: cert.nombre_display,
        course: cert.titulo_ruta,
        date: cert.completed_at
          ? new Date(cert.completed_at).toLocaleDateString('es-CL')
          : (local.certificate && local.certificate.date) || ''
      };
    }

    MF_RUTAS.setProgress(rutaId, merged);
    return merged;
  };

  MF_RUTAS.syncProgress = async function (rutaId) {
    await MF_RUTAS.authReady();
    if (!user || !getClient()) return { ok: false, reason: 'no-session' };

    var p = MF_RUTAS.getProgress(rutaId);
    var { error } = await client.from('ruta_progreso').upsert(
      {
        user_id: user.id,
        ruta_id: rutaId,
        done_modulos: p.done || [],
        updated_at: new Date().toISOString()
      },
      { onConflict: 'user_id,ruta_id' }
    );

    if (error) {
      console.warn('[MF_RUTAS] sync progreso:', error.message);
      return { ok: false, error: error.message };
    }
    return { ok: true };
  };

  MF_RUTAS.syncCertificate = async function (rutaId, cert) {
    await MF_RUTAS.authReady();
    if (!user || !getClient() || !cert) return { ok: false, reason: 'no-session' };

    var { error } = await client.from('ruta_certificados').upsert(
      {
        user_id: user.id,
        ruta_id: rutaId,
        codigo: cert.code,
        nombre_display: cert.name,
        titulo_ruta: cert.course,
        completed_at: new Date().toISOString()
      },
      { onConflict: 'user_id,ruta_id' }
    );

    if (error) {
      console.warn('[MF_RUTAS] sync certificado:', error.message);
      return { ok: false, error: error.message };
    }
    return { ok: true };
  };

  MF_RUTAS.listMyCertificates = async function () {
    await MF_RUTAS.authReady();
    if (!user || !getClient()) return [];
    var { data, error } = await client
      .from('ruta_certificados')
      .select('ruta_id, codigo, nombre_display, titulo_ruta, completed_at')
      .eq('user_id', user.id)
      .order('completed_at', { ascending: false });
    if (error) {
      console.warn('[MF_RUTAS] list certificados:', error.message);
      return [];
    }
    return data || [];
  };

  MF_RUTAS.validarCodigo = async function (codigo) {
    var c = getClient();
    if (!c) return null;
    var { data, error } = await c.rpc('validar_certificado_ruta', { p_codigo: codigo });
    if (error) {
      console.warn('[MF_RUTAS] validar:', error.message);
      return null;
    }
    return (data && data[0]) || null;
  };

  /** Lista de curso_id con inscripción activa */
  MF_RUTAS.getEnrolledCourseIds = async function () {
    await MF_RUTAS.authReady();
    if (!user || !getClient()) return [];
    var { data, error } = await client
      .from('inscripciones')
      .select('curso_id')
      .eq('user_id', user.id)
      .eq('estado', 'activo');
    if (error) {
      console.warn('[MF_RUTAS] inscripciones:', error.message);
      return [];
    }
    return (data || []).map(function (r) { return r.curso_id; });
  };

  /**
   * @returns {{ ok: boolean, reason: string, enrolled: string[], unlockAll: boolean }}
   * reason: 'ok' | 'no-session' | 'no-enrollment'
   */
  MF_RUTAS.checkAccess = async function (rutaId, enrolledOverride) {
    await MF_RUTAS.authReady();
    if (!user && !(enrolledOverride && enrolledOverride.length)) {
      return { ok: false, reason: 'no-session', enrolled: [], unlockAll: false };
    }
    var enrolled = Array.isArray(enrolledOverride)
      ? enrolledOverride.slice()
      : await MF_RUTAS.getEnrolledCourseIds();
    var unlockList = (MF_RUTAS.access && MF_RUTAS.access.unlockAllCursos) || [];
    var anyUnlocks = !!(MF_RUTAS.access && MF_RUTAS.access.anyActiveEnrollmentUnlocksAll);
    var unlockAll =
      (anyUnlocks && enrolled.length > 0) ||
      enrolled.some(function (id) { return unlockList.indexOf(id) !== -1; });
    if (unlockAll) {
      return { ok: true, reason: 'ok', enrolled: enrolled, unlockAll: true };
    }
    var ruta = rutaId ? MF_RUTAS.byId(rutaId) : null;
    var specific = ruta && ruta.cursoId ? ruta.cursoId : (rutaId ? MF_RUTAS.cursoIdFor(rutaId) : null);
    if (specific && enrolled.indexOf(specific) !== -1) {
      return { ok: true, reason: 'ok', enrolled: enrolled, unlockAll: false };
    }
    if (!rutaId) {
      var anySpecific = MF_RUTAS.all().some(function (r) {
        return enrolled.indexOf(r.cursoId || MF_RUTAS.cursoIdFor(r.id)) !== -1;
      });
      if (anySpecific) {
        return { ok: true, reason: 'ok', enrolled: enrolled, unlockAll: false };
      }
    }
    return { ok: false, reason: 'no-enrollment', enrolled: enrolled, unlockAll: false };
  };

  MF_RUTAS.canAccessRuta = async function (rutaId) {
    var a = await MF_RUTAS.checkAccess(rutaId);
    return a.ok;
  };
})(window);
