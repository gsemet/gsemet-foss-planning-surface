b = open("C:/Users/gaeta/Projets/chantier.worktrees/batch-29-CR-398/skills/chantier/references/driver.md", "rb").read().replace(b"\r\n", b"\n").decode().split("\n")
heads = [(i, l) for i, l in enumerate(b) if l.startswith("## ")]
common = ["Means: the record and the workers", "Means: context and your folder", "Means: worktree, rebase and push", "Means: the long gate", "Means: CI", "Means: commits, the PR's state and the evidence", "Means: your end", "CR driver"]
tot = len("\n".join(b[: heads[0][0]]).encode())
for k, (i, l) in enumerate(heads):
    j = heads[k + 1][0] if k + 1 < len(heads) else len(b)
    n = len("\n".join(b[i:j]).encode()) + 1
    if l[3:] in common:
        tot += n
    print(n, l)
print("opening", len("\n".join(b[: heads[0][0]]).encode()), "TOTAL", tot)
