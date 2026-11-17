# Verify CR-323 

Head: 3cdf05dd12272a132a6bcd39ca8e591d1da48170

All claims judged at 3cdf05d. Base (before): cb7a1f5.

1. Spec Evidence tests exist and pass at head. `pytest test_board_running.py test_surface_batches.py test_board.py -q` -> `40 passed in 5.21s`. (They sit in two new files, not test_board.py; the PR names this in Autonomous decisions.)
2. The same two test files fail on the base (cb7a1f5, detached worktree, removed after): `ModuleNotFoundError: No module named 'chantier.core.surface_batches'`, `2 errors during collection`.
3. Real boards, scratch repo (made-up folder inside the worktree, removed after), head's CLI:
   - first `board --port 0` printed `board on http://127.0.0.1:64994/...`; `board.json` held `running` {pid 22836, host, port 64994, version 0.11.0, served, started}.
   - second `board --port 0` and `board --port 8123` both printed `board already running at http://127.0.0.1:64994/?k=...`, exit 0.
   - record edited to a silent port (1): `error: board not started: a chantier board 0.11.0 (PID 22836) holds this surface at 127.0.0.1:1 and does not answer: stop it (taskkill /PID 22836 /T /F), then run board again`, exit 4.
   - After I stopped my own board by id (22836, hard kill): the stale record was ignored, a new board started and wrote pid 12396 (gone afterwards).
   - Not run for real: the "another version" line (no second chantier version at hand); covered by the passing parametrized unit test (claim 1). A record edited to 0.9.9 while the live board answered 0.11.0 reused it (the answer's version is compared).
4. P14: `preflight` in the in-project scratch repo: 0 P14 lines. On a scratch two-project surface, `preflight --project projects/a` printed `P14 ok   no other batch on this surface` (other P-checks failed on the scratch, unrelated). With batches open, `just scenario --unit surface-board --forge github` (external_surface + remote_board) ran at head: `ok surface-board (github): 189/189 checks`, which includes the `status` other-batches line, P14 naming demo's batch, and the second-board reuse with `/api/board` pid.
5. Cards/docs/AGENTS.md diff (`git diff HEAD~1 HEAD`) matches spec B-E: staging rule in chief-of-staff.md, griller.md, concepts.md; P14 in Starting a batch steps 1 and 2; session-start.md two new lines bullet; web-board.md; planning-modes.md paragraph; scenario/README.md; AGENTS.md board line. `grep "git add -A"` in cards shows no other card telling a session to commit the surface by hand.
6. PR #278 description (gh pr view, headRefOid = 3cdf05d): renders, Summary/Deliverables/Changes match the diff, Known gaps present, no images.
7. Gate: lead says `just scenario` passed locally and CI green at this head (not re-run by me; my unit run above is an independent pass).

Process note: I started my scratch board with a `nohup` background launch (a rule slip); it was stopped by its id and no other process was touched.

VERIFIED

## Description pass (PR #278 body as posted)

Head: 3cdf05dd12272a132a6bcd39ca8e591d1da48170

Judged at 3cdf05d. The PR's base is the CR-322 branch, so its diff is `git diff --stat HEAD~1 HEAD` (18 files, 520+/37-), not main...HEAD.
- Renders: sections, table, code blocks, fold; no images.
- Summary, Deliverables, Changes match the HEAD~1..HEAD diff: running.py, command.py, key.py, routes.py, surface_batches.py, preflight.py, batch_status.py, the cards and docs listed, scenario/README.md, AGENTS.md, both new test files. Also touched, not itemised: scenario/run_scenario.py (the Autonomous decisions bullet names the remote_board change). No claimed change is missing.
- SHAs: all `3cdf05d`, the head. Proof for each is in claims 1-7 above.
- Review box: `$CHANTIER log 323` has "r1 approved at cb7a1f5..., committed as 3cdf05d": matches.
- Known gaps: the UNVERIFIED-type items (another-version line only unit-tested, Windows-only local scenario, --clock case) are present.
- Template audit: internal references (CR-323, work/coder/r1.md) only under Internal references. Role names (Chief of Staff, Foreman, Drivers) are product terms of the change.

VERIFIED

# Restack pass

Head: 0feef12c360c8d9daf8fdb4c2fd0f072ff3352a1

Move 3cdf05d -> 0feef12 (restack onto CR-322 91114fe; base brought many changes). `git range-diff 3cdf05d~1..3cdf05d 91114fe..HEAD` shows the patch differs only in AGENTS.md (board line merged with the base's worktree-removal text), routes.py context (base added `served_origin`) and batch_status.py (import context, `status()` lines list). Cards, docs, running.py, command.py, key.py, surface_batches.py, preflight.py, tests: unchanged.

1. Spec Evidence tests exist and pass (judged at 0feef12). Running `tests` with PYTHONPATH on the worktree src (plain `uv run` imports the main checkout, which lacks `closing._to_remove` and errors in test_batch_end, unrelated): `443 passed in 58.10s`, includes test_board_running.py, test_surface_batches.py, test_board.py.
2. Fails on base: carried from 3cdf05d: the new test files import `chantier.core.surface_batches`, absent from the base; the move does not change that.
3. Real boards on a scratch repo: carried from 3cdf05d for board/running.py, command.py, key.py (patch unchanged); routes.py context-only change, covered by the 443 passing tests. Not re-run for real (a real board needs a background process, forbidden to me).
4. P14 / status line (judged at 0feef12, touched by the batch_status.py resolution): the diff `91114fe..HEAD` of batch_status.py shows `_other_batches_lines` and the lines list `[batch_line, *autosync, *other_batches]`, then `_unpaused_line`, last_closed: both lines kept; test_surface_batches and the status tests pass in the 443. Scenario unit surface-board is the CI job `just scenario (ubuntu-latest)`: IN_PROGRESS at the time of this check (gh pr view statusCheckRollup); check, macOS, Windows, eval-dry-run: SUCCESS.
5. Cards/docs/AGENTS.md (judged at 0feef12): AGENTS.md diff shows the board line keeps both the CR's PID/address/version text and the base's "removes the merged CRs' worktrees and branches at a batch's end (below)": resolution correct. Cards: `git grep "git add -A" -- skills` shows only the rules "never git add -A" (chief-of-staff.md:359, griller.md:73, driver.md:588). Rest carried from 3cdf05d (range-diff unchanged).
6. PR #278 description (gh pr view, headRefOid 0feef12): FAILS. Test plan still names `3cdf05d` for "Local gates", "Review: approved", "Verified" and "CI green" (5 lines); 3cdf05d is not in the head's history, and no proof at 0feef12 yet (no long gate pass at 0feef12; CI scenario in progress; the Review box needs a note at 0feef12: the log has "inspector approved at 0feef12" as a Driver note, but the box cites 3cdf05d). The driver's own ship line flagged the same.
7. Gate: no local gate pass at 0feef12 (the user's Windows run is a later step); CI `just scenario (ubuntu-latest)` not finished.

NOT VERIFIED (description names a SHA outside the head's history; CI scenario not yet green at the head)

# Second restack pass

Head: 0feef12c360c8d9daf8fdb4c2fd0f072ff3352a1

Carried from the restack pass above (patch unchanged since): claims 1-5.

6. CI at 0feef12: `gh pr checks 278` -> check macOS/ubuntu/windows pass, eval-dry-run pass, `just scenario (ubuntu-latest)` pass (2m53s). Long gate green.
7. PR #278 body as posted (headRefOid 0feef12c36...): no `3cdf05d` left (grep of the body: none). Review box `approved at 0feef12`: `chantier log 323` line 23 "move 3cdf05d..0feef12 (restack) inspector approved at 0feef12" matches. Renders, no images.
8. FAILS: Test plan line 72 states as fact, checked, "Local gates at 0feef12: `just check` (395 tests), `just scenario` (pass, Windows)". No local `chantier gate` pass exists at 0feef12 (the Driver's own ship line 27: "no long gate passed at 0feef12"); the test count was 443 in my run at 0feef12 (restack pass, claim 1), not 395. The Known gaps bullet "The scenario ran locally on Windows only" is likewise not true at this head. Fix: narrow line 72 to what ran (or uncheck it) and name in Known gaps "the Windows local `just scenario` at 0feef12 is not run yet (the user's step)"; drop or correct "395 tests".

NOT VERIFIED (description claims a local Windows scenario pass at the head that was never run)

# Third restack pass

Head: 0feef12c360c8d9daf8fdb4c2fd0f072ff3352a1

Claims 1-5 and the CI/Review-box claims carried from the second pass (patch unchanged).

8. Fixed. `gh pr view 278 --json body` at headRefOid 0feef12: line 72 now reads "`just check` (443 tests) ... `just scenario` locally on Windows at this head: not yet run (Known gaps)"; Known gaps line 46 names "The Windows local `just scenario` at `0feef12` is not run yet (the user's step before merge)". No `395`, no `3cdf05d` left (grep). `gh pr checks 278`: five checks pass at the head, including `just scenario (ubuntu-latest)`.

VERIFIED
