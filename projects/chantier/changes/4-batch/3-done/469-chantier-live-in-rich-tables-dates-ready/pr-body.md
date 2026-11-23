## Summary

`chantier live`, the terminal view of a project's batch, looked plain: a monochrome, headerless grid with every time in UTC and no date, so an event of an earlier day looked like a time gap. This PR redraws it with Rich (already a pinned dependency): rounded boxes, tables with headers, the board's state colours, every time in the local zone with its date, a key `t` to show how long ago each event happened, the project's sessions in an Agents box, and a Ready box above Tasks that lists the pull requests ready to review or to merge, each with a clickable number where the terminal allows. `--once` stays plain text.

## Deliverables

One `--once` capture (120 columns, zone Europe/Paris, prepared events; the screen in a terminal adds the colours):

```text
chantier live  /work/demo  v0.15.1  ws  live  2026-11-23 12:26:25 UTC+01:00
working 1  ready 2  held 1  done 0
╭─ Projects ───────────────╮╭─ Flow ───────────────────────────────────────╮╭─ Ready ──────────────────────────────────╮
│ demo  batch-01 running … ││ Time           Who        Event              ││ PR  CR     State          Age Title      │
│   inbox 0 backlog 2      ││ 11-22 18:40:12 chief-of-… open               ││ #13 CR-103 ready to merge 35m Add the a… │
╰──────────────────────────╯│ 11-23 10:02:31 foreman    take CR-101        ││ #12 CR-102 checks running 12m Fix the l… │
╭─ Agents ─────────────────╮│ 11-23 11:51:00 foreman    handback CR-103    │╰──────────────────────────────────────────╯
│ Chief of Staff (seat)  … ││ 11-23 12:14:00 foreman    handback CR-102    │╭─ Tasks ──────────────────────────────────╮
│ Foreman  beat 3 min ago  ││                                              ││ State   Task                             │
│ Driver CR-101 coder r1   ││                                              ││ working CR-101  Export the report as CSV │
╰──────────────────────────╯╰──────────────────────────────────────────────╯╰──────────────────────────────────────────╯
```

Choices:

- Colours are the board's eight state colours, always next to a word, never alone; a test keeps them equal to the web client's `tokens.css`.
- The Flow's time is `MM-DD HH:MM:SS` in the local zone; the header gives the full date and the UTC offset; `t` switches the column to the time since the event.
- Ready's data comes from the server's `prs` topic: `live` calls neither `gh` nor `glab`. The state words (`ready to merge`, `checks running`, `to review`, `draft`, `conflicting`, `checks failing`, `closed`, `merged, not recorded`, `not read`) are the screen's own.
- `--once` prints at its deadline with `not read` in Ready when the forge has not answered.

## Blast radius

Grade: 1. Only the read-only terminal client and its docs change; the server, its API and the web client do not. A `git revert` restores the previous screen.

## Autonomous decisions

- The time and word helpers moved to a new `times.py`, the Ready box to `ready.py` and shared drawing helpers to `parts.py`, to keep each module short.
- The tests share a prepared state in `tests/live_world.py`.

## Known gaps

- Not yet checked by hand in Windows Terminal (rounded boxes, colours, `t`, a click on a PR number).
- The local Windows run of the long gate was not made (port 8765 is held by another program here); the pipeline's scenario job is green at the head.
- The `docs/boards.md` capture is drawn from prepared events, not from a real server.
- In the narrow right column the Ready title is cut when the state word is long (`merged, not recorded`).

<details>
<summary>Details</summary>

## Changes

- `clients/tui/model.py`, `times.py`: local zone, `since`, Agents list, `prs` subscription per batch, `pending_prs`.
- `clients/tui/screen.py`, `parts.py`, `ready.py`: rounded panels, tables, colours, Ready box and OSC 8 link.
- `clients/tui/view.py`: the `t` key, help line and footer.
- `commands/live.py`: `--once` height for four boxes; waits for `prs` and prints `not read` at the deadline.
- `docs/boards.md`, `docs/server-api.md`, `scenario/README.md`.
- `scenario/run_scenario.py`: `live_once` reads the Tasks row by its State word first, then the CR id.

## Human decisions

- Agents lists the project's sessions (seat holder, Foreman, Drivers); the seat line claims nothing about whether that session runs; QA drivers are left out.
- Times are in the user's local zone with the UTC offset in the header; Flow lines use the short `MM-DD HH:MM:SS` form.
- Ready comes from the server's published API; Tasks loses its to-review section, whose age moves to Ready.
- `--once` prints at the deadline when only the forge has not answered.

## Impacts

The terminal screen is redrawn as shown above; no other behaviour changes.

## Test plan

- [ ] New or changed tests (`test_live_model.py`, `test_live_ready.py`, `test_live_link.py`)
- [x] Local gates: `just check` passed at 56385da; the local long gate was not run (port 8765 is held by another program on the author's machine), the pipeline's `just scenario (ubuntu-latest)` is green at 56385da
- [x] Evidence: capture in `docs/boards.md`
- [x] Review: approved at 56385da
- [x] Verified at 56385da
- [x] CI green at 56385da: `just check` (ubuntu, macos, windows), `just eval-dry-run`, `just scenario`

## Internal references

- CR-469 live-rich

</details>
