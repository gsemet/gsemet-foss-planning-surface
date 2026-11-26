# CR-514 verification

Head: 739f9e3ecd771efce1938ebdb0685f324a6cf0a2

Base of every "before": `223a8c49a47f8af786412e7cff748860b18d3782`. Second verification; the first
one (`verify-a5550c3.md`, NOT VERIFIED at a5550c32, claims F1 to F3) is the source of every
`carried from a5550c3`. The move since then: a forge rebase with identical content, then one commit
(739f9e3, round 4). Verdict at the end: NOT VERIFIED (claims A, B and C fail; everything else
listed holds).

Placeholders: `<wt>` the CR worktree; `<base>` = `<wt>/out/vbase`, a detached worktree of the base;
`<repro>` = the folder `verifier/repro` beside this file; `<r2>` = `verifier/r2`; `<build>` = `<wt>`
(head) or `<base>`; `<node>` = `fnm exec -- node --import ./scripts/register-myst-patches.mjs`, run
from the build root; `<chantier>` the CLI of the brief with `--batch batch-09`. Probe outputs are
saved in `<r2>` as the logs named below. Before and after: `verifier/evidence/before-after.md`.

## The head moved on the forge during this verification

PR #535 (CR-513) was merged and the forge rebased this branch on `main`: PR #540 head is now
`8539f1cc64a9b76b08f1bc3f70b1afae32247ab1` on base `5f0746d79ca28e564841daa19288075aa7823776`.
The worktree stays at 739f9e3. Every judgment below applies to 8539f1cc, because the content is
identical.

- Command: `git rev-parse 223a8c49^{tree} 5f0746d7^{tree} 739f9e3^{tree} 8539f1cc^{tree}`
- Output: the two bases `e6f6894de333c24969709306715c4f3c06d06418`, the two heads
  `6c2bb41f5ef4635515955bf68a3bdceb2c2280a1`.
- Command: `git range-diff 223a8c49..739f9e3 5f0746d7..8539f1cc`
- Output: `c506f050 = 5a686ab0`, `4e4eeb4e = b09dc7d0`, `739f9e3e = 8539f1cc` (all `=`).
- Command: `gh pr view 540 --json headRefOid,baseRefOid,baseRefName,isDraft,state`
- Output: `{"baseRefName":"main","baseRefOid":"5f0746d7...","headRefOid":"8539f1cc...","isDraft":true,"state":"OPEN"}`
- The description's clip links still name the 739f9e3 SHA (`curl -sL`: MP4 200, 543383 B; WebM 200,
  368400 B; GIF 200, 1696690 B).

## Failed claims

### A. Enter on a formula in a list of a box opens the wrong lines: NOT VERIFIED (739f9e3)

Claimed by: specification ("Enter then opens that element only"); PR Deliverables ("that element
opens"); PR Changes ("A block held directly by a list item maps its own lines, up to the next block
of the item and never across a fence"); BLOCK-014 criteria row (Enter on such a block carries "that
block's lines"); CHANGELOG ("now edits the selected paragraph, list item or directive only (a
diagram, a formula or a code block opens whole)"). Not in Known gaps.

- Command: `<node> <repro>/gesture.js <wt> <r2>/shapes/dollar-<shape>.md "y = 2" enter erase`
  (`dollar-one-blank.md` = `":::{note}\n- Text\n  $$\n  y = 2\n  $$\n\n- next\n:::\n"`)
- Output (`dollar-739f9e3e.log`):

  | shape | Enter on the formula opens | editor text | after erasing it and committing |
  | --- | --- | --- | --- |
  | one-blank, two-blank, trailing | lines 2-2 | `"- Text\n"` | the item's text is gone, the formula stays |
  | alert | lines 2-2 | `"> - Text\n"` | the same |
  | quote (a quote, then the formula) | lines 6-6 | `"  > quoted\n"` | the quoted line is gone, the formula stays |
  | tight | lines 4-8 | text line and formula | both gone |
  | aftercode | lines 3-9 | code block, `tail`, formula | all three gone |

