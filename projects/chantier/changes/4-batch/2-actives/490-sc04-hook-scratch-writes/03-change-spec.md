# SC04: Let the write guard pass scratch writes

Child 4 of 28 of the program CR `simplify-cards-and-prompts`. Its `03-change-spec.md`, "Child 4",
and its `02-answers.md` answers 3 and 17 to 22 rank above this file. One Driver and one PR, in the
running stack batch (batch-31). Code read: `origin/main` at `8a960d34`. The host read:
Claude Code 2.1.330, from the bundled code of its own binary (see "The host's hook API" below).

## Goal

The owner's rule (answer 3, simplify-cards-Q6): a refusal that more than 2 % of a role's runs hit
is a tool bug, not a card gap. Study-behaviour S5 counted 577 write-guard refusals. 490 of them were
scratch writes, which the host's own system prompt recommends: the session's scratchpad, `/tmp`,
and `/dev/null`. The host tells a worker to use its scratchpad, and chantier's guard refuses it,
so the worker loses a turn and often a retry. This child makes the guard pass two kinds of write:
a write to a null device, in every form a worker uses, and a write inside the session's
scratchpad. Every other write is judged exactly as today.

## Place in the chain

- **Base:** child 3's branch (`refusals-name-next-step`), the previous CR of the stack. Child 3
  changes only the CLI's refusal texts and their test. It does not touch `hooks/`, so this child
  has nothing to reconcile with it.
- **Depends on this child:**
  - Child 5 (`behaviour-measure`) builds on this branch. Its measure counts write-guard refusals
    per role, and child 28's run uses that count as this child's proof on the host.
  - Child 23 (host and shared cards) rewrites `references/hosts/claude-code.md`, whose guard
    section today says the scratchpad is refused (see "Out of scope"). That card must describe
    the guard as this child leaves it.
  - Child 24 (the swap) changes the hook's reload message, in another function of the same file.
    It does not touch the guard.

## Decisions carried

| Source | Decision | Here |
| --- | --- | --- |
| Answer 3 (simplify-cards-Q6) | A refusal seen in more than 2 % of a role's runs is a tool bug | "Goal" |
| Program child 4, Scope | `writtenBy` and `judgeShell` never judge a write to `/dev/null`, `NUL` or `$null` | "What changes", 1 |
| Program child 4, Scope and F17 | This specification chooses the scratch folder by reading the hook API the host ships: variant a if the host gives the scratchpad's path, else variant b | "The host's hook API": variant a is chosen |
| Program child 4, Scope | Cases for the passes are added in `hooks/register.test.tsx` | "What changes", 4 |
| Program child 4, Must not | No deny list; the main session stays unguarded; no judging inside an interpreter's inline code; a call the guard cannot cut still passes with a note; nothing changes on Copilot | "Out of scope" |
| Program child 4, Risk; AGENTS.md | `just mod` is owed (a change to `hooks/`), run by the Driver; a Driver who cannot run it stops and says so | "Gates and evidence" |
| Answer 22, F17 | A claim about the host that this program has not proved is marked "unproved", in this file and in the PR | "The host's hook API", "Known gaps" |
| Answer 22, F20 | The PR states the seconds its tests add to `just test` | "Gates and evidence" |
| Answer 18 | Tools first: no existing card text changes; every intermediate `main` works with the old cards | "Out of scope" |
| Answer 22, Q1 | No hook deny list in this program | "Out of scope" |

## What the refusals were (read for this specification)

All the figures below come from the user's transcripts under `~/.claude/projects`.

- **The null device.** Every recorded `/dev/null` refusal has the same text:
  `refused: a shell write to /dev/null) is outside the folders…`. Here is a seen call:
  `OB=$(git merge-base 14004ed origin/main 2>/dev/null); echo OB=$OB; …`.
  - The guard already passes a plain `2>/dev/null` (`NULLS` in `hooks/register.tsx`).
  - It fails inside a command substitution. The redirection target is read up to a blank, `;`,
    `|`, `&`, `<` or `>`, so the closing `)` of `$(…)` becomes part of the target. `/dev/null)`
    does not match `NULLS`, so it is judged as a relative path and refused.
  - The same happens to a target closed by a Bash backtick substitution (`` `cmd 2>/dev/null` ``)
    and to a PowerShell subexpression (`$(Get-Item x 2>$null)`).
- **The scratchpad.**
  - Refused paths have the form `C:/Users/<user>/AppData/Local/Temp/claude/<16 hex>/<session id>/scratchpad/…`.
    The same paths also appear in their Git Bash form, `/c/Users/…/scratchpad/…`.
  - In the 50 subagent transcripts sampled, the `<session id>` in the refused path is the
    session folder that holds the subagent's transcript. So a subagent writes in its main
    session's scratchpad, not in a scratchpad of its own.
