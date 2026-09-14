# -*- coding: utf-8 -*-
"""Genera 10 papers (HTML + PDF + portada) y actualiza data/blog-posts.json."""

from __future__ import annotations

import json
import os
import textwrap
from datetime import date
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

BASE = Path(__file__).resolve().parent
BATCH = BASE / "data" / "new-papers-batch.json"
POSTS = BASE / "data" / "blog-posts.json"
BLOG = BASE / "blog"
PDF_DIR = BLOG / "pdf"
IMG_DIR = BASE / "assets" / "blog"
LOGO = BASE / "assets" / "brand" / "logo-mf-horizontal-white.png"
PUBLISHED = "2026-09-14"

HEAD_CSS = r"""
    <style>
        body { font-family: 'Open Sans', sans-serif; color: #404041; background: #FAFAFA; }
        h1, h2, h3, h4 { font-family: 'Montserrat', sans-serif; }
        .article-content p { margin-bottom: 1.15rem; line-height: 1.9; font-size: 1.05rem; text-align: justify; hyphens: auto; }
        .article-content h2 { margin-top: 2.2rem; margin-bottom: 0.9rem; font-weight: 700; font-size: 1.45rem; color: #460877; text-align: left; }
        .justified { text-align: justify; hyphens: auto; }
        .abstract-box { border-left: 5px solid #5CB85C; background: linear-gradient(90deg, #F3FBF3 0%, #FFFFFF 100%); }
        .clinical-box { border: 1px solid #5CB85C33; background: #F8FFF8; box-shadow: 0 10px 30px rgba(92,184,92,0.08); }
        .sidebar-card { background: white; border: 1px solid #E5E7EB; box-shadow: 0 8px 24px rgba(70,8,119,0.06); }
        .keyword-chip { display: inline-block; background: rgba(255,255,255,0.14); color: #fff; border: 1px solid rgba(255,255,255,0.22); border-radius: 999px; padding: 0.28rem 0.75rem; font-size: 0.7rem; letter-spacing: 0.04em; text-transform: uppercase; font-family: Montserrat, sans-serif; font-weight: 600; }
        .mf-pdf-cta { background: #460877 !important; color: #fff !important; display: inline-block; text-decoration: none !important; }
        .mf-pdf-cta:hover { background: #5a0a99 !important; }
        aside .mf-pdf-cta { display: block; width: 100%; box-sizing: border-box; text-align: center; }
        .mf-rating-box { width: 100%; max-width: 28rem; background: #FAFAFA; border: 1px solid #E5E7EB; border-radius: 1rem; padding: 1.1rem 1.25rem; text-align: center; }
        .mf-star { color: #D1D5DB; cursor: pointer; user-select: none; line-height: 1; }
        .mf-star-on { color: #F5B301; }
        .mf-star-off { color: #D1D5DB; }
        .mf-stars-display .mf-star { cursor: default; }
        .mf-stars-input { display: inline-flex; gap: 0.15rem; font-size: 1.85rem; }
        .mf-stars-input button { background: none; border: none; padding: 0; cursor: pointer; }
        .mf-article-header { position: sticky; top: 0; z-index: 50; background: linear-gradient(105deg, #08060c 0%, #14081f 42%, #2a0548 78%, #3b0a66 100%); }
        .article-hero-copy { background: linear-gradient(115deg, #08060c 0%, #16091f 38%, #2a0548 72%, #3b0a66 100%) !important; }
        .article-hero-fade { background: linear-gradient(to right, #16091f 0%, transparent 100%) !important; }
        .mf-article-nav { display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 0.75rem; }
        .mf-article-actions { display: flex; flex-wrap: wrap; align-items: center; gap: 0.5rem; margin-left: auto; }
        .mf-back-link { display: inline-flex; align-items: center; justify-content: center; min-height: 44px; padding: 0.55rem 0.9rem; border-radius: 0.6rem; background: rgba(255,255,255,0.14); color: #fff !important; text-decoration: none !important; font-weight: 600; }
        .mf-header-pdf { display: inline-flex; align-items: center; justify-content: center; min-height: 44px; padding: 0.55rem 0.9rem; border-radius: 0.6rem; background: #5CB85C !important; color: #fff !important; text-decoration: none !important; font-weight: 600; }
        @media (max-width: 640px) {
            .mf-article-actions { margin-left: 0; width: 100%; flex-direction: column; align-items: stretch; }
            .mf-back-link, .mf-header-pdf { width: 100%; }
            .article-hero { grid-template-columns: 1fr !important; }
            .article-hero-copy h1 { font-size: 1.45rem !important; }
            .article-hero-fade { display: none !important; }
        }
    </style>
"""


