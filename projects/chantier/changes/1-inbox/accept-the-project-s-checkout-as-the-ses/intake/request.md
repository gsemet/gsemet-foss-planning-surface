# Accept the project's checkout as the session folder beside the surface

A Claude Code session can hold both the project's main checkout and the planning surface as
working folders, and the project's checkout may be the first one (the session's cwd). chantier
must accept this layout as a natural case: it "switches" to the surface on its own, instead of
failing the preflight.

Seen on 2026-11-23 (Battlestation, chantier 0.15.0), Studio's Chief of Staff session, cwd
`C:\Users\gaeta\Projets\markdown-okf-schema-studio` (main checkout, `--git-dir` = `--git-common-dir`
= `.git`, on `main`, clean), the surface `C:\Users\gaeta\Projets\gsemet-foss-planning-surface`
added as a working folder, `$CHANTIER --project <surface>/projects/markdown-okf-schema-studio`:

    P6 FAIL session folder C:\Users\gaeta\Projets\markdown-okf-schema-studio is not the repository root C:\Users\gaeta\Projets\gsemet-foss-planning-surface
    P7 FAIL this session runs in a linked worktree: the Foreman must start in the main checkout

Both the Foreman-mode preflight and `preflight --direct` fail, so no batch can open; the user's
"start a Foreman in factory" was refused.

Cause: `Repo.session_root` (core/repo.py) is `self.surface or self.root`, and
`_check_checkout` (commands/preflight.py) compares it with the cwd's `--show-toplevel` (P6) and the
surface's git dir with the cwd's `--git-dir` (P7). The project's main checkout always fails both.
P7's message is wrong too: the folder is no linked worktree.

`session-start.md`, section 1, already names this layout valid ("the project's main checkout with
the surface added as a working directory"), so the code and the card disagree.

Wanted:
- P6/P7 pass when the cwd is the project's main checkout (not a linked worktree) and `--project`
  names that project's folder in a surface, as well as when the cwd is the surface's checkout.
- chantier works from the surface for what is the surface's (planning writes, git of the plan,
  the board) and from the project's checkout for what is the project's, whichever folder is the
  session's cwd: the "switch" is chantier's, not the user's.
- A Foreman started from such a session (no `cwd`, it inherits the Chief of Staff's folder) is fit
  too, and its own preflight passes the same way.
- P7 keeps failing for a real linked worktree, of the project or of the surface; its message names
  which check failed.
- The host reference and `session-start.md` say the same as the code.
