"""Verifier of CR-505: use cases without an acceptance test in the new coverage mode, for one tree.

usage (from the head worktree, for its okfreq): python -I w004.py <tree> <copy folder>
Copies <tree>/requirements to <copy folder>, switches the mode in the copy only, validates it against
the markers of <tree>, prints the W004 count and removes the copy. Link warnings are not comparable
here (the copy sits outside its tree), so only W004 and the error count are printed.
"""
import re
import shutil
import subprocess
import sys
from pathlib import Path

tree, copy = Path(sys.argv[1]), Path(sys.argv[2])
shutil.copytree(tree / "requirements", copy)
try:
    config = copy / "config.yml"
    text = config.read_text(encoding="utf-8")
    old = "strs_test_coverage_mode: linked-swrs-and-validation-test"
    assert text.count(old) == 1
    config.write_text(text.replace(old, "strs_test_coverage_mode: linked-swrs-and-acceptance-paths"),
                      encoding="utf-8", newline="\n")
    done = subprocess.run(["uv", "run", "--no-sync", "--group", "requirements", "okfreq", "validate", str(copy),
                           "--check-links", "--project-root", str(tree)], capture_output=True)
    out = done.stdout.decode("utf-8", "replace") + done.stderr.decode("utf-8", "replace")
    summary = re.search(r"(\d+) requirements, (\d+) errors", out)
    w004 = re.findall(r"^W004 .*?: (StRS-MDOKFSTUDIO-[A-Z]+-\d+) has no acceptance test", out, re.M)
    print(f"exit={done.returncode}; {summary.group(0) if summary else out[-400:]}")
    print(f"W004 (use cases without an acceptance test): {len(w004)}")
    print("trust-security:", " ".join(sorted(n.rsplit('-', 2)[1] + '-' + n.rsplit('-', 1)[1] for n in w004 if "-TRUST-" in n)))
finally:
    shutil.rmtree(copy)
