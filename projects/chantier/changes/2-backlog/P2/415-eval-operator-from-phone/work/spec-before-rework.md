# Start an eval's operator, and its Foreman campaigns, from the phone

Change Specification, written 2026-11-20 from `intake/request.md`. Revised the same day with the
user's rule on host isolation and the spec critic's nine findings, as the Chief of Staff settled
them (decisions 0 and 8).

The grill and the trials are in the sibling CR this one was split from,
`4-batch/3-done/414-remote-control-start-session/` (its `01-intent.md`, `02-answers.md` and
`03-change-spec.md`, "part B"). That sibling is merged on chantier's `main` (`4ed0d56c`), and this
specification reads the files as they are at that commit. No issue.

The user asks no more questions. Where the answers are silent, the point is settled here and marked
"Settled by the Chief of Staff (2026-11-20, the user asks no questions)".

## Goal

In the user's terms: "pour controller comment lancer les evals meme en remote", and for the
operator: "trouve la solution pour que ca marche". The user starts a sandbox campaign's operator
from the phone, Foreman campaigns (`real-foreman`, `full`) included. The operator runs in the
workspace, and its context holds only the workspace's instructions. The evals README and the
runbooks state that requirement in host-neutral terms. The Claude Code host card says how Claude
Code meets it from Remote Control, to the result of a real trial on this machine.

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

In the trial, the steering session is chantier's own Chief of Staff, in
`C:\Users\gaeta\Projets\chantier` with the surface added. An operator started there with no `cwd`
lands in chantier's main checkout. During an eval the main checkout does not change (`AGENTS.md`),
so the bootstrap writes nothing before its move.

## Decisions carried

0. **Host isolation, the user's rule (2026-11-20).** The user, verbatim: "tu fais bien attention
   d'isoler ce qui est propre a claude code et son mode remote". Settled by the Chief of Staff
   (2026-11-20, the user asks no questions):
   - **The hosts card.** Every Claude Code and Remote Control specific goes in
     `skills/chantier/references/hosts/claude-code.md` only, in one new section, **"The eval
     operator from a remote client"**. The title avoids the words "Remote Control" so that the
     README's pointer to it passes the search of the Evidence section. This covers:
     - tool names (`start_session`, `change_directory`, `clear_session`, `SendMessage`,
       `mcp__ccd_*`) and `cwd`;
     - the steering folder, the bootstrap prompt, the move and the self-clear;
     - the phone's New session entries, the probe, and typing into a started session from the
       phone;
     - what loads at a session's start (`AGENTS.md`, auto-memory, `.claude/settings*.json`).
   - **The evals docs.** `evals/README.md` and every runbook this CR touches stay host-neutral.
     - Their new text names no Claude Code tool and no Remote Control mechanism.
     - They say what the operator needs: a session started in the workspace, whose context holds
       only the workspace's instructions.
     - They point to the host's card as "Claude Code: hosts/claude-code.md, 'The eval operator
       from a remote client'". Copilot keeps its own line.
     - Existing text outside this CR's scope stays as it is.
   - **The other cards.** No generic card gains Claude Code specifics.
   - **The trial file.** `work/trial-phone.md` may name the exact tools: it is evidence of a run on
     Claude Code.
