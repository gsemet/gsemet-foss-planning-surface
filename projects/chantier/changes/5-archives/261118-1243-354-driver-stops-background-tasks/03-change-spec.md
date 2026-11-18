# Change Specification: a CR Driver starts in its worktree, background tasks stop when done

## Goal

A background task (a background shell or a host monitor) that outlives its purpose costs twice.
First, it wakes its owner each time it reports. In batch-24, an ended Driver's leftover tasks woke
the Foreman 75 times, and the Driver re-sent its hand-back. Second, on Windows a process whose
current folder is inside a folder keeps that folder from being moved or removed (WinError 32).

Two such folders were locked:

- **A CR Driver's shells.** The plugin's mod starts an agent in the first folder of its `writes:`
  line (`hooks/register.tsx`, the `agent.spawn` hook; `concepts.md`, "Starting an agent"). A CR
  Driver's line starts with its CR folder, so every shell of a CR Driver runs inside the CR folder
  of the planning surface.
- **The Foreman's own loop.** It ran `bash -c "until grep -qE ... <task>.output; do sleep 5; done;
  tail -5 ..."` with its current folder in the CR-330 folder. The loop locked that folder and
  delayed the record of CR-330's merge from 20:29 to 21:25.

After this change:

- On Claude Code, a CR Driver starts in its CR's worktree. While that worktree does not exist yet,
  it starts in the project's root: the main checkout, or the project's clone with a planning
  surface. It never starts in the CR folder. It reads its CR by the absolute paths its prompt
  names, and its write guard keeps the same folders (retro-Q3).
- No shell call of a Driver or of the steering session changes its folder into a CR folder. The
  steering session's never changes it into a worktree either.
- A Driver stops each background task it started once its result is read or no longer counts.
  Before any `$CHANTIER handback`, it stops every one still running, except the shell that runs a
  long gate. That shell is left to finish, and the CLI records the result (retro-Q4).
- The steering session (the Foreman, or the Chief of Staff in direct mode) starts no background
  task to wait. It stops any of its own that runs, and it stops an ended Driver that wakes again
  after its recorded hand-back.

The decisions are those of `02-answers.md`. retro-Q3 and retro-Q4 are the user's. The other
decisions were settled by the Chief of Staff: bg-Q1 to bg-Q10, bg-Q8 confirmed, bg-Q3 and bg-Q4
as revised, retro-Q3's start folder, and bg-Q6 refined.

## What changes

The change covers the plugin's mod (`hooks/register.tsx`, `hooks/register.test.tsx`), the cards,
the two host references, the frontmatter of the four Claude Code Driver agents, `CONTRIBUTING.md`
and `docs/boards.md`. The CLI does not change: the `writes:` lines stay as `take` prints them, and
no new command, rail or `status` line is added (bg-Q10). `types/` does not change, because the
hook uses `$.fs.exists`, which the mod already calls.

A card may not name a host tool:
`test_each_host_has_its_reference_and_the_cards_hold_no_host_tool` refuses `TaskStop` in
`concepts.md`, `driver.md` and `foreman.md`. So the cards say "the host's stop of a background
task" and "Stop a Driver", and only `hosts/claude-code.md` names `TaskStop` (bg-Q7).

### 1. The mod: where an agent starts (retro-Q3)

`hooks/register.tsx`, the `agent.spawn` hook (today lines 625-656): when `writesOf(e.prompt)`
found folders and the spawn is not a resume, choose the start folder as follows. Today's code
takes `found.folders[0]`.

