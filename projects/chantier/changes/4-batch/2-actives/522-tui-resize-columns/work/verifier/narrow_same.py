"""Prints the drawn screen at narrow widths, for a diff between the base and the head sources."""

import io
from zoneinfo import ZoneInfo

from chantier.clients.tui import screen
from chantier.clients.tui.link import Event, Linked
from chantier.clients.tui.model import Model

NOW = "2030-01-01T00:00:00Z"


def board(ids, label=""):
    m = Model(clock=lambda: 0.0, zone=ZoneInfo("Europe/Paris"), label=label)
    m.feed(Linked("ws", NOW))
    data = {"version": "0.15.1", "served": "/work/demo", "projects": [{"id": i} for i in ids]}
    m.feed(Event("board", "board", data, NOW))
    for i in ids:
        batch = {"id": "batch-01", "state": "running", "mode": "batch", "crs": [], "stack_lease": None}
        events = [{"t": "2029-12-31T23:50:00Z", "actor": "a-very-long-actor-name", "kind": "took", "cr": "CR-1"}]
        m.feed(Event(f"project:{i}", "project", {"batch": batch, "events": events}, NOW))
        m.feed(Event(f"events:{i}", "events", {"lines": [{"seq": 1, "t": NOW, "source": "hub", "text": "x" * 200}]}, NOW))
    return m


# the widths where the head's Flow is at its minima with no left column (as the base draws it)
CASES = {"one": (lambda: [board(["demo-shop"])], 99), "projects": (lambda: [board(["demo-shop", "demo-site"])], 99),
         "boards": (lambda: [board(["demo-shop"], "a"), board(["demo-site"], "b")], 99)}
for case, (make, top) in CASES.items():
    for width in range(40, 100):
        if case == "one" and width > 94:
            continue
        if case != "one" and width > 99:
            continue
        out = io.StringIO()
        screen.plain(make(), width, 24, out)
        print(f"== {case} {width}")
        print(out.getvalue(), end="")
