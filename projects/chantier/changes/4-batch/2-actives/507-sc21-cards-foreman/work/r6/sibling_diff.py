"""Every changed line of the cards-next files that existed at HEAD (topics.json apart), by word."""

import difflib
import re
import subprocess

WT = "C:/Users/gaeta/Projets/chantier.worktrees/batch-31-CR-507"
D = "skills/chantier/cards-next"


def git(*args: str) -> str:
    return subprocess.run(["git", "-C", WT, *args], capture_output=True, text=True, encoding="utf-8",
                          check=True).stdout


changed = git("diff", "HEAD", "--name-status", "--", D).split("\n")
for entry in filter(None, changed):
    status, path = entry.split("\t")
    name = path[len(D) + 1:]
    if name == "topics.json" or status != "M":
        print("##", status, name)
        continue
    old = git("show", f"HEAD:{path}").split("\n")
    new = open(f"{WT}/{path}", encoding="utf-8").read().replace("\r\n", "\n").split("\n")
    print("##", name)
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(a=old, b=new, autojunk=False).get_opcodes():
        if tag == "equal":
            continue
        print(f"  {tag} old {i1 + 1}-{i2} new {j1 + 1}-{j2}")
        if tag == "replace" and i2 - i1 == j2 - j1:
            for k in range(i2 - i1):
                a = re.findall(r"\S+|\s+", old[i1 + k])
                b = re.findall(r"\S+|\s+", new[j1 + k])
                for t, x1, x2, y1, y2 in difflib.SequenceMatcher(a=a, b=b, autojunk=False).get_opcodes():
                    if t != "equal":
                        print(f"    :{j1 + k + 1} [{''.join(a[x1:x2])[:200]}] -> [{''.join(b[y1:y2])[:240]}]")
        else:
            for k in range(i1, i2):
                print(f"    -{k + 1} {old[k][:240]}")
            for k in range(j1, j2):
                print(f"    +{k + 1} {new[k][:240]}")
