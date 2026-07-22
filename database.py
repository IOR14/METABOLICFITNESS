"""
database.py — Crea e inicializa la base de datos SQLite de certificados.

Ejecuta este archivo UNA vez (o cuando quieras reiniciar la base):
    python database.py

Crea el archivo 'certificados.db' con la tabla 'certificados' y carga
algunos certificados de ejemplo para que puedas probar el validador.
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "certificados.db")


def get_connection():
    """Devuelve una conexión a la base de datos con filas tipo diccionario."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Crea las tablas si no existen."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS certificados (
            serial            TEXT PRIMARY KEY,
            nombre_estudiante TEXT NOT NULL,
            curso             TEXT NOT NULL,
            fecha             TEXT NOT NULL
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS compras (
            session_id   TEXT PRIMARY KEY,
            email        TEXT,
            curso        TEXT,
            moneda       TEXT,
            amount_total INTEGER,
            currency     TEXT,
            payment_status TEXT,
            created_at   TEXT NOT NULL DEFAULT (datetime('now'))
        )
        """
    )
    conn.commit()
    conn.close()


def registrar_compra(session_id, email, curso, moneda, amount_total, currency, payment_status):
    """Registra (o ignora si ya existe) una compra confirmada por webhook."""
    if not session_id:
        return False
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT OR IGNORE INTO compras
            (session_id, email, curso, moneda, amount_total, currency, payment_status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            session_id,
            email or "",
            curso or "",
            moneda or "",
            amount_total,
            currency or "",
            payment_status or "",
        ),
    )
    inserted = cur.rowcount > 0
    conn.commit()
    conn.close()
    return inserted


def seed_data():
    """
    Inserta certificados de ejemplo (no duplica si ya existen).
    Lista vacía: los certificados reales se cargan con 'python generar_qrs.py'.
    """
    ejemplos = []
    if not ejemplos:
        return
    conn = get_connection()
    cur = conn.cursor()
    cur.executemany(
        """
        INSERT OR IGNORE INTO certificados (serial, nombre_estudiante, curso, fecha)
        VALUES (?, ?, ?, ?)
        """,
        ejemplos,
    )
    conn.commit()
    conn.close()


def buscar_certificado(serial):
    """Busca un certificado por su serial. Devuelve un dict o None."""
    if not serial:
        return None
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT serial, nombre_estudiante, curso, fecha FROM certificados WHERE serial = ?",
        (serial.strip(),),
    )
    fila = cur.fetchone()
    conn.close()
    return dict(fila) if fila else None


if __name__ == "__main__":
    init_db()
    seed_data()
    print("Base de datos lista en:", DB_PATH)
    print("Certificados de ejemplo cargados:")
    conn = get_connection()
    for fila in conn.execute("SELECT serial, nombre_estudiante FROM certificados"):
        print(f"  - {fila['serial']}  ->  {fila['nombre_estudiante']}")
    conn.close()