def _font(path: str, size: int):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def make_cover(title: str, out_path: Path, idx: int):
    w, h = 1200, 800
    img = Image.new("RGB", (w, h))
    draw = ImageDraw.Draw(img)
    # Gradientes distintos por índice
    palettes = [
        ((8, 6, 12), (70, 8, 119), (92, 184, 92)),
        ((10, 20, 40), (0, 174, 239), (70, 8, 119)),
        ((20, 10, 30), (90, 20, 120), (0, 174, 239)),
        ((5, 25, 20), (40, 120, 80), (70, 8, 119)),
        ((25, 10, 10), (120, 40, 60), (70, 8, 119)),
    ]
    c1, c2, accent = palettes[idx % len(palettes)]
    for y in range(h):
        t = y / (h - 1)
        r = int(c1[0] + (c2[0] - c1[0]) * t)
        g = int(c1[1] + (c2[1] - c1[1]) * t)
        b = int(c1[2] + (c2[2] - c1[2]) * t)
        draw.line([(0, y), (w, y)], fill=(r, g, b))
    draw.rectangle([0, 0, w, 10], fill=accent)
    draw.rectangle([0, h - 10, w, h], fill=accent)

    title_font = _font(r"C:\Windows\Fonts\arialbd.ttf", 42)
    brand_font = _font(r"C:\Windows\Fonts\arialbd.ttf", 22)
    small = _font(r"C:\Windows\Fonts\arial.ttf", 18)

    draw.text((48, 40), "METABOLIC FITNESS", font=brand_font, fill=(255, 255, 255))
    draw.text((48, 75), "Paper Científicos", font=small, fill=(200, 200, 210))

    # wrap title
    words = title.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=title_font) < w - 100:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    y = 280
    for line in lines[:6]:
        draw.text((48, y), line, font=title_font, fill=(255, 255, 255))
        y += 52

    draw.text((48, h - 70), "Fisiología Clínica del Ejercicio · www.metabolicfitness.cl", font=small, fill=(210, 210, 220))
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    img.save(out_path, quality=90)


def make_pdf(paper: dict, pdf_path: Path):
    pdfmetrics.registerFont(TTFont("Arial", r"C:\Windows\Fonts\arial.ttf"))
    pdfmetrics.registerFont(TTFont("Arial-Bold", r"C:\Windows\Fonts\arialbd.ttf"))
    c = canvas.Canvas(str(pdf_path), pagesize=A4)
    w, h = A4
    margin = 20 * mm
    y = h - margin

    def new_page():
        nonlocal y
        c.showPage()
        y = h - margin

    def ensure(space=16):
        nonlocal y
        if y < margin + space:
            new_page()

    def draw_wrapped(text, font, size, leading, color=(40, 40, 41), max_w=None):
        nonlocal y
        max_w = max_w or (w - 2 * margin)
        c.setFont(font, size)
        c.setFillColorRGB(*(v / 255 for v in color))
        words = text.split()
        line = ""
        for word in words:
            trial = (line + " " + word).strip()
            if c.stringWidth(trial, font, size) <= max_w:
                line = trial
            else:
                ensure(leading)
                c.drawString(margin, y, line)
                y -= leading
                line = word
        if line:
            ensure(leading)
            c.drawString(margin, y, line)
            y -= leading

    # header bar
    c.setFillColorRGB(0.08, 0.05, 0.12)
    c.rect(0, h - 18 * mm, w, 18 * mm, fill=1, stroke=0)
    c.setFillColorRGB(1, 1, 1)
    c.setFont("Arial-Bold", 11)
    c.drawString(margin, h - 11 * mm, "Metabolic Fitness · Paper Científicos")

    y = h - 28 * mm
    draw_wrapped(paper["title"], "Arial-Bold", 14, 18, (70, 8, 119))
    y -= 4
    draw_wrapped("Síntesis clínica · " + PUBLISHED, "Arial", 9, 12, (100, 100, 100))
    y -= 8
    draw_wrapped("Resumen ejecutivo", "Arial-Bold", 11, 14, (92, 184, 92))
    draw_wrapped(paper["abstract"], "Arial", 10, 13)
    y -= 6

    intro = (
        "Esta síntesis clínica de Metabolic Fitness Academy traduce evidencia contemporánea "
        "en fisiología del ejercicio aplicada a criterios prácticos para médicos, kinesiólogos "
        "y fisiólogos clínicos en Latinoamérica."
    )
    draw_wrapped(intro, "Arial", 10, 13)
    y -= 4

    for section in paper["sections"]:
        y -= 4
        draw_wrapped(section["heading"], "Arial-Bold", 12, 15, (70, 8, 119))
        draw_wrapped(section["body"], "Arial", 10, 13)
        y -= 2

    y -= 4
    draw_wrapped("Implicaciones clínicas", "Arial-Bold", 12, 15, (92, 184, 92))
    draw_wrapped(paper["clinical"], "Arial", 10, 13)
    y -= 6
    draw_wrapped("Referencias y marcos de evidencia", "Arial-Bold", 11, 14, (70, 8, 119))
    for ref in paper["refs"]:
        draw_wrapped("• " + ref, "Arial", 9, 12, (80, 80, 80))

    y -= 10
    draw_wrapped(
        "© 2026 Metabolic Fitness · Fisiología Clínica del Ejercicio · www.metabolicfitness.cl",
        "Arial",
        8,
        11,
        (120, 120, 120),
    )
    c.save()