- Command: `<node> <r2>/mapped.js <wt> <r2>/shapes/dollar-one-blank.md` (what the arrows can select)
- Output (`mapped-head.log`): `<p > 2-5 "Text"` and `<div math-display> 2-2 "y = 2"`; with
  `dollar-quote.md`: `<div math-display> 6-6`. The formula is lines 3-5 and 7-9: its own element
  maps a line that holds none of it.
- A formula that ends the box is right (`dollar-top.log`, `dollar-last`: lines 2-5, the item).
- `$$ y $$` on one line and `$$ (label)` are wrong too: `<node> <r2>/items-md.js <wt>` flags
  `WRONG ...|mathOne|quote <DIV> 6,6` and `...|mathLabel|trailing <DIV> 4,4` (formula words missing
  from the opened lines).
- Same command with `<base>` (`dollar-223a8c49.log`): Enter opens the whole `<aside>`, so the
  editor holds the formula.
- Same with a build of 4e4eeb4 (`dollar-4e4eeb4.log`): one-blank 2-6, two-blank, trailing and alert
  2-7, quote 6-10, each holding the formula. The editor without the formula is new in 739f9e3
  (`tight` and `aftercode` were the same at 4e4eeb4).
- Outside a box, base and head: Enter on such a formula opens the whole item, lines 1-5 and 1-6,
  formula included (`dollar-top.log`).
- A click is right (`dollar-click-739f9e3e.log`: the item, lines 2-6 and 4-10).

### B. A callout written as `{div}` with `:class:` is not protected from the chord: NOT VERIFIED (739f9e3)

