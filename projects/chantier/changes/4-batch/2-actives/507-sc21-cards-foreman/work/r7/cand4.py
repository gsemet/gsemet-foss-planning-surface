import pathlib
p = pathlib.Path("cand.py")
s = p.read_text(encoding="utf-8")
SUB = {
3: [("In direct mode the Chief of Staff uses", "Direct mode: the Chief of Staff uses")],
7: [("`, and stop.", "`, then stop.")],
13: [("a queued critical-path CR or the user's next merge only, never on a Driver's say.", "a critical-path CR or the user's next merge only, not on a Driver's say.")],
16: [("Stop stray tasks by id;", "Stop stray background tasks by id;")],
21: [("(its waiver must name it;", "(a waiver must name it;")],
22: [("no branch protection read", "branch protection unread")],
25: [("replace a Driver on silence, or but by `help lost-restart`;", "replace a Driver but by `help lost-restart`, nor on silence alone;")],
31: [("End: the CLI pauses the batch at the last CR.", "End: the CLI pauses at the last CR.")],
}
start = s.index("NEW = {"); end = s.index("here = pathlib")
cur = {}
exec(s[start:end].replace("NEW = {", "cur = {"), cur)
m = dict(cur["cur"])
for k, subs in SUB.items():
    if k not in m:
        m[k] = (p.parent / "foreman.before.md").read_text(encoding="utf-8").split("\n")[k - 1]
    for a, b in subs:
        assert a in m[k], (k, a)
        m[k] = m[k].replace(a, b)
body = "NEW = {\n" + "".join(f'    {k}: """{m[k]}""",\n' for k in sorted(m)) + "}\n"
p.write_text(s[:start] + body + s[end:], encoding="utf-8")
