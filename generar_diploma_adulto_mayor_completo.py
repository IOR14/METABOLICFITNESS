# -*- coding: utf-8 -*-
"""
generar_diploma_adulto_mayor_completo.py

Diploma: Fisiología del Ejercicio en el Adulto Mayor (zip oficial).
Seriales impresos: MF-AD-F01 … MF-AD-F07.

Salida:
    certificados_adulto_mayor/01_MF-AD-F01_Nombre/
        certificado_con_qr.pdf
        QR_MF-AD-F01.png

Uso:
    pip install qrcode[pil] pymupdf
    python generar_diploma_adulto_mayor_completo.py
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
ZIP_DIR = os.path.join(BASE_DIR, "_cert_adulto_mayor_zip")
ORIGINALES = os.path.join(BASE_DIR, "assets", "certificados", "adulto_mayor_originales")
SALIDA_BASE = os.path.join(BASE_DIR, "certificados_adulto_mayor")
CARPETA_QRS = os.path.join(BASE_DIR, "qrs_diplomas")

CURSO = "Programa de Especialización — Fisiología del Ejercicio en el Adulto Mayor"
FECHA = "01-09-2026"

DIPLOMAS = [
    {"orden": 1, "serial": "MF-AD-F01", "nombre": "Vicente Vidal", "origen": "1.pdf"},
    {"orden": 2, "serial": "MF-AD-F02", "nombre": "Cristina Barra", "origen": "2.pdf"},
    {"orden": 3, "serial": "MF-AD-F03", "nombre": "Karla Brigitte González Sánchez", "origen": "3.pdf"},
    {"orden": 4, "serial": "MF-AD-F04", "nombre": "Ignacio Javier Calbete", "origen": "4.pdf"},
    {"orden": 5, "serial": "MF-AD-F05", "nombre": "Saúl Morales Aguas", "origen": "5.pdf"},
    {"orden": 6, "serial": "MF-AD-F06", "nombre": "Frida Licea Licona", "origen": "6.pdf"},
    {"orden": 7, "serial": "MF-AD-F07", "nombre": "José Luis Santana Vargas", "origen": "7.pdf"},
]

QR_RECT = fitz.Rect(625, 392, 715, 482)


def _slug(nombre: str) -> str:
    limpio = re.sub(r"[^\w\s-]", "", nombre, flags=re.UNICODE)
    return limpio.replace(" ", "_")[:55]


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


def _preservar_registros_existentes(conn: sqlite3.Connection) -> None:
    """No borra otros programas; solo asegura lotes anteriores si faltan en DB."""
    try:
        from generar_certificados_entrega import ESTUDIANTES as E1, CURSO as C1, FECHA as F1
    except ImportError:
        E1 = {}
        C1 = F1 = ""
    for numero, nombre in E1.items():
        conn.execute(
            """
            INSERT INTO certificados (serial, nombre_estudiante, curso, fecha)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(serial) DO NOTHING
            """,
            (f"MF-FRM-{numero:02d}", nombre, C1, F1),
        )
    try:
        from generar_diploma_celular_completo import DIPLOMAS as CEL, CURSO as C2, FECHA as F2
    except ImportError:
        CEL = []
        C2 = F2 = ""
    for item in CEL:
        conn.execute(
            """
            INSERT INTO certificados (serial, nombre_estudiante, curso, fecha)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(serial) DO NOTHING
            """,
            (item["serial"], item["nombre"], C2, F2),
        )


def main():
    init_db()
    os.makedirs(SALIDA_BASE, exist_ok=True)
    os.makedirs(CARPETA_QRS, exist_ok=True)
    os.makedirs(ORIGINALES, exist_ok=True)

    for item in DIPLOMAS:
        src = _resolver_pdf(item)
        dst = os.path.join(ORIGINALES, item["origen"])
        if os.path.abspath(src) != os.path.abspath(dst):
            shutil.copy2(src, dst)

    conn = sqlite3.connect(DB_PATH)
    _preservar_registros_existentes(conn)

    for item in DIPLOMAS:
        serial = item["serial"]
        nombre = item["nombre"]
        pdf_src = _resolver_pdf(item)
        png_bytes = _png_qr(serial)

        carpeta = os.path.join(
            SALIDA_BASE,
            f"{item['orden']:02d}_{serial}_{_slug(nombre)}",
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
        doc[0].insert_image(QR_RECT, stream=png_bytes, overlay=True)
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

    from exportar_datos_web import main as exportar_web

    exportar_web()
    print(f"\nListo. {len(DIPLOMAS)} diplomas en: {SALIDA_BASE}")


if __name__ == "__main__":
    main()
