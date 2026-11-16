# CR-187 round 1 result

Worktree `C:\Users\gaeta\Projets\chantier.worktrees\batch-12-CR-187`, nothing committed. `just check` passes (45 tests, release notes ok). The long `just scenario` was not run (the Driver's gate); the new scenario checks are written but not run.

## CLI (commands.py, status.py, board.py, cli.py)
- New `batch.json` field `heartbeat_stopped` (None at `open`, read with `.get`).
- `_refresh` returns `(lines, code, prev)`; a wake (`--epoch`) keeps the overwritten heartbeat, clears the stop mark, writes the new one. `status` prints `heartbeat never | N min | stopped`; a wake's own line prints `heartbeat 0 min (N min since the last)` (same `:.0f` rounding), bare `0 min` on the first wake. No-epoch refresh moves nothing.
- Stop recording: `status --stop-heartbeat --epoch <n>` (exit 3 on stale epoch, under the Batch lock, one `heartbeat_stopped` event, no refresh). It requires `--epoch` (usage error without). `pause` also sets the mark.
- STATUS.json (batch view and index) carries `heartbeat_stopped`; `board.py` prints "heartbeat stopped". `hooks/` untouched, no `just mod` needed.
- `cli.py` help of `status`, `--refresh`, `--stop-heartbeat`.

## Cards and docs
chief-of-staff.md ("Your epoch" one rule, "Recovery" names heartbeat stopped), foreman.md (record the stop before ending), hosts/claude-code.md and hosts/copilot.md (Heartbeat sections), status-layout.md, docs/use-cases-direct.md, README.md (line ~444), docs/cr-lifecycle-texts.md (`--epoch <n>` on the loop command). session-start.md needed no change (it already says no epoch on a refresh). No agents/ change, no version bump.

## Scenario (direct_batch, after the `order qa` check)
New checks: never; first wake with no gap and its event; 45 min old `status` ~45; no-epoch refresh leaves heartbeat and prints ~45; wake prints `0 min (44-46 min since the last)` and logs its event; next status `0 min`; stale stop exits 3 with batch.json byte-identical; stop prints `heartbeat stopped`, one event, mark in STATUS.json; no-epoch refresh keeps the stop; next wake clears it. `lost_messages` check unchanged (it only needs a truthy heartbeat). Not done: a separate check that `pause` sets the mark.

## Manual smoke (scratch direct batch, not the scenario)
never; first wake `0 min`; 45 -> `45 min`; no-epoch refresh `45 min`; stale stop refused; wake `0 min (45 min since the last)`; stop -> `stopped`; next wake clears it. All as specified.

## Caveats
- The scenario edit is untested; one risk is the first-wake `status --refresh --epoch 1` running before the chief transcript exists (expect=None used, the line still prints).
- Heartbeat events carry `kind` in `events.jsonl` (the helper counts by `kind`).
