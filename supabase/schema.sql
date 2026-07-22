-- Metabolic Fitness — Portal Alumnos
-- Pegar completo en: Supabase → SQL Editor → New query → Run

-- Perfiles (extiende auth.users)
create table if not exists public.profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  email text,
  full_name text,
  role text not null default 'student' check (role in ('student', 'admin')),
  created_at timestamptz not null default now()
);

-- Catálogo de cursos
create table if not exists public.cursos (
  id text primary key,
  titulo text not null,
  descripcion text,
  precio_clp integer,
  precio_usd numeric(10,2),
  activo boolean not null default true,
  created_at timestamptz not null default now()
);

-- Inscripciones (quién compró qué)
create table if not exists public.inscripciones (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  curso_id text not null references public.cursos(id) on delete cascade,
  estado text not null default 'activo' check (estado in ('activo', 'suspendido', 'expirado')),
  origen text default 'manual',
  lemon_order_id text,
  created_at timestamptz not null default now(),
  unique (user_id, curso_id)
);

-- Lecciones / materiales por curso
create table if not exists public.lecciones (
  id uuid primary key default gen_random_uuid(),
  curso_id text not null references public.cursos(id) on delete cascade,
  titulo text not null,
  orden integer not null default 1,
  tipo text not null default 'video' check (tipo in ('video', 'pdf', 'texto', 'link')),
  storage_path text,
  contenido text,
  duracion_min integer,
  created_at timestamptz not null default now()
);

-- Crear perfil al registrarse
create or replace function public.handle_new_user()
returns trigger
language plpgsql
security definer
set search_path = public
as $$
begin
  insert into public.profiles (id, email, full_name)
  values (
    new.id,
    new.email,
    coalesce(new.raw_user_meta_data->>'full_name', '')
  );
  return new;
end;
$$;

drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created
  after insert on auth.users
  for each row execute function public.handle_new_user();

-- Cursos iniciales
insert into public.cursos (id, titulo, descripcion, precio_clp, precio_usd)
values
  (
    'adulto-mayor',
    E'Fisiolog\u00eda del Adulto Mayor',
    E'Formaci\u00f3n cl\u00ednica para prescribir ejercicio con precisi\u00f3n fisiol\u00f3gica en personas mayores.',
    130000,
    150
  ),
  (
    'pediatria-salud',
    E'Pediatr\u00eda y Salud',
    E'Formaci\u00f3n cl\u00ednica para prescribir ejercicio y actividad f\u00edsica en ni\u00f1os y adolescentes.',
    130000,
    150
  )
on conflict (id) do update set
  titulo = excluded.titulo,
  descripcion = excluded.descripcion,
  precio_clp = excluded.precio_clp,
  precio_usd = excluded.precio_usd;

-- RLS
alter table public.profiles enable row level security;
alter table public.cursos enable row level security;
alter table public.inscripciones enable row level security;
alter table public.lecciones enable row level security;

-- Profiles: cada uno ve/edita el suyo
drop policy if exists "profiles_select_own" on public.profiles;
create policy "profiles_select_own" on public.profiles
  for select to authenticated using (auth.uid() = id);

drop policy if exists "profiles_update_own" on public.profiles;
create policy "profiles_update_own" on public.profiles
  for update to authenticated using (auth.uid() = id);

-- Cursos activos: visibles para alumnos autenticados (catálogo)
drop policy if exists "cursos_select_activo" on public.cursos;
create policy "cursos_select_activo" on public.cursos
  for select to authenticated using (activo = true);

-- Inscripciones: solo las propias
drop policy if exists "inscripciones_select_own" on public.inscripciones;
create policy "inscripciones_select_own" on public.inscripciones
  for select to authenticated using (auth.uid() = user_id);

-- Lecciones: solo si el alumno está inscrito en ese curso
drop policy if exists "lecciones_select_enrolled" on public.lecciones;
create policy "lecciones_select_enrolled" on public.lecciones
  for select to authenticated
  using (
    exists (
      select 1 from public.inscripciones i
      where i.user_id = auth.uid()
        and i.curso_id = lecciones.curso_id
        and i.estado = 'activo'
    )
  );

-- Storage: bucket privado de materiales del curso
insert into storage.buckets (id, name, public)
values ('course-materials', 'course-materials', false)
on conflict (id) do nothing;

drop policy if exists "course_materials_select_enrolled" on storage.objects;
create policy "course_materials_select_enrolled" on storage.objects
  for select to authenticated
  using (
    bucket_id = 'course-materials'
    and exists (
      select 1 from public.inscripciones i
      where i.user_id = auth.uid()
        and i.estado = 'activo'
        and (storage.foldername(name))[1] = i.curso_id
    )
  );
