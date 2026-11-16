# CR-187 investigation: the heartbeat in direct mode

Round 0. Code read at the worktree's base (74256ab); line numbers below are that base's, they
differ from the spec's (read on 1e99343). Nothing in the repo was changed.

## Reproduction (scratch repo in `%TEMP%\hb187`, outside the repo)

Setup: git repo + bare clone as `origin`, `chantier init`, one CR filed and triaged, then
`CLAUDE_CODE_SESSION_ID=uuid-chief CHANTIER_HOST=claude chantier open <cr> --direct --slots 1
--default-branch main`, `foreman set uuid-chief --epoch 1`. An older heartbeat is set by rewriting
`batch.json` (UTF-8, no BOM; a BOM written by PowerShell `Set-Content -Encoding utf8` makes the CLI
crash with JSONDecodeError, which is a scratch artifact, not a finding).

| Step | Command | batch.json `heartbeat` before -> after | Printed |
|---|---|---|---|
| after `open` + `foreman set` | `status` | null | `heartbeat never` |
| first wake | `status --refresh --epoch 1` | null -> now | `heartbeat 0 min` |
| hb set 170 min ago | `status` | 170 min old, unchanged | `heartbeat 170 min` (true) |
| same | `status --refresh` (no epoch) | unchanged | `heartbeat 170 min` (true age of the last wake, but the session was seen refreshing) |
| same | `status --refresh --epoch 1` | 170 min old -> now | `heartbeat 0 min` (the gap is lost) |
| next | `status` | now | `heartbeat 0 min` |
| hb set 439 min ago | `status` and `status --refresh` | unchanged | `heartbeat 439 min` |
| stale epoch | `status --refresh --epoch 2` | unchanged | error, exit 3 (stale Foreman) |

## Source of each value

- **0**: not a bug of the clock, a design artefact. `_refresh` (commands.py 1293-1315) writes
  `b.data["heartbeat"] = now()` at line 1300 when `epoch is not None`; `status` (1335-1347) then
  re-reads `batch.json` and prints `age_minutes(heartbeat)` at 1340/1347. A wake's own line
  therefore always prints 0, and it hides the gap since the previous wake. Printed 0 is the true age
  of the heartbeat just written; it says nothing of the loop's health.
- **170**: the printed number is the true age of the last `status --refresh --epoch` (reproduced:
  hb 170 min old, `status --refresh` with no epoch leaves it unchanged, prints 170). What misled is
  the other rule: cards tell the steering session to run `status --refresh` with no epoch before a
  report (chief-of-staff.md 27, 311; status-layout.md 11; session-start.md 180), while
  chief-of-staff.md 522-525 ("Your epoch") says to carry `--epoch <n>` on every `status --refresh`.
  A session following the first rule is seen refreshing (STATUS.md rewritten, spend moved) while
  `heartbeat` keeps its age, so "170 min right after a refresh" is exactly the no-epoch refresh. The
  fix is to make the one rule explicit in the cards, plus the wake line's gap. Not reproducible as a
  wrong value in the CLI: the value was true to the old definition.
- **439**: true age of a heartbeat nobody renews. The loop ended (`ScheduleWakeup stop: true`,
  hosts/claude-code.md 48-55; foreman.md 185-193) and the CLI cannot know: no field marks a stopped
  loop, so `status` keeps growing the age (reproduced by setting hb 439 min old: it prints 439,
  no-epoch refresh does not move it). A true value but ambiguous (stopped on purpose or dead).

No other cause found: `heartbeat` has one writer (`_refresh` 1300; `open` sets None at 752), one
CLI reader (`status` 1340), no clock skew (both sides UTC, `age_minutes` state.py 158-162), no
lost write (written under `changes_lock` + `Batch`), no wrong-folder effect in the reproduction. I
could not inspect the real batch-09 `batch.json` (not in this checkout); the three values are
explained by the code and reproduced, not recovered from batch-09's record. `foreman set` and
takeover do not clear the heartbeat (grep: no other write).

## Map: files and entry points

CLI (`skills/chantier/scripts/cli/src/chantier/`):
- `commands.py` `_refresh` 1293 (epoch check at 1298, write 1300-1301; actor "foreman" with
  epoch, "chief-of-staff" without); `status` 1335 (age at 1340, line at 1344-1350); `pause` 2082
  (check_epoch 2089; the natural place for a stop recorded at once); `open` sets `heartbeat: None`
  at 752 (add the new field there).
- `state.py` `check_epoch` 551 (exit 3), `age_minutes` 158, `Batch` context manager (lock + log).
- `status.py` 287 (STATUS.json `heartbeat` field; add the mark next to it) and 415 (index per
  batch); also `board.py` 134 (`heartbeat {_ago(...)}` in the board's facts: would show a growing
  age under a stopped loop; spec says only STATUS.json, but board.py reads `batch['heartbeat']`
  directly: decide, probably print "stopped" there too, cheap).
- `cli.py` 119-127: help of `status` and `--refresh`.
- Hook: `hooks/register.tsx` 617 (`minutesSince(b.heartbeat)`, "Foreman silent"), tests
  `hooks/register.test.tsx` 525-531: out of scope except it gains the mark; touching `hooks/`
  requires `just mod` in the gate record (worker.md Inspector). Avoid touching it.
- Scenario: `direct_batch` run_scenario.py 1167-; `edit(**fields)` at 1187 rewrites batch.json;
  `lost_messages` 3794, the check at 3812 ("a wake ... records the heartbeat") only needs
  `w.batch()["heartbeat"]` truthy: unaffected by the wake line change, but check its out[0].

