"""Verifier: dropped topic homes that a looser reading (a topic is named when any of its
readings in topics.json is named by a held line) would keep. Run from the worktree."""
import ast, json, re, subprocess

BASE = "fbdb53d2a2860a95257235dc7f592ab0e75ce45e"
P = "skills/chantier/scripts/cli/tests/test_card_homes.py"


def homes(rev):
    s = subprocess.run(["git", "show", f"{rev}:{P}"], capture_output=True, text=True,
                       encoding="utf-8", check=True).stdout
    d = [n for n in ast.parse(s).body
         if isinstance(n, ast.Assign) and n.targets[0].id == "HOMES"][0]
    return {k: v[0].split() for k, v in ast.literal_eval(d.value).items()}


data = json.load(open("skills/chantier/references/topics.json", encoding="utf-8"))
topics = data.get("topics", data)
base, head = homes(BASE), homes("HEAD")
held = [l for l in open("docs/protective-rules.md", encoding="utf-8") if "| `held` |" in l]
named = set(re.findall(r"`topics/([a-z0-9-]+)\.md`", " ".join(held)))
n = 0
for k, v in base.items():
    for t in v:
        if t in head.get(k, []):
            continue
        entry = topics.get(t) if isinstance(topics, dict) else None
        pages = set(re.findall(r"topics/([a-z0-9-]+)\.md", json.dumps(entry)))
        if pages & named:
            n += 1
            print(k, t, "-> named pages:", sorted(pages & named))
print("dropped homes a looser reading would keep:", n)
