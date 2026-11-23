## Summary

`session-start.md` was read whole at each session start by the router, the Chief of Staff and the Griller, although most of it concerned one role or one moment. It is now split: the common file keeps what chooses and changes the role, and each role reads only its own file when it needs it. The startup cards also speak of "a forge" instead of naming `gh` and `glab`.

## Deliverables

Before and after, in LF bytes:

| File | Before | After |
| --- | --- | --- |
| `session-start.md` | 29 428 | 12 270 |
| `session-start-chief-of-staff.md` (new) | - | 10 925 |
| `session-start-griller.md` (new) | - | 571 |
| `titles.md` (new) | - | 2 660 |
| `sync-checkout.md` (new) | - | 4 801 |
| `forges/github.md`, `forges/gitlab.md` (new) | - | 739, 744 |

Startup / reload bytes per role (limit 12 544), Claude Code: chief-of-staff 11 623 / 12 515 -> 11 636 / 12 527; griller 11 184 / 12 076 -> 11 197 / 12 088; status 11 390 / 12 282 -> 11 385 / 12 276; router 11 140 / 12 032 -> 11 135 / 12 026; foreman 7 721 / 8 613 -> 7 740 / 8 631. Copilot figures move the same way (all under the limit).

Section 1 of `session-start.md` is byte-identical to the merge base (empty diff from `## 1.` to `## 2.`).

Table of moves (each row checked by `test_session_start_split.py`):

| Instruction (from) | Now in | Read when, by whom |
| --- | --- | --- |
| section 2 "The board." paragraph, board question alone on a host without watcher, stale-build paragraph, board lines, `serve --seat` keeps `--project` | `session-start-chief-of-staff.md`, The board | Chief of Staff, session start (common header); `chief-of-staff` and `board` actions |
| section 2 "The watcher." and its lines, "When it starts and stops" | same, The watcher | same |
| section 2 "Stopping the board by hand", "A reload starts nothing" | same, Stopping the board by hand | same |
| section 2 a Griller never starts the board or the watcher | `session-start-griller.md` (and one line in common section 2) | Griller, session start (common header) |
| section 3 titles, whole, Foreman row included | `titles.md` | Chief of Staff and Griller, session start; `chief-of-staff` action |
| section 6 sync, six steps | `sync-checkout.md` | the syncing session, before its first sync (`sync` action) |
| sections 2 and 4 `gh`, `glab` | `forges/github.md`, `forges/gitlab.md` | by link, when the forge's tool matters |

Kept in common section 2: the seat and its table, the role-change paragraph and the rule "read the file of the role the seat gives you, again when the role changes", "Re-read the seat".

## Blast radius

Grade: **2**. Cards and tests only, no CLI code, but every session start reads these files and several cards cite them. Rollback: revert the commit.

## Autonomous decisions

- The manifest, counted in every role's startup, grew with the new action lines; to stay under the limit its `actions` entries were re-indented (4 to 2 spaces) and its `paths` text shortened. The Foreman's startup is therefore 19 bytes larger, not unchanged; its content did not change.
- The Chief of Staff and Griller Startup core sentences point to the role file ("then your role's file there, again when the role changes"); the rule's exact words are in `session-start.md`.

## Known gaps

- The Chief of Staff's independent reading of the split (merge-base file against the new files and the table) is owed on the ready PR, before the merge.

<details>
<summary>Details</summary>

## Changes

- `session-start.md` slimmed; new `session-start-chief-of-staff.md`, `session-start-griller.md`, `titles.md`, `sync-checkout.md`, `forges/github.md`, `forges/gitlab.md`.
- `startup-manifest.json`: `chief-of-staff` and `board` readings, new `sync` action.
- The four skills' launch paragraph points to `sync-checkout.md`; citations in `chief-of-staff.md`, `griller.md`, `concepts.md`, `hosts/`, `CONTRIBUTING.md` and `docs/forge-connectors.md` ("Adding a connector" gains the forge reference step) follow the moves.
- Tests: new `test_session_start_split.py`; `test_launch_modes.py`, `test_command_names.py`, `test_plugin_files.py` updated.

## Impacts

No visual change; sessions read less at start.

## Test plan

- [ ] New or changed tests (they fail on the previous code)
- [ ] Local gates at `<sha7>`: `just check` (2193 passed, 20 skipped)
- [ ] Evidence: no before/after screenshots (cards only)
- [ ] Review: approved at `<sha7>`
- [ ] Verified at `<sha7>`
- [ ] CI green at `<sha7>`

## Internal references

CR-470 slim-session-start

</details>
