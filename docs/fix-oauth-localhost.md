# Fix: Google OAuth redirige a localhost:3000

Si al entrar con Google terminas en `localhost:3000` con `bad_oauth_state` / `ERR_CONNECTION_REFUSED`, el **Site URL** de Supabase sigue en localhost.

## 1) Supabase (obligatorio)

Dashboard → **Authentication** → **URL Configuration**:

https://supabase.com/dashboard/project/epvakbxseshjksfhoorl/auth/url-configuration

**Site URL**
```
https://www.metabolicfitness.cl
```

**Redirect URLs** (agregar todas):
```
https://www.metabolicfitness.cl/**
https://www.metabolicfitness.cl/aula.html
https://www.metabolicfitness.cl/portal.html
https://metabolicfitness.cl/**
http://localhost:5500/**
http://127.0.0.1:5500/**
```

Guarda cambios.

## 2) Probar de nuevo

1. Cierra pestañas de `localhost:3000`
2. Abre **https://www.metabolicfitness.cl/portal.html** (no localhost)
3. “Continuar con Google” → elige tu cuenta
4. Debes caer en **Mi Aula** (`/aula.html`)

## 3) Si aún falla

Google Cloud → Credenciales → tu OAuth Client:

- **Authorized JavaScript origins:** `https://www.metabolicfitness.cl`
- **Authorized redirect URIs:** `https://epvakbxseshjksfhoorl.supabase.co/auth/v1/callback`

## Alternativa sin Google

En el portal puedes entrar con **email + contraseña** (no depende de este redirect).