def make_html(paper: dict, img_rel: str, pdf_rel: str) -> str:
    slug = paper["slug"]
    chips = "".join(f'<span class="keyword-chip">{k}</span>' for k in paper["keywords"])
    sections_html = "".join(
        f"<h2>{s['heading']}</h2><p>{s['body']}</p>" for s in paper["sections"]
    )
    keypoints = "".join(
        f'<li class="flex gap-3"><span class="text-metabolic-green font-bold">•</span><span>{k}</span></li>'
        for k in paper["keypoints"]
    )
    refs = "".join(
        f'<li class="border-l-4 border-metabolic-green pl-4 py-2"><p class="font-body text-sm text-metabolic-charcoal/90">{r}</p></li>'
        for r in paper["refs"]
    )
    intro = (
        "Esta síntesis clínica de Metabolic Fitness Academy traduce evidencia contemporánea "
        "en fisiología del ejercicio aplicada a criterios prácticos para médicos, kinesiólogos "
        "y fisiólogos clínicos en Latinoamérica."
    )
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="icon" href="/assets/brand/mf-favicon.ico?v=3" sizes="any">
    <link rel="icon" type="image/png" href="/assets/brand/mf-favicon-32.png?v=3" sizes="32x32">
    <link rel="apple-touch-icon" href="/assets/brand/mf-apple-touch-icon.png?v=3">
    <title>{paper['title']} - Metabolic Fitness</title>
    <meta name="description" content="{paper['excerpt']}">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700;800;900&family=Open+Sans:wght@300;400;600;700&display=swap" rel="stylesheet">
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {{
            theme: {{
                extend: {{
                    colors: {{
                        'metabolic-green': '#5CB85C',
                        'metabolic-charcoal': '#404041',
                        'metabolic-cyan': '#00AEEF',
                        'metabolic-purple': '#460877',
                        'metabolic-bg': '#FFFFFF',
                        'metabolic-bg-secondary': '#FAFAFA',
                    }},
                    fontFamily: {{
                        'heading': ['Montserrat', 'sans-serif'],
                        'body': ['Open Sans', 'sans-serif'],
                    }},
                }},
            }},
        }}
    </script>
{HEAD_CSS}
</head>
<body class="antialiased">
    <header class="mf-article-header text-white shadow-lg">
        <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-3">
            <nav class="mf-article-nav" aria-label="Navegacion del articulo">
                <a href="../blog.html" class="mf-logo-link flex items-center gap-2 min-w-0">
                    <img src="../assets/brand/logo-mf-nav-white.png?v=4" alt="Metabolic Fitness" class="h-10 sm:h-12 w-auto max-w-[200px] object-contain object-left">
                    <span class="font-heading font-bold text-sm hidden md:inline text-white/95">Paper Cientificos</span>
                </a>
                <div class="mf-article-actions">
                    <a href="../blog.html" class="mf-back-link font-body text-sm">← Volver al blog</a>
                    <a href="{pdf_rel}" download class="mf-header-pdf font-body text-sm">Descargar PDF</a>
                </div>
            </nav>
        </div>
    </header>

    <section class="relative">
        <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 pt-8">
            <div class="article-hero rounded-2xl sm:rounded-3xl overflow-hidden shadow-2xl bg-white grid lg:grid-cols-[1.05fr_0.95fr] min-h-[22rem]">
                <div class="article-hero-copy p-6 sm:p-12 flex flex-col justify-center text-white order-2 lg:order-1">
                    <div class="flex flex-wrap items-center gap-3 mb-5">
                        <span class="px-3 py-1 rounded-full bg-white text-metabolic-purple text-xs font-heading font-semibold uppercase tracking-wide">Clinica</span>
                        <span class="text-xs font-body text-white/80">{PUBLISHED}</span>
                        <span class="text-xs font-body text-white/80">7 min de lectura</span>
                    </div>
                    <h1 class="font-heading font-bold text-3xl sm:text-[2.35rem] leading-tight">{paper['title']}</h1>
                    <div class="mt-5 flex flex-wrap gap-2">{chips}</div>
                </div>
                <div class="article-hero-media relative min-h-[14rem] order-1 lg:order-2">
                    <img src="../{img_rel}?v=1" alt="{paper['title']}" class="w-full h-full object-cover">
                    <div class="article-hero-fade absolute inset-y-0 left-0 w-24 hidden lg:block"></div>
                </div>
            </div>
        </div>
    </section>

    <main class="mf-article-main max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-10">
        <div class="grid lg:grid-cols-12 gap-6 lg:gap-8">
            <article class="lg:col-span-8 min-w-0">
                <div class="abstract-box rounded-2xl p-6 sm:p-8 mb-8">
                    <p class="text-xs font-heading font-bold uppercase tracking-widest text-metabolic-green mb-3">Resumen ejecutivo</p>
                    <p class="font-body text-lg leading-relaxed text-metabolic-charcoal/90 justified">{paper['abstract']}</p>
                </div>
                <div class="article-content font-body text-metabolic-charcoal/90 bg-white rounded-2xl p-6 sm:p-8 shadow-sm border border-gray-100">
                    <p>{intro}</p>
                    {sections_html}
                </div>
                <section class="clinical-box rounded-2xl p-6 mt-8">
                    <h2 class="font-heading font-bold text-xl text-metabolic-charcoal mb-3">Implicaciones clinicas</h2>
                    <p class="font-body text-metabolic-charcoal/85 leading-relaxed justified">{paper['clinical']}</p>
                </section>
                <section id="referencias" class="mt-12 pt-8 border-t border-gray-200">
                    <h2 class="font-heading font-bold text-2xl text-metabolic-charcoal mb-6">Referencias</h2>
                    <ol class="space-y-4 list-none">{refs}</ol>
                </section>
            </article>
            <aside class="lg:col-span-4 space-y-6 min-w-0">
                <div class="sidebar-card rounded-2xl p-6">
                    <p class="text-xs font-heading font-bold uppercase tracking-widest text-metabolic-purple mb-4">Descarga profesional</p>
                    <p class="font-body text-sm text-metabolic-charcoal/75 mb-4">Documento PDF con estructura editorial Metabolic Fitness.</p>
                    <a href="{pdf_rel}" download class="mf-pdf-cta block text-center text-white px-4 py-3 rounded-xl font-body font-semibold">Descargar articulo en PDF</a>
                </div>
                <div class="sidebar-card rounded-2xl p-6">
                    <p class="text-xs font-heading font-bold uppercase tracking-widest text-metabolic-green mb-4">Puntos clave</p>
                    <ul class="space-y-3 font-body text-sm text-metabolic-charcoal/85">{keypoints}</ul>
                </div>
                <div class="sidebar-card rounded-2xl p-6">
                    <p class="text-xs font-heading font-bold uppercase tracking-widest text-metabolic-cyan mb-4">Evidencia de origen</p>
                    <p class="font-body text-sm text-metabolic-charcoal/75">Síntesis clínica elaborada por Metabolic Fitness Academy a partir de guías y revisiones contemporáneas de fisiología del ejercicio.</p>
                </div>
            </aside>
        </div>
    </main>

    <footer class="bg-white border-t border-gray-200 py-10 mt-8">
        <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col items-center gap-5">
            <section class="mf-rating-box" id="mf-paper-rating" data-slug="{slug}" data-editorial-rating="4.0" aria-label="Evaluacion del paper">
                <p class="text-xs font-heading font-bold uppercase tracking-widest text-metabolic-purple mb-2">Evaluacion del paper</p>
                <div class="flex flex-col items-center gap-1 mb-3">
                    <div class="mf-stars-display text-2xl" aria-hidden="true"><span class="mf-star mf-star-on">★</span><span class="mf-star mf-star-on">★</span><span class="mf-star mf-star-on">★</span><span class="mf-star mf-star-on">★</span><span class="mf-star mf-star-off">★</span></div>
                    <p class="font-body text-sm text-metabolic-charcoal/80">Calidad editorial: <strong id="mf-editorial-score">4.0</strong>/5</p>
                </div>
                <p class="font-body text-xs text-metabolic-charcoal/60 mb-2">Tu evaluacion (0 a 5 estrellas)</p>
                <div class="mf-stars-input" role="radiogroup" aria-label="Califica este paper">
                    <button type="button" class="mf-star" data-value="1" aria-label="1 estrella">★</button>
                    <button type="button" class="mf-star" data-value="2" aria-label="2 estrellas">★</button>
                    <button type="button" class="mf-star" data-value="3" aria-label="3 estrellas">★</button>
                    <button type="button" class="mf-star" data-value="4" aria-label="4 estrellas">★</button>
                    <button type="button" class="mf-star" data-value="5" aria-label="5 estrellas">★</button>
                </div>
                <p class="font-body text-xs text-metabolic-charcoal/55 mt-2" id="mf-rating-status">
                    Promedio lectores: <span id="mf-avg-score">—</span> · <span id="mf-vote-count">0</span> votos
                </p>
            </section>
            <a href="https://www.metabolicfitness.cl" class="inline-block">
                <img src="../assets/brand/logo-mf-horizontal.png" alt="Metabolic Fitness" class="h-11 w-auto object-contain bg-transparent">
            </a>
            <p class="font-body text-metabolic-charcoal/60 text-sm text-center">
                © 2026 Metabolic Fitness · Fisiologia Clinica del Ejercicio<br>
                <a href="https://www.metabolicfitness.cl" class="hover:text-metabolic-purple transition-colors">www.metabolicfitness.cl</a>
            </p>
        </div>
    </footer>
    <script src="../js/blog-rating.js?v=2"></script>
