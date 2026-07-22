"""
app.py — Servidor Flask para Metabolic Fitness.

Sirve tu sitio web actual TAL CUAL está (todos los .html, imágenes, CSS y JS
quedan en la raíz del proyecto, no hace falta moverlos) y agrega:
  - Validación de certificados en /validar
  - Checkout de Stripe para compra de cursos

Cómo ejecutar:
    1) pip install -r requirements.txt
    2) Copia .env.example a .env y pega tus claves de prueba
    3) python database.py        (solo la primera vez)
    4) python app.py
    5) Abre: http://127.0.0.1:5000
"""

import os

import stripe
from dotenv import load_dotenv
from flask import Flask, abort, jsonify, redirect, render_template, request, send_from_directory

from database import buscar_certificado, init_db, registrar_compra, seed_data
from email_notify import notify_purchase
from bbb_client import ensure_meeting, join_url, list_recordings

load_dotenv()

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, template_folder="templates", static_folder=None)

stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "")
STRIPE_WEBHOOK_SECRET = (os.getenv("STRIPE_WEBHOOK_SECRET") or "").strip()
DOMAIN = os.getenv("DOMAIN", "http://127.0.0.1:5000").rstrip("/")
BBB_URL = (os.getenv("BBB_URL") or "").strip()
BBB_SECRET = (os.getenv("BBB_SECRET") or "").strip()
SYNC_CRON_SECRET = (os.getenv("SYNC_CRON_SECRET") or "").strip()
SUPABASE_URL = (os.getenv("SUPABASE_URL") or "").strip()
SUPABASE_SERVICE_ROLE_KEY = (os.getenv("SUPABASE_SERVICE_ROLE_KEY") or "").strip()

print(
    f"[Config] Stripe key={'si' if stripe.api_key else 'NO'} | "
    f"webhook_secret={'si' if STRIPE_WEBHOOK_SECRET.startswith('whsec_') else 'NO'} | "
    f"BBB={'si' if BBB_URL and BBB_SECRET else 'NO'}"
)

# Catálogo Lemon Squeezy (internacional). Pega el link "Share" → Checkout Overlay / Buy.
LEMON_CHECKOUT = {
    "adulto-mayor": os.getenv("LEMON_SQUEEZY_CHECKOUT_ADULTO_MAYOR", "").strip(),
    "pediatria-salud": os.getenv("LEMON_SQUEEZY_CHECKOUT_PEDIATRIA_SALUD", "").strip(),
    "rutas-fisiologia": os.getenv("LEMON_SQUEEZY_CHECKOUT_RUTAS", "").strip(),
    "rutas-fisiologia-clp": os.getenv("LEMON_SQUEEZY_CHECKOUT_RUTAS_CLP", "").strip(),
    "rutas-fisiologia-usd": os.getenv("LEMON_SQUEEZY_CHECKOUT_RUTAS_USD", "").strip(),
}

# Catálogo Stripe (modo test / futuro Atlas). Clave = curso + moneda.
COURSE_PRICES = {
    "adulto-mayor": {
        "clp": os.getenv("STRIPE_PRICE_ADULTO_MAYOR_CLP", "price_1TvKwFIffBywVZ8XhjHxLizp"),
        "usd": os.getenv("STRIPE_PRICE_ADULTO_MAYOR_USD", "price_1TvKwFIffBywVZ8X2GwYYMW4"),
    },
    "pediatria-salud": {
        "clp": os.getenv("STRIPE_PRICE_PEDIATRIA_SALUD_CLP", ""),
        "usd": os.getenv("STRIPE_PRICE_PEDIATRIA_SALUD_USD", ""),
    },
    "rutas-fisiologia": {
        "clp": os.getenv("STRIPE_PRICE_RUTAS_CLP", ""),
        "usd": os.getenv("STRIPE_PRICE_RUTAS_USD", ""),
    },
}

init_db()
seed_data()


@app.route("/")
def home():
    """Página de inicio."""
    return send_from_directory(ROOT_DIR, "index.html")


