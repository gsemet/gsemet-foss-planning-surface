# Verify, CR-481

Head: bf5fdbd49334c62e952cec8dcc72c2d3a149f5b0

Re-verification after a move: 007aa019..bf5fdbd4, rebase with a resolved conflict, old base
c155c897, new base origin/main 0bd42a68. Previous verdict VERIFIED at 007aa019 (on c155c897).

## The move

- `git range-diff c155c897..007aa019 0bd42a68..bf5fdbd4`: commit 1 differs only by dropping its
  `orders_apply.py` hunk (removal of an unused `CrEntry` import), which main already made
  (`grep -n CrEntry .../commands/orders_apply.py` at bf5fdbd4: no output). Commit 2 differs only in
  `board/address.py`: main's `_call(..., timeout: float = 2)` kept, and main's new `call_op` now
  calls `links.base(host, port)` instead of the removed `_base`.
- `git diff 0bd42a68 bf5fdbd4 -- board/address.py`: helpers removed, re-exported from `links`
  (`__all__`), `probe`, `register_seat`, `call_op` use `links.base`; nothing else.
- Stale private names: `grep -rn "_base\b|address\._|_default_route_address|_loopback_of|_bracket"`
  over src, tests and scenario (links.py aside): no use of a removed name remains.
- Base brought changes to board code the proofs exercise (address.py, restart.py, ops, many
  others): so the pane/services tests and the board address tests are judged again below.

## Claims judged at bf5fdbd49334c62e952cec8dcc72c2d3a149f5b0

1. Services test: `uv run --locked --group dev pytest -q skills/chantier/scripts/cli/tests/test_status_index_services.py`
   -> `3 passed in 1.23s`.
2. Pane tests: `just mod` -> `94 pass, 0 fail` (including "with no readable server.json the links
   carry no key and one line says so" and "an index of the older shape ... draws as it did").
3. The resolved address.py and its callers (main's `call_op` in restart, `live`, remote CLI, serve
   and webui links): `uv run --locked --group dev pytest -q test_status_index_services.py
   test_board_restart.py test_board_exposure.py test_remote_cli.py test_serve_webui.py
   test_board.py test_board_read_key.py` -> `163 passed in 36.45s`.
4. Lint of the two touched modules: `uvx ruff check board/address.py board/links.py` -> `All checks passed!`.
5. Review of the move: `$CHANTIER log CR-481` note 2026-11-24T20:22:19Z "move 007aa01..bf5fdbd
   (conflict) inspector approved at bf5fdbd"; same note: `just check`, `just eval-dry-run`,
   `just mod` pass at bf5fdbd.
6. PR head: `gh pr view 457 --json headRefOid` -> bf5fdbd49334c62e952cec8dcc72c2d3a149f5b0. CI at
   this head when read: `just eval-dry-run` SUCCESS; `just check` (3 OS) and `just scenario`
   IN_PROGRESS (not yet proof).

## Carried

- Spec claims proved by item 1 and 2 of the previous note (merged/created/counts/services in
  STATUS.json, no key text, the pane's states, folds, links): carried from 007aa01 and re-run
  green above at bf5fdbd.
- The red-at-base proof (`3 failed`, `KeyError: 'services'` at c155c89): carried from 007aa01:
  the move did not change the test file nor the status writer (range-diff shows no hunk there).
- Not proved: the pane in a real Claude Code session (screenshot); a Known gap, not a failure.

## Not judged in this pass

- Long gate at bf5fdbd: none yet (runs separately, per the brief); `handoff` will need it.
- PR description: the PR is a draft and its body still names 007aa01 in Evidence and Test plan
  (lines 25-29, 75-79; `ship` listed them as off at 20:22:27Z). It owes an update to bf5fdbd (or
  `carried from 007aa01` with a reason) and a description pass before it is ready.

VERIFIED
