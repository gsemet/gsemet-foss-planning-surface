# Answers

## 2026-11-20, grill with the user (Remote Control)

1. **The no-argument mode under Remote Control.** Asked: now that a Foreman can start from Remote
   Control, does a batch planned with no argument under Remote Control become Foreman? The user:
   "Direct, comme aujourd'hui". The no-argument rule stays: direct under Remote Control, Foreman
   at the desk. The docs only stop saying a Foreman cannot start there; a forced `foreman` under
   Remote Control now starts a new Foreman with no `cwd` (not only the reuse of the last one).
2. **Starting an eval's operator from the phone** (a start with `cwd` = the workspace is refused).
   The user: "trouve la solution pour que ca marche". The Chief of Staff's trials (01-intent.md)
   give one route that works today: the steering session starts the operator with no `cwd`, the
   operator moves itself into the workspace with `change_directory` (no question inside the
   trusted tree) and runs its campaign from its next turn on. Its open point is isolation: the
   operator keeps the instructions of the folder it started in (chantier's `AGENTS.md`), which an
   eval forbids. The Driver settles it, in this order, and records each try as proved or not:
   - the operator clears its own context after the move (`clear_session` with `self`, which the
     host offers), so its next turn loads only the workspace's instructions; the trial checks what
     its context holds after the clear;
   - else the user starts the operator from the phone's own New session on the workspace folder
     (the evals README's route, unproved), the Chief of Staff giving the user the folder and the
     `prompt` line;
   - else the steering session starts in a neutral folder (the eval root itself) so that a start
     with no `cwd` lands outside chantier.
   The Chief of Staff's own clear of another session was denied by the auto mode classifier: no
   route may depend on it, nor on asking another session to do what was denied.
3. **Foreman campaigns from the phone** (`real-foreman`, `full`). The user: "Oui". The operator,
   once in the workspace, starts the Foreman with no `cwd`, so the Foreman lands on the workspace's
   main checkout. The evals README ("Prerequisites", "The operator", "Starting the Foreman") and
   the `full` runbook stop requiring the desk for this.
4. **The proof before the merge.** The user: "Essai du Studio + un essai ici". The Studio's trial
   and the Chief of Staff's trials (01-intent.md) are quoted; the route of answer 2 is tried for
   real on this machine, from Remote Control, before the PR is ready (a start with no `cwd`, the
   move, and the isolation check of answer 2), its output in the evidence. The first eval run from
   the phone proves the campaigns end to end.

## Scope (settled by the Chief of Staff)

- `skills/chantier/references/hosts/claude-code.md`: the classes row, the Surfaces table's start
  row, the "Remote" paragraphs (the 2026-11-10 finding: a remote session cannot be started outside
  a worktree) and "The trial that settles a new Foreman from a remote client", each marked with
  the trials above.
- Every card and doc that repeats "cannot start a session under Remote Control"
  (`chief-of-staff.md` "Starting a batch" and the forced `foreman` case, `session-start.md`,
  `init.md`, `planning-modes.md`'s Remote section and its texts file, `docs/hosts.md`,
  `docs/tutorial-claude-code.md`, `docs/use-cases-direct.md`, the evals README and the `full`
  runbook): true again, with the no-argument mode unchanged (answer 1).
- When merged, the Studio's Chief of Staff is told in one line (its request).