Claimed by: PR Changes ("A move that would put an unindented `---` line first in the body, or a
heading first in an untitled admonition or in a callout, is refused"); Autonomous decisions
("covers ... callouts, and its `---` refusal every kind of box"); BLOCK-124 S7; user guide
(`docs/user/editing.md`, the same refusal). Not in Known gaps.

- Command: `<node> <r2>/calloutdiv.js <wt>`
- Output (`calloutdiv-739f9e3e.log`): source
  `":::{div}\n:class: callout-tip\n\nBefore.\n\n---\n\nAfter.\n:::\n"` renders
  `<aside admonition simple tip> "TipBefore.After." hr=1`; chord down on "Before.": `ok=true`,
  written `":::{div}\n:class: callout-tip\n\n---\n\nBefore.\n\nAfter.\n:::\n"`; after:
  `<aside admonition simple tip> "Tip" hr=0` (the whole body is gone from the preview).
- Heading variant: `ok=true`; after: `"HeadBefore.After."`, the title "Tip" is replaced by "Head".
- Control `::: {.callout-tip}`: `ok=false reason=A --- line cannot start an admonition or an alert:
  its content would not show.`
- Command: `<node> <r2>/attack.js <wt>` (every box spelling, prefix and first-block candidate)
- Output (`attack-head.log`): `{"docs":5040,"moved":10386,"refused":1019,"broken":136}`; the two
  `{div}` with `:class:` boxes break with `---`, `-----`, ATX and setext headings; every other box
  breaks only with the disclosed bold-only paragraph.
- Cause: `src/core/mapping/boxFirstBlock.ts` `directiveBox` finds `.callout-` in the braces of the
  opening line only; `mystNormalize.ts` renders a `div` with a `callout-<kind>` class as an
  admonition.
- Base: its page has no inner move (`calloutdiv-223a8c49.log`:
  `moves.moveNeighbour is not a function`), so no chord writes that document.
- The text stays in the file.

### C. Two Known gaps sentences say less than what happens: NOT VERIFIED (739f9e3)

- Claim: "Erasing the first block of a box body can leave a `---` line first, and the box then shows
  its title only". Command: `<node> <r2>/gaps4.js <wt>` and `<node> <r2>/lines.js <wt>`.
  Output: true for a note and an alert (`after <aside admonition note> "Note" hr=0`); for a
  `{dropdown}` titled `T` nothing is left, title included (`gaps4-head.log`: `after` empty;
  `lines-739f9e3e.log`: the page holds only the following `<p> "End."`).
- Claim: "A card or a div inside a box whose body starts with dashes misrenders the same way".
  Command: `<node> <r2>/render-only.js <wt>`. Output (`render-only-739f9e3e.log`): the card shows
  `"NoteCard text."` (part of its body, not a title alone); a `{div}` makes the renderer throw
  `TypeError: Cannot read properties of undefined (reading 'length')`, so no page is produced.
- The renderer behaviour is the base's (`render-only-223a8c49.log`, `lines-223a8c49.log`): only the
  sentences are wrong.

## Claims that hold

### Gate, handoff and CI: VERIFIED (739f9e3; CI also at 8539f1cc)

- Command: first line and result lines of `work/gates/prepush-739f9e3-preflight.log`
- Output: `head 739f9e3ecd771efce1938ebdb0685f324a6cf0a2 base 223a8c49a47f8af786412e7cff748860b18d3782: just preflight`;
  clip-kit `tests 56 pass 56 fail 0`; unit `tests 5450 pass 5442 fail 0 skipped 8`; security
  `tests 116 pass 116 fail 0`; `1228 requirements, 0 errors, 26 warnings`; `ci-static: passed`;
  `preflight: visual, viewer-graph, integration, acceptance, report and gallery stages skipped on Windows; CI runs them`;
  `exit 0`.
- Command: `<chantier> handoff CR-514`
- Output: `rounds: 4 of 6`; "before push at 739f9e3...: just preflight exit 0 ... tree clean";
  "r4 approved at 4e4eeb4..., committed as 739f9e3..."; "CI green at 739f9e3"; long gate
  "none in chantier.yaml".
- Command: `gh pr checks 540` and `gh api .../commits/8539f1cc.../check-runs`
- Output: `static`, `static-windows`, `visual`, `visual-2`, `viewer-graph`, `report`, `checks` pass
  (7 success, 9 skipped: `acceptance`, `integration`, `stress`, `toc-loop`, `release-check`,
  `gallery`, `pages`, `release`, `tag-release`).

### New tests pass at the head and fail without their change: VERIFIED (739f9e3)

- Command: `<node> --test --test-reporter=spec` on the nine test files named in `verify-a5550c3.md`,
  after `fnm exec -- npm.cmd run compile`
- Output: `tests 231 pass 231 fail 0 skipped 0` (`tests-head.log`).
- The failures on the base of the eight other files: carried from a5550c3: round 4 changes none of
  those test files (only `boxBlockSourceLines.test.ts`) and the base tree is identical.

### `boxBlockSourceLines.test.ts` and the Test plan's counts: VERIFIED (739f9e3)

- Command: that test file in `<base>` built with the head's `test/` and, in turn, the sources named
- Output: head 41/41; base renderer 18 pass 23 fail (`tests-base-renderer.log`: the 14 renderer
  tests and 5 unclosed-fence tests of the description, 3 list-item tests and 1 refused move);
  4e4eeb4 `src` 24 pass 17 fail (`tests-pre-r4-src.log`: the 4 fence cases and 13 refused moves);
  c506f050 `mystBoxLines.ts` and `mystUnclosedFences.ts` 33 pass 8 fail
  (`tests-pre-unclosed-fix.log`: the 5 unclosed-fence tests and 3 list-item tests); whole base
  `src` 1 pass 40 fail.

### Earlier F1, a captioned `{table}` or `{figure}` in a list cut a fence: fixed, VERIFIED (739f9e3)

- Command: `<node> <repro>/gesture.js <wt> <repro>/gap-note.md "Step one" enter erase` (also
  `gap-alert.md`, and `gap-fig.md "Caption text"`)
- Output (`f1-head.log`): lines 2-3 (`"- Step one\n\n"`), 2-3, and 5-5 (`"  Caption text\n"`); after
  commit both fences of each directive stay.
- Command: `<node> <repro>/property.js <wt> <corpus>`:
  `{"docs":280,"opens":4315,"openCuts":0,"moves":876,"refused":20,"moveBreaks":0,"erases":0,"eraseBreaks":0}`
  (14 cuts at a5550c32).
- Command: `<node> <r2>/items.js <wt>`: `{"docs":4050,"opens":135366,"cuts":0,"overlaps":135,...}`
  (the overlaps are `$$` shapes, claim A); the same at 4e4eeb4: 1831 cuts, 1289 overlaps.
- `items-md.js` also reports `CUT` lines, all on `$$ (label)` shapes, where the probe reads the
  closing `$$ (label)` as an opening fence.

### Earlier F2, the image sentence of Known gaps: resolved, VERIFIED (739f9e3)

- Command: `<node> <repro>/image-gap.js <wt>`: 58 `ACROSS-IMAGE: refused`, 0 `MOVED`.
- Command: `<node> <repro>/image-gap2.js <wt>`:
  `{"shapes":980,...,"clicksOnWholeBox":526,"crossing":970,"crossingMoved":0,...}`, every refusal
  with "Text between the two blocks (a comment or a link definition) prevents the move.", which is
  what the description now says.

### Earlier F3, first-place refusal, for the other spellings: VERIFIED (739f9e3; limited by B)

- Command: `<node> <repro>/firstplace.js <wt>`
- Output: `---` refused in a colon note, a backtick note and an alert; a heading refused in the two
  notes with their reason; a heading in an alert and a field list move and render with the title.
- Command: `<node> <repro>/kinds2.js <wt>`: `{"moved":268,"broken":0}`.
- The disclosed bold-only paragraph still moves first (`gaps4-head.log`, `attack-head.log`).

### Pointed or selected element opens; title, frame or selected box opens all: VERIFIED outside A (739f9e3)

- Command: `fnm exec -- npm.cmd run visual:render`, then
  `.venv/Scripts/python.exe test/visual/capture.py --scenario <id>` for `gfm/v14`, `gfm/v15`,
  `block-editing/v57`, `v58`, `v59` (full ids)
- Output: `{"status": "passed", "scenario_count": 5, "screenshot_count": 5}`; the five images are
  byte-identical to the a5550c32 "after" images; opened: no user name or home folder.
- `v14`, `v57`, `v59` fail on the base: carried from a5550c3: round 4 changes no visual file and the
  base tree is identical.
- `v27`, `v36` to `v39` and the admonition that no longer scrolls: carried from a5550c3: round 4
  changes no style and no visual file; CI `visual` and `visual-2` pass at 739f9e3 and 8539f1cc.
- Command: `<node> <repro>/gaps.js <wt>`: body blocks open on their own lines on click and Enter
  (`<p 2-2> "First." click=<p 2-2> enter=<p 2-2>`), Enter on a selected box opens all of it, a
  version admonition body maps its written line (`<p 7-7> "Late body."`).

### Blocks outside a box are mapped as before: VERIFIED (739f9e3)

- Command: `<node> <repro>/diff-outside.js <wt> <base> .` and the same over the generated corpus
- Output: `files=2176 errors=0 outsideBoxMappingDiffs=0 insideBoxMappingDiffs=3 htmlDiffsBesidesLineAttributes=0`;
  corpus `files=401 errors=0 outsideBoxMappingDiffs=0 insideBoxMappingDiffs=148 htmlDiffsBesidesLineAttributes=0`.

### Move chord limits, other refusals, Down and Up at list edges: VERIFIED (739f9e3)

- Command: `<node> <repro>/gaps.js <wt>`: no chord from a block inside an item, a quote or a card;
  body blocks swap inside the box (`chord down from <p 6-7>: no neighbour, nothing sent`;
  `chord down from <p 2-2>: MOVED past <blockquote 4-4>`).
- Command: `<node> <repro>/refusal.js <wt>`: a link definition or a `%` comment between two blocks:
  "Text between the two blocks (a comment or a link definition) prevents the move."; an alert block
  and the paragraph after the alert: "The preview is out of date. Refresh it and try again."; two
  whole quotes swap.
- The refusal shown next to the insert point and Down/Up at the ends of a list: page tests in the
  231-test run (`T36: a refused move says why next to the bar`, passing).

### Erased alert block keeps the alert: VERIFIED (739f9e3)

- Command: `<node> <repro>/gaps.js <wt>` ("alert block, no lazy line")
- Output: `erase 2-2: writes=1 -> "> [!NOTE]\n>\n>\n> Second.\n>\n> Third.\n"`, one admonition, no
  plain quote; also after autosave then commit, and indented in a list item.

### Keyboard navigation clip: VERIFIED from its committed files (carried)

- carried from a5550c3: `git diff 4e4eeb4 739f9e3 -- test/visual test/integration docs/demo-video test/shared CHANGELOG.md media skills package.json`
  is empty (clip, frames, check file, replay edit).
- At 739f9e3: `gesture.js` on the clip's `stage/release-plan.md`: Enter on "the VSIX" opens lines
  8-8 `"  - the VSIX\n"`, on "Build the packages" 7-7 (`clip-739f9e3e.log`): the filmed walk is
  unchanged.
- Command: `node --test docs/demo-video/clip-kit/lib/storyboard.test.mjs`: `tests 40 pass 40 fail 0`.
- The take was filmed in round 2, before later fixes; maintainer review pending (disclosed).

### Other Known gaps: VERIFIED apart from C (739f9e3)

- Command: `<node> <r2>/gaps4.js <wt>`: erasing the first block before a heading makes it the title
  of a note and of a callout; `:::{ note }` lets a heading and `---` move first; a fence div
  `.callout-zzz` has a heading refused; a later paragraph after code in a tight item opens the item
  (lines 2-6); erasing the first line of an item that holds a directive removes the list marker and
  keeps both fences; with an options block before a rule, the blocks before the rule map one line
  down (the same on the base, `lines-223a8c49.log`).
- Command: `<node> <repro>/gaps.js <wt>` (`gaps-head.log`): outside a box,
  `chord down from <p 1-1>: MOVED past <figure 3-3>` writes the paragraph into a top-level
  `{mermaid}` fence (the same for `{math}`, `{code-block}`, a captioned `{table}`); lazy
  continuation line, `erase 4-5` leaves `plain blockquotes 1` outside the alert.
- Contact sheet without the list selections, replay run only on main or a heavy run: carried from
  a5550c3: neither file changed, `integration` is skipping on this PR.

### Requirements, markers, changelog, user guide: VERIFIED apart from A and B (739f9e3)

- Command: `git diff 223a8c49 739f9e3 --stat -- requirements docs/user CHANGELOG.md`: 17 files.
- Command: `git diff 223a8c49 739f9e3 -- requirements | grep -cE "^[+-]req_lifecycle"`: `0`; no
  StRS file and no `skills/` file in `--name-only` (count `0`).
- Markers and lint: `just preflight` in the gate log (0 errors).
- The CHANGELOG, BLOCK-014, BLOCK-124 and user guide sentences named in A and B do not hold for
  those shapes.

### PR description form: VERIFIED apart from A, B, C (739f9e3)

- Command: `gh pr view 540 --json body,title` compared with `work/pr-body.md`
- Output: `posted 11443 local 11443 equal true`; title
  `feat(editor): edit the pointed block inside admonitions and alerts`. Template sections plus
  Autonomous decisions and Known gaps; the internal reference is under Internal references, before
  the Claude Code line.
- Command: `git grep -nE "(function|const) (mapBoxSourceLines|editingElementFor|planBlockMove|planAlertPlaceholder)\b" -- src`
- Output: `sourceEdits.ts:339`, `blockMove.ts:109`, `mystBoxLines.ts:241`, `mappedBlocks.ts:188`:
  the diagram's names exist.
- Test plan boxes and before/after screenshots are filled at closing (brief), so not judged.

## Limits

- No real VS Code window, no new take, no macOS or Linux run of mine; integration, acceptance and
  stress did not run in CI for this PR.
- Browser behaviour is covered by the visual harness and DOM-level page tests only; claims A and B
  were judged through the real renderer, page helpers and `PreviewManager`, not in a browser.
- Plain `{div}` with the class as its argument (`:::{div} callout-note`) renders as a `div`, not a
  box. Moving `---` first in it is accepted and the written document makes the renderer throw, as
  the base renderer does on that shape (`calloutdiv-739f9e3e.log`, `render-only-223a8c49.log`): a
  renderer defect noted for follow-up, not counted as a failed claim.

NOT VERIFIED
