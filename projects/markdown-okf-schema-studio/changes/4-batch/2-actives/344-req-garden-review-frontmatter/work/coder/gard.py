"""CR-344 round 1 scaffolding: helpers to edit StRS authored sections."""
import pathlib, re

ROOT = pathlib.Path("requirements/tiers")
LINKS = "<!-- okf:links:start -->"


def strs_path(i):
    scope = {"FMEDIT": "frontmatter-editing", "FMSCHEMA": "frontmatter-schema", "REVIEW": "review-annotations"}[i.split("-")[0]]
    return ROOT / "strs" / scope / f"StRS-MDOKFSTUDIO-{i}.md"


def swrs_path(i):
    return next((ROOT / "swrs").glob(f"*/SwRS-MDOKFSTUDIO-{i}.md"))


def read(p):
    t = p.read_bytes().decode("utf-8")
    assert "\r" not in t, p
    return t


def write(p, t):
    p.write_bytes(t.encode("utf-8"))


def sections(t):
    """Return (head, rationale, diagram, main, tail) as strings; each section keeps its heading."""
    li = t.find(LINKS)
    tail = t[li:] if li >= 0 else ""
    body = t[:li] if li >= 0 else t
    def cut(h, s):
        i = s.find(h)
        return i
    ri = body.index("### Rationale and constraints")
    head = body[:ri]
    rest = body[ri:]
    di = rest.find("### Use case diagram")
    mi = rest.find("### Main paths")
    if di >= 0 and (mi < 0 or di < mi):
        rat = rest[:di]
        dia = rest[di:mi] if mi >= 0 else rest[di:]
    else:
        rat = rest[:mi] if mi >= 0 else rest
        dia = ""
    main = rest[mi:] if mi >= 0 else ""
    return head, rat, dia, main, tail


def block(s):
    return s.strip("\n") + "\n\n"


def edit_strs(i, rationale=None, diagram=None, main=None, main_sub=None, head_sub=None):
    p = strs_path(i)
    t = read(p)
    head, rat, dia, mn, tail = sections(t)
    if head_sub:
        for a, b in head_sub:
            assert a in head, (i, a)
            head = head.replace(a, b)
    if rationale is not None:
        rat = "### Rationale and constraints\n\n" + rationale.strip("\n") + "\n\n"
    else:
        rat = block(rat)
    if diagram is not None:
        dia = "### Use case diagram\n\n```mermaid\n" + diagram.strip("\n") + "\n```\n\n"
    else:
        dia = block(dia) if dia.strip() else ""
    if main is not None:
        mn = main.strip("\n") + "\n\n"
    else:
        mn = block(mn) if mn.strip() else ""
    if main_sub:
        for a, b in main_sub:
            assert a in mn, (i, a)
            mn = mn.replace(a, b)
    write(p, head + rat + dia + mn + tail)


def get_list(t, key):
    m = re.search(r"^" + key + r":(?: \[\])?\n((?:- .*\n)*)", t, re.M)
    if not m:
        return None, None
    items = [l[2:] for l in m.group(1).splitlines()]
    return m, items


def set_list(i, key, remove=(), add=(), after=None, swrs=True):
    """Edit a frontmatter list of an SwRS (or StRS if swrs False)."""
    p = swrs_path(i) if swrs else strs_path(i)
    t = read(p)
    m, items = get_list(t, key)
    if m is None:
        assert add, (i, key)
        items = []
        # insert after the `after` key list (or derives_from)
        am, _ = get_list(t, after or "derives_from")
        assert am, (i, after)
        pos = am.end()
    else:
        pos = None
    for r in remove:
        assert r in items, (i, key, r)
        items.remove(r)
    for a in add:
        if a not in items:
            items.append(a)
    new = (key + ":\n" + "".join("- %s\n" % x for x in items)) if items else (key + ": []\n")
    if m is not None:
        t = t[:m.start()] + new + t[m.end():]
    else:
        t = t[:pos] + new + t[pos:]
    write(p, t)
