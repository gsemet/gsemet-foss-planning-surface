## Summary

On a paused batch, `chantier cost` and `chantier status` without `--batch` answered `no running batch: run chantier open first`, which sends the user to open a new batch when `--batch <name>` was all that was missing. And `chantier board` on a port already in use failed with a bare OS error (`[WinError 10048] ...`) that names neither the port nor the way out.

Now the commands that only read the batch use the only paused batch by themselves; every other command refuses naming the paused batch and `--batch`; and a held board port is named, with what holds it when chantier can tell, and the way out.

## Deliverables

Before and after, on a project whose only batch is paused:

| Command, no `--batch` | Before | After |
| --- | --- | --- |
| `cost` (all forms), `status` | `no running batch: run chantier open first` | reads the paused batch |
| `status --refresh`, `asks`, `take`, `pause`, ... | `no running batch: run chantier open first` | `no running batch; paused: batch-18: pass --batch batch-18` (several: `paused: a, b: pass --batch <name>`), last-closed note kept |

A held board port (one line on stderr, exit 4, prefix `board not started: ` kept):

- a chantier board over another folder behind the same key: `port 8765 on 0.0.0.0 is held by a chantier board over <folder>: open <link>, or pass --port <n> (0: any free port)`;
- a chantier board behind another key (its `401`): `... is held by another chantier board (another project's key; its session printed its link): pass --port <n> ...`;
- anything else: `... is in use (a board may already run there, or another program): pass --port <n> ...`;
- when the port came from `board.port` in `chantier.yaml`, the way out also says `or change board.port in chantier.yaml`.

Choice: a command that writes the batch never picks a paused one silently, since some of them would set it running again.

## Blast radius

Grade: 1. Only refusal texts and the batch lookup of two reading commands change; a `git revert` restores the previous behaviour.

## Autonomous decisions

- `address.probe` returns `"another-key"` for a `401` carrying the board's key-needed text, to tell a board behind another key from any other program.

## Known gaps

- The local `just scenario` run before the rebase passed every check but exceeded its time limits on the stack (483 s) and series-deps (280 s) runs, on a loaded machine; the pipeline's `just scenario (ubuntu-latest)` job is the long gate.

<details>
<summary>Details</summary>

## Changes

- `core/batch.py`, `core/repo.py`: `resolve_batch(repo, batch, paused=False)` and `Repo.paused_batches()`; with `paused=True` and one paused batch it is returned, else the refusal names the paused batches.
- `commands/cost/command.py`, `commands/batch_status.py`: opt in (`status` only without `--refresh` and `--stop-heartbeat`).
- `board/address.py`, `board/command.py`: address-in-use (POSIX and Windows 10048) gives the held-port line above.
- `docs/use-cases.md`, `docs/web-board.md`: updated.
- Tests in `test_rail_refusals.py` and `test_board.py`; scenario section 9 and the held-port check extended.

## Impacts

No visual change. Texts of two refusals change; exit codes are unchanged.

## Test plan

- [x] New or changed tests (they fail on the previous code)
- [ ] Local gates at `6114491` (run before a clean rebase onto main): `just check` (200 tests) passed; `just scenario` locally passed every check (time limits exceeded, see Known gaps)
- [ ] Evidence at `6114491`: scenario section 9 and the held-port check
- [x] Review: approved at `9d4136c` (reviewed state, committed as `6114491`)
- [x] Verified at `6114491`
- [x] CI green at `6114491`: all five checks pass, `just scenario (ubuntu-latest)` included

## Internal references

CR-278 paused-batch-messages.

</details>
