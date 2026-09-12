# -*- coding: utf-8 -*-
"""
generar_diploma_celular_completo.py

Genera QR + PDF con QR incrustado para el Diploma en Fisiología Celular
(del zip oficial). Seriales impresos: MF-DP-F01 … MF-DP-F09.

Salida por alumno (carpeta ordenada):
    certificados_diploma_celular/01_MF-DP-F01_Nombre/
        certificado_con_qr.pdf
        QR_MF-DP-F01.png

También copia QR a qrs_diplomas/ y actualiza certificados.db + certificados-data.js.
No modifica diseño del PDF (solo superpone el QR).

Uso:
    pip install qrcode[pil] pymupdf pillow
    python generar_diploma_celular_completo.py
"""

from __future__ import annotations

import io
import os
import re
import shutil
import sqlite3
import sys

import fitz
import qrcode

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

from database import init_db, DB_PATH

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_URL = "https://www.metabolicfitness.cl"
ZIP_DIR = os.path.join(BASE_DIR, "_cert_celular_zip")
ORIGINALES = os.path.join(BASE_DIR, "assets", "certificados", "diploma_celular_originales")
SALIDA_BASE = os.path.join(BASE_DIR, "certificados_diploma_celular")
CARPETA_QRS = os.path.join(BASE_DIR, "qrs_diplomas")

CURSO = "Diploma Fisiología Celular del Ejercicio Aplicada a la Salud"
FECHA = "01-09-2026"

# Datos leídos de los PDF 1.pdf … 8.pdf (serial impreso en pie de página)
DIPLOMAS = [
    {"orden": 1, "serial": "MF-DP-F01", "nombre": "Vicente Vidal", "origen": "1.pdf"},
    {"orden": 2, "serial": "MF-DP-F02", "nombre": "Luis Rogelio Gutiérrez Camacho", "origen": "2.pdf"},
    {"orden": 3, "serial": "MF-DP-F03", "nombre": "Hannia Varela", "origen": "3.pdf"},
    {"orden": 4, "serial": "MF-DP-F04", "nombre": "Alan Guzmán", "origen": "4.pdf"},
    {"orden": 5, "serial": "MF-DP-F05", "nombre": "Cristina Barra", "origen": "5.pdf"},
    {"orden": 6, "serial": "MF-DP-F06", "nombre": "David Barria", "origen": "6.pdf"},
    {"orden": 7, "serial": "MF-DP-F07", "nombre": "Fernando González", "origen": "7.pdf"},
    {"orden": 8, "serial": "MF-DP-F08", "nombre": "Orlando Rodríguez", "origen": "8.pdf"},
    {"orden": 9, "serial": "MF-DP-F09", "nombre": "Felix Miranda", "origen": "9.pdf"},
]

# Posición calibrada (pt PDF): QR sobre la célula, sin tocar textos centrales
QR_RECT = fitz.Rect(625, 392, 715, 482)

SERIALES_ERRONEOS = [f"MF-FRM-{n:02d}" for n in range(29, 37)]


def _slug(nombre: str) -> str:
    limpio = re.sub(r"[^\w\s-]", "", nombre, flags=re.UNICODE)
    limpio = limpio.replace(" ", "_")
    return limpio[:55]


def _resolver_pdf(item: dict) -> str:
    for base in (ORIGINALES, ZIP_DIR):
        ruta = os.path.join(base, item["origen"])
        if os.path.isfile(ruta):
            return ruta
    raise FileNotFoundError(
        f"No se encuentra {item['origen']}. Extrae el zip en {ZIP_DIR} "
        f"o copia los PDF a {ORIGINALES}"
    )


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


def _sync_otros_certificados(conn: sqlite3.Connection) -> None:
    try:
        from generar_certificados_entrega import ESTUDIANTES as ENTREGA, CURSO as C1, FECHA as F1
    except ImportError:
        ENTREGA, C1, F1 = {}, "", ""
    for numero, nombre in ENTREGA.items():
        serial = f"MF-FRM-{numero:02d}"
        conn.execute(
            """
            INSERT INTO certificados (serial, nombre_estudiante, curso, fecha)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(serial) DO NOTHING
            """,
            (serial, nombre, C1, F1),
        )


def _limpiar_registros_incorrectos(conn: sqlite3.Connection) -> None:
    for serial in SERIALES_ERRONEOS:
        conn.execute("DELETE FROM certificados WHERE serial = ?", (serial,))


def main():
    init_db()
    os.makedirs(SALIDA_BASE, exist_ok=True)
    os.makedirs(CARPETA_QRS, exist_ok=True)
    os.makedirs(ORIGINALES, exist_ok=True)

    for item in DIPLOMAS:
        src = _resolver_pdf(item)
        dst_orig = os.path.join(ORIGINALES, item["origen"])
        if os.path.abspath(src) != os.path.abspath(dst_orig):
            shutil.copy2(src, dst_orig)

    conn = sqlite3.connect(DB_PATH)
    _sync_otros_certificados(conn)
    _limpiar_registros_incorrectos(conn)

    for item in DIPLOMAS:
        serial = item["serial"]
        nombre = item["nombre"]
        orden = item["orden"]
        pdf_src = _resolver_pdf(item)

        png_bytes = _png_qr(serial)
        carpeta = os.path.join(
            SALIDA_BASE,
            f"{orden:02d}_{serial}_{_slug(nombre)}",
        )
        os.makedirs(carpeta, exist_ok=True)

        qr_path = os.path.join(carpeta, f"QR_{serial}.png")
        with open(qr_path, "wb") as f:
            f.write(png_bytes)

        qr_global = os.path.join(CARPETA_QRS, f"QR_{serial}.png")
        with open(qr_global, "wb") as f:
            f.write(png_bytes)

        out_pdf = os.path.join(carpeta, "certificado_con_qr.pdf")
        doc = fitz.open(pdf_src)
        page = doc[0]
        page.insert_image(QR_RECT, stream=png_bytes, overlay=True)
        doc.save(out_pdf)
        doc.close()

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

        print(f"[OK] {serial}  {nombre}")
        print(f"     PDF: {out_pdf}")
        print(f"     URL: {BASE_URL}/validar.html?serial={serial}")

    conn.commit()
    conn.close()

    for serial in SERIALES_ERRONEOS:
        ruta = os.path.join(CARPETA_QRS, f"QR_{serial}.png")
        if os.path.isfile(ruta):
            os.remove(ruta)

    from exportar_datos_web import main as exportar_web

    exportar_web()
    print(f"\nListo. {len(DIPLOMAS)} diplomas en: {SALIDA_BASE}")


if __name__ == "__main__":
    main()
