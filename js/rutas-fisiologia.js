/**
 * Catálogo — Rutas de Certificación en Ciencias Fisiológicas
 * Metabolic Fitness Academy
 */
window.MF_RUTAS = {
  brand: 'Metabolic Fitness',
  overview: {
    title: 'Resumen de las Rutas de Certificación en Fisiología',
    lead:
      'Las rutas de certificación y exámenes están diseñados para reconocer y validar el conocimiento de los profesionales, investigadores y estudiantes que analizan y comprenden los mecanismos funcionales del cuerpo humano. Ya seas biólogo, investigador, docente o profesional de las ciencias biomédicas, nuestras certificaciones destacan tu dominio teórico y analítico.',
    benefits: [
      'Construir confianza en tus capacidades de análisis funcional y biológico.',
      'Obtener una ventaja competitiva en tu carrera académica, científica o de laboratorio.',
      'Demostrar credibilidad ante colegas, comités científicos y centros de investigación.',
      'Ganar insignias digitales para compartir tus logros académicos con el mundo.'
    ],
    cta: 'Selecciona tu sistema biológico o área integrativa en el menú de la izquierda para explorar y comenzar tu viaje de certificación.'
  },
  sistemas: [
    {
      id: 'celular-molecular',
      grupo: 'sistemas',
      titulo: 'Fisiología Celular y Molecular',
      badge: 'Sistema',
      resumen: 'Membranas, señalización, transporte y metabolismo celular como base de toda función fisiológica.',
      audiencia: 'Estudiantes y profesionales de ciencias biomédicas, biología y fisiología.',
      duracionExamen: '90 min',
      preguntas: 35,
      aprobacion: '80%',
      modulos: [
        { id: 'cm1', titulo: 'Membrana celular y transporte', tipo: 'Micro-learning', duracion: '25 min', desc: 'Difusión, osmosis, canales y bombas.' },
        { id: 'cm2', titulo: 'Señalización intracelular', tipo: 'eLearning', duracion: '40 min', desc: 'Receptores, segundos mensajeros y cascadas.' },
        { id: 'cm3', titulo: 'Metabolismo energético celular', tipo: 'eLearning', duracion: '45 min', desc: 'Glucólisis, ciclo de Krebs y fosforilación oxidativa.' },
        { id: 'cm4', titulo: 'Evaluación del sistema', tipo: 'Examen', duracion: '90 min', desc: 'Validación de conocimientos del módulo celular-molecular.' }
      ]
    },
    {
      id: 'neurofisiologia',
      grupo: 'sistemas',
      titulo: 'Neurofisiología (Sistema Nervioso)',
      badge: 'Sistema',
      resumen: 'Potenciales de acción, sinapsis, integración neural y control motor/sensorial.',
      audiencia: 'Profesionales de la salud, kinesiólogos, fisiólogos y neurocientíficos en formación.',
      duracionExamen: '2 h',
      preguntas: 40,
      aprobacion: '80%',
      modulos: [
        { id: 'n1', titulo: 'Potencial de membrana y de acción', tipo: 'eLearning', duracion: '40 min', desc: 'Canales iónicos y propagación del impulso.' },
        { id: 'n2', titulo: 'Sinapsis y neurotransmisores', tipo: 'eLearning', duracion: '35 min', desc: 'Transmisión química y plasticidad.' },
        { id: 'n3', titulo: 'Integración sensoriomotora', tipo: 'Caso clínico', duracion: '50 min', desc: 'Reflejos, control motor y percepción.' },
        { id: 'n4', titulo: 'Examen de certificación', tipo: 'Examen', duracion: '2 h', desc: 'Evaluación final de neurofisiología.' }
      ]
    },
    {
      id: 'cardiovascular',
      grupo: 'sistemas',
      titulo: 'Sistema Cardiovascular',
      badge: 'Sistema',
      resumen: 'Electrofisiología cardíaca, hemodinámica, regulación de la presión y adaptación al ejercicio.',
      audiencia: 'Clínicos del ejercicio, cardiólogos en formación, fisiólogos y kinesiólogos.',
      duracionExamen: '2 h',
      preguntas: 40,
      aprobacion: '80%',
      modulos: [
        { id: 'c1', titulo: 'Anatomía funcional del corazón', tipo: 'Micro-learning', duracion: '20 min', desc: 'Cámaras, válvulas y circulación coronaria.' },
        { id: 'c2', titulo: 'Electrofisiología y ECG básico', tipo: 'eLearning', duracion: '45 min', desc: 'Nodo SA/AV, ondas y ritmo.' },
        { id: 'c3', titulo: 'Hemodinámica y gasto cardíaco', tipo: 'eLearning', duracion: '40 min', desc: 'Precarga, poscarga y regulación.' },
        { id: 'c4', titulo: 'Cardiovascular en el ejercicio', tipo: 'Caso clínico', duracion: '50 min', desc: 'Respuestas agudas y crónicas al entrenamiento.' },
        { id: 'c5', titulo: 'Examen de certificación', tipo: 'Examen', duracion: '2 h', desc: 'Evaluación final del sistema cardiovascular.' }
      ]
    },
    {
      id: 'respiratorio',
      grupo: 'sistemas',
      titulo: 'Sistema Respiratorio',
      badge: 'Sistema',
      resumen: 'Mecánica ventilatoria, intercambio gaseoso, control neural y respuesta al ejercicio.',
      audiencia: 'Fisiólogos, terapeutas respiratorios y profesionales del ejercicio clínico.',
      duracionExamen: '90 min',
      preguntas: 35,
      aprobacion: '80%',
      modulos: [
        { id: 'r1', titulo: 'Mecánica de la ventilación', tipo: 'eLearning', duracion: '35 min', desc: 'Volúmenes, compliance y resistencia.' },
        { id: 'r2', titulo: 'Intercambio gaseoso', tipo: 'eLearning', duracion: '40 min', desc: 'Difusión, V/Q y transporte de O₂/CO₂.' },
        { id: 'r3', titulo: 'Control de la respiración', tipo: 'Micro-learning', duracion: '25 min', desc: 'Quimiorreceptores y centros respiratorios.' },
        { id: 'r4', titulo: 'Examen de certificación', tipo: 'Examen', duracion: '90 min', desc: 'Evaluación final respiratoria.' }
      ]
    },
    {
      id: 'endocrino',
      grupo: 'sistemas',
      titulo: 'Sistema Endocrino',
      badge: 'Sistema',
      resumen: 'Ejes hormonales, feedback y regulación del metabolismo y el crecimiento.',
      audiencia: 'Profesionales biomédicos, nutrición clínica y fisiología del ejercicio.',
      duracionExamen: '90 min',
      preguntas: 35,
      aprobacion: '80%',
      modulos: [
        { id: 'e1', titulo: 'Principios de endocrinología', tipo: 'Micro-learning', duracion: '20 min', desc: 'Hormonas, receptores y feedback.' },
        { id: 'e2', titulo: 'Eje hipotálamo-hipófisis', tipo: 'eLearning', duracion: '40 min', desc: 'Regulación central y periferia.' },
        { id: 'e3', titulo: 'Metabolismo y hormonas', tipo: 'eLearning', duracion: '45 min', desc: 'Insulina, glucagón, cortisol y tiroides.' },
        { id: 'e4', titulo: 'Examen de certificación', tipo: 'Examen', duracion: '90 min', desc: 'Evaluación final endocrina.' }
      ]
    },
    {
      id: 'renal',
      grupo: 'sistemas',
      titulo: 'Sistema Renal y Fluidos',
      badge: 'Sistema',
      resumen: 'Filtración, reabsorción, balance hidroelectrolítico y regulación ácido-base.',
      audiencia: 'Estudiantes de medicina, enfermería y ciencias fisiológicas.',
      duracionExamen: '90 min',
      preguntas: 35,
      aprobacion: '80%',
      modulos: [
        { id: 'k1', titulo: 'Nefrón y filtración glomerular', tipo: 'eLearning', duracion: '40 min', desc: 'TFG, clearances y autorregulación.' },
        { id: 'k2', titulo: 'Balance de agua y electrolitos', tipo: 'eLearning', duracion: '40 min', desc: 'ADH, aldosterona y volumen.' },
        { id: 'k3', titulo: 'Ácido-base renal', tipo: 'Caso clínico', duracion: '35 min', desc: 'Compensaciones metabólicas y respiratorias.' },
        { id: 'k4', titulo: 'Examen de certificación', tipo: 'Examen', duracion: '90 min', desc: 'Evaluación final renal.' }
      ]
    },
    {
      id: 'gastrointestinal',
      grupo: 'sistemas',
      titulo: 'Sistema Gastrointestinal',
      badge: 'Sistema',
      resumen: 'Motilidad, secreción, absorción y regulación neuroendocrina digestiva.',
      audiencia: 'Profesionales de nutrición, gastroenterología y fisiología.',
      duracionExamen: '90 min',
      preguntas: 30,
      aprobacion: '80%',
      modulos: [
        { id: 'g1', titulo: 'Motilidad y secreción', tipo: 'eLearning', duracion: '35 min', desc: 'Peristalsis, enzimas y jugos digestivos.' },
        { id: 'g2', titulo: 'Absorción de nutrientes', tipo: 'eLearning', duracion: '40 min', desc: 'CHO, lípidos, proteínas y micronutrientes.' },
        { id: 'g3', titulo: 'Examen de certificación', tipo: 'Examen', duracion: '90 min', desc: 'Evaluación final GI.' }
      ]
    },
    {
      id: 'inmunologico',
      grupo: 'sistemas',
      titulo: 'Sistema Inmunológico',
      badge: 'Sistema',
      resumen: 'Inmunidad innata y adaptativa, inflamación y respuesta al estrés fisiológico.',
      audiencia: 'Biomédicos, clínicos e investigadores en inmunofisiología.',
      duracionExamen: '90 min',
      preguntas: 35,
      aprobacion: '80%',
      modulos: [
        { id: 'i1', titulo: 'Inmunidad innata', tipo: 'Micro-learning', duracion: '25 min', desc: 'Barreras, inflamación y fagocitosis.' },
        { id: 'i2', titulo: 'Inmunidad adaptativa', tipo: 'eLearning', duracion: '45 min', desc: 'Linfocitos, anticuerpos y memoria.' },
        { id: 'i3', titulo: 'Examen de certificación', tipo: 'Examen', duracion: '90 min', desc: 'Evaluación final inmunológica.' }
      ]
    }
  ],
  integrativa: [
    {
      id: 'metabolismo-energetico',
      grupo: 'integrativa',
      titulo: 'Metabolismo Energético y Bioquímica',
      badge: 'Integrativa',
      resumen: 'Integración de vías metabólicas, sustratos energéticos y control hormonal del gasto.',
      audiencia: 'Fisiólogos del ejercicio, nutrición clínica e investigación metabólica.',
      duracionExamen: '2 h',
      preguntas: 40,
      aprobacion: '80%',
      modulos: [
        { id: 'me1', titulo: 'Sustratos y vías energéticas', tipo: 'eLearning', duracion: '45 min', desc: 'CHO, lípidos y proteínas en reposo y ejercicio.' },
        { id: 'me2', titulo: 'Regulación hormonal del metabolismo', tipo: 'eLearning', duracion: '40 min', desc: 'Insulina, catecolaminas y cortisol.' },
        { id: 'me3', titulo: 'Casos de gasto energético', tipo: 'Caso clínico', duracion: '50 min', desc: 'Aplicación clínica y de laboratorio.' },
        { id: 'me4', titulo: 'Examen de certificación', tipo: 'Examen', duracion: '2 h', desc: 'Evaluación final de metabolismo energético.' }
      ]
    },
    {
      id: 'estres-adaptacion',
      grupo: 'integrativa',
      titulo: 'Fisiología del Estrés y Adaptación',
      badge: 'Integrativa',
      resumen: 'Respuestas alostáticas, ejes del estrés y adaptación al entrenamiento y la enfermedad.',
      audiencia: 'Clínicos, investigadores y docentes en fisiología del estrés.',
      duracionExamen: '90 min',
      preguntas: 35,
      aprobacion: '80%',
      modulos: [
        { id: 'ea1', titulo: 'Ejes del estrés', tipo: 'eLearning', duracion: '40 min', desc: 'HPA, SAM y mediadores inflamatorios.' },
        { id: 'ea2', titulo: 'Adaptación y sobrecarga', tipo: 'Caso clínico', duracion: '45 min', desc: 'Hormesis, recuperación y burnout fisiológico.' },
        { id: 'ea3', titulo: 'Examen de certificación', tipo: 'Examen', duracion: '90 min', desc: 'Evaluación final.' }
      ]
    },
    {
      id: 'neuroendocrinologia',
      grupo: 'integrativa',
      titulo: 'Neuroendocrinología Integrada',
      badge: 'Integrativa',
      resumen: 'Interfase cerebro-hormonas: ritmo, conducta, metabolismo y reproducción.',
      audiencia: 'Especialistas en endocrinología, neurociencias y fisiología.',
      duracionExamen: '90 min',
      preguntas: 35,
      aprobacion: '80%',
      modulos: [
        { id: 'ne1', titulo: 'Ejes neuroendocrinos', tipo: 'eLearning', duracion: '40 min', desc: 'Integración central y periférica.' },
        { id: 'ne2', titulo: 'Examen de certificación', tipo: 'Examen', duracion: '90 min', desc: 'Evaluación final.' }
      ]
    },
    {
      id: 'cronobiologia',
      grupo: 'integrativa',
      titulo: 'Cronobiología y Ritmos Circadianos',
      badge: 'Integrativa',
      resumen: 'Relojes biológicos, sueño, metabolismo y rendimiento a lo largo del día.',
      audiencia: 'Investigadores, clínicos del sueño y fisiólogos del rendimiento.',
      duracionExamen: '75 min',
      preguntas: 30,
      aprobacion: '80%',
      modulos: [
        { id: 'cr1', titulo: 'Reloj molecular y SCN', tipo: 'Micro-learning', duracion: '25 min', desc: 'Genes reloj y sincronizadores.' },
        { id: 'cr2', titulo: 'Ritmos y metabolismo', tipo: 'eLearning', duracion: '40 min', desc: 'Alimentación, ejercicio y jet lag fisiológico.' },
        { id: 'cr3', titulo: 'Examen de certificación', tipo: 'Examen', duracion: '75 min', desc: 'Evaluación final.' }
      ]
    },
    {
      id: 'fisiologia-ambiental',
      grupo: 'integrativa',
      titulo: 'Fisiología Ambiental (Altitud, Temperatura)',
      badge: 'Integrativa',
      resumen: 'Adaptaciones a hipoxia, calor, frío y estrés ambiental extremo.',
      audiencia: 'Medicina deportiva, expediciones y fisiología aplicada.',
      duracionExamen: '90 min',
      preguntas: 35,
      aprobacion: '80%',
      modulos: [
        { id: 'fa1', titulo: 'Altitud e hipoxia', tipo: 'eLearning', duracion: '40 min', desc: 'Aclimatación y eritropoyesis.' },
        { id: 'fa2', titulo: 'Termorregulación', tipo: 'eLearning', duracion: '35 min', desc: 'Calor, frío y balance térmico.' },
        { id: 'fa3', titulo: 'Examen de certificación', tipo: 'Examen', duracion: '90 min', desc: 'Evaluación final.' }
      ]
    },
    {
      id: 'acido-base',
      grupo: 'integrativa',
      titulo: 'Regulación del Equilibrio Ácido-Base',
      badge: 'Integrativa',
      resumen: 'Buffers, compensación respiratoria/renal e interpretación clínico-fisiológica.',
      audiencia: 'Clínicos, laboratoristas y estudiantes avanzados de fisiología.',
      duracionExamen: '75 min',
      preguntas: 30,
      aprobacion: '80%',
      modulos: [
        { id: 'ab1', titulo: 'Buffers y pH', tipo: 'Micro-learning', duracion: '20 min', desc: 'Sistemas amortiguadores.' },
        { id: 'ab2', titulo: 'Compensaciones y casos', tipo: 'Caso clínico', duracion: '45 min', desc: 'Acidosis/alcalosis metabólica y respiratoria.' },
        { id: 'ab3', titulo: 'Examen de certificación', tipo: 'Examen', duracion: '75 min', desc: 'Evaluación final.' }
      ]
    }
  ]
};

