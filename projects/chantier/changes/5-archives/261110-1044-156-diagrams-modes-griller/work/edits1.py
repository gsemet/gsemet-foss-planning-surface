import sys, io, os

os.chdir(sys.argv[1])


def rep(f, old, new, count=1):
    with open(f, encoding="utf-8", newline="") as fh:
        t = fh.read()
    n = t.count(old)
    if n != count:
        raise SystemExit(f"{f}: expected {count} of {old!r}, found {n}")
    with open(f, "w", encoding="utf-8", newline="") as fh:
        fh.write(t.replace(old, new))


S = "docs/cr-lifecycle-simple.svg"
T = "docs/cr-lifecycle-simple-texts.md"
rep(S, " · 👷 Foreman · 🚜 driver · 🔨 worker</text>", " · 🔥 Griller (optional) · 👷 Foreman · 🚜 driver · 🔨 worker</text>")
rep(T, "👤 you · 🤵 Chief of Staff · ✍️ spec-writer · 👷 Foreman", "👤 you · 🤵 Chief of Staff · ✍️ spec-writer · 🔥 Griller (optional) · 👷 Foreman")
for f in (S, T):
    rep(f, "PLAN · 🤵 Chief of Staff, with you", "PLAN · 🤵 Chief of Staff, or a 🔥 Griller (optional), with you")
rep(S, ">🤵 with 👤 you<", ">🤵 or 🔥 with 👤 you<")
rep(T, "\n🤵 with 👤 you\n", "\n🤵 or 🔥 with 👤 you\n")
print("ok")
