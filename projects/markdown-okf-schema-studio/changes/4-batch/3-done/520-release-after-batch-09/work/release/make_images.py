"""Compose the release images from the verified captures."""

import sys
from pathlib import Path

from PIL import Image, ImageDraw

archives, folder = Path(sys.argv[1]), Path(sys.argv[2])
folder.mkdir(parents=True, exist_ok=True)

admonition = next(archives.glob("*-514-*")) / "work/verifier/evidence"
region = (130, 290, 1670, 846)
halves = []
for name in ("before-admonition-body-click.png", "after-admonition-body-click.png"):
    half = Image.open(admonition / name).convert("RGB").crop(region)
    halves.append(half.resize((half.width // 2, half.height // 2), Image.LANCZOS))
gap = 24
width = halves[0].width + halves[1].width + gap
joined = Image.new("RGB", (width, halves[0].height), halves[0].getpixel((1, 1)))
joined.paste(halves[0], (0, 0))
joined.paste(halves[1], (halves[0].width + gap, 0))
x = halves[0].width + gap // 2
ImageDraw.Draw(joined).line([(x, 0), (x, joined.height)], fill=(110, 110, 110), width=2)
joined.save(folder / "admonition-block-edit-before-after.png", optimize=True)

chart = next(archives.glob("*-503-*")) / "evidence/chart-hover-cream.png"
Image.open(chart).convert("RGB").crop((148, 726, 672, 1008)).save(
    folder / "chart-hover.png", optimize=True
)
