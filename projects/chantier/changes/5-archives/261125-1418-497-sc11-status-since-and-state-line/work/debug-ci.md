# CI diagnosis: PR #482, run 45591838006 (`just scenario`)

Head 5d9698265e3f5d9bc001b7a87f3b9c8ed0cf52ae. Verdict: no defect in the code; the new lines are
printed as designed, and the scenario's existing exact-list checks (and the new SC13 check) were not
updated for them. Two independent causes.

## 1. qa-driver: "the line that arrives late changes nothing"

Reproduced locally (Windows):
`uv run --locked python scenario/run_scenario.py --unit qa-driver --verbose` -> FAIL 80/81, same check.

Transcript (`scenario/results/scenario-20261125-111915-40248.md`, line 370):

    $ chantier order done O-1 --epoch 1  -> exit 0
      O-1 already done
      next: nothing due: wait

Cause: SC12 (commit 7f5f9445) routes `order` through `commands/next_lines.py:order` (declare/orders.py),
which appends a `next:` line to `order merged`/`order done` when `--epoch` is given (next_lines.py:55-68).
The check at `scenario/run_scenario.py:11155-11156` compares the whole output:
`w.chantier("order", "done", order, "--epoch", 1)[1] == [f"{order} already done"]`.

Fix (scenario): compare the first line only, or the list with the `next:` line, e.g.
`out[:1] == [f"{order} already done"]` (optionally also check `out[-1].startswith("next: ")`).
(Alternative, a design choice: no `next:` line on a no-op `already done`; the spec decides.)

## 2. surface-board: the 14 watcher checks

Cause: SC11 (commit e8278a9e) makes the steering session's watcher print the batch's `state:` line
just before its last line, both at an end and at each `--stream` telling:
`hub/watch.py:348` (`tell`) and `hub/watch.py:369-370` (end), via `hub/watch_reads.py:70-82`
`steering_state`, which returns the line for the seat's watcher of a batch steered `direct`
(foreman None) or for the Foreman's watcher. Every surface-board world opens its batches with
`--direct` (run_scenario.py:2564, 2567, 2834, 3132, 11699, ...), so every watcher there now ends
`[..., "state: <batch> ...", <cursor/still watching line>]`.

The failing checks compare exact lists that lack it, e.g.
- run_scenario.py:2642-2643 `got == [says(...), cursor(base + 1)]`
- run_scenario.py:2720-2721 (the watcher wakes on the board's line), same shape
- run_scenario.py:11588-11589 `got == ["config changed on the board: ...", cursor(base + 3)]`
- run_scenario.py:2938-2942 (the new SC13 step): `len(got) == 3` for note, blocked, `still watching`;
  the block is now 4 lines with the `state:` line. The `block()` helper (2848) reads up to
  `still watching`.
The other listed failures (two merges within the quiet, checks red, paused batch on the board's
line, version 0 line, first/second/third block, batch's merge block, paused with one PR merged)
are the same exact-list or line-count comparisons on watcher output. No scenario step checks the
watcher's `state:` line (only `status --since` at run_scenario.py:1452).

Not reproduced locally (the unit takes ~7 min on CI, longer than a foreground call here); the cause
is read from the code and the check bodies and matches all 14 names.

Fix (scenario, minimal): drop the `state:` line before comparing watcher output, in the shared
helpers: in `ended()` (run_scenario.py:2514-2523, 11543-11551, and 3792 if its checks are exact)
and `block()` (2848-2855) skip lines that start with `"state: "`, then add one check that the
seat's watcher of a direct batch prints a `state: <batch> ...` line just before its last line
(the SC11 behaviour, otherwise only unit-tested in tests/test_watch_state_line.py). Or update each
expected list to include the `state:` line and the SC13 check to `len(got) == 4`.
