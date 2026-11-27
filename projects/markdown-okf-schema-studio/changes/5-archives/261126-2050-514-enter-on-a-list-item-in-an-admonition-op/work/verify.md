# CR-514 verification

Head: f9dc2c630b852635e8bffcd0b00b42cc886b293c

Base of every "before": `5f0746d79ca28e564841daa19288075aa7823776` (`origin/main`). Sixth
verification, a short pass on the posted description of pull request 540 alone. The previous
verdict at this head is kept as `verify-f9dc2c6-third.md` (NOT VERIFIED on its claim E6 only: the
screenshot proof named no SHA). The code did not change since; the description did. Verdict at the
end: VERIFIED.

Placeholders: `<work>` the folder of this file; `<wt>` the CR worktree; `<r2>` to `<r6>` = the
folders `verifier/r2` to `verifier/r6`; `<node>` =
`fnm exec -- node --import ./scripts/register-myst-patches.mjs`, run from `<wt>`; `<chantier>` the
CLI of the brief with `--batch batch-09`; the other placeholders of the carried claims are `<base>` =
a detached base worktree used by the first verdict (since removed) and `<repro>` =
`verifier/repro`.

## Judged in this pass

### F1. The posted body is `pr-body.md`; since the last pass only the named parts changed: VERIFIED (f9dc2c6)

- Command: `gh pr view 540 --json number,headRefOid,baseRefName,baseRefOid,isDraft,state,title,body,updatedAt`
  (saved as `r6/pr-540-f9dc2c6-sixth.json`), `python -I <r6>/desc.py <work>` (against
  `r5/pr-540-f9dc2c6-closing.json`; log `r6/desc-diff-f9dc2c6.log`)
- Output: head `f9dc2c630b852635e8bffcd0b00b42cc886b293c`, base `5f0746d...`, draft, OPEN, same
  title, updated `2026-11-26T19:55:27Z` (the same at the end of this pass); old 16727 characters,
  new 16957; `posted equals pr-body.md (trailing newline ignored): True`. Hunks: the screenshot
  sentence in Impacts; the clip paragraph; the GIF link; the Local gates item ("unit and contract
  tests" to "tests" after "5503 unit"); one blank line at the end. Nothing else.

### F2. The screenshot proof names its SHAs, and they hold (failed before as E6): VERIFIED (f9dc2c6)

Posted: "Screenshots from the visual test harness: before at `5f0746d` (carried from `cd3b8e6`: the
same tree), after at `f9dc2c6`."

- Command: `git rev-parse 'cd3b8e6^{tree}' '5f0746d^{tree}'` (log `r6/shas-f9dc2c6.log`);
  `gh api repos/gsemet/markdown-okf-schema-studio/commits/cd3b8e6a8f02c18e3bca13aa5a32259ef01f720f --jq '.sha + " " + .commit.tree.sha'`
- Output: `e6f6894de333c24969709306715c4f3c06d06418` twice; the forge answers
  `cd3b8e6a8f02c18e3bca13aa5a32259ef01f720f e6f6894de333c24969709306715c4f3c06d06418`.
- Command: `evidence/before-after.md`; `r3/visual-capture-f9dc2c6.log` (carried from f9dc2c6: same
  head); the downloads of F5
- Output: before captured on `cd3b8e6`, the tree of the base; after: the five scenarios captured at
  `f9dc2c6`, `"status": "passed", "scenario_count": 5, "screenshot_count": 5`, byte-identical to the
  `after-*.png`. The six posted uploads are byte-identical to the evidence pairs, each in the column
  the table names.

### F3. The clip paragraph names the commits the take predates, and the walk at the head: VERIFIED (f9dc2c6)

Posted: "... the extension built from this change before its last three commits (`b09dc7d` to
`f9dc2c6`); the filmed walk opens the same lines at `f9dc2c6`".

- Command: `git log --reverse --format='%h %ci %s' 5f0746d..f9dc2c6`, the same with
  `-- docs/demo-video/clips/keyboard-navigation` (log `r6/shas-f9dc2c6.log`);
  `git diff --stat 9023d10a f9dc2c6 -- docs/demo-video/clips/keyboard-navigation`, the commit dates
  of `9023d10a`, `a2ebb0e3`, `739f9e3e`, the dates of the take's logs (log `r6/take-f9dc2c6.log`)
