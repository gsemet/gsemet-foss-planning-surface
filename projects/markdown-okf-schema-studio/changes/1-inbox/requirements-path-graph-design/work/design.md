# Use case path graph: joined map (proposal 2)

The owner liked the path graph but found it far too big, and rejected proposal 1 (one row per path, with grey
copies of shared states): "quand les noeuds sont les mêmes entre 2 paths ils sont joints". Proposal 2 draws every
state once. Paths enter and leave a shared state like metro lines, each keeps its colour, and a shared step shows
both colours side by side. Proposal 1 is kept in [rounds/proposal-1/](rounds/proposal-1/).

Kept from the current look: cream background, rust path 1, pills "ID · N tests", coloured scenario dots, Play path.

## What changes

- **Size.** The SVG is drawn at its natural size (a `width` attribute and `max-width:100%`), no longer stretched
  to the page (it was upscaled about 1.7 times). Narrow screens scroll, with a shadow on the right edge.
- **One node per state.** A state shared by several paths is one circle, thicker. A step taken by two paths is
  two parallel strokes in their colours. The goal ring takes the colours of the paths that end there.
- **Joins and splits.** A path that leaves a shared state goes down in a lane left of that state, then along its
  own row; one that joins comes up the same way. A path that starts at a state of an earlier path shows its number
  in a disc on the lane, and the legend says "path 2: …, starts at (2)".
- **Packing.** A path that shares no state with the others goes on the right of an earlier row when it fits, one
  column right of any climb, so it never reads as the continuation of another path.
- **Other outcomes.** A list under their state, on a dotted stem, wrapped to the room before the next state. A new
  behaviour is a dashed pill with its dots under it. An outcome of a behaviour already on the map shows its id and
  test count in grey text, then its dots.
- **Text.** Captions wrap at 34 characters (24 before a state whose path goes down); backticks become monospace.
- **What a path is, in one line.** Above the graph, one short line for a non-specialist: "This use case (StRS) is
  reached by 3 paths, one per coloured line. A path goes from one situation (circle) to the next; each step (pill)
  is a behaviour (SwRS) with its own tests. Where paths meet, they share the circle or the step." The acronyms are
  grey; the last sentence only when paths share something. It replaces the old hint paragraph above the map.
- **Legend.** Path keys with their titles, a "shared step" key (two colours, only when two paths share a step),
  "other outcome", and "one dot = one scenario checked" with dot swatches.
- **Play.** `viewer.js` lights the steps whose `data-paths` contain the path, in the order of `data-step-N`, so
  Play path 2 runs through the joined states.

## Size and overlaps (map height in px, 1280 px window / 800 px window)

| StRS | Shape | Before | After |
| --- | --- | --- | --- |
| BLOCK-003 | 1 path, 3 outcomes | 1041 / 770 | 533 / 560 |
| FMSCHEMA-014 | path 2 splits early | 791 / 616 | 653 / 694 |
| BLOCK-014 | 3 paths, 2 join, 1 alone | 1183 / 901 | 861 / 864 |
| MYST-006 | short | 910 / 675 | 374 / 401 |
| REVIEW-012 | long captions | 1582 / 1190 | 774 / 786 |
| MYST-009 | path 2 splits mid-way | 949 / 731 | 704 / 726 |

The after heights include the new explanation line and the legend (about 50 px).

Overlapping text or pills: before 1 to 8 per map in four maps; after 0 in all twelve shots. Shots in
[before/](before/) and [after/](after/), counts in their `metrics.txt` (made by [shoot.cjs](shoot.cjs)).

## Critic rounds (Fable, screenshots and the owner's rule only)

- **j1:** join rule met. Fixed after: outcome dots running into the next stem, the climb crossing dots, a faint
  shared step, no start mark, no scroll cue.
- **j2:** join rule met, readable without zooming; BLOCK-014 still one screen tall. Fixed after: packing of the
  lone path, wider captions, ids of outcomes at a split state, the climb moved to its own lane, bigger start disc in
  the legend, dots always under outcome pills, softer bends.
- **j3:** join rule met, 25-30 % shorter, no overlap. Fixed after: the lone path of BLOCK-014 read as the end of
  path 2 (now one free column apart), outcome ids and test counts shown everywhere, shared pills bordered in the
  first path's colour.

- **j4 (extra round, owner's wish that a non-specialist understands what a path is and that steps are shared):**
  "path" and "step = behaviour with tests" understood; asked to name the circles, to soften the acronyms, and to
  say "one dot = one scenario checked" (4 tests above 10 dots read as a contradiction). Done after, with its wording.
  Left: numbered badges at every path's start, a two-colour border on shared pills.

Notes: [rounds/joined/](rounds/joined/) (`critic-j1.md` to `critic-j4.md`, shots of each round).

## Open points for the owner

- **Narrow screens scroll.** At 800 px the maps of four columns scroll sideways (MYST-009, BLOCK-014) rather than
  shrink; the critic asked for a scroll hint stronger than the edge shadow.
- **BLOCK-014 is wider than the page** (five columns): it is drawn about 8 % smaller at 1280 px, to save 300 px of
  height.
- **Path numbers on the graph.** Only a path that starts on another path's state shows its number (the disc); the
  critic asked for a number at the start of every path, and a two-colour border on a shared step's pill.
- **Outcome stem beside a climb.** At a shared state, the dotted outcome list hangs 26 px from the coloured climb
  (BLOCK-014, MYST-009); readable, but close.

## Requirements touched

- SwRS-MDOKFSTUDIO-CORE-081 (the path graph of a use case): its text describes the graph; it needs the joined
  states, the two-colour shared steps, the start disc and the natural size.
- A new SwRS, or a CORE-081 item, for Play path over joined states (no SwRS covers Play today).

## Tests a change request needs

- Unit test of `buildMetroMap`: one node per shared state, an edge per step listing its paths, columns, packing of a
  lone path one column right of a climb.
- Unit test of `metroSvg`: `data-paths` and `data-step-N` on every step, one stroke per path, the start disc.
- No-overlap check on the generated pages: no two texts or pills overlap, no text runs past the SVG width (the
  check in `shoot.cjs`, moved into the visual tests).
- Visual capture of one StRS per shape (the six above) at both widths.
- Play test: Play path 2 of BLOCK-014 lights its three steps and four states, the joined ones included.

## Patch

[graph-design.patch](graph-design.patch) applies to `origin/main` 7c88b89c (`git apply`); it touches only
`test/site/requirementsViewer/` (`layout.ts`, `pages.ts`, `viewer.css`, `viewer.js`). The 31 unit tests of the
viewer pass with it.
