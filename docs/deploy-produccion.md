# Deploy a producción — Metabolic Fitness

El sitio público actual (`www.metabolicfitness.cl`) está en **GitHub Pages** (solo HTML).
Los pagos, webhooks y alta automática de alumnos requieren **Flask** en la nube.

## Estado actual (julio 2026)

- **Sitio:** `https://www.metabolicfitness.cl` (GitHub Pages)
- **API Flask + Stripe:** `https://metabolicfitness.vercel.app`
- Los botones de pago en Academia / Suscripción apuntan a la API de Vercel
- Webhook Stripe → `https://metabolicfitness.vercel.app/webhook`
- Tras el pago, redirect a `https://www.metabolicfitness.cl/pago-exito.html`

Para unificar todo en un solo dominio, agrega `www.metabolicfitness.cl` al proyecto Vercel y cambia el DNS en Cloudflare (ver abajo).

## Opción recomendada: Vercel (Flask completo)

Sirve el sitio + API en el mismo origen.

### 1. Push a GitHub
```bash
git push origin main
```

### 2. Deploy
```bash
npx vercel --prod
```

### 3. Variables de entorno (Vercel → Project → Settings → Environment Variables)

| Variable | Valor |
|----------|--------|
| `DOMAIN` | `https://www.metabolicfitness.cl` (o la URL `.vercel.app` mientras pruebas) |
| `STRIPE_SECRET_KEY` | `sk_test_...` o `sk_live_...` |
| `STRIPE_WEBHOOK_SECRET` | `whsec_...` del endpoint de producción |
| `STRIPE_PRICE_ADULTO_MAYOR_CLP` / `_USD` | price_... |
| `STRIPE_PRICE_PEDIATRIA_SALUD_CLP` / `_USD` | price_... |
| `STRIPE_PRICE_RUTAS_*` | price_... |
| `SUPABASE_URL` | `https://epvakbxseshjksfhoorl.supabase.co` |
| `SUPABASE_SERVICE_ROLE_KEY` | `sb_secret_...` |
| `NOTIFY_EMAIL_TO` | correos del equipo |

### 4. Dominio
1. Vercel → Domains → agrega `www.metabolicfitness.cl` y `metabolicfitness.cl`
2. En **Cloudflare DNS**, apunta:
   - `www` → CNAME `cname.vercel-dns.com` (o el que indique Vercel)
   - raíz `@` según instrucciones de Vercel
3. Desactiva temporalmente GitHub Pages si compite por el mismo host

### 5. Webhook Stripe (producción)
Dashboard → Developers → Webhooks → Add endpoint:
- URL: `https://www.metabolicfitness.cl/webhook`
- Eventos: `checkout.session.completed`, `invoice.paid`, `invoice.payment_failed`, `customer.subscription.deleted`
- Copia el `whsec_...` a `STRIPE_WEBHOOK_SECRET`

### 6. Supabase Auth URLs
Site URL: `https://www.metabolicfitness.cl`  
Redirects: `https://www.metabolicfitness.cl/**`

## Opción B: GitHub Pages + API aparte

1. Deja Pages para el HTML
2. Despliega solo Flask (Vercel/Railway/Render)
3. En el HTML, antes de `js/api-config.js`:
   ```html
   <script>window.MF_API_BASE_OVERRIDE = 'https://TU-API.vercel.app';</script>
   ```
4. `DOMAIN=https://www.metabolicfitness.cl` (páginas `pago-exito.html` / `pago-cancelado.html` en la raíz del repo)
5. Webhook Stripe → `https://TU-API.vercel.app/webhook`

## Smoke test
1. https://www.metabolicfitness.cl/academia.html → Pagar USD 150 (test card `4242…`)
2. Stripe Dashboard → pago OK
3. Supabase → Auth + `inscripciones` con el email del comprador
4. Portal / Mi Aula con ese email
