# Verify CR-433

Head: 5709a66cb5230acd6bc5867240e1375171b0ff57

Second pass after the restack move 6249e54..5709a66 (rebased onto origin/main; conflicts resolved in docs/web-board.md, clients/web/DESIGN.md, tests/test_board_design.py). Previous verdict VERIFIED at 6249e54 (kept as verify-6249e54.md.log).

1. Server and client claims, judged again at 5709a66: from `skills/chantier/scripts/cli` in the worktree,
   `PYTHONPATH=src uv run --no-sync --project <main checkout> python -m pytest tests/test_board_design.py tests/test_board_waits.py tests/test_board_times.py -q` -> `49 passed in 3.36s` (stage test, shipped-files design test, DESIGN tests after the conflict resolution).
2. Four batch views pass `priority: c.stage`, no `c.priority`: `grep -rn "c\.priority" clients/web/js` -> no output; `grep -rn "priority: c.stage" clients/web/js | wc -l` -> `4`.
3. Kanban's reading of `stage` (the move touched it): `clients/web/js/views/batch-kanban*.js` filters `rows.filter((c) => c.stage === folder)` with folders `1-pending`, `2-actives`, `3-done`: the same key and values `_row` now writes; no `priority` read. Consistent.
4. Resolved docs: `git diff origin/main HEAD -- docs/web-board.md` shows the Kanban paragraph from main intact plus the last sentence replaced by "A CR's top row begins with the batch folder it is in (`1-pending`, `2-actives` or `3-done`), in a grey chip; a CR no longer in the batch's folders, or a closed batch's record, shows none." `git diff --stat origin/main HEAD` -> 13 files, 64 insertions, 47 deletions, only the CR's files (DESIGN.md 4 lines).
5. Tests fail on the previous code: carried from 6249e54 (the CR's own diff is unchanged in substance; the move changed only the conflict files, rerun at 5709a66 in claim 1).
6. Gate: no `chantier gate` pass exists at 5709a66 (the ship event says so; gates/ holds logs first-lined e7584d7 and 6249e549 only). Not run by me: the long gate is the pipeline's `just scenario (ubuntu-latest)`, pending at the head (`gh pr checks 406`: check ubuntu and eval-dry-run pass; macos, windows, scenario pending). Windows local `chantier gate` is the Driver's, CR being on top of the stack.
7. Review box: the Driver's log (`$CHANTIER log 433`) holds no note of an inspector approval at 5709a66 (last approvals: 6249e54, e7584d7). The Driver must record it before the box says `Review: approved at 5709a66`; otherwise that box is NOT VERIFIED.
8. PR description (PR #406, headRefOid 5709a66, base main, draft): Summary, Deliverables, Changes match the diff; no image. Stale: lines 57, 59, 60, 61 name 6249e54 (see the reply). Known gaps line 31 ("No CI runs on this PR while its base is the stack's branch") is stale: base is main and CI runs.

Not captured: no visual before/after (none required by the spec).

VERIFIED (the code and docs at 5709a66); the description is to be updated as listed before it is posted.
