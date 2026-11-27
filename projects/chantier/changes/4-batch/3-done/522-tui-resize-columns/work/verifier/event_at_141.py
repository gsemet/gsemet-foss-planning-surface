import io
from zoneinfo import ZoneInfo
import chantier
from chantier.clients.tui import screen
from chantier.clients.tui.link import Event, Linked
from chantier.clients.tui.model import Model
from chantier.clients.tui.view import View

print("source:", "base 4d12a5be" if "scratch" in chantier.__file__.replace("\\", "/") else "head 3412cd9")
now = "2030-01-01T00:00:00Z"
m = Model(clock=lambda: 0.0, zone=ZoneInfo("Europe/Paris"), label="")
m.feed(Linked("ws", now))
m.feed(Event("board", "board", {"version": "0.15.1", "served": "/work/demo", "projects": [{"id": "demo-shop"}]}, now))
row = {"cr": "CR-1", "title": "Demo change", "state": "working", "phase": "coding", "round": 1, "round_limit": 3, "blocked": None, "lease": None}
batch = {"id": "batch-01", "state": "running", "mode": "batch", "crs": [row], "stack_lease": None}
ev = [{"t": "2029-12-31T23:50:00Z", "actor": "driver", "kind": "took", "cr": "CR-1"}]
m.feed(Event("project:demo-shop", "project", {"batch": batch, "events": ev}, now))
for width in (121, 140, 141):
    out = io.StringIO()
    screen.plain([m], width, 24, out, View())
    lines = out.getvalue().splitlines()
    top = next(x for x in lines if "Flow " in x)
    left = top.rfind("╭", 0, top.index("Flow "))
    head = next(x for x in lines if " Who " in x and "Event" in x)
    inner = head[left + 2 : top.index("╮", left) - 1]
    print(f"width {width}: left {left}, Who {inner.index('Event') - inner.index('Who') - 1}, Event {len(inner) - inner.index('Event')}")
