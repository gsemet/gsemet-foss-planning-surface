"""Verifier of CR-505: break one behaviour in the compiled output (ignored out/), run the tests, restore.

usage (from the worktree): python -I mutate.py
Each break edits one file under out/src/, runs the three test files of the four tightened tests and
writes the original bytes back.
"""
import re
import subprocess
from pathlib import Path

TESTS = [
    "out/test/session/trustReq.roots.requirements.test.js",
    "out/test/security/readOnlyRoot.requirements.test.js",
]
BREAKS = [
    ("none", None, None, None),
    ("restricted-root message no longer names the home folder", "out/src/core/security/resource-policy.js",
     "is in your home folder", "is in a broad folder"),
    ("workspace folder not added for restricted reads", "out/src/session/features/rendering.js",
     "? [workspaceFolder] : [];", "? [] : [];"),
    ("bundle folder not pushed to the roots", "out/src/session/features/rendering.js",
     "localResourceRoots.push(bundleRoot);", "void bundleRoot;"),
]


def run():
    done = subprocess.run(["fnm", "exec", "--", "node", "--import", "./scripts/register-myst-patches.mjs", "--test",
                           "--test-reporter=spec", *TESTS], capture_output=True)
    text = done.stdout.decode("utf-8", "replace")
    summary = " ".join(re.findall(r"^\S+ ((?:tests|pass|fail) \d+)", text, re.M))
    failed = sorted(set(re.findall(r"^\s*✖ (.*?) \([\d.]+ms\)", text, re.M)))
    return done.returncode, summary, failed


for label, file, old, new in BREAKS:
    path = Path(file) if file else None
    original = path.read_bytes() if path else None
    try:
        if path:
            count = original.count(old.encode())
            if count != 1:
                raise SystemExit(f"{label}: expected one match in {file}, found {count}")
            path.write_bytes(original.replace(old.encode(), new.encode()))
        code, summary, failed = run()
    finally:
        if path:
            path.write_bytes(original)
    print(f"== break: {label}\n   exit {code}; {summary}")
    for name in failed:
        print(f"   FAIL {name}")
    if path:
        print(f"   restored: {path.read_bytes() == original}")
