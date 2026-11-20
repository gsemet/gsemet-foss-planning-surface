# Start an eval's operator, and its Foreman campaigns, from the phone

Change Specification, written 2026-11-20 from `intake/request.md`. The grill and the trials are in
the sibling CR this one was split from,
`4-batch/3-done/414-remote-control-start-session/` (its `01-intent.md`, `02-answers.md` and
`03-change-spec.md`, "part B"). That sibling is merged on chantier's `main` (`4ed0d56c`), and this
specification reads the files as they are at that commit. No issue.

The user asks no more questions. Where the answers are silent, the point is settled here and marked
"Settled by the Chief of Staff (2026-11-20, the user asks no questions)".

## Goal

In the user's terms: "pour controller comment lancer les evals meme en remote", and for the
operator: "trouve la solution pour que ca marche". From the phone, under Remote Control, the user
starts a sandbox campaign's operator, Foreman campaigns (`real-foreman`, `full`) included. The
operator runs in the workspace and holds none of chantier's own instructions. The evals README and
both Foreman runbooks say how, to the result of a real trial on this machine.

## The facts this change starts from

These were proved 2026-11-20 on Battlestation (sibling `01-intent.md`). The hosts card already
records them in its "Move a started session to another folder" row
(`skills/chantier/references/hosts/claude-code.md` line 50) and in its rule "starting a session
from Remote Control".

- From a session driven by Remote Control, `start_session` with a `cwd` (the eval root) or a
  `preset` is refused. With neither, the session starts in the steering session's own folder.
- The started session moved itself into `C:\Users\gaeta\Projets\chantier-eval` with
  `mcp__ccd_directory__change_directory`. No question was asked (trusted tree, auto mode), and its
  next turn ran there.
- After the move, the session still held chantier's `AGENTS.md`, because a move does not reload
  project instructions. An eval forbids that.
- The Chief of Staff's `clear_session` of that session was denied by the auto mode classifier.

The steering session in the trial is chantier's own Chief of Staff, in
`C:\Users\gaeta\Projets\chantier` with the surface added. An operator started there with no `cwd`
lands in chantier's main checkout. During an eval the main checkout does not change (`AGENTS.md`),
so the bootstrap writes nothing before its move.

## Decisions carried

From `02-answers.md` of the sibling (answers 2, 3 and 4) and the critic's findings 2, 4 and 6 on its
first specification, as `intake/request.md` carries them.

1. **The route (answer 2, finding 2).** The steering session (the user's Chief of Staff, driven
   from the phone) starts the operator with `start_session`: no `cwd`, no `preset`,
   `use_worktree: false`, the user's permission mode. Its prompt is a short **bootstrap prompt**,
   not setup's `prompt` line. The bootstrap prompt:
   - moves the session into the workspace with `change_directory`;
   - takes the isolation step (decision 2);
   - loads no skill, runs no chantier command and writes nothing before the move.

   When that turn ends, the steering session sends the **check message** (decision 3). Once the
   check passes, it sends setup's `prompt` line verbatim, by message (`send_message`, as the hosts
   card names it). `evals/kit/setup.py` does not change. A bootstrap prompt that began with
   `/chantier:chief-of-staff` would run the boot skill in the steering folder before the move, where
   the live Chief of Staff holds the seat, so the operator would become a Griller. A self-clear
   would also wipe such a prompt. That is why the slash line comes by message, after the move.
