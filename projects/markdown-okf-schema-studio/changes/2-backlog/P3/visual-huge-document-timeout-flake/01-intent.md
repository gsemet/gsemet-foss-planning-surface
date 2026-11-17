# Backlog (P3, rule 12): visual huge-document v20 timeout

- Run: https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40804420093 (attempt 1, normal
  CI of PR #206 after the stack rebase, 2026-10-29).
- Scenario: `rendering-core/v20-huge-document-bottom-dark-900`, fixture
  `gen-huge-document--dark--sticky-3--default.html`: "scenario exception: Timeout 30000ms exceeded",
  then "last content or bottom padding is missing from final frame".
- 1 occurrence, slow runner suspected: #206 changes test files only; the same scenario was green on the
  rebased neighbours #194 (run 40804417796) and #200 (run 40804439747, which contains #206's commit).
  Failed jobs re-run once (attempt 2).
- Next: watch for a second occurrence; if it recurs, measure the huge-document render time per run.

## Root cause found (2026-10-31)

The hang is in the harness, not the product:
- `page.wait_for_load_state("networkidle")` (test/visual/capture.py:294) never resolves when preview.js is requested more than about 0.5 s after the document finished loading. This is a Playwright 1.64.1 idle-tracking race.
- The narrow-toolbar fix made this gap frequent on the huge fixture.

Fix in progress: CR 232 removes that wait. Close this item when CR 232 lands.
