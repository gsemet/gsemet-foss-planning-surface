# Change Specification: a Driver stays a Driver

## Goal

In batch 15, CR Drivers did work that belongs to their workers, and paid for it in context.
CR-200's Driver ran low on context, patched `costs.py` itself through PowerShell and damaged a
docstring. CR-212's round-3 Driver ran `git reset --hard` in its worktree after a coder's attempt
went wrong. A stray `round` call spent a round of CR-211 before any work. The Drivers of CR-200
and CR-208 ran out of context and never handed back, and 8 Drivers were restarted on CRs that
already had one.

After this change a CR Driver:

- delegates the work;
- keeps large outputs in files and reads them in parts;
- sees its own context size and hands back `context:` before it runs out;
- cannot write a project file through the shell without the guard refusing it;
- never discards work in its worktree (a worker does that);
- cannot spend a round on which nothing happened.

The user ordered the four retro items merged into this one CR ("regroupe en moins de CR"). Each
item's fix is below, and none is dropped.

There is no `01-intent.md` and no `02-answers.md`: the grill is `intake/request.md` alone, and its
first line already chooses the fix for each item. Where the request offered a choice, that line's
choice is carried. Where a detail was still open and the user sees no difference, this
specification picks one and says why.

## What changes

### 1. `round` refuses a round on which nothing happened (CLI)

From `stray-round-call`. The request offered two fixes: `round` refuses, or the card says when to
call it. The request's first line picks the refusal. The card's wording is tightened too (area 5),
at no extra cost.

- **Files:** `skills/chantier/scripts/cli/src/chantier/commands.py` (`round_`) and
  `skills/chantier/scripts/cli/src/chantier/rails.py` (a new check beside `check_round`).
- **The rule:** `round <cr>` is refused with exit 2 (a precondition) when the CR already has a
  round **and** both of these hold:
  - no event of the CR other than a `round` was logged after its last `round` event. A `note`,
    `gate`, `verdict`, `ship`, `take`, `handback`, `agents` or order event counts. The round's own
    `--note` is part of the `round` event, so it does not count.
  - the worktree's content is the same as when that last round was counted: the same head, the
    same uncommitted changes and the same untracked files.
- **Never refused by this rule:** a CR with no round yet. A new Driver after a `take` is not
  refused either, because the `take` event counts.
- **Order of the checks:** the budget first, then the round limit (both exit 5, as today), then
  this rule. A Driver whose budget is spent still reads `budget:`.
- **What the record keeps:** the `round` event records the worktree's head and a fingerprint of
  its uncommitted and untracked content, so the next `round` can compare. The fingerprint uses
  read-only commands and file reads only. The CLI changes nothing in git, so it cannot use a
  command that writes objects such as `git stash create`. If the worktree does not exist when the
  round is counted, no fingerprint is recorded, and the next `round` judges by the events alone.
- **When refused:** the round count is unchanged and nothing is logged. The message, on one line:
  `<cr>: round <n> was counted and nothing happened since (no note, the worktree unchanged): start that round's coder; to read the facts, `handoff <cr>`; if a new round is really needed, note why first`.
- **Why the worktree counts:** the card says a `FIX-REQUIRED` needs no note. After a coder and a
  `FIX-REQUIRED` review, the coder's edits change the worktree, so the next round passes with no
  extra note.

### 2. Each CR Driver's context is measured (CLI)

From `driver-context-exhaustion`: "measure a Driver's context".

- **What `note <cr>` and `round <cr>` print:** one more line, `context: <n> tokens (agent <id>)`.
  `<n>` is the last call's prompt size (input, cache writes and cache reads) in the transcript of
  the agent recorded on the CR (`agents set`). The CLI already computes this as
  `costs.py` `last_context`. The CLI knows no role: it reports the recorded agent, which is the
  CR's Driver.
- **Where the transcript is:** `<steering transcript>/subagents/agent-<id>.jsonl`, found the way
  `costs.agent_records` finds it, across every steering transcript the batch records (the
  Foreman's, or in direct mode the Chief of Staff's).
