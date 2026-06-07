# -*- coding: utf-8 -*-
"""
generar_pdf_qrs.py — Genera un PDF imprimible con todos los códigos QR de los
diplomas, cada uno etiquetado con el nombre del estudiante y su código de serie.

Requisitos previos:
    - Haber ejecutado antes 'python generar_qrs.py' (crea la base y los QR).

Cómo ejecutar:
    1) pip install reportlab
    2) python generar_pdf_qrs.py

Resultado:
    - Crea el archivo 'diplomas_qrs.pdf' con una grilla de QR (3 columnas)
      listo para imprimir y recortar.
"""

import os
import sqlite3

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

from database import DB_PATH

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CARPETA_QRS = os.path.join(BASE_DIR, "qrs_diplomas")
PDF_SALIDA = os.path.join(BASE_DIR, "diplomas_qrs.pdf")

# Disposición de la grilla
COLUMNS = 3          # tarjetas por fila
ROWS = 4             # filas por página  -> 12 tarjetas por página
MARGEN = 15 * mm     # margen exterior de la página


def obtener_certificados():
    """Devuelve los certificados del curso (serial MF-FRM-XX) ordenados."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    filas = conn.execute(
        """
        SELECT serial, nombre_estudiante, curso, fecha
        FROM certificados
        WHERE serial LIKE 'MF-FRM-%'
        ORDER BY serial
        """
    ).fetchall()
    conn.close()
    return filas


def truncar(texto, maximo):
    """Acorta un texto largo para que quepa en la tarjeta."""
    return texto if len(texto) <= maximo else texto[: maximo - 1] + "…"


def main():
    certificados = obtener_certificados()
    if not certificados:
        print("No se encontraron certificados MF-FRM-* en la base de datos.")
        print("Ejecuta primero:  python generar_qrs.py")
        return

    page_w, page_h = A4
    c = canvas.Canvas(PDF_SALIDA, pagesize=A4)

    # Tamaño de cada celda de la grilla
    cell_w = (page_w - 2 * MARGEN) / COLUMNS
    cell_h = (page_h - 2 * MARGEN) / ROWS
    qr_size = min(cell_w, cell_h) - 22 * mm  # deja espacio para el texto

    # Portada / título en la primera página
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(page_w / 2, page_h - MARGEN + 2 * mm,
                        "Metabolic Fitness · Validación de Diplomas")

    por_pagina = COLUMNS * ROWS
    faltan_png = []

    for i, cert in enumerate(certificados):
        if i > 0 and i % por_pagina == 0:
            c.showPage()

        pos = i % por_pagina
        col = pos % COLUMNS
        row = pos // COLUMNS

        # Esquina superior izquierda de la celda
        x0 = MARGEN + col * cell_w
        y0 = page_h - MARGEN - (row + 1) * cell_h

        ruta_qr = os.path.join(CARPETA_QRS, "QR_{}.png".format(cert["serial"]))

        # Centramos el QR en la parte superior de la celda
        qr_x = x0 + (cell_w - qr_size) / 2
        qr_y = y0 + cell_h - qr_size - 6 * mm

        if os.path.isfile(ruta_qr):
            c.drawImage(ImageReader(ruta_qr), qr_x, qr_y, qr_size, qr_size)
        else:
            faltan_png.append(cert["serial"])
            c.rect(qr_x, qr_y, qr_size, qr_size)
            c.setFont("Helvetica", 7)
            c.drawCentredString(x0 + cell_w / 2, qr_y + qr_size / 2, "QR no encontrado")

        # Texto debajo del QR: nombre, serial y fecha
        text_cx = x0 + cell_w / 2
        ty = qr_y - 5 * mm
        c.setFont("Helvetica-Bold", 9)
        c.drawCentredString(text_cx, ty, truncar(cert["nombre_estudiante"], 28))
        c.setFont("Helvetica", 8)
        c.drawCentredString(text_cx, ty - 4.5 * mm, cert["serial"])
        c.setFont("Helvetica-Oblique", 6.5)
        c.drawCentredString(text_cx, ty - 9 * mm, truncar(cert["curso"], 40))

    c.showPage()
    c.save()

    print("PDF generado: {}".format(PDF_SALIDA))
    print("Total de QR incluidos: {}".format(len(certificados)))
    if faltan_png:
        print("Aviso: faltan estas imágenes en 'qrs_diplomas/': {}".format(", ".join(faltan_png)))
        print("Ejecuta 'python generar_qrs.py' para regenerarlas.")


if __name__ == "__main__":
    main()
