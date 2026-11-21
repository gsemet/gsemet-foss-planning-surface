feat(board): the server watches the planning files; boards and watchers subscribe

## Summary

An open board page made the surface server walk each project's planning folder several times
every 2 seconds (about 0.65 to 1 s of work per pass). The server now learns of a change from the
operating system's file notifications (a check every 5 s where none works), settles 1 s after
the last change, and every read uses the kept state. It reads the forge only while a client is
subscribed. Work in progress (round 1 of 3): the server side; the watcher rework, the cards and
the docs follow in later commits of this PR.

## Deliverables

- Before/after measure of `fingerprint()` calls and CPU over 60 s idle with one page open: to be
  added at the PR's head.
- New board lines: `board: watches the planning files` and `board: no file notifications here;
  checks every 5 s`; options `--stop-idle` and `--forge-always`.

## Blast radius

The surface server's read path, its push loop and the forge hub's cadence. No protocol change.

## Autonomous decisions

- Board write operations settle their project right after writing, so the next read is fresh.

## Known gaps

- The watcher, cards, docs and scenario parts are not in this round.
- No measure yet at the head.

<details><summary>Details</summary>

### Changes

Server side: file watch thread with a settle rule, kept revisions, wake of the push loop,
observed-only forge reads, idle stop, hub line forms, writer start hint.

### Impacts

A change shows about 1 s after the last write.

### Test plan

`just check`, `just eval-dry-run`; new tests for the settle rule, zero walks per pass, the real
notification backend, the check mode, the idle stop and the forge-only-while-observed rule.

### Internal references

CR-429 (fp-cache).

</details>
