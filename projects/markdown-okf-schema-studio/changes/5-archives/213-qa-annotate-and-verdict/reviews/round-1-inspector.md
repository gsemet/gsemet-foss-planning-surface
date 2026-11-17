# CR 213 — Inspector review, round 1

**Verdict: CHANGES REQUESTED** (not too fragile: the fixes are small and local, about 20 lines in
`drawAnnotations`/`annotations` and a re-shot of the proof.)

Gates I ran myself: `node --check` on every `scripts/*.mjs` OK; Python files parse; `bash -n` on
`*.sh` and `q` OK; 22 scenarios parse as JSON; linkcheck.py: 18 links, 1 broken, the pre-existing
`(…)` placeholder at `references/harness-pitfalls.md:83` (not in this diff). Scope: only
`.agents/skills/markdown-studio-exploratory-qa-claude/` changed (5 files + staged rename);
`grep -rn bug-sheet-template` in the whole worktree finds nothing outside archived CRs.
`pgrep -fl msq-cr213` empty; `/private/tmp/claude-502/cr213-driver/qa` gone. New prose lines are
<= 100 chars except tables, the existing `FINDING` return lines and one link line (acceptable).
I opened the proof image.

## Required changes

1. **Label height is measured on a detached element, so every label lands on top of its own
   outline** (`scripts/qa.mjs`, `drawAnnotations`). `label.getBoundingClientRect().height` is read
   before `root` is appended to `document.body`, so it returns 0; `top` becomes `n.y - m - 3` and
   the 20 px label extends downward over the top of the box. That is exactly what the proof shows:
   the red label hides "lazy continuation line of the note.", the very text pointed at. Fix: append
   `root` to `document.body` before the loop (or append each label first, then measure), then place
   the label strictly outside the outline: above it, else below it.

2. **Labels must not cover other annotations** (`scripts/qa.mjs`, `drawAnnotations`). Even with
   item 1 fixed, the green label (above the green box) would sit on the bottom of the adjacent red
   box. Keep the placed rects (frames and labels) in a list; for each label try above, then below,
   then inside the top-right corner of its own frame, and take the first spot that intersects no
   other frame or label. If none is free, keep "above" and print a warning
   (`annotate: label of <target> overlaps another annotation`). A caption band would also work but
   is harder with a selector clip; the side flip is enough. Document the rule in one sentence in
   "How to annotate" (`references/qa-bug-template.md`).

3. **Labels are placed against the window, not against the shot clip** (`scripts/qa.mjs`, `shot`
   and `drawAnnotations`). With `--clip SELECTOR` (12 px padding) or a tight `--clip x,y,w,h`, the
   label "above" the box falls outside the clip and is cut off; the "below" fallback only triggers
   when the label would leave the window (`< 0`). Pass the resolved clip rect (or the window rect
   when there is no clip) to `drawAnnotations` and use it as the bounds for the above/below/inside
   choice of item 2; also clamp `left` so the label does not run past the right edge of the bounds.

4. **Empty or off-screen boxes are drawn silently** (`scripts/qa.mjs`, `annotations`). A hidden
   element (`display:none`) gives `w=0 h=0` at the webview origin and draws an 8x8 square in a
   corner; an element scrolled out of the preview gives a box outside the webview, drawn over the
   workbench chrome. Fix: throw `annotate: <target> has an empty box` when `w === 0 || h === 0`;
   print a warning (stderr) when the box does not intersect the shot bounds (clip, or visible
   webview for selector targets). Evidence must not carry an outline in the wrong place.

5. **Re-take the proof** (`<CR folder>/reports/cr213-annotated-proof.jpg`) after 1–4, in a clean
   state: inline editor closed (`Escape`), pointer moved off the toolbar so no tooltip shows. Use the
   same two annotations (red on the alert's lazy line, green on the quote) so labels sit outside
   their outlines and do not overlap; also take one with `--clip '<selector>'` to show item 3. Stop
   the session and delete the QA root again.

6. **Stale overlay** (`scripts/qa.mjs`). If a run is killed between draw and cleanup, the overlay
   stays in the window and the next cleanup removes only the first `#qa-annotations`. Fix: in
   `drawAnnotations` start with
   `document.querySelectorAll('#qa-annotations').forEach((e) => e.remove())`, and do the same in the
   `finally` (and run it even when `notes` is empty, it is cheap).

## Optional nits

- `annotations()` ignores `--which`; `box`, `clicksel`, `feval` honour it. Pass `options.which` to
  `wv` so annotations work with two previews.
- Warn when there are more `--note` (or more than one `--color` but fewer than `--annotate`) than
  `--annotate` values: a silent mismatch shifts notes onto the wrong box. A bare `--note` with no
  value currently renders the label "true".
- `scenario-format.md`: mention the `{ "at", "note", "color" }` object form that the code and
  "How to annotate" describe.
- `qa-bug-template.md`, full form: the owner's "Test to add" example (link-card click) sits under a
  wide-table sheet title; add a lead-in such as "Example:" or one sentence saying the example is
  from another finding, so the template does not read as one inconsistent sheet. Also show the
  `No test: <reason>` form once in a code block under "Proposals and balance".
- Short form folds test and requirement under a single tick, so the owner cannot accept one and
  reject the other; consider two tick lines, or say that unticking drops both.
- Gap row of the Verdict table: the spec adds "The sheet names the missing test (the template's
  'Test to add')"; add it, qualified by the balance rule ("or says No test: <reason>").
- linkcheck.py does not check `#anchor` targets; `#how-to-annotate` resolves today (heading exists),
  checked by hand.

## Docs checked and found correct

Part 2 items 1–7 present (Purpose first paragraph of `SKILL.md`; requirements search in `SKILL.md`
and `charters.md`; "Why this is wrong" after Currently / Expected; Verdict and Requirements fields
and table; Expected names its source; triage paragraph; severity line in the index description and
the template). Part 3 rename staged as a rename, draft sections kept, plain line under the title, no
front matter, every link updated. Part 3b: tick line on all four proposal sections, `No test:
<reason>` + tick, balance rule in template AND `SKILL.md`, fix CR does only ticked sections, owner's
example present, no separate "Owner decisions" checklist. "How to annotate" with an example in the
template and in `charters.md`; design choice (overlay in the workbench page, no install) documented.
`FINDING` return lines carry `<Bug|Gap|Decision>` in both charter prompts.
