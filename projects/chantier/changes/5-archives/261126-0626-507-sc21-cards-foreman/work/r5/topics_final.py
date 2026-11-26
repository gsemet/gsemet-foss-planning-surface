"""Finish cards-next/topics.json: the base names still missing and the two new topics."""

import json
from pathlib import Path

CN = Path("C:/Users/gaeta/Projets/chantier.worktrees/batch-31-CR-507/skills/chantier/cards-next")
BASE = CN.parent / "references" / "topics.json"
path = CN / "topics.json"
raw = path.read_text(encoding="utf-8")
data = json.loads(raw)
assert json.dumps(data, indent=2, ensure_ascii=False) + "\n" == raw.replace("\r\n", "\n"), "format"
base = json.loads(BASE.read_text(encoding="utf-8"))
topics = data["topics"]


def t(*names: str) -> list[str]:
    return [f"topics/{n}.md" for n in names]


def pair(name: str, parts: int = 2) -> list[str]:
    return [f"{name}-p{i}" for i in range(1, parts + 1)]


COS = ["chief-of-staff"]
# base name -> readings: the topics the family inventories give as homes of the base card's rows
FROM_BASE = {
    "grill": (
        "grill-series",
        t(
            "grill-series", "grill-options", "grill-restate", *pair("grill-backlog"),
            *pair("grill-specify"), "grill-critic", "grill-critic-steps", "where-cr-goes", "writer",
        ),
        ["chief-of-staff", "griller"],
    ),
    "batch-start": (
        "trials",
        t(
            "trials", "batch-plan", "batch-plan-show", *pair("batch-plan-mode"), "batch-plan-cut",
            *pair("foreman-start"), "foreman-start-more",
        ),
        COS,
    ),
    "steering": (
        "steering-reports",
        t(
            *pair("steering-reports"), "asks", "driver-question", "chain-conflict",
            "rounds-exception", "watcher-events", "watcher-lines", *pair("refused-push-chief"),
            *pair("refused-push-chief-more"), "refused-rebase-chief", "refused-answer",
            "refused-push-judgement", "refused-push-gate", "refused-push-route",
            "refused-push-run", "refused-rebase", "refused-rebase-run",
        ),
        COS,
    ),
    "ready-to-merge": (
        "merge-words",
        t(
            "merge-words", "merge-gaps", "merge-recorded", *pair("merge-series-stack"),
            *pair("merge-stack-ready"), "merge-stack-gitlab", *pair("stack-changes-chief"),
        ),
        COS,
    ),
    "batch-end": (
        "batch-pause",
        t(
            "batch-pause", *pair("retro-route"), *pair("retro-route-chantier"),
            *pair("batch-close"), *pair("batch-close-stopped"), "recovery",
        ),
        COS,
    ),
    "direct": (
        "direct-mode",
        t(*pair("direct-mode", 3), *pair("direct-mode-epoch"), *pair("direct-mode-accept")),
        COS,
    ),
    "release-procedure": (
        "release-chief",
        t(
            *pair("release-chief"), *pair("release-chief-approve"), *pair("release-chief-auto"),
            *pair("release-chief-after"),
        ),
        COS,
    ),
}


def insert(before_or_after: str, name: str, entry: dict, after: bool = False) -> None:
    assert name not in topics, name
    items = list(topics.items())
    at = [n for n, _ in items].index(before_or_after) + (1 if after else 0)
    items.insert(at, (name, entry))
    topics.clear()
    topics.update(items)


for name, (anchor, readings, roles) in FROM_BASE.items():
    trigger = base["topics"][name]["trigger"]
    anchor = anchor if anchor in topics else f"{anchor}-p1" if f"{anchor}-p1" in topics else anchor
    insert(anchor, name, {"readings": readings, "roles": roles, "trigger": trigger})

insert(
    "worker-shell",
    "session-shell",
    {
        "readings": t("session-shell"),
        "roles": [
            "cr-driver", "release-driver", "stack-driver", "qa-driver", "chief-of-staff",
            "foreman", "griller", "spec-writer", "spec-critic", "retro-critic",
        ],
        "trigger": "a shell call that waits, backgrounds or changes folder; a text for the forge",
        "review_by": "0.16.0",
    },
    after=True,
)
insert(
    "cr-rounds",
    "cr-review-step",
    {
        "readings": t("cr-review-step"),
        "roles": ["cr-driver"],
        "trigger": "an extra review step of `Team:` to brief",
    },
    after=True,
)
data["paths"] = (
    "relative to this folder (cards-next/); a reading: file, file#heading (a level-2 heading of "
    'that file), or {"claude": ..., "copilot": ...} (that host only)'
)
out = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
path.write_text(out, encoding="utf-8", newline="")
print(len(topics), "topics")
