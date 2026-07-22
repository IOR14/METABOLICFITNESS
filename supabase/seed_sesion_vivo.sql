-- Sesión de ejemplo (después de schema_live.sql)
-- Ajusta starts_at a tu horario local

insert into public.sesiones_vivo (
  curso_id,
  titulo,
  bbb_meeting_id,
  starts_at,
  estado,
  record,
  attendee_pw,
  moderator_pw
)
values (
  'adulto-mayor',
  E'Clase en vivo \u2014 Fisiolog\u00eda del Adulto Mayor',
  'mf-adulto-mayor-demo-001',
  now() + interval '1 hour',
  'programada',
  true,
  'ap',
  'mp'
)
on conflict (bbb_meeting_id) do update set
  titulo = excluded.titulo,
  starts_at = excluded.starts_at,
  estado = excluded.estado;