@app.route("/validar")
def validar():
    """
    Validación de certificados.
    - /validar                 -> muestra el buscador
    - /validar?serial=XXXX      -> valida ese serial
    """
    serial = (request.args.get("serial") or "").strip()

    if not serial:
        return render_template("validar.html", estado="buscar", serial="", cert=None)

    cert = buscar_certificado(serial)
    if cert:
        return render_template("validar.html", estado="valido", serial=serial, cert=cert)
    return render_template("validar.html", estado="invalido", serial=serial, cert=None)


@app.route("/api/lemon-checkout/<curso>")
def lemon_checkout_url(curso):
    """Devuelve la URL de checkout de Lemon Squeezy para el curso."""
    key = curso.strip().lower()
    moneda = (request.args.get("moneda") or "").strip().lower()
    url = ""
    if moneda in ("clp", "usd"):
        url = LEMON_CHECKOUT.get(f"{key}-{moneda}", "")
    if not url:
        url = LEMON_CHECKOUT.get(key, "")
    if not url or "REEMPLAZA" in url:
        return jsonify({"url": None, "error": f"Checkout de Lemon Squeezy no configurado para '{curso}' en .env"}), 503
    sep = "&" if "?" in url else "?"
    if "checkout[custom][curso]" not in url:
        url = f"{url}{sep}checkout[custom][curso]={key}"
    return jsonify({"url": url})


def _activar_inscripcion_supabase(email: str, curso: str) -> bool:
    """Activa inscripción en Supabase si encontramos el perfil por email."""
    email = (email or "").strip().lower()
    curso = (curso or "").strip()
    if not email or not curso:
        return False
    if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
        return False
    try:
        profiles = _supabase_rest(
            f"profiles?email=eq.{email}&select=id"
        ) or []
        if not profiles:
            print(f"[Supabase] Sin perfil para {email}; inscripción manual pendiente")
            return False
        user_id = profiles[0]["id"]
        _supabase_rest(
            "inscripciones",
            method="POST",
            json_body={
                "user_id": user_id,
                "curso_id": curso,
                "estado": "activo",
                "origen": "pago",
            },
            prefer="resolution=merge-duplicates,return=minimal",
        )
        print(f"[Supabase] Inscripción activa: {email} → {curso}")
        return True
    except Exception as exc:  # noqa: BLE001
        print(f"[Supabase] No se pudo activar inscripción: {exc}")
        return False


def _supabase_rest(path: str, *, method: str = "GET", json_body=None, prefer=None):
    """Llamada mínima a PostgREST con service role (solo servidor)."""
    import json
    from urllib.error import HTTPError
    from urllib.request import Request, urlopen

    if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
        raise RuntimeError("SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY no configurados")
    url = SUPABASE_URL.rstrip("/") + "/rest/v1/" + path.lstrip("/")
    headers = {
        "apikey": SUPABASE_SERVICE_ROLE_KEY,
        "Authorization": f"Bearer {SUPABASE_SERVICE_ROLE_KEY}",
        "Content-Type": "application/json",
    }
    if prefer:
        headers["Prefer"] = prefer
    data = None if json_body is None else json.dumps(json_body).encode("utf-8")
    req = Request(url, data=data, headers=headers, method=method)
    try:
        with urlopen(req, timeout=30) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw) if raw else None
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(detail or str(exc)) from exc


