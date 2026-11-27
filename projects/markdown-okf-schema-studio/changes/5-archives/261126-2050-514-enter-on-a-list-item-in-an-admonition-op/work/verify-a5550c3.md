# CR-514 verification

Head: a5550c32100a24e646efdf293db93cdac30e3cba

Base of every "before": `cd3b8e6a8f02c18e3bca13aa5a32259ef01f720f`. First verification of this
change; nothing is carried from an earlier judgment. Verdict at the end: NOT VERIFIED (three
claims fail; everything else listed holds).

Placeholders: `<wt>` the CR worktree; `<base>` = `<wt>/out/vbase`, a detached worktree of the base;
`<repro>` = the folder `verifier/repro` beside this file; `<node>` =
`fnm exec -- node --import ./scripts/register-myst-patches.mjs`; `<chantier>` the CLI of the brief
with `--batch batch-09`. All commands run from `<wt>` unless said otherwise. Before and after
captures: `verifier/evidence/before-after.md`.

## The head moved on the forge during this verification

Judged at a5550c32. The branch was restacked on the forge (head
`4e4eeb4eb548fc4a8f05838f6d0257b76d6b9f0e`, base `223a8c49a47f8af786412e7cff748860b18d3782`); the
worktree was not fetched and stays at a5550c32. The judgments below apply to 4e4eeb4 because the
patches and trees are identical.

- Command: `git show --no-textconv --format=%H <sha> | git patch-id --stable` and
  `gh api repos/gsemet/markdown-okf-schema-studio/commits/<sha> -H "Accept: application/vnd.github.patch" | git patch-id --stable`
- Output: 54a3ac4a and c506f050 both `71fd5b0739ba76dbfec8911af04a72031c56343c`; a5550c32 and
  4e4eeb4 both `087865f1fd99690b67f7e5cf01893100d4b4267b`.
- Command: `git rev-parse <sha>^{tree}` and `gh api .../git/commits/<sha> --jq .tree.sha`
- Output: cd3b8e6a and 223a8c49 both `e6f6894de333c24969709306715c4f3c06d06418`; a5550c32 and
  4e4eeb4 both `43825577ca55366cfb0fac9a2596b99ca1744dd8`.
- Command: `gh pr view 540 --json headRefOid,baseRefOid,isDraft,state`
- Output: `{"baseRefOid":"223a8c49...","headRefOid":"4e4eeb4e...","isDraft":true,"state":"OPEN"}`

## Failed claims

### F1. "Nothing ever cuts or writes into a fence": NOT VERIFIED (judged at a5550c32)

