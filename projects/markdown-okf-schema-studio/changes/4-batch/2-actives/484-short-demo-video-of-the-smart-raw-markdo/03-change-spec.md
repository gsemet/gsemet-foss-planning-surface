# Storyboard, two captions and several marks for the raw copy clip

Short name: `raw-copy-demo`. No tracker issue (verbal request of the owner).

## Goal

The owner likes the merged feature clip `docs/demo-video/clips/raw-copy-balance-edges/` (CR-482,
PR #501): one continuous shot, the copy in the page on the left, then a zoom on the pasted text on
the right. This change:

1. gives the clip, and every later feature clip, a storyboard in Markdown that the owner reviews and
   edits as easily as the main video's `docs/demo-video/short-demo-01/01-storyboard.md`: a section
   per beat with its time, its filmed shot, one picture per key moment and its on-screen texts. That
   file stays the clip's live source (the kit reads it);
2. adds to the recipe the owner's review of the storyboard before the take and before a render, and
   the rule that the clip is watchable in the PR's review;
3. teaches the clip kit two captions in turn, several marks in turn, combined key badges
   ("Ctrl+C / ⌘C") and a size and frame rate read from the storyboard;
4. films a new scene (new stage document, new take) and renders the clip again at 1280x720, 15 fps.

The approved storyboard draft is `work/storyboard/clip.md` of this CR's folder, with its stage in
`work/storyboard/stage/` (`runbook.md`, and `notes.md`, an empty file). The Griller's trial changes
to the kit (evidence, not the implementation) are in `prototypes/01-trial-kit-changes/`
(`kit.diff`, `scenario.mjs`, `clip.kit.md`, `README.md`). Both folders are in the planning surface:
`C:/Users/gaeta/Projets/gsemet-foss-planning-surface/projects/markdown-okf-schema-studio/changes/2-backlog/P1/short-demo-video-of-the-smart-raw-markdo/`
(or the CR's folder wherever the batch moved it).

Everything is done on Windows (Q9): the take, the render and the evidence.

## Decisions carried from `02-answers.md`

The answers Q1 to Q6, Q10 to Q14, Q16, Q17 and Q24 are superseded by Q27 where they differ (no
second shot, no `short-demo-02/`, no square crop, no new layout); Q8's off-clip checks are not part
of this CR (Q27). Q7 is revised by Q9, Q12 and Q13 by Q28, Q28's size by Q33, Q18 by Q22 and Q30.

| Answer | Decision | Where in this spec |
| --- | --- | --- |
| Q4 | The take films a VSIX built from the branch (`just package`), in the kit's throwaway profile | "New take and render" |
| Q9 | Everything on Windows; the texts name both shortcuts; macOS Cmd+C stays not proved in a real window (a known gap, not a task) | "New take", "Host and default matrix" |
| Q10, Q11 | No card, no music, silent | Storyboard `Cards` row, recipe unchanged on this |
| Q15, Q29 | Badges read "Ctrl+C / ⌘C" and "Ctrl+V / ⌘V" whatever the platform filmed; `storyboard.mjs` and the recipe's badge rule allow and use the combined form | "Kit: badges" |
| Q19 | P1, it gates the 1.13.0 release | - |
| Q21 | The recipe stays `docs/demo-video/guidelines/feature-clip-process.guidelines.md`, linked from `AGENTS.md` (already merged); shared rules stay in `short-demo-process.guidelines.md`, linked, not copied | "Recipe" |
| Q22, Q23, Q30, Q32 | The owner reviews and corrects the storyboard, with a picture per key moment from a trial take, before the take and before a render; the draft is reviewed outside the repository, before any branch, then moved into the clip folder as its live storyboard; the storyboard is Markdown as easy to edit as the main video's | "Storyboard", "Recipe" |
| Q26, Q27 | The batch brings the approved storyboard into the repository, changes the kit and the recipe, films, renders and opens the PR | whole spec |
| Q28, Q33 | 16:9; this clip is 1280x720 at 15 fps (MP4 and WebM); the GIF stays at or under 12 fps and 960 px; size and frame rate are storyboard fields the kit reads, and the recipe's 1920x1080 and 30 fps rules follow them | "Kit: size and frame rate", "Recipe" |
| Q31 | One continuous shot kept; two captions in turn, one during the action, one during the zoom; the storyboard holds both texts and times | "Kit: captions" |
| Q34, Q39 | New scene: the selection starts inside the untitled `important` admonition, in the middle of the bold, crosses a small table and a `---`, and ends inside the `warning` admonition; new stage document and new take; the merged take is not kept | "New take" |
| Q35 | Every part the setting adds is outlined in turn: the opening `:::{important}` line, the opening `**`, the closing `:::`; the kit accepts several marks | "Kit: marks" |
| Q36 | Text 1: "From the preview, select and copy **raw Markdown**" | Storyboard |
| Q37, Q41 | Text 2: "Cut-off syntax is **completed** on copy to ensure valid Markdown"; the setting is not named on screen | Storyboard |
| Q38 | The storyboard is approved | Storyboard |
| Q40 | A storyboard section may hold several pictures, one per key moment (the selection, the paste, one per mark) | "Storyboard", "Kit: key frames" |
| Q42 | The PR body shows the GIF inline from the branch's committed file at the PR's head, and links the MP4 and the WebM by their raw URLs at the same head; each new render pushed updates the links; the recipe gains this rule | "PR", "Recipe" |
| Q43, Q44 | Seven more feature clips are planned, each its own CR depending on this one; this CR stays the raw copy clip only | "Out of scope" |
| Q45 | The Griller decided the remaining choices alone (Q46, Q47); they are listed as its choices in the PR's "Autonomous decisions" | "PR" |
| Q46 | If GitHub does not play the GIF in the PR body from the PR's head (Git LFS), the PR uses the PR guideline's `-assets` side branch for the GIF, MP4 and WebM and says so in the body; the owner can watch the clip from the PR page either way | "PR" |
| Q47 | Studio's floating "Comment" button beside the page selection after the paste is kept as filmed: no extra step to clear the selection | "New take and render" |

## What changes

All paths are relative to the repository root, on a branch from `origin/main` (which holds CR-482's
kit and clip; the local `main` may be behind: fetch first).

### 1. The live storyboard: `docs/demo-video/clips/raw-copy-balance-edges/clip.md`

Replace the merged `clip.md` (one field table) with the approved draft `work/storyboard/clip.md`,
adapted only as follows, without changing any on-screen text, time or shot the owner approved:

- Front matter: `status: approved` (the owner approved it on 2026-11-24, Q38), `date:` the day of
  the commit. The opening paragraph notes that the times and pictures follow the batch's take (the
  approved texts and shots do not change); the owner still reviews the cut in the PR.
- The opening paragraph speaks of the repository, not of the review draft: "This is the live
  storyboard. The clip is built from this file: edit any row marked *(on screen)*, save, and run
  `just clip raw-copy-balance-edges render`, then `check`. Rows marked *(filmed)* describe the take:
  changing them means a new take." Drop the sentences "Once approved, this file replaces ..." and
  "The pictures and times below come from the Griller's trial ...". Keep: one continuous shot, two
  texts in turn, the meaning of `**bold**`.
- `## Clip` table: the `Format` row is split so the kit can read it: `Size *(on screen)*` =
  `1280x720 16:9`, `Frame rate *(on screen)*` = `15 fps`, and an `Outputs` row with the rest
  ("silent, loops; MP4 (X, release), WebM (docs site), GIF 960 px (release notes, docs page)").
  `Length` stays `9.8 s` unless the new take needs another value (see section 5). `Filmed on` gives
  the batch's take: Windows, the VS Code version written in `check.json`, the extension version and
  "VSIX built from the branch".
- `## 2. Zoom on the pasted text`: add the row `Zoom | result, hold to 8.8 s` (the hold the section's
  Time already states), so the kit reads the zoom from the section that shows it.
- Pictures: the links point at the kit's key frames in `frames/` (section 3, "Key frames"):
  section 1 shows `frames/01-selected.png` and `frames/02-pasted.png`; section 2 shows one picture
  per mark, `frames/04-mark-1.png`, `frames/05-mark-2.png`, `frames/06-mark-3.png`, with the draft's
  alt texts. No `images/` folder and no JPEG in the repository.
- The "Expected paste" block stays as approved; the scenario's `EXPECTED` holds the same text,
  character for character (section 4).
- "Review notes": keep the note on the setting off (not filmed) and the note on the raw screencast's
  frame rate (the selection grows by steps; replace "trial" by the batch's measured `rawFps`). Drop
  the note on the Griller's scratch folder.
- Times and pictures come from the batch's own take and render: when the new take moves an action
  time, the section's `Time` row and the marks' times are updated in the same commit, so the file
  stays exact.

The storyboard format this file follows is the kit's contract, written in the recipe (section 6).

### 2. Stage and scenario: `docs/demo-video/clips/raw-copy-balance-edges/`

- `stage/runbook.md`: replaced by `work/storyboard/stage/runbook.md` (title "Release runbook",
  untitled `important` admonition with the bold "database migrations first", the two-row table, the
  `---`, the paragraph, the `warning` admonition, the "Rollback" section). `stage/notes.md` stays
  an empty file.
- `scenario.mjs`: replaced by the trial's `prototypes/01-trial-kit-changes/scenario.mjs`, with these
  changes:
  - the header comment describes the new scene (from inside the bold of the untitled admonition,
    across a table and a thematic break, to inside the warning admonition);
  - the mark ids are the storyboard's row numbers: `t.mark("1", …)` for the opening line,
    `t.mark("2", …)` for the opening `**`, `t.mark("3", …)` for the closing `:::` (and the matching
    `unmark`), each with a comment naming what it outlines;
  - `run(t)`: the check after the paste expects the non-empty count of the 16 pasted lines (12), not "at
    least 7": `if (lines.length !== 12) throw …` with a message naming 12;
  - `EXPECTED` is exported (`export const EXPECTED = ...`), so the storyboard test compares it with
    the shipped `clip.md` (section 7); `scenario.mjs` keeps importing nothing, so the test can load
    it without VS Code;
  - `verify(t)` throws when the paste differs, as the merged scenario does: `if (pasted !== EXPECTED)
    throw new Error(\`notes.md does not hold the expected text. Pasted: ${JSON.stringify(pasted)}\`)`.
    A difference is a finding against the feature (recipe, section 6), never "fixed" in the scenario.

### 3. The kit: `docs/demo-video/clip-kit/`

The trial's `kit.diff` shows the shape; write it properly, in the kit's style, with the tests of
section 7. Every refusal message starts with `clip.md:` as today.

**Storyboard parser, `lib/storyboard.mjs`.**

- Split pure functions out of the file reads so they can be tested: `parseClipText(markdown)` (what
  `parseClip(file)` does today, from a string; `parseClip` stays as its file wrapper) and
  `validateStory(story, take, host)` (the checks `buildStory` does against `take.json` and
  `host.json`; `buildStory` keeps the reads and the write of `story.json`).
- Field names: a trailing italic annotation `*(on screen)*` or `*(filmed)*` is stripped before the
  name is read (`Text 1 *(on screen)*` is the field `Text 1`). Rows of every table of the file are
  read, as today; a row is attached to the section (`## ` heading) it is in.
- Fenced code blocks (a line starting with three backticks or three tildes, up to the matching
  closing fence) are skipped: no field and no heading is read inside them. The "Expected paste"
  block holds a Markdown table (`| Step | Command |`, `| Migrate | ... |`) that must not become
  fields of section 2. `parseClipText` also returns the text of the fenced block that follows the
  line starting with "Expected paste" (`expectedPaste`, the block's lines joined with `\n`, the
  fences excluded), or `null` when there is none.
- `Length`: seconds, with or without a trailing ` s` (as today), 5 to 12.
- `Size`: `<width>x<height>` at the start of the value (text after it, such as `16:9`, is ignored);
  both even integers, aspect 16:9 (width * 9 === height * 16), else a refusal. Absent: 1920x1080.
- `Frame rate`: `<n> fps`, an integer from 12 to 30, else a refusal. Absent: 30.
- `Cards`: absent or `none`; any other value is refused ("the kit renders no card").
- Captions: a section's `Text <n>` row is a caption shown during that section's `Time`, whose value
  starts with `<from> to <to> s` (text after it, in parentheses or not, is ignored). Refused: a
  `Text` row in a section with no `Time` row or with an unreadable one; more than one `Text` row in
  a section; no caption at all; caption times that are not end to end from 0 to `Length` (the first
  starts at 0, each starts where the previous ends, the last ends at `Length`, within 0.05 s).
  The legacy single `Caption` row is no longer read (the only clip is migrated).
- `Badge <id>`: as today (the keycap text of each `press(…, id)`).
- `Zoom`: as today, `<id>, hold to <seconds> s`, one at most, wherever it is in the file.
- `Mark <id>`: any number, each `<what>, <from> to <to> s` (the trial's `timed` reading). A clip
  with no mark has no `Mark` row: the merged convention "`-` for none" is dropped (a `Mark` row whose
  value has no readable times is refused). Refused:
  a mark that ends before it starts, marks that overlap (they are shown in turn), a mark with no
  `Zoom`, and, in `validateStory`, a mark the take did not log or a mark outside the zoom hold
  (`to > zoom.holdTo` or `from < 0`). The take may log several marks; drop "the take logged more
  than one mark".
- `story.json` carries `captions: [{ text, from, to }]`, `marks: [{ id, what, from, to }]`,
  `width`, `height`, `fps` (from `Frame rate`, replacing the fixed `fps: 30`), and the rest as today.

**Badges.** `wrongModifier(text, platform)` is kept for a badge that names only the other
platform's modifier (`⌘C` alone filmed on Windows, `Ctrl+C` alone filmed on macOS: still refused).
A combined badge `<Ctrl form> / <⌘ form>` (exactly one ` / `, the first group with `Ctrl`, the
second with `⌘`) is accepted on every platform. In `remotion/src/Clip.tsx`, `Keycaps` splits a
badge on ` / ` into key groups separated by a white "/" (the trial's rendering): `Ctrl+C` is the
keys `Ctrl` and `C`, `⌘C` is the keys `⌘` and `C`.

**Captions in turn, `remotion/src/Clip.tsx`.** One caption pill per `story.captions` entry, at the
place and look of today's single pill; the first is fully shown at frame 0, the last until the last
frame, and two captions cross-fade over 0.2 s at their boundary (the trial's 6 frames at 30 fps).

**Marks in turn, `remotion/src/Clip.tsx`.** One orange outline per `story.marks` entry, its
rectangle from the take's logged mark of the same id, fading in and out over 0.2 s inside its
`from`/`to`, with the look of today's single mark.

**Size and frame rate.**

- `remotion/src/Clip.tsx`: the composition's `width`, `height` and `fps` come from `story.json`
  (not the constants `VW = 1920`, `VH = 1080`, `FPS = 30`). Every overlay dimension designed for
  1920 px (caption font 50 and padding, keycaps 44, badge and caption offsets, cursor, ripple, mark
  border, logo 56 and its margin) is multiplied by `width / 1920`, so a 1280x720 render looks like
  the trial's 1920x1080 render scaled down. Every duration now counted in frames at 30 fps
  (`ZOOM_FRAMES` 18, `BADGE_SHOW` 36, `BADGE_FADE` 10, `MARK_FADE` 6, `SEAM` 8, the caption
  cross-fade 6) is written in seconds and converted with the composition's `fps`, so the timing does
  not change with the frame rate. The scale factor from the take's window to the frame (`k`) follows
  the frame width.
- `lib/prepare.mjs` is unchanged: its `clip.mp4` stays the 1920x1080, 30 fps source footage, so a
  change of `Size` or `Frame rate` needs only `render`, not a new take.
- `lib/encode.mjs`: the poster and the key frames are at the master's size; the GIF ladder's width
  is `min(step width, story.width)`; the frame count uses `story.fps` (already the case).
- `lib/check.mjs`: "mp4 size" and "webm same size, fps and duration" compare with `story.width`,
  `story.height` and `story.fps`; "mp4 30 fps" becomes "mp4 <fps> fps"; the one-frame tolerance is
  `1 / story.fps`; the line "screencast at least 30 frames per second after retiming" becomes "at
  least the storyboard's frame rate after retiming" (the source is retimed to 30, which is at least
  any allowed frame rate). `check.json` writes the measured size and fps, as today.

**Key frames, `lib/encode.mjs`.** Keep `frames/01-selected.png`, `frames/02-pasted.png` and
`frames/03-zoomed.png`; add one frame per mark, at the middle of its `from`/`to`, named
`frames/<NN>-mark-<id>.png` numbered from 04 in the storyboard's order (`04-mark-1.png`,
`05-mark-2.png`, `06-mark-3.png`). The step empties `frames/` first, so no stale frame stays.

**The rest.** `clip.mjs`, `lib/take.mjs`, `lib/profile.mjs`, `lib/platform.mjs` change only where
the above needs it (`take.mjs`'s `mark`/`unmark` already log several marks). No new dependency, no
change to `package.json` or the lock files.

### 4. New take and render

On Windows, on this machine, with the screen unlocked and no other change running app-window tests
(`.agents/guidelines/local-worktree.guidelines.md`):

```bash
just dev
just package                                   # out/reports/package/markdown-okf-schema-studio.vsix
just clip raw-copy-balance-edges doctor
just clip raw-copy-balance-edges all --vsix out/reports/package/markdown-okf-schema-studio.vsix
```

- The take films the new scene of section 2 with `markdownOkfSchemaStudio.preview.rawCopy.balanceEdges`
  on, in reading mode, a CDP mouse drag from "migrations" to "every worker", `ControlOrMeta+C`, a
  click in `notes.md`, `ControlOrMeta+V`, the zoom on the pasted lines and the three marks in turn.
- After the paste, Studio's floating "Comment" button stays beside the page selection until the
  end and shows at the loop seam: it is kept as filmed (Q47); the scenario adds no step to clear
  the selection, and the storyboard gains no row for it. The owner may ask otherwise at the review.
- `verify` must pass: the paste equals the storyboard's "Expected paste" exactly. A difference stops
  the work: it is reported with the pasted text, as a finding against the feature.
- The trial measured 9.85 s filmed, so `Length` 9.8 s gives a playback rate near 1.0. If the batch's
  take differs, `Length` and the times in the storyboard follow the take (playback rate inside 0.77
  to 1.3), in the same commit as the render.
- Commit together (the recipe's rule): `clip.md`, `scenario.mjs`, `stage/`, the three outputs
  (`raw-copy-balance-edges.mp4`, `.webm`, `.gif`, Git LFS), `poster.png`, `contact-sheet.png`,
  `first-last.png`, `frames/*.png` and `check.json`. The merged take's outputs and frames are
  replaced; no file of the merged take that the new render does not write stays.

### 5. Docs that name the clip or the kit

- `docs/user/settings.md`: the clip's image stays at the same place; its alt text describes the new
  clip: "A selection from inside a bold text in an admonition, across a table and a thematic break,
  to inside another admonition is copied with Ctrl+C / ⌘C and pasted with Ctrl+V / ⌘V: the opening
  line, the opening bold and the closing line are added".
- `.agents/glossary/common.md`, "Feature clip": "one caption" becomes "one caption per beat, shown
  in turn", "one zoom on the result" stays, and "marks in turn" is added; the size is "1920x1080 or
  smaller, 16:9, set in its storyboard".
- No change to `README.md`, `docs/releases-notes/` or `CHANGELOG.md` (no `feat` or `fix` commit).

### 6. The recipe: `docs/demo-video/guidelines/feature-clip-process.guidelines.md`

Project guidelines name no process role and link no process document (constitution, section 8):
the text says "the maintainer" and "the agent", never a chantier role or a CR.

- Intro: "plays 5 to 12 seconds" stays; add that a clip may show one caption per beat and several
  marks in turn. The sentence "The kit adds no dependency ... and is not part of `just check`,
  `just preflight` or CI" becomes: the kit adds no dependency; its storyboard parser's tests run in
  `just check` (section 7); the take and the render are not part of `check`, `preflight` or CI.
- New section "The storyboard first", before "1. The kit and a take", with the order of the work:
  1. the agent writes the storyboard draft (section 2's format) outside the repository, before any
     branch, where the work is planned, with one picture per key moment from a trial take;
  2. the maintainer edits the rows marked *(on screen)* and says when done; the agent brings the
     rest of the file in line;
  3. only then the take; once approved, the draft is moved to `clips/<clip>/clip.md` and becomes the
     live storyboard;
  4. before each render after a change of text or time, the maintainer reviews `clip.md` again;
  5. the maintainer reviews the cut in the pull request (section 6).
- Section 1, "A trial first", (d): "at least 30 frames per second after retiming" becomes "at least
  the storyboard's frame rate after retiming". "Pacing": "zoom in and out over 600 ms (20 frames at
  30 fps)" becomes "over 600 ms".
- Section 2 rewritten as the contract of the Markdown storyboard, modelled on
  `short-demo-01/01-storyboard.md`: front matter `title`, `status`, `date`; a `## Clip` table
  (`Length`, `Size`, `Frame rate`, `Outputs`, `Cards` = `none`, `Logo`, `Setting filmed`,
  `Filmed on`, `Stage`); then one `## <n>. <beat>` section per beat, each with its pictures (one per
  key moment, the kit's `frames/`) and a table: `Time` (`<from> to <to> s`, then free text),
  `Shot *(filmed)*`, at most one `Text <n> *(on screen)*`, and, where they belong, `Badge <id>`,
  `Zoom`, `Mark <id>` (`<what>, <from> to <to> s`); the "Expected paste" block, the same text as the
  scenario's check; "Review notes". The annotations *(on screen)* (a new render) and *(filmed)* (a
  new take) are explained. The refusals of `storyboard.mjs` are listed (section 3 of this spec).
- The badge rule: badges read the combined form `Ctrl+C / ⌘C`, so one clip serves both platforms;
  a badge naming only the other platform's modifier is still refused.
- Section 2 also drops the "`-` for none" convention of `Mark <id>`: a clip with no mark has no
  `Mark` row.
- Section 3: the master is rendered at the storyboard's `Size` and `Frame rate` (1920x1080 and 30
  fps when absent), the WebM and the poster at the same. In the outputs table, the WebM row's
  "1920x1080, 30 fps" becomes "the master's size and frame rate" and the poster row's "frame 0,
  1920x1080" becomes "frame 0, at the master's size". The GIF stays at 12 fps or less and 960 px or
  less (or the master's width if smaller); "30 fps in the MP4 and WebM" becomes "the storyboard's
  frame rate"; "**960 px wide** (half the master)" becomes "**960 px wide** (half a 1920 px master;
  the master's width when it is narrower)".
- Section 5, the traps table, row "A window at device scale 2 ...": "the master is 1920x1080
  whatever the scale" becomes "the master is at the storyboard's `Size` whatever the scale".
- Section 6: "the three named frames" becomes "the named frames (`01-selected`, `02-pasted`,
  `03-zoomed`, and one per mark)". The `check` lines name the storyboard's size and frame rate
  instead of 1920x1080 and 30 fps. Add the rule of Q42: the pull request of a clip shows the GIF inline in its body, from the
  file committed at the PR's head, and links the MP4 and the WebM by their raw URLs at the same
  head, so the maintainer watches the clip without checking out the branch; each render pushed
  updates the three links to the new head. When GitHub does not play the GIF from the PR's head
  (Git LFS), the three files go to the pull request guideline's `-assets` side branch (raw blobs,
  "Screenshots in the PR") and the body links them there and says so (Q46).
- The host and default matrix rule stays.

### 7. Tests and the `just` target

- New file `docs/demo-video/clip-kit/lib/storyboard.test.mjs` (`node:test`, `node:assert/strict`,
  only Node built-ins, no ffmpeg, no VS Code, no network):
  - it reads the shipped `docs/demo-video/clips/raw-copy-balance-edges/clip.md` from the repository
    (path from the test file's own location, at the head under test, never a copy) with `parseClip`
    and asserts: length 9.8 (or the committed value), size 1280x720, fps 15, two captions with the
    exact texts of Q36 and Q41 and times end to end from 0 to the length, badges
    `Ctrl+C / ⌘C` and `Ctrl+V / ⌘V`, zoom `result`, three marks `1`, `2`, `3` in turn inside the
    hold; section 2 (`## 2. Zoom on the pasted text`) has no field `Step` and no field `Migrate`
    (the rows of the fenced "Expected paste" block are not read);
  - it imports `EXPECTED` from the shipped `docs/demo-video/clips/raw-copy-balance-edges/scenario.mjs`
    and asserts it equals the `expectedPaste` that `parseClip` returns for the shipped `clip.md`
    (the "Expected paste" fenced block), character for character;
  - it runs `validateStory` on that parsed story with a `take` object listing presses `copy` and
    `paste`, zoom `result` and marks `1` to `3`, once with `host.platform` `win32` and once `darwin`:
    both pass (the combined badges);
  - prepared texts, named in the test as refusal cases the shipped file cannot hold: a badge `⌘C`
    alone on `win32` and `Ctrl+C` alone on `darwin` (refused), a size not 16:9, a frame rate of 60,
    `Cards | opening`, two `Text` rows in one section, captions with a gap, overlapping marks, a mark
    the take did not log, a mark outside the hold, a missing caption, a `Mark 1 | -` row;
  - a prepared storyboard whose fenced block holds a `| Field | Content |`-shaped table: its rows
    give no field (a prepared text, since the shipped file's block holds another table);
  - a prepared storyboard with no `Size` and no `Frame rate` gives 1920x1080 and 30.
- `justfile`: a recipe `clip-kit-test` running
  `fnm exec -- node scripts/node-test.mjs clip-kit "docs/demo-video/clip-kit/lib/*.test.mjs"`
  (`node --test <dir>/` fails; the helper expands the pattern itself, with no shell, and writes the
  JUnit report to `out/reports/clip-kit/tests-clip-kit.xml`), following the `clip` recipe's style,
  with a one-line comment, added to the `check` dependency list. `AGENTS.md`'s "Main targets" line on `just check` and the "Feature clip" line mention it.
- These tests run in `just check`, so in the `ci-static` job (section "CI").
- `scripts/check-file-sizes.mjs`, `check-unused-exports.mjs` and the formatters: run `just check`
  and `just format`; if a script scans the new file and fails, fix the file, not the script.

### 8. The pull request

- Commits by area, Conventional Commits, no scope for `build` (allowed scopes are for `feat` and
  `fix` only): `build: read captions, marks, size and frame rate from the clip storyboard` (kit and
  its tests, the `just` recipe), `docs: add the storyboard step and the clip review rule to the
  feature clip process` (recipe, glossary, `AGENTS.md`), `docs: film the raw copy clip again from
  its Markdown storyboard` (clip folder, `docs/user/settings.md`).
- The PR body follows `.github/PULL_REQUEST_TEMPLATE.md` and the PR guideline. Impacts shows the
  clip inline: the GIF as `![...](https://github.com/gsemet/markdown-okf-schema-studio/raw/<head
  sha>/docs/demo-video/clips/raw-copy-balance-edges/raw-copy-balance-edges.gif)` (the `github.com
  /raw/` form resolves Git LFS; `raw.githubusercontent.com` serves the LFS pointer), and the MP4 and
  WebM linked with the same form at the same head sha. After each push of a new render, the links
  are moved to the new head with `gh pr edit <n> --body-file <file>`. Check that the GIF plays in
  the rendered PR page. If it does not (Q46), push the GIF, MP4 and WebM as raw blobs to the side
  branch named after the change branch with `-assets` added, as the PR guideline's "Screenshots in
  the PR" does, link them by their `raw.githubusercontent.com/<owner>/<repo>/<commit>/<name>` URLs,
  and say in the body that they come from the assets branch, rendered from the head sha named
  there. Each new render pushed refreshes them the same way. Either way the owner watches the clip
  from the PR page.
- "Autonomous decisions" lists the choices this spec made where the answers were silent: the field
  names `Size`, `Frame rate`, `Outputs` and the `Zoom` row added to section 2; mark ids as row
  numbers; the kit's allowed ranges (16:9, 12 to 30 fps); the parser tests in `just check`; the key
  frame names; the alt text and glossary updates; the parser skipping fenced blocks and the "`-` for
  none" convention dropped. It also lists, as the Griller's choices under Q45: the `-assets` fallback
  for the video in the PR (Q46) and the floating "Comment" button kept as filmed (Q47).

## Out of scope

- A second shot, a square crop, cards, music, the folder `short-demo-02/` (superseded, Q27, Q28).
- The off-clip checks of Q8 (context-menu Copy, paste into a rich editor) and a macOS take (Q9):
  macOS Cmd+C stays not proved in a real window.
- A smoother selection: the raw screencast's rate (about 4 to 5 frames per second) is a known limit,
  written in the storyboard's review notes, not fixed here.
- The seven other feature clips of Q43: each is its own CR, depending on this one (Q44).
- Placing the clip in the release notes or the announcement (the 1.13.0 release CR does it).
- Any change to the extension's code (`src/`) or to an SwRS: the kit and the clip are documentation
  tooling; no `@implements_req` or `@tests_req` marker moves. `SwRS-MDOKFSTUDIO-CORE-095` (the site
  turns a clip GIF into a video) is unchanged.

## CI

The only CI change is that `just check` runs `clip-kit-test`, inside the existing `ci-static` job
(Linux and Windows, `.github/workflows/ci.yml`).

- Environment: the CI machine set up by `just dev-ci` from the lock files: Node.js 24 from `.nvmrc`
  through `fnm`. Absent there and present locally: `ffmpeg`, the kit's scratch folder, the VS Code
  download, Remotion, a display. The tests need none of them (pure parsing of a committed file and
  of prepared strings).
- Before the push: `just check` passes on Windows (this machine), and `just clip-kit-test` alone
  passes; the output goes in the evidence. `just ci-static` on Windows.
- Only the first CI run proves the Linux leg (path handling of the test's file location, the
  quoted glob expanded by `scripts/node-test.mjs` under `fnm exec`).

## Host and default matrix

The clip depends on the host (the platform's copy chord) and on a configured value of an
off-by-default setting (`preview.rawCopy.balanceEdges`, filmed on).

| Host | VS Code | balanceEdges | Expected | Proof |
| --- | --- | --- | --- | --- |
| Windows 11, `Ctrl+C` / `Ctrl+V` through CDP | pinned `DEFAULT_CODE_VERSION` (1.147.0 unless moved) | on | paste equals "Expected paste" | the take's `verify` and `check.json` ("scenario verify passed") |
| macOS, `⌘C` / `⌘V` | same | on | same | not proved (Q9, known gap) |
| Linux | same | on | same | not proved |
| any | same | off (default) | copy from `migrations first**` to `every worker`, nothing added | not filmed; stated in the storyboard's review notes |

The storyboard parser's tests run on Windows locally and on Linux and Windows in `ci-static`.

## Evidence

1. `just clip-kit-test` and `just check` pass on Windows; the test reads the shipped `clip.md` at
   the head under test.
2. `just clip raw-copy-balance-edges all --vsix …` passes; `check.json` shows `passed: true`, MP4
   and WebM 1280x720 at 15 fps, the MP4 duration equal to `Length` within one frame, GIF at most
   960 px and 12 fps, loop seam SSIM in [0.98, 1.0), `verifyPassed: true`, `pasteWidgets: 0`,
   `readingMode: off`, playback rate inside 0.77 to 1.3, platform `win32`, extension source `vsix`.
3. The agent looks at the contact sheet and every key frame: the selection from "migrations" to
   "every worker", the table and the `---` in the paste, Text 1 during the action and Text 2 during
   the zoom, each mark on its added part in turn (`:::{important}`, the opening `**`, the closing
   `:::`), badges reading `Ctrl+C / ⌘C` and `Ctrl+V / ⌘V`, no tooltip, no personal name or path, no
   dirty tab. What was not checked (motion, rhythm, the loop as watched) is said.
4. A text-only change proves the "no new take" path: change Text 1 in `clip.md`, `just clip
   raw-copy-balance-edges render` then `check`, see the new text in a frame, revert, render again.
5. `just preflight` passes (on Windows, its static stage).
6. The PR body plays the GIF and links the MP4 and WebM at the head sha, or, when GitHub does not
   play it from the head, links the three files on the `-assets` branch and says so (Q46).

## Open questions

None: `02-answers.md` settles every point this specification needs.
