"""Read-only: run the audit on every row `rehome.py` moved, listing only the rows whose home
does not seem to hold a clause or a span. `--min N` sets the score to print from."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
ARGS = sys.argv[1:]
sys.argv = sys.argv[:1]
import audit  # noqa: E402
import rehome  # noqa: E402

MIN = float(ARGS[ARGS.index("--min") + 1]) if "--min" in ARGS else 2.0
keys = set(rehome.MOVES) | set(rehome.APPEND)
idf, top = audit.idf_table()
cache: dict = {}
textless = []
count = 0
for _, row, _, seg in audit.segments():
    if row["id"] not in keys:
        continue
    count += 1
    files = audit.home_files(row["new home"])
    if not files:
        textless.append(f"{row['id']} -> {row['new home']}")
        continue
    score, lost, bad = audit.check(seg, files, idf, top, cache)
    if score >= MIN:
        print(f"{row['id']} {score} [{row['kind']}] -> {row['new home']}")
        print(f"   S: {seg[:420]}")
        if lost:
            print(f"   spans: {lost}")
print(count, "moved rows;", len(textless), "with no text home:")
for item in textless:
    print("  ", item[:200])
