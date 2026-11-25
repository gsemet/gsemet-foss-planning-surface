import re, sys, json, pathlib, subprocess
sys.path.insert(0, "C:/Users/gaeta/Projets/gsemet-foss-planning-surface/projects/chantier/changes/4-batch/2-actives/507-sc21-cards-foreman/work/coder")
import split

WT = pathlib.Path("C:/Users/gaeta/Projets/chantier.worktrees/batch-31-CR-507/skills/chantier")
CN = WT / "cards-next"
REF = WT / "references"
EVD = pathlib.Path("C:/Users/gaeta/Projets/gsemet-foss-planning-surface/projects/chantier/changes/4-batch/2-actives/507-sc21-cards-foreman/evidence")

CHIEF_FILES = ["chief-of-staff", "chief-of-staff-any", "chief-of-staff-batch-start", "chief-of-staff-steering",
               "chief-of-staff-merge", "chief-of-staff-batch-end", "chief-of-staff-direct", "chief-of-staff-grill",
               "chief-of-staff-release", "chief-of-staff-writer", "session-start", "session-start-chief-of-staff",
               "titles", "ticket-summary-example"]
GRILLER_FILES = ["griller", "session-start-griller"]


def tok(t):
    t = t.lower()
    w = re.findall(r"[a-z][a-z0-9-]{3,}", t)
    return w


def sc(t, text_w, text_b):
    w = tok(t)
    if not w:
        return 0.0
    s1 = sum(1 for x in set(w) if x in text_w) / len(set(w))
    bg = list(zip(w, w[1:]))
    s2 = (sum(1 for x in set(bg) if x in text_b) / len(set(bg))) if bg else s1
    return 0.6 * s1 + 0.4 * s2


def mk(text):
    w = tok(text)
    return set(w), set(zip(w, w[1:]))


# ---- the new texts
topics = json.load(open(CN / "topics.json", encoding="utf-8"))["topics"]
tp_text = {}
for n, r in topics.items():
    txt = ""
    for rd in r["readings"]:
        f = CN / rd.split("#")[0]
        if f.exists() and n == f.stem.rsplit("-p", 1)[0] or (f.exists() and f.stem == n):
            txt += open(f, encoding="utf-8").read() + "\n"
        elif f.exists():
            # a part-list row: parts have their own file; skip
            txt += open(f, encoding="utf-8").read() + "\n"
    tp_text[n] = txt
tp_idx = {n: mk(t) for n, t in tp_text.items()}


def lines_of(p):
    return open(p, encoding="utf-8").read().split("\n")


FLOOR_L = lines_of(CN / "floor.md")


def card_info(name):
    L = lines_of(CN / name)
    return L, [mk(l) for l in L]


PROT = re.compile(r"\b(never|must not|do not|does not|not without|only (?:on|with|when|after)|user's (?:word|yes|answer|go)|"
                  r"refus|force|merge[sd]?\b|irreversible|delet|discard|username|secret|kill|stop(?:s|ped)? (?:a|the|it)|"
                  r"settings\.json|publish|post(?:s|ed)? (?:it|a|the)|approv|grant|asks? (?:first|before)|without (?:the |a )?(?:user|yes|ask))", re.I)

STRONG = re.compile(r"\b(never|not without|only on the user|only with the user|user's (?:own )?(?:word|yes|answer)|only after the user|must not|refus\w*|no guess|without the user)\b", re.I)
# (regex on the sentence, home, phrase to find in the home line)
THEMES_C = [
 (r"settings\.json|allow rule|P10", "card chief-of-staff.md:13", "settings.json"),
 (r"publication done|publish|announcement|irreversible|\bauto\b|grant|approv", "card chief-of-staff.md:15; floor 6", "publication done"),
 (r"close --yes|--stopped|worktree|branch(?:es)? (?:and|or)|delete|discard|abandon|restore|remove", "card chief-of-staff.md:16; floor 5", "close --yes"),
 (r"stop(?:s|ping|ped)?\b.*\b(process|board|watcher|holder|session|agent)|kill|by name|pattern", "card chief-of-staff.md:14; floor 10", "by name or pattern"),
 (r"\bgh pr (?:ready|edit)|chain(?:ed)? ", "card chief-of-staff.md:8-9", "gh pr ready"),
 (r"rebase", "card chief-of-staff.md:7", "rebase"),
 (r"not chantier's|default branch|non-CR|is not a CR|foreign", "card chief-of-staff.md:17; floor 2", "default branch"),
 (r"force|lease|\bpush(?:es|ed)?\b", "card chief-of-staff.md:6, 10; floor 2", "force-with-lease"),
 (r"\bmerge[sd]?\b|mergeable", "floor 1", "none (floor)"),
 (r"tracker|issue|ticket|comment|Jira|demo\.html", "card chief-of-staff.md:24", "tracker issue"),
 (r"writer|commit the plan|pull or push the surface|surface's checkout", "card chief-of-staff.md:25", "writer"),
 (r"priority|label|group", "card chief-of-staff.md:26", "priority"),
 (r"seat|another live session|another session", "card chief-of-staff.md:20", "seat"),
 (r"another project|of the surface|clone", "card chief-of-staff.md:21", "another project"),
 (r"message a Driver|Driver's|transcript|implement|look-alike agent|refused start|prompt", "card chief-of-staff.md:22", "message a Driver"),
 (r"batch\.json|events\.jsonl|STATUS", "card chief-of-staff.md:23", "events.jsonl"),
 (r"delivery|time the batch|prediction", "card chief-of-staff.md:28", "delivery time"),
 (r"fallback|workaround|look-alike|another tool|another way|cannot run", "floor 3, 4", "none (floor)"),
 (r"username|home folder|image", "floor 8", "none (floor)"),
 (r"refus", "floor 9; card chief-of-staff.md:10, 32", "refusal"),
 (r"user starts|start (?:a|any) (?:CR|work|backlog)|never start", "floor 7", "none (floor)"),
 (r"past fact|unknown|source", "card chief-of-staff.md:31", "source"),
 (r"preflight", "card chief-of-staff.md:29", "preflight"),
]
THEMES_C = [(re.compile(a, re.I), b, c) for a, b, c in THEMES_C]
PTR = re.compile(r"^(see|more:|read|details|the rest|for the|on that)\b", re.I)
HOST = re.compile(r"copilot|claude code|host", re.I)
UNPR = re.compile(r"unproved|not proved|trial", re.I)


