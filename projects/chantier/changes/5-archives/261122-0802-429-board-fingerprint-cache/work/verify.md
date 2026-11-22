# Verify CR-429

Head: 5afaae4de0977060dfb7fc1443bd90ba91ae03c2

## Claims of the specification (judged at 5afaae4)

- Settle rule (1 s quiet, 5 s at most, one walk per settle), zero walks per push pass, real
  notification backend, check mode (5 s), idle stop (30 min, writer's last cycle first), forge only
  while observed (`--forge-always` keeps it), watcher seat/server matrix, detached start, lost link
  reopened, idle end (2 h, `IDLE_END_S = 7200.0` in hub/times.py), state entries kept across a read error.
  Command, at 5afaae4, worktree:
  `uv run --locked --group dev pytest -q -n 4 tests/test_file_watch.py test_board_idle.py test_watch_board.py test_state_lost_update.py test_surface_server.py test_forge_hub.py test_live_link.py test_board_prs.py test_watch_events.py test_watcher_autostart.py test_board_exposure.py`
  Output: `188 passed in 77.25s`. The tests named after each claim exist (test_file_watch.py: settle times,
  settle once, zero walks per pass, notification backend, check mode; test_board_idle.py: idle stop,
  forge observed / always, start lines; test_watch_board.py: seat rule, detached start, lost link, idle end).
  PASS.
- Carried-from-15ca278 judgment. `git range-diff e5dc6952 15ca278 HEAD`: commits 1, 2 and 4 (all code) are `=`
  (exact same patch, rebased from e417190 onto e5dc6952); commit 3 (docs/scenario) differs only by rebase context
  and the scenario cli_form/restart step; two new commits touch only `scenario/run_scenario.py` (events frames kept
  while waiting a move result; plugin-mode `cli_form`). The base moved (store reads, many files), so the proofs that
  run code were run again at 5afaae4 (above), not carried. The scenario edits are proved only by the pipeline's
  `just scenario (ubuntu-latest)`, still pending at this check (`gh pr checks 414`: scenario pending; check ubuntu
  pass, eval-dry-run ubuntu pass; macOS, Windows pending). Not judged here (no local scenario by order).
  Local `just check` at 5afaae4: Driver's log work/gates/check-r5.log (1693 passed); not rerun by me.

## Description claims (PR 414, as posted, at 5afaae4)

- FAIL, consistency: "Base: ... four commits directly on `e417190`". At the head the branch is six commits on
  `e5dc6952` (`git log --oneline e5dc6952..HEAD | wc -l` = 6; `git merge-base HEAD origin/main` = e5dc6952).
- FAIL, SHA: the Test plan's `just check`, `just eval-dry-run`, new tests and Review box name `15ca278`, not in the
  head's history (the CLI's `ship` listed them as `off`), with no "carried from" reason; the head's own Inspector
  approval (note of 07:33:57, at 5afaae4) and the passes at 5afaae4 are not what the box cites.
- FAIL, proof: the Deliverables table (70 -> 4 walks, 37.7 s -> 2.1 s, 63.8% -> 7.9%) names no SHA. Its source,
  evidence/fp-cache-measure.md, was measured at `c9c0852` plus an uncommitted tree, base `7c1d890`; neither is this
  head or a carry with a reason. I did not re-run it against the live planning surface.
- Known gaps lists the Windows `chantier gate` and host trials; the pipeline's long gate at the head is not green yet.

## Description pass 2 (PR 414 body re-read, at 5afaae4de0977060dfb7fc1443bd90ba91ae03c2)

Command: `gh pr view 414 -R gsemet/chantier --json body -q .body`; SHA checks `git merge-base --is-ancestor <sha> HEAD`.
- Base sentence FIXED: "six commits directly on `e5dc6952`"; `git rev-list --count e5dc6952..HEAD` = 6, `git merge-base origin/main HEAD` = e5dc6952 (in history).
- Test plan SHAs FIXED: `just check`, `just eval-dry-run`, tests and Verified boxes name 5afaae4 (in history); Review box names no SHA outside history and says it was approved before the rebase, with the range-diff reason; the Inspector note at 5afaae4 (07:33:57Z) exists in `chantier log`.
- Deliverables measurement FIXED: names c9c0852 plus an uncommitted tree on base 7c1d890, stated as "not re-run at 5afaae4" with the reason (rebase and two scenario-only commits). Both SHAs exist as objects but are not in the head's history (pre-rebase); they appear only as a carry source with its reason, which the card allows. Noted, not a failure.
- Known gaps names the Windows gate, host trials and the unchecked CI/gate boxes stay unchecked. Renders as clean sections and fold; no image. Role names: none outside Internal references.
- Pending CI (Windows check, scenario) is not a description failure; its boxes are unchecked.

## Verdict

VERIFIED (description pass 2 at 5afaae4; code claims above hold at 5afaae4).
