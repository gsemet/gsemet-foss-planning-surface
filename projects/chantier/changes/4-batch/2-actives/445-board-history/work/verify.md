# Verify CR-445 board-history (restack move)

Head: 4c7a1ea0717129fbb926401842ce02ec7fce4dee

Move: rebased from fe3e404 onto CR-443's local head 11f98d99; conflicts resolved in 11 files plus scenario (22 ops, 7 topics). Previous judgment (12e6f7b) is the baseline; the move touched protocol, ops, topics, docs, history page, client and scenario, so those claims are judged again at 4c7a1ea.

## Claims (judged at 4c7a1ea)

1. History page server, protocol, close keys, client files, design test (spec Evidence 1-9): VERIFIED.
   Command (worktree, skills/chantier/scripts/cli): `uv run --no-sync --project ../../../.. pytest tests/test_board_history.py tests/test_board_history_client.py tests/test_order_drop_to.py tests/test_board_design.py tests/test_server_api_calls.py -q`
   Output: `107 passed in 29.99s`.
2. Op and topic counts agree: protocol.json holds 22 `op.*` keys (backlog 7, board.get, config 2, costs 2, dashboard.get, history.get, journal 2, project 3, prs.get, seats.register, writer.sync) and 7 `topic.*` keys (board, costs, events, history, journal, project, prs). `scenario/run_scenario.py` line 1795 and `scenario/README.md` line 492 say "22 ops, 7 topics"; docs/server-api.md lists `history.get` and the `history` topic; no stale "21" left in docs, tests or api code (grep). VERIFIED by reading.
3. `just check` at 4c7a1ea (worktree clean): `1808 passed, 20 skipped in 113.17s`, `release-notes ... ok`. VERIFIED.
4. Scenario's welcome check (22 ops, 7 topics) is NOT run at this head: no gate pass exists at 4c7a1ea (last gate log 20261122-040514 is at 12e6f7b, at 21 ops). Static agreement only; the Driver owes the pipeline's scenario job and the local gate for the top CR.
5. PR body: stale SHAs only, per the brief; not judged further. Look of the page in a browser: UNVERIFIED as before (carried from 12e6f7b, no browser tool).

VERIFIED
