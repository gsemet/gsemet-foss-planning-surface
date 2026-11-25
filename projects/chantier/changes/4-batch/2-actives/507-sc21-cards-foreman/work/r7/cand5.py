import pathlib
p = pathlib.Path("cand.py")
s = p.read_text(encoding="utf-8")
for a, b in [("else as unknown.", "else unknown."), ("as its drop order says", "per its drop order"), ("never your memory of another", "never memory of another")]:
    assert s.count(a) >= 1, a
    s = s.replace(a, b)
p.write_text(s, encoding="utf-8")
