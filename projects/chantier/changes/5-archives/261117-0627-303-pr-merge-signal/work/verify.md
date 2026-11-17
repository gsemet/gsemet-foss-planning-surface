# Verify CR-303 (first verification)

Head: 0d14ae5742c7771cb48a80a8e34b800bf85b5bde

Verdict: VERIFIED

All claims judged at 0d14ae5 (`git rev-parse HEAD` in the worktree; PR 252 `headRefOid` equal).

1. Signal file, once per batch and CR, fields incl. `into`/`into_cr`, cached read and closed PR write nothing, Q13 line (0d14ae5)
   - `pytest skills/chantier/scripts/cli/tests/test_board_prs.py skills/chantier/scripts/cli/tests/test_board_forge_read.py -q` -> `47 passed in 8.87s`.
   - Read of `test_board_prs.py` lines 235-273: parametrized (main / another CR's branch) asserts the exact line fields, a cached read after unlink writes nothing, a second fresh read writes none more; closed, open and recorded cases write no line.
   - Code read: `board/seen.py` `signal` appends under `changes_lock`, UTF-8, dedup on (batch, cr); `board/prs.py` signals only when `fresh and not error`.
2. `status` line in both forms, stops after `order merged`, other batch / cancelled / unreadable / `into_cr` tail (0d14ae5)
   - Same pytest run: `test_status_prints_the_signal_until_the_merge_is_recorded[direct|heartbeat]` and `test_status_names_what_it_cannot_read_and_prints_only_the_open_crs_of_its_batch` pass (lines 276-318 read: exact text `board saw merged: <cr> <pr> into main at <t>; for the Chief of Staff: order merged <cr>`, tail `not landed, tell the user, record nothing until <into_cr> lands`, `board-seen.jsonl: line 1 unreadable`).
3. IGNORED, fingerprint, rescan leaves the file, route writes nothing but the file (0d14ae5)
   - `test_the_signal_file_is_local_counted_by_no_one_and_moves_the_fingerprint` passes (asserts `SEEN in files.IGNORED and SEEN in fingerprint.SINGLE`, `journal.rescan` keeps the file, `since_rescan == []`). Route read-only test (test_board_prs.py lines 142-143) passes: everything but `board-seen.jsonl` unchanged.
4. Cards, AGENTS.md, CONTRIBUTING.md, docs (0d14ae5), by reading `git diff <base>...HEAD`
   - `chief-of-staff.md`: "While it runs" row names `a board saw merged line in status`; the merge bullet records `order merged <cr>` at that status, and for `into <other cr>'s branch` says do not run `order merged`, tell the user, wait.
   - `foreman.md`: heartbeat bullet says do nothing, send no message, not an undone order.
   - `AGENTS.md` and `CONTRIBUTING.md`: the second named exception, same words as the spec. `docs/web-board.md`: the signal, Q10 (read only when a status runs), Q13 paragraphs; intro still says the page writes nothing in a batch.
   - Host agent files unchanged: `git diff --stat` lists no `agents/` or `com.github.copilot/` path.
5. Scenario `surface-board` steps and README (0d14ae5)
   - `git diff` of `scenario/run_scenario.py` shows the steps: one line after the merge, no second line, `status` line, heartbeat form with orders unchanged, line gone after `order merged`; README names them under surface-board.
   - Gate log `work/gates/20261116-220053.log`: first line `gate CR-303 branch chantier/batch-22/cr-303-change-specification-the-board-signals-a head 0d14ae5742c7771cb48a80a8e34b800bf85b5bde`, last line `result: pass at 0d14ae5742c7771cb48a80a8e34b800bf85b5bde`.
6. `just check` (0d14ae5): run in the worktree -> `309 passed in 56.59s`, biome `Checked 104 files ... No fixes applied`, `release-notes ... ok`.
7. `just test` budget: at head `309 passed in 63.14s`; on the base (detached worktree of the base branch, 0141856) the same machine now gives `300 passed in 61.22s`. The CR adds about 2 s; the absolute figure exceeds 18.5 s + 30 s on this machine today for the base as well, so it is not the CR's. Detached worktree removed.
8. PR description (0d14ae5): Summary and Changes match the diff (seen.py new, prs.py/routes.py, batch_status.py, files.py/fingerprint.py, cards, AGENTS/CONTRIBUTING/docs, tests, scenario). Notes for the Driver, not failures of the code: Known gaps still says the scenario steps were not run, while the gate log passes at this head, and the Test plan boxes still carry `<sha7>` placeholders; update both at handback.

Evidence before/after: not applicable (no visual change).


## Description pass (head 0d14ae5742c7771cb48a80a8e34b800bf85b5bde)

VERIFIED. Posted body (gh pr view 252) equals work/pr-body.md (compared, equal). Judged at 0d14ae5: Summary, Deliverables (names seen.py, prs.py, _seen_lines exist in the diff), Changes and Impacts match `git diff --stat 0141856 HEAD` (15 files). Template audit 1-10 holds: sections in order, fold with blank lines and nothing after it, no CR name outside Internal references (Chief of Staff and Foreman are product terms of the cards this diff changes), Known gaps None with no UNVERIFIED claim, Test plan SHAs all 0d14ae5, no STALE, no placeholder. Review box: `chantier log` note 'r1 approved at 0141856, committed as 0d14ae5' proves it. The two notes of the first pass (Known gaps wording, sha7 placeholders) are fixed. Verdict already recorded VERIFIED at this head; not recorded again.
