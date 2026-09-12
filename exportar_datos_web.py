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
import re
import sqlite3

from database import DB_PATH

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SALIDA_JS = os.path.join(BASE_DIR, "certificados-data.js")
VALIDAR_HTML = os.path.join(BASE_DIR, "validar.html")


def _serial_sort_key(serial: str):
    """Orden lógico MF-FRM-NN / MF-DP-FNN para cache-bust."""
    m = re.match(r"^MF-(FRM|DP)-F?(\d+)$", serial.strip().upper())
    if not m:
        return (9, serial)
    fam = 0 if m.group(1) == "FRM" else 1
    return (fam, int(m.group(2)))


def _actualizar_cache_validar_html(cache_tag: str) -> None:
    """Fuerza recarga del JS de certificados en validar.html (evita caché del navegador)."""
    if not os.path.isfile(VALIDAR_HTML):
        return
    with open(VALIDAR_HTML, encoding="utf-8") as f:
        html = f.read()
    nuevo = re.sub(
        r'(certificados-data\.js\?v=)[^"\']+',
        r"\g<1>" + cache_tag,
        html,
        count=1,
    )
    if nuevo != html:
        with open(VALIDAR_HTML, "w", encoding="utf-8") as f:
            f.write(nuevo)
        print("Cache validar.html actualizado: certificados-data.js?v={}".format(cache_tag))


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
        "// version: {} certificados ({})\n".format(len(data), max(data.keys()) if data else "none")
        + "window.CERTIFICADOS = "
        + json.dumps(data, ensure_ascii=False, indent=2)
        + ";\n"
    )

    with open(SALIDA_JS, "w", encoding="utf-8") as f:
        f.write(contenido)

    ultimo = max(data.keys(), key=_serial_sort_key) if data else "none"
    cache_tag = "{}-{}".format(len(data), ultimo)
    _actualizar_cache_validar_html(cache_tag)

    print("Archivo generado: {}".format(SALIDA_JS))
    print("Certificados exportados: {}".format(len(data)))


if __name__ == "__main__":
    main()
