import re
from pathlib import Path

W = Path("<worktree>/skills/chantier/cards-next")
F = Path("<CR folder>/evidence/cards-inventory-foreman.md")
card = (W / "foreman.md").read_text(encoding="utf-8").split("\n")
used = {}
for line in F.read_text(encoding="utf-8").split("\n"):
    c = [x.strip() for x in re.split("(?<!" + chr(92)*2 + ")" + chr(92) + "|", line.strip())[1:-1]]
    if len(c) != 8 or not c[0].startswith("FM-"):
        continue
    rid, _, trig, beh, src, kind, home, check = c
    m = re.search(r"foreman\.md:(\d+)", home)
    if m and home.startswith("card"):
        used.setdefault(int(m[1]), []).append((rid, kind, trig, beh))
for n in sorted(used):
    print(f"\n### foreman.md:{n}: {card[n-1][:110]}")
    for rid, kind, trig, beh in used[n]:
        if n == 21 or (n == 22 and kind == "a"):
            continue
        print(f"  {rid} {kind} | {beh[:170]}")
    if n in (21, 22):
        print("  ids:", [r[0] for r in used[n]])
print("\nevidence in card:", [i + 1 for i, l in enumerate(card) if "evidence" in l.lower()])