@app.route("/api/live/join", methods=["POST"])
def live_join():
    """
    Join BBB (fallback local). Body JSON: { sesion_id? , curso_id? , full_name?, user_id?, as_moderator? }
    En producción preferir Edge Function live-join con JWT de Supabase.
    """
    if not BBB_URL or not BBB_SECRET:
        return jsonify({"error": "BBB no configurado (BBB_URL / BBB_SECRET)"}), 503

    body = request.get_json(silent=True) or {}
    sesion_id = (body.get("sesion_id") or "").strip()
    curso_id = (body.get("curso_id") or "").strip()
    full_name = (body.get("full_name") or body.get("email") or "Alumno").strip()
    user_id = (body.get("user_id") or "").strip() or None
    as_moderator = bool(body.get("as_moderator"))

    try:
        if sesion_id:
            rows = _supabase_rest(
                f"sesiones_vivo?id=eq.{sesion_id}&select=*"
            )
        elif curso_id:
            rows = _supabase_rest(
                f"sesiones_vivo?curso_id=eq.{curso_id}&estado=in.(programada,en_vivo)&select=*&order=starts_at.asc&limit=1"
            )
        else:
            return jsonify({"error": "Indica sesion_id o curso_id"}), 400

        if not rows:
            return jsonify({"error": "No hay sesión en vivo disponible"}), 404
        sesion = rows[0]

        if user_id:
            insc = _supabase_rest(
                f"inscripciones?user_id=eq.{user_id}&curso_id=eq.{sesion['curso_id']}&estado=eq.activo&select=id"
            )
            if not insc and not as_moderator:
                return jsonify({"error": "No estás inscrito en este curso"}), 403

        attendee_pw = sesion.get("attendee_pw") or "ap"
        moderator_pw = sesion.get("moderator_pw") or "mp"
        ensure_meeting(
            BBB_URL,
            BBB_SECRET,
            sesion["bbb_meeting_id"],
            sesion.get("titulo") or "Clase Metabolic",
            attendee_pw=attendee_pw,
            moderator_pw=moderator_pw,
            record=bool(sesion.get("record", True)),
        )
        _supabase_rest(
            f"sesiones_vivo?id=eq.{sesion['id']}",
            method="PATCH",
            json_body={"estado": "en_vivo"},
            prefer="return=minimal",
        )
        password = moderator_pw if as_moderator else attendee_pw
        url = join_url(
            BBB_URL,
            BBB_SECRET,
            sesion["bbb_meeting_id"],
            full_name,
            password,
            user_id=user_id,
        )
        return jsonify({"url": url, "sesion_id": sesion["id"], "meeting_id": sesion["bbb_meeting_id"]})
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


@app.route("/api/live/sync-recordings", methods=["POST"])
def live_sync_recordings():
    """Sincroniza grabaciones BBB → sesiones_vivo + lecciones. Protegido con X-Sync-Secret."""
    if SYNC_CRON_SECRET:
        if request.headers.get("X-Sync-Secret", "") != SYNC_CRON_SECRET:
            return jsonify({"error": "No autorizado"}), 401
    if not BBB_URL or not BBB_SECRET:
        return jsonify({"error": "BBB no configurado"}), 503

    try:
        sesiones = _supabase_rest("sesiones_vivo?select=id,curso_id,titulo,bbb_meeting_id,recording_id") or []
        updated = 0
        lessons = 0
        for sesion in sesiones:
            mid = sesion.get("bbb_meeting_id")
            if not mid:
                continue
            recs = [r for r in list_recordings(BBB_URL, BBB_SECRET, mid) if r.get("published") and r.get("playback_url")]
            if not recs:
                continue
            rec = recs[-1]
            if sesion.get("recording_id") == rec["recording_id"]:
                continue
            _supabase_rest(
                f"sesiones_vivo?id=eq.{sesion['id']}",
                method="PATCH",
                json_body={
                    "recording_url": rec["playback_url"],
                    "recording_id": rec["recording_id"],
                    "estado": "finalizada",
                },
                prefer="return=minimal",
            )
            updated += 1
            existing = _supabase_rest(
                f"lecciones?bbb_recording_id=eq.{rec['recording_id']}&select=id"
            )
            if not existing:
                orden_rows = _supabase_rest(
                    f"lecciones?curso_id=eq.{sesion['curso_id']}&select=orden&order=orden.desc&limit=1"
                ) or []
                orden = (orden_rows[0]["orden"] if orden_rows else 0) + 1
                _supabase_rest(
                    "lecciones",
                    method="POST",
                    json_body={
                        "curso_id": sesion["curso_id"],
                        "titulo": f"Grabación: {sesion.get('titulo') or rec.get('name') or 'Clase en vivo'}",
                        "orden": orden,
                        "tipo": "vivo",
                        "contenido": rec["playback_url"],
                        "bbb_recording_id": rec["recording_id"],
                    },
                    prefer="return=minimal",
                )
                lessons += 1
        return jsonify({"ok": True, "sesiones_actualizadas": updated, "lecciones_creadas": lessons})
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


