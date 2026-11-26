"""Read-only: the rows of a source whose home names one of the topics: who.py <source basename> <topic>..."""

import contextlib
import importlib.util
import io
import re
import sys
from pathlib import Path

args = sys.argv[1:]
sys.argv = sys.argv[:1]
spec = importlib.util.spec_from_file_location("sl", Path(__file__).parent / "split_lists.py")
sl = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()):
    spec.loader.exec_module(sl)
src_name, names = args[0], set(args[1:])
for path in sl.FILES:
    for line in path.read_text(encoding="utf-8").splitlines():
        if not re.match(r"\| [A-Z]{1,3}-?B?\d", line):
            continue
        c = [x.strip() for x in re.split(r"(?<!\\)\|", line)[1:-1]]
        if len(c) < 8:
            continue
        if path == sl.HOST:
            idx = [i for i, x in enumerate(c) if i >= 4 and sl.SRC.match(x)]
            if not idx or idx[-1] + 2 >= len(c):
                continue
            i = idx[-1]
            src, home = sl.SRC.match(c[i]).group(1), c[i + 2]
        else:
            m = re.search(r"([A-Za-z-]+\.md)", c[4])
            if not m:
                continue
            src, home = m.group(1), c[6]
        if src.split("/")[-1] != src_name:
            continue
        hit = set(re.findall(r"[a-z0-9][a-z0-9-]*", home)) & names
        if hit and "topic" in home:
            print(path.name, c[0], sorted(hit), "|", home[:160])
