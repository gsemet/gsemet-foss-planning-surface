import pathlib
p = pathlib.Path("cand.py")
s = p.read_text(encoding="utf-8")
for a, b in [
    ("(a push judged too; never `-x` or `--exec`, a conflict left stopped)", "(a push judged too; no `-x`/`--exec`; a conflict stays stopped)"),
    ("(`inbox --epoch <n>`) at next wake", "(`inbox --epoch <n>`) next wake"),
]:
    assert s.count(a) == 1, a
    s = s.replace(a, b)
p.write_text(s, encoding="utf-8")
