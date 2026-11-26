"""Owner steps 5 and 6 and the other marker rules, one broken marker at a time on a scratch copy.

usage: uv run --no-project python -I ownersteps.py <worktree> <scratch copy>
"""
import pathlib
import subprocess
import sys

repo, copy = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
script = repo / "scripts" / "check-marker-companions.mjs"


def check():
    p = subprocess.run(["fnm", "exec", "--", "node", str(script), "--root", str(copy)],
                       cwd=repo, capture_output=True, text=True, encoding="utf-8", shell=True)
    return p.returncode, (p.stdout + p.stderr).strip()


def mutate(title, rel, old, new):
    path = copy / rel
    original = path.read_bytes()
    text = original.decode("utf-8")
    assert old in text, (rel, old)
    path.write_bytes(text.replace(old, new, 1).encode("utf-8"))
    code, out = check()
    path.write_bytes(original)
    print(f"== {title}: {rel}: {old!r} -> {new!r}\nexit {code}\n{out}\n")


print("== untouched copy", *check(), sep="\n")
R = "test/core/render/renderPipeline.test.ts"
M = "// @tests_req SwRS-MDOKFSTUDIO-CORE-001#S1"
V = "test/visual/scenarioDefinitions2.ts"
mutate("owner step 5 (accepts in test/visual)", V, M, M + "\n    // @accepts_req StRS-MDOKFSTUDIO-TRUST-012#S1")
mutate("owner step 6 (fragment removed)", R, M, "// @tests_req SwRS-MDOKFSTUDIO-CORE-001")
mutate("undeclared fragment", R, M, "// @tests_req SwRS-MDOKFSTUDIO-CORE-001#S99")
mutate("accepts on a SwRS", R, M, "// @accepts_req SwRS-MDOKFSTUDIO-CORE-001#S1")
mutate("StRS tests_req in test/integration", "test/integration/mystBlocksWindow.ts",
       "@accepts_req StRS-MDOKFSTUDIO-MYST-016#S2", "@tests_req StRS-MDOKFSTUDIO-MYST-016#S2")
