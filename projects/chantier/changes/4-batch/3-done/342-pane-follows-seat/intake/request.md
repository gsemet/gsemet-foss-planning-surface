# The CR board pane shows the session's own project on a planning surface

The user (2026-11-17), on a screenshot of the CR board pane (`/chantier:board`) in the Studio
Chief of Staff's session: the pane shows "No chantier status here:
.../projects/agentic-planning-surface/changes/STATUS.json not found." then chantier's batch-24,
not Studio's batch. The user asked for a debug agent and then chose its option 1.

Diagnosis (read-only debug agent, 2026-11-17):
- The pane works out its project from the session's folder alone: `findRoot`
  (`hooks/register.tsx:173-184`, `git rev-parse --git-common-dir` of `$.session.cwd()`), then
  `findBases` (`:155-171`): with no `<root>/.agents/changes` and a surface root, it returns
  every `projects/<name>/changes`, sorted by name; `Board` (`:1011-1028`) draws one section
  each, and a project with no index gets the "No chantier status here" line (`:1017`).
- The CLI refuses the same ambiguity (`core/repo.py:116-118`, `SurfaceChoice`); the pane does not.
- `projects/<name>/changes/seat.json` already names the session holding a project's seat (Studio's
  names `local_f2e6c4ee-...`).
- A second trap: a stale `.agents/changes/` in Studio's repo (only `1-inbox`, `3-requests`,
  `.lifecycle.lock`, from 2026-11-10) makes both the pane (`findBases:158`) and the CLI
  (`repo.py:116`) take it as in-project planning and ignore the `planning:` line.

Chosen fix (option 1): on a surface root, the pane keeps only the project whose `seat.json` names
this session; with no seat for it, it shows the list as today under a line saying so.