Claimed by: PR "Autonomous decisions" ("Inside a box, a directive that shares no block of its own
opens as a whole directive, and text on an opening line opens its directive, so that nothing ever
cuts or writes into a fence"); `requirements/tiers/log.md` ("never cuts a fence"); BLOCK-014
criteria ("maps a block only on lines that hold no fence line of a directive around it"); also
against "a block of the body opens on its own lines" (PR Changes) and "Enter then opens that
element only" (specification). Not in Known gaps.

- Command: `<node> <repro>/gesture.js <wt> <repro>/gap-note.md "Step one" enter erase` (source: a
  `::::{note}` holding the item `Step one` with a captioned `{table}` nested in it)
- Output: `enter on "Step one" opens <p> lines 2-4`;
  `editor text: "- Step one\n\n  ```{table} Caption\n"`; after commit (writes: 1):
  `"::::{note}\n\n  | a | b |\n  | - | - |\n  | 1 | 2 |\n  ```\n::::\n\nAfter.\n"`
- Same with `<repro>/gap-alert.md` (alert): opens `<p>` lines 2-4, same editor shape, the directive
  line and caption are erased, the closing fence stays.
- Command: the same with `<repro>/gap-fig.md "Caption text"` (a `{figure}` in a list of a note)
- Output: `opens <p> lines 5-7`; `editor text: "  Caption text\n  ```\n\n"`; after commit:
  `"::::{note}\n- item\n\n  ```{figure} x.png\n\n- next item\n::::\n"` (the closing fence is gone)
- Command: `<node> <repro>/figrender.js <wt>`
- Output: gap-note and gap-alert after: `<table>...</table><pre><code></code></pre>` inside the box,
  no caption; gap-fig after: `<figure class="numbered"><img src="x.png"></figure>`, no caption.
- Command at the base: the same three with `<base>` and without `erase`
- Output: Enter opens the whole `<aside>` (lines 1-9, 1-8, 1-9): no fence is cut there.
- Unchanged text writes nothing (writes: 0). A click on "Step one" opens the whole item (lines
  2-8): only Enter cuts.
- Command: `fnm exec -- node <repro>/make-corpus.js <corpus>`, then `<node> <repro>/property.js <wt> <corpus>`
- Output: `{"docs":280,"opens":4321,"openCuts":14,...}`; the 14 `OPEN-CUT` lines are paragraphs in
  list items inside boxes, opened with Enter, in nested corpus documents.
- The figure shape is not new outside a box: `<node> <repro>/gesture.js <base> <repro>/top-fig.md "Caption text" enter`
  (a `{figure}` in a top-level list) and the same with `<wt>` both give `opens <p> lines 4-6`,
  `editor text: "  Caption text
  ```

"`. Inside a box it is newly reachable.

### F2. Known gap on images, second half: NOT VERIFIED (judged at a5550c32)

Claimed by PR "Known gaps": "An image-only paragraph or an `{image}` directive in a box does not
open on its own with a click, and the move chord of a neighbouring block swaps that block across
it." The first half holds; the second is false in every shape tried.

- Command: `<node> <repro>/image-gap.js <wt>`
- Output: 58 chord attempts whose two blocks sit on both sides of the image, 58
  `ACROSS-IMAGE: refused (Text between the two blocks (a comment or a link definition) prevents the move.)`,
  0 `ACROSS-IMAGE: MOVED`.
- Command: `<node> <repro>/image-gap2.js <wt>` (five image spellings, seven neighbour kinds on each
  side, with and without blank lines, note and alert)
- Output: `{"shapes":980,...,"crossing":970,"crossingMoved":0,"reasons":{"Text between the two blocks (a comment or a link definition) prevents the move.":970}}`
- Code at the head: `src/core/mapping/blockMove.ts` refuses a swap unless every line between the two
  blocks is blank (`if (!separator.every(isBlank))`).
- First half: same output, `"image-only paragraph | blank | whole box": 98` of 98 and every
  `{image}` shape `whole box`. A linked-image or two-images paragraph opens its own `<p>`.
- Not tried: shapes outside those two probes (for example a quote or a card inside a box).

### F3. The move chord moves a block among the body's blocks: NOT VERIFIED (judged at a5550c32)

Claimed by: PR Deliverables ("the block (for an item: its list) moves among the body's blocks"),
Changes, the CHANGELOG line, specification section 2 ("MyST accepts it"). Not in Known gaps. Moving
a block so that a thematic break becomes the first line of the body empties the whole box in the
preview.

- Command: `<node> <repro>/firstplace.js <wt>` (body `Before.` / `---` / `After.`, chord down on
  "Before.")
- Output, colon note: `moved`, written `":::{note}\n\n---\n\nBefore.\n\nAfter.\n:::\n"`, rendered
  `<aside class="admonition note"><p class="admonition-title">Note</p></aside>` (before the chord:
  title, "Before.", rule, "After."). Backtick note and alert: the same
  (`"> [!NOTE]\n>\n> ---\n>\n> Before.\n>\n> After.\n"`, title only).
- Command: `<node> <repro>/kinds2.js <wt>`
- Output: `{"moved":276,"broken":8}`: six are the thematic break (note, alert; a `{dropdown}` is
  then not rendered at all: `[0,[]]`), two a heading moved to the first line of a colon note.
- Same output of `firstplace.js`: a heading moved first in a MyST note becomes the box title
  (`<p class="admonition-title">Head</p>`); an alert and a field list keep their title.
- Erasing the paragraph above the rule does the same: `<node> <repro>/gesture.js <wt> <repro>/hr-note.md "Before." click erase`
  writes `":::{note}\n\n\n---\n\nAfter.\n:::\n"`, which renders as the title only.
- Base: `<node> <repro>/render2.js <base>` renders such a note as the title only too (the renderer
  is not new); on the base a gesture inside a box opens the whole box
  (`gesture.js <base> ... hr-note.md "Before." click`: `opens <aside> lines 1-7`), so no inner
  move or erase writes that document.
- The text stays in the file.

## Claims that hold

### Gate, handoff and CI: VERIFIED (a5550c32; CI at 4e4eeb4)

- Command: first line and result lines of `work/gates/prepush-a5550c3-preflight.log`
- Output: `head a5550c32100a24e646efdf293db93cdac30e3cba base cd3b8e6a8f02c18e3bca13aa5a32259ef01f720f: just preflight`;
  clip-kit `tests 56 pass 56 fail 0`; unit `tests 5431 pass 5423 fail 0 skipped 8`; security
  `tests 116 pass 116 fail 0`; `1228 requirements, 0 errors, 26 warnings`; `ci-static: passed`;
  `preflight: visual, viewer-graph, integration, acceptance, report and gallery stages skipped on Windows; CI runs them`;
  `exit 0`.
- Command: `<chantier> handoff CR-514`
- Output: note "before push at a5550c32... just preflight exit 0 ... tree clean"; "move
  a2ebb0e..a5550c3 (conflict) inspector approved at a5550c32..."; long gate "none in chantier.yaml";
  "verdict VERIFIED" unchecked.
- Command: `gh pr checks 540 -R gsemet/markdown-okf-schema-studio`
- Output: `static`, `static-windows`, `visual`, `visual-2`, `viewer-graph`, `report`, `checks` pass;
  `integration`, `acceptance`, `stress`, `toc-loop`, `release-check`, `gallery` skipping.

### New tests pass at the head and fail on the base: VERIFIED (a5550c32)

- Command: `<node> --test --test-reporter=spec` on `out/test/session/{alertBlockEditOpen,boxBlockSourceLines,emptiedBlockDelete}.test.js`,
  `out/test/core/edits/sourceEdits.test.js`, `out/test/core/mapping/blockMove.test.js`,
  `out/test/page/{runtimeBlockMoves,runtimeStructuralNavigation,blockReq.requirements}.test.js`,
  `out/test/site/e2eGroups.test.js`, after `fnm exec -- npm.cmd run compile`
- Output at the head: `tests 212 pass 212 fail 0`.
- Output in `<base>` (the head's `test/` over the base `src/`; the two head-only source files
  present, imported by no base code): `tests 212 pass 155 fail 57`.
- Every test the PR names is `✖` on the base and `✔` at the head: Enter on an element of a MyST
  admonition and of a GitHub alert; a click on a paragraph of a MyST admonition; Right, Down, Right
  into a list item; Down and Up at the ends of a list; the chord in a block editor; two blocks of an
  alert body swap; an erased paragraph of an alert body (LF, CRLF, lone CR).

### `boxBlockSourceLines.test.ts`: 22 tests, 14 and 5: VERIFIED (a5550c32)

- Command: that test file in `<base>` with the base renderer, then with `mystBoxLines.ts` and
  `mystUnclosedFences.ts` of 54a3ac4a (checked out in `<base>`, recompiled)
- Output: base renderer `tests 22 pass 3 fail 19` (14 renderer tests and 5 unclosed-fence tests
  fail; the 3 `{table}` and card tests pass); with 54a3ac4a's two files `pass 17 fail 5` (the
  unclosed-fence tests); head `22 pass` (in the 212).

