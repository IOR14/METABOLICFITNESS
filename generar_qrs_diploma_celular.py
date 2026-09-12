# -*- coding: utf-8 -*-
"""
generar_qrs_diploma_celular.py — QR + registro web para el Diploma en
Fisiología Celular del Ejercicio Aplicada a la Salud.

No modifica ni borra certificados/QR anteriores (MF-FRM-02 … MF-FRM-28).
Asigna seriales nuevos MF-FRM-29 … MF-FRM-36.

Uso:
    pip install qrcode[pil]
    python generar_qrs_diploma_celular.py
"""

from __future__ import annotations

import os
import sqlite3
import sys

import qrcode

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

from database import init_db, DB_PATH

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_URL = "https://www.metabolicfitness.cl"
CARPETA_QRS = os.path.join(BASE_DIR, "qrs_diplomas")

CURSO = "Diploma en Fisiología Celular del Ejercicio Aplicada a la Salud"
FECHA = "09-03-2026"

# Orden según diplomas impresos (1 … 8 en la planilla)
ESTUDIANTES = {
    29: "Vicente Vidal",
    30: "Luis Rogelio Gutiérrez Camacho",
    31: "Hernán Varela",
    32: "Ana Guzmán",
    33: "Cristina Barría",
    34: "David Barría",
    35: "Fernando González",
    36: "Orlando Rodríguez",
}


def _sync_entrega_obesidad(conn: sqlite3.Connection) -> None:
    """Asegura MF-FRM-20…28 en la DB sin tocar 02…19 ni otros cursos."""
    try:
        from generar_certificados_entrega import ESTUDIANTES as ENTREGA, CURSO as C_ENTREGA, FECHA as F_ENTREGA
    except ImportError:
        return
    for numero, nombre in ENTREGA.items():
        serial = f"MF-FRM-{numero:02d}"
        conn.execute(
            """
            INSERT INTO certificados (serial, nombre_estudiante, curso, fecha)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(serial) DO NOTHING
            """,
            (serial, nombre, C_ENTREGA, F_ENTREGA),
        )


def _generar_qr(serial: str) -> tuple[str, str]:
    os.makedirs(CARPETA_QRS, exist_ok=True)
    url = f"{BASE_URL}/validar.html?serial={serial}"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=12,
        border=1,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#404041", back_color="white")
    ruta = os.path.join(CARPETA_QRS, f"QR_{serial}.png")
    img.save(ruta)
    return url, ruta


def main():
    init_db()
    conn = sqlite3.connect(DB_PATH)
    _sync_entrega_obesidad(conn)

    for numero, nombre in ESTUDIANTES.items():
        serial = f"MF-FRM-{numero:02d}"
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
        url, ruta = _generar_qr(serial)
        print(f"[OK] {serial}  {nombre}")
        print(f"     Validar: {url}")
        print(f"     QR:      {ruta}")

    conn.commit()
    conn.close()

    from exportar_datos_web import main as exportar_web

    exportar_web()
    print(f"\nListo. {len(ESTUDIANTES)} QR nuevos (MF-FRM-29 … MF-FRM-36).")
    print("Coloca cada PNG en el cuadro QR del diploma correspondiente.")


if __name__ == "__main__":
    main()