def heading_map(fname):
    m = {}
    cur = fname
    for i, l in enumerate(lines_of(REF / (fname + ".md")), 1):
        if l.startswith("#"):
            cur = l.lstrip("# ").strip()
        m[i] = cur
    return m


def parent(n):
    return n


def walk(files, role, card, skip=None):
    CL, CI = card_info(card)
    rows = []
    for f in files:
        hm = heading_map(f)
        for a, b, t in split.sentences(f):
            if skip and skip(f, a):
                continue
            rows.append((f, a, b, t, hm.get(a, f)))
    out = []
    for f, a, b, t, trig in rows:
        w, bg = mk(t)
        # card
        bc, bcn = 0.0, 0
        for i, (cw, cb) in enumerate(CI, 1):
            if not CL[i - 1].strip():
                continue
            s = sc(t, cw, cb)
            if s > bc:
                bc, bcn = s, i
        bf, bfn = 0.0, 0
        for i, l in enumerate(FLOOR_L, 1):
            if not l.strip():
                continue
            s = sc(t, *mk(l))
            if s > bf:
                bf, bfn = s, i
        bt, btn = 0.0, ""
        for n, (tw, tb) in tp_idx.items():
            s = sc(t, tw, tb)
            roles = topics[n]["roles"]
            if role in roles:
                s += 0.02
            if s > bt:
                bt, btn = s, n
        prot = bool(PROT.search(t))
        kind, home, chk, why = "e", "", "", ""
        if PTR.search(t.strip()) and len(t) < 160:
            kind, home, chk, why = "f", "duplicate: the card's pointers and `help`", "none (duplicate)", "pointer"
        elif UNPR.search(t) and HOST.search(t) and re.search(r"unproved|not proved", t):
            if re.search(r"GitLab|glab|MR", t):
                kind, home, chk = "d", f"topic {btn} (the word \"unproved\" kept for GitLab only)", f"help {btn}"
            else:
                kind, home, chk = "d", "host row (unproved bookkeeping dropped from the topic)", "none (host row owns it)"
        elif role == "chief-of-staff" and STRONG.search(t) and max(bc, bf) >= 0.4 and max(bc, bf) >= bt - 0.1:
            if bf >= bc:
                kind, home, chk = "a", f"floor {FLOOR_L[bfn-1].split('.')[0]}", "none (floor)"
            else:
                ph = (re.findall(r"`([^`]{4,30})`", CL[bcn - 1]) or [re.sub(r"[^A-Za-z ]", "", CL[bcn - 1])[:24].strip()])[0]
                kind, home, chk = "a", f"card {card}:{bcn}", f"grep -c '{ph}' {card}"
        elif role == "chief-of-staff" and STRONG.search(t) and bt >= 0.4 and any(rx.search(t) for rx, _, _ in THEMES_C):
            rx, h, ph = next((rx, h, ph) for rx, h, ph in THEMES_C if rx.search(t))
            kind, home, chk = "e", f"topic {btn}; the rule it applies: {h}", f"help {btn}"
        elif prot and max(bc, bf) >= 0.5 and max(bc, bf) >= bt - 0.05:
            if bf >= bc:
                kind, home, chk = "a", f"floor {FLOOR_L[bfn-1].split('.')[0]}", "none (floor)"
            else:
                ph = (re.findall(r"`([^`]{4,30})`", CL[bcn - 1]) or [re.sub(r"[^A-Za-z ]", "", CL[bcn - 1])[:24].strip()])[0]
                kind, home, chk = "a", f"card {card}:{bcn}", f"grep -c '{ph}' {card}"
        elif bt >= 0.4:
            kind, home, chk = "e", f"topic {btn}", f"help {btn}"
        elif max(bc, bf) >= 0.4:
            if bf > bc:
                kind, home, chk = "e", f"floor {FLOOR_L[bfn-1].split('.')[0]}", "none (floor)"
            else:
                kind, home, chk = "e", f"card {card}:{bcn}", "none (worded in the card)"
        else:
            kind, home, chk = "b", "inferable", "none (a capable model infers it; no protecting rule)"
            if prot:
                kind = "?"
        out.append(dict(f=f, a=a, b=b, t=t, trig=trig, kind=kind, home=home, chk=chk, sb=round(bt, 2), sc=round(bc, 2), prot=prot))
    return out


if __name__ == "__main__":
    which = sys.argv[1]
    if which == "chief":
        res = walk(CHIEF_FILES, "chief-of-staff", "chief-of-staff.md")
    else:
        def skip(f, a):
            return f == "griller" and 102 <= a <= 136
        res = walk(GRILLER_FILES, "griller", "griller-skill.md", skip)
    from collections import Counter
    print(len(res), Counter(r["kind"] for r in res))
    json.dump(res, open(pathlib.Path(__file__).parent / f"rows-{which}.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    for r in res:
        if r["kind"] == "?":
            print(r["f"], r["a"], r["t"][:160])