- **Kept refused.** `/tmp/…`, `../x.log` and other paths outside the folders stay refused. The
  program scope covers only the null device and the scratch folder. See the open question.

## The host's hook API (variant a, chosen)

The host's hook types are not in the repository. `claude-code` is resolved by the host, and
`types/index.d.ts` holds only chantier's own shapes. This was read from the bundled code of the
Claude Code 2.1.330 binary the user runs:

- The engine's `$.session` includes `info()`, next to `cwd()`, `id()`, `root()` and the rest.
  `$.session.info()` takes no argument and returns
  `{ transcriptPath, scratchpadDir?, promptId?, agentType?, configRoot?, platform, isHosted }`.
- `scratchpadDir` is the current session's scratchpad. It is omitted when the scratchpad is
  disabled or when the session is hosted.
- The host's own file-write rule passes this folder too ("Files that Claude Code keeps for the
  session are not refused: its plan files, scratchpad…").

Variant a is therefore available, and this specification chooses it. Variant b would add a
`scratch:` line to the prompts (`src/driver_prompt.py`, `src/plugin_files.py`). It is not built,
for two reasons:

- the `<cr>/work/scratch` folder that `take` prints (`src/commands/facts.py`, line 145) is
  already inside the CR folder, and every guarded agent's `writes:` line names that folder, so
  the guard already passes it;
- no recorded refusal targets it.

**Unproved (F17):**

- That `$.session.info()` is callable from a mod's `tool.call` handler, and returns the main
  session's `scratchpadDir` when the call is a subagent's. The binary's code and the transcripts
  (above) say yes. Only `just mod` (validate: the call type-checks against the host's own types)
  and a real session prove it.
- How `claude plugin validate` types `session.info`'s result: it was read from the code, not
  from a `.d.ts`.

If `just mod` shows that `$.session.info` is not in the host's `EngineInterface`, the Driver stops
and hands back blocked with that line. It does not build variant b on its own: the variant is this
specification's choice, not the Driver's (F17). The Chief of Staff then has this file re-specified
for variant b.

## What changes

All in `hooks/register.tsx` and `hooks/register.test.tsx`. No CLI, card, type or configuration
file changes.

### 1. The null device inside a substitution (`judgeShell`)

- In `judgeShell`, the null-device test (`if (NULLS.test(raw)) continue`) is applied to the
  target with any trailing `)` and `` ` `` characters removed. This makes `/dev/null)`,
  `` /dev/null` ``, `$null)` and `NUL)` pass, case-insensitively as `NULLS` already reads them.
  The pass is silent: no note, as for the plain forms today.
- The judged path of every other target is left exactly as today. A non-null target followed by
  `)` keeps today's reading.
- `splitShell` and `writtenBy` are not changed. The other forms of the scope (`> /dev/null`,
  `2>/dev/null`, `&>/dev/null`, `tee /dev/null`, `2>NUL`, `2>$null`, `Out-File -FilePath $null`)
  already pass through `NULLS` for every target `writtenBy` returns. The tests in 4 pin them.

### 2. The session's scratchpad (`tool.call`)

- The guard's folders for one call are the agent's `writes:` folders, plus the session's
  scratchpad when the host gives one.
- The scratchpad is read lazily. `$.session.info()` is called at most once per call, and only
  when the call would otherwise be refused: for Write, Edit or NotebookEdit, when the path is
  outside every `writes:` folder; for Bash or PowerShell, when `judgeShell` returns an
  `outside` path.
- The guard then judges again with `[...known.folders, scratchpadDir]`:
  - For Write, Edit or NotebookEdit, the path passes if `guardInside(scratchpadDir, abs)` is true.
  - For the shell, `judgeShell(command, known.cwd, [...known.folders, scratchpadDir])` is called
    again, and the call is refused only if it still returns an `outside` path. A command with two
    targets, one in the scratchpad and one outside, is still refused, and the refusal names the
    one outside.
- When `scratchpadDir` is absent (the scratchpad is disabled, or the session is hosted), the
  folders are the `writes:` folders alone, and the call is refused as today, with no note.