- Output: four commits, the last three `b09dc7d0`, `8539f1cc`, `f9dc2c63`; only the first,
  `5a686ab0`, touches the clip. VSIX packaged `12:38`, take `12:41`, committed in `9023d10a` at
  `13:20`; the originals of the later commits are from `14:23`, `16:31` and (head) `19:59`; the clip
  folder of `9023d10a` and of the head differ by 0 lines.
- Command: `r3/clip-f9dc2c6.log` (carried from f9dc2c6: same head;
  `<node> <repro>/gesture.js` on `stage/release-plan.md`)
- Output: `enter on "the VSIX" opens <p> lines 8-8`, editor `"  - the VSIX\n"`; "Build the packages"
  7-7: the lines of the filmed walk.

### F4. The GIF is the file at the pull request's head; the MP4 and WebM links too: VERIFIED (f9dc2c6)

- Command: `python -I <r6>/images.py <work> <wt>` (log `r6/images-f9dc2c6.log`);
  `curl -sIL <the GIF link>`; `git cat-file -p f9dc2c6:<the GIF path>`
- Output: `.../raw/f9dc2c630b85.../keyboard-navigation.gif`: 302 to `media.githubusercontent.com`,
  then `200`, `Content-Type: image/gif`, 1696690 B, sha256 `e6775d0b4ccb...`, the LFS object id
  committed at the head and the worktree file; the repository is `PUBLIC`. MP4 200, 543383 B, and
  WebM 200, 368400 B, both at the head and the same as the worktree files.
- Rule: `feature-clip-process.guidelines.md`: "The pull request of a clip shows the GIF inline in
  its body, from the file committed at the PR's head, and links the MP4 and the WebM by their raw
  URLs at the same head": followed.

### F5. It renders, and its images resolve and match: VERIFIED (f9dc2c6)

- Command: `gh api repos/gsemet/markdown-okf-schema-studio/pulls/540 -H "Accept: application/vnd.github.html+json" --jq .body_html`
  (saved as `r6/pr-540-body.html`, signed tokens removed), then F4's `images.py`
- Output: headings `Summary, Deliverables, Changes, Impacts, Blast radius, Autonomous decisions,
  Known gaps, Test plan, Internal references`; the Deliverables table 9 rows of 3 cells; the
  screenshot table 4 rows of 3 cells with 2 images in each of its 3 body rows; 7 images; 6 checked
  boxes. The 7 image links answer 200 without credentials; six PNGs byte-identical to
  `evidence/{before,after}-{alert-body-click,admonition-body-click,admonition-keyboard-enter}.png`
  (the before images of two pairs equal the unchanged title images, as expected), the seventh the
  committed GIF.
- User name and home folder: carried from f9dc2c6: the bytes are those of the images opened in the
  earlier passes (the six PNGs, and sampled frames of the GIF): none shows either.

### F6. The Local gates item: VERIFIED (f9dc2c6)

- Command: first line and result lines of `work/gates/prepush-f9dc2c6-preflight.log` (extract
  `r6/gate-f9dc2c6.log`); `<chantier> handoff CR-514`
- Output: `head f9dc2c630b852635e8bffcd0b00b42cc886b293c base 5f0746d79ca28e564841daa19288075aa7823776: just preflight`;
  unit `tests 5503 pass 5495 fail 0 skipped 8`; the contract target `tests 0`, so all 5503 are unit
  tests; security `tests 116 pass 116`; clip kit `tests 56 pass 56`;
  `1228 requirements, 0 errors, 26 warnings`; `ci-static: passed`;
  `preflight: visual, viewer-graph, integration, acceptance, report and gallery stages skipped on Windows; CI runs them`;
  `exit 0`. The handoff's "before push at f9dc2c6" note says the same.

### F7. Each proof names its SHA; no stale mark, role as a doer or local path: VERIFIED (f9dc2c6)

- Command: `desc.py` (log `r6/desc-diff-f9dc2c6.log`, which holds the whole body, numbered)
- Output: Impacts: the screenshots name `5f0746d`, `cd3b8e6` and `f9dc2c6` (line 74-75), the clip
  names `b09dc7d` to `f9dc2c6` and links at the head (lines 87-92); each of the six Test plan items
  names `f9dc2c6` (lines 206-237). `STALE: False UNVERIFIED: False unchecked boxes: 0 checked: 6`;
  role words: none; local paths: `lines matched: 0`. The only internal reference is under Internal
  references. No Known gaps bullet changed; the section is not "None".

