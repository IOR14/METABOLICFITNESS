# -*- coding: utf-8 -*-
"""
generar_qrs.py — Puebla la base de datos certificados.db con los 17 estudiantes
del curso y genera un código QR (imagen PNG) por cada certificado.

Cómo ejecutar:
    1) pip install qrcode[pil]
    2) python generar_qrs.py

Resultado:
    - Inserta/actualiza los 17 registros en la tabla 'certificados'.
    - Crea la carpeta 'qrs_diplomas' con un QR por estudiante:
      QR_MF-FRM-02.png, QR_MF-FRM-03.png, ...
"""

import os
import sys
import sqlite3
import qrcode

# La consola de Windows usa cp1252 por defecto y no puede mostrar algunos
# caracteres (ej: la "č" de Potočnik). Forzamos UTF-8 en la salida.
try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

# Reutilizamos la base de datos y la creación de tabla ya definidas en database.py
from database import init_db, DB_PATH

# URL pública del sitio en GitHub Pages
BASE_URL = "https://ior14.github.io/METABOLICFITNESS"

# Datos oficiales del certificado (MF-FRM-02 … MF-FRM-18)
CURSO = "Fisiología en Rehabilitación Metabólica - Método 1X2X3"
FECHA = "06-06-2026"

ESTUDIANTES = {
    2: "Antonio Paez",
    3: "Ricardo Escobar",
    4: "Claudia Corrales",
    5: "Omar Potóchník",
    6: "Sofia Garfias",
    7: "Gerardo Alvarado",
    8: "Lisbeth Casarrubia",
    9: "Ramon Sepulveda",
    10: "Javier Cañete",
    11: "Vicente Vila",
    12: "Hannia Varela",
    13: "Alan Guzmán",
    14: "Felix Miranda",
    15: "David Barria",
    16: "Luis Rogelio",
    17: "Fernando González",
    18: "Cristina Barra",
}

# Carpeta donde se guardarán las imágenes de los QR
CARPETA_QRS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "qrs_diplomas")


def main():
    init_db()
    os.makedirs(CARPETA_QRS, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    total = 0
    for numero, nombre in ESTUDIANTES.items():
        serial = "MF-FRM-{:02d}".format(numero)
        curso = CURSO
        fecha = FECHA

        cur.execute(
            """
            INSERT INTO certificados (serial, nombre_estudiante, curso, fecha)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(serial) DO UPDATE SET
                nombre_estudiante = excluded.nombre_estudiante,
                curso             = excluded.curso,
                fecha             = excluded.fecha
            """,
            (serial, nombre, curso, fecha),
        )

        url = "{}/validar?serial={}".format(BASE_URL, serial)
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="#404041", back_color="white")

        ruta_img = os.path.join(CARPETA_QRS, "QR_{}.png".format(serial))
        img.save(ruta_img)

        total += 1
        print("[OK] {}  ->  {}".format(serial, nombre))
        print("     URL : {}".format(url))
        print("     QR  : {}".format(ruta_img))

    conn.commit()
    conn.close()

    try:
        from exportar_datos_web import main as exportar_web
        exportar_web()
    except Exception as e:
        print("Aviso: no se pudo exportar certificados-data.js automáticamente:", e)

    print("\nListo. {} certificados procesados.".format(total))
    print("Imágenes QR guardadas en: {}".format(CARPETA_QRS))


if __name__ == "__main__":
    main()
