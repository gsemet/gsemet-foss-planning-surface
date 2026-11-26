"""Round 8: B012 and B017 are dropped, no host row holds them (run once)."""
from pathlib import Path

PATH = Path(__file__).resolve().parents[2] / "evidence" / "boundaries-split.md"
raw = PATH.read_bytes()
for old, new in (
    (b"(B012: Copilot host row)", b"(B012: dropped, unproved bookkeeping; no host row holds it)"),
    (b"B017: Copilot host row,", b"B017: dropped, unproved bookkeeping (no host row holds it),"),
):
    assert raw.count(old) == 1, old
    raw = raw.replace(old, new)
PATH.write_bytes(raw)
print("ok")
