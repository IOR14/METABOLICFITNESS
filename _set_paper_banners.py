# -*- coding: utf-8 -*-
"""Asigna las ilustraciones del usuario como banners de los 10 papers."""

from pathlib import Path

from PIL import Image

SRC = Path(
    r"C:\Users\DELL\.cursor\projects\c-Users-DELL-Desktop-israel-DESARROLLOS-IOR14-WEB-SERVICE-Metabolic-Fitness\assets"
)
BASE = Path(__file__).resolve().parent
DST = BASE / "assets" / "blog"
SRC_KEEP = BASE / "assets" / "infografias" / "_src"
BLOG = BASE / "blog"

DST.mkdir(parents=True, exist_ok=True)
SRC_KEEP.mkdir(parents=True, exist_ok=True)

MAPPING = {
    "illus-cronobio": "cronobiologia-del-ejercicio-ritmos-circadianos-y-control-metabolico",
    "illus-fuerza": "fuerza-muscular-como-predictor-de-mortalidad-cardiometabolica-de-la-dinamometria-a-la-prescripcion",
    "illus-epoc": "prescripcion-de-ejercicio-en-epoc-capacidad-funcional-dispnea-y-fuerza-periferica",
    "illus-hiit": "hiit-versus-entrenamiento-continuo-en-hipertension-arterial-que-dice-la-fisiologia-clinica",
    "illus-mitocondrias": "mitocondrias-ejercicio-e-insuficiencia-cardiaca-rehabilitacion-metabolica-de-precision",
    "illus-hueso": "entrenamiento-de-fuerza-y-salud-osea-en-mujeres-posmenopausicas-evidencia-clinica-aplicada",
    "illus-oncologia": "ejercicio-en-oncologia-seguridad-dosis-y-recuperacion-funcional-durante-y-despues-del-tratamiento",
    "illus-parkinson": "ejercicio-y-neuroplasticidad-en-enfermedad-de-parkinson-de-la-evidencia-a-la-sesion-clinica",
    "illus-microbiota": "ejercicio-y-microbiota-intestinal-en-obesidad-puentes-entre-intestino-musculo-y-metabolismo",
    "illus-sueno": "sueno-recuperacion-e-inmunidad-en-deportistas-y-pacientes-clinicos-una-mirada-integrada",
}

TARGET_W, TARGET_H = 1200, 800


def main():
    files = list(SRC.glob("*_images_illus-*.png"))
    by_key = {}
    for f in files:
        for key in MAPPING:
            if key in f.name:
                by_key[key] = f
                break

    missing = [k for k in MAPPING if k not in by_key]
    if missing:
        raise SystemExit(f"Missing images: {missing}")

    for key, slug in MAPPING.items():
        src = by_key[key]
        img = Image.open(src).convert("RGBA")
        img.save(SRC_KEEP / f"{key}.png", optimize=True)
        img.save(DST / f"{slug}.png", optimize=True)

        bg = Image.new("RGB", (TARGET_W, TARGET_H), (255, 255, 255))
        ratio = min(TARGET_W / img.width, TARGET_H / img.height)
        nw = max(1, int(img.width * ratio))
        nh = max(1, int(img.height * ratio))
        resized = img.resize((nw, nh), Image.Resampling.LANCZOS)
        layer = Image.new("RGB", resized.size, (255, 255, 255))
        layer.paste(resized, mask=resized.split()[-1])
        x = (TARGET_W - nw) // 2
        y = (TARGET_H - nh) // 2
        bg.paste(layer, (x, y))
        out_jpg = DST / f"{slug}.jpg"
        bg.save(out_jpg, quality=92, optimize=True)
        print(f"OK {key} -> {out_jpg.name}")

        html_path = BLOG / f"{slug}.html"
        if html_path.exists():
            text = html_path.read_text(encoding="utf-8")
            text = text.replace(f"{slug}.jpg?v=2", f"{slug}.jpg?v=3")
            text = text.replace(f"{slug}.jpg?v=1", f"{slug}.jpg?v=3")
            if f"{slug}.jpg?v=3" not in text and f"{slug}.jpg" in text:
                text = text.replace(f"{slug}.jpg", f"{slug}.jpg?v=3")
            html_path.write_text(text, encoding="utf-8")
            print(f"   updated HTML cache-bust {slug}")

    print("done", len(MAPPING))


if __name__ == "__main__":
    main()
