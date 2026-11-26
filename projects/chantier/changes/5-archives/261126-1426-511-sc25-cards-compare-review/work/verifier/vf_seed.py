import re
import sys
from collections import Counter
from pathlib import Path

wt = Path(sys.argv[1])
done = Path(sys.argv[2])
files = [
    done / "505-sc19-cards-workers/evidence/cards-inventory-workers.md",
    done / "505-sc19-cards-workers/evidence/cards-inventory-drivers.md",
    done / "507-sc21-cards-foreman/evidence/cards-inventory-foreman.md",
    done / "507-sc21-cards-foreman/evidence/cards-inventory-chief-of-staff.md",
    done / "507-sc21-cards-foreman/evidence/cards-inventory-griller.md",
    done / "507-sc21-cards-foreman/evidence/cards-inventory-host-and-shared.md",
]


def cells(line):
    parts = re.split(r"(?<!\\)\|", line.strip()[1:-1])
    return [p.strip() for p in parts]


final = {}
section = None
for line in (wt / "docs/proofs/cards-inventory.md").read_text("utf-8").splitlines():
    if line.startswith("## "):
        section = line[3:]
    elif section == "Rows" and line.startswith("| "):
        c = cells(line)
        if re.match(r"^[A-Z]{1,2}-", c[0]):
            final[c[0]] = c[5]

seed = {}
conflicts = []
for path in files:
    header = None
    for line in path.read_text("utf-8").split("\n"):
        if not line.startswith("|"):
            header = None
            continue
        c = cells(line)
        if header is None:
            header = [x.lower() for x in c]
            continue
        if not (header[0] == "id" and "source" in header and "kind" in header and "trigger" in header):
            continue
        rid = c[0].strip("`")
        if not re.match(r"^[A-Z]{1,2}-[A-Z]?\d{3,4}$", rid):
            continue
        k = header.index("kind")
        # a row with an unescaped pipe has extra cells: take the first single-letter kind cell
        if len(c) == len(header):
            kind = c[k].strip("`")
        else:
            kind = next((x for x in c[k:] if re.fullmatch(r"[a-f]", x)), "?")
        if rid in seed and seed[rid] != kind:
            conflicts.append((rid, seed[rid], kind))
        seed[rid] = kind

print("final rows", len(final), "seed rows parsed", len(seed))
common = sorted(set(final) & set(seed))
diff = [(i, seed[i], final[i]) for i in common if seed[i] != final[i]]
print("common", len(common), "kind differs", len(diff))
for d in diff[:40]:
    print("  ", d)
extra = sorted(set(final) - set(seed))
print("final ids with no seed row", len(extra), extra[:40])
gone = sorted(set(seed) - set(final))
print("seed ids not in final", len(gone), Counter(seed[i] for i in gone), gone[:40])
print("seed duplicate conflicts", conflicts[:10])
