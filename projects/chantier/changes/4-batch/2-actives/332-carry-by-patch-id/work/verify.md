Head: 3758c5224caa0161b9b17cb1272c92be4b5f3019

All claims judged at 3758c5224caa0161b9b17cb1272c92be4b5f3019.

1. Unit tests of the carry, carry_at/readers, ship carry and unreadable ref.
   Command: `uv run --no-sync --project . python -m pytest skills/chantier/scripts/cli/tests/test_gate_carry.py skills/chantier/scripts/cli/tests/test_carry_ship.py skills/chantier/scripts/cli/tests/test_cli_units.py -q`
   Output: `31 passed in 17.93s`
2. Scenario unit 12f and the new stack-shape unit (both inside the `gates` unit).
   Command: `uv run --no-sync python scenario/run_scenario.py --unit gates --forge github`
   Output: `ok  gates (github): 115/115 checks, 246.2 s` (carry event keys, `carried:` line, restack of a ready CR, CR-316 shape, `ship --conflict` refused twice with `the rebase resolved a conflict`, commit-after-verdict `the rebase changed the patch`).
3. Direct probe of `carry_check` on a scratch git repo (log: work/verifier-probe.log), git 2.56:
   - identical patch rebased onto a moved base: `None` (carries)
   - whitespace-only change: `the rebase changed the patch`
   - no recorded base: `the pass at 2938387 recorded no base: run the long gate again`
4. PR description (as posted, `gh pr view 290`): matches work/pr-body.md; Summary, Deliverables, Changes match the diff stat (carry.py, crs.py, delivery.py, declare, gate.py, gate_run.py, readers, cards, docs, scenario, tests); Known gaps names the one-time cost and the missing pane screenshot; the mermaid renders; no images. The "sits on none of its base branches" autonomous decision exists at crs.py:188. Test plan boxes are the template's open ones (Driver's to tick).
5. CI at this head: reported green by the Driver (not re-judged here).

VERIFIED

## Description pass at 3758c5224caa0161b9b17cb1272c92be4b5f3019

Head: 3758c5224caa0161b9b17cb1272c92be4b5f3019

- Posted body (`gh pr view 290 -R gsemet/chantier --json body`) equals work/pr-body.md (diff: one trailing blank line only). Template order, fold with blank lines, nothing after `</details>`, Known gaps present, mermaid fenced, no images, no internal reference outside Internal references. Judged at 3758c52.
- Claims hold at 3758c52: `--conflict` (declare/delivery.py:33), `does not carry` lines (carry.py:105), `sits on none of its base branches` (crs.py:188), Carried step (status/steps.py:36); diff files match the Changes list (small extras: driver.py, records.py `base` field, SCORECARD C7 row, covered by readers and base-on-events).
- Review box: log shows `r2 approved at c103c07, committed as 46a1797`; carried over clean rebase to 3758c52 (rebase note in log). CI: `gh pr checks 290` all 5 pass.

VERIFIED