### Pointed or selected element opens; title, frame or selected box opens all: VERIFIED outside F1 (a5550c32)

- Command: `fnm exec -- npm.cmd run visual:render`, then
  `.venv/Scripts/python.exe test/visual/capture.py --scenario <id>`, at the head and in `<base>`
- Output at the head: pass for `gfm/v14`, `gfm/v15`, `block-editing/v57`, `v58`, `v59`, `v27`,
  `v36` to `v39`.
- Output in `<base>`: `v14`, `v57`, `v59` fail; `v15`, `v58`, `v27`, `v36`, `v38` pass.
- `block-editing/v04` fails the same way on both ("paragraph editor caret is not at the clicked
  word (selectionStart=63, clicked_word=None)"): not this change's.
- Screenshots: title clicks are pixel-identical before and after; body clicks and keyboard Enter
  change from the whole box to the block. Opened: no user name or home folder.
- Command: `<node> <repro>/gaps.js <wt>` and `<base>`
- Output: head `<p 2-2> "First." click=<p 2-2> enter=<p 2-2>`, base
  `click=<aside 1-6> enter=<aside 1-6>`; nested tip and alert in a list item open their own block;
  version admonition body `<p 7-7> "Late body."` (base `<p 5-5>`), so it maps its written lines;
  `versionadded` with an inline body opens the whole directive.
- Hover follows the click rule: `editMode.ts` calls `editingElementFor(mapped).element`, tested.
- Enter on the box selected as a whole opens all of it: the page tests in the 212-test run.
- In the editor of an alert block the `> ` markers are part of the text: `gesture.js` on
  `gap-alert.md` shows `editor text: "> - Step one
..."`.
- Diagram, formula, code, `{list-table}`, `{csv-table}` directives and one-line opening-line text
  open whole: the 22 tests of `boxBlockSourceLines.test.ts` pass (above).

### Blocks outside a box are mapped as before: VERIFIED (a5550c32)

- Command: `<node> <repro>/diff-outside.js <wt> <base> .` and the same over the generated corpus
- Output: `files=2176 errors=0 outsideBoxMappingDiffs=0 insideBoxMappingDiffs=0 htmlDiffsBesidesLineAttributes=0`;
  corpus `files=401 errors=0 outsideBoxMappingDiffs=0 insideBoxMappingDiffs=117 htmlDiffsBesidesLineAttributes=0`.

### Move chord limits and refusals: VERIFIED (a5550c32)

- Command: `<node> <repro>/gaps.js <wt>` ("neighbouring rules", "topic in a note")
- Output: `no neighbour, nothing sent` for blocks inside an item, a paragraph in a quote and in a
  card (an item's editor moves its list: page tests above); body blocks swap inside the box.
  `kinds.js`: a `{div}` body does not move and
  nothing moves past it. The `{table}` cases are in the tests (above).
- Command: `<node> <repro>/refusal.js <wt>`
- Output: `planner, alert block and the paragraph after the alert: {"refused":"The preview is out of date. Refresh it and try again."}`
  (decision "different quote prefixes"); whole quotes still swap as blocks; a link definition or a
  `%` comment between two alert blocks: "Text between the two blocks (a comment or a link
  definition) prevents the move."
- The refusal reason shown next to the insert point: asserted by `runtimeBlockMoves.test.ts`
  (status role), passing above.
- A neighbour that is not a direct block stops the chord (decision): `kinds.js` `{div}` row
  `Before down: none; K up: none; K down: none; After up: none`.
- Note: step 6 of the specification's evidence names `<!-- x -->` as a refusing case; it moves (a
  comment is a mapped chip, as at top level). Not a claim of the PR.

