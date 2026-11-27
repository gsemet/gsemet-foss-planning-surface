"""(file, SwRS id) pairs that had a test marker at base and have none at head, split files grouped.

usage: uv run --no-project python -I lastmarker.py <worktree> <base> <head>
"""
import collections
import re
import subprocess
import sys

REPO, BASE, HEAD = sys.argv[1:4]
MARK = re.compile(r"^\s*(?:(?:#|//|/\*|\*|<!--)\s*)?@(tests_req|accepts_req)\s+((?:SwRS|StRS)-[A-Za-z0-9]+-[A-Z]+-\d+)")
GROUPS = [
    ["test/core/preview/previewStyles.test.ts", "test/core/preview/previewStylesGutter.test.ts"],
    ["test/integration/previewEditing.test.ts", "test/integration/previewEditingSchemaSteps.ts"],
    ["test/page/modules/editActions.test.ts", "test/page/modules/editActionsColour.test.ts"],
    ["test/page/runtimeTableCellEditor.test.ts", "test/page/runtimeTableCellEditorReveal.test.ts"],
    ["test/visual/capture.py", "test/visual/capture_cell_editor_checks.py", "test/visual/capture_comment_checks.py",
     "test/visual/capture_edit_checks.py", "test/visual/capture_first_gap_checks.py"],
    ["test/visual/scenarioDefinitions2.ts", "test/visual/scenarioDefinitions3.ts", "test/visual/scenarios.ts"],
]
ALIAS = {f: g[0] for g in GROUPS for f in g}


def pairs(rev):
    p = subprocess.run(["git", "-C", REPO, "grep", "-n", "-I", "-E", "@(tests_req|accepts_req) ", rev, "--", "test", "src", "sphinx", "scripts"],
                       capture_output=True)
    out = collections.defaultdict(set)
    for line in p.stdout.decode("utf-8", "replace").split("\n"):
        parts = line.split(":", 3)
        if len(parts) < 4:
            continue
        m = MARK.match(parts[3])
        if m:
            out[(ALIAS.get(parts[1], parts[1]), m.group(2))].add(m.group(1))
    return out


old, new = pairs(BASE), pairs(HEAD)
gone = sorted(k for k in old if k not in new and k[1].startswith("SwRS"))
print("base (file, SwRS) pairs", sum(1 for k in old if k[1].startswith("SwRS")), "gone at head", len(gone))
by_dir = collections.defaultdict(list)
for f, i in gone:
    by_dir["/".join(f.split("/")[:2])].append((f, i))
for d, items in sorted(by_dir.items()):
    ids = sorted({i.split("-", 2)[2] for _, i in items})
    print("==", d, "pairs", len(items), "distinct ids", len(ids))
    print("  ", " ".join(ids))
integ = [(f, i) for f, i in gone if f.startswith("test/integration/")]
for f, i in integ:
    print(f, i.split("-", 2)[2])
