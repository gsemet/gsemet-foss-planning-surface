# Intent

The user, 2026-11-17, in a Griller session: assess the XState v6 beta
(<https://stately.ai/blog/2026-11-05-xstate-v6-beta>) on chantier itself. Research what it does,
find the gnarliest problem in chantier it could help with, build a proof of concept in a draft PR,
verify it fully, grade it (API nuance, type safety, testability, cyclomatic complexity, docs,
deployment changes) and give a recommendation. The full request is in `intake/request.md`.

This is an assessment, not a change to ship: the draft PR is evidence and is not to be merged.
The assessment, its grades and its evidence are in `prototypes/01-xstate-board-feeds/README.md`.

## What exists today

- chantier's own state machines are in Python: the CR lifecycle (`lifecycle/stages.py`, the stage
  folders), the batch record and the rails (`rails.py`). XState is a JavaScript/TypeScript
  library: it cannot reach them.
- The JavaScript in chantier is the web board's frame (`board/web/js/`, plain ES modules, no
  build, no npm, about 5,800 lines) and the plugin's pane (`hooks/register.tsx`, which imports
  only `claude-code`).
- The board's two hand-written pollers hold its gnarliest client-side state: `core/refresh.js`
  (the record every 5 s) and `views/prs-feed.js` (the forge every 10 s while a PR is not done,
  paused when the page is hidden, restarted when a CR gets a new PR, one read at a time, dropped
  answers after the view or the project changed). The proof of concept rewrites `prs-feed.js`.
