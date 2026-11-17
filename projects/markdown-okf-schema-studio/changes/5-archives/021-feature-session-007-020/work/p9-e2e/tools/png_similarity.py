"""Read-only: report exact, near-duplicate and low-information PNGs in the e2e screenshot folder.

Usage: .venv/bin/python -I <this file> out/reports/e2e/screenshots
"""
import hashlib
import itertools
import pathlib
import sys

from PIL import Image, ImageStat

root = pathlib.Path(sys.argv[1])
rows = []
for path in sorted(root.glob("*.png")):
    image = Image.open(path).convert("L")
    thumb = list(image.resize((48, 48)).getdata())
    stat = ImageStat.Stat(image)
    rows.append((path.name, image.size, stat.stddev[0], thumb,
                 hashlib.sha256(path.read_bytes()).hexdigest()))
print("# exact duplicates")
by_hash = {}
for name, *_rest, digest in rows:
    by_hash.setdefault(digest, []).append(name)
for names in by_hash.values():
    if len(names) > 1:
        print("EXACT", " ".join(names))
print("# low information (stddev < 12)")
for name, size, std, *_ in rows:
    if std < 12:
        print("LOWINFO", name, size, round(std, 1))
print("# near duplicates (same size, mean abs thumb diff < 1.0, not exact)")
for a, b in itertools.combinations(rows, 2):
    if a[1] != b[1] or a[4] == b[4]:
        continue
    diff = sum(abs(x - y) for x, y in zip(a[3], b[3])) / len(a[3])
    if diff < 1.0:
        print("NEAR", round(diff, 3), a[0], b[0])
