"""Round 8: one sibling-edit row sibling.py missed (run once)."""
from pathlib import Path

PATH = Path(__file__).resolve().parents[2] / "evidence" / "cards-inventory-host-and-shared.md"
raw = PATH.read_bytes().decode("utf-8")
nl = "\r\n" if "\r\n" in raw else "\n"
lines = raw.split(nl)
at = next(i for i, x in enumerate(lines) if x.startswith("| topics/release-chief-after-p2.md:5 |"))
lines.insert(at, "| topics/refused-push-chief-p2.md:3 | a protected-branch rejection is handled as a failed lease and told as information | review |")
PATH.write_bytes(nl.join(lines).encode("utf-8"))
print("ok")
