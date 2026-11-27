# CR-514 verification

Head: f9dc2c630b852635e8bffcd0b00b42cc886b293c

Base of every "before": `5f0746d79ca28e564841daa19288075aa7823776` (`origin/main`). Fourth
verification, a short pass on the posted description of pull request 540. The first verdict at this
head is kept as `verify-f9dc2c6-first.md` (NOT VERIFIED on its claim C, the card sentence of Known
gaps). The code did not change since; the description did. Verdict at the end: VERIFIED.

Placeholders: `<wt>` the CR worktree; `<r3>`, `<r4>` = the folders `verifier/r3`, `verifier/r4`
beside this file; `<node>` = `fnm exec -- node --import ./scripts/register-myst-patches.mjs`, run
from `<wt>`; `<chantier>` the CLI of the brief with `--batch batch-09`; the other placeholders of the
carried claims are `<base>` = a detached base worktree used by the first verdict (since removed),
`<repro>` and `<r2>` = `verifier/repro` and `verifier/r2`.

## Judged in this pass

### D0. Only three Known gaps bullets changed: VERIFIED (f9dc2c6)

- Command: `gh pr view 540 --json number,headRefOid,isDraft,title,body,updatedAt,state,baseRefName`
  (saved as `verifier/pr-540-f9dc2c6-second.json`); `git rev-parse HEAD`
- Output: head `f9dc2c630b852635e8bffcd0b00b42cc886b293c` on both, draft, OPEN, base `main`, same
  title, updated `2026-11-26T19:39:07Z`.
- Command: `python -I verifier/desc-diff.py <work>` (the body judged by the first verdict,
  `pr-540-f9dc2c6-end.json`, against the one posted now; log `verifier/desc-diff-f9dc2c6.log`)
- Output: `old chars 14243 new chars 14542 local chars 14542`,
  `posted equals pr-body.md (trailing newline ignored): True`, and three `replace` hunks only: the
  bullets "Clicking the first paragraph of a tight list item", "Emptying the first block of a box
  body" and "A card of a box". Nothing else is new.

### D1. The card bullet (failed before as claim C): VERIFIED (f9dc2c6)

Posted: "A card of a box loses words of its body when a `---` line that no second `---` line closes
stands right under the card's opening line (it is read as the start of a block of options), and a
`{div}` that is not shown as a box (the callout class written as its argument) and starts with `---`
stops the preview (both as before this change); the move chord does not refuse to write that in such a
`{div}`."

- Command: `<node> <r4>/three.js <wt> C` (log `r4/three-C-f9dc2c6.log`)
- Output: with the unclosed line right under the opening line, all 7 body shapes in all 4 card
  spellings lose a word (`missing=Beta`, and `missing=Alpha` for the one-word body); the DOM shows the
  lines read as options (`<code .shiki.language-yaml>`). A closed block and a `---` after a blank line
  show every word (`missing=-`). The three `{div}` callout-argument spellings throw
  (`THROWS Cannot read properties of undefined (reading 'length')`) for every body that starts with
  `---`, blank line first or not; a closed options block draws.
- Command: `<node> <r3>/cards2.js <wt>`, then `cmp` with `r3/cards2-5f0746d.log` (base)
- Output: `cards2-same-as-base`: 315 pages, byte-identical to the base ("as before this change").
- Command: `diff` of the "cards and divs with dashes" section of `r3/gapsC-f9dc2c6.log` and
  `r3/gapsC-5f0746d.log`
- Output: `cards-and-divs-section-same-as-base` (the `{div}` throws on the base too).
- Command: `<node> <r2>/calloutdiv.js <wt>`, then `cmp` with the first verdict's log
- Output: `calloutdiv-same`: in `{div} with class argument, ---` the chord answers `ok=true`, writes
  the `---` first and the page `THROWS`; the `:class:` spelling and the fence div are refused.

### D2. "Emptying the first block of a box body": VERIFIED (f9dc2c6)

