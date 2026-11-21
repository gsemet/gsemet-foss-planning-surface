# Verify CR-440

Head: 8d99cd1e393fac6a7e978f442c1af80b1e5831e9

Gate pass cited: work/gates/20261121-003908.log, first line
`gate CR-440 branch chantier/batch-07/cr-440-requirements-viewer-shows-table-scenario head 8d99cd1e393fac6a7e978f442c1af80b1e5831e9`, last line `result: pass at 8d99cd1e393fac6a7e978f442c1af80b1e5831e9` (`just preflight`, static stage on Windows).

Claims, each judged at 8d99cd1e393fac6a7e978f442c1af80b1e5831e9:

1. The new tests and the home assertion fail on the base and pass at the head.
   - Base a18bcac12a3fe47cf16f4f5455e6d1cde096d4cb (detached worktree), the head's 5 test files copied in: `tsc -p .` exit 2,
     errors `Module './pages' has no exported member 'scenarioBody'`, `Property 'blocks' does not exist on type 'Scenario'`
     (base-compile.log); emitted JS run with `node --test` (base-tests.log): 4 fail: `no scenario card of the requirements bundle is empty`,
     `home: layers, areas, sections and figures` (assertion on the old hint), `the model reads table scenarios, notes and mixed scenarios in source order`,
     `a table scenario shows its table and a mixed scenario shows steps, note and table in order`.
   - Head: `node --test out/test/site/requirementsViewer/{home,pages,bundle,model}.test.js` -> `ℹ tests 19 / pass 19 / fail 0` (head-tests.log).
2. `just check` at head: exit 0, tail `use case diagrams: 93 StRS checked, all parse`, `0 requirement OKF projections would change`, `0 files would change` (check-head.log).
3. `okfreq validate --check-links --project-root .` at head: exit 0 (validate-head.log; only W2 warnings on other files' example links, none on CORE-082).
4. Site at head (`just requirements-report`, `npm run site`, exit 0): BLOCK-130 first card is a table with th Input, Outcome and 4 rows, 0 gwt; the chord card holds the note
   "The move chord is Cmd+Alt with ArrowUp or ArrowDown on macOS and Ctrl+Alt elsewhere." and a 2-row table; the retry card holds one gwt with text (236 chars), no table;
   0 empty gwt cards on the page, against 6 of 7 at the base (shoot-after.log, shoot-before.log; evidence/after-*.png, before-*.png, opened and checked).
5. GFM-021: cards 1-3 (list) byte-identical markup before and after, cards 4-8 (table) now tables (gfm021-cards-base.log, gfm021-cards-head.log). A Given/When/Then card keeps three columns (retry card above).
6. Phone width, 390 px: document scrollWidth 390 = clientWidth on BLOCK-130 (shoot-after.log); a widened cell scrolls inside its table (probe-wide.log: tScrollW 1721, tClientW 340, scrollLeft 300, document 390). No bundle page has a table wider than its card (scan-phone-head.log). 13 pages already overflow sideways at the base too (scan2-base.log vs scan2-head.log): pre-existing, not this CR's.
7. Description pass: the posted body (`gh pr view 448`, headRefOid 8d99cd1e393fac6a7e978f442c1af80b1e5831e9) equals work/pr-body.md (diff: one trailing blank line). Summary, Deliverables and Changes match the diff (`git diff --stat a18bcac1 HEAD`: model.ts, pages.ts, viewer.css, home.ts, fixture.ts, three test files plus bundle.test.ts, CORE-082, log.md; generated coverage unchanged: `0 files would change`). Mermaid block and sections render. Known gaps says None: nothing left uncaptured except the screenshots, which are announced as "Screenshots: to come at the verified head". Pending for the Driver: attach after-block130-first-card.png and after-block130-chord-card.png (no path or username on them), replace the `<sha7>` placeholders, fill the Review box. No role name in the description outside Internal references.

Notes: base worktree removed at the end; probes and scripts (shoot.cjs, scan*.cjs, probe-wide.cjs) are in work/verifier/.

8. Description pass at 8d99cd1e393fac6a7e978f442c1af80b1e5831e9 (posted body of PR 448): structure, fold, SHA marks (a18bcac base, 8d99cd1 head), no placeholder, Review box (note r1 approved at a18bcac, committed 8d99cd1e), four images (HTTP 200, PNG, opened: captions match, no username or home folder), CI green (gh pr checks 448) all pass.
   FAILED: Summary says "421 requirement files hold at least one table scenario": the number is in the spec only, not in verify.md or before-after.md (no command and output prove it). Narrow it or add the proof.

NOT VERIFIED

9. Description pass, second start, at 8d99cd1e393fac6a7e978f442c1af80b1e5831e9: the "421 files" claim is now "Many requirement files" (backed by 6 of 7 empty cards on BLOCK-130 and 5 of 8 on GFM-021, before-after.md and claim 4/5); the four images return HTTP 200 image/png; gh pr checks 448 green; structure, SHA marks and Known gaps unchanged and pass. Claim 8 failure is resolved.

VERIFIED
