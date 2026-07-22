-- Permisos para subir grabaciones a Storage + crear lecciones
-- Ejecutar en Supabase SQL Editor → Run

drop policy if exists "course_materials_insert_enrolled" on storage.objects;
create policy "course_materials_insert_enrolled" on storage.objects
  for insert to authenticated
  with check (
    bucket_id = 'course-materials'
    and exists (
      select 1 from public.inscripciones i
      where i.user_id = auth.uid()
        and i.estado = 'activo'
        and (storage.foldername(name))[1] = i.curso_id
    )
  );

drop policy if exists "lecciones_insert_enrolled" on public.lecciones;
create policy "lecciones_insert_enrolled" on public.lecciones
  for insert to authenticated
  with check (
    exists (
      select 1 from public.inscripciones i
      where i.user_id = auth.uid()
        and i.curso_id = lecciones.curso_id
        and i.estado = 'activo'
    )
  );

-- Permitir actualizar recording_url de la sesión (inscritos)
drop policy if exists "sesiones_vivo_update_enrolled" on public.sesiones_vivo;
create policy "sesiones_vivo_update_enrolled" on public.sesiones_vivo
  for update to authenticated
  using (
    exists (
      select 1 from public.inscripciones i
      where i.user_id = auth.uid()
        and i.curso_id = sesiones_vivo.curso_id
        and i.estado = 'activo'
    )
  )
  with check (
    exists (
      select 1 from public.inscripciones i
      where i.user_id = auth.uid()
        and i.curso_id = sesiones_vivo.curso_id
        and i.estado = 'activo'
    )
  );
