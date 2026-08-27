#!/usr/bin/env python3
"""Regenerate the favicon set and the Open Graph social card.

    python3 tools/make-brand-assets.py          # from the repo root

Writes assets/favicon.ico, apple-touch-icon.png, icon-192.png, icon-512.png
and og-image.png. assets/favicon.svg is hand-maintained — keep it in sync
with HOUSE/CROSS below if you change the glyph.

Brand fonts (Lora, Lato) are not vendored as TTF. They are already embedded
as woff2 subsets inside index.html's bundle manifest, so this script pulls
them straight back out — no network, no font files to track.

Requires: pip install Pillow fonttools brotli
"""
import base64
import gzip
import json
import os
import re
import sys

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "assets")
BUNDLE = os.path.join(ROOT, "index.html")

# Brand palette — see README "Brand quick reference"
BARK, CREAM, SAND = (58, 50, 43), (244, 237, 226), (219, 174, 132)
MUTED, PANEL, TERRA = (184, 164, 140), (74, 64, 56), (168, 97, 63)

# The mark, simplified for small sizes. The full line-art logo in
# assets/mbc-mark.png turns to mush below ~48px, so icons use a solid
# house silhouette with the cross knocked out of it. 100-unit coordinates.
HOUSE = [(50, 20), (79, 45), (79, 81), (21, 81), (21, 45)]
CROSS = [(45.5, 34, 54.5, 75), (33, 49, 67, 58)]

SS = 8  # supersample factor, downsampled with LANCZOS


# ── icons ────────────────────────────────────────────────────────────────
def glyph(size, radius_frac=0.18, bg=BARK, fg=SAND):
    n = size * SS
    k = n / 100.0
    im = Image.new("RGBA", (n, n), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if radius_frac:
        d.rounded_rectangle([0, 0, n - 1, n - 1], radius=int(n * radius_frac), fill=bg)
    else:
        d.rectangle([0, 0, n - 1, n - 1], fill=bg)
    d.polygon([(x * k, y * k) for x, y in HOUSE], fill=fg)
    for x0, y0, x1, y1 in CROSS:
        d.rectangle([x0 * k, y0 * k, x1 * k, y1 * k], fill=bg)
    return im.resize((size, size), Image.LANCZOS)


def make_icons():
    # Lives at the repo root: /favicon.ico is the well-known path that
    # browsers and link previewers probe without reading the page.
    glyph(64).save(os.path.join(ROOT, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)])
    # iOS applies its own mask and dislikes alpha, so: square, opaque.
    glyph(180, radius_frac=0.0).convert("RGB").save(os.path.join(ASSETS, "apple-touch-icon.png"))
    glyph(192).save(os.path.join(ASSETS, "icon-192.png"))
    glyph(512).save(os.path.join(ASSETS, "icon-512.png"))
    print("wrote favicon.ico (root), apple-touch-icon.png, icon-192.png, icon-512.png")


# ── fonts, recovered from the bundle ─────────────────────────────────────
def extract_fonts(dest):
    """Pull Lora/Lato woff2 subsets out of the bundle and convert them to TTF.

    Returns {(family, weight, italic): path}. The bundle ships each family
    sliced by unicode-range and by style, so we keep only slices that cover
    basic latin and index them by what they actually are — picking blind
    gets you the italic slice.
    """
    from fontTools.ttLib import TTFont

    src = open(BUNDLE, encoding="utf-8").read()
    man = json.loads(re.search(r'<script type="__bundler/manifest">(.*?)</script>',
                               src, re.S).group(1))
    os.makedirs(dest, exist_ok=True)
    found = {}
    for uuid, entry in man.items():
        if entry["mime"] != "font/woff2":
            continue
        raw = base64.b64decode(entry["data"])
        if entry.get("compressed"):
            raw = gzip.decompress(raw)
        tmp = os.path.join(dest, uuid + ".woff2")
        open(tmp, "wb").write(raw)
        try:
            f = TTFont(tmp)
            cmap = set(f.getBestCmap())
            # Keep only slices covering the characters the card actually sets.
            if not all(ord(c) in cmap for c in "MemorialBaptistChurch ,.·0123456789"):
                continue
            fam = f["name"].getDebugName(1) or "?"
            weight = f["OS/2"].usWeightClass
            italic = bool(f["OS/2"].fsSelection & 1) or f["post"].italicAngle != 0
            key = (fam, weight, italic)
            if key in found:
                continue
            out = os.path.join(dest, "%s-%s-%s.ttf" % (fam.replace(" ", ""), weight,
                                                       "i" if italic else "n"))
            f.flavor = None
            f.save(out)
            found[key] = out
        except Exception:
            continue
        finally:
            if os.path.exists(tmp):
                os.remove(tmp)
    return found