window.MF_RUTAS.all = function () {
  return [].concat(window.MF_RUTAS.sistemas, window.MF_RUTAS.integrativa);
};

window.MF_RUTAS.byId = function (id) {
  return window.MF_RUTAS.all().find(function (r) { return r.id === id; }) || null;
};

window.MF_RUTAS.progressKey = function (rutaId) {
  return 'mf_ruta_progress_' + rutaId;
};

window.MF_RUTAS.getProgress = function (rutaId) {
  try {
    return JSON.parse(localStorage.getItem(window.MF_RUTAS.progressKey(rutaId)) || '{"done":[]}');
  } catch (e) {
    return { done: [] };
  }
};

window.MF_RUTAS.setProgress = function (rutaId, data) {
  localStorage.setItem(window.MF_RUTAS.progressKey(rutaId), JSON.stringify(data));
};

window.MF_RUTAS.markDone = function (rutaId, moduloId) {
  var p = window.MF_RUTAS.getProgress(rutaId);
  if (p.done.indexOf(moduloId) === -1) p.done.push(moduloId);
  window.MF_RUTAS.setProgress(rutaId, p);
  return p;
};

window.MF_RUTAS.isComplete = function (ruta) {
  var p = window.MF_RUTAS.getProgress(ruta.id);
  return ruta.modulos.every(function (m) { return p.done.indexOf(m.id) !== -1; });
};

/**
 * Acceso a learning paths:
 * - Cualquier inscripción activa a unlockAllCursos abre TODAS las rutas (alumno pagado / suscrito).
 * - O inscripción al curso específico de esa ruta (venta individual).
 */
window.MF_RUTAS.access = {
  unlockAllCursos: ['adulto-mayor', 'pediatria-salud', 'rutas-fisiologia'],
  buyUrl: 'academia.html',
  portalUrl: 'portal.html',
  aulaRutasUrl: 'aula.html#rutas'
};

/** Curso de producto asociado a una ruta (para venta específica) */
window.MF_RUTAS.cursoIdFor = function (rutaId) {
  return 'ruta-' + rutaId;
};

window.MF_RUTAS.all().forEach(function (r) {
  if (!r.cursoId) r.cursoId = window.MF_RUTAS.cursoIdFor(r.id);
});
