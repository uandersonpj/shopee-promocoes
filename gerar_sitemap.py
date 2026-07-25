"""Gera sitemap.xml a partir das categorias presentes em produtos.json.

Executado pelo push.bat a cada ciclo, para que novos nichos entrem no sitemap
automaticamente.
"""
import json
from datetime import date
from urllib.parse import quote

BASE = "https://uandersonpj.github.io/shopee-promocoes/"
HOJE = date.today().isoformat()

try:
    with open("produtos.json", encoding="utf-8") as f:
        produtos = json.load(f).get("products", [])
except (OSError, json.JSONDecodeError) as e:
    print(f"[sitemap] nao foi possivel ler produtos.json: {e}")
    raise SystemExit(1)

# Categorias ordenadas por volume de ofertas
contagem = {}
for p in produtos:
    cat = p.get("category")
    if cat:
        contagem[cat] = contagem.get(cat, 0) + 1
categorias = sorted(contagem, key=contagem.get, reverse=True)

urls = [(BASE, "1.0", "hourly"), (BASE + "privacidade.html", "0.3", "yearly")]
urls += [
    (f"{BASE}?categoria={quote(cat)}", "0.8", "hourly")
    for cat in categorias
]

linhas = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for loc, prio, freq in urls:
    linhas += [
        "  <url>",
        f"    <loc>{loc.replace('&', '&amp;')}</loc>",
        f"    <lastmod>{HOJE}</lastmod>",
        f"    <changefreq>{freq}</changefreq>",
        f"    <priority>{prio}</priority>",
        "  </url>",
    ]
linhas.append("</urlset>")

with open("sitemap.xml", "w", encoding="utf-8") as f:
    f.write("\n".join(linhas) + "\n")

print(f"[sitemap] {len(urls)} URLs ({len(categorias)} categorias)")