1. **The route (answer 2, finding 2).** This route is Claude Code's and is written only in the
   hosts card's new section.
   - **The start.** The steering session (the user's Chief of Staff, driven from the phone) starts
     the operator with `start_session`: no `cwd`, no `preset`, `use_worktree: false`, the user's
     permission mode.
   - **The bootstrap prompt.** The operator's first prompt is a short bootstrap prompt, not setup's
     `prompt` line. It:
     - moves the session into the workspace with `change_directory`;
     - takes the isolation step (decision 2);
     - loads no skill, runs no chantier command and writes nothing before the move.
   - **The messages.** When that turn ends, the steering session sends the **check message**
     (decision 3). Once the check passes, it sends setup's `prompt` line **verbatim, with the mode
     blank filled**, by message. The tool is named as the card's row "Message another session of
     the user" names it (`SendMessage` to the session's id).
   - **Why the slash line comes by message.** A bootstrap prompt that began with
     `/chantier:chief-of-staff` would run the boot skill in the steering folder before the move.
     There, the live Chief of Staff holds the seat, so the operator would become a Griller. A
     self-clear would also wipe such a prompt. So the slash line comes by message, after the move,
     and `evals/kit/setup.py` does not change.
2. **Isolation: three trials, in this order (answer 2).** Each is recorded proved or not proved. The
   first one proved becomes the route the hosts card documents, and the later ones are not tried.
   - **(a) The self-clear.** The operator's bootstrap prompt ends with `clear_session` on `self`,
     after the move. The trial checks what its context holds afterwards (decision 3).
   - **(b) The phone's New session.** If (a) is not proved, the user starts the operator from the
     remote client's own New session on the workspace folder. The user follows the hosts card's
     two tries ("The trial that settles a new Foreman from a remote client", lines 643-646):
     - first the "Remote Control" entry;
     - in a second try, the "Local" group's entry or a saved environment with Worktree off.

     In each try the check runs with `git rev-parse`, because a session created from the remote
     client landed in a worktree on 2026-11-10. The Chief of Staff gives the user the folder
     (setup's `workspace` line), the check message and the `prompt` line. The user pastes the
     check message first, and the `prompt` line only once the check passes. There is no move and no
     clear.
   - **(c) A neutral steering folder.** If (b) is not proved, the steering session itself runs in
     the eval root, which has no `AGENTS.md` and no `CLAUDE.md` (the trial checks this). A start
     with no `cwd` then lands outside chantier, and the operator moves into the workspace as in
     (a), with no clear. Settled by the Chief of Staff (2026-11-20, the user asks no questions):
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
     - list the path of every instruction and memory file its context shows (finding 1);
     - quote the canary line if its project instructions hold one, or say "no canary";
     - say whether its instructions hold chantier's marker.
   - **Pass, (a) and (b).** All of these must hold:
     - `--git-dir` and `--git-common-dir` are the same folder, and the top level is the workspace;
     - the token quoted matches;
     - the marker is absent;
     - no listed instruction or memory file belongs to chantier's checkout or its auto-memory;
     - the transcript shows no file read, and no shell output that could have given the token, in
       that turn.
   - **Pass, (c).** The same, except that "no canary" is expected, since the operator loaded no
     project instructions.
   - **The settings (trial only, finding 1).** The trial also records whether a command that only
     the workspace's `.claude/settings.local.json` allows runs with no prompt, as decision 8 says.
   - **In every real run.** The check is sent too, before the `prompt` line: by the steering session
     under (a) and (c), or pasted by the user under (b).
     - The sandbox's own `AGENTS.md` line "shelf is a small reading list served on the web" stands
       in for the canary under (a) and (b).
     - That line alone does not prove isolation: it proves that the workspace's instructions
       loaded, not that no other instructions did. Isolation rests on the marker's absence, the
       list of files, and the rule that no file was read in that turn.
     - A Fail stops the run before the `prompt` line, and the report records it.
4. **Foreman campaigns from the phone (answer 3).** Once in the workspace and started by the
   `prompt` line, the operator starts the Foreman with no `cwd`, as the hosts card's rule says. The
   Foreman then lands on the workspace's main checkout. The README and the `full` and
   `real-foreman` runbooks stop requiring the desk, but only to the trial's result (decision 6),
   and in host-neutral words (decision 0).
5. **The trial, before the PR is ready (answer 4).** It runs for real on this machine, from Remote
   Control. It covers:
   - the start with no `cwd`, the move and the isolation check;
   - the `prompt` line by message;
   - where a session started by the moved operator lands;
   - whether the user can type into that session from the phone.

   A Driver has no session tools, so the Chief of Staff runs the trial with the user driving from
   the phone, at the Driver's request:
   - The Driver opens a **draft PR** and writes the trial file with every step **pending**.
   - It asks the steering session to run the trial, with the draft PR's link and the trial file's
     path. Under a Foreman, the Foreman relays the request to the Chief of Staff.
   - The Chief of Staff and the user run the trial, and the Chief of Staff fills the file in.
   - The Driver is **resumed** with the result and writes the lines of decision 6.
6. **Claims after the proof (finding 4, critic finding 4 of this revision).** These lines say what a
   moved operator, or a session it starts, does, or where the user must be. The Driver writes them
   only after the trial's last step, to its result:
   - the README's "Prerequisites" (lines 29-36);
   - the README's "The operator" opening, line 127 ("at the desk for a Foreman campaign: it starts
     the Foreman's sessions");
   - the README's "Starting the Foreman" bullet in "The host's limits" (lines 261-267);
   - the "Start" section of both Foreman runbooks, with `real-foreman` line 44 ("the go typed in
     the desktop app") and the `ping` lines (`full` lines 126-129, `real-foreman` lines 74-76);
   - the hosts card's new section, for where a session started by a moved session lands and
     whether the user can type into it from the phone.

   If a step is not proved, these lines say what was seen and keep what is true today (a Foreman
   campaign at the desk), with the trial's date. Before the trial, the draft PR holds only the
   route in the hosts card, marked "unproved until the trial of `work/trial-phone.md` reports".
7. **The trust premise (finding 6).** The README's setup step (lines 104-109) currently says that
   "a workspace inside the trusted root does not ask for trust (unproved), so the operator's session
   can start from Remote Control". It is rewritten in host-neutral words: a workspace inside the
   trusted eval root asks for no new trust, as the host's card records for the route found
   ("Claude Code: hosts/claude-code.md, 'The eval operator from a remote client'"). The hosts card
   carries the Claude Code facts:
   - the move into a workspace inside the trusted eval root asks nothing (proved 2026-11-20);
   - a start on that folder from the phone's own New session stays unproved unless trial (b) ran.

   The hosts card's "Trust of a workspace inside a trusted folder" row (line 49) says the same, and
   its trial becomes this CR's trial instead of "the first `real-direct` run after the eval root
   change".
8. **The spec critic's nine findings on this specification.** Settled by the Chief of Staff
   (2026-11-20, the user asks no questions):
   1. **What loads at start.** The check message also asks for the path of every instruction and
      memory file the operator's context shows (decision 3). The trial also records whether a
      command allowed only by the workspace's `.claude/settings.local.json` runs with no prompt
      ("The trial", step 4). The result goes in the hosts card's new section. The README states only
      the host-neutral requirement.
   2. **Typing into the Foreman's session.** A step follows the probe's start: the user finds the
      probe session on the phone and types one line in it, recorded proved or not proved ("The
      trial", step 8). The `ping` lines and "typed in the desktop app" follow the result
      (decision 6). The runbooks stay host-neutral: "where the user can type into the Foreman's
      session; Claude Code: hosts card".
   3. **The message tool.** It is named as the card's row "Message another session of the user"
      names it (`SendMessage`). The trial file records the exact tool used.
   4. **README line 127** is in decision 6's list, and its pattern is in the search.
   5. **The search** uses the pattern `until the trial`, with its matches at the base listed.
   6. **Trial (b)'s result in the card.** When trial (b) has run, both passages of the hosts card
      carry its result, with the date: "The trial that settles a new Foreman from a remote client"
      (lines 641-646) and the "For you" block "A new Foreman, from a remote client" (lines 745-750).
   7. **(b) follows the card's two tries** (lines 643-646). Its step 2 becomes the user's start
      from the phone.
   8. **The `prompt` line** is sent "verbatim, with the mode blank filled". The trial file names the
      mode used.
   9. **The Pass rule in the README.** The README states that the Pass rule rests on the rule that
      no file was read in that turn, and that the sandbox line alone does not prove isolation. It
      stays host-neutral.

## The trial

Settled by the Chief of Staff (2026-11-20, the user asks no questions).

### The trial workspace

It is a workspace made by setup for a Foreman campaign:
`uv run --no-project python evals/kit/setup.py real-foreman <eval root>/trial-phone-<date>`, after
`sandbox.py reset --yes` if the sandbox is not at its base. That costs no model and pushes nothing.

The Chief of Staff adds two things to it, both local and never pushed:

- **In the workspace's `AGENTS.md`:** the canary line, and below it this line:

  > This workspace is a trial. When chantier's chief-of-staff skill starts here, run `preflight`,
  > report its first lines and the planning folder you use, and stop: open no batch.

  The skill's later start of the probe session (step 7) is the steering session's explicit
  request, which this line does not forbid.
- **In the workspace's `.claude/settings.local.json`** (which setup writes): one allow rule for a
  harmless command that no other settings file of the user allows. For example,
  `Bash(git rev-parse --is-bare-repository)`. The Chief of Staff checks first that neither
  `~/.claude/settings.json` nor the steering folder's `.claude/settings*.json` allows it.

After the trial, the workspace and its `<workspace>.run.json` are deleted. No run number is used,
because no PR was opened.

### The steps, in order

Each step is recorded in the trial file with:

- the exact tool call and its output, or a screenshot from the phone when the output is only on
  the phone;
- **proved** or **not proved**.

1. The user, on the phone, drives the steering session under Remote Control. The Remote Control
   notice is seen in its turn.
2. The steering session starts the operator with no `cwd` and the bootstrap prompt (route (a)). The
   trial records where it landed. Under route (b), this step is the user's start from the phone, in
   the hosts card's two tries (decision 2).
3. The operator moves into the trial workspace (`change_directory`) and calls `clear_session` on
   `self`. The trial records whether the self-clear was granted, refused or denied.
4. The steering session sends the check message (decision 3), with the exact tool it used. The trial
   records:
   - the answer, the list of instruction and memory files, and the Pass or Fail;
   - whether the settings command of "The trial workspace" ran with no prompt, and the session's
     permission mode. Under auto mode, a run with no prompt is recorded "not conclusive", since auto
     mode alone may allow it.

   On Fail, or if step 3 was refused, (a) is not proved. The trial then goes to (b), then to (c),
   each run from step 2 with its own check, until one passes or all three are recorded not proved.
5. The steering session sends setup's `prompt` line verbatim, with the mode blank filled, by message.
   The trial file names the mode.
6. The trial checks that the operator's next turn ran the chief-of-staff skill **in the
   workspace**:
   - its `preflight` lines name the workspace's `.agents/changes`;
   - it holds the workspace's seat, not a Griller's;
   - it stops as the trial line of the workspace's `AGENTS.md` asks.

   A message that does not run the skill is recorded not proved. The route then falls to (b), where
   the user pastes the line into the session's own field.
7. The steering session asks the operator to start one **probe session** with no `cwd` and this
   prompt:

   > Run `pwd`, `git rev-parse --git-dir`, `git rev-parse --git-common-dir` and
   > `git rev-parse --show-toplevel`; list the instruction and memory files your context shows;
   > quote the canary line of your project instructions, or say none; say whether they hold the line
   > 'Run `just check` before you hand back'; read no file; then stop.

   The probe stands in for the Foreman: it is started by `start_session` with no `cwd`, the same
   call as the Foreman's, from a turn that another session's message started. The trial records
   whether the start was granted, and the probe's answer.
8. The user finds the probe session on the phone and types one line in it (for example `ping`).
   The trial records whether the session was found, whether the line was taken and whether the
   probe answered, proved or not proved. This is the trial's last step.
9. The Chief of Staff archives the operator's and the probe's sessions, through the user if the host
   does not let it do so itself, and deletes the trial workspace.

### The trial file

`work/trial-phone.md` in this CR's folder. The Driver writes it with the steps above pending. The
Chief of Staff fills it in. It names the exact tools and the mode used, and keeps out the canary's
token, writing only "matched" or "did not match". The PR body quotes its results.

## What changes

### 1. `skills/chantier/references/hosts/claude-code.md`

- **A new section, "The eval operator from a remote client".** It holds every Claude Code and Remote
  Control specific of this CR, to the trial's results:
  - the steering folder and the start (`start_session`, no `cwd`, no `preset`,
    `use_worktree: false`);
  - the exact bootstrap prompt, with `<workspace>` to fill in from setup's `workspace` line;
  - the move (`change_directory`) and the isolation route proved: (a) the self-clear, (b) the
    phone's New session entry that worked, or (c) the neutral steering folder;
  - the routes tried and not proved, each in one line with the trial's date. A route not reached is
    named unproved;
  - the check message as sent, and setup's `prompt` line sent by `SendMessage`, verbatim, with the
    mode blank filled;
  - the steering session's message cost: the check and the `prompt` line, two messages under the
    10-message limit (under (b) the user pastes both, and the steering session sends none);
  - what loads at a session's start or after the self-clear: `AGENTS.md`, the auto-memory and
    `.claude/settings*.json`, from steps 4 and 7;
  - where a session started by the moved operator lands (step 7), and whether the user can type
    into it from the phone (step 8). These items are written after the last step (decision 6);
  - a pointer to the evals README's "The operator" for the host-neutral check and its Pass rule.
- **Row "Trust of a workspace inside a trusted folder"** (line 49): decision 7. The move asks
  nothing (proved 2026-11-20). The trial becomes this CR's (`work/trial-phone.md`), and the row is
  marked by its result for the New session start if (b) ran.
- **Row "Move a started session to another folder"** (line 50): its "Not recorded here: the
  operator's route, the self-clear, and where a session started by a moved session lands" becomes a
  pointer to the new section, which records all three.
- **When trial (b) has run** (finding 6): "The trial that settles a new Foreman from a remote
  client" (lines 641-646) and the "For you" block "A new Foreman, from a remote client"
  (lines 745-750) carry its result, with the date. When (b) was not reached, both stay as they are.
- **Nothing else** in the card changes. The rule "starting a session from Remote Control" and the
  classes table stay as merged.

### 2. `evals/README.md`

All new text here is host-neutral (decision 0). It names no Claude Code tool and no Remote Control
mechanism, and it points to "Claude Code: hosts/claude-code.md, 'The eval operator from a remote
client'". Copilot keeps its own line.

- **"Prerequisites"**, the eval root bullet (lines 29-36):
  - The trust sentence follows decision 7.
  - The last sentence, "A Foreman campaign ... still needs the desk ... only the campaigns with no
    Foreman ... start from the phone", is rewritten after the trial (decision 6).
- **The steps paragraph** (lines 40-43): "start the operator with the `prompt` line setup printed"
  gains "(away from the desk: see 'The operator')".
- **Setup step 4** (lines 104-109): its trust clause follows decision 7.
- **"The operator"** (lines 126-151):
  - **Rewritten after the trial:** line 127's "at the desk for a Foreman campaign: it starts the
    Foreman's sessions" (decision 6).
  - **Kept:** the two desk routes, New session and a chantier session at the desk. This is existing
    text outside this CR's scope.
  - **Replaced:** the "away from the desk" route and its trial (lines 134-144, "the first
    `real-direct` run after this change"). In their place go:
    - **The requirement:** the operator is a session started in the workspace, on its main
      checkout, whose context holds only the workspace's instructions: no other project's
      instructions, memory or settings.
    - **The check, before the `prompt` line, in every run.** In a turn where it reads no file, the
      operator gives:
      - its folder, with the three `git rev-parse` lines;
      - the instruction and memory files its context shows;
      - whether its instructions hold the sandbox's line "shelf is a small reading list served on
        the web", and chantier's line "Run `just check` before you hand back".
    - **The Pass rule** (finding 9):
      - `--git-dir` equals `--git-common-dir`, and the top level is the workspace;
      - the sandbox line is present and chantier's line is absent;
      - no listed file belongs to another project.

      The rule rests on the condition that no file was read in that turn. The sandbox line alone
      does not prove isolation: it shows that the workspace's instructions loaded, not that no
      others did. A Fail stops the run before the `prompt` line.
    - **How to start it away from the desk, per host:** "Claude Code: hosts/claude-code.md, 'The
      eval operator from a remote client'". Copilot: unproved, as its line says today.
  - **Removed:** the sentence "A Foreman campaign is started at the desk" (line 139), if the trial
    proved the Foreman's start (decision 6).
- **"The host's limits", "Starting the Foreman"** (lines 261-267): it still says a session "started
  or driven under Remote Control cannot start another session". That is no longer true (the hosts
  card's rule since `4ed0d56c`). It is rewritten after the trial (decision 6), in host-neutral words:
  - where the operator, away from the desk, starts the Foreman;
  - where the user can type into the Foreman's session;
  - each with the pointer "Claude Code: hosts card".

  Or else what was seen, with the trial's date.

### 3. `evals/full/RUNBOOK.md` and `evals/real-foreman/RUNBOOK.md`

Both are written after the trial (decision 6), in host-neutral words:

- **"Start":**
  - "In a new Code session ... (not under Remote Control)" becomes "at the desk, or away from the
    desk as the evals README's 'The operator' says".
  - "This campaign needs the desk, to start the Foreman and type the go" goes, or stays with the
    trial's date if the probe's start was not proved.
  - The trust clause "(**unproved** until the trial reports)" follows decision 7.
- **`real-foreman` line 44**, "the go typed in the desktop app": follows step 8's result.
- **The `ping` lines** (`full` lines 126-129, `real-foreman` lines 74-76) read "the user types `ping`
  in the Foreman's session, where the user can type into it (Claude Code: hosts card)". This
  follows step 8's result.

### 4. `evals/real-direct/RUNBOOK.md` and `evals/ticket-summary/RUNBOOK.md`

Each has one trust clause, "(**unproved** until the trial reports)" (lines 30 and 23), that points
at the trial this CR replaces. It follows decision 7, in host-neutral words. The next line, "from
the phone, under Remote Control: see the evals README, 'The operator'", is existing text outside
this CR's scope and stays.

Settled by the Chief of Staff (2026-11-20, the user asks no questions): the request names only the
two Foreman runbooks, but leaving these two clauses would point at a trial that no longer exists.

### 5. The trial file

`work/trial-phone.md` in this CR's folder, as "The trial" says.

## Out of scope

- `evals/kit/` and `setup.py`: unchanged (finding 2). The `prompt` line stays a slash line.
- The cards outside `hosts/claude-code.md`, the CLI, `hooks/`, `types/`, the agents files and
  Copilot (`hosts/copilot.md` and the `copilot` runbook).
- Existing text of the evals docs outside the lines named above, including tool names it already
  holds (`mcp__ccd_pr__set_monitor`).
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
| Claude Desktop under Remote Control, campaign with no Foreman | phone's New session route in the README, unproved | the route proved by the trial, in the hosts card's new section; the README points there |
| Claude Desktop under Remote Control, Foreman campaign (`real-foreman`, `full`) | desk required | the moved operator starts the Foreman with no `cwd`, if step 7 is proved; `ping` from the phone if step 8 is proved; else desk required, with the trial's date |
| Steering session in chantier's main checkout (surface added) | operator would hold chantier's `AGENTS.md` and auto-memory | isolated by (a), or not used (b, c) |
| Steering session in the eval root, (c) only | not described | described in the hosts card if (c) is the route proved |
| Copilot | per its runbook | unchanged; the README keeps its own line |

## Evidence

- **The trial file**, filled in, with each step proved or not proved, quoted in the PR body. The PR
  leaves draft only once the file has no pending step and the lines of decision 6 match it.
- **A search for stale wording**, run with `grep -rnF "<pattern>" evals skills --include=*.md` on the
  repository's files as they ship, at the base and at the PR's head, with the command and its output
  in the PR. At the base (`4ed0d56c`, 2026-11-20):

  | Pattern | Matches at the base | At the head |
  | --- | --- | --- |
  | `until the trial` | `evals/README.md:34,108,135,138`, `evals/full/RUNBOOK.md:42`, `evals/real-foreman/RUNBOOK.md:39`, `evals/real-direct/RUNBOOK.md:30`, `evals/ticket-summary/RUNBOOK.md:23` | none, except "until the trial of `work/trial-phone.md` reports" in the hosts card while the PR is a draft |
  | ``the first `real-direct` run after`` | `evals/README.md:140`, `skills/chantier/references/hosts/claude-code.md:49` | none |
  | `cannot start another session` | `evals/README.md:264` | none |
  | `needs the desk` | `evals/README.md:35,265`, `evals/full/RUNBOOK.md:40`, `evals/real-foreman/RUNBOOK.md:37` | none if step 7 is proved; otherwise only with the trial's date beside it |
  | `desk for a Foreman campaign` | `evals/README.md:127` | none if step 7 is proved; otherwise only with the trial's date beside it |
  | `Not recorded here: the operator's route` | `skills/chantier/references/hosts/claude-code.md:50` | none |

  Two clauses wrap across lines and need a reading check, named in the PR: "(not under Remote /
  Control)" in both Foreman runbooks (lines 26-27), and "typed in the desktop app" in
  `real-foreman` (line 44).
- **A search for host specifics in the evals docs** (decision 0). The lines this CR adds to
  `evals/README.md` and the four runbooks carry none of these patterns. Run it with
  `git diff 4ed0d56c..HEAD -- evals/README.md evals/full/RUNBOOK.md evals/real-foreman/RUNBOOK.md evals/real-direct/RUNBOOK.md evals/ticket-summary/RUNBOOK.md | grep '^+' | grep -F "<pattern>"`,
  which must print nothing, and put the command and its output in the PR. So the check is diffable,
  the matches at the base, from `grep -nF "<pattern>"` on the same five files, are:

  | Pattern | Matches at the base |
  | --- | --- |
  | `start_session` | none |
  | `change_directory` | none |
  | `clear_session` | none |
  | `Remote Control` | `evals/README.md:109,135,264,266`, `evals/real-direct/RUNBOOK.md:31`, `evals/ticket-summary/RUNBOOK.md:24` (both Foreman runbooks wrap it across lines 26-27) |
  | `cwd` | none |

  A line this CR rewrites counts as added, so the README's lines 109, 135 and 264-266 leave the
  patterns behind when they are rewritten.
- **`just check`**, green in the worktree at the rebased head. No new test: the change is prose and
  a trial record, and the project's tests check structure and the CLI's refusals. The existing test
  `test_each_host_has_its_reference_and_the_cards_hold_no_host_tool`
  (`skills/chantier/scripts/cli/tests/test_plugin_files.py`) reads the shipped cards and keeps host
  tools out of the generic ones.

## Gates (the project's `AGENTS.md`)

- **`just check`** before the hand-back, run by the Driver in the worktree at the rebased head it
  pushes, before the first push.
- **The long gate is owed.** This CR changes a card (`skills/chantier/references/hosts/claude-code.md`),
  so the pipeline's `just scenario (ubuntu-latest)` job must be green at the PR's head before the PR
  is ready. Without the hosts card, the change would be docs alone (the `evals/` README and runbooks
  are docs, not the eval kit) and would owe none.
- **Windows coverage:** if this CR is on top of its batch's stack, it also passes `just scenario`
  locally (`chantier gate`) at its head before the user merges. When a CR joins on top, the local
  run moves to that CR.
- **Not owed:** `just eval-dry-run`, because nothing changes under `evals/kit/` or the CLI's
  `src/`; and `just mod`, because nothing changes under `hooks/` or `types/`.
- **The trial** (decision 5) holds the PR in draft until it reports. It is not a gate of
  `AGENTS.md` but this CR's own condition.

## Open questions

None. The user asks no more questions. Each point the answers and the critic left open is settled
above and marked "Settled by the Chief of Staff (2026-11-20, the user asks no questions)".
