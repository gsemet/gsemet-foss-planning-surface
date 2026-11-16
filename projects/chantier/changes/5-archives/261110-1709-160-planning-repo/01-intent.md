# Intent: an external planning surface, a fully supported mode

The user's idea, filed during batch-08 (steered in direct mode), amended the same day; to be
grilled once that batch completes. The full specification is written at the grill.

## Name

**External planning surface.** The *planning surface* is the tree chantier plans in (inbox,
backlog, requests, trash, batch state). By default it lives inside the project
(`.agents/changes/`, today's behaviour, unchanged); in this mode it lives in a git repository
of its own, outside the project. The two modes: *in-project* (default) and *external*.

## What the user wants

- **A fully supported mode**, not a workaround: every command, card, agent and host works the
  same on an external surface as in-project, and `just scenario` covers it.
- **One surface for one or several projects:** each project gets a sub-folder holding the whole
  chantier tree without the archives. For the user's open-source projects:
  https://github.com/gsemet/agentic-planning-surface.
- **Archives stay with the code:** a landed CR's archive goes to the project's own repository
  (for example `.agents/changes/archives`), in the same format, cleaned and committed there.
- **The archive folder is separate in both modes**, so it can be cleaned and committed.

## How it should work (to settle at the grill)

1. **Declaring it:** the project's `AGENTS.md` names the surface (its repository, local path,
   and the project's sub-folder), as the only configuration; nothing set means in-project.
   Where the local clone lives and who clones it.
2. **Finding it:** how `$CHANTIER` resolves the root of planning and the root of archives from
   the project, and from a Driver's worktree; a project sub-folder name when two projects share
   a surface.
3. **What goes where:** inbox, backlog, requests, STATUS files, batch state and trash on the
   surface; archives in the project. Which files an archive keeps once "cleaned" (the
   specification, the report, the cost; not the transcripts' scratch).
4. **Git on the surface:** who commits and pushes it and when (the Chief of Staff after a file,
   a grill, a batch open or close?), the commit message, conflicts when two sessions or two
   machines plan at once. The CLI does not operate git (CLI scope): the agents do.
5. **Git on the archives:** the archive lands in the project with the CR's PR, or in a later
   commit at `close`; who commits it, on which branch, given that `main` may be protected.
6. **One batch at a time:** per project or per surface.
7. **Drivers and workers:** they read their CR folder on the surface from a worktree of the
   project; paths in prompts and briefs.
8. **The rule in AGENTS.md** "chantier writes only in `.agents/changes/`" becomes "only in the
   planning surface and the archive folder".
9. **Migration:** moving an existing project's tree to a surface, and back; existing archives.
10. **Hosts:** Claude Code and Copilot alike; Remote Control.
11. **Privacy:** a public surface repository exposes requests and grills; the user chooses.
