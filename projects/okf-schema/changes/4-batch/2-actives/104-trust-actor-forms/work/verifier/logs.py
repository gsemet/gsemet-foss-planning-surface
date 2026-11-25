"""Compare the gate logs the description's claims rest on (argv[1]: the CR's work folder)."""

import os
import re
import sys
from pathlib import Path

work = Path(sys.argv[1])
logs = {
    "gate 7a33d92": work / "gates/20261125-224645.log",
    "gate 1ae8870": work / "gates/20261125-222513.log",
    "base 2f09cef, links refused": work / "debugger/base-test.log",
    "base 2f09cef, links allowed": work / "debugger/base-test-devmode.log",
}
failed = {}
for name, path in logs.items():
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    print(f"=== {name}: {path.name}")
    print("first line:", re.sub(r"[A-Z]:[\\/]Users[\\/][^\\/ ]+", "~", lines[0])[:200])
    failed[name] = sorted({m.group(1) for line in lines if (m := re.match(r"FAILED (\S+)", line))})
    for line in lines:
        if re.search(r"=+ .*\d+ (passed|failed).* in [\d.]+s|Total coverage|^build succeeded|^result:|sphinx-build -W", line):
            print("  ", line.strip())
    print("   'warnings summary' lines:", sum("warnings summary" in line for line in lines),
          "| lines with 'Warning:' :", sum("Warning:" in line for line in lines),
          "| lines with WinError 1314:", sum("WinError 1314" in line for line in lines))
    for name_ in failed[name]:
        print("   FAILED", name_)
print("same failing tests, 1ae8870 and base:",
      failed["gate 1ae8870"] == failed["base 2f09cef, links refused"], len(failed["gate 1ae8870"]))
target = Path(__file__).parent / "link-probe"
target.mkdir(exist_ok=True)
(target / "t.txt").write_text("x", encoding="utf-8")
os.symlink(target / "t.txt", target / "l.txt")
os.symlink(target, target / "ld", target_is_directory=True)
print("symlink probe on this host: file", (target / "l.txt").is_symlink(), "| directory", (target / "ld").is_symlink())
os.remove(target / "l.txt")
os.rmdir(target / "ld")
os.remove(target / "t.txt")
target.rmdir()