- When `$.session.info()` throws, the existing outer `catch` applies: the call passes, with the
  board's note `Write guard: could not judge the <tool> call of agent <id> (<message>); the call
  passed.`. A guard at fault costs nothing.
- `guardInside` compares as today. A drive-form scratchpad (`C:\Users\…\scratchpad`, backslashes
  folded by `slash`) and a Git Bash target (`/c/Users/…/scratchpad/x`) match, as the
  `writes:` folders already do.
- Nothing is recorded at spawn. The `workers` atom keeps its shape (`workers-2`), and
  `types/index.d.ts` does not change. The scratchpad is read when it is needed, so a reload or a
  scratchpad created late changes nothing.
- No scratchpad path is written anywhere. It is only compared.

### 3. The refusal's folder list

- When the host gave a scratchpad, a refusal lists it after the `writes:` folders, since it is
  now a folder the agent may write in:
  - `refused: <path> is outside the folders this agent may write in (<folder>; <folder>; <scratchpad>); write there`
  - `refused: a shell write to <path> is outside the folders this agent may write in (<folder>; <scratchpad>); the shell follows the same rule as Write and Edit`
- The wording around the list does not change. The quotes in `references/hosts/claude-code.md`
  (`(<folder>; <folder>)`) still describe the form.
- When the host gave no scratchpad, the text is exactly today's.

### 4. The comment block

- The comment at the top of "the worker write guard" section of `hooks/register.tsx` (lines
  523 to 531 at `8a960d34`) gains one sentence: a write inside the session's scratchpad, which
  the host names through `$.session.info()`, passes, and so does a null device closing a
  command substitution.

### 5. Tests (`hooks/register.test.tsx`)

- `guardWorld` gains a parameter for the scratchpad: `scratch: string | null | 'throw'`, default
  `null`. It mocks the call as the file already mocks `session.cwd`:
  `on('session.info', () => ({ value: { transcriptPath: '', platform: 'linux', isHosted: false, ...(scratch ? { scratchpadDir: scratch } : {}) } }))`.
  `'throw'` answers `{ deny: '…' }`. With the default, every existing case keeps its expected
  text unchanged.
- New cases, few and table-driven like the file's `for (const [what, command, tool, part] of …)`
  block, each through the real `register` (spawn with `DRIVER_PROMPT` or `WORKER_PROMPT`, then a
  `tool.call`):
  - **The null device in a substitution passes.** A case per form: `` OB=$(git merge-base a b 2>/dev/null); echo $OB `` (Bash, the seen call), `` x=`ls 2>/dev/null` `` (Bash),
    `$v = $(Get-Item x 2>$null)` (PowerShell), `$(dir 2>NUL)` (PowerShell), each with `deny`
    undefined and no `could not` in the board's note.
  - **A non-null target closed by `)` keeps today's reading.** `$(echo x > ${ROOT}/a)` is still
    refused.
  - **A scratchpad write passes, for each tool.** With `scratch = SCRATCH` (a constant such as
    `C:/Users/u/AppData/Local/Temp/claude/0123456789abcdef/11111111-2222-3333-4444-555555555555/scratchpad`):
    Write, Edit and NotebookEdit to `${SCRATCH}/notes/a.md`; PowerShell
    `Set-Content -Path ${SCRATCH}/x.txt -Value y`; Bash `echo x > ${SCRATCH}/x.txt`; Bash in the
    Git Bash form `echo x > /c/Users/u/AppData/Local/Temp/claude/0123456789abcdef/11111111-2222-3333-4444-555555555555/scratchpad/x.txt`.
    All pass silently.
  - **Writes outside are still refused, with the scratchpad listed.** With `scratch = SCRATCH`:
    Write to `${ROOT}/src/a.py` gives `refusal(\`${ROOT}/src/a.py\`, \`${WT}; ${FOLDER}; ${SCRATCH}\`)`;
    Bash `echo x > /tmp/x.log` gives the shell refusal naming `/tmp/x.log`; a sibling of the
    scratchpad (`${SCRATCH}-other/x`) and its parent (`${SCRATCH}/../x`) are refused;
    `echo a > ${SCRATCH}/ok; echo b > ${ROOT}/a` is refused, naming `${ROOT}/a`.
  - **No scratchpad from the host.** With `scratch = null`, a Write to `${SCRATCH}/a.md` is
    refused with today's text (no scratchpad in the list).
  - **The host's call fails.** With `scratch = 'throw'`, a Write outside every folder passes,
    and the board's note holds `could not judge`.
  - **The read is lazy.** With a counter in the `session.info` mock, a Write inside the
    `writes:` folders makes no call, and a refused Write makes exactly one.
  - **An unguarded agent stays unguarded.** An agent with no `writes:` line makes no
    `session.info` call, and its writes pass as today (extend `an agent with no writes line has
    its shell left alone` with the counter).
- The tests read the shipped `hooks/register.tsx` through the file's own `register` import, at
  the head under test. No copy of the guard is made.

## Out of scope

- Any card text: `references/hosts/claude-code.md` (the guard's section, which says the
  scratchpad is outside the worktree and that a worker writes in its work folder instead), and
  `references/concepts.md`, "A CR's folder holds its work" (a CR's work is written in its folder,
  never in the host's scratchpad or a temporary folder).
  - No child before 19 edits a card (answer 18, program rules).
  - The card rule keeps its force as guidance. The hook simply stops enforcing it at the
    scratchpad. That rule was never the hook's: the hook refused only because the scratchpad lies
    outside the `writes:` folders.
  - The new card set (children 19 to 23) settles the wording.
- `/tmp`, `$TMPDIR`, `%TEMP%`, and relative paths that climb out of the folders (`../x.log`):
  they stay refused, or unjudged when they hold a variable, as today. See the open question.
- A deny list of commands (answer 22, Q1).
- Guarding the main session, the Release driver, the stack driver, the QA driver, or any agent
  with no `writes:` line.
- Judging inside an interpreter's inline code (`python -c`, `node -e`) or a script's own writes.
- A call the guard cannot cut still passes with its note. No new refusal is added.
- Copilot. It has no hook, and nothing in `com.github.copilot/` changes.
- Variant b: the `scratch:` prompt line in `src/driver_prompt.py` and `src/plugin_files.py`.
- `types/index.d.ts`, the `workers` atom's shape, and the agent spawn handler.
- AGENTS.md. The hook is not a CLI tool, and no named exception changes.

## Host and default matrix

The pass depends on the host and on whether the host gives a scratchpad.

| Cell | Expected | Proved by |
| --- | --- | --- |
| Claude Code, scratchpad given, Windows drive form | scratchpad writes pass, others refused with the scratchpad listed | `register.test.tsx` cases (mocked); real session unproved |
| Claude Code, scratchpad given, Git Bash form target | passes as the drive form | `register.test.tsx` Git Bash case |
| Claude Code, scratchpad given, POSIX path | passes | `register.test.tsx`, a POSIX `SCRATCH` variant of one Write case |
| Claude Code, scratchpad disabled or hosted (`scratchpadDir` absent) | today's behaviour and text | `register.test.tsx` "no scratchpad" case |
| Claude Code, `session.info` fails | the call passes with the note | `register.test.tsx` "throw" case |
| Copilot | no hook; the `writes:` line is inert | unchanged; nothing to test |

## Gates and evidence

- **`just mod`**, run by the Driver in the worktree, at the head it pushes. It runs
  `claude plugin validate .` (which must accept `$.session.info()` against the host's own types)
  and `claude plugin test .` (the cases above).
  - A Driver who cannot run it stops and says so, with no workaround (AGENTS.md).
  - The PR quotes the last lines of both steps.
- **`just check`**, before the first push (AGENTS.md).
  - `just eval-dry-run` is not owed: nothing changes under `src/` or `evals/kit/`.
- **Long gate.** This child changes no CLI, card or scenario file, so the program rule ("owed if
  variant b changes the CLI") does not apply.
  - The pipeline's `just scenario (ubuntu-latest)` job still runs on the PR, and its result is
    quoted.
  - The local Windows run `chantier gate <cr> scenario` is owed only if this CR is the stack's top
    when it is presented as ready.
- **`just test` seconds (F20).** Under Deliverables, the PR states the seconds its tests add to
  `just test`, measured before and after on the same machine. The expected figure is 0 s: no
  pytest file changes, and the hook cases run under `just mod`. The PR also states the seconds
  that `claude plugin test .` takes before and after.
- **The behaviour proof on the host.** Child 5's measure counts write-guard refusals per role,
  and child 28's run reports it. The scratchpad and `/dev/null)` lines of S5 should fall to none.
  This child only names that proof, as a Known gap.

## Known gaps (to carry into the PR)

- "Scratchpad pass unproved in a real session: `$.session.info().scratchpadDir`, read from the
  host's 2.1.330 code, is only mocked in `register.test.tsx`; child 28's run measures it."
- "`references/hosts/claude-code.md` and `references/concepts.md` still describe the scratchpad
  as refused or banned for a CR's work; child 23 and the new floor settle the wording."

## Risk

- **A false refusal blocks a worker.** The change only adds passes. A refusal can only appear
  where one appears today, and its text gains the scratchpad in the list.
- **A false pass.** A write to the scratchpad is no longer stopped. Work written there is lost to
  the CR's folder: it is not archived, and not seen by the Inspector. The card rule still asks
  for the CR's folder. The real-run measure of child 28 shows whether workers then leave results
  in the scratchpad.
- **The host's API changes.** If a later host drops or renames `session.info`, `claude plugin
  validate` fails at `just mod`. If the call fails at run time, the call passes with the note
  (no worker is blocked).

## Open questions

1. **`/tmp` writes (scope).** S5 counted 115 `/tmp` refusals, and about 260 refusal lines in the
   full transcripts. This specification keeps them refused, since the program's scope names only
   the null device and the scratch folder. The refusal now names the scratchpad, so a worker
   can move there in one step. The host's own prompt also says to use `/tmp` only when the user
   asks. Should `/tmp` (and `%TEMP%` outside the scratchpad) pass too? If yes, that is a
   separate inbox item, not this child.
