"""Gera og-image.png (1200x630) usada nas meta tags Open Graph do site."""
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

W, H = 1200, 630
BG_TOP, BG_BOT = (15, 15, 19), (26, 10, 0)
ORANGE, YELLOW, GREEN, WHITE, MUTED = (255, 85, 34), (255, 230, 0), (34, 197, 94), (240, 240, 248), (150, 150, 172)

# Plataformas com oferta no ar. Quando o Mercado Livre for liberado, basta
# acrescentar ("Mercado Livre", YELLOW) a esta lista e rodar o script de novo.
PLATAFORMAS = [("Shopee", ORANGE)]


def font(size, bold=False):
    for name in (("arialbd.ttf", "seguisb.ttf") if bold else ("arial.ttf", "segoeui.ttf")):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default(size)


def width(draw, text, f):
    box = draw.textbbox((0, 0), text, font=f)
    return box[2] - box[0]


img = Image.new("RGB", (W, H))
d = ImageDraw.Draw(img)

# Fundo em gradiente vertical
for y in range(H):
    t = y / H
    d.line([(0, y), (W, y)], fill=tuple(int(a + (b - a) * t) for a, b in zip(BG_TOP, BG_BOT)))

# Brilho laranja difuso atrás do selo (desenhado e suavizado antes de compor)
glow = Image.new("RGB", (W, H), (0, 0, 0))
ImageDraw.Draw(glow).ellipse([W - 520, -240, W + 160, 440], fill=(96, 34, 10))
glow = glow.filter(ImageFilter.GaussianBlur(90))
img = ImageChops.add(img, glow)
d = ImageDraw.Draw(img)

d.text((70, 106), "ACHADINHOS  ·  ATUALIZADO A CADA 15 MIN", font=font(22, True), fill=ORANGE)
d.text((70, 168), "SUPER", font=font(100, True), fill=WHITE)
d.text((70, 274), "PROMOÇÕES", font=font(100, True), fill=ORANGE)

# Linha das plataformas, posicionada por medição
f_plat = font(42, True)
x = 70
for i, (nome, cor) in enumerate(PLATAFORMAS):
    if i:
        d.text((x, 424), "+", font=f_plat, fill=MUTED)
        x += width(d, "+", f_plat) + 18
    d.text((x, 424), nome, font=f_plat, fill=cor)
    x += width(d, nome, f_plat) + 18

d.text((70, 506), "Entre no grupo e receba antes de todo mundo", font=font(30), fill=MUTED)

# Selo de desconto, centralizado no retângulo
f_selo = font(42, True)
selo = "ATÉ 90% OFF"
x0, y0, x1, y1 = 838, 206, 1132, 330
d.rounded_rectangle([x0, y0, x1, y1], radius=24, fill=ORANGE)
d.text(((x0 + x1) / 2, (y0 + y1) / 2), selo, font=f_selo, fill=WHITE, anchor="mm")

# Faixa inferior bicolor
d.rectangle([0, H - 14, W // 2, H], fill=GREEN)
d.rectangle([W // 2, H - 14, W, H], fill=ORANGE)

img.save("og-image.png", "PNG", optimize=True)
print("og-image.png gerada:", img.size)
