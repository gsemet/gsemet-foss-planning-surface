import re, sys, json, pathlib
CRF = pathlib.Path(r"C:/Users/gaeta/Projets/gsemet-foss-planning-surface/projects/chantier/changes/4-batch/2-actives/507-sc21-cards-foreman/work/coder3")
OUT = pathlib.Path(r"C:/Users/gaeta/Projets/chantier.worktrees/batch-31-CR-507/skills/chantier/cards-next/topics")
write = "--write" in sys.argv
LIMIT = 1450
seen, parts, sizes = {}, {}, {}
for b in sorted(CRF.glob("b[0-9]*.txt")):
    sp = re.split(r"^=== (\S+)\n", b.read_text(encoding="utf-8"), flags=re.M)
    for name, body in zip(sp[1::2], sp[2::2]):
        body = body.rstrip("\n") + "\n"
        if name in seen:
            print("DUP", name)
        seen[name] = len(body.encode("utf-8"))
        if seen[name] <= 1500:
            chunks = [(name, body)]
        else:
            lines = body.split("\n")
            title = lines[0]
            rest = [l for l in lines[1:] if l != ""]
            groups, cur = [], []
            for l in rest:
                cand = "\n".join([title + " (part 1 of 9)", ""] + cur + [l]) + "\n"
                if cur and len(cand.encode("utf-8")) > LIMIT:
                    groups.append(cur)
                    cur = [l]
                else:
                    cur.append(l)
            groups.append(cur)
            chunks = [(f"{name}-p{i+1}", f"{title} (part {i+1} of {len(groups)})\n\n" + "\n".join(g) + "\n") for i, g in enumerate(groups)]
            parts[name] = [c[0] for c in chunks]
        for cn, cb in chunks:
            n = len(cb.encode("utf-8"))
            sizes[cn] = n
            if n > 1500:
                print("STILL OVER", cn, n)
            if write:
                (OUT / f"{cn}.md").write_text(cb, encoding="utf-8", newline="\n")
json.dump({"parts": parts, "sizes": sizes, "names": list(seen)}, open(CRF / "parts.json", "w"), indent=1)
print(len(seen), "topics;", len(parts), "split;", len(sizes), "files")
