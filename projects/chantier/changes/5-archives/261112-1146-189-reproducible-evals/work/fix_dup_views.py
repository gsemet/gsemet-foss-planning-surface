import re

p = "src/shelf/views.py"
t = open(p, encoding="utf-8").read()
m = re.search(r"<<<<<<< [^\n]*\n(.*?)=======\n(.*?)>>>>>>> [^\n]*\n", t, re.S)
head = m.group(1)
old = 'status: str = "", query: str = "", sort: str = "oldest"\n) -> str:'
assert old in head
head = head.replace(old, 'status: str = "", query: str = "", sort: str = "oldest",\n    duplicate: dict | None = None,\n) -> str:')
t = t[: m.start()] + head + t[m.end():]
open(p, "w", encoding="utf-8", newline="\n").write(t)
