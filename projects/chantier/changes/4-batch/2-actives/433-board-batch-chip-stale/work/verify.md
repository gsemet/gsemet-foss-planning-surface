# Verify CR-433

Head: 6249e549e4fdcb88ec54357fe2d4c625748c5395

All claims judged at 6249e549 unless stated. Tests run with `PYTHONPATH=src` from the worktree's `skills/chantier/scripts/cli` (the `uv run --project <main checkout>` otherwise imports the main checkout's code and the new server test fails with KeyError: that is the invocation, not the CR).

1. Batch row carries `stage` (folder, from disk) and no `priority`: `git diff d91edcf3 HEAD -- board/crs.py` shows `"priority": priority_of(...)` replaced by `"stage": stage_of(repo, folder)`; `test_a_batch_row_carries_the_batch_folder_...` passes (1-pending, 2-actives, 3-done, None for a backlog path and for no folder; no row has "priority").
   Command: `python -m pytest tests/test_board_design.py tests/test_board_waits.py tests/test_board_times.py -q` -> `42 passed in 1.25s`.
2. Four batch views pass `priority: c.stage`: `grep -rn "priority:" clients/web/js` outside ui/ -> batch-gantt.js:64, batch-graph.js:68, batch-pr-card.js:76, batch-timecards.js:55, all `priority: c.stage`; the design test asserts it and that no js file contains `c.priority`.
3. Kanban card and backlog views unchanged: `git diff d91edcf3 HEAD --stat -- clients/web/js/views` lists only the four batch-* files; no Kanban/backlog view file in the diff. No new colour or `.tag.pri-*` rule for the folders (asserted by the design test).
4. Docs and DESIGN.md say so: diff shows `docs/web-board.md` (Batch paragraph: folder chip in grey, none for a CR out of the folders) and `clients/web/DESIGN.md` (batch CR card shows its batch folder in a neutral grey chip, never a priority).
5. Tests fail on the previous code: detached worktree of base d91edcf3 with the two new test files copied in: `python -m pytest tests/test_board_design.py tests/test_board_waits.py -q` -> `2 failed, 29 passed` (test_a_batch_view_draws_the_batch_folder_chip_not_a_priority; test_a_batch_row_carries_..., KeyError: 'stage'). Base worktree removed.
6. Triage lane item: moot, CR-428 removed the Triage lane code.
7. Gate pass at head: `work/gates/20261121-214652.log` first line `gate CR-433 branch chantier/batch-30/cr-433-a-batch-cr-s-card-shows-its-batch-folder head 6249e549e4fdcb88ec54357fe2d4c625748c5395`.
8. PR #406 description (headRefOid 6249e549): Summary, Deliverables and Changes match the diff (stage/priority swap, four views, priority_of removed, docs, tests); no image; Known gaps names the unretaken screenshots and the unchecked live board. Test-plan boxes still hold `<sha7>` placeholders and unticked boxes, for the Driver to fill at ready; not a content mismatch.

Not captured: no visual before/after (no screenshot required by the spec; Known gaps says no live-board check).

VERIFIED