@app.route("/webhook/lemonsqueezy", methods=["POST"])
def lemon_squeezy_webhook():
    """
    Webhook Lemon Squeezy (eventos order_created / order_refunded).
    Dashboard → Settings → Webhooks → URL: https://tudominio.com/webhook/lemonsqueezy
    """
    import hashlib
    import hmac
    import json

    payload = request.data
    secret = (os.getenv("LEMON_SQUEEZY_WEBHOOK_SECRET") or "").strip()
    signature = request.headers.get("X-Signature", "")

    if secret:
        digest = hmac.new(secret.encode("utf-8"), payload, hashlib.sha256).hexdigest()
        if not hmac.compare_digest(digest, signature):
            return "Firma inválida", 400

    try:
        event = json.loads(payload.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        return str(exc), 400

    meta = event.get("meta") or {}
    event_name = meta.get("event_name") or ""
    data = (event.get("data") or {}).get("attributes") or {}

    if event_name in ("order_created", "subscription_created", "subscription_payment_success"):
        order_id = str((event.get("data") or {}).get("id") or data.get("identifier") or "")
        email = data.get("user_email") or data.get("customer_email") or ""
        # total en centavos USD habitualmente
        total = data.get("total")
        currency = (data.get("currency") or "usd").lower()
        custom = data.get("custom_data") or meta.get("custom_data") or {}
        curso = custom.get("curso") or "adulto-mayor"
        status = data.get("status") or "paid"

        nueva = registrar_compra(
            session_id=f"ls_{order_id}",
            email=email,
            curso=curso,
            moneda=currency,
            amount_total=total,
            currency=currency,
            payment_status=status,
        )
        print(f"[Lemon] {event_name} {order_id} email={email} curso={curso} registrada={nueva}")
        _activar_inscripcion_supabase(email, curso)
        if nueva:
            notify_purchase(
                session_id=f"ls_{order_id}",
                email=email,
                curso=curso,
                moneda=currency,
                amount_total=total,
                currency=currency,
            )
    else:
        print(f"[Lemon] Evento: {event_name}")

    return "", 200


@app.route("/crear-checkout-session", methods=["POST"])
def crear_checkout_session():
    """
    Crea una Checkout Session Stripe.
    Form: curso=... & moneda=clp|usd & mode=payment|subscription
    """
    if not stripe.api_key or stripe.api_key.startswith("sk_test_REEMPLAZA"):
        abort(500, description="Configura STRIPE_SECRET_KEY en el archivo .env")

    curso = (request.form.get("curso") or "adulto-mayor").strip().lower()
    moneda = (request.form.get("moneda") or "clp").strip().lower()
    mode = (request.form.get("mode") or "payment").strip().lower()
    if mode not in ("payment", "subscription"):
        mode = "payment"
    # Suscripción de rutas siempre en modo subscription
    if curso == "rutas-fisiologia":
        mode = "subscription"

    precios = COURSE_PRICES.get(curso)
    if not precios:
        abort(400, description="Curso no válido")

    price_id = precios.get(moneda)
    if not price_id:
        abort(400, description="Moneda no válida o Price ID no configurado (usa clp o usd)")

    try:
        session = stripe.checkout.Session.create(
            mode=mode,
            line_items=[{"price": price_id, "quantity": 1}],
            success_url=f"{DOMAIN}/pago-exito?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{DOMAIN}/pago-cancelado",
            metadata={"curso": curso, "moneda": moneda, "mode": mode},
            customer_creation="always",
            billing_address_collection="required",
            locale="es",
        )
    except stripe.StripeError as exc:
        abort(502, description=str(exc.user_message or exc))

    return redirect(session.url, code=303)

@app.route("/pago-exito")
def pago_exito():
    """Página de confirmación tras Checkout (el fulfillment real va por webhook)."""
    session_id = (request.args.get("session_id") or "").strip()
    return render_template("pago-exito.html", session_id=session_id)


@app.route("/pago-cancelado")
def pago_cancelado():
    return render_template("pago-cancelado.html")


@app.route("/webhook", methods=["POST"])
def stripe_webhook():
    """
    Endpoint de webhooks. En local:
      stripe listen --forward-to localhost:5000/webhook
    Eventos: checkout.session.completed, invoice.paid, invoice.payment_failed
    """
    payload = request.data
    sig_header = request.headers.get("Stripe-Signature", "")

    if not STRIPE_WEBHOOK_SECRET:
        app.logger.error("STRIPE_WEBHOOK_SECRET no configurado en .env")
        return "Webhook secret no configurado", 500

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
    except ValueError as exc:
        return str(exc), 400
    except stripe.SignatureVerificationError as exc:
        return str(exc), 400

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        if hasattr(session, "to_dict"):
            session = session.to_dict()
        meta = session.get("metadata") or {}
        details = session.get("customer_details") or {}
        email = details.get("email") or session.get("customer_email") or ""
        nueva = registrar_compra(
            session_id=session.get("id"),
            email=email,
            curso=meta.get("curso"),
            moneda=meta.get("moneda"),
            amount_total=session.get("amount_total"),
            currency=session.get("currency"),
            payment_status=session.get("payment_status"),
        )
        print(
            f"[Stripe] Pago completado: {session.get('id')} "
            f"curso={meta.get('curso')} email={email} registrada={nueva}"
        )
        if nueva:
            notify_purchase(
                session_id=session.get("id") or "",
                email=email,
                curso=meta.get("curso") or "",
                moneda=meta.get("moneda") or "",
                amount_total=session.get("amount_total"),
                currency=session.get("currency") or "",
            )
            _activar_inscripcion_supabase(email, meta.get("curso") or "")
        else:
            print("[Stripe] Evento duplicado; no se reenvían correos.")
    elif event["type"] == "invoice.paid":
        invoice = event["data"]["object"]
        if hasattr(invoice, "to_dict"):
            invoice = invoice.to_dict()
        print("[Stripe] Factura pagada:", invoice.get("id"), invoice.get("number"))
        # Renovación de suscripción: reactivar acceso a rutas
        meta = invoice.get("subscription_details", {}).get("metadata") or {}
        lines = ((invoice.get("lines") or {}).get("data") or [])
        curso = meta.get("curso") or "rutas-fisiologia"
        cust_email = ""
        try:
            cust_email = (invoice.get("customer_email") or "") or ""
        except Exception:
            cust_email = ""
        if cust_email:
            _activar_inscripcion_supabase(cust_email, curso)    elif event["type"] == "invoice.payment_failed":
        invoice = event["data"]["object"]
        if hasattr(invoice, "to_dict"):
            invoice = invoice.to_dict()
        print("[Stripe] Factura fallida:", invoice.get("id"))

    return "", 200


@app.route("/<path:filename>")
def archivos_estaticos(filename):
    """Sirve archivos estáticos del sitio desde la raíz del proyecto."""
    if filename.startswith("api/"):
        abort(404)
    ruta_absoluta = os.path.join(ROOT_DIR, filename)
    if os.path.isfile(ruta_absoluta):
        return send_from_directory(ROOT_DIR, filename)
    abort(404)


if __name__ == "__main__":
    # use_reloader=False evita procesos duplicados que rompen el webhook en Windows
    app.run(host="127.0.0.1", port=5000, debug=True, use_reloader=False)
