# -*- coding: utf-8 -*-
"""
exportar_datos_web.py — Exporta los certificados de la base SQLite a un archivo
JavaScript estático (certificados-data.js) que usa la página validar.html.

Esto permite validar los certificados SIN servidor (ideal para Netlify u otro
hosting estático): los datos viajan en un .js y la validación ocurre en el
navegador del visitante.

Cómo ejecutar:
    python exportar_datos_web.py

Resultado:
    - Crea/actualiza 'certificados-data.js' con todos los certificados.
"""

import os
import json
import sqlite3

from database import DB_PATH

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SALIDA_JS = os.path.join(BASE_DIR, "certificados-data.js")


def main():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    filas = conn.execute(
        "SELECT serial, nombre_estudiante, curso, fecha FROM certificados ORDER BY serial"
    ).fetchall()
    conn.close()

    data = {
        fila["serial"]: {
            "nombre_estudiante": fila["nombre_estudiante"],
            "curso": fila["curso"],
            "fecha": fila["fecha"],
        }
        for fila in filas
    }

    contenido = (
        "// Archivo generado automaticamente por exportar_datos_web.py\n"
        "// NO editar a mano. Para actualizar: python exportar_datos_web.py\n"
        "window.CERTIFICADOS = "
        + json.dumps(data, ensure_ascii=False, indent=2)
        + ";\n"
    )

    with open(SALIDA_JS, "w", encoding="utf-8") as f:
        f.write(contenido)

    print("Archivo generado: {}".format(SALIDA_JS))
    print("Certificados exportados: {}".format(len(data)))


if __name__ == "__main__":
    main()