1. Read the prompt's first `worktree:` line, with a new helper beside `writesOf` (for example
   `worktreeOf(prompt)`). It matches `/^\s*worktree:\s+(.+?)\s+branch\s/m`, which is the form
   `take` and `handoff` print (`worktree: <path> branch <branch> …`, one of the copied fact lines
   of a CR Driver's prompt). The path must be absolute; otherwise there is no `worktree:` line.
2. With no `worktree:` line, start in the first `writes:` folder, as today. A worker's prompt
   takes this case, since its first folder is its worktree.
3. With a `worktree:` line whose folder exists (`await $.fs.exists(path)`), start in it.
4. With a `worktree:` line whose folder does not exist yet, start in the project's root that the
   prompt's first line names. Read it with a helper such as `rootOf(prompt)`: on the prompt's
   first line, take the last match of `/, in the project (.+)\.\s*$/`. That is every chantier
   first line, for example `chantier cr-driver for <cr> "<title>" of batch <batch>, in the project
   <root>.`. `<root>` is the main checkout in-project, or the project's clone with a planning
   surface (`Repo.root`). Use it when it is absolute and exists.
5. If neither folder is usable, the agent starts with the spawn's own `cwd` unchanged (its
   parent's folder). It is still guarded by its `writes:` folders, and the board gets the note
   `Write guard: the worktree <path> does not exist and the project's root could not be read; the
   agent started guarded, in its parent's folder.`

The recorded `Worker` keeps `folders: found.folders` unchanged. Its `cwd` becomes the start folder
chosen (in case 5, the spawn's `cwd` when that is a string, else the first `writes:` folder), so a
relative path is judged against the folder the agent really runs in. A resume stays untouched, as
today. The rest of the guard does not change.

`hooks/register.test.tsx`: add tests next to "the spawn reaches the engine in the first folder…"
(they use `guardWorld` and `spawn`, and make the worktree folder exist with the mock world's
`put`, as the other tests make files exist):

- A CR Driver prompt `chantier cr-driver for CR-5 "T" of batch b, in the project ${ROOT}.` holding
  `worktree: ${WT} branch chantier/b/cr-5 …` and `writes: ${FOLDER}`, with `WT` existing: the
  engine gets `cwd` `WT`. A Write to `${FOLDER}/work/a.md` passes. A relative Write `a.md` is
  refused, because it is read against `WT`, which is outside the folders.
- The same prompt with `WT` absent: the engine gets `cwd` `ROOT`.
- The same prompt with `WT` absent and a first line without `, in the project …`: the spawn's
  `cwd` is unchanged, a Write outside `${FOLDER}` is still refused, and the board's note holds
  `started guarded, in its parent's folder`.
- A worker prompt (`WORKER_PROMPT`) with a `worktree:` line added keeps starting in `WT`.

The existing tests keep passing unchanged. `DRIVER_PROMPT` holds no `worktree:` line, so it still
starts in `FOLDER`.

### 2. Where the mod is described (retro-Q3)

- `skills/chantier/references/hosts/claude-code.md`, "The write guard", the sentence "A spawn whose
  prompt holds the line starts in the first folder (the mod rewrites the spawn's `cwd`, except on a
  resume)". Replace it with: "A spawn whose prompt holds the line starts in the first folder,
  except a spawn whose prompt also holds a `worktree:` line (a CR Driver's). That one starts in
  that worktree, or, while the worktree does not exist yet, in the project's root its first line
  names (the main checkout, or the project's clone with a planning surface). With neither, it
  starts in its parent's folder, still guarded, with the board's note. The mod rewrites the
  spawn's `cwd`, except on a resume." Then, under "Tools", one row after "Stop a Driver": `| A CR
  Driver's start folder | the mod's, as "The write guard" says | unproved; trial: the first CR
  Driver of the batch after the merge runs `pwd` (or `Get-Location`) and gets its worktree, or the
  main checkout or the clone on a first take |`.
- `skills/chantier/references/concepts.md`, "Starting an agent", the paragraph "On Claude Code the
  plugin starts an agent whose prompt holds the `writes:` line in its first folder …": after "in
  its first folder", insert "(a CR Driver, whose prompt also holds `worktree:`, in that worktree,
  or in the project's root while the worktree does not exist yet: never in its CR folder)".
- `CONTRIBUTING.md`, the mod's item (the sentence "it starts an agent whose prompt holds a
  `writes:` line in its first folder"), and `docs/boards.md`, "The guard of a worker's and a CR
  Driver's writes" ("a CR Driver's: its CR folder"). Make both say: a CR Driver starts in its
  worktree, or in the project's root before the worktree exists.
- `skills/chantier/references/hosts/copilot.md`, "Tools": after the row "Stop a Driver", add `| A
  Driver's start folder | the host's; no mod moves it (unproved; trial: a Copilot CR Driver runs
  its first shell and records the folder) |`.

### 3. `concepts.md`, "Rules", rule 8 (bg-Q2, bg-Q3 revised, bg-Q9, the critic's fixes)

Rule 8 contains the sentence "No `sleep`, no polling loop: a wait is the forge's own watch, in a
background shell (except two bounded waits, … "Merging on GitHub")." Right after it, and before
"`git -C <worktree>` is accepted", insert:

> For a Driver and the steering session (the workers keep their cards' ground rules): a
> background task is a background shell or a host monitor (a tool that streams a command's output
> to its owner). A task that waits on a file or on another task's output (`until grep …; do sleep
> …; done`) is a polling loop. No shell call changes its folder (`cd`, `Set-Location`, `pushd`,
> alone or chained before a command) into a CR folder (any stage). The steering session's never
> changes it into a worktree either. A Driver's shells run from the folder it starts in (its
> worktree on Claude Code). Name the target instead: `git -C <worktree>`, absolute paths,
> `gh … --repo <owner>/<name>`, `glab … -R <owner>/<name>`. Whoever starts a background task
> stops it by its id, with the host's stop of a background task, once its result is read or no
> longer counts (the board keeps `session-start.md`'s start and stop rules; only the
> current-folder rule applies to it). The shell that runs `$CHANTIER gate` is the gate itself: it
> ends when the gate ends and records its result, and it is stopped only with `gate <cr> --stop`.
> The reasons: on Windows a process whose current folder is inside a folder keeps that folder from
> being moved or removed (WinError 32), so a CR's move between stages or a worktree's removal
> fails; and a task left running wakes its owner each time it reports. [driver](driver.md) and
> [foreman](foreman.md) say when each role stops its tasks.

### 4. `driver.md` (bg-Q1, bg-Q4 revised, retro-Q3, retro-Q4)

a. "Your means": add a new bullet right after the bullet that begins "Every git command a Driver
runs names its worktree" (it ends "never cleaned by force.") and before "The worktree is your
first step":

> - Your folder and your background tasks ([concepts](concepts.md), rule 8). On Claude Code a CR
>   Driver starts in its worktree, or, before the worktree exists, in the project's root (the main
>   checkout, or the project's clone); never in its CR folder. Read and write the CR folder's files
>   by the absolute paths your prompt names (`folder:`, `specification:`): a relative path lands
>   where you run. Change no shell's folder into a CR folder, and name targets (`git -C <worktree>`,
>   absolute paths, `gh … --repo`, `glab … -R`). Keep the id of each background task you start (the
>   long gate's shell, the CI watch, a host monitor). Stop each one by that id, with the host's stop
>   of a background task (your host's reference, "Tools"), as soon as its result is read or no
>   longer counts. Before every `$CHANTIER handback`, ready or blocked, whatever the reason
>   (`context:` and `waits: push` included), stop every one still running, except the shell that
>   runs `$CHANTIER gate`. A long gate still running is left to finish: the CLI records its result
>   for the next Driver. Stop only what waits on it or reads it besides that shell. When that
>   gate's end wakes you after your hand-back, send nothing and end your turn. A task left running
>   wakes you after your hand-back, and a re-sent hand-back wakes the steering session for nothing.

b. "Your means", the bullet "Your end comes in this order: first `$CHANTIER handback <cr> …`":
change its opening to "Your end comes in this order: first your background tasks stopped (the
"Your folder and your background tasks" bullet above), then `$CHANTIER handback <cr> …`; once the
CLI accepted it, the host's hand-back …". Leave the rest of the bullet unchanged.

c. "Your means", the `stop` sentence ("`stop`: stop a long gate of yours that is running
(`gate <cr> --stop`), then `handback blocked stopped`"): after "(`gate <cr> --stop`)", add "and
every other background task of yours". The steering session's `stop` still stops the gate: retro-Q4
is about the Driver's own hand-back.

d. "Release driver: the end": just before the last item (`$CHANTIER handback <cr> ready <release
link or tag>`), add the item `- [ ] Every background task of yours stopped (a deploy watch
included), as "Your means", "Your folder and your background tasks", says.`

The existing CI rule "The gate fails first: … Stop the CI watch's shell you started, by its id"
stays as it is.

### 5. `foreman.md` (bg-Q1, bg-Q5, bg-Q6 refined, the critic's fix)

a. "A lost Driver", the sub-bullet "**A Driver waiting on its own background work** has not
ended.": after "has not ended", insert "while its CR is `working` (a hand-back already recorded:
"An ended Driver that wakes again")".

b. Right after that sub-bullet, add:

> - **An ended Driver that wakes again.** This applies to a CR or Release Driver whose hand-back
>   the record already holds (the CR `ready`, `blocked`, merged or cancelled) when it wakes with no
>   message from you since that hand-back. The signs: its hand-back line comes a second time;
>   another line from it answers nothing you sent; or the host's notice says it is waiting on its
>   own background work while `status` shows no `gate running` and no `gate queued` for that CR.
>   With a gate running, leave it alone: that shell is its long gate, and it ends on its own. A
>   background task it left running woke it. Do not act on the line again, since the record holds
>   the hand-back. Stop that Driver by the host's means (your host's reference, "Stop a Driver"),
>   then `$CHANTIER note <cr> "stopped: leftover background work after its hand-back"`, then
>   `agents set <cr> - --epoch <n>`, in the same turn, as "Keeping its own stops apart" asks for
>   your own stops. It is not a restart and not a silent end, and it counts toward nothing. A
>   Driver still recorded on a `blocked` CR that answers your note (a `waits:` that landed, a
>   `question:` answered to it) is not concerned: that is the note's answer.

c. "A CR taken back from `ready`", the sub-bullet "Note the Driver's agent id first …": add at its
end "When no id is recorded (the Driver was stopped after its hand-back, "An ended Driver that
wakes again"), `take <cr> --note "resume: <the take's note>" --epoch <n>` and start a new CR Driver
from the skeleton it prints, then `agents set <cr> <id> --epoch <n>`; the resume steps below do not
apply."

d. "End the heartbeat, never your session …": before "When you end it, record the stop first",
add "Before you end it, no background task of yours is left running ([concepts](concepts.md),
rule 8): stop each by its id."

e. The closing paragraph "How you start, message and stop a Driver … Keep each turn short: never
wait inside a call, never run a long command;": after "never run a long command;", insert "start
no background task of your own to wait for anything (a file, a task's output, a Driver, CI). A
Driver's line, the host's notice about a Driver, an order and the heartbeat wake you. Stop a task
of yours found running at once, by its id, with the host's stop of a background task; change no
shell's folder into a CR folder or a worktree;". The Chief of Staff in direct mode reads this card,
so this holds for it too.

### 6. Host rows for the stop (bg-Q7, bg-Q8)

`hosts/claude-code.md`, "Tools": after the row "Stop a Driver" (and the start-folder row of
section 2), add:

- `| Stop a background task of one's own (a shell, a monitor) | `TaskStop` with the id its start
  returned (`Bash` or `PowerShell` with `run_in_background: true`, or `Monitor`); the Driver agents
  list `TaskStop` in their tools for it | unproved; trial: a CR Driver of the first batch after the
  merge stops its CI watch when its gate fails first, or a task before its hand-back, and its
  transcript shows the `TaskStop` call and no notification from that task after it |`
- `| Stop an ended Driver that wakes again (`foreman.md`, "An ended Driver that wakes again") |
  `TaskStop` with the Driver's agent id, as "Stop a Driver" | the stop: proved, same as "Stop a
  Driver"; whether it also ends the background tasks that Driver left running: unproved; trial: the
  next such stop, then no task notification from that Driver's tasks in the steering transcript |`

`hosts/copilot.md`, "Tools": after the row "Stop a Driver", add `| Stop a background task of one's
own | the host's stop of a background shell, within the agent's `execute` tool set (unproved;
trial: a Copilot CR Driver stops its CI watch before its hand-back and the host's events show no
output from it afterwards) |`.

### 7. The Claude Code Driver agents' tools (bg-Q8, confirmed)

In `agents/cr-driver.md`, `agents/stack-driver.md`, `agents/qa-driver.md` and
`agents/release-driver.md`, add `TaskStop` at the end of the frontmatter's `tools:` line, after
`Monitor`. Nothing else changes: the bodies stay identical to their Copilot counterparts, which do
not change.

### File edits (checklist for the Coder)

- `hooks/register.tsx`: the `agent.spawn` start folder and the two read helpers (section 1).
- `hooks/register.test.tsx`: four tests (section 1).
- `skills/chantier/references/hosts/claude-code.md`: "The write guard" sentence; three rows in
  "Tools" (sections 2 and 6).
- `skills/chantier/references/hosts/copilot.md`: two rows in "Tools" (sections 2 and 6).
- `skills/chantier/references/concepts.md`: the "Starting an agent" paragraph (section 2); rule 8's
  passage (section 3).
- `skills/chantier/references/driver.md`: 4a to 4d.
- `skills/chantier/references/foreman.md`: 5a to 5e.
- `CONTRIBUTING.md` and `docs/boards.md`: the start folder's wording (section 2).
- `agents/cr-driver.md`, `agents/stack-driver.md`, `agents/qa-driver.md`,
  `agents/release-driver.md`: `TaskStop` on `tools:` (section 7).

No `## Startup core` section changes.

## Out of scope

- The CLI: the `writes:` lines, `take`'s facts, the gate, and any new command, rail or `status`
  line. The gate stays one foreground CLI process. A detached gate that would let the Driver stop
  its own shell is not built.
- What the CR board pane draws: the mod's pane code is untouched.
- The workers' cards: they already run no background shell.
- The board's start and stop.
- Removing `Monitor` from the Driver agents' tools, and the Copilot agent files.
- A Driver's start folder on Copilot: unproved, named in Known gaps.
- Any other CR folder.

## Evidence and gates

Required by AGENTS.md:

- **`just check`** in the worktree, at the rebased head the Driver pushes, before the first push. It
  includes `test_each_host_has_its_reference_and_the_cards_hold_no_host_tool`.
- **`just mod`** (`claude plugin validate .` then `claude plugin test .`), because `hooks/`
  changes. It runs `hooks/register.test.tsx` with the new tests, and the agent runs it itself. An
  agent that cannot run it stops and says so, with no workaround.
- **The long gate:** the pipeline's `just scenario (ubuntu-latest)` job green at the PR's head,
  because the cards change. Windows coverage: if this CR is on top of the batch's stack, it also
  passes `just scenario` locally (`chantier gate`) at its head before the user merges.
- **Not owed:**
  - `just eval-dry-run`: nothing changes under `skills/chantier/scripts/cli/src/` or `evals/kit/`.
  - A pane screenshot: what the CR board pane draws does not change.

The Verifier checks at the pushed head:

- `rg -n "TaskStop" skills/chantier/references` matches only `hosts/claude-code.md`.
- Each of the four `agents/*-driver.md` has `TaskStop` on its `tools:` line, and the bodies are
  unchanged.
- The `just mod` output shows the four new hook tests passing.
- Each passage of sections 2 to 5 is present at its place, with the words above.

The PR's Known gaps names the trials of the new host rows, which stay unproved until a real batch.
They cover the start folder on Claude Code and on Copilot, `TaskStop` by a Driver, and whether
stopping an ended Driver ends its leftover tasks.

## Open questions

None for the user. One reading for the Chief of Staff to confirm: retro-Q4 assumes a shell that
only waits on the gate. Today the shell running `$CHANTIER gate` is the gate itself: stopping it
ends the CLI process before it records anything. So the spec leaves that shell running at a
hand-back and stops every other task (bg-Q4 revised). The ended Driver then wakes once at the
gate's end, sends nothing and ends, and the Foreman leaves it alone while `gate running` shows.
