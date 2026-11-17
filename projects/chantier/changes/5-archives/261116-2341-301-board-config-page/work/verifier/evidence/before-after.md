# Before and after

- Base (before): origin/main. The Configuration page and `/api/projects/<id>/config` do not exist there, so no
  before capture is possible (a new page).
- After, at 0198fd53a476f3e037a33127ed14482b19620264:
  - `after-config-pc-full.png`: the page on a scratch copy of docs/demo (top of the pane only; the pane scrolls).
  - `../../evidence-config-get.json`, `../../evidence-config-put.json`, `../../evidence-config.diff`: a GET with an
    `overridden_by` row and Copilot plans, a PUT and the written file's diff.
  - Reproduce: `work/verifier/probe.py <scratch> <work> <worktree>` and `work/verifier/shot.py <scratch> <out> <worktree>`
    on a scratch surface (a git copy of docs/demo whose `projects/shop-api/.repo` is a git repository holding a
    `chantier.yaml`).
