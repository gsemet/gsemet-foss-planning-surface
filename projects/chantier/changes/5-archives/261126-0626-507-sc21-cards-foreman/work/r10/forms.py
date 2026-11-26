"""Round 10: the forms of the `new home` cells, and the rows whose home names no text file."""

import collections
import re
import sys

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
from inv import home_files, rows, source_lines, source_range  # noqa: E402

forms = collections.Counter()
nofile = collections.defaultdict(list)
nosrc = []
total = 0
for inv, n, r in rows():
    total += 1
    home = r["new home"]
    head = re.split(r"[ :;(]", home.strip("`"))[0]
    forms[head] += 1
    if not home_files(home):
        nofile[head].append((r["id"], home[:90]))
    rng = source_range(r["source"])
    if not rng or source_lines(rng[0]) is None:
        nosrc.append((r["id"], r["source"][:80]))
print("rows", total)
print(forms.most_common())
for k, v in sorted(nofile.items(), key=lambda kv: -len(kv[1])):
    print(f"--- no text home, form {k}: {len(v)}")
    for x in v[: int(sys.argv[1]) if len(sys.argv) > 1 else 6]:
        print("   ", x)
print("no source:", len(nosrc), nosrc[:20])