- **Read only the file's end:** the last usage record, not the whole transcript, because this runs
  on every note.
- **When it cannot be measured:** no agent is recorded, the file is not found, or the host is
  Copilot. The line then reads `context: not measured (<why>)`. That is not an error, and both
  commands still succeed.
- **`note`'s output** stays within ten lines: `ok`, then the context line.
- **`cost --by cr`:** each CR's line adds its Drivers' peak context and their compaction count,
  e.g. `(… calls; Driver peak context 162,000 tokens, 1 compaction)`. The figures come from the
  `peak_context` and `compactions` already kept per row. The retro then reads the measure from
  the CLI, not from a guess. This is the request's "measure", shown where the user already reads
  cost by CR. `cost --summary` is unchanged.

### 3. A CR Driver's write guard, which covers the shell (hook)

From `driver-no-shell-writes`. The request asks for both: "the no-edit rule also covers shell
writes, and the write guard names it", and "its write guard covers the shell".

**The CR Driver gets a `writes:` line** in its prompt, written by its steering session from the
`take` facts:

- `writes: <CR folder>`;
- in external mode, when `take` prints `archive: in the PR at <path>`, the line is
  `writes: <CR folder>; <path>`.

The hook is unchanged on this point: the agent starts in the first folder, which is the CR
folder, and its Write, Edit and NotebookEdit outside the folders named are refused. So a CR
Driver can still write:

- its notes;
- `work/pr-body.md`;
- its large outputs under `work/` (area 4);
- the cleaned archive.

It can no longer write any other file in the worktree.

Why the CR folder comes first: it exists when the Driver starts, and the worktree does not yet.
The Driver already uses `git -C <worktree>` (rule 8 of concepts), so starting in the CR folder
changes nothing the user sees.

**The shell guard** goes in `hooks/register.tsx`, `tool.call`. For an agent recorded with a
`writes:` line, a Bash or PowerShell call is judged as follows.

It is a write when it holds one of these forms with a target path:

- a redirection `>` or `>>`;
- `tee`;
- `sed -i` or `perl -i`;
- `cp`, `mv`, `rm`, `touch`, `truncate`;
- `Set-Content`, `Add-Content`, `Out-File`, `Clear-Content`;
- `New-Item`, `Copy-Item`, `Move-Item`, `Remove-Item`, `Rename-Item`;
- `[IO.File]::Write*`.

It is not a write when:

- the target is a null device (`$null`, `/dev/null`, `NUL`), or it is `2>&1`;
- the command is `git`, `gh`, `glab` or `uv run --script …chantier.py`. These tools write by their
  nature: git moves the worktree, and the CLI writes the planning folder.

What the guard does:

- **Refuse** a write whose target, read against the agent's folder like a Write's relative path,
  is outside every folder named. The one message names the rule:
  `refused: a shell write to <path> is outside the folders this agent may write in (<folder>; <folder>); the shell follows the same rule as Write and Edit`.
- **Let the call pass, and say so in the board's note,** when a path cannot be judged: it holds a
  variable, `~`, a `cd`, `Set-Location` or `pushd` earlier in the call, or a form the guard cannot
  parse. This is the guard's existing rule: a guard at fault costs nothing.
- **Leave alone** what the guard cannot see, such as an interpreter's inline code
  (`python -c`, `node -e`) and a script's own writes. The card's rule covers those (area 5).

This guard is role-free. The hook knows no role, so it applies to every agent with a `writes:`
line, the workers included. A worker's shell writes inside its worktree and CR folder pass, as
its Write does. A worker's shell write elsewhere is refused, as its Write already is, and
`worker.md` already says "never retry by another means, a shell write included". This is
consistent with what workers are already told, so nothing the user sees changes for them.

**Not guarded, unchanged:**

- the steering sessions, the Release driver, the stack driver, the QA driver, the Spec-writer,
  the Griller and the Demo explorer;
- Copilot, where the line stays inert.

The Release driver runs the project's procedure in its worktree, version bump included, so a
CR-folder-only line would block it. The stack driver has no single CR folder. Both keep the card
rule alone (area 5).

