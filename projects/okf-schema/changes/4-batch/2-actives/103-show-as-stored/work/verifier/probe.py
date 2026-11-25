"""Before and after of ``show`` and ``trust``, with the base and head wheels.

Usage: python probe.py BASE_SHA HEAD_SHA OUTPUT_DIR
"""

import hashlib
import subprocess
import sys
from pathlib import Path

here = Path(__file__).resolve().parent
base_sha, head_sha = sys.argv[1:3]
out = Path(sys.argv[3]).resolve()
bundle = here / "probe" / "bundle"
bundle.mkdir(parents=True, exist_ok=True)
subprocess.run(["git", "init", "-q", str(here / "probe")], check=True)
(here / "probe" / "outside.md").write_bytes(b"# Outside\n")
(bundle / "sub").mkdir(exist_ok=True)

concepts = {
    "styled.md": b"---\r\ntype: concept  # keep this comment\r\ntitle: 'Quoted'\r\n"
    b"tags: [alpha, beta]\r\nverified: {by: human:alice, at: 2026-11-01T10:00:00Z}\r\n"
    b"stale_after: 2020-01-01\r\n---\r\n\r\nBody\r\n",
    "plain.md": b"# Plain\n\nNo frontmatter.\n",
    "broken.md": b"---\ntitle: [unclosed\n---\nBody\n",
    "latin1.md": b"---\ntitle: caf\xe9\n---\n",
}
for name, content in concepts.items():
    (bundle / name).write_bytes(content)


def tidy(data: bytes) -> str:
    text = data.decode("utf-8", "backslashreplace").replace("\r\n", "\n")
    for form in (str(here / "probe"), (here / "probe").as_posix()):
        text = text.replace(form, "<probe>")
    for form in (str(here), here.as_posix()):
        text = text.replace(form, "<S>")
    home = Path.home()
    return text.replace(str(home), "~").replace(home.as_posix(), "~").replace(home.name, "user")


def run(side: str, *args: str) -> tuple[list[str], subprocess.CompletedProcess]:
    exe = here / ("vb" if side == "before" else "vh") / "Scripts" / "okf-schema.exe"
    done = subprocess.run(
        [str(exe), args[0], "--path", str(bundle), *args[1:]], capture_output=True
    )
    lines = [f"$ okf-schema {args[0]} --path <probe>/bundle {' '.join(args[1:])}"]
    lines.append(f"exit code: {done.returncode}")
    if args[0] == "show" and done.returncode == 0:
        target = bundle / args[1]
        if not target.is_file():
            target = bundle / f"{args[1]}.md"
        stored = target.read_bytes()
        lines.append(f"stdout bytes: {done.stdout!r}")
        lines.append(f"identical to the stored file: {done.stdout == stored}")
    else:
        lines.append("stdout:")
        lines.append(tidy(done.stdout).rstrip("\n"))
    error = tidy(done.stderr).strip().splitlines()
    lines.append(f"stderr lines: {len(error)}")
    lines.extend(error if len(error) < 4 else [error[0], "  ...", error[-1]])
    return lines + [""], done


def digest() -> str:
    h = hashlib.sha256()
    for path in sorted(bundle.rglob("*")):
        if path.is_file():
            h.update(path.relative_to(bundle).as_posix().encode())
            h.update(path.read_bytes())
            h.update(str(path.stat().st_mtime_ns).encode())
    return h.hexdigest()


for side, sha in (("before", base_sha), ("after", head_sha)):
    for command in ("show", "trust"):
        report = [f"{side}: okf-schema {command}, wheel built from {sha}, Windows", ""]
        start = digest()
        names = ["styled", "plain", "broken", "latin1"]
        for name in names:
            report += run(side, command, name)[0]
        for name in ("missing", "missing.md", "sub", "../outside.md"):
            report += run(side, command, name)[0]
        report.append(f"bundle content and times unchanged: {start == digest()}")
        text = "\n".join(report) + "\n"
        (out / f"{side}-{command}.txt").write_bytes(text.encode("utf-8"))
        print(text)

print("=== frontmatter probes (head trust; base show for the same file)")
odd = {
    "impossible_date": b"stale_after: 2020-02-30",
    "impossible_other_key": b"created: 2020-13-01",
    "impossible_quoted": b'stale_after: "2020-02-30"',
    "verified_int": b"verified: 5",
    "verified_text": b"verified: yes please",
    "verified_list_int": b"verified: [1, null]",
    "verified_by_int": b"verified: {by: 5}",
    "verified_by_list": b"verified: {by: [a]}",
    "stale_list": b"stale_after: [1]",
    "stale_int": b"stale_after: 5",
    "stale_huge": b"stale_after: 9999-12-31T23:59:59-12:00",
    "stale_min": b"stale_after: 0001-01-01T00:00:00+12:00",
    "duplicate_key": b"title: a\ntitle: b",
    "undefined_alias": b"title: *nothing",
    "tab": b"title:\n\t- a",
    "list_frontmatter": b"- a\n- b",
    "bad_int_tag": b"count: !!int abc",
    "recursive_anchor": b"a: &a [*a]",
}
for name, frontmatter in odd.items():
    (bundle / f"{name}.md").write_bytes(b"---\n" + frontmatter + b"\n---\nBody\n")
for name, frontmatter in odd.items():
    for side, command in (("after", "trust"), ("after", "show"), ("before", "show")):
        lines, done = run(side, command, name)
        shown = done.stdout.decode("utf-8", "replace").split() if command == "trust" else ""
        err = tidy(done.stderr).strip().splitlines()
        print(name, side, command, "exit", done.returncode, shown, err[-1] if err else "")
print("=== list with the impossible date only")
for name in odd:
    if name != "impossible_date":
        (bundle / f"{name}.md").unlink()
for side in ("before", "after"):
    lines, done = run(side, "list")
    err = tidy(done.stderr).strip().splitlines()
    print(side, "list exit", done.returncode, err[-1] if err else "")
