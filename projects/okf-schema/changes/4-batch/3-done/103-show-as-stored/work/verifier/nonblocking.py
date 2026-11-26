"""What ``show`` does on a non-blocking standard output that is full (real process, real pipe)."""

import io
import os
import subprocess
import sys
import threading
from pathlib import Path

here = Path(__file__).resolve().parent
python = str(here / "vh" / "Scripts" / "python.exe")
bundle = here / "nb"
bundle.mkdir(exist_ok=True)
content = b"0123456789abcde\n" * 250000
(bundle / "big.md").write_bytes(content)
code = "from okf_schema.cli import cli; cli()"

for label, flags in (("default (buffered) stdout", []), ("python -u (raw) stdout", ["-u"])):
    read_end, write_end = os.pipe()
    os.set_blocking(write_end, False)
    child = subprocess.Popen(
        [python, *flags, "-c", code, "show", "--path", str(bundle), "big.md"],
        stdout=write_end,
        stderr=subprocess.PIPE,
    )
    os.close(write_end)
    errors: list[bytes] = []
    reader_err = threading.Thread(target=lambda c=child, e=errors: e.append(c.stderr.read()))
    reader_err.start()
    # Nobody reads standard output for three seconds: the pipe is full.
    try:
        child.wait(timeout=3)
        state = f"ended by itself with exit code {child.returncode} while nobody read"
    except subprocess.TimeoutExpired:
        state = "still running after 3 s with a full pipe"
    received = bytearray()
    while chunk := os.read(read_end, 65536):
        received += chunk
    child.wait(timeout=60)
    reader_err.join(timeout=10)
    os.close(read_end)
    lines = b"".join(errors).decode("utf-8", "replace").strip().splitlines()
    print(label)
    print("  while full:", state)
    print("  exit code:", child.returncode)
    print(f"  received {len(received)} of {len(content)} bytes")
    print("  stderr last line:", lines[-1] if lines else "(empty)")
