import re, sys
import gen
from gen import *


def classify(f, a, b, t):
    sg = seg_of(f, a)
    if sg is None:
        return None
    trig, cand, dk = sg
    # protecting
    for pf, rx, k2, home, chk in OVR:
        if pf == f and re.search(rx, t):
            return trig, k2, home, chk, 1.0
    for pf, (pa, pb), rx, home, chk in PROT:
        if pf == f and pa <= a <= pb and home != "none" and re.search(rx, t, re.I):
            return trig, "a", home, chk, 1.0
    if RX_D_HOST.search(t) and re.search(r"unproved|skip|does not run|where P10", t):
        return trig, "d", "host row (Copilot reference: `hosts/copilot.md`)", "none (host row owns it)", 1.0
    if RX_D_UNPROVED.search(t) and re.search(r"GitLab|glab|MR", t):
        best = best_topic(t, [c for c in cand if not c.startswith("@")] or ["stack"])
        return trig, "d", f"topic {best[0]} (the word \"unproved\" kept for GitLab only)", f"help {best[0]}", best[1]
    if RX_D_UNPROVED.search(t):
        return trig, "d", "host row (unproved bookkeeping dropped from the topic)", "none (host row owns it)", 1.0
    if RX_F.search(t):
        return trig, "f", "duplicate: the card's pointers and `help --for foreman`", "none (duplicate)", 1.0
    for pf, rx in INFER:
        if pf == f and re.search(rx, t):
            return trig, "b", "inferable", "none (a capable model infers it; no protecting rule)", 1.0
    if dk in ("b", "f") and cand == ["@inferable"]:
        return trig, dk, "inferable" if dk == "b" else "duplicate", "none (no protecting rule)", 1.0
    # topic or card home
    best = best_topic(t, cand)
    name, sc = best
    kind = dk
    if name == "@judge":
        home, chk = "next: the `judge` line (words the ask); " + C("own15"), "none (`judge` prints it)"
    elif name == "@refusal":
        home, chk = REF_FR + "; floor 9", "none (refusals)"
    elif name == "@help":
        home, chk = "`help --for foreman` and `startup-manifest.json`; card foreman.md:37", "help --for foreman"
    elif name == "@inferable":
        home, chk = "inferable", "none"
    elif name == "@card":
        ln = best_card_line(t)
        home = f"card foreman.md:{ln}"
        tk = [x for x in re.findall(r"`([^`]+)`", t) if x in CARD]
        chk = f"grep -c '{tk[0]}' foreman.md" if tk else "none (worded in the card)"
    else:
        home, chk = f"topic {name}", f"help {name}"
    return trig, kind, home, chk, sc


def best_topic(t, cand):
    best = (cand[0], -1.0)
    for c in cand:
        if c == "@card":
            s = score(t, CARD)
        elif c.startswith("@"):
            s = 0.5
        else:
            s = score(t, topic_text(c))
        if s > best[1]:
            best = (c, s)
    return best


def best_card_line(t):
    ls = CARD.split("\n")
    bl, bs = 3, -1
    for i, l in enumerate(ls, 1):
        if not l.strip():
            continue
        s = score(t, l)
        if s > bs:
            bl, bs = i, s
    return bl


def esc(s):
    return s.replace("|", "\\|")


def short(t, n=230):
    t = re.sub(r"\s+", " ", t)
    return t if len(t) <= n else t[: n - 1].rstrip() + "…"


if __name__ == "__main__":
    rows = build()
    low, un = [], []
    cnt = {}
    for f, a, b, t in rows:
        r = classify(f, a, b, t)
        if r is None:
            un.append((f, a, b, t[:80]))
            continue
        trig, kind, home, chk, sc = r
        cnt[kind] = cnt.get(kind, 0) + 1
        if kind in ("e", "c") and sc < 0.34:
            low.append((f, a, b, sc, home, t[:110]))
    print(cnt, len(rows))
    print("UNASSIGNED", len(un))
    for x in un:
        print(x)
    print("LOW", len(low))
    for x in low:
        print(f"{x[0]}:{x[1]}-{x[2]} {x[3]:.2f} {x[4]} | {x[5]}")