- Command: `<node> <r4>/three.js <wt> B` (log `r4/three-B-f9dc2c6.log`: click the first paragraph,
  empty the editor through `PreviewManager`, render again; every case keeps `Lastword kept=true`)
- Output: `{admonition}` with a title, 10 spellings (colon and backtick fence, `:class: dropdown`,
  also with `:open:`, `:class: tip`, `:class: tip dropdown`, `:name:`, a title with markup): title
  "Admonition", its own title as a body paragraph, nothing else of the box. `{note}`, `{tip}`,
  `{warning}`, alert, callout, callout with a `title` attribute: the title only. `{dropdown}`: no box.
  `{dropdown}` with `:open:`: `after THROWS value.replace is not a function`.
- The heading half of the first sentence is unchanged: carried from f9dc2c6 (`gapsC-f9dc2c6.log`:
  `note|heading` after shows "Headword" as the title).

### D3. "Clicking the first paragraph of a tight list item": VERIFIED (f9dc2c6)

- Command: `<node> <r4>/three.js <wt> A` (log `r4/three-A-f9dc2c6.log`: 8 following contents in a
  note, a dropdown and an alert; the arrows walked with the real `structuralMove`; each editor emptied)
- Output: "click on first paragraph" opens the `<li>` with the following content in all 24 cases and
  `after emptying, content left=false`. "Enter on the item" (`block 1, Right, Right`) does the same in
  all 12 HTML comment and HTML cases.
- Observation, not counted: Enter on the whole item takes the hidden content for the other listed
  kinds too. What differs by kind is Enter on the item's first paragraph (one Right further): of the
  listed contents it takes only an HTML comment or HTML written with no blank line before it. The
  sentence is true as written and does not say otherwise.

### D4. The posted description renders, with no new claim, name or mark: VERIFIED (f9dc2c6)

- Command: `gh api repos/gsemet/markdown-okf-schema-studio/pulls/540 -H "Accept: application/vnd.github.html+json" --jq .body_html`,
  then `python -I <r4>/rendered.py <r4>/pr-540-body.html` (log `r4/rendered-f9dc2c6.log`)
- Output: headings `Summary, Deliverables, Changes, Impacts, Blast radius, Autonomous decisions,
  Known gaps, Test plan, Internal references`; each of the three bullets renders as one list item with
  its whole text. Their text (D0) names no role as a doer, no person and no path, and adds no mark.
- Command: `gh pr checks 540`; `git ls-remote origin refs/heads/main <branch>`; first and last lines
  of `work/gates/prepush-f9dc2c6-preflight.log`; `<chantier> handoff CR-514`
- Output: `checks`, `report`, `static`, `static-windows`, `viewer-graph`, `visual`, `visual-2` pass,
  the others skipping; branch `f9dc2c63...`, main `5f0746d7...`;
  `head f9dc2c630b852635e8bffcd0b00b42cc886b293c base 5f0746d...: just preflight`, `exit 0`,
  `tree checked`; handoff: rounds 6 of 6, head f9dc2c6.

## Carried claims

### Previous claim A, Enter on a formula of a list in a box: fixed, VERIFIED (f9dc2c6)

_carried from f9dc2c6: same head, and none of the description text it judges changed (claim D0)._

- Command: `<node> <r3>/formula.js <wt> <r2>/shapes/dollar-*.md`
- Output (`formula-f9dc2c6.log`): `held=true` 41 times, `held=false` 0: the click and Enter on
  every element that shows the formula open lines that hold all of it (one-blank shape: `<li>` 2-7,
  `<p>` 2-5; the formula is no block of its own).
- Command: `<node> <r2>/items.js <wt>`:
  `{"docs":4050,"opens":135025,"cuts":0,"overlaps":0,"inBoxItems":6180}` (135 overlaps at 739f9e3).
