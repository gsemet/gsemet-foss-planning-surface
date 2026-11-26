"""topics.json against HEAD: existing entries changed or removed, and the foreman's list."""

import json
import subprocess

WT = "C:/Users/gaeta/Projets/chantier.worktrees/batch-31-CR-507"
P = "skills/chantier/cards-next/topics.json"
old = json.loads(subprocess.run(["git", "-C", WT, "show", f"HEAD:{P}"], capture_output=True, text=True,
                                encoding="utf-8", check=True).stdout)
new = json.loads(open(f"{WT}/{P}", encoding="utf-8").read())
print("top keys", list(old), list(new))
for key in new:
    if key != "topics" and old.get(key) != new[key]:
        print("top key changed:", key)
a, b = old["topics"], new["topics"]
if isinstance(a, list):
    a, b = {t["name"]: t for t in a}, {t["name"]: t for t in b}
print(len(a), "topics at HEAD,", len(b), "now; removed:", sorted(set(a) - set(b)))
print("added:", len(set(b) - set(a)))
for name in a:
    if name in b and a[name] != b[name]:
        x, y = a[name], b[name]
        for k in sorted(set(x) | set(y)):
            if x.get(k) != y.get(k):
                print(" ", name, k, ":", x.get(k), "->", y.get(k))
for n in ("take-back", "orders", "hold", "stack", "lease", "retro", "merge", "long-gate", "local-gate",
          "lost-driver", "wakes", "session-shell", "refused-push"):
    t = b.get(n)
    print(n, "exists" if t else "MISSING", {k: v for k, v in (t or {}).items() if k in ("roles", "for")})