2. **Isolation: three trials, in this order (answer 2).** Each is recorded proved or not proved. The
   first one proved becomes the route the README documents, and the later ones are not tried.
   - **(a) The self-clear.** The operator's bootstrap prompt ends with `clear_session` on `self`,
     after the move. The trial checks what its context holds afterwards (decision 3).
   - **(b) The phone's New session.** If (a) is not proved, the user starts the operator from the
     phone's own New session, on the workspace folder. The Chief of Staff gives the user the folder
     (setup's `workspace` line), the check message and the `prompt` line. The user pastes the
     check message first, and the `prompt` line only once the check passes. There is no move and
     no clear. The check
     also covers the session's checkout (`git rev-parse`), because a session created from the
     remote client landed in a worktree on 2026-11-10 (hosts card, "A Chief of Staff and Grillers
     in remote").
   - **(c) A neutral steering folder.** If (b) is not proved, the steering session itself runs in
     the eval root, which has no `AGENTS.md` and no `CLAUDE.md` (the trial checks this). A start with
     no `cwd` then lands outside chantier, and the operator moves into the workspace as in (a), with
     no clear. Settled by the Chief of Staff (2026-11-20, the user asks no questions):
     - That steering session is a plain Claude Desktop session on the eval root. The user opens it
       at the desk before leaving and connects it to Remote Control. It is not a chantier session.
     - Under (c), the operator holds no project instructions after its move. It reads the
       workspace's rules with `$CHANTIER rules`, as `chief-of-staff.md` already has it do. The
       Foreman and the Drivers start fresh in the workspace and load its `AGENTS.md` themselves.

   No route depends on the Chief of Staff clearing or stopping another session. No route asks
   another session to do what was denied.
3. **The check, with observable evidence.** The isolation check never trusts the operator's word
   alone. Settled by the Chief of Staff (2026-11-20, the user asks no questions):
   - **The canary (trial only).** Before the trial, the Chief of Staff appends one line to the trial
     workspace's `AGENTS.md`: `Trial canary: <token>`. The token is drawn at that moment (for
     example 8 random hex characters) and written nowhere else, neither in this CR nor in a prompt.
   - **chantier's marker.** chantier's `AGENTS.md` first bullet, "Run `just check` before you hand
     back".
   - **The check message.** It asks the operator to do these things, in its next turn, without
     reading any file:
     - run `pwd`, `git rev-parse --git-dir`, `git rev-parse --git-common-dir` and
       `git rev-parse --show-toplevel`;
     - quote the canary line if its project instructions hold one, and say "no canary" if not;
     - say whether its instructions hold chantier's marker.
   - **Pass, (a) and (b):** `--git-dir` and `--git-common-dir` are the same folder, the top level is
     the workspace, the token quoted matches, the marker is absent, and the transcript shows no file
     read or shell output that could have given the token in that turn.
   - **Pass, (c):** the same, except that "no canary" is expected, since the operator loaded no
     project instructions.
   - **In every real run** the check message is sent too, before the `prompt` line: one message
     from the steering session under (a) and (c), or pasted by the user under (b).
     The sandbox's own `AGENTS.md` line "shelf is a small reading list served on the web" stands in
     for the canary under (a) and (b). A Fail stops the run before the `prompt` line, and the
     report records it.
4. **Foreman campaigns from the phone (answer 3).** Once in the workspace and started by the
   `prompt` line, the operator starts the Foreman with no `cwd`, as the hosts card's rule says. The
   Foreman then lands on the workspace's main checkout. The README and the `full` and
   `real-foreman` runbooks stop requiring the desk, but only to the trial's result (decision 6).
5. **The trial, before the PR is ready (answer 4).** It runs for real on this machine, from Remote
   Control, and covers: the start with no `cwd`, the move, the isolation check, the `prompt` line by
   message, and where a session started by the moved operator lands. A Driver has no session tools,
   so the Chief of Staff runs the trial with the user driving from the phone, at the Driver's
   request:
   - The Driver opens a **draft PR** and writes the trial file with every step **pending**.
   - It asks the steering session to run the trial, with the draft PR's link and the trial file's
     path. Under a Foreman, the Foreman relays the request to the Chief of Staff.
   - The Chief of Staff and the user run the trial, and the Chief of Staff fills the file in.
   - The Driver is **resumed** with the result and writes the lines of decision 6.
6. **Claims after the proof (finding 4).** These lines say what a moved operator, or a session it
   starts, does. The Driver writes them only after the trial's last step, to its result:
   - the README's "Prerequisites" (lines 29-36);
   - the README's "Starting the Foreman" bullet in "The host's limits" (lines 261-267);
   - the "Start" section of both runbooks;
   - the hosts card's row for where a session started by a moved session lands.

   If a step is not proved, these lines say what was seen and keep what is true today (a Foreman
   campaign at the desk), with the trial's date. Before the trial, the draft PR holds only the
   bootstrap route marked "unproved until the trial of `<trial file>` reports".
7. **The trust premise (finding 6).** The README's setup step (lines 104-109) currently says that
   "a workspace inside the trusted root does not ask for trust (unproved), so the operator's session
   can start from Remote Control". It is rewritten to the route found:
   - the move into a workspace inside the trusted eval root asks nothing (proved 2026-11-20);
   - a start on that folder from the phone's own New session stays unproved unless trial (b) ran.

   The hosts card's "Trust of a workspace inside a trusted folder" row (line 49) says the same, and
   its trial becomes this CR's trial instead of "the first `real-direct` run after the eval root
   change".

## The trial

Settled by the Chief of Staff (2026-11-20, the user asks no questions):

- **The trial workspace.** It is a workspace made by setup for a Foreman campaign:
  `uv run --no-project python evals/kit/setup.py real-foreman <eval root>/trial-phone-<date>`,
  after `sandbox.py reset --yes` if the sandbox is not at its base. That costs no model and pushes
  nothing. The only extra is the canary line, appended to that workspace's `AGENTS.md` and never
  pushed. Below it, still in the same file, the Chief of Staff appends one more line:

  > This workspace is a trial. When chantier's chief-of-staff skill starts here, run `preflight`,
  > report its first lines and the planning folder you use, and stop: open no batch.

  The skill's later start of the probe session (step 7) is the steering session's explicit
  request, which this line does not forbid. After the trial, the workspace and its
  `<workspace>.run.json` are deleted, and no run number is used, because no PR was opened.
- **The steps, in order.** Each step is recorded in the trial file with the tool call, its output
  (or a screenshot from the phone, when the output is only on the phone) and **proved** or **not
  proved**.
  1. The user, on the phone, drives the steering session under Remote Control (the Remote Control
     notice is seen in its turn).
  2. The steering session starts the operator with no `cwd` and the bootstrap prompt (route (a)).
     The trial records where it landed.
  3. The operator moves into the trial workspace (`change_directory`) and calls `clear_session` on
     `self`. The trial records whether the self-clear was granted, refused or denied.
  4. The steering session sends the check message (decision 3). The trial records the answer and the
     Pass or Fail. On Fail, or if step 3 was refused, (a) is not proved: the trial goes to (b), then
     to (c), each run from step 2 with its own check, until one passes or all three are recorded
     not proved.
  5. The steering session sends setup's `prompt` line verbatim, by message.
  6. The trial checks that the operator's next turn ran the chief-of-staff skill **in the
     workspace**. Its `preflight` lines name the workspace's `.agents/changes`, it holds the
     workspace's seat (not a Griller's), and it stops as the canary file asks. A message that does
     not run the skill is recorded not proved. The route then falls to (b), where the user pastes
     the line in the session's own field.
  7. The steering session asks the operator to start one **probe session** with no `cwd` and this
     prompt: "Run `pwd`, `git rev-parse --git-dir`, `git rev-parse --git-common-dir` and
     `git rev-parse --show-toplevel`; quote the canary line of your project instructions, or say
     none; say whether they hold the line 'Run `just check` before you hand back'; read no file;
     then stop." The probe stands in for the Foreman: it is started by `start_session` with no
     `cwd`, the same call as the Foreman's, from a turn that another session's message started.
     The trial records whether the start was granted, and the probe's answer. This is the trial's
     last step.
  8. The Chief of Staff archives the operator's and the probe's sessions through the user, if the
     host does not let it do so itself, and deletes the trial workspace.
