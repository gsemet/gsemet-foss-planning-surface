# Start an eval's operator, and its Foreman campaigns, from the phone

# Start an eval's operator, and its Foreman campaigns, from the phone

Split from `remote-control-start-session` (2026-11-20), whose grill and trials it carries. That CR
keeps the rule for starting the Foreman and Grillers from Remote Control; this one carries the eval
operator. The user asks no more questions: where the answers below are silent, the Chief of Staff
settles it ("Settled by the Chief of Staff (2026-11-20, the user asks no questions)"). The user wants
it before the next evals: "pour controller comment lancer les evals meme en remote".

## Facts (remote-control-start-session, 01-intent.md, 2026-11-20, Battlestation)

- **Refused:** from a session driven by Remote Control, `start_session` with a `cwd` (the eval
  root) or a `preset` is refused.
- **Started:** with no `cwd` it starts, in the steering session's own folder.
- **The move:** the started session moved itself into `C:\Users\gaeta\Projets\chantier-eval` with
  `mcp__ccd_directory__change_directory`, with no question asked (trusted tree, auto mode). Its
  next turn ran there.
- **The leak:** after the move it still held chantier's `AGENTS.md`, because a move does not
  reload project instructions. An eval forbids that.
- **The denied clear:** the Chief of Staff's `clear_session` of that session was denied by the
  auto mode classifier, and not retried.

## The user's answers carried over

2. **The operator from the phone.** The user: "trouve la solution pour que ca marche". The steering
   session starts the operator with no `cwd`. The operator moves itself into the workspace with
   `change_directory` and runs its campaign from its next turn on. Isolation is settled by trials in
   this order, each recorded proved or not:
   - the operator clears its own context after the move (`clear_session` with `self`), and the
     trial checks what its context holds afterwards;
   - else the user starts the operator from the phone's own New session on the workspace folder,
     the Chief of Staff giving the folder and the `prompt` line;
   - else the steering session starts in a neutral folder (the eval root), so that a start with no
     `cwd` lands outside chantier.

   No route may depend on the Chief of Staff clearing another session, nor on asking another
   session to do what was denied.
3. **Foreman campaigns from the phone** (`real-foreman`, `full`): "Oui". The operator, once in the
   workspace, starts the Foreman with no `cwd`, so the Foreman lands on the workspace's main
   checkout. The evals README and the `full` and `real-foreman` runbooks stop requiring the desk.
4. **Proof before the PR is ready:** "Essai du Studio + un essai ici". The route of answer 2 is
   tried for real on this machine, from Remote Control, and its output goes in the CR's evidence.
   The trial covers the start with no `cwd`, the move, the isolation check, and where a session
   started by the moved operator lands. A Driver has no session tools: the Chief of Staff runs the
   trial, with the user driving from the phone, at the Driver's request (a draft PR, the trial
   file's steps pending, then the Driver resumed).

## The spec critic's findings carried over (on remote-control-start-session's first specification)

- **Finding 2, the operator's prompt.** The `prompt` line that `evals/kit/setup.py` prints
  (lines 74-100 and 274-280) starts with `/chantier:chief-of-staff ...`. A session started with
  that prompt and no `cwd` runs the boot skill at once, in the steering folder, before any move.
  There, the seat is held by the live Chief of Staff, so the operator would become a Griller. A
  self-clear also wipes the prompt.
  Settled by the Chief of Staff: the steering session starts the operator with a short bootstrap
  prompt (the move into the workspace, the isolation step, then a report). Once the operator
  reports, the steering session sends setup's `prompt` line verbatim by message. `setup.py` is
  unchanged, and the trial checks that this works.
- **Finding 4, claims before the proof.** The lines saying a Foreman started by a moved operator
  lands in the workspace are unproved until the trial's last step. These are:
  - the README's "Prerequisites" and "Starting the Foreman";
  - both runbooks' "Start";
  - the hosts matrix row.
  They are written after the trial, to its result.
- **Finding 6, the trust premise.** The README's setup step (`evals/README.md` lines 105-109)
  rests on "a workspace inside the trusted root does not ask for trust (unproved), so the
  operator's session can start from Remote Control". It is aligned with the route found: the
  move asks nothing (proved), and the hosts card's "Trust of a workspace" row says the same.

## Scope

- `evals/README.md`, `evals/full/RUNBOOK.md` and `evals/real-foreman/RUNBOOK.md`.
- The rows of `skills/chantier/references/hosts/claude-code.md` for the self-clear, the operator's
  route and the folder of a start made by a moved session.
- The trial's evidence file in the CR's folder.

Mind `2-backlog/P3/evals-rework`, which edits the same README sections and renames the runbooks.
