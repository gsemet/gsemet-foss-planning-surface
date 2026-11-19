# Diagnosis: `empty_batch` leg, "`status` says `spent none yet` ... never $0.00"

## Verdict
The check is wrong. The CLI's status output for the empty batch is right.

## Reproduction (local, same as CI, 80/81)
    uv run --locked python scenario/run_scenario.py --unit direct --forge github --keep
Transcript: scenario/results/20261118-195513-41864/direct-github.md (line 1339 on).

## Evidence
`status` printed (the failing check's own detail):

    batch-06 paused steering direct (the Chief of Staff) shape parallel live 0/4 queued 0 foreman none e0 heartbeat stopped spent none yet (paused, cost to date), no CR yet
    no CR yet: `order add --note <folder> --batch batch-06` joins one
    last closed: batch-04, closed 2026-11-18, 0 merged, 1 dropped, $0.00

The first line has `spent none yet` and ends with `no CR yet`: both halves pass. The check fails only on
`not any("$0.00" in ln for ln in out)`, which scans every line of `status`, including the
`last closed: batch-04 ... $0.00` line: an earlier batch of the same scenario world (dropped CR, real cost of $0.00).
That line is unrelated to the empty batch. The `direct` unit runs earlier cases in the same workspace, so a closed
batch is always there to report; the pytest twin (test_open_empty_batch.py line 95) checks the batch line alone and passes.

## Minimal fix
scenario/run_scenario.py, `empty_batch` (around line 5320): restrict the `$0.00` test to the batch's own line, e.g.

    line = next((ln for ln in out if ln.startswith(w.name)), "")
    check(..., code == 0 and "spent none yet" in line and line.endswith("no CR yet") and "$0.00" not in line, str(out))

No CLI change needed.
