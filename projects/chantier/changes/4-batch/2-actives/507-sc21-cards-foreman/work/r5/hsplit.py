"""Sentence units of the host-and-shared sources, read from git at the base (HEAD).

A unit is one sentence (a full stop outside a code span; over 190 characters cut again at a
top-level semicolon, as work/coder/split.py), one table row, or one fenced block. Headings and
blank lines give no unit; the nearest heading is the unit's trigger.
"""

import json
import re
import subprocess

WT = "C:/Users/gaeta/Projets/chantier.worktrees/batch-31-CR-507"
REFS = "skills/chantier/references/"

SOURCES = [
    "concepts.md", "pr-template.md", "release-template.md", "status-layout.md", "routing.md",
    "init.md", "review-step.md", "sync-checkout.md", "forges/github.md", "forges/gitlab.md",
    "hosts/claude-code.md", "hosts/copilot.md", "startup-core.md", "role-core.md",
    "host-core-claude-code.md", "host-core-copilot.md", "reload-rules.md",
]


def base_text(path: str) -> str:
    run = subprocess.run(["git", "-C", WT, "show", f"HEAD:{path}"], capture_output=True, check=True)
    return run.stdout.decode("utf-8")


def split_sentences(buf):
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
    cuts = [0] + [m.end() for m in re.finditer(r"[.!?](?=\s+(?:[A-Z`\[*(\"<]|\d+\.))", ms)]
    cuts.append(len(s))

    def lnof(p):
        r = pos[0][1]
        for st, ln in pos:
            if st <= p:
                r = ln
        return r

    spans = []
    for a, b in zip(cuts, cuts[1:]):
        if b - a > 190:
            depth, last = 0, a
            for i in range(a, b):
                c = ms[i]
                if c in "([":
                    depth += 1
                elif c in ")]":
                    depth = max(0, depth - 1)
                elif c == ";" and depth == 0 and i + 1 < b and ms[i + 1] == " " and i - last > 50:
                    spans.append((last, i + 1))
                    last = i + 2
            spans.append((last, b))
        else:
            spans.append((a, b))
    for a, b in spans:
        seg = s[a:b].strip()
        if not seg:
            continue
        aa = a
        while aa < b and s[aa] == " ":
            aa += 1
        yield lnof(aa), lnof(max(aa, b - 1)), seg


def units(name: str):
    """(first line, last line, text, trigger, form) of references/<name> at the base."""
    lines = base_text(REFS + name).split("\n")
    heading = name
    out, buf = [], []
    fence = None

    def flush():
        if buf:
            for a, b, t in split_sentences(buf):
                out.append((a, b, t, heading, "text"))
            buf.clear()

    for i, raw in enumerate(lines, 1):
        t = raw.rstrip()
        st = t.lstrip()
        if fence is not None:
            if st.startswith("```"):
                out.append((fence[0], i, "```" + " / ".join(fence[1]) + "```", heading, "block"))
                fence = None
            else:
                fence[1].append(st)
            continue
        if st.startswith("```"):
            flush()
            fence = (i, [])
            continue
        if t.startswith("#") or not st:
            flush()
            if t.startswith("#"):
                heading = t.lstrip("# ").strip()
            continue
        if st.startswith("|"):
            flush()
            if not re.fullmatch(r"[|\s:-]+", st):
                out.append((i, i, st, heading, "row"))
            continue
        if re.match(r"^(- |\d+\. )", st):
            flush()
            st = re.sub(r"^(- |\d+\. )", "", st)
        buf.append((i, st))
    flush()
    return out


if __name__ == "__main__":
    total = 0
    for name in SOURCES:
        u = units(name)
        total += len(u)
        print(len(u), name)
    manifest = json.loads(base_text(REFS + "startup-manifest.json"))
    print(total, "units;", "manifest keys:", list(manifest))
    print(json.dumps(manifest, indent=1)[:6000])
