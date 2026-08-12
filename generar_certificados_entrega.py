# -*- coding: utf-8 -*-
"""
generar_certificados_entrega.py — Certificados PDF + QR + validación web.

Entrega 08-08-2026 · Programa de Especialización
Fisiología del Ejercicio Físico y de la Obesidad

Uso:
    pip install qrcode[pil] reportlab pillow
    python generar_certificados_entrega.py

Salida:
    certificados_entrega/Diploma_MF-FRM-XX_Nombre.pdf
    qrs_diplomas/QR_MF-FRM-XX.png
    certificados.db + certificados-data.js (validación en metabolicfitness.cl)
"""

from __future__ import annotations

import os
import sqlite3
import sys

import qrcode
from PIL import Image, ImageDraw
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

from database import init_db, DB_PATH

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_URL = "https://www.metabolicfitness.cl"
CARPETA_QRS = os.path.join(BASE_DIR, "qrs_diplomas")
CARPETA_SALIDA = os.path.join(BASE_DIR, "certificados_entrega")

PROGRAMA = "Programa de Especialización"
CURSO = "Fisiología del Ejercicio Físico y de la Obesidad"
CURSO_TITULO_PDF = "FISIOLOGÍA DEL EJERCICIO FÍSICO Y DE LA OBESIDAD"
FECHA = "08-08-2026"

PURPLE = HexColor("#401750")
PURPLE_LIGHT = HexColor("#E8DCEF")
TEAL = HexColor("#2A9D8F")
GREY = HexColor("#6B7280")
WHITE = HexColor("#FFFFFF")
BLACK = HexColor("#1A1A1A")

# Entrega 08-08-2026 (seriales MF-FRM-20 … MF-FRM-28)
ESTUDIANTES = {
    20: "Vicente Bugueño Alfaro",
    21: "Ana Colina Correa",
    22: "Hernán Carrasco",
    23: "Sofía Garfias Cruz",
    24: "Eric Bello Bautista",
    25: "Tatiana Ramírez de Plaza",
    26: "Nermari Aular",
    27: "Héctor Mario Bustos",
    28: "Silvia Sánchez Cárdenas",
}


def _registrar_fuente(nombre: str, candidatos: list[str]) -> str | None:
    for path in candidatos:
        if os.path.isfile(path):
            try:
                pdfmetrics.registerFont(TTFont(nombre, path))
                return nombre
            except Exception:
                continue
    return None


def _init_fuentes():
    script = _registrar_fuente(
        "MFScript",
        [
            os.path.join(BASE_DIR, "assets", "fonts", "GreatVibes-Regular.ttf"),
            r"C:\Windows\Fonts\FREESCPT.TTF",
            r"C:\Windows\Fonts\BRUSHSCI.TTF",
            r"C:\Windows\Fonts\ITCEDSCR.TTF",
        ],
    )
    serif = _registrar_fuente(
        "MFSerif",
        [
            os.path.join(BASE_DIR, "assets", "fonts", "PlayfairDisplay-Bold.ttf"),
            r"C:\Windows\Fonts\timesbd.ttf",
            r"C:\Windows\Fonts\times.ttf",
        ],
    )
    sans = _registrar_fuente(
        "MFSans",
        [
            os.path.join(BASE_DIR, "assets", "fonts", "Montserrat-Bold.ttf"),
            r"C:\Windows\Fonts\arialbd.ttf",
            r"C:\Windows\Fonts\arial.ttf",
        ],
    )
    sans_reg = _registrar_fuente(
        "MFSansReg",
        [
            os.path.join(BASE_DIR, "assets", "fonts", "Montserrat-Regular.ttf"),
            r"C:\Windows\Fonts\arial.ttf",
        ],
    )
    return {
        "script": script or "Helvetica-Oblique",
        "serif": serif or "Times-Bold",
        "sans": sans or "Helvetica-Bold",
        "sans_reg": sans_reg or "Helvetica",
    }


def _generar_qr(serial: str) -> str:
    os.makedirs(CARPETA_QRS, exist_ok=True)
    url = f"{BASE_URL}/validar.html?serial={serial}"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=12,
        border=2,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#404041", back_color="white")
    ruta = os.path.join(CARPETA_QRS, f"QR_{serial}.png")
    img.save(ruta)
    return ruta


def _dibujar_sello(c: canvas.Canvas, cx: float, cy: float, r: float):
    c.setStrokeColor(GREY)
    c.setFillColor(HexColor("#F3F4F6"))
    c.setLineWidth(1)
    c.circle(cx, cy, r, stroke=1, fill=1)
    c.setFillColor(GREY)
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(cx, cy - 6, "✓")


def _nombre_archivo_seguro(nombre: str) -> str:
    limpio = "".join(ch if ch.isalnum() or ch in " -_" else "_" for ch in nombre)
    return limpio.replace(" ", "_")[:60]