</body>
</html>
"""


def main():
    papers = json.loads(BATCH.read_text(encoding="utf-8"))
    existing = json.loads(POSTS.read_text(encoding="utf-8"))
    by_slug = {p["slug"]: p for p in existing}

    BLOG.mkdir(exist_ok=True)
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    IMG_DIR.mkdir(parents=True, exist_ok=True)

    for i, paper in enumerate(papers):
        slug = paper["slug"]
        img_rel = f"assets/blog/{slug}.jpg"
        pdf_rel = f"pdf/{slug}.pdf"
        pdf_index = f"blog/pdf/{slug}.pdf"

        make_cover(paper["title"], IMG_DIR / f"{slug}.jpg", i)
        make_pdf(paper, PDF_DIR / f"{slug}.pdf")
        html = make_html(paper, img_rel, pdf_rel)
        (BLOG / f"{slug}.html").write_text(html, encoding="utf-8")

        entry = {
            "slug": slug,
            "title": paper["title"],
            "category": "Clinica",
            "category_color": "metabolic-cyan",
            "gradient": "from-metabolic-cyan/20 to-metabolic-green/20",
            "excerpt": paper["excerpt"],
            "published_at": PUBLISHED,
            "image": img_rel,
            "pdf": pdf_index,
            "keywords": paper["keywords"],
            "rating": 4.0,
        }
        by_slug[slug] = entry
        print(f"[OK] {slug}")

    # newest first-ish: keep previous + prepend new by published date sort happens in JS
    merged = list(by_slug.values())
    merged.sort(key=lambda p: p.get("published_at", ""), reverse=True)
    POSTS.write_text(json.dumps(merged, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"\nTotal posts en índice: {len(merged)}")


if __name__ == "__main__":
    main()
