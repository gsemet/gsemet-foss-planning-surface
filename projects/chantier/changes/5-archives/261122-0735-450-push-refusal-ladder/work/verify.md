# Verify CR-450

Head: 6ac8498f81f895eb8238294c269d1c6486df7b52

All claims judged at 6ac8498 (`git rev-parse HEAD` in the worktree; tree clean).

1. Long gate pass at this head. Gate log `work/gates/20261122-044933.log`, first line
   `gate CR-450 branch chantier/batch-30/cr-450-a-refused-push-climbs-foreman-then-chief head 6ac8498f81f895eb8238294c269d1c6486df7b52`;
   last line `result: pass at 6ac8498f81f895eb8238294c269d1c6486df7b52` (`just scenario`).
2. CI at 6ac8498 (`gh pr view 422 --json statusCheckRollup`): just check ubuntu/macos/windows,
   just scenario (ubuntu-latest), just eval-dry-run (ubuntu-latest): all SUCCESS; headRefOid = 6ac8498f.
3. Tests (command: `pytest test_came_back.py test_startup_manifest.py test_cli_runs.py -k "push_ladder or manifest or allow"`):
   `43 passed, 18 deselected` (includes test_the_cards_name_the_push_ladder, the allow-rule and manifest tests).
4. New dry-run case (`python evals/kit/dry_run.py --case foreman-route-push`):
   `ok foreman-route-push: ...` and `dry run: 1 of 1 cases as expected`; case is in the CASES list, dispatch table (dry_run.py:1444) and docstring (line 22).
5. Card edits by grep at the head: `foreman.md:945 ## A Driver's refused force push`; chief-of-staff.md holds 0 occurrences of
   "the local head holds the remote head's work rebased" (moved); driver.md:421 "the steering session does not send it", no
   "Chief of Staff does not send it"; startup-manifest.json:55 holds `foreman.md#A Driver's refused force push` after chief-of-staff.md;
   claude-code.md rows at 267, JSON lines 331-332 and "Every batch" row carry `git -C * push --force-with-lease=chantier/* origin *chantier/*`;
   concepts.md:729 "(or the same with `git -C <checkout>`)"; SCORECARD J11 and J22 carry the ladder and the note exemption.
5b. Diff stat (`git diff --stat main...HEAD`): 17 files, matching sections 1-12 of the spec (allow_samples.py, test_cli_runs.py, test_came_back.py, audit.py, dry_run.py, SCORECARD, docs, copilot.md, routing.md, status-layout.md included); agents/ untouched.
6. Review box: `$CHANTIER log 450` has "r1 approved at e4171908..., committed as 6ac8498f..." matching the box `approved at 6ac8498`.
7. PR description (gh pr view 422): renders (sections, mermaid, details fold); Summary, Deliverables and Changes match the diff stat;
   Known gaps names the two unproved items; no images; Internal references holds only the CR; gates cited at 6ac8498. The
   "Verified" and "CI green" boxes are open for this pass and the Driver.

Not run by me: `just check` full and the long gate (cited from CI and the gate log at the same head).

VERIFIED

## Description pass (PR 422 body)

Head: 6ac8498f81f895eb8238294c269d1c6486df7b52

Description pass at 6ac8498: body read with gh pr view 422; Summary, Deliverables, Changes match git diff main...HEAD (17 files; allow_samples.py route rule, audit.py route_pushes, dry_run.py case foreman-route-push, 19 CASES, test_the_cards_name_the_push_ladder, copilot.md sentence). Review note: approved at e4171908 committed as 6ac8498 (chantier log 450). Known gaps present, no images, no STALE. VERIFIED
