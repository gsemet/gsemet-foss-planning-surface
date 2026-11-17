# Verify CR-302 (PRs page of the web board), round 3: the move 0141856..edf4642 (conflict resolution)

Head: edf46420390964482afc94033891074bcb33b7d0

Verdict: VERIFIED (description re-check, round 4)

All claims judged at edf4642 (clean tree in the worktree) unless a line says `carried`.

## Claims judged again (touched by the move)

1. **AGENTS.md wording**. `git diff origin/main...HEAD -- AGENTS.md`: the no-network bullet gains
   "packages, except the board's PRs page (below))" and the board bullet gains the named exception
   (10 s per project, plus one read when the page opens, read-only, user's own `gh`/`glab`, on its
   own, needs the network); the Configuration-page text from main is kept intact. Judged OK.
2. **routes.py, en.js, fr.js, registry.js, test_board.py after conflict resolution**. Same diff: routes imports
   `autosync_api, config_api, costs, files, guard, prs, static, write_api` and registers
   `GET /api/projects/([^/]+)/prs` beside the config routes; `en.js` has `'nav.prs': 'PRs'` beside `nav.config`
   and `...prs` beside `...board`; `fr.js` same; `registry.js` has `prs` after batch and `config` still last
   (`Select-String` on registry.js: ids home, triage, kanban, batch, prs, costs, config); `test_board.py` MODULES has
   `config_api`, `prs`, `forge_read`. `git diff --check origin/main...HEAD` prints nothing.
3. **Tests**. `uv run --no-sync pytest skills/chantier/scripts/cli/tests/test_board_prs.py skills/chantier/scripts/cli/tests/test_board.py -q`:
   `63 passed in 15.64s`.
4. **PRs page beside the Configuration page, real board**. `just scenario --unit surface-board` at edf4642:
   `ok  surface-board (github): 178/178 checks, 182.7 s` (budget 250); the unit covers the PRs route and the
   Configuration page's routes on one board. CI at the head (`gh pr checks 251`): just check x3, eval-dry-run, just scenario (ubuntu-latest) all pass.
   No `chantier gate` pass at this head (the ship line says so); I did not run the long gate.

## Carried

5. carried from 0141856: the route's behaviour in `test_board_prs.py` (item 1 of the earlier note; re-run above, passes).
6. carried from 0141856: docs, CONTRIBUTING, chief-of-staff and scenario README wording; the move did not touch them (the diff of the other files is unchanged by the conflicts, which were in AGENTS.md, routes.py, en.js, test_board.py).
7. carried from 0141856: `evidence/prs-page.png` (the page's front end files are unchanged by the move except the nav key and registry, rechecked in item 2). `just test` timing: not rerun, the Known gap names it.

## PR description (as posted, draft, head edf4642): fails

8. The posted body still dates its proofs at the old head and gives no reason for the move: "Local gates at `0c1180c`, carried
   from `0c1180c` over a clean rebase to `0141856`", "Verified at `0141856`", "CI green at `0141856`" (checked boxes), the
   caption "PRs page at 0141856", and "Review: approved at `0c1180c`". The move 0141856..edf4642 was a conflict resolution, not a clean
   rebase, so the carry reason "clean rebase" no longer holds, and `Verified` and `CI green` name a SHA that is neither the head nor
   carried with its reason. The Driver's log has `inspector approved at edf4642...` for the move, which the Review box does not cite. Fix: update the
   Test plan lines to edf4642 (verified, CI green, gates) and the Review box to the move's approval, and say the screenshot is carried from 0141856 over a conflict resolution that touched the nav key only. Content (Summary, Deliverables, Changes, Known gaps) matches the diff; the "New or changed tests" box is unchecked although `test_board_prs.py` is in the diff (note).

## Not provable here (Known gaps, not failures)

- Three real-forge trials, a real-browser screenshot on a real forge, the refresh stop/restart driven in a browser, Windows full `just scenario`.

NOT VERIFIED (description only; the code and tests at edf4642 pass).

## Description re-check at edf4642 (round 4)

Commands: `gh pr view 251 --json body,headRefOid` (headRefOid edf46420390964482afc94033891074bcb33b7d0), `chantier log CR-302`, `gh pr checks 251`.
- Test plan now dates gates, Verified and CI green at edf4642, with the 0c1180c carries named; Review box cites 0c1180c (log: r2 approved at cb7690a, committed as 0c1180c) and the move's approval at edf4642 (log 2026-11-16T23:49:19Z: move 0141856..edf4642 inspector approved at edf4642...). Screenshot carried from 0141856 with its reason. Fixes item 8.
- CI at edf4642: just check x3, eval-dry-run, just scenario (ubuntu-latest) all pass.
- Known gaps list present and matches items above; code proof carried from the earlier items 1-7.

VERIFIED
