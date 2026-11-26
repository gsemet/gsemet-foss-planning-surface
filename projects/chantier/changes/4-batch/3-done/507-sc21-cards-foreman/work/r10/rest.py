"""Round 10: the flagged rows not in chunks/index.txt, each with its words missing from the home,
the source text and the home sentences nearest to it.

usage: rest.py <min score> <max chars per chunk>"""

import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from audit import check, home_text, idf_table, segments, stems  # noqa: E402
from inv import home_files  # noqa: E402

MIN, MAX = float(sys.argv[1]), int(sys.argv[2])
done = {line.split()[1] for line in (HERE / "chunks" / "index.txt").read_text(encoding="utf-8").splitlines()}
idf, top = idf_table()
cache, out, count = {}, [], 0
for inv, r, path, seg in segments():
    files = home_files(r["new home"])
    if not files or r["id"] in done:
        continue
    score, lost, bad = check(seg, files, idf, top, cache)
    if score < MIN:
        continue
    count += 1
    sents = [s for s in re.split(r"(?<=[.;:])\s+|\n+", home_text(files)) if s.strip()]
    want = set(stems(seg))
    near = sorted(range(len(sents)), key=lambda i: -len(want & set(stems(sents[i]))))[:3]
    block = [f"{r['id']} [{r['kind']}] -> {','.join(sorted(files))}", f"  S: {seg}"]
    block += [f"  H: {sents[i].strip()[:400]}" for i in sorted(near)]
    out.append("\n".join(block))

(HERE / "rest").mkdir(exist_ok=True)
chunk, number = [], 1
for block in out:
    if chunk and sum(len(x) + 1 for x in chunk) + len(block) > MAX:
        (HERE / "rest" / f"{number:02d}.txt").write_text("\n".join(chunk) + "\n", encoding="utf-8", newline="\n")
        chunk, number = [], number + 1
    chunk.append(block)
if chunk:
    (HERE / "rest" / f"{number:02d}.txt").write_text("\n".join(chunk) + "\n", encoding="utf-8", newline="\n")
print("rows", count, "chunks", number)
