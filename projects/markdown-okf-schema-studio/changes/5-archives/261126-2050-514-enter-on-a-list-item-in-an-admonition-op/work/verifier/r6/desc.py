import difflib, json, pathlib, re, sys

work = pathlib.Path(sys.argv[1])


def body(name):
    return json.loads((work / name).read_text(encoding="utf-8"))["body"].replace("\r\n", "\n")


old = body("verifier/r5/pr-540-f9dc2c6-closing.json")
new = body("verifier/r6/pr-540-f9dc2c6-sixth.json")
local = (work / "pr-body.md").read_text(encoding="utf-8").replace("\r\n", "\n")
meta = json.loads((work / "verifier/r6/pr-540-f9dc2c6-sixth.json").read_text(encoding="utf-8"))
print({k: meta[k] for k in ("number", "headRefOid", "baseRefName", "baseRefOid", "isDraft", "state", "title", "updatedAt")})
print("old chars", len(old), "new chars", len(new), "local chars", len(local))
print("posted equals pr-body.md (trailing newline ignored):", new.rstrip("\n") == local.rstrip("\n"))
a, b = old.split("\n"), new.split("\n")
for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
    if tag == "equal":
        continue
    print(f"== {tag} old {i1 + 1}-{i2} new {j1 + 1}-{j2}")
    for line in a[i1:i2]:
        print("- " + line)
    for line in b[j1:j2]:
        print("+ " + line)
print("== marks and sections")
print("STALE:", "STALE" in new, "UNVERIFIED:", "UNVERIFIED" in new, "unchecked boxes:", new.count("- [ ]"), "checked:", new.count("- [x]"))
print([line for line in new.split("\n") if line.startswith("## ")])
print("== role words")
for number, line in enumerate(new.split("\n"), 1):
    if re.search(r"(?i)\b(coder|inspector|verifier|driver|foreman|chantier|reviewer|agent)\b", line):
        print(number, line)
print("== local paths (drive letter, users or home folder, user name)")
names = {pathlib.Path.home().name.lower()}
hits = 0
for number, line in enumerate(new.split("\n"), 1):
    low = line.lower().replace("\\", "/")
    if re.search(r"(?<![a-z])[a-z]:/(?!/)", low) or "/users/" in low or "/home/" in low or any(n in low.replace("gsemet", "") for n in names):
        hits += 1
        print(number, line)
print("lines matched:", hits)
print("== full body, numbered")
for number, line in enumerate(new.split("\n"), 1):
    print(f"{number:3} {line}")