- Command: `<node> <r3>/items-md-label.js <wt>`:
  `{"docs":4275,"opens":114298,"cuts":0,"overlaps":0,...,"wrong":268}`. The probe now reads a
  `$$ (label)` line as a closing fence; the `wrong` lines are comment shapes, where the probe expects
  the text of a comment chip in the source lines.

### Previous claim B, a `{div}` callout and the chord: fixed, VERIFIED (f9dc2c6)

_carried from f9dc2c6: same head, and none of the description text it judges changed (claim D0)._

- Command: `<node> <r2>/calloutdiv.js <wt>`
- Output (`calloutdiv-f9dc2c6.log`): with `:class: callout-tip`, `---` and a heading are refused
  with their reasons, the document unchanged; the fence-div control is refused too.
- Command: `<node> <r2>/attack.js <wt>`: `{"docs":5040,"moved":10328,"refused":1077,"broken":78}`,
  every broken case the disclosed bold-only paragraph.
- Command: `<node> <r3>/spell.js <wt>` (ways to write the callout class):
  `{"spellings":1848,"boxes":1280,"sent":1280,"moved":88,"refused":1192,"broken":0,"throwsSource":0}`
- `:::{div} callout-note` renders no box: the move is accepted and the page then throws (disclosed
  in Known gaps).

### Gate, handoff, pull request and CI: VERIFIED (f9dc2c6)

_carried from f9dc2c6: same head, and none of the description text it judges changed (claim D0)._

- Command: first line and result lines of `work/gates/prepush-f9dc2c6-preflight.log`
- Output: `head f9dc2c630b852635e8bffcd0b00b42cc886b293c base 5f0746d79ca28e564841daa19288075aa7823776: just preflight`;
  clip-kit 56/56; unit `tests 5503 pass 5495 fail 0 skipped 8`; security 116/116;
  `1228 requirements, 0 errors, 26 warnings`; `ci-static: passed`;
  `preflight: visual, viewer-graph, integration, acceptance, report and gallery stages skipped on Windows; CI runs them`;
  `exit 0`.
- Command: `<chantier> handoff CR-514`
- Output: rounds 6 of 6; before push at f9dc2c6 preflight exit 0, tree clean; r6 approved at
  8539f1cc and committed as f9dc2c630; CI green; long gate none.
- Command: `gh pr view 540 --json title,headRefOid,baseRefOid,isDraft,state,body`; `gh pr checks 540`;
  `git ls-remote origin refs/heads/main <branch>`
- Output: head f9dc2c6, base 5f0746d, draft, OPEN, `feat(editor): edit the pointed block inside
  admonitions and alerts`; remote heads the same. `checks`, `report`, `static`, `static-windows`,
  `viewer-graph`, `visual`, `visual-2` pass; `acceptance`, `integration`, `stress`, `toc-loop`,
  `release-check`, `gallery`, `pages`, `release`, `tag-release` skipping.

### New tests pass at the head and fail without their change: VERIFIED (f9dc2c6)

_carried from f9dc2c6: same head, and none of the description text it judges changed (claim D0)._

- Command: `fnm exec -- npm.cmd run compile`, then `<node> --test --test-reporter=spec` on
  `alertBlockEditOpen`, `boxBlockSourceLines`, `emptiedBlockDelete`, `core/edits/sourceEdits`,
  `core/mapping/blockMove`, `page/runtimeBlockMoves`, `page/runtimeStructuralNavigation`,
  `page/blockReq.requirements`, `site/e2eGroups` (`.test.ts`)
- Output (`tests-head-f9dc2c6.log`): `tests 284 pass 284 fail 0 skipped 0`; the box file alone 94/94.
- The same files in `<base>` (head `test/` and the three head-only source files over the base
  `src/`; 4 expected type errors, JavaScript emitted): 284 tests, 177 pass, 107 fail
  (`tests-base-f9dc2c6tests.log`); box file 23 pass, 71 fail.
