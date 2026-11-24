# Verify CR-482

Head: f1c0f5af0396706f0f2b921f8060808878195af4

All claims judged at f1c0f5a.

## Claims

1. Evidence tests at the head (f1c0f5a). Command, from skills/chantier/scripts/cli:
   `python -m pytest tests/test_board_help.py tests/test_board_inbox_design.py tests/test_board_history_client.py tests/test_board_web_menu.py tests/test_board_griller_client.py tests/test_board_design.py tests/test_board_overview.py tests/test_board_read_key.py tests/test_board_history.py -q`
   Output: `138 passed in 21.93s`. These cover: Help last / History overview (help, web_menu), nav.inbox Notifications en+fr,
   no kanban view/files/go, batch-kanban.js and kanban-cards.js kept, GRILL_BUTTON constant off (`export const GRILL_BUTTON = false;`, grillAction returns '' when off),
   `--backdrop` token in tokens.css and DESIGN.md table, backdrop click via `confirmLeave().then(ok => ok && closePanel())` (main.js diff),
   all-projects history for two projects, open-PR rows (red CI vs ready, no forge call), feed newest 20, public key sees no cost/round. VERIFIED.
2. Grep at the head: no `go: 'kanban'` / `data-go="kanban"` in clients/web; kanban.js and kanban.css absent; registry.js and index.html name no kanban. VERIFIED.
3. Gate pass: work/gates/20261124-181910.log first line `gate CR-482 branch chantier/batch-31/cr-482-web-board-menu-detail-overlay-multi-proj head f1c0f5af0396706f0f2b921f8060808878195af4`;
   scenario-run.log `pass just scenario at f1c0f5a`; check.log and eval.log present. VERIFIED (cited, not re-run).
4. PR #458 head is f1c0f5af0396706f0f2b921f8060808878195af4 (`gh pr view 458 --json headRefOid`). Summary/Deliverables/Changes match the diff stat (kanban files and PNGs removed, overview.py, history-filter.js, backdrop in main.js). VERIFIED.
5. PR description: still the draft: first line `<!-- draft; SHAs filled at ship -->` and Test plan holds `<sha7>` placeholders; Deliverables says "Screenshots: to be added at the head"; Known gaps names the missing screenshots and the old docs pictures. Note for the Driver: fill the SHAs and the screenshots at ship; a description left so is not clean.

## UNVERIFIED

- The five spec screenshots (All-projects home, All-projects History, menu, panel over dimmed page, leave dialog): not taken. Playwright is not installed here (`ModuleNotFoundError: No module named 'playwright'`), so scripts/docs_screenshots.py cannot run. No images in evidence/.
- Real red CI from a live forge, and the Grill constant switched on: not provable here (as the brief says).

## Verdict

VERIFIED (code and tests at f1c0f5a). Pending for the Driver: screenshots and the filled PR description.