**Proof:** `hooks/register.test.tsx` gets cases for:

- a refused `Set-Content` into the worktree from a Driver whose line names the CR folder;
- a refused `>` redirection;
- a passed `> <CR folder>/work/x.log`;
- a passed `git -C <worktree> commit`;
- a passed `2>$null`;
- a passed `$CHANTIER` call;
- a note, and the call passed, for `> $env:TEMP\x`;
- a worker writing into its worktree through `Set-Content`, passed.

`just mod` must pass (AGENTS.md: a change to `hooks/` passes `just mod` before its PR). If the
agent cannot run it, it stops and says so, with no workaround.

### 4. Large outputs stay in files (card)

From `driver-context-exhaustion`: "keep large outputs (gate logs, diffs) in files it reads in
part". This is card text in `skills/chantier/references/driver.md`, "Your means". The Driver never
takes a whole large output into its context:

- **A gate log:** read its result from `handoff` (the last five lines it already prints) or from
  the log's last lines, never the whole log.
- **A diff:** read `git diff --stat` or `--name-only`. The Inspector reads the diff itself.
- **A CI failure:** write its log into `<work folder>/ci-<run>.log`, for example
  `gh run view <run> --log-failed > <work folder>/ci-<run>.log` (a shell write inside the CR
  folder, which the guard allows), then read it with Grep or with Read's offset and limit, or give
  it to a `debugger`.
- **Anything over about 200 lines:** a file under `work/` first, then read in parts.

These logs are never sent to the forge, so rule 9's "never written by the shell" (text sent to
the forge) does not apply. They stay in the `work/` files the `.gitignore` already covers
(`work/gates/`, `*.log`).

### 5. The cards and docs

**`skills/chantier/references/driver.md`, "Your means":**

- `writes:` line: replace "your own prompt never holds the line" with: "a CR Driver's own prompt
  holds `writes: <CR folder>` (and `; <archive path>` when `take` prints one): you write your
  notes, `pr-body.md`, your large outputs and the archive, nothing else".
- `round`:
  - add that `round` also refuses (exit 2) a round on which nothing happened. Read the fact with
    `handoff`, start the round's coder, or note why a new round is needed.
  - say that it prints `context:`.
- Add a **Context** bullet:
  - after each `note` and `round`, read its `context:` line. At 150,000 tokens or more, record
    your state with `note`, then `handback <cr> blocked context: <where it stopped, what is next>`,
    before the host compacts or ends you.
  - why 150,000: three quarters of the 200,000 `autoCompactWindow` the plugin's Driver agents
    carry, which leaves room for the note and the hand-back. This is an internal threshold the
    user does not see, so it is set here.
  - `context: not measured`: go on, and keep to the large-output rules.
  - add the large-output rules of area 4.

**`driver.md`, "CR driver":**

- After "A CR Driver edits no code, card, doc or other project file itself, not even one line",
  add: "through the shell either (a redirection, `Set-Content`, `sed -i`, an interpreter's inline
  code): the guard refuses what it sees, and the rule holds for what it does not".