def generar_pdf(serial: str, nombre: str, qr_path: str, fonts: dict) -> str:
    os.makedirs(CARPETA_SALIDA, exist_ok=True)
    page_w, page_h = landscape(A4)
    out = os.path.join(
        CARPETA_SALIDA,
        f"Diploma_{serial}_{_nombre_archivo_seguro(nombre)}.pdf",
    )

    c = canvas.Canvas(out, pagesize=landscape(A4))
    bar_h = 22 * mm

    # Barras superior e inferior
    c.setFillColor(PURPLE)
    c.rect(0, page_h - bar_h, page_w, bar_h, fill=1, stroke=0)
    c.rect(0, 0, page_w, bar_h, fill=1, stroke=0)

    # Logo texto (header)
    c.setFillColor(WHITE)
    c.setFont(fonts["sans"], 14)
    c.drawString(18 * mm, page_h - bar_h + 11 * mm, "METABOLIC")
    c.setFont(fonts["sans_reg"], 8)
    c.drawString(18 * mm, page_h - bar_h + 6 * mm, "FITNESS")

    # Título header
    c.setFont(fonts["sans"], 16)
    c.drawCentredString(page_w / 2, page_h - bar_h + 9 * mm, "CERTIFICADO DE FINALIZACIÓN")

    # Marca de agua molecular (sutil)
    c.setStrokeColor(PURPLE_LIGHT)
    c.setLineWidth(0.6)
    mx, my = page_w - 45 * mm, page_h - 55 * mm
    for dx, dy in [(0, 0), (8, 5), (-6, 8), (10, -4)]:
        c.circle(mx + dx, my + dy, 3 * mm, stroke=1, fill=0)

    # Programa
    c.setFillColor(BLACK)
    c.setFont(fonts["sans_reg"], 13)
    c.drawCentredString(page_w / 2, page_h - bar_h - 22 * mm, PROGRAMA)

    # Línea gradiente simulada
    gx = page_w / 2 - 35 * mm
    gy = page_h - bar_h - 27 * mm
    c.setStrokeColor(PURPLE)
    c.setLineWidth(2)
    c.line(gx, gy, gx + 35 * mm, gy)
    c.setStrokeColor(TEAL)
    c.line(gx + 35 * mm, gy, gx + 70 * mm, gy)

    c.setFont(fonts["sans_reg"], 9)
    c.drawCentredString(page_w / 2, page_h - bar_h - 36 * mm, "SE OTORGA EL PRESENTE DIPLOMA A:")

    # Nombre (script)
    c.setFont(fonts["script"], 28)
    c.drawCentredString(page_w / 2, page_h - bar_h - 52 * mm, nombre)

    c.setFont(fonts["sans_reg"], 9)
    c.drawCentredString(
        page_w / 2, page_h - bar_h - 62 * mm, "POR LA APROBACIÓN SATISFACTORIA DEL CURSO:"
    )

    # Título del curso (serif, mayúsculas)
    c.setFont(fonts["serif"], 15)
    c.drawCentredString(page_w / 2, page_h - bar_h - 74 * mm, CURSO_TITULO_PDF)

    # Firma
    sig_x = 42 * mm
    sig_y = 38 * mm
    c.setStrokeColor(BLACK)
    c.setLineWidth(0.8)
    c.line(sig_x, sig_y + 8 * mm, sig_x + 55 * mm, sig_y + 8 * mm)
    c.setFont("Helvetica-Oblique", 10)
    c.setFillColor(BLACK)
    c.drawString(sig_x, sig_y + 2 * mm, "Carlos Saavedra MSc. / Univ Laval, Canadá.")

    # Sello verificación
    _dibujar_sello(c, page_w / 2, 48 * mm, 10 * mm)

    # QR
    qr_size = 32 * mm
    qr_x = page_w - 52 * mm
    qr_y = 28 * mm
    if os.path.isfile(qr_path):
        c.drawImage(ImageReader(qr_path), qr_x, qr_y, qr_size, qr_size, mask="auto")

    # Footer
    c.setFillColor(WHITE)
    c.setFont(fonts["sans"], 11)
    c.drawString(18 * mm, 8 * mm, f"SERIAL: {serial}")
    c.drawRightString(page_w - 18 * mm, 8 * mm, f"FECHA: {FECHA}")

    c.showPage()
    c.save()
    return out


def _guardar_db(conn: sqlite3.Connection, serial: str, nombre: str):
    conn.execute(
        """
        INSERT INTO certificados (serial, nombre_estudiante, curso, fecha)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(serial) DO UPDATE SET
            nombre_estudiante = excluded.nombre_estudiante,
            curso             = excluded.curso,
            fecha             = excluded.fecha
        """,
        (serial, nombre, CURSO, FECHA),
    )


def main():
    init_db()
    os.makedirs(CARPETA_SALIDA, exist_ok=True)
    fonts = _init_fuentes()
    conn = sqlite3.connect(DB_PATH)

    pdfs = []
    for numero, nombre in ESTUDIANTES.items():
        serial = f"MF-FRM-{numero:02d}"
        _guardar_db(conn, serial, nombre)
        qr_path = _generar_qr(serial)
        pdf_path = generar_pdf(serial, nombre, qr_path, fonts)
        pdfs.append(pdf_path)
        print(f"[OK] {serial}  {nombre}")
        print(f"     PDF: {pdf_path}")
        print(f"     QR : {qr_path}")
        print(f"     URL: {BASE_URL}/validar.html?serial={serial}")

    conn.commit()
    conn.close()

    try:
        from exportar_datos_web import main as exportar_web

        exportar_web()
        print("\n[OK] certificados-data.js actualizado para validación web.")
    except Exception as exc:
        print(f"\nAviso: no se pudo exportar certificados-data.js: {exc}")

    print(f"\nListo. {len(pdfs)} certificados en: {CARPETA_SALIDA}")


if __name__ == "__main__":
    main()
