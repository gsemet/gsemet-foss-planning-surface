"""Throwaway: tests/test_cli_runs.py's allow-rules assertions, run on cards-next's host card."""

import json
import re
from pathlib import Path

from chantier.commands.allow_samples import RECOMMENDED_ALLOW, SAMPLES
from chantier.commands.permissions import rule_matches

# the CLI imported here is the worktree's own (uv run --project <worktree>)

CN = Path("C:/Users/gaeta/Projets/chantier.worktrees/batch-31-CR-507/skills/chantier/cards-next")
text = (CN / "hosts" / "claude-code.md").read_text(encoding="utf-8")
section = text.split("### Allow rules\n", 1)[1]
found = re.search(r"```json\n(.*?)\n```", section, re.S)
assert found is not None
assert tuple(json.loads(found[1])["permissions"]["allow"]) == RECOMMENDED_ALLOW
assert any("<checkout>" in r for r in RECOMMENDED_ALLOW)
assert any("<plugin root>" in r for r in RECOMMENDED_ALLOW)


def fill(text: str) -> str:
    return text.replace("<checkout>", "/some/path").replace("<plugin root>", "/some/path")


for _, _, command, rule in SAMPLES:
    assert all(
        rule_matches(f"{tool}({fill(rule)})", tool, fill(command)) for tool in ("Bash", "PowerShell")
    ), command
assert rule_matches("SendMessage", "SendMessage")
assert not any("release create" in rule for rule in RECOMMENDED_ALLOW)
assert not any("merge-async" in rule or "/stacks" in rule for rule in RECOMMENDED_ALLOW)
table = text.split("### Capabilities and their commands\n", 1)[1].split("\n###", 1)[0]
rows = [ln for ln in table.splitlines() if ln.startswith("| ") and "---" not in ln][1:]
in_table = [re.findall(r"`([^`]+)`", ln.split(" | ")[3]) for ln in rows]
in_samples = [
    list(dict.fromkeys(s[3] for s in SAMPLES if s[0] == cap))
    for cap in ("batch", "stack", "release", "fixes")
]
assert in_table == in_samples, (in_table, in_samples)
print("allow-rules assertions pass on cards-next/hosts/claude-code.md:",
      len(RECOMMENDED_ALLOW), "rules,", len(SAMPLES), "samples,", len(rows), "capability rows")
