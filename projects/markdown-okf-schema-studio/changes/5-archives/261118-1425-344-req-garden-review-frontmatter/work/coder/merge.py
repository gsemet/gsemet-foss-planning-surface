"""CR-344 round 1: merge an absorbed SwRS into its survivor (text only; supersede is run separately)."""
import json
import re
import sys

sys.path.insert(0, sys.path[0])
from gard import *  # noqa: E402,F401

PFX = "SwRS-MDOKFSTUDIO-"


def fm_get(t, key):
    m = re.search(r"^" + key + r":[ ]?(.*(?:\n  .*)*)", t, re.M)
    raw = m.group(0)[len(key) + 1:].strip()
    # unfold continuation lines
    raw = re.sub(r"\n\s+", " ", raw)
    if raw.startswith('"') and raw.endswith('"'):
        raw = json.loads(raw)
    elif raw.startswith("'") and raw.endswith("'"):
        raw = raw[1:-1].replace("''", "'")
    return raw


def fm_set(t, key, value):
    m = re.search(r"^" + key + r":.*(?:\n  .*)*", t, re.M)
    assert m, key
    return t[:m.start()] + key + ": " + json.dumps(value, ensure_ascii=False) + t[m.end():]


def split_links(t):
    li = t.find(LINKS)
    return (t[:li], t[li:]) if li >= 0 else (t, "")


def split_sections(body):
    """Return list of (heading_line or None, text including the heading line)."""
    parts = re.split(r"(?m)^(?=### )", body)
    out = []
    for p in parts:
        if p.startswith("### "):
            out.append((p.split("\n", 1)[0], p))
        else:
            out.append((None, p))
    return out


def set_head(t, title=None, desc=None):
    old_title = fm_get(t, "title")
    old_desc = fm_get(t, "description")
    if title is not None:
        t = fm_set(t, "title", title)
        t = t.replace("\n## " + old_title + "\n", "\n## " + title + "\n", 1)
    if desc is not None:
        t = fm_set(t, "description", desc)
        t = t.replace("### Normative behavior\n\n" + old_desc + "\n", "### Normative behavior\n\n" + desc + "\n", 1)
    return t


def merge(surv, absorbed, title=None, desc=None, suffix=None, scen=None, rename=None, drop_notes=False):
    """absorbed: SwRS short ID (e.g. 'REVIEW-069'). scen: optional manual text of scenarios to add;
    when None, every '### Scenario' section of the absorbed is copied (renamed by `rename`)."""
    rename = rename or {}
    ps, pa = swrs_path(surv), swrs_path(absorbed)
    ts, ta = read(ps), read(pa)
    body_s, tail_s = split_links(ts)
    body_a, _ = split_links(ta)
    old_desc = fm_get(body_s, "description")
    if suffix is not None:
        assert desc is None
        desc = old_desc.rstrip(".") + suffix
    body_s = set_head(body_s, title, desc)
    secs_a = split_sections(body_a)
    add_scen = ""
    notes = ""
    known = ""
    for h, txt in secs_a:
        if h is None:
            continue
        if h.startswith("### Scenario"):
            if scen is None:
                new = txt
                for a, b in rename.items():
                    new = new.replace(a, b)
                add_scen += new.rstrip("\n") + "\n\n"
        elif h == "### Verification notes":
            notes = txt.split("\n", 1)[1].strip("\n")
        elif h == "### Known issues":
            known = txt.split("\n", 1)[1].strip("\n")
    if scen is not None:
        add_scen = scen.strip("\n") + "\n\n"
    for a, b in rename.items():
        notes = notes.replace(a, b).replace(a[0].lower() + a[1:], b[0].lower() + b[1:])
    # insert scenarios before the first of these headings
    pos = None
    for h in ("### Known issues", "### Related requirements", "### Verification notes"):
        k = body_s.find("\n" + h + "\n")
        if k >= 0 and (pos is None or k < pos):
            pos = k + 1
    assert pos is not None, surv
    body_s = body_s[:pos] + add_scen + body_s[pos:]
    # known issues
    if known:
        k = body_s.find("\n### Known issues\n")
        if k >= 0:
            e = body_s.find("\n### ", k + 5)
            body_s = body_s[:e].rstrip("\n") + "\n" + known + "\n\n" + body_s[e + 1:]
        else:
            k = body_s.find("\n### Related requirements\n")
            if k < 0:
                k = body_s.find("\n### Verification notes\n")
            body_s = body_s[:k + 1] + "### Known issues\n\n" + known + "\n\n" + body_s[k + 1:]
    # notes
    if notes and not drop_notes:
        k = body_s.find("### Verification notes")
        assert k >= 0, surv
        body_s = body_s.rstrip("\n") + "\n" + notes + "\n\n"
    # drop Related lines naming the absorbed
    aid = PFX + absorbed
    body_s = re.sub(r"(?m)^- " + re.escape(aid) + r"\b.*\n", "", body_s)
    ts = body_s + tail_s
    write(ps, ts)
    # depends_on
    m, deps = get_list(ta, "depends_on")
    if deps:
        _, cur = get_list(read(ps), "depends_on")
        add = [d for d in deps if d != PFX + surv and d != aid and d not in (cur or [])]
        if add:
            set_list(surv, "depends_on", add=add)


def refs_fix(absorbed_to_survivor):
    """Rewrite lists/lines naming an absorbed ID in every other authored requirement file."""
    for p in list(ROOT.glob("swrs/*/SwRS-*.md")) + list(ROOT.glob("strs/*/StRS-*.md")):
        t = read(p)
        body, tail = split_links(t)
        # frontmatter lists
        changed = False
        for a, s in absorbed_to_survivor.items():
            aid, sid = PFX + a, PFX + s
            if aid not in body or p.name == "SwRS-MDOKFSTUDIO-%s.md" % a:
                continue
            this = p.name[:-3]
            # drop Related-requirements lines when the survivor is already named or is this file
            lines = body.split("\n")
            out = []
            for ln in lines:
                if aid in ln and ln.startswith("- " + aid):
                    if sid in body or this == sid:
                        changed = True
                        continue
                if aid in ln and ln.startswith("- ") and ln.strip() == "- " + aid:
                    # list item (depends_on / relates_to)
                    if sid in body or this == sid:
                        changed = True
                        continue
                out.append(ln)
            body = "\n".join(out)
            if aid in body:
                body = body.replace(aid, sid)
                changed = True
        if changed:
            write(p, body + tail)
            print("refs fixed", p.name)
