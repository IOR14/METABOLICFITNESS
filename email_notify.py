"""
email_notify.py — Avisos por correo al equipo y al alumno tras una compra.

Configura SMTP en .env (Gmail, Outlook, hosting, etc.).
Si SMTP no está configurado, guarda el correo en logs/emails/ para pruebas locales.
"""

from __future__ import annotations

import os
import smtplib
import ssl
from datetime import datetime, timezone
from email.message import EmailMessage
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
LOG_DIR = ROOT_DIR / "logs" / "emails"

COURSE_NAMES = {
    "adulto-mayor": "Fisiología del Adulto Mayor",
    "pediatria-salud": "Pediatría y Salud",
    "rutas-fisiologia": "Suscripción Rutas de Aprendizaje (mensual)",
}

WHATSAPP_ACCESS = "https://wa.me/56910111167?text=Hola%2C%20acabo%20de%20comprar%20un%20curso%20y%20necesito%20el%20acceso."


def _env(name: str, default: str = "") -> str:
    return (os.getenv(name) or default).strip()


def format_amount(amount_total, currency: str) -> str:
    if amount_total is None:
        return "—"
    cur = (currency or "").lower()
    # CLP es moneda de cero decimales en Stripe
    if cur == "clp":
        return f"${amount_total:,.0f} CLP".replace(",", ".")
    if cur == "usd":
        return f"USD {amount_total / 100:.2f}"
    return f"{amount_total} {cur.upper()}"


def course_label(curso: str) -> str:
    return COURSE_NAMES.get(curso or "", curso or "Curso Metabolic Fitness")


def _smtp_ready() -> bool:
    return bool(_env("SMTP_HOST") and _env("SMTP_USER") and _env("SMTP_PASSWORD") and _env("SMTP_FROM"))


def _save_local_copy(to_addrs: list[str], subject: str, body: str) -> Path:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    safe_subj = "".join(c if c.isalnum() or c in "-_" else "_" for c in subject)[:60]
    path = LOG_DIR / f"{stamp}_{safe_subj}.txt"
    path.write_text(
        f"To: {', '.join(to_addrs)}\nSubject: {subject}\n\n{body}\n",
        encoding="utf-8",
    )
    return path


def send_email(to_addrs: list[str], subject: str, body: str) -> bool:
    """Envía correo por SMTP o lo guarda en logs/emails/. Devuelve True si se envió o guardó."""
    recipients = [a.strip() for a in to_addrs if a and a.strip()]
    if not recipients:
        print("[Email] Sin destinatarios; se omite.")
        return False

    if not _smtp_ready():
        path = _save_local_copy(recipients, subject, body)
        print(f"[Email] SMTP no configurado; guardado en {path}")
        return True

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = _env("SMTP_FROM")
    msg["To"] = ", ".join(recipients)
    msg.set_content(body)

    host = _env("SMTP_HOST")
    port = int(_env("SMTP_PORT", "587"))
    user = _env("SMTP_USER")
    password = _env("SMTP_PASSWORD")
    use_tls = _env("SMTP_TLS", "true").lower() in ("1", "true", "yes")

    try:
        if use_tls:
            with smtplib.SMTP(host, port, timeout=30) as server:
                server.starttls(context=ssl.create_default_context())
                server.login(user, password)
                server.send_message(msg)
        else:
            with smtplib.SMTP_SSL(host, port, timeout=30, context=ssl.create_default_context()) as server:
                server.login(user, password)
                server.send_message(msg)
        print(f"[Email] Enviado a {recipients}: {subject}")
        return True
    except Exception as exc:  # noqa: BLE001 — no tumbar el webhook por fallo de correo
        path = _save_local_copy(recipients, subject, body)
        print(f"[Email] Error SMTP ({exc}); copia en {path}")
        return False


def notify_purchase(
    *,
    session_id: str,
    email: str,
    curso: str,
    moneda: str,
    amount_total,
    currency: str,
) -> None:
    """Avisa al equipo y confirma al alumno."""
    nombre_curso = course_label(curso)
    monto = format_amount(amount_total, currency)
    portal = _env("DOMAIN", "https://www.metabolicfitness.cl").rstrip("/") + "/portal.html"

    team = [
        a.strip()
        for a in _env("NOTIFY_EMAIL_TO", "director@whitesoultech.cl").split(",")
        if a.strip()
    ]

    team_body = (
        f"Nueva venta en Metabolic Fitness\n"
        f"{'=' * 40}\n\n"
        f"Curso: {nombre_curso}\n"
        f"Email alumno: {email or '(sin email)'}\n"
        f"Moneda elegida: {(moneda or currency or '').upper()}\n"
        f"Monto: {monto}\n"
        f"Session ID: {session_id}\n\n"
        f"Acción: contactar al alumno y otorgar acceso al curso / portal.\n"
        f"Portal: {portal}\n"
        f"WhatsApp acceso: {WHATSAPP_ACCESS}\n"
    )
    send_email(team, f"[Venta] {nombre_curso} — {email or session_id}", team_body)

    if email:
        student_body = (
            f"Hola,\n\n"
            f"¡Gracias por tu compra en Metabolic Fitness!\n\n"
            f"Curso: {nombre_curso}\n"
            f"Monto: {monto}\n"
            f"Referencia: {session_id}\n\n"
            f"En breve te enviaremos (o confirmaremos) el acceso al contenido.\n"
            f"También puedes escribirnos por WhatsApp para agilizar el acceso:\n"
            f"{WHATSAPP_ACCESS}\n\n"
            f"Portal del estudiante: {portal}\n\n"
            f"Saludos,\n"
            f"Equipo Metabolic Fitness\n"
            f"https://www.metabolicfitness.cl\n"
        )
        send_email([email], f"Confirmación de compra — {nombre_curso}", student_body)
    else:
        print("[Email] Compra sin email de alumno; solo se avisó al equipo.")