### Down and Up at the edges of a list keep the editor: VERIFIED (a5550c32)

- Command: the 212-test run above. Output: `✔ Down at the end of the last item and Up at the start of the first, of a list in an admonition, keep the editor` (`✖` on the base).

### Erased alert block keeps the alert: VERIFIED (a5550c32)

- Command: `<node> <repro>/gaps.js <wt>` and `<base>` ("alert block, no lazy line")
- Output: head `erase 2-2: writes=1 -> "> [!NOTE]\n>\n>\n> Second.\n>\n> Third.\n"`, one admonition,
  no plain quote (also after autosave then commit, and indented in a list item); base writes an
  empty line and renders one plain quote beside an alert reduced to "Note". A MyST note writes the
  same text on both.

### Open admonition no longer scrolls, palette clear of the text box: VERIFIED (a5550c32)

- Command: `git show HEAD:src/core/preview/styles/admonitionEditStyles.ts`: `.admonition:has(.sphinx-preview-block-editor-host) { overflow: visible; }`
- Command: the same rule forced to `auto` in the built file, render, capture `v57` and `v59`, then
  recompiled
- Output: both fail "the palette of the open editor ends above its text box"; with the shipped rule
  both pass. "Wide content does not scroll meanwhile" follows from that rule (not captured).

### Keyboard navigation clip: VERIFIED from its committed files (a5550c32)

- Command: read `docs/demo-video/clips/keyboard-navigation/check.json`, contact sheet, frames and
  GIF (LFS files)
- Output: `"passed": true`, `"length": 26`, 15 presses, MP4 543383 B, WebM 368400 B, GIF 1696690 B,
  960 px, 12 fps, 128 colours, `"ladderStep": 0`, `loopSeamSsim 0.99037`, VS Code 1.147.0, extension
  1.12.1 from a vsix, win32; GIF 960x540, 312 frames; frames show the walk into the nested sub-item
  and Enter opening that line; no user name or home folder.
- `poster.png`, `01-selected.png`, `edit-on.png` are unchanged files; SSIM against the new MP4
  1.000000, 0.999953, 0.999997.
