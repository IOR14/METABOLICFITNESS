# Suscripción Rutas de Aprendizaje — $20.000 CLP / mes (≈ USD 22)

## 1) Lemon Squeezy (recomendado en Vercel)

1. Crea un producto **Subscription** mensual:
   - CLP **20000** / mes, o
   - USD **22** / mes
2. Share → copia el link `checkout/buy/...`
3. Pégalo en:
   - `.env` → `LEMON_SQUEEZY_CHECKOUT_RUTAS=...` (servidor Flask), y/o
   - `js/checkout-config.js` → `lemon.clp` / `lemon.usd` (sitio estático Vercel)
4. Webhook: eventos `order_created`, `subscription_created`, `subscription_payment_success`
   → `https://TU-DOMINIO/webhook/lemonsqueezy`
5. Custom data: el checkout añade `curso=rutas-fisiologia`

## 2) Supabase

Ejecuta `supabase/schema_rutas_cursos.sql` (incluye curso `rutas-fisiologia`).

Tras el pago, el webhook intenta activar la inscripción automáticamente si el email
coincide con un perfil en `profiles`. Si no, actívalo a mano:

```sql
insert into public.inscripciones (user_id, curso_id, estado, origen)
values ('UUID-DEL-ALUMNO', 'rutas-fisiologia', 'activo', 'pago')
on conflict (user_id, curso_id) do update set estado = 'activo';
```

## 3) Página de compra

`suscripcion-rutas.html` — enlace desde Mi Aula → **Obtener / renovar acceso**.
