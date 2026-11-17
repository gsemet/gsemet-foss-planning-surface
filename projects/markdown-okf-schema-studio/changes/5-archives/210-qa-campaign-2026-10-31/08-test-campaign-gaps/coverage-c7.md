# Coverage note C7 (width modes, wide tables, sticky headings)

Exercised (session c7, side preview 220-786 px, Cream/Current/Dark/White themes):

- Width mode cycle margin/auto/full at 393, 566 and 786 px: attribute cycles correctly; content
  width identical in all three at these sizes (a 1440 px preview was not reachable: Electron window
  fixed, maximized group gives 786 px).
- Wide pipe table and long code line (`synth/c7-wide.md`): table and `pre` are `overflow-x:auto`
  with scrollWidth 1858/1137 vs 406 clientWidth; no page-level horizontal scroll at 220/438/786 px;
  no block outside the viewport in chapter 08 at 220 px.
- Sticky headings while scrolling (band text h1 then h1 + h2, inViewport, noClip) and while an
  inline paragraph editor is open (editor clear of the band, buffer unchanged).
- TOC column: hidden at 438 px (by CSS, but the toolbar toggle stays active with no hint), visible
  at 786 px, no overlap with content, jump target below the band.
- Heading fold: fold all, single fold/unfold keeps scroll position and heading top.
- Theme cycle: band and body background and text colours change together on all 4 themes.

Not exercised: real horizontal wheel/drag on the wide table scrollbar (reachability inferred from
overflow metrics), 1440 px width, sticky band with h3+ depth, edit-in-table while the band is
pinned (covered by C5), light-theme visual review of every mode.
