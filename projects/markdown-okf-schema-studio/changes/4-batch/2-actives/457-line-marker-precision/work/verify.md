# CR-457 verification

Head: 3778f00a996a2f0c753492c368bef3e447c44973

Verdict: VERIFIED (for the behaviour claims below; the PR description is not judged here, see the last section).

Base for the before: `eb3b6eccac951660001fedc1094fd0737c40a9a1` (= `origin/main`, version 1.11.0). All claims judged at
the head above, `git status` of the worktree clean.

## Gate

- Long gate: `work/gates/20261121-212309.log`, first line `gate CR-457 branch chantier/batch-07/cr-457-line-marker-on-the-table-row-the-hidden- head 3778f00a996a2f0c753492c368bef3e447c44973`,
  last line `result: pass at 3778f00a996a2f0c753492c368bef3e447c44973`. Not re-run.
- PR 471 checks at the head (`gh pr view 471 --json statusCheckRollup`): static, static-windows, visual, viewer-graph, report, checks SUCCESS.
  The caller reports heavy run 44946809805 green at the head; not re-checked here.

## Claims

1. Visual scenarios of the group pass at the head. Command (worktree, head):
   `npm run visual:render` then `uv run --no-sync --group docs python test/visual/capture.py --group lifecycle-sync --workers 2`
   (logs `work/gates/verifier-after-render.log`, `work/gates/verifier-after-capture.log`). Output end:
   `passed: lifecycle-sync/v14-line-marker-delimiter-line-light-900` ... `v23-line-marker-edit-mode-tab-panel-dark-900`
   and `{"status": "passed", "scenario_count": 23, "screenshot_count": 23}`. `manifest.json` revision is the head.
2. Table row, every container (head). Driver `work/verifier/drive.py after <worktree> ...` on fixture 94 sends `previewRevealLine`
   (`work/verifier/after-facts.json`): line 15 marker `{top 82, height 34.6}` = `beta` row `{82, 34.6}`; line 20 (quote) marker `{81.8, 34.6}` =
   `second` row `{81.8, 34.6}`; line 26 (note) marker `{81.7, 34.6}` = `south` row; both themes, one marker each. Before (1.11.0,
   `before-facts.json`): line 15 marker `{82.3, 22.4}` while the `beta` row is at 152; line 20 marker at 81.8 and the `second` row at 171.8;
   line 26 marker 82 and the `south` row at 151.7, so the marker was on the top of the block. Captures `before|after-table-row*-{light,dark}.png`, opened and checked.
   Delimiter line to the header row: scenario v14 passes (claim 1). Render-level rows for top level, quote, alert, admonition, list item,
   tab item, CRLF: `out/test/core/render/markerLines.test.js` in claim 5.
3. Hidden tab, exact line, nested (head). Line 36 (third source line of the paragraph in tab `Second`): panels hidden `[true, false, false, true]`
   (Second shown), marker `{81.7, 22.4}` on the third wrapped line of a paragraph starting at 35.9 (35.9 + 2 x 22.4 = 80.7). Line 39: marker `{82, 18.7}` =
   the code line `second_tab_code = 1` `{82, 18.7}`. Line 48 (nested): panels hidden `[true, false, true, false]` (outer `Second` and inner `Other` shown), marker
   `{100.2, 22.4}` = `Nested hidden tab line.` `{100.2, 22.4}`. Before: panels `[false, true, false, true]` (nothing selected), marker `{81.5, 22.4}` on the
   tab bar, the target element has zero size (hidden). Captures `before|after-hidden-tab-*`, opened and checked. One marker in every case.
4. Front matter row (head). Line 4: marker `{71.9, 29.5}` = `tr[data-okf-field=owner]` `{71.9, 29.5}`; line 6 (list value): marker `{81.5, 59}` = the whole
   `tags` row; line 2 (comment): marker `{20, 19}` on the section top (section top 20), as the spec says. Before: line 4 marker `{20, 19}` (title row, the `owner` row at 123.9);
   line 6 marker `{82.1, 35}` on the page heading below the table (the `tags` row at -9.5, the bug (a) of the spec's section 2).
5. Render, page and tab tests at the head. Command: `node --import ./scripts/register-myst-patches.mjs --test out/test/page/runtimeLineMarkerPlacement.test.js
   out/test/page/runtimeLineMarker.test.js out/test/page/modules/tabs.test.js out/test/core/render/markerLines.test.js out/test/core/frontmatter/propertiesTable.test.js`
   (log `work/gates/verifier-head-targeted.log`): `tests 110`, `pass 110`, `fail 0`. Among them the collapsed properties table
   ("a row line expands a collapsed properties table and marks the row; a fence line leaves it collapsed", "a properties table the reader collapses again hides the marker, and a later
   placement never expands it"), the nested tab ("a line in a nested hidden tab selects the outer tab first, then the inner one"), and the sync group
   ("a tab revealed by the marker takes the click's path: the sets of its sync group follow", `tabs.test.js` "reveal of a tab with a sync key makes the other set of the group follow, and a set of another group stays",
   "a revealed tab with no sync key stays after apply ... (C1)").
6. Collapsed properties table and sync groups have no image: fixture 94 has no sync key and no visual scenario collapses the table; the page and tab tests of claim 5 are their proof (named in `before-after.md`, "Not captured").
7. Edit mode (head): v22 (property row) and v23 (line in a tab panel) pass with "arrow meets no control" and no `textarea` assertions (claim 1).
8. Evidence is made-up-path clean: the captured pages show the document only, no local path or user name, each image opened.

## Notes

- `gh pr view 471` reports `isDraft: false` while the brief says draft; reported to the Driver, no verdict impact.
- The leftover scratch worktree `verifier-457-before` of an earlier attempt (only a `node_modules` junction, not a working tree) and my `verifier-457-base` were removed with `git worktree remove`; `git worktree list` shows no `verifier-*`.
- PR description: not judged. Its Impacts section is a placeholder in `work/pr-body.md` ("To be filled") until the Driver adds the captures of `before-after.md`; the description pass (clean render, consistency with the diff, images, Known gaps, Review box) is for the pass after that.

VERIFIED

## PR description pass at 3778f00a996a2f0c753492c368bef3e447c44973 (NOT VERIFIED)

Command: gh pr view 471 --json body; curl -s -o /dev/null -w '%{http_code}' on each raw URL (24 images, all 200).
- Deliverables holds five image tables with relative paths (./verifier/evidence/...): they do not resolve on GitHub (broken images). A second table follows with working raw URLs: the section is duplicated.
- Known gaps (top level) says "None" while the Details Known gaps names a gap (collapsed properties table expand and sync group follow have no screenshot): contradiction.
- Impacts, Autonomous decisions and Known gaps appear twice (top level and inside the fold); Impacts and Human decisions sit inside the fold.

## PR description pass (3778f00a996a2f0c753492c368bef3e447c44973)

Command: gh pr view 471 --json body; curl of the 24 raw image URLs (all 200 image/png, md5 equal to the local evidence files); opened after-hidden-tab-nested-light.png and after-frontmatter-list-value-dark.png (made-up content, no path or username). Layout follows the template (Summary, Deliverables, Blast radius, Autonomous decisions, Known gaps visible; fold holds Changes, Human decisions, Impacts, Test plan, Internal references), no duplicate section, Known gaps lists the uncaptured pairs, CR number only in Internal references. Description: VERIFIED.
