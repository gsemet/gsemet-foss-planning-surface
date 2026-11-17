# Requirements viewer on the published site (GitHub Pages)

User request (2026-10-24, renewed 2026-11-12): the published site shows the requirements, not only
the test gallery, as a viewer a reader can walk layer by layer, on a wide screen and on a phone.
It must look good and a little striking, and stay a professional tool (no glow, no particles, no
"AI slop").

## Intent

- Walk the traceability chain in four views, one level of detail each:
  1. the areas (the 16 scopes) with their description;
  2. one area: its use cases (StRS);
  3. one use case: a metro map of its main paths, the behaviours (SwRS) as the transitions and
     the options at each state; a click picks a behaviour;
  4. one behaviour: its rule, scenarios, and the source and test files that carry its markers.
- Search everywhere (areas, use cases, behaviours, files).
- Show why a use case names one or two paths while its behaviours are tested one by one (the
  combinatorics of the map).
- Superseded and deprecated requirements hidden by default, shown with a History toggle.

## State (2026-11-12)

Design explored and chosen; prototypes in `prototypes/journey/` (see `README.md`). Not started as
a change: no code, no requirement file changed yet.
