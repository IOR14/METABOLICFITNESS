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

# Certificados alineados con los diplomas impresos (MF-FRM-02 … MF-FRM-18)
CERTIFICADOS = [
    {
        "numero": 2,
        "nombre": "Antonio Paez",
        "curso": "Obesidad y Rehabilitación Metabólica - Nivel Inicial",
        "fecha": "20-05-2024",
    },
    {
        "numero": 3,
        "nombre": "Ricardo Escobar",
        "curso": "Obesidad y Rehabilitación Metabólica - Nivel Inicial",
        "fecha": "20-05-2024",
    },
    {
        "numero": 4,
        "nombre": "Claudia Corrales",
        "curso": "Obesidad y Rehabilitación Metabólica - Nivel Inicial",
        "fecha": "20-05-2024",
    },
    {
        "numero": 5,
        "nombre": "Omar Potočnik",
        "curso": "Obesidad y Rehabilitación Metabólica - Nivel Inicial",
        "fecha": "20-05-2024",
    },
    {
        "numero": 6,
        "nombre": "Sofia Garfias",
        "curso": "Obesidad y Rehabilitación Metabólica - Nivel Inicial",
        "fecha": "20-05-2024",
    },
    {
        "numero": 7,
        "nombre": "Gerardo Alvarado",
        "curso": "Obesidad y Rehabilitación Metabólica - Nivel Inicial",
        "fecha": "20-05-2024",
    },
    {
        "numero": 8,
        "nombre": "Lisbeth Casarrubia",
        "curso": "Obesidad y Rehabilitación Metabólica - Nivel Inicial",
        "fecha": "20-05-2024",
    },
    {
        "numero": 9,
        "nombre": "Ramon Sepulveda",
        "curso": "Obesidad y Rehabilitación Metabólica - Nivel Inicial",
        "fecha": "20-05-2024",
    },
    {
        "numero": 10,
        "nombre": "Javier Cañete",
        "curso": "Obesidad y Rehabilitación Metabólica - Nivel Inicial",
        "fecha": "20-05-2024",
    },
    {
        "numero": 11,
        "nombre": "Vicente Vila",
        "curso": "Diploma en Entrenamiento Metabólico - Método 1X2X3",
        "fecha": "05-05-2024",
    },
    {
        "numero": 12,
        "nombre": "Hannia Varela",
        "curso": "Diploma en Entrenamiento Metabólico - Método 1X2X3",
        "fecha": "05-05-2024",
    },
    {
        "numero": 13,
        "nombre": "Alan Guzmán",
        "curso": "Diploma en Entrenamiento Metabólico - Método 1X2X3",
        "fecha": "05-05-2024",
    },
    {
        "numero": 14,
        "nombre": "Felix Miranda",
        "curso": "Diploma en Entrenamiento Metabólico - Método 1X2X3",
        "fecha": "05-05-2024",
    },
    {
        "numero": 15,
        "nombre": "David Barria",
        "curso": "Diploma en Entrenamiento Metabólico - Método 1X2X3",
        "fecha": "05-05-2024",
    },
    {
        "numero": 16,
        "nombre": "Luis Rogelio",
        "curso": "Diploma en Entrenamiento Metabólico - Método 1X2X3",
        "fecha": "05-05-2024",
    },
    {
        "numero": 17,
        "nombre": "Fernando González",
        "curso": "Diploma en Entrenamiento Metabólico - Método 1X2X3",
        "fecha": "05-05-2024",
    },
    {
        "numero": 18,
        "nombre": "Cristina Barra",
        "curso": "Diploma en Entrenamiento Metabólico - Método 1X2X3",
        "fecha": "05-05-2024",
    },
]

# Carpeta donde se guardarán las imágenes de los QR
CARPETA_QRS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "qrs_diplomas")


def main():
    init_db()
    os.makedirs(CARPETA_QRS, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    total = 0
    for cert in CERTIFICADOS:
        serial = "MF-FRM-{:02d}".format(cert["numero"])
        nombre = cert["nombre"]
        curso = cert["curso"]
        fecha = cert["fecha"]

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
