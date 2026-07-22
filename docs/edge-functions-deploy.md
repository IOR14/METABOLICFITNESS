# Despliegue Edge Functions — Clases en vivo

Requisitos: [Supabase CLI](https://supabase.com/docs/guides/cli) instalado y login.

```bash
# Desde la raíz del proyecto
npx supabase login
npx supabase link --project-ref epvakbxseshjksfhoorl

# Secrets (nunca en el frontend)
npx supabase secrets set BBB_URL="https://live.metabolicfitness.cl/bigbluebutton/"
npx supabase secrets set BBB_SECRET="TU_SECRET_DE_bbb-conf_--secret"
npx supabase secrets set SYNC_CRON_SECRET="genera-un-token-largo-aleatorio"
# SUPABASE_SERVICE_ROLE_KEY y SUPABASE_ANON_KEY / URL suelen inyectarse solos en Functions;
# si hace falta, configúralos también:
# npx supabase secrets set SUPABASE_SERVICE_ROLE_KEY="eyJ..."

npx supabase functions deploy live-join
npx supabase functions deploy live-sync-recordings --no-verify-jwt
```

## Cron de grabaciones

Cada 15–30 minutos:

```bash
curl -X POST "https://epvakbxseshjksfhoorl.supabase.co/functions/v1/live-sync-recordings" \
  -H "X-Sync-Secret: TU_SYNC_CRON_SECRET" \
  -H "Content-Type: application/json"
```

O con Flask local:

```bash
curl -X POST "http://127.0.0.1:5000/api/live/sync-recordings" \
  -H "X-Sync-Secret: TU_SYNC_CRON_SECRET"
```

Puedes usar cron-job.org, GitHub Actions o el scheduler de tu VPS.
