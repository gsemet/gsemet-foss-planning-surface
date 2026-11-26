"""Round 10: write the flagged rows to review chunks, each home's text once before its rows.

usage: chunks.py <min score> <max chars per chunk>"""

import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from audit import check, idf_table, segments  # noqa: E402
from inv import CARDS, home_files  # noqa: E402

MIN, MAX = float(sys.argv[1]), int(sys.argv[2])
idf, top = idf_table()
cache = {}
groups = {}
seen_rows = 0
for inv, r, path, seg in segments():
    files = home_files(r["new home"])
    if not files:
        continue
    score, lost, bad = check(seg, files, idf, top, cache)
    if score < MIN:
        continue
    seen_rows += 1
    files = set(files)
    main = sorted([f for f in files if f != "floor.md"] or files)
    groups.setdefault(tuple(main), []).append((r, seg, bad, lost, files))


def sortkey(key):
    topic = [f for f in key if f.startswith("topics/")]
    return (0 if topic else 1, (topic or list(key))[0], key)


out = HERE / "chunks"
out.mkdir(exist_ok=True)
chunk, printed, number, index = [], set(), 1, []


def size():
    return sum(len(x) + 1 for x in chunk)


def close():
    global chunk, printed, number
    if chunk:
        (out / f"{number:02d}.txt").write_text("\n".join(chunk) + "\n", encoding="utf-8", newline="\n")
        number += 1
    chunk, printed = [], set()


def heading(f):
    data = (CARDS / f).read_bytes().replace(b"\r\n", b"\n")
    body = data.decode("utf-8").rstrip("\n") if len(data) <= 7000 else "(large: read the file)"
    return f"----- {f} ({len(data)} B)\n{body}"


for key in sorted(groups, key=sortkey):
    files = list(key)
    for r, seg, bad, lost, allf in sorted(groups[key], key=lambda x: x[0]["id"]):
        gone = sorted({g for _, gs, _ in bad for g in gs})[:8]
        hint = ",".join(gone) + ("".join(f" `{s[:40]}`" for s in lost[:4]))
        extra = sorted(allf - set(key))
        more = f" (+{','.join(extra)})" if extra else ""
        row = f"{r['id']}{more}: {seg}" if len(hint) else f"{r['id']}{more}: {seg}"
        block = "\n".join([*(heading(f) for f in files if f not in printed), row])
        if size() + len(block) > MAX and chunk:
            close()
            block = "\n".join([*(heading(f) for f in files), row])
        chunk.append(block)
        printed.update(files)
        index.append((number, r["id"]))
close()
(out / "index.txt").write_text("".join(f"{n:02d} {i}\n" for n, i in index), encoding="utf-8", newline="\n")
print("rows", seen_rows, "groups", len(groups), "chunks", number - 1)
for p in sorted(out.glob("[0-9]*.txt")):
    t = p.read_text(encoding="utf-8")
    print(p.name, len(t), t.count("\n-----") + t.startswith("-----"))
