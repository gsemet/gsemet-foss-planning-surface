# Change Specification: the worker write guard, redesigned

Written 2026-11-11 from the second grill (`02-answers.md`, answers 12 to 17, with 6, 7 and 8).
It replaces the specification written after the first grill.

## Goal

The user, after batch-10 stopped: "Redesign cette protection". Then, on the first design:
"J'ai peur qu'on over design cette partie alors qu'il faut mettre en place de manière générale
un mécanisme le plus simple et efficace et extensible".

What happened (`intake/request.md`): CR-171's guard (`hooks/register.tsx`, on main at 1e99343)
refused every Write and Edit of every worker in batch-10, in its own worktree and CR folder too,
with an empty path in the message. Its tests never ran. The batch stopped at $2.47.

The redesign, in one paragraph: an agent whose prompt holds a `writes:` line is started in the
first folder that line names and may Write, Edit or NotebookEdit only inside the folders it
names. A guard that cannot judge lets the call pass and says so on the CR board. One recipe,
`just mod`, runs the mod's checks, and an agent runs it. The steering session looks at the main
checkout with `git status` before each report, which also covers the shell.

## The cause (checked on main 1e99343, against the engine's types 2.1.309)

- `hooks/register.tsx`, lines 390-391: the `tool.call` hook reads `(e as any).input.file_path`.
  A `tool.call` event carries the tool's arguments flat beside `tool` (`ToolCallInput =
  ToolCallEnvelope & AgentLoop & ToolRequestMeta`; `file_path` for Write and Edit,
  `notebook_path` for NotebookEdit; `agentId` from `AgentLoop`). `input` exists only on
  `tool.check` (`ToolCheckInput`). So the path read was `''`, judged outside, and refused.
- `hooks/register.test.tsx`, lines 704-705 and 733, 794-795: the tests call the hook with
  `{ tool, input: { file_path }, agentId }` through `as any`. They mirror the bug, and nobody
  ran them: `claude` is not on this machine's PATH and CI has no `claude` binary.
- The same hook keeps a list of roles (`WORKER_ROLES`) and parses the wording of two lines the
  CLI prints (`worktree: … branch …`, `folder: … (work/, evidence/)`): a new role or a changed
  line breaks it silently.

## What changes

Six pieces. Each says why it is needed.

### 1. The `writes:` line (answer 14)

Why: it is the whole contract between the cards and the hook. It replaces the role list and
the parsing of the CLI's lines, and it is the one place a later role or a stricter rule plugs in.

- Format, one line of the prompt, at the start of a line:
  `writes: <absolute folder>; <absolute folder>` (one folder or more, separated by `;`).
  The first folder is where the agent starts (piece 2).
- `skills/chantier/references/concepts.md`, "Starting an agent": the prompt template gains
  the line, after the lines copied from `take`, `round` or `handoff`:
  `writes: <worktree>; <CR folder>   (a worker's prompt only: where it may write, the worktree first)`
  and one sentence under the template: on Claude Code the plugin starts an agent whose prompt
  holds this line in its first folder and refuses its Write, Edit or NotebookEdit outside the
  folders named; a prompt without the line is not guarded; a role that needs other folders, or
  fewer, gets its own line from the card that starts it.
- `skills/chantier/references/driver.md`, "Your means", the "Children" bullet (lines 18-24):
  every worker's prompt holds `writes: <worktree>; <CR folder>`, the two paths as `take`,
  `round` or `handoff` printed them (`worktree:` and `folder:`), absolute. A Driver's own prompt
  never holds the line (commit 1e99343: a Driver is not guarded).
- `skills/chantier/references/worker.md`, the shared paragraph (lines 10-12): replace "on
  Claude Code a Write or Edit outside the worktree and the CR folder is refused by the plugin:
  the path is wrong, so fix it, never retry by another means, a shell write included" with: on
  Claude Code the plugin starts you in the worktree and refuses a Write or Edit outside the
  folders your prompt's `writes:` line names: the path is wrong, so fix it, never retry by
  another means, a shell write included.
- The CLI prints no `writes:` line and is not changed: a Driver copies `take`'s lines into its
  own prompt, so a line printed there would guard the Driver, and the CLI knows no role.
- Not guarded, as today: the main session, the Drivers, the Spec-writer, the Griller, the Demo
  explorer, any agent with no `writes:` line.

### 2. The hook (`hooks/register.tsx`, "the worker write guard", lines 349-400)

Why: it is the guard itself; today's is the bug.

Remove `WORKER_ROLES`, `workerPlace` and the two regular expressions. The hook knows no role
and no card wording; it reads one line.

**At `agent.spawn`:**

- Read the first line of `e.prompt` matching `writes:` at its start; split on `;`, trim, drop
  empty entries. No such line: `next(e)` untouched, nothing recorded.
- Every entry must be an absolute path (`/…` or `<drive>:/…`, either slash). Otherwise the line
  cannot be read: `next(e)` untouched, nothing recorded, a board note (below).
- **Start in the first folder (answer 12):** call `next({ ...e, cwd: <first folder> })`
  (`AgentSpawnInput.cwd`: "A rewrite is where the subagent runs"). Why: a worker that starts in
  the main checkout writes there by any relative path or shell command; started in its
  worktree, it does not, the shell included, with nothing to refuse. Not on a resume
  (`e.resume` set): the engine ignores a rewrite there, and the record made at the first start
  still holds.
- Once the spawn resolves with an `agentId`, record `{ folders, cwd }` under that id (`cwd`:
  the folder the agent runs in). A denied spawn records nothing, as today. The atom's shape
  changes: change its tag (`workers-1` to `workers-2`), as the file's own comment asks.

**At `tool.call`:**

- Not a recorded agent, or `e.tool` not `Write`, `Edit` or `NotebookEdit`: `next(e)` untouched.
  Bash and PowerShell are not guarded (piece 5 covers them).
- The path is `e.file_path` for Write and Edit, `e.notebook_path` for NotebookEdit: the
  documented flat shape and nothing else. No `e.input`, no `path`, no other key (AGENTS.md: no
  fallback). Narrow on `e.tool` with the engine's types where they allow it, instead of
  `(e as any)`, so a type-check sees a wrong field.
- A relative path is read against the recorded `cwd`; slashes and the drive's case as today
  (`slash`, `clean`, `fold`, `isInside`, unchanged).
- Inside one of the folders: `next(e)`. Outside: the one refusal (answer 17), word for word:
  `refused: <path> is outside the folders this agent may write in (<folder>; <folder>); write there`

**A guard that cannot judge (answer 13):** the call passes and the board says so. Why: the
batch-10 failure was a guard at fault stopping every worker; a guard at fault must cost nothing.

- The cases: a recorded agent's Write, Edit or NotebookEdit whose path field is missing, not a
  string or empty; a `writes:` line that cannot be read; anything the guard's own code throws,
  at either event.
- The call (or the spawn, with its `cwd` not rewritten) goes on exactly as asked, and
  `next` is called once: judge inside the `try`, call `next` outside it.
- The note goes in the board's existing note (`feed.note`, drawn in italics by the pane): one
  sentence naming the tool, the agent id and why, ending with "the call passed", for instance
  `Write guard: could not read the Write call of agent <id> (no file_path); the call passed.`
  The last note stands; no list, no new pane element.
- Removed: `refused: the write guard failed (…)`. There is no "the guard is at fault" marker and
  no second refusal message (answer 17).

Update the section's comments to say this.

### 3. The hook's tests (`hooks/register.test.tsx`, lines 692-798)

Why: they are the proof of the refusals (answer 6), and they mirrored the bug.

- The helpers call the engine with the real shape: `$.tool.call({ tool, file_path, agentId })`,
  `notebook_path` for NotebookEdit, `command` flat for Bash. `WORKER_PROMPT` holds a `writes:`
  line and no longer depends on the `worktree:` and `folder:` lines.
- Cases, each one test or folded with a neighbour:
  - A guarded agent writes inside each folder of its line (Write, Edit, NotebookEdit).
  - Outside is refused with the exact message, for the three tools.
  - Bash passes.
  - A Windows path in another drive case or with backslashes is judged the same.
  - The spawn reaches the engine with `cwd` equal to the first folder, and a relative path is
    read against it.
  - A prompt with no `writes:` line is not guarded and its `cwd` is not rewritten: the main
    session, each Driver's prompt, the Spec-writer's, the Griller's, a plain prompt, and a
    worker's prompt without the line.
  - A role the hook never heard of, with a `writes:` line, is guarded (no role list).
  - A denied spawn records nothing.
  - **The batch-10 regression:** a guarded agent's Write shaped `{ tool: 'Write', input: {
    file_path }, agentId }` (no flat path) passes, and the board shows the note.
  - An empty `file_path` passes with the note; a `writes:` line with a relative entry leaves
    the agent unguarded and unmoved, with the note; a guard that throws (a getter on the flat
    `file_path`) passes with the note.

### 4. `just mod` (answer 15)

Why: the tests existed and nobody could run them; one recipe an agent can run removes the
"not on the PATH" excuse.

- `justfile`: a recipe `mod` that runs `claude plugin validate .` then `claude plugin test .`
  from the repository's root and fails when either fails. It finds the binary itself: `claude`
  on the `PATH`, else the executable of the process `CLAUDE_PID` names (CONTRIBUTING.md, lines
  93-95; checked on this machine: `(Get-Process -Id $env:CLAUDE_PID).Path` gives the session's
  `claude.exe`, which knows `plugin validate` and `plugin test`). Neither: it exits non-zero
  with one line saying no `claude` binary was found. Portable (POSIX and Windows), no
  dependency: a short script under `scripts/` run as the other recipes are, or two
  OS-attributed recipes; the Coder's choice. `validate`'s two known warnings (the marketplace
  description, the missing icon) do not fail it.
- Not part of `just check`: CI has no `claude` binary.
- `AGENTS.md`, one line after the long gate's: a change to `hooks/` or `types/` passes
  `just mod` before its PR; the agent runs it itself, and one that cannot stops and says so,
  with no workaround.
- `CONTRIBUTING.md`, "Daily work": `just mod` joins the recipe list; the paragraph of lines
  93-101 names it as the way to run `validate` and `test` (the `tsc` lines stay).
- No card names `just mod`: it is this project's rule, which `$CHANTIER rules` gives every role.

### 5. The main checkout, looked at by the steering session (answer 16)

Why: the hook cannot see a shell write; `git status` sees every write, whoever made it, with
no hook. It replaces the Driver's before and after check of the first design.

- `skills/chantier/references/chief-of-staff.md`, where it builds its Progress and Completion
  reports: before each, in both modes, the Chief of Staff runs `git status --porcelain` on the
  main checkout (with a planning surface, the clone `take` names) and names every path outside
  the planning folder that it has not named yet. It reverts nothing and it holds no CR back:
  another Driver or the user may be its cause (answer 10, kept on this point). One place only
  (answer 20): the Foreman's card does not change.
- `skills/chantier/references/status-layout.md`, "Progress": when the steering session named
  a trace since the last report, the next report has one line with the paths, and **For you**
  asks what to do with them.
- No CLI command, no snapshot file, no Driver step.

### 6. The texts that describe the guard

Why: they state today's design.

- `skills/chantier/references/hosts/claude-code.md`, "A worker's writes stay in its CR" (lines
  272-286): rewrite to pieces 1 and 2 (the `writes:` line, the start folder, the three tools,
  the flat arguments, the one refusal, the pass with a board note, who is not guarded, the
  scratchpad sentence kept). The "Unproved" paragraph becomes answer 6: the refusals are proved
  by `hooks/register.test.tsx` through `just mod`; the passes are proved by the next real
  eval's normal use; **Unproved** until that eval reports; no refusal is planted.
- `README.md`, lines 236-237: the mod starts an agent whose prompt holds a `writes:` line in
  its first folder and refuses its Write, Edit or NotebookEdit outside the folders named; a
  shell write is not guarded: the steering session reports what changed in the main checkout.
- `CONTRIBUTING.md`, lines 51-52: the same, in the mod's description.
- `README.md`, the layout tree (about line 455, "and the guard of a worker's writes"): true
  again once this CR merges; check its wording matches (answer 24).
- `skills/chantier/references/inspector.md`: for a diff that touches `hooks/`, the Inspector
  checks that the CR's gate record holds `just mod` (answer 23), since CI does not run it.

### 7. The eval's audit (answer 21)

`evals/kit/audit.py`: one check, that each worker's prompt holds a `writes:` line. Why: a
Driver that forgets the line leaves its worker unguarded with no sign, and the audit is where
the next eval "shows by normal use" (answer 6). The `evals-redesign` CR, which extends the audit
to the real campaigns, builds on it.

### Not changed

- The CLI (`rails.py`, `commands.py`): nothing.
- `agents/` and `com.github.copilot/agents/`: their bodies do not name the guard (grep).
- `hosts/copilot.md`: no guard there; the `writes:` line is in the shared cards and is inert
  on Copilot.
- `types/index.d.ts`: the board's contract, untouched.
- The version: no bump; the release is its own CR and waits for this one (answer 7).
- A Driver writing in a refused worker's place (answers 3 and 17): no card gains it. Rule 7 of
  `concepts.md` already says a refusal is reported, never worked around.
- A refused round (answer 8): it stays counted; the steering session adds one with the
  existing order if the CR runs short.

## The trial of the start folder (answer 12)

The user: "Essai d'abord". The risk: the host may stop an agent started in the worktree from
writing its notes in the planning folder, which is in the main checkout.

- When: in the first round, once the Coder's hook holds the `cwd` rewrite.
- What must be seen, with a real agent under the worktree's hook, its prompt holding
  `writes: <worktree>; <CR folder>`:
  1. its shell's current folder is the worktree;
  2. a Write with a relative path lands in the worktree;
  3. a Write of a note under `<CR folder>/work/` succeeds;
  4. a Write at the main checkout's root is refused with the message of piece 2.
- How: the mod loads from the main checkout, so the Driver's own workers do not run the
  worktree's hook. The known means is a session of the session's own `claude` (found as
  `just mod` finds it) started from the main checkout with `--plugin-dir <worktree>`, whose
  prompt starts that one agent. The Driver keeps the command and its output in
  `<work folder>/gates/`.
- 1 to 4 seen: the piece stays.
- 3 fails because of the start folder: the CR ships without the rewrite (the hook leaves
  `e.cwd` alone and records `e.cwd`, else the session's folder, for relative paths; the cards
  and texts lose "starts you in the worktree"), and the hand-back says so.
- The trial cannot run: the same as a failure (answer 19): the CR ships without the rewrite,
  and the hand-back says so with what was seen.
- Step 4 (a real refusal in a real session) is required whatever happens to the rewrite
  (answer 22): a guard that passes what it cannot read must be seen refusing once before it
  ships. If step 4 cannot be seen, the Driver hands back `blocked`, not `ready`.

## How this CR runs

- P1, alone, before the eval is relaunched; v0.9.0 waits for its merge (answer 7).
- The long gate is `just scenario` (cards change) and `just mod` (the hook changes):
  `$CHANTIER gate <cr> "just scenario" "just mod"`. The Coder runs `just mod` and `just check`
  in its round. A `just mod` that finds no binary stops the round: `handback blocked`, no
  workaround, no asking the user to run it (answer 15 replaces answers 4, 5 and 11).
- It starts only once the broken guard is off main (answer 18): a first small PR removes the
  `tool.call` guard from `hooks/register.tsx` (and its tests), with nothing else, and the user
  merges it. This CR then puts the new guard back.

## Out of scope

- Guarding shell writes in the hook.
- Running the mod's tests in CI.
- A planted refusal in the next eval, and the eval itself (answer 6).
- A `writes:` line for any role but the workers a Driver starts (the Demo explorer, the
  Spec-writer, a stricter line for the Inspector): the mechanism allows it, this CR adds none.
- Points 2 and 3 of `1-inbox/cr-171-retro-fixes`. Its point 1 is here (piece 4); that item's
  text still says "by hand": the Chief of Staff updates it.
- The untracked empty files at the main checkout's root (`commands.py`, `state.py`,
  `concepts.md`).

## Evidence

- `just mod` green at the pushed head, its log in `work/gates/`: `validate`, and every case of
  piece 3.
- `just check` (Linux, macOS, Windows in CI) and `just scenario`.
- The trial's output (1 to 4), or the hand-back line saying the rewrite was left out.
- Before and after for the PR: before, batch-10's refusal (`refused:  is outside this CR's
  worktree …`, from the batch-10 record); after, the test run showing a flat Write passing
  inside, the refusal outside, and the old shape passing with the board note.
- The Inspector checks: no role list and no `worktree:` or `folder:` parsing left in the hook;
  no read of `e.input`; one refusal message, the same in the hook, its tests and
  `hosts/claude-code.md`; `writes:` spelled the same in the hook, `concepts.md`, `driver.md`
  and `worker.md`; `foreman.md`, `status-layout.md`, README.md and CONTRIBUTING.md say what
  the hook does.
- After merge, not this CR's proof: the relaunched `real` eval shows the workers' writes in
  their worktree and `work/` with no refusal (answer 6).

## The answers, carried

| Answer | Where |
| --- | --- |
| 6, proof by normal use, no planted refusal | piece 6, Evidence |
| 7, P1, the release waits | How this CR runs |
| 8, a refused round stays counted | Not changed |
| 12, start in the worktree, trial first | piece 2, The trial |
| 13, an unreadable call or a throw passes, note on the board | piece 2 |
| 14, the `writes:` line, no role list | pieces 1 and 2 |
| 15, `just mod`, run by the agent, else stop | piece 4, How this CR runs |
| 16, `git status` by the steering session before each report | piece 5 |
| 17, no Driver copy, no fault marker, one refusal message | piece 2, Not changed |
| 1 to 5, 9 to 11 | superseded; 9 has no object left (no guard-fault refusal); of 10, "reported only, never blocking" is kept in piece 5 |

## Open questions

None. The four the spec-writer raised were settled by the user on 2026-11-11 (`02-answers.md`,
answers 18 to 21): the broken guard comes off main first in its own small PR; a trial that cannot
run means shipping without the rewrite; the `git status` look is the Chief of Staff's, before
each of its reports; the audit check is kept.
