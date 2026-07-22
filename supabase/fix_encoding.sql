-- Corregir tipografía / acentos (UTF-8) en cursos y sesión demo
-- Pegar en SQL Editor → Run

update public.cursos set
  titulo = E'Fisiolog\u00eda del Adulto Mayor',
  descripcion = E'Formaci\u00f3n cl\u00ednica para prescribir ejercicio con precisi\u00f3n fisiol\u00f3gica en personas mayores.'
where id = 'adulto-mayor';

update public.cursos set
  titulo = E'Pediatr\u00eda y Salud',
  descripcion = E'Formaci\u00f3n cl\u00ednica para prescribir ejercicio y actividad f\u00edsica en ni\u00f1os y adolescentes.'
where id = 'pediatria-salud';

update public.sesiones_vivo set
  titulo = E'Clase en vivo \u2014 Fisiolog\u00eda del Adulto Mayor'
where bbb_meeting_id = 'mf-adulto-mayor-demo-001';
