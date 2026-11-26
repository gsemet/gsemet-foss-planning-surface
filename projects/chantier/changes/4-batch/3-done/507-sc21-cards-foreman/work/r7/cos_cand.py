import re, sys, inv
S = re.compile(r"\b(never|not without|only on the user|only with the user|user's (?:own )?(?:word|yes|answer)|only after the user|must not|refus\w*|no guess|without the user)\b", re.I)
T = (inv.EV / "cards-inventory-chief-of-staff.md").read_text(encoding="utf-8")
m = re.search(r"## Protecting-looking rows[^\n]*\n(.*?)(?=\n## |\Z)", T, re.S)
listed = set(re.findall(r"^\| (C-[A-Z0-9]+) \|", m[1], re.M))
out = []
for _, d in inv.rows("chief-of-staff"):
    cand = d["kind"].startswith("e") and "topic " in d["new home"] and S.search(d["behaviour"])
    if cand or d["id"] in listed:
        h = d["new home"]
        topic = h.split(";")[0].replace("topic ", "T:")
        rule = h.split("rule it applies:")[-1].strip() if "rule it applies" in h else "-"
        rule = rule.replace("chief-of-staff.md:", "c").replace("card ", "").replace("floor ", "F")
        out.append(f"{d['id']} [{topic}|{rule}] {d['behaviour'][:230]}")
a, b = int(sys.argv[1]), int(sys.argv[2])
print(len(out))
print("\n".join(out[a:b]))
