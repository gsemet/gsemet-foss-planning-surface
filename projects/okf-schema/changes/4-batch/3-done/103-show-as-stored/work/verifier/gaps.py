"""Known gaps of the description, probed with the head wheel (byte order mark, bad dates)."""

import subprocess
from pathlib import Path

here = Path(__file__).resolve().parent
exe = str(here / "vh" / "Scripts" / "okf-schema.exe")
python = str(here / "vh" / "Scripts" / "python.exe")
front = b"---\ntype: concept\nverified: {by: human:alice, at: 2026-11-01}\n---\n\nBody\n"


def run(bundle: Path, command: str, *args: str) -> None:
    done = subprocess.run([exe, command, "--path", str(bundle), *args], capture_output=True)
    errors = done.stderr.decode("utf-8", "replace").strip().splitlines()
    out = done.stdout.decode("utf-8", "replace").split("\r\n") if command == "trust" else []
    print(command, *args, "exit", done.returncode, out, errors[-1] if errors else "")


bom = here / "bom"
bom.mkdir(exist_ok=True)
(bom / "marked.md").write_bytes(b"\xef\xbb\xbf" + front)
(bom / "unmarked.md").write_bytes(front)
for name in ("marked", "unmarked"):
    run(bom, "trust", name)
code = (
    "import sys; from okf_schema.api import show_bundle; "
    "d = show_bundle(sys.argv[1], 'marked'); print('show_bundle marked:', d.frontmatter, d.trust_tier)"
)
subprocess.run([python, "-I", "-c", code, str(bom)], check=True)

for label, line in (("date", b"stale_after: 2020-02-30"), ("tag", b"count: !!int abc")):
    bundle = here / label
    bundle.mkdir(exist_ok=True)
    (bundle / "odd.md").write_bytes(b"---\ntype: concept\n" + line + b"\n---\nBody\n")
    print("==", line.decode())
    run(bundle, "trust", "odd")
    run(bundle, "show", "odd")
    run(bundle, "list")
