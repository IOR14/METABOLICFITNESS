-- Metabolic Fitness — Rutas de Certificación (progreso + certificados)
-- Pegar en: Supabase → SQL Editor → New query → Run
-- Requiere que exista public.profiles (schema.sql)

create table if not exists public.ruta_progreso (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  ruta_id text not null,
  done_modulos jsonb not null default '[]'::jsonb,
  updated_at timestamptz not null default now(),
  unique (user_id, ruta_id)
);

create table if not exists public.ruta_certificados (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  ruta_id text not null,
  codigo text not null unique,
  nombre_display text not null,
  titulo_ruta text not null,
  completed_at timestamptz not null default now(),
  unique (user_id, ruta_id)
);

create index if not exists ruta_progreso_user_idx on public.ruta_progreso (user_id);
create index if not exists ruta_certificados_user_idx on public.ruta_certificados (user_id);
create index if not exists ruta_certificados_codigo_idx on public.ruta_certificados (codigo);

alter table public.ruta_progreso enable row level security;
alter table public.ruta_certificados enable row level security;

-- Progreso: solo el dueño
drop policy if exists "ruta_progreso_select_own" on public.ruta_progreso;
create policy "ruta_progreso_select_own" on public.ruta_progreso
  for select to authenticated using (auth.uid() = user_id);

drop policy if exists "ruta_progreso_insert_own" on public.ruta_progreso;
create policy "ruta_progreso_insert_own" on public.ruta_progreso
  for insert to authenticated with check (auth.uid() = user_id);

drop policy if exists "ruta_progreso_update_own" on public.ruta_progreso;
create policy "ruta_progreso_update_own" on public.ruta_progreso
  for update to authenticated using (auth.uid() = user_id);

-- Certificados: el dueño lee/escribe; validación pública solo por código (RPC)
drop policy if exists "ruta_certificados_select_own" on public.ruta_certificados;
create policy "ruta_certificados_select_own" on public.ruta_certificados
  for select to authenticated using (auth.uid() = user_id);

drop policy if exists "ruta_certificados_insert_own" on public.ruta_certificados;
create policy "ruta_certificados_insert_own" on public.ruta_certificados
  for insert to authenticated with check (auth.uid() = user_id);

drop policy if exists "ruta_certificados_update_own" on public.ruta_certificados;
create policy "ruta_certificados_update_own" on public.ruta_certificados
  for update to authenticated using (auth.uid() = user_id);

-- Validación pública de certificado (sin login)
create or replace function public.validar_certificado_ruta(p_codigo text)
returns table (
  codigo text,
  nombre_display text,
  titulo_ruta text,
  completed_at timestamptz
)
language sql
security definer
set search_path = public
as $$
  select c.codigo, c.nombre_display, c.titulo_ruta, c.completed_at
  from public.ruta_certificados c
  where upper(c.codigo) = upper(trim(p_codigo))
  limit 1;
$$;

grant execute on function public.validar_certificado_ruta(text) to anon, authenticated;
