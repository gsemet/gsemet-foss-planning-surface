# Follow-ups from the final inspection of stack #230 → #234 (2026-10-31)

Not blocking; filed so they are not lost once the stack lands.
- Grid card editor CSS: `min-width: 24em` makes a one-column grid scroll in panes narrower than
  ~26em; use `min(24em, 100%)`. Auto-column grids may overlap instead of push; the wide palette can
  cover the first characters of the next card. (`src/core/preview/styles/gridCardEditStyles.ts`)
- `test/build/test_workflows.py`: assert the dispatch-only `toc-loop` job never runs on push/PR and
  is in no job's `needs`.
- Rewrap doc lines > 100 chars: `.agents/guidelines/ci.guidelines.md:80`,
  `CONTRIBUTING.md:443`, `CONTRIBUTING.md:447`.
- `comments.ts` `post()`: optional bounded retry after an UNREADABLE read (today stale until the
  next file event or render).
- `--myst-grid-track-min` leaks into nested grids; SwRS BLOCK-257 says "9em or 30% of the viewport"
  but the CSS takes min(9em, 30vh).
