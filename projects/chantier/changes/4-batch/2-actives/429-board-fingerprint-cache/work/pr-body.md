feat(board): the server watches the planning files; boards and watchers subscribe

## Summary

An open board page made the surface server walk each project's planning folder several times
every 2 seconds. The server now learns of a change from the operating system's file
notifications (inotify, FSEvents, ReadDirectoryChangesW), or checks every 5 s where none works,
publishes 1 s after the last change, and every read uses the kept state. It reads the forge only
while a client (a board page, a session's watcher, `chantier live`) is subscribed. A session's
watcher no longer reads the journal or acts as the forge hub: it subscribes to the server's
`events` topic and starts the board, detached, when none runs and its session holds the seat.

## Deliverables

One page open on the live surface (four projects), 60 s, measured at the base and at the head
(base `7c1d890`, head `f90c6a3`):

| | base | head |
|---|---|---|
| fingerprint walks | 70 | 4 (one per real change) |
| time in walks | 37.7 s | 2.1 s |
| process CPU | 63.8% of a core | 7.9% of a core |

New board lines: `board: watches the planning files`, `board: no file notifications here;
checks every 5 s`; new options `board --stop-idle` (the watcher's board stops 30 min after its
last client) and `board --forge-always` (a host that cannot run the watcher keeps the forge read
every 20 s). The watcher ends by itself 2 h after its start with no event.

## Blast radius

Grade 2: the surface server's read path, push loop and forge cadence, the watcher's whole
working, and the cards that describe them. No protocol change (still 1), no web client change.

## Autonomous decisions

- Board write operations settle their project right after writing, so the next read is fresh.
- The watcher prints the finished sentence the server sends in each event's `text`.
- A board a watcher starts from a code clone looked up its project by bare name and died on a
  surface with several projects; fixed with a test.

## Known gaps

- Windows: that a watcher-started board's writer pushes with no console window appearing is
  unproved until `chantier gate` runs there with the user at the screen.
- Host trials (the board outliving the watcher on Claude Code and Copilot) are unproved; the
  host cards say how to run them.
- On a network share or a WSL `/mnt` folder the system may send no notification; documented.
- `just test` runs above the stated time budget on a loaded machine; not measured on a quiet one.

<details><summary>Details</summary>

### Changes

- Server: a file-watch thread with a settle rule (1 s quiet, 5 s at most), kept revisions, push
  loop woken on settle, forge reads only while observed, idle stop, hub line forms.
- Watcher: subscribes through the shared link, seat rule when no server runs, detached start,
  the board's lines passed on, the 2 h idle end.
- Cards, AGENTS.md, CONTRIBUTING.md, docs and the scenario rewritten to the new model.

### Human decisions

Notifications over scans, check every 5 s only where none works; 1 s settle; one question
covers the watcher and the board; a watcher-started board stops after 30 min with no client;
a board started by hand keeps no idle stop; a host with no watcher keeps the 20 s forge read;
the watcher ends after 2 h with no event.

### Impacts

A change shows about 1 s after the last write (up to 5 s in the check mode). An idle board
reads no forge.

### Test plan

- [x] `just check` at 15ca278
- [x] `just eval-dry-run` at 15ca278
- [x] new tests at 15ca278: settle rule, zero walks per pass, real notification backend, check
  mode, idle stop, forge only while observed, watcher seat/server matrix, idle end, state
  entries kept across a transient read error
- [x] Review: approved at f90c6a3, the same patch rebased onto the base as 15ca278
- [ ] Verified at the PR's head (to record)
- [ ] CI green at the PR's head, `just scenario (ubuntu-latest)` included (to record)
- [ ] `chantier gate` on Windows

### Internal references

CR-429 (fp-cache), after CR-426.

</details>
