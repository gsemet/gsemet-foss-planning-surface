# Verify CR-445 board-history (restack move to fca2ce1)

Head: fca2ce1275b0a3ac90bda6a103dd8c797b026b8c

Move: 4c7a1ea (base 11f98d9) to fca2ce1 (base 187d6b6); conflicts in clients/web DESIGN.md and i18n en/fr, biome import-order fix squashed. The base brought many files (docs, web client, cards), so each proof that runs the web client, protocol or docs is judged again at fca2ce1.

## Claims (judged at fca2ce1)

1. History page server, protocol, close keys, client files, design test: VERIFIED.
   Command (worktree, skills/chantier/scripts/cli): `uv run --no-sync --project ../../../.. pytest tests/test_board_history.py tests/test_board_history_client.py tests/test_order_drop_to.py tests/test_board_design.py tests/test_server_api_calls.py -q`
   Output: `107 passed in 26.39s`.
2. Op and topic counts agree: `grep -c '"op\.' protocol.json` gives 22, `grep -c '"topic\.' protocol.json` gives 7; `scenario/run_scenario.py:1795` says "the 22 ops and 7 topics" and `scenario/README.md:492` "the 22 ops, the 7 topics". The only "21 ops" left are in `scenario/results/` (git-ignored old run output). VERIFIED.
3. `just check` at fca2ce1 (worktree clean): `1835 passed, 20 skipped in 118.51s`, `release-notes: ... ok`. This covers lint, biome and the web client tests and build steps `just check` holds. VERIFIED.
4. Scenario welcome check (22 ops, 7 topics) NOT run: `just scenario` was barred by the brief (a Windows local gate runs elsewhere). Static agreement only (claim 2); the Driver owes the pipeline's scenario job and the local gate for the top CR.
5. Screenshots and look of the History page in a browser: UNVERIFIED (not run at this head; no browser tool; carried unjudged from 12e6f7b). PR body: not judged here.

VERIFIED (claims 1-3 at fca2ce1; 4 and 5 are open gaps, not failures)
