# Verify CR-446

Head: acb1cd3380c5ce59477089323d97ffe52b5ba89a

All claims judged at acb1cd3 (the pushed head), in the CR's worktree.

1. Live tests, test_board lazy import. VERIFIED (acb1cd3)
   `uv run --no-sync python -m pytest tests/test_live_model.py tests/test_live_link.py tests/test_board.py -q` -> `77 passed in 8.90s`.
   `-v` over the keys, cap-free key/exit/keystroke/footer/watch/two-boards/refusal tests -> `46 passed` (view scroll/pause/filter/help, q and ctrl-c, 13 keystroke mappings, footer, `watch` five exits: q, ctrl-c key, interrupt, refusal, drawing; two boards; five/twice/only-two/only-one/wrong-key-second refusals; cap test `test_each_board_keeps_2000_lines_and_home_shows_the_oldest_of_the_merged_view` is in the 77).
2. Refusals by the real CLI. VERIFIED (acb1cd3)
   Five `--url`: `error: --url: at most 4 boards in one screen`, exit=1.
   Same twice: `error: --url http://127.0.0.1:9/: given twice`, exit=1 (no connection made).
   Exit 1 is EXIT_USAGE (`core/errors.py`: `EXIT_USAGE... = 1, 2, 3, 4, 5`), the spec wrote 2: accepted by the Driver, named in the PR's Autonomous decisions and Known gaps.
   `--only nope` over two boards, one board, and wrong key on the second board (exit 4, server sentence plus `(board http://127.0.0.1:<port>/)`, key absent) are asserted whole by `test_the_refusals_of_several_boards` against two real servers (all 5 cases PASSED). `test_two_boards_print_one_screen_with_a_label_each_and_no_key` PASSED: header lines, `a/proj`, `b/proj`, `a CR-`, `b CR-`, `ws live` twice, no key in output.
3. Lazy blessed. VERIFIED (acb1cd3): `pyproject.toml:61` banned list holds `blessed`; `tests/test_board.py:54` LAZY holds it; the only import is inside a function, `screen.py:328 from blessed import Terminal`; `blessed==1.53.0` at `pyproject.toml:14`.
4. Untouched files. VERIFIED (acb1cd3): `git diff --name-only <base> HEAD` lists only docs/boards.md, docs/server-api.md, pyproject.toml, uv.lock, clients/tui/{model,screen,view}.py, commands/live.py, declare/live.py and three tests. No link.py, AGENTS.md, cards, agents, hooks, web client or server.
5. Docs. VERIFIED (acb1cd3): `git diff` of docs shows boards.md (one to four boards, repeatable --url, fifth/twice refused, keys table, pause, filter, no keyboard, terminal given back but a killed process) and the one-phrase change in server-api.md.
6. PR body matches the posted description (diff of `gh pr view 418` body against pr-body.md shows only a trailing blank line) and the diff.
7. SIGTERM handler: code present (`commands/live.py:193-206`), the test only checks the handler is put back off Windows; delivery of a real SIGTERM is not run. UNVERIFIED (named in Known gaps).
8. Multi-board `--once` deadline sentence (`live: no first answer within 10 s for <missing>`): code at `commands/live.py:165-172`, no test over several boards. UNVERIFIED (named in Known gaps).
9. Evidence 10 (real terminals, Windows key decoding): not tried, UNVERIFIED, named in Known gaps by the Driver.
10. `just test` time 85 s: the Driver's measure, not rerun here; I ran only the live tests (8.90 s for 77).

VERIFIED

11. Description pass at acb1cd3: posted body matches pr-body.md; CI all 5 jobs pass at acb1cd3 (gh pr checks 418); review note "approved ... committed as acb1cd33" in log; gate pass head acb1cd3380c5 in log; Known gaps hold each UNVERIFIED. Counts (1693 passed, 85 s) are the Driver measures, not rerun.

VERIFIED

## Restack at 0ae9685e (local, base 4c7a1ea0)

Head: 0ae9685e0a18032c802d481f6f543d925f6d8ccb

12. Move: clean rebase, the CR's patch changed (ship: commit 1 of 1 differs); base brought changes to link.py, commands/live.py, pyproject, uv.lock, test_board, test_live_link, docs/server-api.md. Judged again at 0ae9685e.
13. Live tests: `cd skills/chantier/scripts/cli; uv run --no-sync python -m pytest tests/test_live_model.py tests/test_live_link.py tests/test_board.py -q` -> `79 passed in 11.29s` (0ae9685e). Covers claim 1 and 5-boards/twice/only refusals (tests).
14. Refusal by the real CLI (0ae9685e): five `--url ... --once` -> `error: --url: at most 4 boards in one screen`, exit=1. Same URL twice without key -> `error: --url: the link holds no key (?k=...)...`, exit=1 (key refusal first; "given twice" asserted by the passing test).
15. Lazy blessed (0ae9685e): `pyproject.toml:16 blessed==1.53.0`, banned list line 63 holds `"watchfiles", "blessed"`; only import `screen.py:328 from blessed import Terminal` inside a function. The merge with the base's watchfiles/tzdata lines is intact.
16. Files touched by the CR patch at 0ae9685e: docs/boards.md, docs/server-api.md, pyproject.toml, uv.lock, tui/{model,screen,view}.py, commands/live.py, declare/live.py, three tests; no link.py (base's Refusal change is the base's). 
17. Carried from acb1cd3: docs claim 5, claims 7-9 (UNVERIFIED, in Known gaps), evidence note; ruff not available here (`Failed to spawn: ruff`), lint left to `just check`/CI.
18. PR body: stale SHAs only, per the Driver's note; not otherwise re-judged. CI and gate pass at the new head are not yet there (local, unpushed).

VERIFIED
