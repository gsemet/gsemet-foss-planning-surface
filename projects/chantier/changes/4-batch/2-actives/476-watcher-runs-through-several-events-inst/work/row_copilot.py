import sys
from pathlib import Path
p = Path(sys.argv[1])
t = p.read_bytes().decode("utf-8")
subs = [
    ("as is (the CLI prints no `--stream` on this host: the watcher ends after each block of events and is started again from its last line); its end",
     "as is (no `--stream` here: it ends after each block, started again from its last line); its end"),
    ("wakes the watcher like a merge: unproved until a session sees a save end the watcher and start a turn; trial:",
     "wakes the watcher like a merge: unproved; trial:"),
    ("nothing told to the user; it comes only while no batch is in flight (none running, none paused with a PR the record holds neither merged nor cancelled), 2 h after the latest of the watcher's start, its last event and the last moment a batch was in flight.",
     "nothing told to the user; it comes only with no batch in flight."),
    ("which is not a background task of the session: unproved that it outlives the watcher and that the host does not see it as a background task;",
     "no background task of the session: unproved that it outlives the watcher and that the host does not see it as one;"),
]
for a, b in subs:
    assert t.count(a) == 1, a
    t = t.replace(a, b)
p.write_bytes(t.encode("utf-8"))
