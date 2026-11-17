# CR 213 — Inspector review, round 2

**Verdict: CHANGES REQUESTED.** All the round-1 items are fixed and the code is in good shape. What
is left is one small code change (selector clip padding), two doc fixes and a re-shot of the clip
proof. That fits in round 3.

What I checked myself: the full `git diff HEAD` against c1399a18. Only
`.agents/skills/markdown-studio-exploratory-qa-claude/` changed: 4 modified files plus the staged
rename `bug-sheet-template.md -> qa-bug-template.md`. No `bug-sheet-template` reference is left
outside archived CRs. I opened both proof images.

Gates, run by me:
- `node --check`: 8/8 `scripts/*.mjs` OK.
- Python: 4/4 files parse (`ast.parse`, so no `__pycache__` was created; none exists in the skill).
- `bash -n`: `setup-workspace.sh` and `q` OK.
- Scenarios: 22/22 parse as JSON.
- linkcheck.py: 18 links, 1 broken. That one is the pre-existing `…` placeholder at
  `references/harness-pitfalls.md:83`, which is not in this diff.
- Line length: no added prose line is over 100 chars. The only long lines are tables, the
  `FINDING` return lines and the link line in the NOTE. The other lines over 100 chars in `SKILL.md`
  and `charters.md` were already there before this change.

Cleanup: `pgrep -fl msq-cr213` is empty and `/private/tmp/claude-502/cr213-driver/qa` is gone.

## Round-1 items, verified in the code

1. **Label measured after attach.** Fixed: `root` is appended before any label is measured.
2. **Collisions.** Fixed. Each label tries above, then below, then the top-right corner inside its
   own outline. It is checked against every frame and every label already placed. If no spot is
   free, it goes above and a warning is printed.
3. **Bounds.** Fixed. The bounds are the resolved clip, or the window when there is no clip.
   `left` is clamped to the right edge.
4. **Empty and outside boxes.** Fixed. A 0x0 box throws. A box outside the clip, or outside the
   visible preview for a selector target, prints a warning on stderr.
5. **Proof retaken in a clean state.** No inline editor and no tooltip in the shot. The red label
   sits above its outline and the green label below its outline. Neither hides the text it points
   at, and nothing is cut off.
6. **Stale overlay.** Fixed. Every `#qa-annotations` is removed before drawing and again in
   `finally`.

The error paths are correct when I read the code; I did not run them, because inspectors do not
launch VS Code. `annotations()` throws before anything is drawn, and `finally` clears the overlay.

All the round-1 nits are done: `--which`, the count-mismatch warning, the error on a bare `--note`,
the object form in scenario-format.md, the "Example, from another finding" lead-in, the
`No test: <reason>` block, separate ticks in the short form, and the Gap row.

Option parsing: only `annotate`, `note` and `color` collect lists, and no other command reads
those keys. `--wait`, `--shot`, `--clip` and the other options keep last-value behaviour. Scenario
steps reach `shot()` through `ctx.shot(step.shot, step)`, and `[].concat` accepts a string or a list
there.

Code size: about 95 lines for the parser change, `annotations` and `drawAnnotations`. It is
readable, in qa.mjs style, with no new dependency. It is not over-engineered.

## Required changes

1. **A `--clip SELECTOR` shot always puts the label inside the annotated element**
   (`scripts/qa.mjs`, `resolveClip` / `shot`). The 12 px padding leaves no room for a label of
   about 20 px above or below the outline. So the label always falls back to the inside top-right
   corner. In the clip proof that corner happens to be empty space. On a paragraph target the label
   would sit on the very text it points at, which is the round-1 defect again. This is the common
   case: the template recommends `--clip SELECTOR` for the Currently shot, and the Expected shot
   is "the Currently shot annotated".
   - **Fix:** when the shot has notes, use a larger padding for the selector clip, enough for one
     label above and below. For example: `const pad = hasNotes ? 34 : 12`, passed from `shot()`
     into `resolveClip`, about 2 lines.
   - **Retake** `reports/cr213-annotated-proof-clip.jpg` with the same command. Confirm that the
     label now sits outside the outline.

2. **Document the known limit on neighbouring text** (`references/qa-bug-template.md`, "How to
   annotate"). Collision avoidance only covers outlines and labels, so a label can cover text that
   is not annotated. The current proof shows it: the green label hides "Tail paragraph.". This is
   acceptable as a known limit and does not need more code, but the doc must say it. Add one
   sentence such as: "A label can cover nearby text that is not annotated: open the shot, and
   shorten or drop the note if it hides something that matters." Put the same sentence in
   `charters.md` after "Check the printed boxes and open the image once."

3. **Fix the canonical example in "How to annotate"** (`references/qa-bug-template.md`, lines
   162–165). It does not match the fixture, the proof or the colour rule:
   - `aside[data-okf-github-alert] p:last-child` selects "Line one of a note.", not the lazy line.
     In `synth/admon.md` the lazy line ends up outside the alert, as `aside … ~ p`.
   - The red outline (defect) carries an "Expected: …" note.

   Agents will copy this example. Replace it with the command used for the proof:

   ```bash
   q shot QA210-03-currently --clip preview \
     --annotate 'aside[data-okf-github-alert] ~ p' --note 'Defect: lazy line leaves the Note' --color red \
     --annotate 'blockquote' --note 'Works: the quote keeps its lazy line' --color green
   ```

   Wrap the first `--annotate` line if it goes over 100 chars.

## Optional nits

- A bare `--annotate` (no value) is dropped without a message (`filter((a) => a !== true)`).
  Throw `annotate: --annotate needs a selector or x,y,w,h`, as `--note` already does.
- `--color` values other than `green` (a typo such as `gren`) silently become red. A one-line
  warning would help.
- `annotations()` indexes the visible previews without a clamp: `[Number(options.which ?? 0)]`.
  `wv()` clamps with `Math.min(which, len - 1)`. When `--which` is out of range, the "outside the
  visible preview" check is silently skipped. Clamp the same way as `wv()` so the two agree.
- "How to annotate" says "Labels are placed outside their outline … else inside its top-right
  corner". Consider "outside their outline when there is room (above, then below), else inside its
  top-right corner" so the sentence does not read as a contradiction.
