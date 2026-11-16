# Answers

Grill with the user, 2026-11-13 (asked in French, recorded in English).

1. **What the pages describe.** The docs already exist (with maybe some gaps), but this CR adds
   pages in `docs/` that explain how the web board's UI is launched and how it works. User's
   words: "la doc existe deja, il y a d'ailleurs peut etre des trous, mais la je veux des pages
   dans docs/ qui expliquent comment la UI se lance et fonctionne".
2. **When.** After the server's CRs: the docs are written once the server exists, with
   screenshots of the real server, not the prototype. ("tu feras la docs apres les CR du
   serveur".) So it runs after visualization-backend, board-read-views, board-backlog-edit and
   surface-autosync.
3. **When the screenshots are retaken.** By a command run by hand (e.g. a `just` recipe over a
   fixed demo batch), when the UI changes or before a release. Not at each release, not in CI.
4. **The README's representative screenshot.** The web board with a batch running; it replaces
   the pane's image (`docs/board-mod-batch.png`) in the README.
5. **Screens.** Each view is captured at PC width and at phone width, like the final QA.
6. **Data.** A fixed demo planning folder kept in the repository: the screenshots are the same
   from one run to the next.
7. **Gaps in the existing docs.** In this CR too: it goes through `docs/` and fills the gaps it
   finds, beyond the web board.

## Decisions after the specification

Asked by the Chief of Staff, 2026-11-13 (in French, recorded in English).

- **The page's language: both.** English by default and French, from one word file per language, built so that more translations can be added later. The prototype's French labels are the French file. Where an open point above says English only or French only, this answer replaces it.
- The other open points stay at the specification's defaults.
