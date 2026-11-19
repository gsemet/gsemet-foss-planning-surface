## Summary

`chantier board` and the forge hub become one elected process, the surface server, per planning surface and machine. It runs the board's pages, the forge hub loop and the journal writes, and holds `chantier/hub.lock`. One state file, `chantier/server.json`, replaces `board.json` and `hub.json`. This is a foundation: it adds no index, API, notification or new wake.

## Deliverables

- One process instead of two, one state file instead of two (`server.json` with `key`, `server` and `hub` entries, written under `server.json.lock`).
- `chantier status` names which process is the hub: `forge hub: PID <n>, the surface server, ...` or `..., a watcher, ...`.
- The board's start question now also names the forge reads.
- A watcher yields the hub to a live server and elects again when the server is gone.
- No screenshot: no UI change. The three forms of the `status` line:

```text
forge hub: none running
forge hub: PID 4242, the surface server, last read 12:00:20
forge hub: PID 5151, a watcher, last read 12:00:20
```

## Blast radius

Grade 2 (moderate): it touches how the board, the hub and the watchers start and elect, on every machine that runs them. Rollback: revert the PR; a leftover `server.json` is ignored by the older version, and its own `board.json` is recreated at its next start.

The CLI's board, hub and watcher modules, the board/forge-hub text of AGENTS.md and CONTRIBUTING.md, the board and watcher cards, the scenario. An older board still running at upgrade is found through the migrated `server` entry and a second board is refused as today.

## Autonomous decisions

- The new state module is `hub/state.py`.
- The hub thread runs inside the board's start function; if it dies the server stops with an error line.
- The `surface-board` scenario budget was raised from 300 s to 500 s.

## Known gaps

- Real run on the user's Windows machine (server up, second board, real forge merge wake, hard kill and takeover): not done yet.
- Linux and macOS are covered by CI only.
- The surface-board scenario checks that no second hub reads the forge by counting reads in a 6 s window (5 to 7 allowed with 1 s cycles); on a heavily loaded runner that bound could be flaky. It passed in CI at 0158783 (carried from e0f6e1f).

<details><summary>Details</summary>

## Changes

- `hub/state.py` (new): `server.json`, locked per-entry writes, liveness, migration.
- `board/` and `hub/` modules read and write through it; `hub/watch.py` elects only while no live server is named and yields to one.
- `hub/lines.py`: the `forge hub:` line forms.
- Tests, scenario, AGENTS.md, CONTRIBUTING.md, `docs/web-board.md`, `session-start.md`.

## Human decisions

- One process runs the board and the forge hub; there is no board without the hub, and the board's start question names the forge reads.
- A watcher that is the hub yields to a live server and elects again when none is left.
- No index, API or new wake in this change.
- An upgrade never runs two boards: the move to `server.json` carries the old board record over with the key, so a second board is still refused with the stop command.
- The planning-folder read module is not part of this change: it ships apart, so the election and the read refactor stay separate.

## Impacts

The git folder's `chantier/` holds `server.json`, `server.json.lock`, `hub.lock` and the watchers' locks.

## Test plan

- [x] New or changed tests (they fail on the previous code): state, election, yield, hub thread, status line, migration (125 passed across the board, hub and scenario-coverage test files at 0158783 (carried from e0f6e1f))
- [x] Local gates at 0158783 (carried from e0f6e1f): `just check` pass; `just eval-dry-run` pass (18 of 18)
- [x] Evidence: no screenshot (no UI change); the `status` line forms are in Deliverables
- [x] Review: approved at 0158783 (carried from f9fb169)
- [x] Verified at 0158783 (carried from e0f6e1f)
- [x] CI green at 0158783: `gh pr checks 354`, five jobs including `just scenario (ubuntu-latest)`
- [x] Long gate at 0158783: `chantier gate CR-386` (`just scenario`, local, Windows) pass, log `work/gates/20261119-101536.log`

## Internal references

CR-386 (batch-28), after CR-385. Verifier note: `work/verify.md` (in the planning folder, not in the PR).

</details>


🤖 Generated with [Claude Code](https://claude.com/claude-code)
