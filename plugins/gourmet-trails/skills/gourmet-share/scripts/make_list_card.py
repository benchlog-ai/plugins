#!/usr/bin/env python3
"""Render a Gourmet Trails "Best of" list as one PNG to send to friends.

Usage:
  python3 make_list_card.py --spec list.json --out best-of-brunch.png [--size post|story]

list.json:
  {"title": "Best of brunch", "note": "Weekend tables I'd send a friend to.", "by": "Maya",
   "footer": "Gourmet Trails",
   "places": [{"name": "Morning Table", "area": "Old Town", "city": "<city>",
               "order": "Shakshuka", "rating": 4, "photo": "morning-table.jpg"}, ...]}

"by" (optional) signs the header ("MAYA'S BEST OF"); "footer" (optional) is the brand line.

3–6 places. A place without "photo" gets an empty plate. Rating 0 or missing hides the dots.
"""
import argparse, json, os
from PIL import Image, ImageDraw, ImageOps

from make_card import font, wrap, CLOTH, INK, MUTED, OLIVE, RULE

PLATE = (241, 239, 230)


def main():
    a = argparse.ArgumentParser()
    a.add_argument("--spec", required=True); a.add_argument("--out", required=True)
    a.add_argument("--size", choices=["post", "story"], default="post")
    o = a.parse_args()
    spec = json.load(open(o.spec))
    base = os.path.dirname(os.path.abspath(o.spec))
    places = spec["places"][:6]

    W, H = (1080, 1350) if o.size == "post" else (1080, 1920)
    card = Image.new("RGB", (W, H), CLOTH)
    d = ImageDraw.Draw(card)
    x, maxw = 72, W - 144

    y = 84 if o.size == "post" else 200
    eyebrow = font("DMMono-Regular.ttf", 24)
    by = spec.get("by", "").strip()
    brand = (spec.get("footer") or "Gourmet Trails").strip().upper()
    d.text((x, y), (f"{by.upper()}'S " if by else "") + f"BEST OF · {brand}", font=eyebrow, fill=OLIVE); y += 50
    size = 76
    title = font("BodoniModa-Italic.ttf", size, 500)
    while d.textlength(spec["title"], font=title) > maxw and size > 48:
        size -= 4; title = font("BodoniModa-Italic.ttf", size, 500)
    d.text((x, y), spec["title"], font=title, fill=INK)
    y = d.textbbox((x, y), spec["title"], font=title)[3] + 22  # Bodoni's descenders run deep
    if spec.get("note"):
        nf = font("Karla.ttf", 30, 400)
        for line in wrap(d, spec["note"], nf, maxw)[:2]:
            d.text((x, y), line, font=nf, fill=MUTED); y += 40
    y += 18
    d.rectangle([x, y, x + maxw, y + 3], fill=INK); d.rectangle([x, y + 9, x + maxw, y + 10], fill=INK); y += 34

    foot = H - (90 if o.size == "post" else 200)
    row = min(210, (foot - 30 - y) // max(len(places), 1))
    thumb = min(row - 28, 170)
    y += max(0, (foot - 30 - y - row * len(places)) // 2)  # centre short lists in the space
    num = font("BodoniModa-Italic.ttf", 44, 400)
    name_f = font("BodoniModa-Italic.ttf", 40, 500)
    small = font("Karla.ttf", 26, 400)
    for i, p in enumerate(places):
        ty = y + i * row
        d.text((x, ty + thumb / 2 - 28), str(i + 1), font=num, fill=OLIVE)
        tx = x + 52
        if p.get("photo"):
            ph = ImageOps.fit(ImageOps.exif_transpose(Image.open(os.path.join(base, p["photo"]))).convert("RGB"),
                              (thumb, thumb), Image.LANCZOS)
            mask = Image.new("L", (thumb, thumb), 0)
            ImageDraw.Draw(mask).rounded_rectangle([0, 0, thumb, thumb], 14, fill=255)
            card.paste(ph, (tx, ty), mask)
        else:
            d.rounded_rectangle([tx, ty, tx + thumb, ty + thumb], 14, fill=PLATE)
            d.ellipse([tx + thumb * .2, ty + thumb * .2, tx + thumb * .8, ty + thumb * .8], outline=MUTED, width=2)
        cx = tx + thumb + 28
        cw = x + maxw - cx
        nm = p["name"]
        while d.textlength(nm, font=name_f) > cw and len(nm) > 4:
            nm = nm[:-2].rstrip() + "…"
        d.text((cx, ty + 2), nm, font=name_f, fill=INK)
        where = ", ".join(v for v in [p.get("area"), p.get("city")] if v)
        d.text((cx, ty + 54), where, font=small, fill=MUTED)
        if p.get("order"):
            k, val = "Order", p["order"]
            kw = d.textlength(k, font=small)
            while d.textlength(val, font=small) > cw - kw - 60 and len(val) > 4:
                val = val[:-2].rstrip() + "…"
            vw = d.textlength(val, font=small)
            ly = ty + 92
            d.text((cx, ly), k, font=small, fill=MUTED)
            for dx in range(int(cx + kw + 12), int(x + maxw - vw - 12), 9):
                d.ellipse([dx, ly + 20, dx + 3, ly + 23], fill=MUTED)
            d.text((x + maxw - vw, ly), val, font=small, fill=INK)
        r = int(p.get("rating") or 0)
        if r and thumb >= 130:
            for j in range(5):
                bx = cx + j * 24
                d.ellipse([bx, ty + 136, bx + 14, ty + 150], fill=OLIVE if j < r else None, outline=OLIVE, width=2)
        if i < len(places) - 1:
            d.line([cx, ty + row - 14, x + maxw, ty + row - 14], fill=RULE, width=2)

    d.line([x, foot, x + maxw, foot], fill=RULE, width=2)
    d.text((x + maxw - d.textlength(brand, font=eyebrow), foot + 22), brand, font=eyebrow, fill=MUTED)
    d.text((x, foot + 22), f"{len(places)} PLACES", font=eyebrow, fill=MUTED)
    card.save(o.out, "PNG", optimize=True)
    print(o.out)


if __name__ == "__main__":
    main()
