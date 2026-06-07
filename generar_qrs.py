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

# ===========================================================================
#  IMPORTANTE: cambia BASE_URL por tu URL real de GitHub Pages.
#  Ejemplos:
#     - Sitio de usuario:  'https://TU-USUARIO.github.io'
#     - Sitio de proyecto: 'https://TU-USUARIO.github.io/NOMBRE-REPO'
#  El QR apuntará a:  <BASE_URL>/validar.html?serial=MF-FRM-XX
# ===========================================================================
BASE_URL = "https://TU-USUARIO.github.io/NOMBRE-REPO"

# Datos comunes a todos los certificados
CURSO = "Fisiología en Rehabilitación Metabólica - Método 1X2X3"
FECHA = "06-06-2026"

# Lista exacta de estudiantes (clave = número, valor = nombre)
ESTUDIANTES = {
    2: "Antonio Ruíz",
    3: "Ricardo Escobar",
    4: "Claudia Corrales",
    5: "Omar Potočnik",
    6: "Sofia Garfias",
    7: "Gerardo Alvarado",
    8: "Ixchell Cuaranta",
    9: "Ramón Sepúlveda",
    10: "Javier Calbete",
    11: "Vicente Vidal",
    12: "Hannia Varela",
    13: "Alan Guzman",
    14: "Felix Miranda",
    15: "David Barria",
    16: "Luis Rogelio",
    17: "Fernando González",
    18: "Cristina Barra",
}

# Carpeta donde se guardarán las imágenes de los QR
CARPETA_QRS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "qrs_diplomas")


def main():
    # 1) Aseguramos que la tabla 'certificados' exista
    init_db()

    # 2) Creamos la carpeta de salida si no existe
    os.makedirs(CARPETA_QRS, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    total = 0
    for numero, nombre in ESTUDIANTES.items():
        # Serial con número a dos dígitos -> MF-FRM-02, MF-FRM-03, ...
        serial = "MF-FRM-{:02d}".format(numero)

        # 3) Insertar o actualizar el registro en la base de datos
        cur.execute(
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

        # 4) Generar el código QR con la URL de validación
        url = "{}/validar.html?serial={}".format(BASE_URL, serial)
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

    # Mantiene sincronizado el archivo de datos que usa la web estática (Netlify).
    try:
        from exportar_datos_web import main as exportar_web
        exportar_web()
    except Exception as e:
        print("Aviso: no se pudo exportar certificados-data.js automáticamente:", e)

    print("\nListo. {} certificados procesados.".format(total))
    print("Imágenes QR guardadas en: {}".format(CARPETA_QRS))
    if "TUDOMINIO.com" in BASE_URL:
        print("\n*** RECUERDA: cambia 'TUDOMINIO.com' por tu dominio real en BASE_URL "
              "y vuelve a ejecutar el script para regenerar los QR. ***")


if __name__ == "__main__":
    main()
