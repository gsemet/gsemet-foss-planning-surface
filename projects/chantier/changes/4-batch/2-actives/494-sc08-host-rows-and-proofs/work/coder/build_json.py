import json
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).parent))
from rows import ROWS, P  # noqa: E402

OUT = Path(sys.argv[1])
BAD = re.compile(
    r"\d{4}-\d{2}-\d{2}|batch-\d+|CR-\d+|PR \d+|#\d+|\b(proved|unproved|documented|untested|trial)\b",
    re.I,
)
ids = [r["id"] for r in ROWS]
assert len(set(ids)) == 50
for host, fname, key in (("claude", "claude-code.json", "claude"), ("copilot", "copilot.json", "copilot")):
    rows = []
    for r in ROWS:
        means = r[key]
        assert 2 <= len(means) <= 4, (r["id"], host)
        for line in means:
            assert len(line) <= 160, (r["id"], host, len(line), line)
            assert not BAD.search(line), (r["id"], host, line)
        rows.append(
            {
                "capability": r["id"],
                "name": r["name"],
                "roles": r["roles"],
                "means": means,
                "mark": r["mark"] if host == "claude" else "untested",
            }
        )
    (OUT / fname).write_text(
        json.dumps({"host": host, "rows": rows}, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
print("ok")
