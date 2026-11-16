# CR-173 investigation (investigator's report, saved by the Driver: the worker's Write was refused by the guard)

Verdict: the CLI prints the true age of the timestamp batch.json holds, every time (UTC both sides: state.py now() 125, age_minutes 158). No wrong checkout/session, lost write or clock found. What feeds the value is wrong.

## Reproductions (scratch repo, `open --direct`, `foreman set uuid-chief --epoch 1`, heartbeat edited in batch.json)

| Value | Command | batch.json heartbeat | True age of last `status --refresh --epoch`? |
|---|---|---|---|
| never | `status` right after open | null | n/a |
| 0 | `status --refresh --epoch 1` | written by the same call (commands.py 1148) before it reads (1186) | true but trivial: the wake's own line always says 0, the gap to the previous wake is lost |
| 170 | `status` or `status --refresh` (no epoch), heartbeat set 170 min back | unchanged | true; an epochless refresh moves nothing |
| 439 | same, set 439 min back | unchanged | true; nothing records that the loop ended |

`status --refresh --epoch 1` over a 170-min-old heartbeat overwrote it and printed "heartbeat 0 min". `--epoch 0` (stale) exits 3, heartbeat unchanged (check_epoch runs before the write, in the lock).

## Sources
- 0: the wake's own line reads the heartbeat it just wrote.
- 170: two rules for one session. chief-of-staff.md 26 and 286, status-layout.md 11, session-start.md 163 make the Chief of Staff refresh with no epoch before a report; chief-of-staff.md 485-488 say `--epoch <n>` on every refresh. Mechanism proven; which refresh batch-09 ran is not in the files.
- 439: a loop ended on purpose (`ScheduleWakeup stop: true`, claude-code.md 48-53), no mark in the batch.

## Code map (paths under skills/chantier/scripts/cli/src/chantier/)
- commands.py `_refresh` 1140-1166: writes heartbeat 1147-1149; previous value is `b.data.get("heartbeat")` just before 1148; must hand it back to `status` for the gap. Clear the stop mark here when epoch is not None.
- commands.py `status` 1181-1196: only reader (1193). Add "stopped" and the gap.
- `open_batch` commands.py:665 sets heartbeat None; add the stop field (read with .get for old batches).
- `pause` commands.py 1880-1914 (epoch=True, cli.py 186): set the mark near 1912 in the same lock. An idle-wake stop needs a form on `status` (e.g. `--stop`, requires `--epoch`; check_epoch returns on None so refuse a missing epoch). cli.py 105-112 help texts.
- status.py:281 (STATUS.json) and 405 (index row): carry the mark. STATUS.json is rewritten only on a Batch write, so the stop command must write it.
- Scenario direct_batch (run_scenario.py 914+): open 959, claim epoch 1 at 987, edit() 934-936; new checks after 987, heartbeat set from the real now (transcripts use fixed 2026-03 dates); `Foreman(w, epoch=1).turn()` at 1001 may already refresh with an epoch. lost_messages 3004-3030, check 3022-3024 should keep passing (gap is a suffix).
- Cards: chief-of-staff.md 26, 286, 435-436, 485-488, 539; status-layout.md 11-12; foreman.md 154-160; hosts/claude-code.md 48-53; hosts/copilot.md 36-44.
- Docs: docs/use-cases-direct.md 88 and 118; README.md 395-406, 442; docs/cr-lifecycle-texts.md: the "/loop" text is on line 3 (one long line), not 203.
- No change in agents/ or com.github.copilot/agents/.

## Evidence plan (Verifier)
1. `just check`. 2. `just scenario` with new direct_batch checks, each also shown failing on main: N>=30 min reading; epochless refresh leaves heartbeat unchanged; wake line "heartbeat 0 min (N min since the last)" + event + following status "0 min"; first wake no gap; stop with --epoch 1 (status form and pause) prints "heartbeat stopped", event logged, STATUS.json and index carry the mark; stale epoch exit 3 and batch.json unchanged; next epoch refresh clears the mark and prints gap; epochless refresh does not clear; lost_messages still passes. 3. Hand reproduction in a scratch repo on main and branch. 4. git diff --stat: nothing in agents/, no version bump. 5. Grep cards/docs for --epoch on wakes only and "heartbeat stopped" in foreman.md, both host refs, chief-of-staff.md 435. 6. PR: draft, first line exactly `**Eval run: do not merge.** The maintainer decides what happens to this PR.`, not merged.
