# Measure: time the spend refresh adds to a round

Head 6dbb81d, Windows 11, worktree code (`refresh_spend` = `cost_rows` + `record_costs` + record write, the path of `status --refresh` and the budget checks).

Set measured: batch-18's own record (copy) and its Foreman transcript 446cff2e (13.4 MB main file) with its subagent transcripts: see counts below. Larger than the real-foreman run 2 eval (2 sessions, 47 jsonl files, 21 MB; that eval's batch record is archived, not runnable). Work done on a copy of `.agents/changes` in a scratch git folder; nothing written to the live batch.

Command (3 runs, each a fresh process; time is `refresh_spend` only, not interpreter start):
`CHANTIER_ROOT=<scratch> uv run --no-sync --project <worktree> python -I measure.py <scratch>`

Runs: 1.45 s, 1.37 s, 1.50 s. Median 1.45 s.
