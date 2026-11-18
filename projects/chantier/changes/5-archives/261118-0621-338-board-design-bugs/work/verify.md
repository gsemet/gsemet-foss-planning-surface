Head: c34c04de27b9ffa5a8742fd5a8ccbdd11945bdf4

# CR-338 verification (second pass, after the restack 7b8b87c -> c34c04d, base cr-335 -> main 6f1e4f76)

Move: `git diff --stat 6f1e4f76 HEAD` -> 14 files changed, 164 insertions, 29 deletions (same 14-file patch). The base change brought other files (docs, stacks.py, prs.py, ...), none that the title tests, the front matter probe or the drawer proof run, except as exercised below; all re-run at c34c04d.

1. Title rule, judged at c34c04d. `uv run --no-sync --project . pytest skills/chantier/scripts/cli/tests/test_titles.py -q` -> `12 passed in 6.72s`. VERIFIED.
2. Front matter probe, judged at c34c04d. `node --input-type=module` importing markdown.js `renderMarkdown`:
   - `---\ntype: cr-answers\ndescription: a <b> x\n  more\n---\n# Hi\n\ntext` -> `<dl class="fm"><dt>type</dt><dd>cr-answers</dd><dt>description</dt><dd>a &lt;b&gt; x more</dd></dl><h3 class="md-h1">Hi</h3><p>text</p>`
   - BOM + `---  ` -> `<dl class="fm"><dt>k</dt><dd>v</dd></dl><p>body</p>`
   - unclosed `---\na: 1\n# H` -> `<p>--- a: 1</p><h3 class="md-h1">H</h3>`
   - empty front matter -> `<p>x</p>`. VERIFIED.
3. Drawer and Kanban in a real browser at c34c04d (Playwright/Chromium, `shoot.py` copy, demo data, 1440x900, my own outdir, removed at the end). Opened as images: the drawer shows plain file rows (icon, name, sizes right-aligned on one x), a muted type/description/status list above "Answers"; the Kanban shows borderless Priorities chips (Inbox, P1..P4) with no grey square and Labels with their coloured dots. VERIFIED.
4. Claims carried from 7b8b87c (title mechanism in views/stages/crs, class renames and no leftover selectors, postit.css, no hooks/ or types/ change): the CR's patch is the same 14 files (above) and the tests and probes above re-run green; carried.
5. Evidence images vs the head (the PR's after-* captured at 7b8b87c): my recapture at c34c04d, sha256 prefix: after-kanban `c6d347ff0a8ab681` and after-batch `83e47c1a70ae2038` are byte-identical to evidence/after-*.png; after-drawer differs only in the "Data: 1 s ago" vs "2 s ago" clock text (viewed side by side, same rendering). So the images still match the head. before-* were not recaptured (base 5b86c93 is not in this history; unchanged by the move). Privacy: the images show shop-api / batch-03 made-up data only; no username or home folder.
6. PR 300 description (gh pr view 300, head c34c04de..., base main): renders, sections and fold fine; Summary/Deliverables/Changes match the 14-file diff; images are the evidence files above; Known gaps lists the title screenshot, pane screenshot and opening.py limits. SHAs: Evidence line names before 5b86c93 and after 7b8b87c: after is proven to still match at c34c04d (item 5); Review, Verified and gates are written "carried from 7b8b87c": the Review is proven by log note `r3 inspector approved ... committed as 7b8b87c4`; "Verified carried from 7b8b87c" holds only with this pass (VERIFIED at c34c04d) - the Driver may say "Verified at c34c04d". CI at c34c04d: `gh pr checks 300` five jobs pass (check x3, eval-dry-run, scenario ubuntu). VERIFIED.

Not proved: the CR board pane (no real session screenshot, a named Known gap); the "---" titles in a browser (demo data records real titles, named Known gap, proven by tests only); no long gate (`chantier gate`) at c34c04d (ship's `off` line), the pipeline's scenario job is green at this head and is not my proof; before-* images not recaptured.

VERIFIED

## Description pass (judged at c34c04de27b9ffa5a8742fd5a8ccbdd11945bdf4)

PR 300 body re-read with `gh pr view 300 --json body,headRefOid` (headRefOid c34c04de27b9ffa5a8742fd5a8ccbdd11945bdf4). Test plan, line by line:
- Tests `tests/test_titles.py`: passed, item 1 above at c34c04d.
- Local gates at 7b8b87c (patch unchanged): `$CHANTIER log CR-338` note 22:55:35Z "before first push at 7b8b87c: just check: pass (484 tests); just eval-dry-run: pass (17 of 17)". Proven; the restack kept the same 14-file patch (item 4 above).
- Evidence before 5b86c93 / after 7b8b87c: after images still match the head (item 5 above).
- Review approved carried from 7b8b87c: log note "r3 inspector approved ... committed as 7b8b87c4" names that SHA. Proven.
- Verified at c34c04d: this file, items 1-6 above, VERIFIED at that head.
- CI green at c34c04d: `gh pr checks 300` -> check x3 pass, eval-dry-run pass, scenario (ubuntu-latest) pass.
Renders (sections, fold, image links to evidence files), Summary/Deliverables/Changes match the diff, Known gaps lists the three gaps, no username or home folder in the images, no stale mark, no role name outside Internal references. No new verdict recorded; the code verdict VERIFIED at c34c04d stands.

VERIFIED (description)
