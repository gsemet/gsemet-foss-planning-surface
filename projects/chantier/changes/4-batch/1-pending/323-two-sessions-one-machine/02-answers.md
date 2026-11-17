# Answers

## Round 1 (2026-11-17)

- two-sessions-Q1 (the web board with two sessions on one surface): A, one board. `chantier
  board` sees that a board already serves this surface (its key is already in the git folder):
  it starts no second one and prints the running board's link.
- two-sessions-Q2 (commits by hand in one surface checkout): A, own project only. The cards say
  each session stages only its own project's folder (`projects/<name>/`), never `git add -A` nor a
  wider folder; then `git pull --rebase --autostash` and `git push`.
- two-sessions-Q3 (the machine's load): A, see it, no limit. No machine-wide cap: at the plan and
  in `status`, a session sees how many Drivers other batches already run, and picks its slots
  knowing it.
- two-sessions-Q4 (what each session knows of the other): A, list it. `preflight` and `status`
  list the other batches running on the same surface (project, batch, steering mode, state), read
  from the folders. No message between sessions.

## Round 2 (2026-11-17)

- two-sessions-Q5 (a board already runs on the surface, but of another chantier version, or it
  does not answer): A, say it, kill nothing. The new `board` reads the running board's version
  and process: same version and alive, it prints its link; another version or silent, it says so
  (version, PID, how to stop it) and does not start; the user decides.
- two-sessions-Q6 (which batches Q3 and Q4 see): A, the surface's. The batches of every project
  of the same planning surface, read from their folders; another surface or repository on the
  machine is not seen.

## Round 3, the spec-writer's questions (2026-11-17)

- two-sessions-Q7 (the one-board rule in a project with no external surface, planning in its own
  `.agents/changes/`): A, everywhere. One board per repository too: one rule everywhere; the
  `remote_board` scenario step changes accordingly.
- two-sessions-Q8 (the board keeps its PID, address and version in `chantier/board.json`, in the
  git folder, beside its key): A, yes. Same file, never published; `AGENTS.md`'s sentence says
  the board keeps there its key and the running board's address, PID and version.

The user asked to include this CR in the running batch-23.
