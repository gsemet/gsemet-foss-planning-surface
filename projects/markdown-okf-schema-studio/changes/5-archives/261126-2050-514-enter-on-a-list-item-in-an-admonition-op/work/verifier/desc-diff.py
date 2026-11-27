import json, sys, difflib, pathlib
work = pathlib.Path(sys.argv[1])
def body(p):
    return json.loads((work / p).read_text(encoding="utf-8"))["body"].replace("\r\n", "\n")
old = body("verifier/pr-540-f9dc2c6-end.json")
new = body("verifier/pr-540-f9dc2c6-second.json")
local = (work / "pr-body.md").read_text(encoding="utf-8").replace("\r\n", "\n")
print("old chars", len(old), "new chars", len(new), "local chars", len(local))
print("posted equals pr-body.md (trailing newline ignored):", new.rstrip("\n") == local.rstrip("\n"))
a, b = old.split("\n"), new.split("\n")
sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == "equal":
        continue
    print(f"== {tag} old {i1+1}-{i2} new {j1+1}-{j2}")
    for l in a[i1:i2]:
        print("- " + l)
    for l in b[j1:j2]:
        print("+ " + l)
