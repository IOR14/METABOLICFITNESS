# -*- coding: utf-8 -*-
"""Asigna las ilustraciones clínicas como banners de los 10 papers recientes."""

from __future__ import annotations

import re
from pathlib import Path

from PIL import Image

SRC = Path(
    r"C:\Users\DELL\.cursor\projects\c-Users-DELL-Desktop-israel-DESARROLLOS-IOR14-WEB-SERVICE-Metabolic-Fitness\assets"
)
BASE = Path(__file__).resolve().parent
BLOG_IMG = BASE / "assets" / "blog"
SRC_DIR = BASE / "assets" / "infografias" / "_src"

MAP = {
    "illus-cronobio.png": "cronobiologia-del-ejercicio-ritmos-circadianos-y-control-metabolico",
    "illus-fuerza.png": "fuerza-muscular-como-predictor-de-mortalidad-cardiometabolica-de-la-dinamometria-a-la-prescripcion",
    "illus-epoc.png": "prescripcion-de-ejercicio-en-epoc-capacidad-funcional-dispnea-y-fuerza-periferica",
    "illus-hiit.png": "hiit-versus-entrenamiento-continuo-en-hipertension-arterial-que-dice-la-fisiologia-clinica",
    "illus-mitocondrias.png": "mitocondrias-ejercicio-e-insuficiencia-cardiaca-rehabilitacion-metabolica-de-precision",
    "illus-hueso.png": "entrenamiento-de-fuerza-y-salud-osea-en-mujeres-posmenopausicas-evidencia-clinica-aplicada",
    "illus-oncologia.png": "ejercicio-en-oncologia-seguridad-dosis-y-recuperacion-funcional-durante-y-despues-del-tratamiento",
    "illus-parkinson.png": "ejercicio-y-neuroplasticidad-en-enfermedad-de-parkinson-de-la-evidencia-a-la-sesion-clinica",
    "illus-microbiota.png": "ejercicio-y-microbiota-intestinal-en-obesidad-puentes-entre-intestino-musculo-y-metabolismo",
    "illus-sueno.png": "sueno-recuperacion-e-inmunidad-en-deportistas-y-pacientes-clinicos-una-mirada-integrada",
}


def main() -> None:
    BLOG_IMG.mkdir(parents=True, exist_ok=True)
    SRC_DIR.mkdir(parents=True, exist_ok=True)

    for src_name, slug in MAP.items():
        src = SRC / src_name
        if not src.exists():
            raise FileNotFoundError(src)
        im = Image.open(src).convert("RGB")
        im.save(SRC_DIR / src_name, optimize=True)
        im.save(BLOG_IMG / f"{slug}.jpg", quality=92, optimize=True)
        im.save(BLOG_IMG / f"{slug}.png", optimize=True)
        print(f"[OK] banner {slug} {im.size}")

        html_path = BASE / "blog" / f"{slug}.html"
        text = html_path.read_text(encoding="utf-8")
        text = re.sub(
            rf'(src=["\']\.\./assets/blog/{re.escape(slug)}\.(?:jpg|png))(?:\?v=[^"\']*)?(["\'])',
            rf"\1?v=14\2",
            text,
            count=1,
        )
        # Only change the hero media image (first object-cover after blog assets)
        text = text.replace(
            'class="w-full h-full object-cover"',
            'class="w-full h-full object-contain bg-white"',
            1,
        )
        html_path.write_text(text, encoding="utf-8")
        print(f"[OK] html   {slug}")

    js_path = BASE / "js" / "blog.js"
    js = js_path.read_text(encoding="utf-8")
    js_path.write_text(js.replace("?v=13", "?v=14"), encoding="utf-8")
    print("[OK] blog.js cache -> v=14")


if __name__ == "__main__":
    main()
