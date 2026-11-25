"""Compare ``show_bundle`` between the base and head wheels on the same files."""

import json
import subprocess
import sys
from pathlib import Path

here = Path(__file__).resolve().parent
bundle = here / "api"
bundle.mkdir(exist_ok=True)
front = b"---\ntitle: T\nverified: {by: human:alice, at: 2026-11-01}\nstale_after: 2020-01-01\n---\n\nBody\n"
files = {
    "lf": front,
    "crlf": front.replace(b"\n", b"\r\n"),
    "cr": front.replace(b"\n", b"\r"),
    "mixed": b"---\r\ntitle: |\r  a\n  b\r\n---\r\r\nBody\r\r\n",
    "bom": b"\xef\xbb\xbf" + front,
    "plain": b"# Plain\r\n",
    "broken": b"---\ntitle: [unclosed\n---\nBody\n",
    "empty": b"",
    "latin1": b"---\ntitle: caf\xe9\n---\n",
}
for name, content in files.items():
    (bundle / f"{name}.md").write_bytes(content)

child = """
import dataclasses, json, sys
from pathlib import Path
from okf_schema.api import show_bundle
out = {}
for name in sys.argv[2:]:
    try:
        detail = dataclasses.asdict(show_bundle(sys.argv[1], name))
        if "raw" in detail:
            stored = (Path(sys.argv[1]) / (name + ".md")).read_bytes()
            detail["raw"] = detail["raw"].encode("utf-8") == stored
        out[name] = detail
    except Exception as exc:
        out[name] = {"error": type(exc).__name__}
print(json.dumps(out, default=str))
"""
results = {}
for side in ("vb", "vh"):
    done = subprocess.run(
        [str(here / side / "Scripts" / "python.exe"), "-I", "-c", child, str(bundle), *files],
        capture_output=True,
        check=True,
    )
    results[side] = json.loads(done.stdout)
for name in files:
    base, head = results["vb"][name], dict(results["vh"][name])
    raw = head.pop("raw", None)
    print(f"{name}: other fields equal={base == head} raw==stored bytes={raw} head={head}")

for args in (["--help"], ["show", "--help"], ["trust", "--help"]):
    done = subprocess.run(
        [str(here / "vh" / "Scripts" / "okf-schema.exe"), *args], capture_output=True, text=True
    )
    lines = [line.strip() for line in done.stdout.splitlines() if line.strip()]
    keep = [l for l in lines if l.startswith(("show ", "trust ", "Print "))]
    print("help", " ".join(args), done.returncode, keep)
