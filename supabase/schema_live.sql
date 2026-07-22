-- Metabolic Fitness — Clases en vivo (BigBlueButton)
-- Ejecutar en Supabase → SQL Editor → Run
-- Requiere que schema.sql base ya esté aplicado (cursos, inscripciones, lecciones)

create table if not exists public.sesiones_vivo (
  id uuid primary key default gen_random_uuid(),
  curso_id text not null references public.cursos(id) on delete cascade,
  titulo text not null,
  bbb_meeting_id text not null unique,
  starts_at timestamptz,
  ends_at timestamptz,
  estado text not null default 'programada'
    check (estado in ('programada', 'en_vivo', 'finalizada', 'cancelada')),
  record boolean not null default true,
  recording_url text,
  recording_id text,
  moderator_pw text,
  attendee_pw text,
  created_at timestamptz not null default now()
);

create index if not exists sesiones_vivo_curso_idx on public.sesiones_vivo (curso_id);
create index if not exists sesiones_vivo_estado_idx on public.sesiones_vivo (estado);
create index if not exists sesiones_vivo_starts_idx on public.sesiones_vivo (starts_at desc);

-- Lecciones: permitir tipo 'vivo' (grabaciones / enlaces de clase)
do $$
begin
  alter table public.lecciones drop constraint if exists lecciones_tipo_check;
exception when undefined_object then
  null;
end $$;

alter table public.lecciones
  add constraint lecciones_tipo_check
  check (tipo in ('video', 'pdf', 'texto', 'link', 'vivo'));

-- Columna opcional para vincular lección ↔ sesión / recording BBB
alter table public.lecciones
  add column if not exists bbb_recording_id text;

alter table public.sesiones_vivo enable row level security;

-- Alumnos inscritos ven sesiones de sus cursos
drop policy if exists "sesiones_vivo_select_enrolled" on public.sesiones_vivo;
create policy "sesiones_vivo_select_enrolled" on public.sesiones_vivo
  for select to authenticated
  using (
    exists (
      select 1 from public.inscripciones i
      where i.user_id = auth.uid()
        and i.curso_id = sesiones_vivo.curso_id
        and i.estado = 'activo'
    )
  );

-- Admins (role=admin en profiles) pueden gestionar sesiones vía service role;
-- inserts/updates desde el dashboard usan service role o SQL Editor.
