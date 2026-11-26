# Verify CR-483

Head: a476dedc035bb888f0c49bb58216136cc5779c5f

All claims judged at a476dedc035bb888f0c49bb58216136cc5779c5f (`git rev-parse HEAD` in the worktree, clean tree).

## Tests at the head (shipped files read in place)

Command (from `skills/chantier/scripts/cli` of the worktree, PYTHONPATH pointing at the worktree's `src`, confirmed by `chantier.__file__`):
`env -u NO_COLOR PYTHONPATH=$PWD/src uv run --no-sync --project <main> python -m pytest tests/test_board_dashboard_all.py tests/test_board_dashboard_client.py tests/test_board_design.py tests/test_board_read_key.py tests/test_board_dashboard.py tests/test_board_history_client.py tests/test_board_overview.py -q`
Output: `123 passed in 22.48s`.

- Hover band: `test_the_hover_band_is_behind_the_series_of_both_chart_kinds` passes. Shipped diff: `.chart-svg` gains `z-index: 1` (above `.chart-cols`), keeps `pointer-events: none`; band fill stays `var(--accent-tint)` on `:hover`/`:focus`. VERIFIED.
- test_board_design.py (no new token, no literal colour): passes. VERIFIED.
- Two-project surface (`test_board_dashboard_all.py`, 7 tests pass): shared batch numbers sum, lone number keeps project count 1 (points `[(5,2),(6,1),(7,1)]`); pooled rounds `(1+3+5)/3` and cost per merged CR `43/5`; duration point = mean of projects, headline = median over batches; model rank over union; top rows carry `project`; each project's own answer equals `answer(records,"all")` with no `projects`/`project` field; range "15" refused (BAD); `two.forge.calls == []`; empty surface answers an empty page. VERIFIED.
- Public key: `test_board_read_key.py` (dashboard.get with `project: "*"` and range all under the read key, same as a project) passes. VERIFIED. Note: `closed_rev` (a 12-hex digest, no figure) is added to the board topic's project line; carries no figure.
- Client: `test_board_dashboard_client.py` passes: registry `overview`, order home, inbox, history, dashboard, help; new words in en and fr. VERIFIED.

## Gates and CI

- Long gate pass: `work/gates/20261124-201940.log` first line `gate CR-483 branch ... head a476dedc035bb888f0c49bb58216136cc5779c5f`; `$CHANTIER log` shows `gate result=pass head=a476dedc... name=scenario`. VERIFIED.
- `just check` and `just eval-dry-run` before push: driver note at a476ded (2577 passed; 19 of 19). CI: `gh pr view 460` headRefOid a476dedc..., checks `["SUCCESS"]`. VERIFIED.
- Review box `approved at a476ded`: `$CHANTIER log` note "r1 approved at c0fb4d04, committed as a476ded". VERIFIED.

## PR description (work/pr-body.md, matches the posted PR head)

Clean sections; Summary, Deliverables and Changes match the diff (21 files: chart.css/chart.js, board answer, registry, dashboard views, feed, DESIGN.md, docs/web-board.md, help words, tests); Known gaps names the UNVERIFIED screenshots; no images attached; Internal references holds only the CR line. `Verified at <sha7>` box is for the Driver to tick. VERIFIED.

## UNVERIFIED (declared Known gap, not a failure)

- Screenshots of the hovered charts and of the All-projects Dashboard on each tab: Playwright is not installed; no visual capture was made. The hover fix is proved from the shipped CSS/JS by the test above, not from a rendered page. before-after.md: no pair captured.

VERIFIED
