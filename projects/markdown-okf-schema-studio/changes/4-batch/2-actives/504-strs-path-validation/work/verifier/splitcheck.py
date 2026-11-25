"""For each split group, lines of the base files missing from the head files, and lines new at head."""
import collections
import re
import subprocess
import sys

REPO, BASE, HEAD = sys.argv[1:4]
GROUPS = [
    ["test/core/preview/previewStyles.test.ts", "test/core/preview/previewStylesGutter.test.ts"],
    ["test/integration/previewEditing.test.ts", "test/integration/previewEditingSchemaSteps.ts"],
    ["test/page/modules/editActions.test.ts", "test/page/modules/editActionsColour.test.ts"],
    ["test/page/runtimeTableCellEditor.test.ts", "test/page/runtimeTableCellEditorReveal.test.ts"],
    ["test/visual/capture.py", "test/visual/capture_cell_editor_checks.py", "test/visual/capture_comment_checks.py",
     "test/visual/capture_edit_checks.py", "test/visual/capture_first_gap_checks.py"],
    ["test/visual/scenarioDefinitions2.ts", "test/visual/scenarioDefinitions3.ts", "test/visual/scenarios.ts"],
]
MARK = re.compile(r"@(tests_req|accepts_req|implements_req)\b")


def lines(rev, path):
    p = subprocess.run(["git", "-C", REPO, "show", f"{rev}:{path}"], capture_output=True)
    if p.returncode:
        return []
    out = []
    for line in p.stdout.decode("utf-8", "replace").replace("\r\n", "\n").split("\n"):
        s = line.strip()
        if s and not MARK.search(s):
            out.append(s)
    return out


for group in GROUPS:
    old = collections.Counter(l for f in group for l in lines(BASE, f))
    new = collections.Counter(l for f in group for l in lines(HEAD, f))
    gone, added = old - new, new - old
    head_all = set(new)
    count = lambda c, pat: sum(n for l, n in c.items() if re.search(pat, l))
    pat = r"\bassert\b|^assert|expect\(|^test\(|^it\(|^(async )?def check_|^id: |\bid: \""
    print("==", group[0].rsplit("/", 1)[1])
    print("   assert/test/case lines base", count(old, pat), "head", count(new, pat))
    print("   lines gone", sum(gone.values()), "new", sum(added.values()))
    for l, n in sorted(gone.items()):
        print("   -", n, l[:150])
