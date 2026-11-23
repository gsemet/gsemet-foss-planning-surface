# Accept the project's checkout as the session folder beside the surface

chantier is for any target project. A project is planned in one of two layouts: in itself
(`.agents/changes/`), or in a planning surface that serves n projects (`<surface>/projects/<name>/changes/`,
the project's `checkout.yml` saying where its clone is: a gitignored subfolder of the surface, or
beside it). In a session of the host, the user may put both folders in the environment, and the first
one (the cwd) may be the project's clone, not the surface. Today the preflight fails then (P6 and P7,
the latter with a false "linked worktree" message), so no batch opens.

## What changes

- P6 and P7 pass when the cwd is the project's main checkout (its clone, not a linked worktree) or the
  surface's main checkout, whichever is first; a real linked worktree, of the project or of the
  surface, and any other folder still fail, each with its own exact message.
- A session finds the surface from the project's `AGENTS.md` pointer line (`- planning: <url>,
  projects/<name>`) and the folders present (the one whose remote is that url), switches to it for
  what is the surface's (planning writes, the plan's git, the board, the writer) and keeps working
  there: every git read of the CLI that concerns the surface (P11's branch, the others) runs on the
  surface whatever the cwd.
- A Foreman started from such a session (no `cwd`, it inherits the Chief of Staff's folder) passes its
  own preflight the same way.
- The cards (`session-start.md`, the host reference, `chief-of-staff.md`) say what the code does,
  for both layouts and both checkout places.

## Source

Filed by Studio's Chief of Staff (`intake/request.md`), seen the same day by chantier's own Chief of
Staff; the user ordered the fix and a release without eval right after (2026-11-23).
