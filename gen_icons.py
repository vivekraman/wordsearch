#!/usr/bin/env python3
"""Generate Brain Games icons using a brain emoji on an indigo rounded background."""

from PIL import Image, ImageDraw, ImageFont

BG = (90, 100, 220, 255)
SIZES = [16, 32, 180, 192, 512]
EMOJI = "🧠"
EMOJI_FONT = "/System/Library/Fonts/Apple Color Emoji.ttc"

# Available bitmap sizes in Apple Color Emoji: 20,32,40,48,64,96,160
# Render at 160px emoji on a proportionally-sized canvas, then scale to target.
RENDER_EMOJI_SIZE = 160
RENDER_ICON_SIZE  = round(RENDER_EMOJI_SIZE / 0.63)   # ~254px


def rounded_rect(draw, x0, y0, x1, y1, r, fill):
    draw.rectangle([x0+r, y0, x1-r, y1], fill=fill)
    draw.rectangle([x0, y0+r, x1, y1-r], fill=fill)
    for ex, ey in [(x0,y0),(x1-2*r,y0),(x0,y1-2*r),(x1-2*r,y1-2*r)]:
        draw.ellipse([ex, ey, ex+2*r, ey+2*r], fill=fill)


def make_icon(size):
    S = RENDER_ICON_SIZE
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    p = round(S * 0.05)
    rounded_rect(d, p, p, S-p, S-p, round(S*0.22), BG)

    font = ImageFont.truetype(EMOJI_FONT, RENDER_EMOJI_SIZE)
    bbox = d.textbbox((0, 0), EMOJI, font=font, embedded_color=True)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    tx = (S - tw) / 2 - bbox[0]
    ty = (S - th) / 2 - bbox[1] - S * 0.02

    d.text((tx, ty), EMOJI, font=font, embedded_color=True)

    return img.resize((size, size), Image.LANCZOS)


for size in SIZES:
    make_icon(size).save(f"icon-{size}.png", "PNG", optimize=True)
    print(f"Saved icon-{size}.png")

make_icon(16).save("favicon.ico", format="ICO", sizes=[(16,16),(32,32)])
print("Saved favicon.ico\nDone!")