- Every test title the Test plan lists passes at the head and fails on the base.
- `src` of 8539f1c with the head's tests: box file 47 pass, 47 fail (`tests-8539src-box.log`): the
  tests of the last commit fail without it. "holds 94 tests. Most fail without the change they
  cover" holds.

### Pointed or selected element opens; title, frame or selected box opens all: VERIFIED (f9dc2c6)

_carried from f9dc2c6: same head, and none of the description text it judges changed (claim D0)._

- Command: `fnm exec -- npm.cmd run visual:render`, then
  `.venv/Scripts/python.exe test/visual/capture.py --scenario <id>` for the five scenarios of
  `verifier/evidence/before-after.md`
- Output (`visual-capture-f9dc2c6.log`):
  `{"status": "passed", "scenario_count": 5, "screenshot_count": 5}`; the five images are
  byte-identical to the `after-*.png` (SHA-256 compared).
- `v14`, `v57` and `v59` fail on the base: carried from a5550c3: no visual file changed since, and
  the base tree is identical.
- `v27`, `v36` to `v39`, and an admonition with an open editor that no longer scrolls: carried from
  a5550c3: no style or visual file changed since; CI `visual` and `visual-2` pass at f9dc2c6.
- Command: `<node> <repro>/gaps.js <wt>` (`gaps-f9dc2c6.log`): body blocks open on their own lines
  on click and Enter (`<p 2-2> "First." click=<p 2-2> enter=<p 2-2>`), Enter on a selected box opens
  all of it, a version admonition body maps its written line.

### The other Changes and Deliverables rows: VERIFIED (f9dc2c6)

_carried from f9dc2c6: same head, and none of the description text it judges changed (claim D0)._

- Command: `<node> <r3>/changes.js <wt>`
- Output (`changes-f9dc2c6.log`): the title of a `{div}` callout opens the whole callout, also
  nested (`[=Tip] click -> <aside 1-7>`); a version admonition body maps its written lines and its
  argument text opens the directive; a note left open at the end of the file keeps the closing fence
  of an inner tip and code block; a one-line `:::{warning} Text` and a card title open their
  directive; `{mermaid}`, `{math}`, `{code-block}` with caption and an alert's fenced code open
  whole; the nearest of nested boxes decides; a click inside a box never takes the list around it.

### Blocks outside a box are mapped as before: VERIFIED (f9dc2c6)

_carried from f9dc2c6: same head, and none of the description text it judges changed (claim D0)._

- Command: `<node> <repro>/diff-outside.js <wt> <base> .`, then over `<r2>/corpus`
- Output: `files=2176 errors=0 outsideBoxMappingDiffs=0 insideBoxMappingDiffs=3 htmlDiffsBesidesLineAttributes=0`;
  corpus `files=401 errors=0 outsideBoxMappingDiffs=0 insideBoxMappingDiffs=148 htmlDiffsBesidesLineAttributes=0`.

### Move chord, refusals, Down and Up at list edges: VERIFIED (f9dc2c6)

_carried from f9dc2c6: same head, and none of the description text it judges changed (claim D0)._

- Commands: `<node> <repro>/gaps.js <wt>`, `<node> <repro>/refusal.js <wt>`,
  `<node> <r3>/chords.js <wt>`
- Output: no move from a block in an item, a quote, a card or a grid; body blocks swap inside the
  box; a `{table}` directive does not move and nothing passes it; `{topic}` paragraphs do not move;
  a link definition or comment between two blocks is refused with its reason; an alert block and the
  paragraph after the alert: "The preview is out of date. Refresh it and try again."; a bold-only
  paragraph moves first (disclosed); a move adds the empty line after the opening fence (disclosed).
- `tests-head-f9dc2c6.log`: "a refused move inside an admonition says why next to the admonition's
  insert point", "Down at the end of the last item and Up at the start of the first, of a list in an
  admonition, keep the editor", "two blocks of an alert body swap and keep the quote's empty line
  between them" pass.

### Erased alert block keeps the alert: VERIFIED (f9dc2c6)

