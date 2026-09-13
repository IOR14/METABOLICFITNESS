# -*- coding: utf-8 -*-
"""
Certificado de reconocimiento y agradecimiento — Dr. Guillermo León.

Salida:
    certificados_reconocimiento/MF-REC-GL01_Guillermo_Leon/
        certificado_con_qr.pdf
        QR_MF-REC-GL01.png

Uso:
    python generar_reconocimiento_guillermo_leon.py
"""

from __future__ import annotations

import io
import os
import sqlite3
import sys

import fitz
import qrcode
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

from database import init_db, DB_PATH

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_URL = "https://www.metabolicfitness.cl"
SALIDA = os.path.join(BASE_DIR, "certificados_reconocimiento", "MF-REC-GL01_Guillermo_Leon")
CARPETA_QRS = os.path.join(BASE_DIR, "qrs_diplomas")
LOGO = os.path.join(BASE_DIR, "assets", "brand", "logo-mf-horizontal-white.png")

SERIAL = "MF-REC-GL01"
NOMBRE = "Dr. Guillermo León"
CURSO = (
    "Reconocimiento por su dedicación docente en Fisiología del Ejercicio "
    "en el Adulto Mayor y Fisiología del Entrenamiento de Fuerza en Pediatría"
)
FECHA = "13-09-2026"

# Paleta cercana a los certificados Adulto Mayor / Pediatría
BAR_TOP = (18, 28, 24)
BAR_BOTTOM = (18, 28, 24)
GOLD = (184, 148, 58)
TEXT = (40, 40, 41)
MUTED = (90, 90, 92)


def _register_fonts():
    pdfmetrics.registerFont(TTFont("Arial", r"C:\Windows\Fonts\arial.ttf"))
    pdfmetrics.registerFont(TTFont("Arial-Bold", r"C:\Windows\Fonts\arialbd.ttf"))
    pdfmetrics.registerFont(TTFont("Times", r"C:\Windows\Fonts\times.ttf"))
    pdfmetrics.registerFont(TTFont("Times-Bold", r"C:\Windows\Fonts\timesbd.ttf"))
    script = r"C:\Windows\Fonts\FREESCPT.TTF"
    if os.path.isfile(script):
        pdfmetrics.registerFont(TTFont("Script", script))
    else:
        pdfmetrics.registerFont(TTFont("Script", r"C:\Windows\Fonts\FRSCRIPT.TTF"))


def _png_qr(serial: str) -> bytes:
    url = f"{BASE_URL}/validar.html?serial={serial}"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=1,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#404041", back_color="white")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def _draw_wrapped(c, text, x, y, max_width, font, size, leading, color=TEXT, align="center"):
    c.setFont(font, size)
    c.setFillColorRGB(*(v / 255 for v in color))
    words = text.split()
    lines = []
    current = ""
    for w in words:
        trial = (current + " " + w).strip()
        if c.stringWidth(trial, font, size) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = w
    if current:
        lines.append(current)
    for i, line in enumerate(lines):
        yy = y - i * leading
        if align == "center":
            c.drawCentredString(x, yy, line)
        else:
            c.drawString(x, yy, line)
    return len(lines) * leading


