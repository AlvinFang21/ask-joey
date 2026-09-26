"""Turn the portrait wallpaper into bg-portrait.jpg + a wide bg-landscape.jpg.

The landscape version places the wallpaper side by side as
normal | mirrored | normal, so the joins line up and don't show a seam.

Usage: python tools/make_backgrounds.py path/to/wallpaper.jpg
"""
import sys
from pathlib import Path

from PIL import Image, ImageOps

site = Path(__file__).resolve().parent.parent
src = Image.open(sys.argv[1]).convert("RGB")
w, h = src.size

src.save(site / "bg-portrait.jpg", quality=88)

mirrored = ImageOps.mirror(src)
wide = Image.new("RGB", (w * 3, h))
for i, tile in enumerate([src, mirrored, src]):
    wide.paste(tile, (i * w, 0))

# crop to 16:9 around the middle
target_h = min(h, round(wide.width * 9 / 16))
top = (h - target_h) // 2
wide = wide.crop((0, top, wide.width, top + target_h))
wide.save(site / "bg-landscape.jpg", quality=88)
print("portrait", src.size, "landscape", wide.size)
