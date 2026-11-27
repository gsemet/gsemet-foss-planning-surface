"""The `--once` capture of `docs/boards.md`: the worktree's `chantier live --once` code (`once`, its
`height_for` and `screen.plain`), fed with prepared events of a made-up scratch batch, at 140
columns in the zone Europe/Paris. No board, no network, no path of this machine.

usage, from the worktree:
    uv run --no-sync python <this file> <out file> [<boards.md to rewrite the capture in>]
"""

import contextlib
import io
import re
import sys
import threading
from pathlib import Path
from zoneinfo import ZoneInfo

from chantier import __version__
from chantier.clients.tui.link import Event, Idle, Linked
from chantier.clients.tui.model import Model
from chantier.commands import live

NOW = "2026-11-23T11:26:25Z"
WIDTH = 140


def cr(number: int, title: str, state: str, **more: object) -> dict[str, object]:
    row = {"phase": None, "round": 0, "round_limit": 3, "lease": None, "blocked": None}
    return {**row, "cr": f"CR-{number}", "title": title, "state": state, **more}


def record(t: str, actor: str, kind: str, number: int | None = None) -> dict[str, str]:
    line = {"t": t, "actor": actor, "kind": kind}
    return {**line, "cr": f"CR-{number}"} if number else line


LEASE = {"n": 1, "renewed": NOW, "expires": "2026-11-23T11:35:20Z", "ended": None, "gate": None}
CRS = [
    cr(101, "Export the report as CSV", "working", phase="coder r1", round=1, lease=LEASE),
    cr(102, "Fix the login redirect", "handed_back", to_review=True,
       handed_back_at="2026-11-23T11:14:00Z"),
    cr(103, "Add the audit log export", "handed_back", to_review=True,
       handed_back_at="2026-11-23T10:51:00Z"),
    cr(104, "Rename the config key", "blocked", blocked="waits for the user's answer"),
]  # fmt: skip
EVENTS = [
    record("2026-11-22T17:40:12Z", "chief-of-staff", "open"),
    record("2026-11-23T09:02:31Z", "foreman", "take", 101),
    record("2026-11-23T10:51:00Z", "foreman", "handback", 103),
    record("2026-11-23T11:14:00Z", "foreman", "handback", 102),
]
BATCH = {
    "id": "batch-01", "state": "running", "mode": "batch", "crs": CRS, "stack_lease": None,
    "merge_order": ["CR-103", "CR-102"], "steering": "foreman",
    "heartbeat": "2026-11-23T11:23:25Z", "steering_wake_min": 55,
}  # fmt: skip
PRS = [
    {"cr": "CR-103", "number": 13, "pr": "https://example.com/demo/pull/13", "ready_now": True},
    {"cr": "CR-102", "number": 12, "pr": "https://example.com/demo/pull/12", "checking": True},
]
BOARD = {
    "version": __version__,
    "served": "/work/demo",
    "projects": [{"id": "demo", "inbox": 0, "backlog": 2}],
}
PROJECT = {"batch": BATCH, "events": EVENTS, "seat": {"title": "Demo, the Chief of Staff"}}


class Prepared:
    """A stand-in link that gives the prepared answers, then idles."""

    base, deadline = "http://127.0.0.1/", None

    def want(self, _wants: object) -> None:
        pass

    def items(self):
        yield Linked("ws", NOW)
        yield Event("board", "board", BOARD, NOW)
        yield Event("project:demo", "project", PROJECT, NOW)
        yield Event("events:demo", "events", {"lines": []}, NOW)
        yield Event("prs:demo:batch-01", "prs", {"batch": "batch-01", "rows": PRS}, NOW)
        while True:
            threading.Event().wait(0.05)
            yield Idle()


live._width = lambda: WIDTH
model = Model(clock=lambda: 0.0, zone=ZoneInfo("Europe/Paris"))
out = io.StringIO()
with contextlib.redirect_stdout(out):
    live.once([Prepared()], [model])
text = out.getvalue()
Path(sys.argv[1]).write_bytes(text.encode("utf-8"))
if len(sys.argv) > 2:
    doc = Path(sys.argv[2])
    old = doc.read_bytes().decode("utf-8")
    newline = "\r\n" if "\r\n" in old else "\n"
    block = f"```text\n{text}```".replace("\n", newline)
    new, count = re.subn(r"```text\r?\nchantier live .*?```", lambda _: block, old, flags=re.DOTALL)
    assert count == 1, count
    doc.write_bytes(new.encode("utf-8"))
sys.stdout.buffer.write(text.encode("utf-8"))