- **Your worktree's work is never discarded by you.** No `git reset --hard`, `git checkout --
  <path>`, `git restore`, `git clean`, and no deletion of a file in the worktree.
- `git rebase --abort` is allowed: it returns to the head before the rebase, and no work is lost.
- After a coder that failed:
  - A dirty worktree goes to a new `coder`, in the same round with no `$CHANTIER round`. Its brief
    names what the failed attempt left and what to do with it: keep it, fix it, or discard it back
    to the round's starting head. Discarding is then the coder's own git. It is a restart of a
    failing child (rule 3), and a round is one coder pass with its reviews, which this attempt
    never reached.
  - The coder is restarted at most once per round. A second failed coder in the same round is the
    next round (`$CHANTIER round`), whose brief carries both failures.
  - A worktree left dirty by a failed rebase goes to a `conflict-resolver`.
- Before round 1 and between rounds, the Driver's own reading of the code is an `investigator` or
  a `debugger`, not the Driver.

**`driver.md`, "Stack driver":** after "You edit no project file yourself", add "through the shell
either", with the same `git reset --hard` rule for the CRs' worktrees: a `conflict-resolver`, or
`git rebase --abort`. The Release driver's `git reset --hard <base>` at a new attempt is unchanged.

**`skills/chantier/references/foreman.md`**, the bullet on starting a Driver (around "To start a
Driver"): a CR Driver's prompt holds `writes: <the take's folder:>` (and `; <the take's archive
path>` when printed), as its own line. A stack, release or QA driver gets none.

**`skills/chantier/references/concepts.md`, "Starting an agent":**

- The template's `writes:` comment becomes: "a worker's prompt: worktree first; a CR Driver's: its
  CR folder, then the archive path when `take` prints one".
- The paragraph under it adds: "a Bash or PowerShell write it can see is judged the same way".

**`skills/chantier/references/hosts/claude-code.md`, "A worker's writes stay in its CR"**, renamed
to "The write guard":

- the CR Driver's line;
- the shell forms judged, the ones passed, the refusal text and the cannot-judge cases;
- "Not guarded" no longer lists the Drivers or "every shell write", only the roles above and the
  shell forms the guard cannot see.

**`skills/chantier/references/hosts/copilot.md`:** if it states that the Driver's prompt has no
`writes:` line, align it. The line stays inert there.

**Other files:**

- `docs/boards.md` ("The guard of a worker's writes") and `CONTRIBUTING.md` (lines ~100–102 and
  119) say the guard covers the CR Driver and the shell forms it sees.
- `scenario/README.md`: the new scenario steps (below).
- The agent files are unchanged: no role's body changes, so `agents/` and
  `com.github.copilot/agents/` stay identical. No version is edited by hand.

## Out of scope

- **The Foreman's restart policy** (`foreman.md`, "A hand-back `blocked context:`", silent ends),
  unchanged. The 8 restarts are a consequence of the Drivers running out of context, which this CR
  addresses. The next eval's retro measures them with `cost --by cr`.
- **A guard for the Release, stack and QA drivers.** They keep the card rule only.
- **An interpreter's inline code and scripts.** The guard does not see these writes, and the card
  rule covers them.
- **Copilot:** no guard, and no context measure (`not measured`).
- **Raising or setting `autoCompactWindow`:** no change to the agent files.
- **Any new CLI command.** Two outputs gain a line, `cost --by cr` gains figures, and `round`
  gains a refusal.

## Evidence

- **`just check`** passes on Linux, macOS and Windows.
- **`tests/test_structure.py`:** the existing round test (around lines 269–276, which calls
  `round` back to back up to the limit) adds a `note` between rounds. New checks:
  - a second `round` with nothing since is refused with exit 2, the count unchanged and no event
    logged;
  - after a `note`, `round` passes;
  - the first round is never refused.
- **`just mod`** passes, with the new `register.test.tsx` cases of area 3.
- **`just scenario`** passes on both forges (this CR changes the CLI and the cards). The
  scenario's `round` loops (`run_scenario.py` around lines 2566, 3011 and 3031) add a note or a
  worktree change between rounds. New steps:
  - a stray second `round` refused with exit 2, the round count unchanged and no `round` event,
    then passing after a `note`;
  - a `round` passing with no note when the scripted Driver's worktree changed since the last
    round;
  - `note` printing `context: not measured (no agent recorded)` before `agents set`, then, with
    `agents set` and a fake `subagents/agent-<id>.jsonl` beside the Foreman's transcript, printing
    `context: <n> tokens (agent <id>)`, with `<n>` the last record's input, cache writes and cache
    reads;
  - `cost --by cr` showing the Driver's peak context and compactions on the CR's line.
- **Unproved until the next real eval:**
  - that Drivers hand back `context:` before running out (the retro counts the Drivers that ended
    with no hand-back, and reads the peak context per CR from `cost --by cr`);
  - that the shell guard refuses a real Driver's shell edit in a live session.

  The PR says both as `UNVERIFIED`.

## Open questions

None. Every choice above either carries the request's first line or changes nothing the user sees.
