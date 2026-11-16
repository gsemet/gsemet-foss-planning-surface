import json, sys
path, before_path, rules_path = sys.argv[1:4]
raw = open(path, "rb").read()
assert not raw.startswith(b"\xef\xbb\xbf"), "BOM"
doc = json.loads(raw.decode("utf-8"))
allow = doc["permissions"]["allow"]
assert len(allow) == len(set(allow)), "duplicate"
rules = json.load(open(rules_path, encoding="utf-8-sig"))
assert all(r in allow for r in rules), "a rule is missing"
if before_path != "-":
    before = json.loads(open(before_path, "rb").read().decode("utf-8-sig"))
    def walk(a, b, where=""):
        for k, v in a.items():
            assert k in b, f"key removed: {where}{k}"
            if k == "allow" and where == "permissions.":
                assert all(x in b[k] for x in v), "rule removed"
            elif isinstance(v, dict):
                walk(v, b[k], where + k + ".")
            else:
                assert v == b[k], f"value changed: {where}{k}"
    walk(before, doc)
print("OK valid JSON, no BOM, no duplicate, nothing removed;", len(allow), "allow rules")

