# Use case path graph: redesign proposal (proven by 3 Fable critic rounds)

Prototype on `origin/main` at 7c88b89c, not committed. Patch: [graph-design.patch](graph-design.patch)
(`test/site/requirementsViewer/layout.ts`, `pages.ts`, `viewer.css`). Screenshots: `before/`, `after/`
(final), `rounds/iterN/` (what each critic saw), critic notes `rounds/critic-1.md`, `critic-2.md`;
round 3 is summarised below. `shoot.cjs` rebuilds only the viewer pages from
`out/reports/requirements/requirements-report.json` and screenshots the map at 1280 and 800 px.

## Sample (6 shapes)

| StRS | Shape |
| --- | --- |
| BLOCK-003 | the owner's example: 1 path, 3 other outcomes at the first state |
| FMSCHEMA-014 | many side branches (7) on 2 paths, long path (5 states) |
| BLOCK-014 | 3 paths that meet (the old layout put paths 2 and 3 on the same row) |
| MYST-006 | one short path (2 states) |
| REVIEW-012 | long captions |
| MYST-009 | another area, 2 paths, path 2 starts on a path 1 state |

## Root causes of "far too big"

1. The SVG was drawn at `width:100%`: a small graph (3 columns, about 620 user units wide) was
   blown up about 1.7 times to fill 1032 px, text included. That is why the owner zoomed to 50%.
2. Every other outcome got its own track, 0.8 track (132 px) further from the line, joined by a long
   dashed curve: three outcomes stacked about 500 px above the line, and their pills, dots and
   captions sat on the curves of the others.
3. Paths after the second all shared row 1 (BLOCK-014: two start states drawn on top of each other).

## Final design (what changed)

- **Natural size.** The SVG has its own width in px and `max-width:100%`; it never grows. Under
  the box width it shrinks to 85% at most, then the box scrolls sideways (with a right-edge shadow
  as the cue). The phone list under 760 px is unchanged.
- **One straight row per path**, titled "Path N: title" in the path colour. A state already on an
  earlier path keeps that path's column when it can and is drawn grey with "↑ path 1: name"; a step
  already drawn on an earlier path is drawn faded, pill only. Path 3 gets its own colour
  (`--p3`, ochre) and legend swatch (it had none). The goal ring takes its path's colour.
- **Bands per row:** state names above the line, pill on the line, dots then caption under it
  (caption wrap 33 chars, 13.5 px, darker ink), then the other outcomes.
- **Other outcomes as a list hanging from their state** on a dotted stem: each outcome is a tick
  ending in a small hollow circle (the end state of the old curves), its dashed pill and its dots on
  one line, its caption under it, as wide as the room up to the next state that has outcomes (up to
  420 px). An outcome that is another scenario of the behaviour drawn on the line just there has
  no second pill (the old one repeated "BLOCK-014 · 16 tests").
- **Backticks** in captions and state names render as monospace without the ticks.
- **Legend:** "one dot per scenario" (the dots are scenarios, the pill counts tests); dotted
  swatch for "other outcome".
- Play path still works (checked: path 2 of BLOCK-014 lights 3 steps and 4 states).

## Size (map box height at 1280 px, before → after)

| StRS | Before | After |
| --- | --- | --- |
| BLOCK-003 | 1041 | 442 |
| FMSCHEMA-014 | 791 | 590 |
| BLOCK-014 | 1183 | 1043 (3 paths; before, two paths were drawn on top of each other) |
| MYST-006 | 910 | 315 |
| REVIEW-012 | 1582 | 714 |
| MYST-009 | 949 | 608 |

Text sizes are now 1:1 (13.5-14 px); before, they were 1.2-1.7 times larger on small graphs.
Overlapping label boxes (texts and pills, from `shoot.cjs`): before 1-8 per graph, after 0 on
all 12 shots.

## Rounds