_carried from f9dc2c6: same head, and none of the description text it judges changed (claim D0)._

- Command: `<node> <repro>/gaps.js <wt>`
- Output: `erase 2-2: writes=1 -> "> [!NOTE]\n>\n>\n> Second.\n>\n> Third.\n"`, one admonition, no
  plain quote; with a lazy line the later quoted lines leave the alert (disclosed).

### Earlier F1, F2, F3: still fixed, VERIFIED (f9dc2c6)

_carried from f9dc2c6: same head, and none of the description text it judges changed (claim D0)._

- `<node> <repro>/gesture.js` on the captioned `{table}` and `{figure}` shapes (`f1-f9dc2c6.log`):
  lines 2-3 and 5-5, both fences kept. `<node> <repro>/property.js <wt> <r2>/corpus`:
  `{"docs":280,"opens":4315,"openCuts":0,"moves":876,"refused":20,"moveBreaks":0,"erases":0,"eraseBreaks":0}`.
- `image-gap.js`, `image-gap2.js` (`crossingMoved 0`, 970 refusals with the disclosed message),
  `firstplace.js`, `kinds2.js` (`{"moved":268,"broken":0}`): output identical to the run at 739f9e3.

### The other Known gaps: VERIFIED (the sentence failed as C is judged in D1) (f9dc2c6)

_carried from f9dc2c6: same head; every bullet but the three of D1 to D3 is unchanged (claim D0). The observation at its end is replaced by D3._

- Commands: `<node> <r3>/bullets.js <wt>`, `<node> <r3>/bullets2.js <wt>`,
  `<node> <r3>/chords.js <wt>`, `<node> <r3>/gapsC.js <wt>` (logs `bullets*`, `chords*`, `gapsC*`;
  `*-5f0746d.log` for the base)
- Output: every other bullet of "Elements of a box that do not open on their own", "Opening or
  emptying", "The move chord, and drawing" and "Outside a box" shows what it says; the "as before
  this change" ones match the base.
- Observation, not counted: the bullet "Clicking the first paragraph of a tight list item followed
  by hidden content ..." also happens with Enter for an item followed by an HTML comment or HTML.

### Keyboard navigation clip: VERIFIED from its committed files (f9dc2c6)

_carried from f9dc2c6: same head, and none of the description text it judges changed (claim D0)._

- `check.json`: passed, 26 s, MP4 543383 B, WebM 368400 B, GIF 1696690 B, 960 px, 12 fps, 128
  colours, ladder step 0, VS Code 1.147.0, win32; the description's figures match it and `clip.md`.
- `curl -sL` of the three description links (at f9dc2c6): 200, same sizes, byte-identical to the
  worktree files.
- `<node> <repro>/gesture.js` on `stage/release-plan.md` (`clip-f9dc2c6.log`): Enter on "the VSIX"
  opens lines 8-8 `"  - the VSIX\n"`, on "Build the packages" 7-7: the filmed walk matches the head.
- `node --test docs/demo-video/clip-kit/lib/storyboard.test.mjs`: `tests 40 pass 40 fail 0`.
- Opened: 24 frames of the GIF (`<r3>/gif/montage-1.png` to `montage-4.png`), one frame per second
  of the MP4 and of the WebM (`<r3>/gif/video-mp4.png`, `video-webm.png`), the corner badge enlarged
  (`corner-mp4.png`: the product logo, no account picture), `contact-sheet.png`. The walk is E,
  arrows into the note, its list and sub-list, Enter opens `  - the VSIX` alone, the word is
  changed, Ctrl+Enter; then the ring is on the whole note (disclosed). The contact sheet shows no
  selected list or sub-list (disclosed). No user name or home folder in what was opened.
- `git diff --stat 8539f1c f9dc2c6 -- docs/demo-video test/visual test/integration test/shared CHANGELOG.md media skills package.json`
  is empty. The take predates later fixes and awaits the maintainer's review (disclosed).