def _build_pdf(path_pdf: str, qr_bytes: bytes):
    _register_fonts()
    page_w, page_h = landscape(A4)
    c = canvas.Canvas(path_pdf, pagesize=landscape(A4))

    # Fondo
    c.setFillColorRGB(1, 1, 1)
    c.rect(0, 0, page_w, page_h, fill=1, stroke=0)

    # Franjas superior e inferior
    bar_h = 52
    c.setFillColorRGB(*(v / 255 for v in BAR_TOP))
    c.rect(0, page_h - bar_h, page_w, bar_h, fill=1, stroke=0)
    c.setFillColorRGB(*(v / 255 for v in BAR_BOTTOM))
    c.rect(0, 0, page_w, bar_h, fill=1, stroke=0)

    # Logo
    if os.path.isfile(LOGO):
        c.drawImage(
            ImageReader(LOGO),
            22,
            page_h - 44,
            width=118,
            height=34,
            mask="auto",
            preserveAspectRatio=True,
            anchor="sw",
        )

    # Título en franja
    c.setFillColorRGB(1, 1, 1)
    c.setFont("Arial-Bold", 18)
    c.drawCentredString(page_w / 2 + 20, page_h - 32, "CERTIFICADO DE RECONOCIMIENTO Y AGRADECIMIENTO")

    # Cuerpo
    cx = page_w / 2
    y = page_h - 95
    c.setFillColorRGB(*(v / 255 for v in MUTED))
    c.setFont("Arial", 12)
    c.drawCentredString(cx, y, "Metabolic Fitness Academy")

    # Línea dorada
    y -= 14
    c.setStrokeColorRGB(*(v / 255 for v in GOLD))
    c.setLineWidth(1.4)
    c.line(cx - 120, y, cx + 120, y)

    y -= 28
    c.setFillColorRGB(*(v / 255 for v in TEXT))
    c.setFont("Arial", 10)
    c.drawCentredString(cx, y, "SE OTORGA EL PRESENTE RECONOCIMIENTO A:")

    y -= 42
    c.setFont("Script", 36)
    c.drawCentredString(cx, y, NOMBRE)

    y -= 28
    c.setFont("Arial", 9)
    c.setFillColorRGB(*(v / 255 for v in MUTED))
    c.drawCentredString(cx, y, "Science y Nature · PhD-MSc · Actividad Física y Salud")

    y -= 30
    texto = (
        "En reconocimiento a su destacada dedicación, rigor práctico e innovación pedagógica "
        "en la conducción y realización de los programas de especialización"
    )
    used = _draw_wrapped(c, texto, cx, y, 520, "Arial", 10, 14, TEXT, "center")

    y -= used + 18
    cursos = [
        "FISIOLOGÍA DEL EJERCICIO EN EL ADULTO MAYOR",
        "FISIOLOGÍA DEL ENTRENAMIENTO DE FUERZA EN PEDIATRÍA",
    ]
    c.setFont("Times-Bold", 13)
    c.setFillColorRGB(*(v / 255 for v in TEXT))
    for i, curso in enumerate(cursos):
        c.drawCentredString(cx, y - i * 18, curso)

    y -= 52
    cierre = (
        "Metabolic Fitness Academy agradece profundamente su compromiso con la formación "
        "de profesionales y su aporte a la fisiología del ejercicio aplicada a la clínica."
    )
    _draw_wrapped(c, cierre, cx, y, 520, "Arial", 9.5, 13, MUTED, "center")

    # Firma izquierda (Director — Fundador)
    sig_x = 95
    sig_y = 105
    c.setStrokeColorRGB(0.55, 0.55, 0.55)
    c.setLineWidth(0.8)
    c.line(sig_x, sig_y + 18, sig_x + 200, sig_y + 18)
    c.setFillColorRGB(*(v / 255 for v in TEXT))
    c.setFont("Arial-Bold", 9)
    c.drawString(sig_x, sig_y, "Israel Orellana R. MSc.")
    c.setFont("Arial", 8)
    c.drawString(sig_x, sig_y - 12, "Fisiología Clínica Del Ejercicio")
    c.drawString(sig_x, sig_y - 24, "IA Engineer")
    c.drawString(sig_x, sig_y - 36, "Director — Fundador Metabolic Fitness")

    # QR derecha
    qr_size = 72
    qr_x = page_w - 118
    qr_y = 78
    c.drawImage(ImageReader(io.BytesIO(qr_bytes)), qr_x, qr_y, width=qr_size, height=qr_size, mask="auto")

    # Pie
    c.setFillColorRGB(1, 1, 1)
    c.setFont("Arial-Bold", 10)
    c.drawString(28, 20, f"SERIAL: {SERIAL}")
    c.drawRightString(page_w - 28, 20, f"FECHA: {FECHA}")

    c.save()


def main():
    init_db()
    os.makedirs(SALIDA, exist_ok=True)
    os.makedirs(CARPETA_QRS, exist_ok=True)

    qr_bytes = _png_qr(SERIAL)
    qr_path = os.path.join(SALIDA, f"QR_{SERIAL}.png")
    with open(qr_path, "wb") as f:
        f.write(qr_bytes)
    with open(os.path.join(CARPETA_QRS, f"QR_{SERIAL}.png"), "wb") as f:
        f.write(qr_bytes)

    pdf_tmp = os.path.join(SALIDA, "_tmp_base.pdf")
    pdf_out = os.path.join(SALIDA, "certificado_con_qr.pdf")
    _build_pdf(pdf_tmp, qr_bytes)

    # Asegura QR embebido también vía PyMuPDF (por si ReportLab lo rasteriza distinto)
    doc = fitz.open(pdf_tmp)
    page = doc[0]
    # el QR ya está dibujado en el PDF base; solo guardamos limpio
    doc.save(pdf_out)
    doc.close()
    try:
        os.remove(pdf_tmp)
    except OSError:
        pass

    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """
        INSERT INTO certificados (serial, nombre_estudiante, curso, fecha)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(serial) DO UPDATE SET
            nombre_estudiante = excluded.nombre_estudiante,
            curso             = excluded.curso,
            fecha             = excluded.fecha
        """,
        (SERIAL, NOMBRE, CURSO, FECHA),
    )
    conn.commit()
    conn.close()

    from exportar_datos_web import main as exportar_web

    exportar_web()

    print(f"[OK] {SERIAL}  {NOMBRE}")
    print(f"     PDF: {pdf_out}")
    print(f"     QR:  {qr_path}")
    print(f"     URL: {BASE_URL}/validar.html?serial={SERIAL}")


if __name__ == "__main__":
    main()