- The storyboard test passes (clip-kit 56/56 in the gate log).
- The take was filmed in round 2, before the unclosed-fence fix and the rebase on CR-513; neither
  touches the closed note it films. No new take and no real VS Code window here.

### Other Known gaps: VERIFIED (a5550c32)

- `{table}` in a box, `{topic}` paragraphs: `gaps.js` and the tests (above).
- Quoted colon admonition left open: `<node> <repro>/quoted3.js <wt>`: quoted `:::{note}` with a
  final `> :::{tip}` ... `> :::` gives `admonition tip[unmapped]`. Wording note: when both are
  written at one quote level under `> ::::{note}`, the tip does open on its own (`gaps.js`).
- Outside a box: `gaps.js` head and base alike: chord down on "Before." moves it inside a
  top-level `{mermaid}`, `{math}`, `{code-block}` fence, and a click on those maps the opening line
  only. The top-level `{table}` ("likely affected, not tried") is affected with a caption
  (`"```{table} Caption\n\nBefore.\n\n| a | b |..."`) and refused without one.
- Lazy continuation line: `gaps.js` head, `erase 4-5` writes
  `"> [!NOTE]\n> First.\n>\n\n>\n> Third.\n"`, one plain quote outside the alert.
- After the save the selection is on the whole admonition, and the contact sheet (12 tiles) shows
  neither the list nor the sub-list selection while `frames/list-selected.png` and
  `sublist-selected.png` do: seen in the committed images. The specification's evidence asked the
  contact sheet to show each selection: unmet, disclosed.
- The edited replay runs only on main or a heavy run: `integration` is skipping on this PR (above).
- Maintainer review pending: stated by the brief; no approval seen.

### Requirements, markers, changelog, user guide, replay edit: VERIFIED (a5550c32)

- Command: `git diff --name-only cd3b8e6a HEAD`
- Output: `requirements/tiers/log.md`, BLOCK-014, 017, 079, 109, 117, 130, 254, 260, 262, 264, the
  block-editing index, MYST-001, PALETTE-021, `CHANGELOG.md`, `docs/user/editing.md`, tests; no StRS
  file and no `skills/` file.
- Command: `git diff cd3b8e6a HEAD -- requirements | grep -cE "^[+-]req_lifecycle"`: `0`.
- Markers and lint: `just preflight` in the gate log (0 errors).
- `git diff ... -- test/integration/realInput/qa210Replays.ts`: the lazy-line replay now clicks the
  alert's title, assertions unchanged (decision, and the commit message says so).
- The CHANGELOG line has one entry under Unreleased naming CR-514 and PR #540; its "moves a block of
  its body" and "that element only" parts are limited by F1 and F3.

### PR description form: VERIFIED apart from F1, F2, F3 (a5550c32)

- The posted body equals `work/pr-body.md` but for a trailing newline (`gh pr view 540 --json body`
  compared). Template sections plus Autonomous decisions and Known gaps; the only internal reference
  is under Internal references, last before the Claude Code line; title
  `feat(editor): edit the pointed block inside admonitions and alerts`.
- Command: `git grep -nE "(function|const) (mapBoxSourceLines|editingElementFor|planBlockMove|planAlertPlaceholder)\b" -- src`
- Output: `sourceEdits.ts:339`, `blockMove.ts:107`, `mystBoxLines.ts:194`, `mappedBlocks.ts:187`:
  the diagram's names exist.
- Command: `curl -sIL` on the GIF, MP4 and WebM raw URLs at a5550c32: `200` for each. An earlier
  download of the three in this verification had the committed files' sizes and SHA-256 prefixes
  (`e6775d0b4ccba840`, `8e9bbc83d9df3199`, `c45ca335cf42e475`).
- No image shows a user name or home folder; no STALE marker. Test plan boxes and screenshots are
  absent on purpose (brief), so not judged.

## Limits and one deviation

- No real VS Code window, no new take, no macOS or Linux run of mine; integration, acceptance and
  stress did not run in CI for this PR.
- Browser behaviour is covered by the visual harness and DOM-level page tests only.
- Deviation: early in this verification I wrote five raw logs (`base-bundle`, `base-render`,
  `base-tests`, `head-render`, `head-tests`, `.log`) to the session scratchpad, outside my writes
  folders. I delete those five files at the end; nothing here depends on keeping them.

NOT VERIFIED