Cards/docs: chief-of-staff.md 27, 311, 468 ("Recovery"), 522-525; status-layout.md 11-12;
session-start.md 177-180; foreman.md 70, 185-193, 210; hosts/claude-code.md 48-55; hosts/copilot.md
36-44; docs/use-cases-direct.md 88; README.md 444 (direct mode heartbeat) and 483;
docs/cr-lifecycle-texts.md line 3 (long line holding the loop command; the spec cited 203).

## Smallest change

1. `batch.json`: new field `heartbeat_stopped` (timestamp or None), set to None at `open`.
2. `_refresh`: with epoch, read `prev = b.data.get("heartbeat")` before overwriting, clear the stop
   mark, write the new heartbeat; return the previous value so `status` prints
   `heartbeat 0 min (N min since the last)` when prev exists and `N = whole minutes`, else
   `heartbeat 0 min`. Without epoch: untouched (already true).
3. `status` line: `heartbeat stopped` when the mark is set (and no wake cleared it), else
   `never` / `N min`. The wake's gap must be computed from the value before the write, so `status`
   needs `_refresh`'s result (return `(lines, code, prev)` or keep prev in a module-level value;
   prefer a returned value).
4. Recording the stop: a form on `pause` is cheap but `pause` refuses while CRs are live and the
   idle-wake stop is not a pause; so use an option of `status` (e.g. `status --epoch <n>
   --stop-heartbeat`), under `Batch` (lock), `check_epoch` (exit 3), one `heartbeat_stopped` event;
   also have `pause` set the mark on success (its end already ends the loop). The Driver picks; I
   recommend both, since cards say "right after `pause`, and on an idle wake".
5. `status.py` 287/415: add `heartbeat_stopped` next to `heartbeat`; `board.py` 134: print stopped.
6. `cli.py` help texts; cards and docs as the spec's sections 3 and 4, with the one rule: `--epoch`
   on the loop's wake and on steering commands, never on the refresh before a report.

## Risks

- `status` is read by many scenario checks matching `out[0]` text: a changed heartbeat segment of
  the line (`heartbeat 0 min (N min since the last)`) can break a `startswith`/substring check;
  search the scenario and `tests/` for `heartbeat ` and ` spent ` ordering (the segment sits before
  ` spent `, keep that order).
- Derived values: the 30-minute interval is repeated (foreman.md 159, claude-code.md 51, copilot
  `/every 4m` for Copilot): not changed. `age_minutes` rounding: `:.0f` rounds, spec says whole
  minutes; "within one minute" in the evidence, keep one rounding rule for both the ordinary line
  and the gap.
- A pre-existing `batch.json` has no `heartbeat_stopped`: read with `.get`.
- Copilot `/every` cannot be ended by the Foreman: the stop mark then clears at the next wake,
  which is true (spec).
- Windows/BOM: scenario's `edit()` writes plain UTF-8, fine.

## Questions only the user can answer

None. Board wording for "stopped" (`board.py`, `register.tsx`) is the only soft point: the spec
covers `STATUS.json` only; recommended: `board.py` prints it (CLI side, no `just mod`), the hook
untouched.

## Evidence plan

Kind: CLI behaviour + cards/docs text. Nothing visual; no screenshot.
- Before/after by command output in a scratch direct batch (the table above is the "before"; the
  Verifier reruns the same steps on the branch): the scenario `direct_batch` is the project's
  test environment, run by the Driver via `just scenario` (the Investigator does not run it).
- Verifier must show, each from a command's output plus `batch.json`/`events.jsonl`/`STATUS.json`
  reads, at epoch 1:
  1. hb N min old (N >= 30): `status` prints `heartbeat N min` (within 1 min).
  2. `status --refresh` (no epoch): `heartbeat` field unchanged, still about N.
  3. `status --refresh --epoch 1`: new heartbeat, a `heartbeat` event in `events.jsonl`, line
     `heartbeat 0 min (N min since the last)`; next `status` prints `heartbeat 0 min`.
  4. First wake on a fresh batch: `heartbeat 0 min`, no gap.
  5. Stop recorded with `--epoch 1`: `status` prints `heartbeat stopped`, one event logged,
     `STATUS.json` carries the mark; with a stale epoch: exit 3, `batch.json` byte-identical.
  6. Next `status --refresh --epoch 1` clears the mark, prints the gap line.
  7. `pause` leaves the mark set (if chosen) and `open` starts with it unset.
  8. For each cause above, a scenario check that fails on main and passes on the branch: (a) wake
     line gap (fails on main: prints bare `0 min`), (b) stop mark absent on main (the form does not
     exist, so check 5 fails), (c) the no-epoch refresh leaves `heartbeat` alone (passes on main:
     keep as a regression guard, say so honestly; the 170 fix is the card rule, shown by the diff
     of chief-of-staff.md, not by a CLI failure).
  9. `lost_messages` check at line 3812 still passes.
- `just check` green; `just scenario` green.
- Cannot be shown: the real host loop (`/loop`, `ScheduleWakeup stop: true`) and a real session
  following the card; only the CLI form and the card text. The batch-09 files were not recovered.
- Docs/cards: shown by the diff; the Inspector checks the single `--epoch` rule appears the same in
  chief-of-staff.md (522-525, 27, 311), status-layout.md 11 and the host references.
