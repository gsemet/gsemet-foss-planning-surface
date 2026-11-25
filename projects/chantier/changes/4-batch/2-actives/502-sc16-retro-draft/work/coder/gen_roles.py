"""Throwaway (CR-502 r3): print roles.yaml's entries from brief_roles.py and the shipped wrappers
(copied, not retyped)."""

import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
sys.path.insert(0, str(ROOT / "skills/chantier/scripts/cli/src"))
from chantier.brief_roles import roles  # noqa: E402
from ruamel.yaml import YAML  # noqa: E402

KIND = {
    "chief-of-staff": "steering", "griller": "steering", "foreman": "steering",
    "cr-driver": "driver", "release-driver": "driver", "stack-driver": "driver", "qa-driver": "driver",
    "inspector": "review-step", "spec-critic": "critic", "retro-critic": "critic",
}
STARTED = {
    "chief-of-staff": ["user"], "griller": ["user"], "foreman": ["chief-of-staff"],
    "cr-driver": ["foreman", "chief-of-staff"], "release-driver": ["foreman", "chief-of-staff"],
    "stack-driver": ["foreman", "chief-of-staff"], "qa-driver": ["foreman", "chief-of-staff"],
    "demo-explorer": ["chief-of-staff"], "spec-writer": ["chief-of-staff"],
    "spec-critic": ["chief-of-staff", "griller"], "retro-critic": ["foreman", "chief-of-staff"],
    "board-griller": ["surface-server"],
}
REPLY = {
    "cr-driver": "driver.md#Means: your end", "stack-driver": "driver.md#Means: your end",
    "qa-driver": "driver.md#Means: your end",
    "release-driver": "release-driver-end.md#Release driver: the end",
    "spec-writer": "spec-writer.md#End", "spec-critic": "spec-critic.md#Reply",
    "retro-critic": "retro-critic.md#Reply", "board-griller": "griller.md#Started from the board",
}
PLAIN = {
    "chief-of-staff": "Steers the user's chantier project: grills, plans and runs its batches. Started by the user.",
    "griller": "Grills one chantier CR with the user until its specification can be written. Started by the user.",
    "foreman": "Runs one chantier batch for the Chief of Staff: starts its Drivers and records their ends. Started by the Chief of Staff.",
}
FM = re.compile(r"\A---\n(.*?)\n---\n", re.S)
yaml = YAML(typ="safe", pure=True)


def q(s):
    return "'" + s.replace("'", "''") + "'"


def front(path):
    return yaml.load(FM.match(path.read_text("utf-8").replace("\r\n", "\n"))[1])


out = []
for r in roles():
    n = r.name
    claude = ROOT / "agents" / f"{n}.md"
    copilot = ROOT / "com.github.copilot/agents" / f"chantier-{n}.agent.md"
    if claude.is_file():
        fc, fp = front(claude), front(copilot)
        desc, _, first = fc["description"].partition(" Prompt starts with: ")
        first = first.strip("`")
        ct = fc["tools"].split(", ")
        pt = list(fp["tools"])
    else:
        desc, first, ct, pt = PLAIN[n], None, [], []
    reply = "none" if KIND.get(n) == "steering" else REPLY.get(n, f"{n}.md#Your part")
    rows = "null" if r.rows is None else "[" + ", ".join(r.rows) + "]"
    out += [
        f"  - name: {n}",
        f"    kind: {KIND.get(n, 'worker')}",
        f"    started_by: [{', '.join(STARTED.get(n, ['driver']))}]",
        f"    writes: {r.writes}",
        f"    reply: {q(reply) if reply != 'none' else 'none'}",
        f"    card: {r.card}",
        f"    first: {q(first) if first else 'null'}",
        f"    description: {q(desc)}",
        f"    unit: {r.unit}",
        f"    rows: {rows}",
        "    hosts:",
        "      claude:",
        f"        wrapper: {'agents/' + n + '.md' if first else 'null'}",
        f"        tools: [{', '.join(ct)}]",
        "      copilot:",
        f"        wrapper: {'com.github.copilot/agents/chantier-' + n + '.agent.md' if first else 'null'}",
        f"        tools: [{', '.join(pt)}]",
    ]
sys.stdout.reconfigure(encoding="utf-8", newline="\n")
print("\n".join(out))
