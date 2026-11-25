import re, json, os
W = "C:/Users/gaeta/Projets/chantier.worktrees/batch-31-CR-507/skills/chantier"
REF = W + "/references/"
CN = W + "/cards-next/"
FILES = ["foreman", "foreman-stack", "foreman-merge", "foreman-hold", "foreman-lost-driver",
         "foreman-conflict", "foreman-release", "foreman-refused", "foreman-pause"]


def sentences(fname):
    lines = open(REF + fname + ".md", encoding="utf-8").read().split("\n")
    out = []
    buf = []

    def flush():
        if not buf:
            return
        s = ""
        pos = []
        for ln, t in buf:
            if s:
                s += " "
            pos.append((len(s), ln))
            s += t.strip()
        mask = list(s)
        for m in re.finditer(r"`[^`]*`|\[[^\]]*\]\([^)]*\)|\*\*", s):
            for i in range(m.start(), m.end()):
                if mask[i] in ".;!?:":
                    mask[i] = "_"
        ms = "".join(mask)
        cuts = [0]
        for m in re.finditer(r"[.!?](?=\s+(?:[A-Z`\[*(\"<]|\d+\.))", ms):
            cuts.append(m.end())
        cuts.append(len(s))

        def lnof(p):
            r = pos[0][1]
            for st, ln in pos:
                if st <= p:
                    r = ln
            return r
        # long sentences split again at a top-level semicolon
        more = []
        for a, b in zip(cuts, cuts[1:]):
            if b - a > 190:
                depth = 0
                last = a
                for i in range(a, b):
                    c = ms[i]
                    if c in "([": depth += 1
                    elif c in ")]": depth = max(0, depth - 1)
                    elif c == ";" and depth == 0 and i + 1 < b and ms[i + 1] == " " and i - last > 50:
                        more.append((last, i + 1)); last = i + 2
                more.append((last, b))
            else:
                more.append((a, b))
        for a, b in more:
            seg = s[a:b].strip()
            if not seg:
                continue
            aa = a
            while aa < b and s[aa] == " ":
                aa += 1
            out.append((lnof(aa), lnof(max(aa, b - 1)), seg))
        buf.clear()
    for i, raw in enumerate(lines, 1):
        t = raw.rstrip()
        if t.startswith("#") or not t.strip():
            flush()
            continue
        st = t.lstrip()
        if re.match(r"^(- |\d+\. )", st):
            flush()
            st = re.sub(r"^(- |\d+\. )", "", st)
        buf.append((i, st))
    flush()
    return out


if __name__ == "__main__":
    tot = 0
    for f in FILES:
        s = sentences(f)
        tot += len(s)
        print(f, len(s))
    print(tot)
