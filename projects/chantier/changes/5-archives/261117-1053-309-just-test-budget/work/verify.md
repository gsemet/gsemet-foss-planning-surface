# Verify CR-309 `just test` back within its budget

Head: 23e0b013b21f4d6b95e595f9c5c157deabbb0565
Base: ab9b0b56b187cd8299da241fd7feb867cebbd835 (detached worktree, left in place)

All claims below are judged at 23e0b01 unless said otherwise.

1. Passes in parallel and serially. `just test` -> `369 passed in 12.90s`; `just test -n 0` -> `369 passed in 49.66s`
   (machine busier than the author's 44 s run, under the 48.5 s budget by margin of parallel run; serial is not the budget path);
   `just test -n 4` twice -> `369 passed in 22.24s`, `369 passed in 18.80s`. PASS.
2. Same test ids. `pytest --collect-only -q -n 0` at head and `pytest --collect-only -q` at base, grep '::' | sort:
   369 lines each, `diff` -> SAME (verifier/head-ids.log, verifier/base-ids.log). PASS.
3. Dependencies. `uv lock --check` -> `Resolved 22 packages`, passes. `git diff ab9b0b5 HEAD -- uv.lock pyproject.toml`: dev group gains
   `pytest-xdist>=3`; lock adds `pytest-xdist 3.8.0` and its own dependency `execnet 2.1.2` only. PASS.
4. Per-worker seeding and copies. `just test -n 4` x2 and `just test -n 3 -k spend` -> 17 passed; `just test -k surface` -> 9 passed;
   `just test -k held_port` -> 1 passed. Seeded answer applies only while `<copy>/.git/HEAD` exists and the key is the repo copy's
   own path (conftest.py `git_cached`); templates built under `tmp_path.parent` / `tmp_path_factory` (per worker). Worktree clean after runs. PASS.
5. Held-port test. Diff: only `monkeypatch` param and a patched `address._call` raising TimeoutError added; the assertions
   (`code == EXIT_EXTERNAL and not out`, one error line starting `error: board not started: `, `port {port}` and `--port` in err)
   are unchanged and the real port is still held. No other test file changed (diff --stat: conftest.py, cost_world.py, test_board.py).
   No assertion removed or weakened. PASS.
6. Timings. Reran `just test` at head: 12.90 s (parallel), far under 48.5 s; work/measure.txt (22/21/16 parallel, 44/43/45 serial,
   87/104/98 base) is consistent with my 12.9-22 s parallel and 49.7 s serial runs. Base serial not rerun. PASS.
7. Scope: diff touches only justfile, pyproject.toml, uv.lock and three test files; no CLI source, card, agent or AGENTS.md change,
   matching the PR's "CLI code not changed" decision. PASS.
8. CI (from the Driver's note at 23e0b01: just check x3, eval-dry-run, just scenario ubuntu pass): not rerun by me; taken from
   `chantier log` note, not proof by itself.
9. PR description (work/pr-body.md): Summary, Changes, timings and Known gaps match the diff. FAIL on the Review box: line
   "Review: approved at `23e0b01` (carried from the pre-rebase pass, a clean rebase)" cites 23e0b01, but `chantier log` has the approved
   notes only at 3df17b9 ("r1 approved at 3df17b969d41 ..., committed as e35193b67da7"); no note of an approved pass at 23e0b01,
   and the box names no `carried from <sha7>`. Fix: "Review: approved at `23e0b01` (carried from `e35193b`)" (or a note of the
   approval at 23e0b01).

NOT VERIFIED

---
Description-only pass at 23e0b013b21f4d6b95e595f9c5c157deabbb0565 (Head unchanged; no code move).
Head: 23e0b013b21f4d6b95e595f9c5c157deabbb0565

Claims 1-8 above (tests, ids, deps, seeding, held-port, timings, scope, CI note): carried from 23e0b01 previous verify.md; the move is a PR description edit only, `gh pr view 265` headRefOid = 23e0b013b21f4d6b95e595f9c5c157deabbb0565, `git status --short` clean.

9. PR description re-judged (`gh pr view 265 --repo gsemet/chantier --json body`): Changes lists the six files of `git diff --stat HEAD~1 HEAD`
   (pyproject.toml, uv.lock, justfile, conftest.py, cost_world.py, test_board.py); Known gaps, Blast radius, test plan SHAs name 23e0b01.
   Review box now "Review: approved at `23e0b01` (carried from `e35193b`, a clean rebase)". `chantier log CR-309` line 11:
   "r1 approved at 3df17b969d41..., committed as e35193b67da7..." -> the note's committed SHA is e35193b, matching the box. PASS.

VERIFIED