**Round 1** (iter1: natural size, rows per path, outcome list). Critic: clearly more readable, no
overlap left. Main points: narrow width shrank text to 7-8 px; shared states truncated with "…";
path 3 same colour as path 2, no swatch; outcome dots ran into the next column; a side pill
repeating the step's id and count; captions narrow and faint. Fixed in round 2: 85% floor then
scroll, full names with "↑ path N", `--p3`, dots under the pill, id-only repeat, wider and darker
captions, monospace code, left-aligned graph.

**Round 2** (iter2). Critic: readable; much smaller for one path, multi-path still tall. Main
points: outcomes take 3-4 lines each with the right side empty; repeated id pill without a count
looks like a bug; "N tests" never matches the dots; captions small; no cue that the narrow map
scrolls. Fixed in round 3: outcomes on one line when the room allows, no pill for the same
behaviour, legend "one dot per scenario", 13.5 px darker captions, tighter gap between paths, scroll
shadow, stronger path titles.

**Round 3** (iter3). Critic: "clearly more readable and, for small graphs, far smaller; the owner
should no longer need 50% zoom"; only the 3-path BLOCK-014 is taller than a screen, and it reads as
three rows. Main points: one caption clipped at the right edge (REVIEW-012); three different
layouts for an outcome; outcomes too close to each other; count vs dots. Fixed after round 3 (the
3-round limit reached, checked by me on the final shots): the SVG width includes the widest
outcome caption, one outcome layout everywhere (tick + hollow circle, pill if another behaviour,
dots, caption under it), a larger gap between outcomes than inside one.

## Open points for the owner (not changed)

1. The pill counts **tests** (test files citing the SwRS), the dots are **scenarios**: they
   never match (for example "REVIEW-133 · 2 tests" over 9 dots). All three critics flagged it. The
   legend now says what a dot is. Options: keep; "2 tests · 9 scenarios"; or drop the count.
2. **Lost from before**, said by every critic: the picture of paths physically merging (now grey
   "↑ path 1" states) and the organic dashed curves. The hollow end circle of an outcome is back.
   A faint connector between the copies of a shared state was not drawn because it would run on
   the outcome stem of the same state.
3. Multi-path maps stay tall (BLOCK-014: 3 rows, 1043 px). Placing two short paths side by side
   was suggested; not tried.
4. Play buttons stay above the map, not beside each path title.

## For the change request

- **Requirements touched:** SwRS-MDOKFSTUDIO-CORE-081 ("draws the map of a use case from its
  Main paths", implemented in `layout.ts`) gains its layout rules: one row per path, natural size
  (never scaled up, at most 15% down, then scrolled), other outcomes listed under their state, no
  overlap of labels. Probably a new SwRS (or scenarios on CORE-081) for "a state or step shared with
  an earlier path is shown once per path, marked as shared" and for "path 3 has its own colour".
  No other viewer SwRS mentions the map; the Play behaviour has no SwRS.
- **Tests a CR needs:**
  - unit (`layout.test.ts` or `pages.test.ts`): `buildLanes` on the fixture (columns, shared
    states, shared steps), the SVG has a `width` attribute and no scaling CSS, an outcome with the
    id of the step has no pill, backticks become a `code` tspan;
  - visual capture per StRS shape (the six above, desktop and 800 px), like `shoot.cjs`;
  - a no-overlap check in Chromium: the bounding boxes of every `text` (except pill text) and
    every `rect.pill` in `svg.metro` do not intersect, on every use case page with paths
    (`shoot.cjs` does it on six; extending it to all 93 is cheap), plus "no text box goes past the
    SVG's width";
  - the Play test: playing path N lights its steps and states.
- **Prototype limits:** text widths are estimated by character counts (6.4-6.8 px/char); a
  measured layout would be safer. `buildGraph` stays only for the walk count. Viewer unit tests
  pass (31/31), `just check-limits` and `just check-exports` pass; `just preflight` not run (no
  commit).
