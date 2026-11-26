"""Round 10: the rows whose home names no text file, of the forms given, with their behaviour.

usage: nofile.py <form regex>"""

import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from inv import home_files, rows  # noqa: E402

count = 0
for inv, n, r in rows():
    home = r["new home"]
    if home_files(home) or not re.match(sys.argv[1], home.strip("`")):
        continue
    count += 1
    print(f"{r['id']} [{r['kind']}] -> {home[:200]}")
    print(f"    {r['behaviour'][:420]}")
    print(f"    ({r['source']})")
print("rows", count)
