# CR-457 before and after

Before: `eb3b6eccac951660001fedc1094fd0737c40a9a1` (origin/main, release 1.11.0).
After: `3778f00a996a2f0c753492c368bef3e447c44973` (pushed head of PR 471).

All files are in `work/verifier/evidence/`, named `<before|after>-<case>-<light|dark>.png`, 900 x 1000
viewport at scale 2. Fixture: `test/visual/fixtures/94-line-marker-precision.md` (the same file for
both sides; it was copied into the before checkout, which has no code change). Every capture shows the
arrow and band drawn after the host message `previewRevealLine` for the line named below, which is
what a search result or an editor jump sends. No capture shows a local path or user name (each was
opened and looked at; the page shows the document only).

| Case | Line | Before (1.11.0) | After (head) |
| --- | --- | --- | --- |
| `table-row` | 15 | band and arrow on the top of the table (header row, 22 px high, table top at 82 px) | band on the `beta` row (top 82.0, height 34.6, equal to the row) |
| `table-row-quote` | 20 | arrow on the top of the quote, `second` row 90 px lower | band on the `second` row of the quoted table (top 81.8, height 34.6) |
| `table-row-note` | 26 | arrow on the top of the note | band on the `south` row inside the note (top 81.7, height 34.6) |
| `hidden-tab-paragraph` | 36 | band on the tab bar of the tab set; tab `First` stays shown, the paragraph is never shown | tab `Second` selected, band on the third wrapped line of the paragraph |
| `hidden-tab-code` | 39 | band on the tab bar of the tab set, `First` shown | tab `Second` selected, band on the code line `second_tab_code = 1` (top 82.0, height 18.7) |
| `hidden-tab-nested` | 48 | band on the tab bar of the outer tab set, nothing selected | outer `Second` and inner `Other` both selected, band on `Nested hidden tab line.` |
| `frontmatter-row` | 4 | band on the top of the properties table (title row) | band on the `owner` row (top 71.9, height 29.5) |
| `frontmatter-list-value` | 6 | band on the page heading below the table (the nearest body block), not on the `tags` row | band on the whole `tags` row (height 59) |
| `frontmatter-comment` | 2 | top of the properties table | top of the properties table (unchanged by design) |

Edit-mode captures (property row and a line in a tab panel, arrow meets no control, no `textarea`)
are the scenarios v22 and v23 of the group `lifecycle-sync`; they pass in
`work/gates/verifier-after-capture.log` and their PNGs are written by the harness under
`out/reports/e2e/screenshots` of the worktree (not copied here).

The measured numbers of each case and side are in `work/verifier/before-facts.json` and
`work/verifier/after-facts.json` (marker box, expected element box, panels hidden state).

## Not captured

- A collapsed properties table that expands on a row line, and the sync group following a revealed
  tab: no visual scenario and no fixture covers them; they are proved by page and tab tests (see
  verify.md claims 6 and 7), not by an image.

## Reproduce

1. Before: `git worktree add --detach <path> eb3b6ecc`, copy `test/visual/fixtures/94-line-marker-precision.md`
   from the head into it, `npm run visual:render` (node_modules and `.venv` of the head linked in).
2. After: in the CR worktree at the head, `npm run visual:render`.
3. `uv run --no-sync --group docs python -I work/verifier/drive.py <before|after> <worktree> work/verifier/evidence`
   (the driver loads the rendered page of the fixture in Chromium, light and dark, sends the
   `previewRevealLine` message as `test/visual/capture_final_checks.py` does, waits, reads the facts, saves the PNG).
