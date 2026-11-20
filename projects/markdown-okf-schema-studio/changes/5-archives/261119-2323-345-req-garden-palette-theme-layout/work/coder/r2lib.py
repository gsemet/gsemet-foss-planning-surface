import re, sys
ROOT = "C:/Users/gaeta/Projets/markdown-okf-schema-studio.worktrees/batch-06-CR-345/"
PFX = "SwRS-MDOKFSTUDIO-"

def rd(p):
    with open(ROOT + p, newline="", encoding="utf-8") as f:
        return f.read()

def wr(p, t):
    with open(ROOT + p, "w", newline="", encoding="utf-8") as f:
        f.write(t)

def eol(t):
    return "\r\n" if "\r\n" in t else "\n"

def mid(i):
    if i.startswith("StRS-") or i.startswith("SwRS-"):
        return i
    return PFX + i

def mark_before(p, anchor, ids, kind="implements", nth=1, comment="//", above_doc=True, contains=False):
    """Insert marker lines before the nth line whose stripped text starts with (or contains) anchor."""
    t = rd(p)
    e = eol(t)
    lines = t.split(e)
    count = 0
    for i, l in enumerate(lines):
        s = l.strip()
        if (anchor in s) if contains else s.startswith(anchor):
            count += 1
            if count == nth:
                at = i
                if above_doc and at > 0 and lines[at - 1].strip().endswith("*/"):
                    j = at - 1
                    while j >= 0 and not lines[j].strip().startswith("/**"):
                        j -= 1
                    if j >= 0:
                        at = j
                indent = re.match(r"\s*", lines[at]).group(0)
                new = [f"{indent}{comment} @{kind}_req {mid(x)}" for x in ids]
                lines[at:at] = new
                wr(p, e.join(lines))
                return
    raise SystemExit(f"anchor not found: {p}: {anchor!r} nth={nth}")

def drop_lines(p, ids, kind=None, lines_at=None):
    """Remove marker lines naming ids (all occurrences, or only at 1-based lines_at)."""
    t = rd(p)
    e = eol(t)
    lines = t.split(e)
    out = []
    for n, l in enumerate(lines, 1):
        m = re.search(r"@(implements|tests)_req\s+(\S+)", l)
        if m and m.group(2) in {mid(x) for x in ids} and (kind is None or m.group(1) == kind) and (lines_at is None or n in lines_at):
            continue
        out.append(l)
    wr(p, e.join(out))

def replace_id(p, old, new, lines_at=None):
    t = rd(p)
    e = eol(t)
    lines = t.split(e)
    for n, l in enumerate(lines, 1):
        if re.search(r"@(implements|tests)_req\s+" + re.escape(mid(old)) + r"\b", l) and (lines_at is None or n in lines_at):
            lines[n - 1] = l.replace(mid(old), mid(new))
    wr(p, e.join(lines))
