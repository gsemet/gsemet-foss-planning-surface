"""CR-429's measure: fingerprint() calls and CPU of a served board with one page open, idle.

Builds the board's push loop in this process (no socket, no forge hub, no writer: nothing is
written anywhere), on the planning surface of the working folder, subscribes the four topics of
one page (`board`, then `project`, `costs` and `prs` of one project), and lets it run idle for the
given seconds. The forge connectors are stubbed to fail at once (no `gh` call, no network, no
journal line), so the `prs` topic costs only its own reading.

Usage, from the surface's root:
  python fp_measure.py --src <the CLI's src folder> --project chantier --seconds 60
The same script runs on the base (a `git archive` of its src) and on the head: at the head it also
starts the file watch, as the board does (`ctx.settle` per project, then `FileWatchThread`).
"""

from __future__ import annotations

import argparse
import json
import sys
import threading
import time

parser = argparse.ArgumentParser()
parser.add_argument("--src", required=True)
parser.add_argument("--project", required=True)
parser.add_argument("--seconds", type=float, default=60.0)
args = parser.parse_args()
sys.path.insert(0, args.src)

import chantier  # noqa: E402
import chantier.board.fingerprint as fp_module  # noqa: E402
from chantier.board.api.push import PushLoop, PushThread  # noqa: E402
from chantier.board.context import Context  # noqa: E402
from chantier.board.projects import open_projects  # noqa: E402
from chantier.board.seats import Seats  # noqa: E402
from chantier.core.errors import ChantierError  # noqa: E402

calls = {"n": 0, "s": 0.0}
lock = threading.Lock()
real = fp_module.fingerprint


def counted(*a, **k):
    began = time.perf_counter()
    try:
        return real(*a, **k)
    finally:
        with lock:
            calls["n"] += 1
            calls["s"] += time.perf_counter() - began


for name in ("chantier.board.context", "chantier.board.reads", "chantier.board.fingerprint"):
    __import__(name)
    mod = sys.modules[name]
    if getattr(mod, "fingerprint", None) is real:
        mod.fingerprint = counted


import chantier.board.api.topics as topics_module  # noqa: E402

reads: dict[str, list[float]] = {}
real_read = topics_module.read


def timed_read(ctx_, topic, *a, **k):
    began = time.perf_counter()
    try:
        return real_read(ctx_, topic, *a, **k)
    finally:
        with lock:
            reads.setdefault(topic, []).append(time.perf_counter() - began)


topics_module.read = timed_read


def no_forge(program, call):
    raise ChantierError(f"{program}: stubbed by the measure", 3)


for name in ("chantier.connectors.github", "chantier.connectors.gitlab"):
    __import__(name)
    sys.modules[name].run = no_forge


import chantier.board.costs as live_costs  # noqa: E402

# the live cost (the 5-minute rule: a page looking at a running batch parses the session
# transcripts once, about 30 s of CPU here, the same at the base and the head) is not the board's
# reading of the planning files: a constant figure in both runs
live_costs.compute = lambda _repo: {"spent_usd": 0.0, "unpriced": {}, "per_cr": {},
                                    "receipt": None, "at": "2026-11-21T00:00:00Z", "error": None}


class NoKey:
    def current(self) -> str:
        return "measure"


projects = open_projects()
ctx = Context(projects, NoKey(), Seats(projects), chantier.__version__, lambda: None, None)
ctx.push = PushLoop(ctx)
files = None
changed: list[str] = []
settles: list[str] = []
mode = "none (the base: a fingerprint per topic read, every 2 s pass)"
if hasattr(ctx, "settle"):  # the head: each project's first fingerprint, then the file watch
    from chantier.board.watch_files import FileWatchThread

    for project in projects.all():
        ctx.settle(project)
    files = FileWatchThread(ctx, None)
    real_feed = files.feed
    real_tick = files.tick

    def fed(paths, now):
        paths = list(paths)
        changed.extend(paths)
        return real_feed(paths, now)

    def ticked(now):
        done = real_tick(now)
        settles.extend(done)
        return done

    files.feed = fed
    files.tick = ticked
    mode = files.start()
events = {"n": 0}


def sink(_event) -> None:
    events["n"] += 1


for topic, topic_args in (
    ("board", {}),
    ("project", {"project": args.project}),
    ("costs", {"project": args.project}),
    ("prs", {"project": args.project}),
):
    got = ctx.push.subscribe(topic, topic_args, sink)
    assert not hasattr(got, "status") or getattr(got, "status", 200) == 200, (topic, got)
startup = dict(calls)
push = PushThread(ctx.push, lambda: None)
cpu0, wall0 = time.process_time(), time.monotonic()
push.start()
end = wall0 + args.seconds
while time.monotonic() < end:
    threading.Event().wait(min(1.0, end - time.monotonic()))
cpu, wall = time.process_time() - cpu0, time.monotonic() - wall0
import psutil  # noqa: E402

names = {t.native_id: t.name for t in threading.enumerate()}
per_thread = sorted(
    ((names.get(t.id, f"native-{t.id}"), round(t.user_time + t.system_time, 2))
     for t in psutil.Process().threads()),
    key=lambda x: -x[1],
)[:8]
push.stop()
if files is not None:
    files.stop()
idle = {"n": calls["n"] - startup["n"], "s": calls["s"] - startup["s"]}
print(
    json.dumps(
        {
            "src": args.src,
            "version": chantier.__version__,
            "projects": [p.id for p in projects.all()],
            "file_watch": mode,
            "seconds": round(wall, 1),
            "startup_fingerprints": startup["n"],
            "startup_fingerprint_s": round(startup["s"], 3),
            "idle_fingerprints": idle["n"],
            "idle_fingerprint_s": round(idle["s"], 3),
            "per_fingerprint_ms": round(1000 * idle["s"] / idle["n"], 1) if idle["n"] else None,
            "idle_cpu_s": round(cpu, 3),
            "idle_cpu_percent_of_one_core": round(100 * cpu / wall, 2),
            "events_after_first": events["n"] - 4,
            "cpu_by_thread_since_start": per_thread,
            "topic_reads":{t: [len(v), round(sum(v), 2)] for t, v in sorted(reads.items())},
            "settles": settles,
            "changed_paths": len(changed),
            "changed_sample": sorted({c.replace("\\", "/").split("/changes/", 1)[-1] for c in changed})[:40],
        },
        indent=2,
    )
)
