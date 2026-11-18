Head: 7b8b87c46a286cbfa17c969e78a1a0a8fcc07173

# CR-338 verification (first pass), judged at 7b8b87c

1. Title rule (`markdown_title`, `_title`, `prepared_cr`, `shown_title`), judged at 7b8b87c.
   `uv run --no-sync --project . pytest skills/chantier/scripts/cli/tests/test_titles.py -q` -> `12 passed in 1.95s`
   (8 markdown_title cases incl. BOM, CRLF, unclosed fence, only-frontmatter; open/_title/shown_title; idea_slug).
   Direct probe `python -I -c "from chantier.core.files import markdown_title ..."` gave: front matter+`# T` -> 'T'; BOM -> 'T'; CRLF -> 'T'; front matter+plain -> 'plain'; `para\n## H` -> 'H'; only front matter -> ''; unclosed `---\na: b\n# H` -> 'H'.
   `git diff 5b86c93f HEAD` shows `shown_title` in status/views.py (cr_view, _row, _past, _done_rows), board/crs.py `_row`, commands/close_archive.py (history record), facts.py, driver.py; `prepared_cr` uses `markdown_title(text) or directory.name`. history.py untouched, as the PR says. VERIFIED.

2. Class renames, no leftover selectors, judged at 7b8b87c.
   `grep -rn "tree .nm\|tree .ind\|class=\"nm\"\|\"ind\"" .../web/js/panel .../web/css/panel.css` -> no output. Diff shows `.nm`->`.fname`, `.ind`->`.nested` in tree.js and panel.css; cards.css and triage.css untouched (not in the diff list). VERIFIED.

3. Priority toggles, judged at 7b8b87c.
   postit.css diff: `.lbtn { border: 0; font: inherit; }` and `.lbtn[data-pf]::before { content: none; }`; priority.js buttons carry `data-pf`, filter.js label buttons do not, so label squares stay. VERIFIED.

4. Front matter in the drawer, judged at 7b8b87c.
   `node --input-type=module -e` importing markdown.js `renderMarkdown`:
   - `---\ntype: cr-answers\ndescription: a <b> x\n  more\n---\n# Hi\n\ntext` -> `<dl class="fm"><dt>type</dt><dd>cr-answers</dd><dt>description</dt><dd>a &lt;b&gt; x more</dd></dl><h3 class="md-h1">Hi</h3><p>text</p>`
   - BOM + `---  ` -> dl then `<p>body</p>`; CRLF -> dl then `<p>b</p>`
   - unclosed `---\na: 1\n# H` -> `<p>--- a: 1</p><h3 ...>H</h3>` (as today)
   - empty front matter -> no dl, `<p>x</p>`.
   CSS `.panel .doc .fm` grid `auto 1fr`, `--text-small`, dt `--ink3`, dd `--ink2`, `overflow-wrap: anywhere`, no border/fill. `wc -l markdown.js` -> 120 (< 300); reader is its own function `readFrontMatter`. Editor untouched (no editor file in the diff). VERIFIED.

5. No change under hooks/ or types/: `git diff --name-only 5b86c93f HEAD | grep -E "^(hooks|types)/"` -> empty. VERIFIED.

6. Screenshots (evidence/before-*.png at 5b86c93, after-*.png at head), opened as images:
   - drawer: before shows grey boxed names offset from icons, unaligned sizes, `--- type: cr-answers description: ... ---` as one line; after shows plain rows, sizes right-aligned on one x, key/value list (type, description, status) in muted grey. Matches the claims.
   - kanban: before shows outset bordered priority and label chips with grey squares on priorities; after shows borderless chips, no square on priorities, labels keep their coloured dots.
   - batch (after only is in the PR? not in the description): shows real CR titles; demo data had real titles already, so no before/after contrast (the PR's Known gaps says so).
   - Privacy: all four viewed images show only `shop-api` / `batch-03` made-up data, no username or home folder path. VERIFIED.
   Note: `verifier/evidence/before-after.md` was not written by me and the images sit in the CR's `evidence/` folder (captured by the Driver's side); the pairs were not re-captured by me, they were opened and judged as above.

7. PR description (gh pr view 300, head 7b8b87c): sections, Known gaps and details render; Summary, Deliverables and Changes match the diff (14 files; each listed; lifecycle/backlog.py, close_archive.py, facts.py, driver.py named). Known gaps names the pane screenshot ("No screenshot of the pane from a real session"), the missing "---" title screenshot and opening.py's unchanged lists. No role names as doers. Images are the demo-data captures above. Test plan checkboxes still hold `<sha7>` placeholders (Driver to fill with Verified at 7b8b87c once the verdict is in). Review box: log shows `r3 inspector approved at 5b86c93f..., committed as 7b8b87c4`, which proves the review for 7b8b87c. VERIFIED.

8. Gates: Driver note `just check: pass (484 tests); just eval-dry-run: pass` at 7b8b87c; CI note 5 jobs green incl. scenario (not re-run by me; not claimed as my proof). No local long gate pass at this head (ship's `off` line): owed by the stack-top rule if this CR is on top.

Pane screenshot from a real session: not captured, named Known gap, not a failure.

VERIFIED

## Description pass (posted description of PR 300), judged at 7b8b87c46a286cbfa17c969e78a1a0a8fcc07173

Head: 7b8b87c46a286cbfa17c969e78a1a0a8fcc07173

- Consistency: `git diff --stat 5b86c93f HEAD` lists 14 files, all named in the Changes section (tree.js, panel.css, markdown.js, postit.css, files.py, views.py, stages.py, lifecycle/backlog.py, board/crs.py, close_archive.py, facts.py, driver.py, tests/test_titles.py; board/backlog.py carries the FRONTMATTER move, stated). No unmentioned change. PR base is cr-335; the cards in `base...HEAD` are the base's, not this CR's.
- Renders: sections, tables, fold, code block fine; four images fetched with curl (200 image/png), sha256 equal to evidence/before-*.png and after-*.png (drawer, kanban) captured at 5b86c93 and 7b8b87c.
- Image look: after-drawer opened, made-up paths (shop-api, 4-batch/2-actives/145-...), no username or home folder. Other three carried from the first pass's look (same sha256).
- Known gaps lists the title screenshot, pane screenshot and opening.py limits; no UNVERIFIED bullet missing. No STALE mark.
- Review box: `$CHANTIER log` has "r3 inspector approved ... committed as 7b8b87c4".
- CI: `gh pr checks 300`: five jobs pass (check x3, eval-dry-run, scenario ubuntu).
Description pass: VERIFIED
