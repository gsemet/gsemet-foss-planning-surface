"""The Verifier's probe: the widths read from the drawn text of `screen.plain`, against an oracle
written from the specification's section 2 (a greedy giving-way, not the code's arithmetic).

usage, from the worktree: uv run --no-sync python <this file>
Made-up data only: served `/work/demo`, projects `demo-shop`, `demo-site`."""

import io
import sys
from zoneinfo import ZoneInfo

from chantier.clients.tui import screen
from chantier.clients.tui.link import Event, Linked
from chantier.clients.tui.model import Model
from chantier.clients.tui.view import View

NOW = "2030-01-01T00:00:00Z"
HIGH = 24
LONG = "an event text long enough to fill any width " * 5


def board(ids, label="", ago_old=False):
    m = Model(clock=lambda: 0.0, zone=ZoneInfo("Europe/Paris"), label=label)
    m.feed(Linked("ws", NOW))
    data = {"version": "0.15.1", "served": "/work/demo", "projects": [{"id": i} for i in ids]}
    m.feed(Event("board", "board", data, NOW))
    for i in ids:
        row = {"cr": "CR-1", "title": "Demo change", "state": "working", "phase": "coding",
               "round": 1, "round_limit": 3, "blocked": None, "lease": None}
        when = "2000-01-01T00:00:00Z" if ago_old else "2029-12-31T23:50:00Z"
        events = [{"t": when, "actor": "a-very-long-actor-name-here", "kind": "took", "cr": "CR-1"}]
        batch = {"id": "batch-01", "state": "running", "mode": "batch", "crs": [row],
                 "stack_lease": None}
        m.feed(Event(f"project:{i}", "project", {"batch": batch, "events": events}, NOW))
        lines = [{"seq": 1, "t": when, "source": "hub", "text": LONG}]
        m.feed(Event(f"events:{i}", "events", {"lines": lines}, NOW))
    return m


def models(case, **kw):
    if case == "one":
        return [board(["demo-shop"], **kw)]
    if case == "projects":
        return [board(["demo-shop", "demo-site"], **kw)]
    n = {"boards": 2, "boards4": 4}[case]
    return [board(["demo-shop"], label="abcd"[i], **kw) for i in range(n)]


def draw(ms, width, view):
    out = io.StringIO()
    screen.plain(ms, width, HIGH, out, view)
    return out.getvalue()


def measure(text):
    """(left, project, who, event, time-or-ago, right) from the Flow's box and header row."""
    lines = text.splitlines()
    at, top = next((i, x) for i, x in enumerate(lines) if "Flow " in x and "╭" in x)
    mark = top.index("Flow ")
    left = top.rfind("╭", 0, mark)
    end = top.index("╮", left)
    head = lines[at + 1][left : end + 1]
    inner = head[2:-2]
    assert head.startswith("│ ") and head.endswith(" │"), head
    who, event = inner.index("Who"), inner.index("Event")
    if "Project" in inner:
        project_at = inner.index("Project")
        project, first = who - project_at - 1, project_at - 1
    else:
        project, first = None, who - 1
    right = len(top) - end - 1
    return left, project, event - who - 1, len(inner) - event, first, right


def oracle(case, width, maximized, first_w):
    """Section 2, applied step by step on one column at a time."""
    several = case != "one"
    label = 2 if case.startswith("boards") else 0
    pmin, pmax = 10 + label, 20 + label

    def event(left, p, w, first):
        flow = width if maximized else width - left - 44
        return flow - 4 - first - 1 - ((p + 1) if several else 0) - w - 1

    # the threshold, with the Time column's width (14) in both modes
    fits = (width - 28 - 44 - 4 - 14 - 1 - ((pmin + 1) if several else 0) - 10 - 1) >= 20
    if fits:
        left, p, w = 42, pmax, 15

        def ev_normal(lft, pp, ww):
            return width - lft - 44 - 4 - 14 - 1 - ((pp + 1) if several else 0) - ww - 1

        while ev_normal(left, p, w) < 20 and left > 28:
            left -= 1
        while ev_normal(left, p, w) < 20 and w > 10:
            w -= 1
        while ev_normal(left, p, w) < 20 and several and p > pmin:
            p -= 1
        assert ev_normal(left, p, w) >= 20
    else:
        left = 0
    if maximized or not left:
        # Project first, then Who, each as far as Event keeps 20
        p, w = pmin, 10
        while several and p < pmax and event(0, p + 1, w, 14) >= 20:
            p += 1
        while w < 15 and event(0, p, w + 1, 14) >= 20:
            w += 1
    shown_left = 0 if maximized else left
    return shown_left, (p if several else None), w, event(shown_left, p, w, first_w), left


def tab_cycle(ms, width):
    view, seen = View(), []
    draw(ms, width, view)
    for _ in range(5):
        view.press("tab")
        draw(ms, width, view)
        seen.append(view.active)
    return view.drawn, seen


