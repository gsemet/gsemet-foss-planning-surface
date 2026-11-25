import pathlib
p = pathlib.Path("cand.py")
s = p.read_text(encoding="utf-8")
before = (p.parent / "foreman.before.md").read_text(encoding="utf-8").split("\n")
start = s.index("NEW = {"); end = s.index("here = pathlib")
cur = {}
exec(s[start:end].replace("NEW = {", "cur = {"), cur)
m = dict(cur["cur"])
SUB = [
(3, "no decision of the user's taken from them", "every decision of theirs left to them"),
(9, "- Read the rules and `status`, send", "- Read rules and `status`; send"),
(10, "(stack batch: `help stack` too)", "(stack: `help stack` too)"),
(16, "(it advises, refusals rule)", "(refusals rule over it)"),
(17, "- The retro (`retro draft --epoch <n>`), then `final`.", "- `retro draft --epoch <n>`, then `final`."),
(22, "(a push judged too)", "(a push judged too; never `-x` or `--exec`, a conflict left stopped)"),
(22, "once its Driver ends", "after its Driver ends"),
(22, "closing or drafting a dropped CR's PR per its drop order", "closing/drafting a dropped CR's PR per its drop order"),
(26, "another Foreman owns the batch. Stop at once.", "another Foreman owns the batch; stop."),
]
for k, a, b in SUB:
    m.setdefault(k, before[k - 1])
    assert a in m[k], (k, a)
    m[k] = m[k].replace(a, b)
body = "NEW = {\n" + "".join(f'    {k}: """{m[k]}""",\n' for k in sorted(m)) + "}\n"
p.write_text(s[:start] + body + s[end:], encoding="utf-8")
