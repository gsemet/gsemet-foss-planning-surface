# Verify CR-457 line marker on the table row, hidden tab and front matter row

Head: 3778f00a996a2f0c753492c368bef3e447c44973

Base: eb3b6eccac951660001fedc1094fd0737c40a9a1 (origin/main; merge-base equals it).

## Claims

1. Long gate pass at the head. Judged at 3778f00a. `work/gates/20261121-212309.log`, first line:
   `gate CR-457 branch chantier/batch-07/cr-457-line-marker-on-the-table-row-the-hidden- head 3778f00a996a2f0c753492c368bef3e447c44973`;
   last line `result: pass at 3778f00a996a2f0c753492c368bef3e447c44973` (command `just preflight`, `ci-static: passed`).
   PASSED.

2. Spec 7.1 and 7.2 targeted tests pass at the head (render marker lines in every container, CRLF, list-table and raw
   table with no row line, front matter end line, export strip, page placement, tabs reveal/apply/onChange). Judged at 3778f00a.
   Command (after `npm run compile`, clean):
   `node scripts/node-test.mjs verif out/test/core/render/markerLines.test.js out/test/page/runtimeLineMarkerPlacement.test.js out/test/page/runtimeLineMarker.test.js out/test/page/modules/tabs.test.js out/test/core/frontmatter/propertiesTable.test.js out/test/core/export/htmlExport.test.js out/test/core/render/cardsTabs.test.js`
   Output (log: `work/gates/verifier-targeted.log`): `tests 154  pass 154  fail 0  cancelled 0  skipped 0`.
   PASSED.

3. The three behaviours in a rendered page, before (eb3b6ecc) and after (3778f00a), light and dark. Judged at 3778f00a.
   `work/verifier/evidence/before-after.md` lists the 10 pairs. I opened every pair: after, the band and arrow sit on the
   `beta` row (top level table), on the `second` row of a table in a quote, on the third wrapped source line of a paragraph
   in the non-selected "Second" tab (the tab is shown), on the `second_tab_code` code line in that tab, and on the `owner`
   row of the properties table; before, each sits on the top of the table, quote, tab set or the properties title, and the
   hidden tab stays hidden. After run: `capture.py --workers 2 --group lifecycle-sync` on the 10 evidence scenarios,
   10 passed (assertions: row top and height within 3 px, tab `aria-selected`, code line, one marker). Before run: 10 failed on those
   same new assertions, as expected. Also run at the head, the CR's own scenarios v08, v17, v18, v20: `passed` x4.
   No path or username shows in any image. PASSED.

## Not judged here

- The PR description (draft, `pr-body.md`): its Impacts section still reads "To be filled with before (1.11.0) and after
  captures" and the Test plan boxes (new tests, local gates, review, CI) are unchecked; there is no Known gaps section.
  The Driver fills Impacts from `work/verifier/evidence/` (note: the before is eb3b6ecc, the base, not the 1.11.0 tag) and
  the description needs its own pass after that. The posted body equals `pr-body.md` apart from a trailing blank line.
- CI (runs 44946649759, 44946809805) is the Driver's report, not re-proved here.

VERIFIED