- The real VS Code replay opens the alert from its title, and runs only on `main` or a heavy run:
  carried from a5550c3: the file did not change; `integration` is skipping on this pull request.

### Requirements, markers, changelog, user guide: VERIFIED (f9dc2c6)

_carried from f9dc2c6: same head, and none of the description text it judges changed (claim D0)._

- Command: `git diff --stat 5f0746d f9dc2c6 -- requirements docs/user CHANGELOG.md`: 17 files.
- `git diff 5f0746d f9dc2c6 -- requirements | grep -cE '^[+-]req_lifecycle'`: `0`; no StRS and no
  `skills/` file in `--name-only` (`0`).
- `grep @implements_req`: `mystBoxLines.ts` BLOCK-014, 130, 254; `boxFirstBlock.ts` BLOCK-124.
- The test names the last commit adds to BLOCK-014, 124 and 254 exist in the box test file
  (`grep -cF`, each at least 1); lint in the gate log: 0 errors.
- The requirements log has dated lines for rounds 5 and 6; `CHANGELOG.md` has one entry under
  Unreleased; the CHANGELOG, user guide and requirement sentences about formulas, tags, options
  blocks and `{div}` callouts agree with the probes above.

### PR description form: VERIFIED (the sentence failed as C is judged in D1) (f9dc2c6)

_carried from f9dc2c6: same head; the template, diagram and name checks stand (claim D0: only three bullets changed). The posted body and its length are judged again in D4._

- Posted body equals `work/pr-body.md` (14243 characters;
  `verifier/pr-540-f9dc2c6-end.json`).
- Template sections plus Autonomous decisions and Known gaps; the only internal reference is under
  Internal references; no STALE mark; no role name as the doer.
- `.venv/Scripts/python.exe <r3>/mermaid-check.py work/pr-body.md <wt>/node_modules/mermaid/dist/mermaid.min.js <r3>/mermaid-pr-body.png`:
  `ok: True`, 9 nodes, 6 edges; opened, readable.
- `git grep` finds `mapBoxSourceLines`, `editingElementFor`, `planBlockMove`,
  `planAlertPlaceholder` and the seven files the diagram names.
- Test plan boxes and before/after screenshots are filled at closing, so not judged.

## Files that may be attached to the pull request

All ten images of `evidence/` hold at f9dc2c6 (details and reproduction in
`evidence/before-after.md`). The two title pairs show no change; the three other pairs show it.
Each image below was opened: no user name or home folder.

Folder of the images:
`C:/Users/gaeta/Projets/gsemet-foss-planning-surface/projects/markdown-okf-schema-studio/changes/4-batch/2-actives/514-enter-on-a-list-item-in-an-admonition-op/work/verifier/evidence/`

- `C:/Users/gaeta/Projets/gsemet-foss-planning-surface/projects/markdown-okf-schema-studio/changes/4-batch/2-actives/514-enter-on-a-list-item-in-an-admonition-op/work/verifier/evidence/before-alert-body-click.png`:
  Before, a click in a note alert's second paragraph opens the whole alert (lines 5-8).
- `C:/Users/gaeta/Projets/gsemet-foss-planning-surface/projects/markdown-okf-schema-studio/changes/4-batch/2-actives/514-enter-on-a-list-item-in-an-admonition-op/work/verifier/evidence/after-alert-body-click.png`:
  After, the same click opens only `> The second paragraph of the note.` inside the rendered alert.
- `C:/Users/gaeta/Projets/gsemet-foss-planning-surface/projects/markdown-okf-schema-studio/changes/4-batch/2-actives/514-enter-on-a-list-item-in-an-admonition-op/work/verifier/evidence/before-admonition-body-click.png`:
  Before, a click in a `{note}`'s second paragraph opens the whole directive (lines 5-9).
