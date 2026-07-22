# Clases en vivo sin VPS — Jitsi Meet (open source)

BigBlueButton es open source, pero **necesita un servidor propio** (VPS de pago).  
Si no puedes contratar VPS, usamos **Jitsi Meet** en `meet.jit.si`:

- Software **100% open source**
- Hosting **gratis** (servidores públicos de Jitsi)
- Se abre desde **Mi Aula** solo si el alumno está inscrito

## Cómo está configurado

En [`js/supabase-config.js`](../js/supabase-config.js):

```js
liveProvider: 'jitsi',
jitsiDomain: 'meet.jit.si'
```

Cuando más adelante tengas VPS, cambia a:

```js
liveProvider: 'bbb'
```

y configura `BBB_URL` / `BBB_SECRET` (ver `docs/bbb-install.md`).

## Uso

1. Crea una fila en `sesiones_vivo` (como la sesión demo).
2. El alumno inscrito entra a Mi Aula → **Unirse a la clase**.
3. Se abre una sala Jitsi: `https://meet.jit.si/MetabolicFitness-<bbb_meeting_id>`

## Grabaciones (sin VPS)

En `meet.jit.si` la grabación es **local** (en el PC). Flujo en Mi Aula:

1. En la clase embebida: menú ⋮ → **Grabar**.
2. Al terminar, detén la grabación (Jitsi guarda un archivo en tu computador).
3. En el panel derecho **Guardar en Metabolic** → elige el archivo → **Subir grabación a Mi Aula**.
4. Queda como lección en **Entrar al curso**.

Antes, ejecuta una vez en Supabase SQL Editor: `supabase/schema_recording_upload.sql`.

## Sala embebida

Al unirse, la clase abre **dentro de Mi Aula** (no en otra pestaña):

- Lista de **participantes / accesos** a la derecha
- Barra de Jitsi con **compartir pantalla**, chat, etc.
- Subida de grabación al curso

## Límites honestos

| | Jitsi (meet.jit.si) | BigBlueButton (VPS) |
|--|---------------------|---------------------|
| Costo | $0 | VPS ~USD 20–40/mes |
| Clase en vivo | Sí | Sí |
| Pizarra / aulas | Básica | Muy completa |
| Grabación automática en el portal | No (manual/local) | Sí |
