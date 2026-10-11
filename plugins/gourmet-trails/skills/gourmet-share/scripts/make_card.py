#!/usr/bin/env python3
"""Render a Gourmet Trails recommendation card as a PNG.

Usage:
  python3 make_card.py --photo dish.jpg --name "Saffron House" --cuisine "South Indian" \
      --area "Old Town" --city "<city>" --order "Veg thali" \
      --note "Ask for extra rasam." --rating 5 --by "Maya" --out card.png \
      [--size story|post] [--footer "GOURMET TRAILS"]

--size post  -> 1080x1350 (Instagram feed, WhatsApp)   [default]
--size story -> 1080x1920 (Instagram/WhatsApp story)
Rating is optional (0 or omitted hides the dots). Note is optional.
--by is the name in the eyebrow ("MAYA RECOMMENDS"); omit it for "RECOMMENDED".
--footer is the brand line at the bottom right.
"""
import argparse, os, textwrap
from PIL import Image, ImageDraw, ImageFont, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "..", "assets")
CLOTH = (251, 250, 246); INK = (38, 48, 28); MUTED = (111, 118, 99); OLIVE = (77, 97, 48); RULE = (220, 220, 207)


def font(name, size, wght=None):
    f = ImageFont.truetype(os.path.join(FONTS, name), size)
    if wght:
        try:
            f.set_variation_by_axes([wght] if "Karla" in name else [11, wght])
        except Exception:
            pass
    return f


def wrap(draw, text, fnt, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= width:
            cur = t
        else:
            lines.append(cur); cur = w
    if cur:
        lines.append(cur)
    return lines


def main():
    a = argparse.ArgumentParser()
    a.add_argument("--photo", required=True); a.add_argument("--name", required=True)
    a.add_argument("--cuisine", default=""); a.add_argument("--area", default=""); a.add_argument("--city", default="")
    a.add_argument("--order", default=""); a.add_argument("--note", default="")
    a.add_argument("--rating", type=int, default=0); a.add_argument("--by", default="")
    a.add_argument("--size", choices=["post", "story"], default="post"); a.add_argument("--out", required=True)
    a.add_argument("--footer", default="GOURMET TRAILS")
    o = a.parse_args()

    W, H = (1080, 1350) if o.size == "post" else (1080, 1920)
    PH = 760 if o.size == "post" else 1180
    card = Image.new("RGB", (W, H), CLOTH)
    photo = ImageOps.fit(ImageOps.exif_transpose(Image.open(o.photo)).convert("RGB"), (W, PH), Image.LANCZOS)
    card.paste(photo, (0, 0))
    d = ImageDraw.Draw(card)
    # double rule under the photo, like a menu card
    d.rectangle([0, PH, W, PH + 4], fill=INK); d.rectangle([0, PH + 10, W, PH + 11], fill=INK)

    x, y, maxw = 72, PH + 52, W - 144
    eyebrow = font("DMMono-Regular.ttf", 24)
    by = o.by.strip()
    label = (f"{by.upper()} RECOMMENDS" if by else "RECOMMENDED") + (f" · {o.cuisine.upper()}" if o.cuisine else "")
    d.text((x, y), label, font=eyebrow, fill=OLIVE); y += 52

    size = 84
    title = font("BodoniModa-Italic.ttf", size, 500)
    while d.textlength(o.name, font=title) > maxw and size > 52:
        size -= 4; title = font("BodoniModa-Italic.ttf", size, 500)
    for line in wrap(d, o.name, title, maxw)[:2]:
        d.text((x, y), line, font=title, fill=INK); y += int(size * 1.08)
    y += 26
    body = font("Karla.ttf", 32, 400)
    where = ", ".join(p for p in [o.area, o.city] if p)
    if where:
        d.text((x, y), where, font=body, fill=MUTED); y += 58

    if o.order:
        k = "Order"; kw = d.textlength(k, font=body)
        val = o.order if d.textlength(o.order, font=body) < maxw - kw - 80 else wrap(d, o.order, body, maxw - kw - 80)[0] + "…"
        vw = d.textlength(val, font=body)
        d.text((x, y), k, font=body, fill=MUTED)
        lx0, lx1, ly = x + kw + 14, x + maxw - vw - 14, y + 26
        for dx in range(int(lx0), int(lx1), 10):
            d.ellipse([dx, ly, dx + 3, ly + 3], fill=MUTED)
        d.text((x + maxw - vw, y), val, font=body, fill=INK); y += 64

    if o.note:
        nf = font("BodoniModa-Italic.ttf", 36, 400)
        for line in wrap(d, f"“{o.note}”", nf, maxw)[:3 if o.size == "post" else 4]:
            d.text((x, y), line, font=nf, fill=INK); y += 48

    foot = H - 80
    d.line([x, foot - 26, x + maxw, foot - 26], fill=RULE, width=2)
    if o.rating:
        for i in range(5):
            cx = x + i * 30
            box = [cx, foot, cx + 18, foot + 18]
            d.ellipse(box, fill=OLIVE if i < o.rating else None, outline=OLIVE, width=2)
    brand = o.footer.upper(); bw = d.textlength(brand, font=eyebrow)
    d.text((x + maxw - bw, foot - 4), brand, font=eyebrow, fill=MUTED)
    card.save(o.out, "PNG", optimize=True)
    print(o.out)


if __name__ == "__main__":
    main()
