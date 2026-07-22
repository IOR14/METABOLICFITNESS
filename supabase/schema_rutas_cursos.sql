-- Producto que desbloquea todas las Rutas de Certificación en Fisiología
-- + cursos individuales opcionales (venta por sistema)
-- Pegar en Supabase → SQL Editor → Run

insert into public.cursos (id, titulo, descripcion, precio_clp, precio_usd, activo)
values
  (
    'rutas-fisiologia',
    E'Rutas de Certificaci\u00f3n en Fisiolog\u00eda',
    E'Acceso a todas las learning paths de sistemas fisiol\u00f3gicos e integrativos en el Portal Alumnos.',
    130000,
    150,
    true
  )
on conflict (id) do update set
  titulo = excluded.titulo,
  descripcion = excluded.descripcion,
  precio_clp = excluded.precio_clp,
  precio_usd = excluded.precio_usd,
  activo = true;

-- Cursos individuales (opcionales). Se activan al vender una ruta suelta.
insert into public.cursos (id, titulo, descripcion, precio_clp, precio_usd, activo)
values
  ('ruta-celular-molecular', E'Ruta: Fisiolog\u00eda Celular y Molecular', E'Learning path individual.', 49000, 55, true),
  ('ruta-neurofisiologia', E'Ruta: Neurofisiolog\u00eda', E'Learning path individual.', 49000, 55, true),
  ('ruta-cardiovascular', E'Ruta: Sistema Cardiovascular', E'Learning path individual.', 49000, 55, true),
  ('ruta-respiratorio', E'Ruta: Sistema Respiratorio', E'Learning path individual.', 49000, 55, true),
  ('ruta-endocrino', E'Ruta: Sistema Endocrino', E'Learning path individual.', 49000, 55, true),
  ('ruta-renal', E'Ruta: Sistema Renal y Fluidos', E'Learning path individual.', 49000, 55, true),
  ('ruta-gastrointestinal', E'Ruta: Sistema Gastrointestinal', E'Learning path individual.', 49000, 55, true),
  ('ruta-inmunologico', E'Ruta: Sistema Inmunol\u00f3gico', E'Learning path individual.', 49000, 55, true),
  ('ruta-metabolismo-energetico', E'Ruta: Metabolismo Energ\u00e9tico', E'Learning path individual.', 49000, 55, true),
  ('ruta-estres-adaptacion', E'Ruta: Fisiolog\u00eda del Estr\u00e9s', E'Learning path individual.', 49000, 55, true),
  ('ruta-neuroendocrinologia', E'Ruta: Neuroendocrinolog\u00eda', E'Learning path individual.', 49000, 55, true),
  ('ruta-cronobiologia', E'Ruta: Cronobiolog\u00eda', E'Learning path individual.', 49000, 55, true),
  ('ruta-fisiologia-ambiental', E'Ruta: Fisiolog\u00eda Ambiental', E'Learning path individual.', 49000, 55, true),
  ('ruta-acido-base', E'Ruta: Equilibrio \u00c1cido-Base', E'Learning path individual.', 49000, 55, true)
on conflict (id) do update set
  titulo = excluded.titulo,
  descripcion = excluded.descripcion,
  activo = true;

-- Nota: alumnos con adulto-mayor o pediatria-salud ya desbloquean todas las rutas
-- (ver js/rutas-fisiologia.js → access.unlockAllCursos).
