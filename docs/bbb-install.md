# Instalación BigBlueButton — Metabolic Fitness

Guía para el servidor de clases en vivo (`live.metabolicfitness.cl`).
El sitio en Vercel **no** aloja BBB: BBB vive en un VPS dedicado y el portal se conecta vía API.

## Requisitos del VPS

- Ubuntu **22.04** limpio (64-bit)
- **8+ GB RAM** (producción recomendada: 16 GB), **4+ vCPU**, **100+ GB** disco
- IP pública fija
- Sin otro software pesado preinstalado

## DNS

En tu proveedor DNS (V2Networks u otro), crea:

| Tipo | Nombre | Valor |
|------|--------|-------|
| A | `live` | IP_DEL_VPS |

Espera a que `live.metabolicfitness.cl` resuelva a la IP del VPS.

## Instalación (como root en el VPS)

```bash
# Opcional: clonar este repo o copiar scripts/bbb-install-metabolic.sh
wget -qO- https://raw.githubusercontent.com/bigbluebutton/bbb-install/v3.0.x-release/bbb-install.sh \
  | bash -s -- -w -v jammy-300 \
      -s live.metabolicfitness.cl \
      -e director@whitesoultech.cl
```

Flags:
- `-w` firewall UFW
- `-v jammy-300` BigBlueButton 3.0
- `-s` hostname
- `-e` email Let's Encrypt

Tras ~15–40 min:

```bash
bbb-conf --check
bbb-conf --secret
```

Copia la **URL** y el **Secret** al `.env` / secrets de Supabase:

```
BBB_URL=https://live.metabolicfitness.cl/bigbluebutton/
BBB_SECRET=xxxxxxxx
```

## Verificación rápida

Abre: https://live.metabolicfitness.cl  
Debe cargar la página de BBB / Greenlight (si instalaste `-g`).

## Integración con Metabolic Fitness

1. Ejecuta en Supabase SQL Editor: `supabase/schema_live.sql`
2. Despliega Edge Functions: `live-join` y `live-sync-recordings`
3. Configura secrets en Supabase (Dashboard → Edge Functions → Secrets):
   - `BBB_URL`
   - `BBB_SECRET`
   - `SUPABASE_SERVICE_ROLE_KEY` (solo en secrets, nunca en el frontend)
   - `SYNC_CRON_SECRET` (token aleatorio para el sync)
4. En Mi Aula, el alumno inscrito usa **Entrar a clase en vivo**

## Crear una sesión (profesor / admin)

En Table Editor → `sesiones_vivo` → Insert:

- `curso_id`: `adulto-mayor` o `pediatria-salud`
- `titulo`: ej. `Clase en vivo — Semana 1`
- `bbb_meeting_id`: id único, ej. `mf-adulto-2026-07-21`
- `starts_at`: fecha/hora
- `estado`: `programada` o `en_vivo`
- `record`: `true`

El Edge Function `live-join` crea/une la reunión en BBB al vuelo.

## Grabaciones

Programa un cron (cada 15–30 min) que llame:

```
POST https://epvakbxseshjksfhoorl.supabase.co/functions/v1/live-sync-recordings
Authorization: Bearer <SYNC_CRON_SECRET>
```

O usa el endpoint Flask local: `POST /api/live/sync-recordings` con header `X-Sync-Secret`.

Las grabaciones publicadas en BBB se registran en `sesiones_vivo.recording_url` y como `lecciones` (tipo `link`).
