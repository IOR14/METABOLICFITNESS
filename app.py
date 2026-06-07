"""
app.py — Servidor Flask para Metabolic Fitness.

Sirve tu sitio web actual TAL CUAL está (todos los .html, imágenes, CSS y JS
quedan en la raíz del proyecto, no hace falta moverlos) y agrega el sistema
de validación de certificados en la ruta /validar.

Cómo ejecutar:
    1) pip install -r requirements.txt
    2) python database.py        (solo la primera vez, crea la base de datos)
    3) python app.py
    4) Abre en el navegador: http://127.0.0.1:5000
"""

import os
from flask import Flask, request, render_template, send_from_directory, abort

from database import init_db, seed_data, buscar_certificado

# Carpeta raíz del proyecto (donde están index.html, academia.html, imágenes, etc.)
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# template_folder='templates' -> aquí vive validar.html (lo usa Jinja2)
# static_folder=None          -> desactivamos el /static por defecto de Flask;
#                                nosotros servimos los archivos desde la raíz.
app = Flask(__name__, template_folder="templates", static_folder=None)

# Nos aseguramos de que la base de datos exista al arrancar.
init_db()
seed_data()


@app.route("/")
def home():
    """Página de inicio."""
    return send_from_directory(ROOT_DIR, "index.html")


@app.route("/validar")
def validar():
    """
    Validación de certificados.
    - /validar                 -> muestra el buscador (entrada manual)
    - /validar?serial=XXXX      -> valida ese serial y muestra el resultado
    """
    serial = (request.args.get("serial") or "").strip()

    if not serial:
        # Entró desde el menú, sin código: mostramos el buscador.
        return render_template("validar.html", estado="buscar", serial="", cert=None)

    cert = buscar_certificado(serial)
    if cert:
        return render_template("validar.html", estado="valido", serial=serial, cert=cert)
    return render_template("validar.html", estado="invalido", serial=serial, cert=None)


@app.route("/<path:filename>")
def archivos_estaticos(filename):
    """
    Sirve cualquier otro archivo del sitio (academia.html, evaluacion.html,
    Logo MF.png, imágenes, etc.) directamente desde la raíz del proyecto.
    Así tu diseño actual funciona sin cambios.
    """
    ruta_absoluta = os.path.join(ROOT_DIR, filename)
    if os.path.isfile(ruta_absoluta):
        return send_from_directory(ROOT_DIR, filename)
    abort(404)


if __name__ == "__main__":
    # debug=True recarga el servidor al guardar cambios. Quítalo en producción.
    app.run(host="127.0.0.1", port=5000, debug=True)