failures = []
checked = 0
THRESH = {"one": (122, 141), "projects": (133, 162), "boards": (135, 164), "boards4": (135, 164)}
for case, (low, full) in THRESH.items():
    first_left, first_full, prev = None, None, None
    for width in range(40, 231):
        for maximized in (False, True):
            for ago, old in ((False, False), (True, False), (True, True)):
                ms = models(case, ago_old=old)
                view = View()
                view.maximized, view.ago = maximized, ago
                text = draw(ms, width, view)
                head = "Ago" if ago else "Time"
                try:
                    left, p, w, ev, first, right = measure(text)
                except (ValueError, StopIteration, AssertionError):
                    if width >= 60 and (maximized or width >= 100):
                        failures.append((case, width, maximized, ago, "unreadable header"))
                    continue
                if ago:
                    # the `Ago` header sits right-aligned: its width is where it ends
                    row = next(x for x in text.splitlines() if " Ago " in x and "Event" in x)
                    first = row.index("Ago", left) + 3 - (left + 2)
                    if p is not None:
                        p = row.index("Who", left) - row.index("Project", left) - 1
                else:
                    first = 14
                    if p is None:
                        row = next(x for x in text.splitlines() if " Who " in x and "Event" in x)
                        first = row.index("Who", left) - (left + 2) - 1
                e_left, e_p, e_w, e_ev, normal_left = oracle(case, width, maximized, first)
                flow_min = (width if maximized else width - 44) - 4 - 14 - 1 - 10 - 1
                if case != "one":
                    flow_min -= (10 + (2 if case.startswith("boards") else 0)) + 1
                if flow_min < 1:
                    continue  # nothing can give: the terminal is too small, as before
                checked += 1
                got = (left, p, w, ev)
                if got != (e_left, e_p, e_w, e_ev):
                    failures.append((case, width, maximized, head, got, (e_left, e_p, e_w, e_ev)))
                if left and ev < 20:
                    failures.append((case, width, "event under 20 with a left column", ev))
                if not maximized and right != 44 and width >= 100:
                    failures.append((case, width, "right column", right))
                if not maximized:
                    if (" Projects " in text) != bool(left) or (" Agents " in text) != bool(left):
                        failures.append((case, width, "left boxes", left))
                    if left:
                        box = next(x for x in text.splitlines() if "Projects " in x)
                        if box.index("╮") + 1 != left:
                            failures.append((case, width, "Projects box", box.index("╮") + 1, left))
                if not ago and not maximized:
                    if left and first_left is None:
                        first_left = width
                    if (left, p, w) == (42, {"one": None, "projects": 20}.get(case, 22), 15):
                        first_full = first_full or width
                    if prev and prev[0] and left:
                        d = (left - prev[0], (p or 0) - (prev[1] or 0), w - prev[2])
                        if sum(d) > 1 or min(d) < 0:
                            failures.append((case, width, "more than one column per step", d))
                    prev = (left, p, w)
    for width in (low - 1, low, 230):
        drawn, seen = tab_cycle(models(case), width)
        want = (["projects", "agents"] if width >= low else []) + ["flow", "ready", "tasks"]
        if drawn != want or set(seen) != set(want):
            failures.append((case, width, "panels", drawn, seen))
        print(f"{case:9} width {width}: panels {drawn}; Tab x5 from flow: {seen}")
    print(f"{case:9} left column first drawn at {first_left} (spec {low}); "
          f"all defaults from {first_full} (spec {full})")
    if (first_left, first_full) != (low, full):
        failures.append((case, "thresholds", first_left, first_full))

print()
print("case      width mode       left project who event")
for case, widths in (
    ("one", (121, 122, 123, 126, 127, 128, 140, 141, 142, 120, 100)),
    ("projects", (132, 133, 134, 142, 143, 144, 148, 149, 161, 162, 117, 110, 90)),
    ("boards", (134, 135, 136, 145, 146, 150, 151, 163, 164)),
):
    for width in sorted(widths):
        for ago in (False, True):
            view = View()
            view.ago = ago
            left, p, w, ev, *_ = measure(draw(models(case), width, view))
            mode = "t (Ago)" if ago else "Time"
            print(f"{case:9} {width:5} {mode:10} {left:4} {p!s:>7} {w:3} {ev:5}")
for case, width in (("one", 90), ("projects", 90), ("boards", 90), ("projects", 70),
                    ("one", 200), ("projects", 140)):
    view = View()
    view.maximized = True
    left, p, w, ev, *_ = measure(draw(models(case), width, view))
    print(f"{case:9} {width:5} maximized  {left:4} {p!s:>7} {w:3} {ev:5}")

# a resize that drops the left column moves the active panel to the Flow
view, ms = View(), models("one")
draw(ms, 140, view)
view.press("tab")
view.press("tab")
view.press("tab")
view.press("tab")
draw(ms, 140, view)
before = view.active
draw(ms, 121, view)
print(f"\nactive panel at 140: {before}; after redraw at 121: {view.active}, drawn {view.drawn}")
if before not in ("projects", "agents") or view.active != "flow":
    failures.append(("settle", before, view.active))

if len(sys.argv) > 1:
    for case, width in (("one", 121), ("one", 122), ("projects", 133), ("boards", 164)):
        with open(f"{sys.argv[1]}/drawn-{case}-{width}.txt", "w", encoding="utf-8",
                  newline="\n") as f:
            f.write(draw(models(case), width, View()))

print(f"\nscreens checked against the oracle: {checked}; failures: {len(failures)}")
for f in failures[:60]:
    print("FAIL", f)
sys.exit(1 if failures else 0)
