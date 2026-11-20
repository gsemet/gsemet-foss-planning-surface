import io
P = "SwRS-MDOKFSTUDIO-PALETTE-"
# (file, line number of existing marker, new id, kind)
jobs = [
 ("src/page/modules/inlineEditActions.ts", 10, "276", "implements"),
 ("src/page/modules/blockEditActions.ts", 36, "277", "implements"),
 ("src/page/modules/blockEditActions.ts", 566, "278", "implements"),
 ("src/session/features/scrollSync.ts", 146, "279", "implements"),
 ("src/session/features/blockEdits.ts", 346, "279", "implements"),
 ("src/core/palette/paletteIcons.ts", 1, "280", "implements"),
 ("test/page/modules/editActions.test.ts", 12, "276", "tests"),
 ("test/page/modules/editActions.test.ts", 14, "277", "tests"),
 ("test/page/modules/editActions.test.ts", 194, "278", "tests"),
 ("test/session/toolbarReq.requirements.test.ts", 679, "279", "tests"),
 ("test/page/runtimeEditPalette.test.ts", 86, "280", "tests"),
]
by = {}
for f, ln, i, k in jobs:
    by.setdefault(f, []).append((ln, i, k))
for f, items in by.items():
    raw = open(f, "rb").read().decode("utf-8")
    crlf = "\r\n" in raw
    lines = raw.split("\r\n" if crlf else "\n")
    for ln, i, k in sorted(items, reverse=True):
        old = lines[ln - 1]
        assert f"@{k}_req" in old, (f, ln, old)
        indent = old[: len(old) - len(old.lstrip())]
        lines.insert(ln, f"{indent}// @{k}_req {P}{i}")
    open(f, "wb").write(("\r\n" if crlf else "\n").join(lines).encode("utf-8"))
