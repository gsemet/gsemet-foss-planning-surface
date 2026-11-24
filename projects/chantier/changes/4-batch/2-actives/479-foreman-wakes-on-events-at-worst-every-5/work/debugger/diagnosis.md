# CR-479 diagnosis: scenario step 13 (surface-board, github)

Reproduction: `just scenario --unit surface-board --forge github` (~14 min); transcript
scenario/results/scenario-20261124-171912-6108.md near lines 29225-29242. Three checks fail, not two:
(0) "on its batch's merge it prints the ... block" got `[]`, then (a), then (b).

## Cause: scenario setup error, not the Foreman's watcher

Step 12 already gave the journal of project `third` a hub `merged@1` line for each of CR-101 (pr 940),
CR-102 (941) and CR-103 (942). Step 13 reuses CR-101 (new PR 944) and CR-103 (new PR 943) and expects the
hub to write a new `merged@1` line for each.

`hub/journal.py` `append` drops any event whose `_key` is already in the journal; the `merged@1` key
(`hub/schemas.py` line 191) is `("merged", batch, cr, bool(landed_with))`: no PR in it. So the hub's
line for (CR-103, 943) is dropped as a duplicate of (CR-103, 942), and likewise (CR-101, 944) of
(CR-101, 940). No line reaches the events topic, the Foreman's watcher (`wf`) has nothing to print,
`block(wf)` waits 60 s and returns `[]`. The watcher itself ran fine: the `foreman watch: running`
line in the same status output and `wf.p.poll() is None` in the transcript show it alive, and its
first check (subscribes, no board started) passed. The Foreman filter (`watch.py` `_lines`,
`foreman_lines`) is not reached. Not a hub-interest problem: the paused batch with CR-101 working on a PR
is followed (`batch_prs.followed_batch`/`to_read`).

(a) `status` prints `forge saw merged: CR-101 .../pull/940`: `journal.lines` (hub/journal.py ~336) lists
the merged line of any open CR of the batch without comparing the PR. CR-101 is open again (working,
pr 944) so step 12's 940 line is listed. The line is the stale step-12 line, a scenario artifact
(CR-103's merge, the point of the check, was recorded; no CR-103 line is shown).

(b) same as (0) for CR-101 / pr 944.

## Fix (scenario only, scenario/run_scenario.py, step 13, ~lines 2822-2870)

1. Give step 13 CRs with no earlier `merged@1` line: simplest is to open step 13 on fresh CRs (a
   fourth and fifth CR filed and added with `order add`, PRs 943 and 944, or a separate project
   `fourth`), instead of re-using `c[0]` and `c[2]`. Remove the `edit("third", c[0]/c[2], ...)`
   re-pointing lines; `base_f` stays the last journal seq.
2. Check (a) (line ~2852): once fresh CRs are used the 940-942 lines belong to merged CRs and are not
   listed, so `not any(x.startswith("forge saw merged") ...)` holds as written. If keeping CR-101,
   narrow it to `c[2]`'s (the CR the Foreman recorded) lines instead.

Alternative (product, not recommended in this CR): add `e.get("pr")` to the `merged@1` key
(`hub/schemas.py` line 191) so a CR that came back with a new PR gets a new line (this matches the
intent of `journal.seen_merged`, which is PR-aware); `journal.lines` would then also need to compare
the PR to drop the 940 line. It is the same on origin/main (steps 1-12 pass there; step 13 does not
exist), so it is out of CR-479's scope.

Proof: code reading (`_key`, `append`, `merged@1` key) and the transcript; I did not rerun the
unit (the task allowed reading). `python -c` could not import (no pydantic outside the uv env).