- `C:/Users/gaeta/Projets/gsemet-foss-planning-surface/projects/markdown-okf-schema-studio/changes/4-batch/2-actives/514-enter-on-a-list-item-in-an-admonition-op/work/verifier/evidence/after-admonition-body-click.png`:
  After, the same click opens only the second paragraph (line 8) inside the rendered note.
- `C:/Users/gaeta/Projets/gsemet-foss-planning-surface/projects/markdown-okf-schema-studio/changes/4-batch/2-actives/514-enter-on-a-list-item-in-an-admonition-op/work/verifier/evidence/before-admonition-keyboard-enter.png`:
  Before, Enter on the first list item reached with the arrows opens the whole directive (lines 3-8).
- `C:/Users/gaeta/Projets/gsemet-foss-planning-surface/projects/markdown-okf-schema-studio/changes/4-batch/2-actives/514-enter-on-a-list-item-in-an-admonition-op/work/verifier/evidence/after-admonition-keyboard-enter.png`:
  After, the same Enter opens only `- The first item of the note.` (line 6).
- `C:/Users/gaeta/Projets/gsemet-foss-planning-surface/projects/markdown-okf-schema-studio/changes/4-batch/2-actives/514-enter-on-a-list-item-in-an-admonition-op/work/verifier/evidence/before-alert-title-click.png`:
  Before, a click on the alert's title opens the whole alert.
- `C:/Users/gaeta/Projets/gsemet-foss-planning-surface/projects/markdown-okf-schema-studio/changes/4-batch/2-actives/514-enter-on-a-list-item-in-an-admonition-op/work/verifier/evidence/after-alert-title-click.png`:
  After, unchanged: a click on the alert's title opens the whole alert.
- `C:/Users/gaeta/Projets/gsemet-foss-planning-surface/projects/markdown-okf-schema-studio/changes/4-batch/2-actives/514-enter-on-a-list-item-in-an-admonition-op/work/verifier/evidence/before-admonition-title-click.png`:
  Before, a click on the note's title opens the whole directive.
- `C:/Users/gaeta/Projets/gsemet-foss-planning-surface/projects/markdown-okf-schema-studio/changes/4-batch/2-actives/514-enter-on-a-list-item-in-an-admonition-op/work/verifier/evidence/after-admonition-title-click.png`:
  After, unchanged: a click on the note's title opens the whole directive.

Clip of the branch (already linked by the description at f9dc2c6):

- `C:/Users/gaeta/Projets/markdown-okf-schema-studio.worktrees/batch-09-CR-514/docs/demo-video/clips/keyboard-navigation/keyboard-navigation.gif`:
  Arrow keys walk into a note down to a nested list item, and Enter opens that line alone.
- `C:/Users/gaeta/Projets/markdown-okf-schema-studio.worktrees/batch-09-CR-514/docs/demo-video/clips/keyboard-navigation/keyboard-navigation.mp4`:
  The same walk, MP4, 26 s.
- `C:/Users/gaeta/Projets/markdown-okf-schema-studio.worktrees/batch-09-CR-514/docs/demo-video/clips/keyboard-navigation/keyboard-navigation.webm`:
  The same walk, WebM, 26 s.
- `C:/Users/gaeta/Projets/markdown-okf-schema-studio.worktrees/batch-09-CR-514/docs/demo-video/clips/keyboard-navigation/contact-sheet.png`:
  Twelve stills of the walk (neither the list nor the sub-list selection is among them).

## Limits

- No real VS Code window, no new take, no macOS or Linux run of mine; integration, acceptance and
  stress did not run in CI for this pull request.
- Browser behaviour is covered by the visual harness and DOM-level page tests; the chord, formula
  and Known gaps claims were judged through the real renderer, page helpers and `PreviewManager`.
- The clip was viewed as sampled frames, not frame by frame.
- This pass: the three bullets were judged through the real renderer, page helpers, cursor model and
  `PreviewManager` at the head; the base side of "as before this change" is carried from the base logs
  of the first verdict (no base build of mine in this pass).

VERIFIED
