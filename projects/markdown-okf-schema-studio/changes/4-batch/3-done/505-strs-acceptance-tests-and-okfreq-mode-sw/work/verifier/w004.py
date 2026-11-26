"""Verifier of CR-505: use cases without an acceptance test in the new coverage mode, for one commit.

usage (from the head worktree, for its okfreq): python -I w004.py <repo> <sha> <empty export folder>
Exports <sha> with `git archive` outside every tracked tree, switches the mode in the export only,
validates it, prints the summary and the W004 use cases, and removes the export. The whole tree is
exported: with a copy of requirements/ alone, okfreq counts no acceptance marker and the links break.
"""
import io
import re
import shutil
import subprocess
import sys
import tarfile
from pathlib import Path

repo, sha, export = sys.argv[1], sys.argv[2], Path(sys.argv[3])
export.mkdir()
try:
    data = subprocess.run(["git", "-C", repo, "archive", "--format=tar", sha], capture_output=True, check=True).stdout
    with tarfile.open(fileobj=io.BytesIO(data)) as archive:
        archive.extractall(export, filter="data")
    config = export / "requirements" / "config.yml"
    text = config.read_text(encoding="utf-8")
    old = "strs_test_coverage_mode: linked-swrs-and-validation-test"
    assert text.count(old) == 1
    config.write_text(text.replace(old, "strs_test_coverage_mode: linked-swrs-and-acceptance-paths"),
                      encoding="utf-8", newline="\n")
    done = subprocess.run(["uv", "run", "--no-sync", "--group", "requirements", "okfreq", "validate",
                           str(export / "requirements"), "--check-links", "--project-root", str(export)],
                          capture_output=True)
    out = done.stdout.decode("utf-8", "replace") + done.stderr.decode("utf-8", "replace")
    summary = re.search(r"(\d+) requirements, (\d+) errors, (\d+) warnings", out)
    w004 = re.findall(r"^W004 .*?: (StRS-MDOKFSTUDIO-[A-Z]+-\d+) has no acceptance test", out, re.M)
    print(f"exit={done.returncode}; {summary.group(0) if summary else out[-400:]}")
    print(f"W004 (use cases without an acceptance test): {len(w004)}")
    print("trust-security:", " ".join(n.replace("StRS-MDOKFSTUDIO-", "") for n in w004 if "-TRUST-" in n))
finally:
    shutil.rmtree(export)
