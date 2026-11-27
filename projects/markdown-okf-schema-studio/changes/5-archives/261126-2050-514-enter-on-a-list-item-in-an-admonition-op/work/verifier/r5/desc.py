import difflib, json, pathlib, re, sys

work = pathlib.Path(sys.argv[1])


def body(name):
    return json.loads((work / name).read_text(encoding="utf-8"))["body"].replace("\r\n", "\n")


old = body("verifier/pr-540-f9dc2c6-second.json")
new = body("verifier/r5/pr-540-f9dc2c6-closing.json")
local = (work / "pr-body.md").read_text(encoding="utf-8").replace("\r\n", "\n")
meta = json.loads((work / "verifier/r5/pr-540-f9dc2c6-closing.json").read_text(encoding="utf-8"))
print({k: meta[k] for k in ("number", "headRefOid", "baseRefName", "isDraft", "state", "title", "updatedAt")})
print("old chars", len(old), "new chars", len(new), "local chars", len(local))
print("posted equals pr-body.md (trailing newline ignored):", new.rstrip("\n") == local.rstrip("\n"))
a, b = old.split("\n"), new.split("\n")
matcher = difflib.SequenceMatcher(None, a, b, autojunk=False)
for tag, i1, i2, j1, j2 in matcher.get_opcodes():
    if tag == "equal":
        continue
    print(f"== {tag} old {i1 + 1}-{i2} new {j1 + 1}-{j2}")
    for line in a[i1:i2]:
        print("- " + line)
    for line in b[j1:j2]:
        print("+ " + line)
print("== links of the posted body")
for url in re.findall(r"https://[^\s)\"<>]+", new):
    print(url)
print("== marks and sections")
print("STALE:", "STALE" in new, "UNVERIFIED:", "UNVERIFIED" in new, "unchecked boxes:", new.count("- [ ]"), "checked:", new.count("- [x]"))
print([line for line in new.split("\n") if line.startswith("## ")])
print("== role words")
for number, line in enumerate(new.split("\n"), 1):
    if re.search(r"(?i)\b(coder|inspector|verifier|driver|foreman|chantier|reviewer|agent)\b", line):
        print(number, line)
print("== local paths")
for number, line in enumerate(new.split("\n"), 1):
    if re.search(r"(?i)([a-z]:[\\/]|/users/|\\users\\|/home/)", line):
        print(number, line)