- **The trial file.** `work/trial-phone.md` in this CR's folder. The Driver writes it with the steps
  above pending. The Chief of Staff fills it in and keeps out the canary's token, writing only
  "matched" or "did not match". The PR body quotes its results.

## What changes

### 1. `evals/README.md`

- **"Prerequisites"**, the eval root bullet (lines 29-36): the trust sentence follows decision 7.
  The last sentence, "A Foreman campaign ... still needs the desk ... only the campaigns with no
  Foreman ... start from the phone", is rewritten after the trial (decision 6).
- **The steps paragraph** (lines 40-43): "start the operator with the `prompt` line setup printed"
  gains "(from the phone: through the steering session, see 'The operator')".
- **Setup step 4** (lines 104-109): its trust clause follows decision 7.
- **"The operator"** (lines 126-151):
  - **Kept:** the two desk routes, New session and a chantier session at the desk.
  - **Replaced:** the "away from the desk" route and its trial (lines 134-144, "the first
    `real-direct` run after this change"). In their place goes **from the phone, through a
    steering session**, the route the trial proved:
    - the exact bootstrap prompt, with `<workspace>` to fill in from setup's `workspace` line;
    - the check message and its Pass rule (decision 3, the sandbox's `AGENTS.md` line standing in
      for the canary);
    - the `prompt` line sent verbatim by message once the check passes;
    - the steering session's message cost: the check and the `prompt` line, two messages under the
      10-message limit.
  - **Recorded:** the routes tried and not proved, each in one line with the trial's date. A
    route not reached is named unproved.
  - **Removed:** the sentence "A Foreman campaign is started at the desk" (line 139), if the trial
    proved the Foreman's landing (decision 6).
- **"The host's limits", "Starting the Foreman"** (lines 261-267): it still says a session "started
  or driven under Remote Control cannot start another session". That is no longer true (the hosts
  card's rule since `4ed0d56c`). The bullet is rewritten after the trial (decision 6): the moved
  operator starts the Foreman with no `cwd`, in the workspace, with the probe's result quoted, or
  else what was seen.

### 2. `evals/full/RUNBOOK.md` and `evals/real-foreman/RUNBOOK.md`, "Start"

Both are written after the trial (decision 6):

- "In a new Code session ... (not under Remote Control)" becomes "at the desk, or from the phone as
  the evals README's 'The operator' says".
- "This campaign needs the desk, to start the Foreman and type the go" goes, or stays with the
  trial's date if the probe's start was not proved.
- The trust clause, "(**unproved** until the trial reports)", follows decision 7.
- `real-foreman`'s line 44, "the go typed in the desktop app", is aligned the same way.

### 3. `evals/real-direct/RUNBOOK.md` and `evals/ticket-summary/RUNBOOK.md`

Each has one trust clause, "(**unproved** until the trial reports)" (lines 30 and 23), that points
at the trial this CR replaces. It follows decision 7, and "see the evals README, 'The operator'"
stays. Settled by the Chief of Staff (2026-11-20, the user asks no questions): the request names
only the two Foreman runbooks, but leaving these two clauses would point at a trial that no longer
exists.

### 4. `skills/chantier/references/hosts/claude-code.md`

- **Row "Trust of a workspace inside a trusted folder"** (line 49): decision 7. The move asks
  nothing (proved 2026-11-20). The trial becomes this CR's (`work/trial-phone.md`), and the row is
  marked by its result for the New session start if (b) ran.
- **Row "Move a started session to another folder"** (line 50): its three "not recorded" items get
  the trial's results:
  - the self-clear (`clear_session` on `self`): granted or not, and what the context holds
    afterwards;
  - the operator's route: the bootstrap prompt, the check, and the `prompt` line by message, with
    a pointer to the evals README's "The operator";
  - where a session started by a moved session lands: the probe's answer. This item is written
    after the last step (decision 6).

  The Driver may split the row in two (the move, and a session started by a moved one) if one row
  grows too long.
- **Nothing else** in the card changes. The rule "starting a session from Remote Control" and the
  classes table stay as merged. No card outside `hosts/` names a host tool: the test
  `test_each_host_has_its_reference_and_the_cards_hold_no_host_tool`
  (`skills/chantier/scripts/cli/tests/test_plugin_files.py`) keeps it so. The evals README is not a
  card and may name tools, as it already names `mcp__ccd_pr__set_monitor`.

### 5. The trial file

`work/trial-phone.md` in this CR's folder, as "The trial" says.

## Out of scope

- `evals/kit/` and `setup.py`: unchanged (finding 2). The `prompt` line stays a slash line.
- The cards outside `hosts/claude-code.md`, the CLI, `hooks/`, `types/`, the agents files and
  Copilot (`hosts/copilot.md` and the `copilot` runbook).
- A full campaign run: the first eval run from the phone proves the campaigns end to end (sibling
  answer 4). This CR's trial stops at the probe.
- Any route that uses the Chief of Staff's clear or stop of another session.
- `2-backlog/P3/evals-rework`, which edits the same README sections and renames the runbooks. This
  CR does not wait for it. After this CR merges, the Chief of Staff re-reads evals-rework before it
  is taken. That is not the Driver's work.
- Release notes and versions.

## Host matrix

| Cell | Before | After |
| --- | --- | --- |
| Claude Desktop at the desk, operator from New session or from a chantier session | documented, worked 2026-11-15 | unchanged |
| Claude Desktop under Remote Control, campaign with no Foreman | phone's New session route, unproved | the bootstrap route through the steering session, to the trial's result; the New session route as (b) recorded |
| Claude Desktop under Remote Control, Foreman campaign (`real-foreman`, `full`) | desk required | the moved operator starts the Foreman with no `cwd`, if the probe step is proved; else desk required, with the trial's date |
| Steering session in chantier's main checkout (surface added) | operator would hold chantier's `AGENTS.md` | isolated by (a), or not used (b, c) |
| Steering session in the eval root, (c) only | not described | described if (c) is the route proved |
| Copilot | per its runbook | unchanged |

## Evidence

- **The trial file**, filled in, with each step proved or not proved, quoted in the PR body. The PR
  leaves draft only once the file has no pending step and the lines of decision 6 match it.
- **A search of the shipped files**, run with `grep -rnF "<pattern>" evals skills --include=*.md`
  on the repository's files as they ship, at the base and at the PR's head, with the command and
  its output in the PR. At the base (`4ed0d56c`, 2026-11-20):

  | Pattern | Matches at the base | At the head |
  | --- | --- | --- |
  | `until the trial reports` | `evals/README.md:108,138`, `evals/full/RUNBOOK.md:42`, `evals/real-foreman/RUNBOOK.md:39`, `evals/real-direct/RUNBOOK.md:30`, `evals/ticket-summary/RUNBOOK.md:23` | none |
  | ``the first `real-direct` run after`` | `evals/README.md:140`, `skills/chantier/references/hosts/claude-code.md:49` | none |
  | `cannot start another session` | `evals/README.md:264` | none |
  | `needs the desk` | `evals/README.md:35,265`, `evals/full/RUNBOOK.md:40`, `evals/real-foreman/RUNBOOK.md:37` | none if the probe step is proved; otherwise only with the trial's date beside it |
  | `Not recorded here: the operator's route` | `skills/chantier/references/hosts/claude-code.md:50` | none |

  The "(not under Remote / Control)" clause of both runbooks wraps at lines 26-27 and needs a
  reading check, named in the PR.
- **`just check`**, green in the worktree at the rebased head. No new test: the change is prose and
  a trial record, and the project's tests check structure and the CLI's refusals. The existing
  host-tool test reads the shipped cards.

## Gates (the project's `AGENTS.md`)

- **`just check`** before the hand-back, run by the Driver in the worktree at the rebased head it
  pushes, before the first push.
- **The long gate is owed.** This CR changes a card (`skills/chantier/references/hosts/claude-code.md`),
  so the pipeline's `just scenario (ubuntu-latest)` job must be green at the PR's head before the PR
  is ready. Without the hosts card, the change would be docs alone (`evals/` README and runbooks
  are docs, not the eval kit) and would owe none.
- **Windows coverage:** if this CR is on top of its batch's stack, it also passes `just scenario`
  locally (`chantier gate`) at its head before the user merges. When a CR joins on top, the local
  run moves to that CR.
- **Not owed:** `just eval-dry-run`, because nothing changes under `evals/kit/` or the CLI's
  `src/`; and `just mod`, because nothing changes under `hooks/` or `types/`.
- **The trial** (decision 5) holds the PR in draft until it reports. It is not a gate of
  `AGENTS.md` but this CR's own condition.

## Open questions

None. The user asks no more questions. Each point the answers left open is settled above and
marked "Settled by the Chief of Staff (2026-11-20, the user asks no questions)".