### F8. Head, pull request and CI: VERIFIED (f9dc2c6)

- Command: `git rev-parse HEAD`, `git status --short | wc -l`,
  `git ls-remote origin refs/heads/main <branch>`, `gh pr checks 540`
- Output: `f9dc2c630b852635e8bffcd0b00b42cc886b293c`, `0`; remote main `5f0746d...`, branch
  `f9dc2c6...`; `checks`, `report`, `static`, `static-windows`, `viewer-graph`, `visual`,
  `visual-2` pass; `acceptance`, `gallery`, `integration`, `pages`, `release`, `release-check`,
  `stress`, `tag-release`, `toc-loop` skipping.

## Observations, not counted

- Hosting of the screenshots. `.agents/guidelines/pull-request.guidelines.md` ("Screenshots in the
  PR") asks for raw links to a `-assets` side branch; the body uses uploaded attachments (what the
  card's `pr-template.md` asks). The project's guidelines rank above the card, so this is a conflict
  to report. It is none of the description's failure cases, and the uploads are byte-identical to
  the evidence.

## Carried claims: the description's unchanged parts

### E2. The sentences on screenshots and clip in Deliverables and on title clicks in Impacts: VERIFIED (f9dc2c6)

_carried from f9dc2c6: same head, and the description text it judges is unchanged (claim F1)._

- "Screenshots before and after the change, and the re-filmed clip, are under Impacts": F5.
- "A click on the title of an admonition or alert opens all of it, before and after":
  `r5/images-f9dc2c6.log`: `alert-title-click before == after: True`,
  `admonition-title-click before == after: True`; the two scenarios' images show the whole box open
  (carried section "Files that may be attached").
- The table's three gestures are the three evidence pairs of `evidence/before-after.md`.

### E4. Test plan items Tests, Requirements, Changelog, Review and CI (Local gates is F6): VERIFIED (f9dc2c6)

_carried from f9dc2c6: same head, and the description text it judges is unchanged (claim F1)._

- Tests. Command: `git diff --name-status 5f0746d f9dc2c6 -- test` (log `r5/testplan-f9dc2c6.log`);
  result lines of `<r3>/tests-head-f9dc2c6.log` and `<r3>/tests-base-f9dc2c6tests.log` (carried from
  f9dc2c6: same head). Output: the changed or added unit and page test files are the nine run;
  `tests 284 pass 284 fail 0`; with the previous source `pass 177 fail 107`.
- Requirements. Output of the same log: 13 SwRS files changed. Gate log lines 5987-5990:
  `0 indexes would change`, `0 requirement OKF projections would change`, `0 files would change`.
- Changelog. Same log: one bullet added under Unreleased, ending `(CR-514 enter-admonition, PR #540)`.
- Review. `<chantier> handoff CR-514`: `r6 inspector approved at 8539f1cc...` and
  `r6 approved at 8539f1cc..., committed as f9dc2c630b852635e8bffcd0b00b42cc886b293c`.
- CI. `gh pr checks 540`: `checks`, `report`, `static`, `static-windows`, `viewer-graph`, `visual`,
  `visual-2` pass; `acceptance`, `gallery`, `integration`, `pages`, `release`, `release-check`,
  `stress`, `tag-release`, `toc-loop` skipping.

## Carried claims: the three bullets of the previous pass

### D1. The card bullet (failed before as claim C): VERIFIED (f9dc2c6)

_carried from f9dc2c6: same head, and the bullet it judges is unchanged (claim F1)._


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

_carried from f9dc2c6: same head, and the bullet it judges is unchanged (claim F1)._


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

_carried from f9dc2c6: same head, and the bullet it judges is unchanged (claim F1)._


- Command: `<node> <r4>/three.js <wt> A` (log `r4/three-A-f9dc2c6.log`: 8 following contents in a
  note, a dropdown and an alert; the arrows walked with the real `structuralMove`; each editor emptied)
- Output: "click on first paragraph" opens the `<li>` with the following content in all 24 cases and
  `after emptying, content left=false`. "Enter on the item" (`block 1, Right, Right`) does the same in
  all 12 HTML comment and HTML cases.
- Observation, not counted: Enter on the whole item takes the hidden content for the other listed
  kinds too. What differs by kind is Enter on the item's first paragraph (one Right further): of the
  listed contents it takes only an HTML comment or HTML written with no blank line before it. The
  sentence is true as written and does not say otherwise.

## Carried claims: code, tests, evidence

### Previous claim A, Enter on a formula of a list in a box: fixed, VERIFIED (f9dc2c6)

_carried from f9dc2c6: same head, and the description text it judges is unchanged (claim F1)._

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

_carried from f9dc2c6: same head, and the description text it judges is unchanged (claim F1)._

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

_carried from f9dc2c6: same head, and the description text it judges is unchanged (claim F1)._

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

_carried from f9dc2c6: same head, and the description text it judges is unchanged (claim F1)._

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

_carried from f9dc2c6: same head, and the description text it judges is unchanged (claim F1)._

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

_carried from f9dc2c6: same head, and the description text it judges is unchanged (claim F1)._

- Command: `<node> <r3>/changes.js <wt>`
- Output (`changes-f9dc2c6.log`): the title of a `{div}` callout opens the whole callout, also
  nested (`[=Tip] click -> <aside 1-7>`); a version admonition body maps its written lines and its
  argument text opens the directive; a note left open at the end of the file keeps the closing fence
  of an inner tip and code block; a one-line `:::{warning} Text` and a card title open their
  directive; `{mermaid}`, `{math}`, `{code-block}` with caption and an alert's fenced code open
  whole; the nearest of nested boxes decides; a click inside a box never takes the list around it.

### Blocks outside a box are mapped as before: VERIFIED (f9dc2c6)

_carried from f9dc2c6: same head, and the description text it judges is unchanged (claim F1)._

- Command: `<node> <repro>/diff-outside.js <wt> <base> .`, then over `<r2>/corpus`
- Output: `files=2176 errors=0 outsideBoxMappingDiffs=0 insideBoxMappingDiffs=3 htmlDiffsBesidesLineAttributes=0`;
  corpus `files=401 errors=0 outsideBoxMappingDiffs=0 insideBoxMappingDiffs=148 htmlDiffsBesidesLineAttributes=0`.

### Move chord, refusals, Down and Up at list edges: VERIFIED (f9dc2c6)

_carried from f9dc2c6: same head, and the description text it judges is unchanged (claim F1)._

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

_carried from f9dc2c6: same head, and the description text it judges is unchanged (claim F1)._

- Command: `<node> <repro>/gaps.js <wt>`
- Output: `erase 2-2: writes=1 -> "> [!NOTE]\n>\n>\n> Second.\n>\n> Third.\n"`, one admonition, no
  plain quote; with a lazy line the later quoted lines leave the alert (disclosed).

### Earlier F1, F2, F3: still fixed, VERIFIED (f9dc2c6)

_carried from f9dc2c6: same head, and the description text it judges is unchanged (claim F1)._

- `<node> <repro>/gesture.js` on the captioned `{table}` and `{figure}` shapes (`f1-f9dc2c6.log`):
  lines 2-3 and 5-5, both fences kept. `<node> <repro>/property.js <wt> <r2>/corpus`:
  `{"docs":280,"opens":4315,"openCuts":0,"moves":876,"refused":20,"moveBreaks":0,"erases":0,"eraseBreaks":0}`.
- `image-gap.js`, `image-gap2.js` (`crossingMoved 0`, 970 refusals with the disclosed message),
  `firstplace.js`, `kinds2.js` (`{"moved":268,"broken":0}`): output identical to the run at 739f9e3.

### The other Known gaps: VERIFIED (the sentence failed as C is judged in D1) (f9dc2c6)

_carried from f9dc2c6: same head; no Known gaps bullet changed since that pass (claim F1). The observation at its end is replaced by D3._

- Commands: `<node> <r3>/bullets.js <wt>`, `<node> <r3>/bullets2.js <wt>`,
  `<node> <r3>/chords.js <wt>`, `<node> <r3>/gapsC.js <wt>` (logs `bullets*`, `chords*`, `gapsC*`;
  `*-5f0746d.log` for the base)
- Output: every other bullet of "Elements of a box that do not open on their own", "Opening or
  emptying", "The move chord, and drawing" and "Outside a box" shows what it says; the "as before
  this change" ones match the base.
- Observation, not counted: the bullet "Clicking the first paragraph of a tight list item followed
  by hidden content ..." also happens with Enter for an item followed by an HTML comment or HTML.

### Keyboard navigation clip: VERIFIED from its committed files (f9dc2c6)

_carried from f9dc2c6: same head, and the description text it judges is unchanged (claim F1)._

- `check.json`: passed, 26 s, MP4 543383 B, WebM 368400 B, GIF 1696690 B, 960 px, 12 fps, 128
  colours, ladder step 0, VS Code 1.147.0, win32; the description's figures match it and `clip.md`.
- `curl -sL` of the three description links (at f9dc2c6): 200, same sizes, byte-identical to the
  worktree files.
  (The description's links as judged then; the posted ones are judged in F4.)
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

_carried from f9dc2c6: same head, and the description text it judges is unchanged (claim F1)._

- Command: `git diff --stat 5f0746d f9dc2c6 -- requirements docs/user CHANGELOG.md`: 17 files.
- `git diff 5f0746d f9dc2c6 -- requirements | grep -cE '^[+-]req_lifecycle'`: `0`; no StRS and no
  `skills/` file in `--name-only` (`0`).
- `grep @implements_req`: `mystBoxLines.ts` BLOCK-014, 130, 254; `boxFirstBlock.ts` BLOCK-124.
- The test names the last commit adds to BLOCK-014, 124 and 254 exist in the box test file
  (`grep -cF`, each at least 1); lint in the gate log: 0 errors.
- The requirements log has dated lines for rounds 5 and 6; `CHANGELOG.md` has one entry under
  Unreleased; the CHANGELOG, user guide and requirement sentences about formulas, tags, options
  blocks and `{div}` callouts agree with the probes above.

## Files that may be attached to the pull request

All ten images of `evidence/` hold at f9dc2c6 (details and reproduction in
`evidence/before-after.md`). The two title pairs show no change; the three other pairs show it.
Each image below was opened: no user name or home folder.

Folder of the images:
`<work>/verifier/evidence/`

- `<work>/verifier/evidence/before-alert-body-click.png`:
  Before, a click in a note alert's second paragraph opens the whole alert (lines 5-8).
- `<work>/verifier/evidence/after-alert-body-click.png`:
  After, the same click opens only `> The second paragraph of the note.` inside the rendered alert.
- `<work>/verifier/evidence/before-admonition-body-click.png`:
  Before, a click in a `{note}`'s second paragraph opens the whole directive (lines 5-9).
- `<work>/verifier/evidence/after-admonition-body-click.png`:
  After, the same click opens only the second paragraph (line 8) inside the rendered note.
- `<work>/verifier/evidence/before-admonition-keyboard-enter.png`:
  Before, Enter on the first list item reached with the arrows opens the whole directive (lines 3-8).
- `<work>/verifier/evidence/after-admonition-keyboard-enter.png`:
  After, the same Enter opens only `- The first item of the note.` (line 6).
- `<work>/verifier/evidence/before-alert-title-click.png`:
  Before, a click on the alert's title opens the whole alert.
- `<work>/verifier/evidence/after-alert-title-click.png`:
  After, unchanged: a click on the alert's title opens the whole alert.
- `<work>/verifier/evidence/before-admonition-title-click.png`:
  Before, a click on the note's title opens the whole directive.
- `<work>/verifier/evidence/after-admonition-title-click.png`:
  After, unchanged: a click on the note's title opens the whole directive.

Clip of the branch (the description links all three at the head, F4):

- `<wt>/docs/demo-video/clips/keyboard-navigation/keyboard-navigation.gif`:
  Arrow keys walk into a note down to a nested list item, and Enter opens that line alone.
- `<wt>/docs/demo-video/clips/keyboard-navigation/keyboard-navigation.mp4`:
  The same walk, MP4, 26 s.
- `<wt>/docs/demo-video/clips/keyboard-navigation/keyboard-navigation.webm`:
  The same walk, WebM, 26 s.
- `<wt>/docs/demo-video/clips/keyboard-navigation/contact-sheet.png`:
  Twelve stills of the walk (neither the list nor the sub-list selection is among them).

## Limits

- No real VS Code window, no new take, no macOS or Linux run of mine; integration, acceptance and
  stress did not run in CI for this pull request.
- Browser behaviour is covered by the visual harness and DOM-level page tests; the chord, formula
  and Known gaps claims were judged through the real renderer, page helpers and `PreviewManager`.
- The clip was viewed as sampled frames, not frame by frame.
- This pass judged the description: no test, build, capture or probe of the code was run again.

VERIFIED
