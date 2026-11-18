# Answers

1. Q: What is it for? User, 2026-11-18: "Ah il faut un déclencheur automatique du watcher. Il faut
   le spécifier ?", after the Chief of Staff had not started it for batch-28.

2. Q: How clear must the cards be? User, 2026-11-18: "Oui il faut que ces instructions soient
   claires pour pas être ratées."

## Settled by the Chief of Staff (2026-11-18, after answer 2)
- The step is not left in one long paragraph. It is written where the Chief of Staff reads it at
  the moment it acts: a numbered step of its own in chief-of-staff.md "Starting a batch" (right
  after `open` and the Foreman's start: "start the watcher"), a line in the Chief of Staff's
  startup core (read at every boot and reload: "a `watch: not running` line in any output: start
  it now"), and a row in the entry-points table for that line.
- The rule is one sentence, with the command as the CLI prints it ("run the printed command as
  is: no flag added"), so no flag is ever made up.
- Evidence includes a structure test that the startup core and "Starting a batch" carry the step.

3. Q: May the startup reading budget rise for the startup core line? User, 2026-11-18: "Je suis
   d'accord pour que la limite à 12K reste, il faut que ce noyau soit optimisé en taille et en
   efficacité." So: the limit does not rise (it stays 12544 in its three places); the startup core
   line fits by trimming wording (never a rule), as CR-363's spec allowed. If it cannot fit without
   dropping a rule, the Driver stops `blocked` with the measured numbers. The wider optimisation of
   the startup core is a CR of its own (`startup-core-optimise`).

## Settled by the Chief of Staff (spec-writer's questions, 2026-11-18)
- The watcher's own end line also carries the exact command (`cli_command(repo)`, no bare
  `chantier`), from the same helper, so the restart is also "run the printed command as is".
- The two cuts in `skills/chief-of-staff/SKILL.md` are accepted: each clause stays where the spec
  says (`session-start.md`, `AGENTS.md`, `chief-of-staff.md` step 1); no rule is lost.

4. Q: Should the watcher's end line say to start it again? User, 2026-11-18: "est-ce que ce
   serait judicieux dans le message de retour du watcher, en plus du ou des messages qu'il donne,
   de donner l'instruction de relancer si un batch est toujours en cours". Settled: yes. When a
   batch still runs, the end line is `watch: <batch> still running: for the Chief of Staff, start
   again in the background now: <exact command>`, the same shape as `watch: not running`; with no
   running batch, `no running batch` and no restart, as today.

## Settled by the Chief of Staff (spec critic, 2026-11-18)
- A watcher left by an earlier or other session: the watcher records the session that started it
  (the host's session id from its environment); the start line prints when no watcher of *this*
  session runs, and `status` names another session's watcher in one line.
- The watcher's own lock file `chantier/watch-<project>.lock` in the git folder, named in
  AGENTS.md's write lists, is accepted.

## Settled by the Chief of Staff (2026-11-18, the user asks no questions)
- The CLI cannot start the watcher itself: its end must wake the Chief of Staff's session, so it
  must be that session's background task. The trigger is therefore a printed step, not a spawn.
- When no watcher of the project runs (the CLI can tell: the forge hub's lock and `hub.json`, or a
  watcher's own record), these outputs end with one line `watch: not running: start in the
  background: <the exact command>`, with the right `--after <seq>` and no flag `watch` refuses:
  `open` (when the batch runs), the `take` or `order` that sets a paused batch running again,
  `status` with a running batch, and the switch to direct mode. When one runs, nothing is added
  (`status` keeps its `watch:` line as today).
- The cards (chief-of-staff "The watcher", session-start) make that line a step done at once,
  with the session's yes; after the user's no in the session, the Chief of Staff does not start it
  and the line is ignored.
- The Chief of Staff, not a Foreman or a Griller, starts it; a Foreman or Driver that sees the line
  ignores it (the line names the Chief of Staff).
- Out of scope: what the watcher reads and when it ends (unchanged); the factory mode's pause
  (a paused batch needs no watcher; the line comes back when it runs again).

## Settled by the Chief of Staff (spec-writer's question, 2026-11-18, second pass)
- The lock is one empty file per session that ran a watcher, `chantier/watch-<project>/<session>.lock`
  in the git folder, never removed; it replaces the single `chantier/watch-<project>.lock`, since
  one lock per project cannot tell this session's watcher from another's. AGENTS.md and
  CONTRIBUTING.md name this form.