def pick(found, family, weight):
    """Nearest upright face of `family` at or above `weight`."""
    cands = [(w, p) for (fam, w, it), p in found.items() if fam == family and not it]
    if not cands:
        return None
    return min(cands, key=lambda wp: (abs(wp[0] - weight), wp[0]))[1]


# ── social card ──────────────────────────────────────────────────────────
def make_og(fonts):
    W, H = 1200, 630
    S = lambda v: v * SS
    lora = pick(fonts, "Lora", 400)     # headings
    lato = pick(fonts, "Lato", 400)     # tagline
    lato7 = pick(fonts, "Lato", 700)    # kicker + address, letter-spaced
    if not (lora and lato and lato7):
        print("!! could not recover Lora/Lato from the bundle; skipping og-image",
              file=sys.stderr)
        return
    F = lambda p, s: ImageFont.truetype(p, s * SS)

    im = Image.new("RGB", (W * SS, H * SS), BARK)
    d = ImageDraw.Draw(im)

    def tracked(xy, text, font, fill, track=0):
        x, y = xy
        for ch in text:
            d.text((x, y), ch, font=font, fill=fill)
            x += d.textlength(ch, font=font) + track * SS

    def wrap(text, font, max_w):
        lines, cur = [], ""
        for w in text.split():
            t = (cur + " " + w).strip()
            if d.textlength(t, font=font) <= max_w:
                cur = t
            else:
                lines.append(cur)
                cur = w
        return lines + ([cur] if cur else [])

    # Arch panel — the brand's signature photo crop, echoed as a shape.
    ax0, ax1, ay0, ay1 = S(792), S(1120), S(96), S(534)
    r = (ax1 - ax0) // 2
    d.rectangle([ax0, ay0 + r, ax1, ay1], fill=PANEL)
    d.pieslice([ax0, ay0, ax1, ay0 + 2 * r], 180, 360, fill=PANEL)

    cx, cy, g = (ax0 + ax1) // 2, S(300), S(150)
    k = g / 100.0
    d.polygon([(cx + (x - 50) * k, cy + (y - 50) * k) for x, y in HOUSE], fill=SAND)
    for x0, y0, x1, y1 in CROSS:
        d.rectangle([cx + (x0 - 50) * k, cy + (y0 - 50) * k,
                     cx + (x1 - 50) * k, cy + (y1 - 50) * k], fill=PANEL)

    x = S(88)
    tracked((x, S(104)), "MIDTOWN TULSA · SINCE 1948", F(lato7, 19), SAND, track=3.4)
    title = F(lora, 78)
    d.text((x, S(168)), "Memorial", font=title, fill=CREAM)
    d.text((x, S(262)), "Baptist Church", font=title, fill=CREAM)

    sub = F(lato, 30)
    y = S(392)
    for line in wrap("For the glory of God and the good of all people.", sub, S(468)):
        d.text((x, y), line, font=sub, fill=MUTED)
        y += S(44)

    d.rectangle([x, S(500), x + S(54), S(504)], fill=TERRA)
    tracked((x, S(538)), "2800 S. YALE AVE., TULSA  ·  SUNDAYS 10:30 AM",
            F(lato7, 20), CREAM, track=1.8)

    im.resize((W, H), Image.LANCZOS).save(os.path.join(ASSETS, "og-image.png"))
    print("wrote og-image.png")


if __name__ == "__main__":
    import tempfile

    make_icons()
    with tempfile.TemporaryDirectory() as tmp:
        make_og(extract_fonts(tmp))
