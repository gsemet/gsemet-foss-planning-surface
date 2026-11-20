import re, pathlib
P = "SwRS-MDOKFSTUDIO-"
S = "StRS-MDOKFSTUDIO-"
def full(i):
    if i.startswith(("SwRS-","StRS-")): return i
    return (S if i.startswith("S:") else P) + i.replace("S:","")
def read(f):
    b = pathlib.Path(f).read_bytes().decode("utf-8")
    crlf = "\r\n" in b
    return b.replace("\r\n","\n"), crlf
def write(f, text, crlf):
    if crlf: text = text.replace("\n","\r\n")
    pathlib.Path(f).write_bytes(text.encode("utf-8"))
def add(f, table, kind="@tests_req", nth=None):
    """table: {line-substring: [ids]} insert marker lines above the unique line containing the substring (indented like it)."""
    text, crlf = read(f)
    lines = text.split("\n")
    for sub, ids in table.items():
        idx = [i for i,l in enumerate(lines) if sub in l]
        if nth is not None and isinstance(nth, dict) and sub in nth: idx = [idx[nth[sub]]]
        assert len(idx)==1, (f, sub, len(idx))
        i = idx[0]
        indent = re.match(r'\s*', lines[i]).group(0)
        # existing markers in the contiguous comment lines above
        j = i-1
        while j>=0 and re.match(r'\s*(//|\*|/\*)', lines[j]): j-=1
        existing = "\n".join(lines[j+1:i])
        new = [f"{indent}// {kind} {full(x)}" for x in ids if full(x) not in existing]
        lines[i:i] = new
    write(f, "\n".join(lines), crlf)
def remove_lines(f, first, last):
    text, crlf = read(f)
    lines = text.split("\n")
    del lines[first-1:last]
    write(f, "\n".join(lines), crlf)
def replace(f, old, new, count=1):
    text, crlf = read(f)
    assert text.count(old)==count, (f, old[:50], text.count(old))
    write(f, text.replace(old,new), crlf)
def add_at(f, table, kind="@tests_req", drop=None):
    """table {lineno(1-based, current file): [ids]}; adds marker lines directly above that line, skipping ids already in the comment run above.
    drop {lineno: [ids]} removes those marker lines from the run above first."""
    text, crlf = read(f)
    lines = text.split("\n")
    for ln in sorted(set(table) | set(drop or {}), reverse=True):
        i = ln - 1
        indent = re.match(r'\s*', lines[i]).group(0)
        j = i - 1
        while j >= 0 and re.match(r'\s*(//|\*|/\*)', lines[j]): j -= 1
        run = lines[j+1:i]
        for d in (drop or {}).get(ln, []):
            run = [l for l in run if not l.rstrip().endswith(full(d))]
        have = "\n".join(run)
        new = [f"{indent}// {kind} {full(x)}" for x in table.get(ln, []) if full(x) not in have]
        lines[j+1:i] = run + new
    write(f, "\n".join(lines), crlf)
