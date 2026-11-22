Short name: `session-folder`

# Answers

Triaged P1 on the user's word, 2026-11-23 (from the filing of Studio's Chief of Staff, which saw P6 and P7 fail in a session whose cwd is the project's main checkout with the surface added). The Chief of Staff of chantier hit the same failure at the start of its own session the same day.

1. session-folder-Q1: **Which session folders pass P6 and P7.** The user did not pick from the form; their words of 2026-11-23: chantier is for any target project, in two layouts (one project, planning in `.agents/changes/`; one surface for n projects, planning in `<surface>/projects/<name>/changes/`), the project's clone may be a gitignored subfolder of the surface or beside it, and the session may hold both folders with the first one not the surface. Chief of Staff reading: option A, both main checkouts (the surface's, the project's clone) and nothing else; a real linked worktree still fails.
2. session-folder-Q2: **How far the switch to the surface goes.** The user's words: "il faut donc que chief of staff se base sur AGENTS.md qui declare la surface, sur la presence de la surface et apres switch de surface et ne se trompe plus par la suite". Chief of Staff reading: option A, every git read of the CLI that concerns the surface is made on the surface whatever the cwd; the surface is found from the project's `AGENTS.md` pointer line and the folders present, then kept.
3. Destination: running batch batch-31. The user's words: "tu vas fixer ce probleme d'initialization tout de suite et faire une release sans eval immediatement apres." No critic (the user asked for speed; the batch's inspector and verifier review the code). Release right after this CR, with no eval run, on the user's word.
