"""Verifier of CR-505: validate the requirements of one commit in the new coverage mode, on a copy.

usage: python -I newmode.py <repo worktree> <sha> <scratch folder that does not exist yet> <log folder>
`git init`s the scratch folder, extracts `git archive <sha>` into it (members whose full path would
pass 259 characters are left out and listed), validates once in the tracked mode, switches
`strs_test_coverage_mode` in the copy only, validates again, compares the two logs and removes the
scratch folder.
"""
import io
import os
import re
import shutil
import stat
import subprocess
import sys
import tarfile
from pathlib import Path

repo, sha, scratch, logs = sys.argv[1], sys.argv[2], Path(sys.argv[3]), Path(sys.argv[4])
assert not scratch.exists()


def writable(function, path, _error):
    os.chmod(path, stat.S_IWRITE)
    function(path)


def validate(label):
    done = subprocess.run(["uv", "run", "--no-sync", "--directory", repo, "--group", "requirements", "okfreq",
                           "validate", str(scratch / "requirements"), "--check-links", "--project-root", str(scratch)],
                          capture_output=True)
    out = done.stdout.decode("utf-8", "replace") + done.stderr.decode("utf-8", "replace")
    (logs / f"newmode-{label}-{sha[:7]}.log").write_text(out, encoding="utf-8", newline="\n")
    summary = re.search(r"(\d+) requirements, (\d+) errors, (\d+) warnings", out)
    codes = {}
    for line in out.splitlines():
        m = re.match(r"([EWI]\d+)\b", line)
        if m:
            codes[m.group(1)] = codes.get(m.group(1), 0) + 1
    print(f"{label}: exit={done.returncode}; {summary.group(0) if summary else out[-600:]}; lines per code: {codes}")
    return out


subprocess.run(["git", "init", "-q", str(scratch)], check=True)
try:
    data = subprocess.run(["git", "-C", repo, "archive", "--format=tar", sha], capture_output=True, check=True).stdout
    skipped = []
    with tarfile.open(fileobj=io.BytesIO(data)) as archive:
        members = []
        for member in archive.getmembers():
            if len(str(scratch.resolve())) + 1 + len(member.name) > 259:
                skipped.append(member.name)
            else:
                members.append(member)
        archive.extractall(scratch, members=members, filter="data")
    tops = sorted({"/".join(n.split("/")[:3]) for n in skipped})
    print(f"extracted {len(members)} members, left out {len(skipped)} (path too long), under: {tops}")
    current = validate("current")
    config = scratch / "requirements" / "config.yml"
    text = config.read_text(encoding="utf-8")
    old = "strs_test_coverage_mode: linked-swrs-and-validation-test"
    assert text.count(old) == 1
    config.write_text(text.replace(old, "strs_test_coverage_mode: linked-swrs-and-acceptance-paths"),
                      encoding="utf-8", newline="\n")
    new = validate("new")
    broken = lambda out: sorted(l for l in out.splitlines() if "Broken cross-link" in l)
    print(f"broken cross-links: current {len(broken(current))}, new {len(broken(new))}, "
          f"same lines: {broken(current) == broken(new)}")
    w004 = re.findall(r"^W004 .*?: (StRS-MDOKFSTUDIO-[A-Z]+-\d+) has no acceptance test", new, re.M)
    print(f"W004 (use cases without an acceptance test): {len(w004)}")
    print("trust-security:", " ".join(n.replace("StRS-MDOKFSTUDIO-", "") for n in w004 if "-TRUST-" in n))
finally:
    shutil.rmtree(scratch, onexc=writable)
    print(f"scratch removed: {not scratch.exists()}")
