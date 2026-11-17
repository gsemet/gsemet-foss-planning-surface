# Decisions (owner, 2026-11-03)

- On a narrow viewport, with the TOC toggle on: a thin rail on the right with one tick per heading,
  the reader's position highlighted.
- Hover or keyboard focus on the rail opens the TOC as an overlay above the text; it closes 300 ms
  after the pointer leaves, or on Escape. A click on a tick navigates to that heading.
- The toggle state is honoured: today the TOC stays hidden although the toggle is on (screenshot).
