# Change Specification: the batch-09 retro's fixes

Priority P1. One CR and one PR ("Une seule CR"). Sources: `intake/request.md`, `01-intent.md`,
`02-answers.md` (which ranks above the request), and `4-batch/retro.md`, points 5, 6, 8, 9, 10,
11, 14 and 16. The code was read on main at fde3da8.

## Goal

The user wants fixes that work "quand chantier sera déployé dans n importe quel type de projet",
without making the process rigid or more costly ("on rigidifie le process et ça augmente les
coûts"). The aim is fewer retries and fewer skipped proofs:

- A worker cannot write outside its CR's worktree. This is enforced by a Claude Code hook that
  costs no token.
- `handback ready` refuses unless the two proofs hold at the PR's head: the long gate passed and
  the last verdict is `VERIFIED`. This is the only new refusal. Every other step stays the
  Driver's judgement.
- A CR handed back with no long gate (`--no-gate`) is checked by the steering session against the
  project's rules, and the docs teach any project how to declare its gates.
- The CLI does the following:
  - it queues `order add` on a running direct batch;
  - it gives the steering session's own subagents their own line in `cost`;
  - it runs a multi-command gate the same way on every OS;
  - it accepts a CR's bare number everywhere;
  - it prints the spec-writer's first prompt line.
- A brief states a past fact only with its source.

Nothing here may rely on this repository's `just`, forge or OS. The CLI stays dependency-free and
portable (POSIX and Windows, UTF-8). A role's contract stays in its card, and the CLI knows no
role.

## Decisions carried from `02-answers.md`

1. The hook **refuses** a worker's write outside its worktree. It does not only warn.
2. A CR the project's rules exempt from the long gate (here: docs only) is handed back with
   `handback <cr> ready --no-gate "<the project's rule>"`. The exemption is logged and shown in
   the report, and the verdict `VERIFIED` stays mandatory.
3. Part 1 is for **Claude Code only**. The Copilot host stays as it is, with nothing added, not
   even a Driver check.
4. Priority P1.
5. The Driver's check of the main checkout (comparing `git status --porcelain` with its state at
   `take`) is **dropped**: the hook's refusal is enough.
6. From before filing:
   - `take` lists the two gates as a checklist.
   - `handback ready` refuses when one is missing.
   - The gate and verdict events go in `events.jsonl`, and the PR's head in `batch.json`.
   - A new `verdict` command records the verdict.
   - The eight parts make one CR.
7. (Answer 7) **The Verifier itself runs `verdict`**, at the head it verified, as it already runs
   `gate`.
8. (Answer 8) `verdict` also records **`NOT VERIFIED`**, and **the last verdict at a head
   decides**. A skipped Verifier pass on the PR description is still not caught by the CLI: it
   stays the Driver's judgement.
9. (Answer 9) A project with no long gate at all:
   - the Driver may hand back with `--no-gate "<the project's rule>"`;
   - the steering session (the Foreman, or the Chief of Staff in direct mode) checks that this is
     legitimate: the project truly has no long gate, or its rules exempt this CR;
   - the docs explain the good practice to a user of any project: what a fast (short) gate and a
     long gate are, how to declare them in `AGENTS.md`, and how to have chantier declare them.
   No project-level setting in `chantier.yaml` is added.
10. (Answers 10 and 11) The hook guards **workers only**, and only their **Write and Edit** (and
    `NotebookEdit`, the same kind of file write). Drivers and writes through a shell stay out.
11. (Answer 12) A **QA driver keeps its own Driver line** in `cost`; it does not go on the
    steering session's line.

## What changes, part by part

### 1. A worker cannot write outside its CR's worktree (Claude Code only)

**File:** `hooks/register.tsx` (the plugin's Claude Code mod, registered by `hooks/hooks.json`).
Its tests go in `hooks/register.test.tsx`.

**How the hook learns the worktree.** Every worker prompt starts with `chantier <role> for <cr>
…` and carries the fact lines that `_facts` prints (`commands.py`), including:

```
folder: <CR folder> (work/, evidence/)
worktree: <path> branch <branch> base <ref>
```

The mod does the following:

- On `agent.spawn`, it looks at the prompt. When the first line starts with `chantier ` and the
  prompt holds a `worktree:` line, it reads the worktree path, and the CR folder from the
  `folder:` line. When the spawn resolves (`next(e)` gives `{ agentId }`), it records `agentId →
  { worktree, folder }`. It records nothing for a denied spawn.
- On `tool.call`, when `agentId` is a recorded worker and the tool is `Write`, `Edit` or
  `NotebookEdit`:
  - It resolves the target path. A relative path is read against the spawn's `cwd`.
  - It allows the write when the path is inside the worktree or inside the CR folder. The CR
    folder covers the work folder `work/<role>/`, including `work/verifier/evidence/`, and the
    CR's `evidence/`.
  - Otherwise it returns `{ deny: "<message>" }`. The message names the path refused and the
    two places allowed, for example: `refused: <path> is outside this CR's worktree <worktree>
    and its folder <folder>; write there`.
- Only workers are guarded (decision 10). A Driver's own prompt carries the batch facts, not a
  worker's `worktree:` line (the Driver checks the two prompt forms in `concepts.md`, "Starting
  an agent", and keys the match on what tells them apart). The main session, Drivers,
  spec-writers, griller agents, unknown agents and the host's own tools are untouched.
- Bash and PowerShell are not guarded (decision 10).

**Implementation notes for the Driver:**

- Use the mod's existing path helpers (`clean`, `fold`, `isInside`) so that Windows drive case
  and separators compare correctly.
- Keep the map in an `atom` so that it survives `/reload-plugins` and a compaction.
- Follow the engine's rule for `tool.call` guards: "a guard that fails is skipped and the tool
  runs". Give the guard a `.catch` that denies when the guard itself fails on a recorded worker,
  and lets the call through otherwise.
- The mod still writes no file and runs nothing new.
- If a recorded worker's first tool call can arrive before the spawn's `next(e)` resolves, the
  guard must still find the record. Key on what the engine gives at both points, or record
  before `next`. The Driver checks this against the engine's types (`types/index.d.ts`).
- The host's own scratchpad (the session temp directory) is outside the worktree. If a worker
  needs it, the refusal message tells it to write in its work folder instead. Do not add an
  exception.

**Cards and docs:**

- `skills/chantier/references/worker.md`: next to "works only in the CR's worktree", say that on
  Claude Code a Write or Edit outside the worktree and the CR folder is refused by the plugin.
  Say also that a refusal means the path is wrong, not that it should be retried by another
  means (a shell write included).
- `skills/chantier/references/hosts/claude-code.md`: a short section on the hook (what it
  guards: workers' Write, Edit and NotebookEdit; what it leaves alone: Drivers, the steering
  session, shell writes), marked unproved until a real trial, as the file marks other unproved
  behaviour.
- `CONTRIBUTING.md` point 4 (the mod's description) and `README.md` (around line 423, where the
  mod is described): the mod also guards a worker's writes.
- Copilot (`com.github.copilot/`, `hosts/copilot*.md`): nothing changes.

### 2. `handback ready` refuses without a passed long gate and a VERIFIED verdict at the head

**New command `verdict`** (`cli.py` parser, `commands.py`):

- Usage: `verdict <cr> VERIFIED` or `verdict <cr> "NOT VERIFIED"` (decision 8). The parser may
  also take `NOT VERIFIED` as two words; both forms must work on POSIX shells, `cmd.exe` and
  PowerShell.
- It reads the head of the CR's worktree (`git rev-parse --short HEAD`, the same short form
  `gate` logs and `ship` compares).
- It logs one event to the batch's `events.jsonl` through `b.log("verdict", cr, result=<VERIFIED
  | NOT VERIFIED>, head=<short sha>)`.
- It prints one line, `verdict <cr> <result> at <head>`.
- It refuses (EXIT_PRECONDITION) for:
  - a CR the batch does not hold;
  - a CR with no worktree;
  - a dirty worktree, because a verdict on uncommitted work cannot be bound to a head.
- **The last verdict at a head decides** (decision 8): a `NOT VERIFIED` after a `VERIFIED` at the
  same head cancels it, and a later `VERIFIED` restores it. A verdict at another head never
  counts.
- It knows a verdict, not a role. The card says who runs it (decision 7).

**`gate` and the head.** `gate` already logs `kind=gate result head command`. Part 5 changes how
a passed gate is computed.

**`handback <cr> ready`** (`commands.py` `handback`, about line 1432). For a CR handback, not the
release kind, which keeps its own path:

1. It still requires a PR (`c.get("pr")`), as now.
2. The head is the one `ship` recorded in `batch.json` (`c["head"]`).
3. **Long gate:** passed at that head (see part 5 for "passed"), unless `--no-gate "<reason>"`
   is given.
4. **Verdict:** the last `verdict` event at that head has `result` `VERIFIED`. `--no-gate` never
   waives it.
5. It refuses with EXIT_PRECONDITION and names each missing gate on its own line, for example:
   - `refused: no long gate passed at <head> (gate <cr> <command>... , or --no-gate "<the
     project's rule>")`
   - `refused: no verdict VERIFIED at <head> (the last verdict there: <NOT VERIFIED | none>)`
6. With `--no-gate "<reason>"`:
   - an empty reason is a usage error (exit 1);
   - the reason is stored on the `handback` event (`no_gate=<reason>`);
   - the hand-back line printed shows it, so the steering session sees it at once:
     `[driver <cr>→foreman] hand-back ready, no long gate: <reason> …`.

**The checklist up front.** `_facts` (printed by `take`, `round` and `handoff`) adds a block that
lists the two gates and their state at the head `ship` recorded, or `not shipped yet`:

```
gates before handback ready, at the PR's head <head|not shipped yet>:
  [ ] long gate passed (gate <cr> <cmd> [<cmd>...]; none in the project's rules: handback --no-gate "<rule>")
  [x] verdict VERIFIED (the Verifier: verdict <cr> VERIFIED|"NOT VERIFIED")
```

The marks are read from `events.jsonl`; the verdict line is `[x]` only when the last verdict at
the head is `VERIFIED`, and says `NOT VERIFIED` when that is the last one. The block stays within
the 10-line output rule, or the command is in `FULL_OUTPUT` if it already is.

**The report and STATUS.md** (`status.py`, `skills/chantier/references/status-layout.md`):

- `_steps` adds a "Verdict" step from the last `verdict` event (its result and head).
- A `--no-gate` hand-back shows in the "Long gate" step as `waived: <reason>`.
- `_now_next` ("…then the verifier at the pushed head.") names the verdict command.
- `status-layout.md` says the report lists a CR handed back with `--no-gate` and its reason.

**Why the Drivers believed the budget stopped them.** `rails.py` refuses on the budget only at
`take`, `round` and `release` (`check_budget`, `check_round`). Yet `driver.md` (the hand-back
lines, about line 87) lists a `budget:` reason with no word on where the budget applies, and
nothing in the card forbids dropping a proof to save budget.

**Cards:**

- The Verifier (`skills/chantier/references/worker.md`, "## Verifier", line 71): its
  output step ends with `$CHANTIER verdict <cr> VERIFIED` or `$CHANTIER verdict <cr> "NOT
  VERIFIED"`, at the head it verified, from the CR's worktree, before it replies. The short pass
  on the posted description records its verdict the same way, so a description found `NOT
  VERIFIED` cancels an earlier `VERIFIED` at that head until a later pass says `VERIFIED`.
- `skills/chantier/references/driver.md`:
  - The gate line (about line 35): the multi-argument form (part 5).
  - The CR flow (line 121 and after): the Verifier records its verdict itself; the Driver does
    not run `verdict` for it.
  - The hand-back (lines 83-92):
    - `ready` needs, at the PR's head, a passed long gate and a last verdict `VERIFIED`;
    - `--no-gate "<the project's rule>"` is only for a project whose rules declare no long gate,
      or exempt this CR from it, and quotes that rule; the steering session checks it;
    - `budget:` follows only a CLI refusal on the budget (`take` or `round` exit 5). A Driver
      never skips a proof pass to save budget.
  - The new refusal adds a failure mode the card's recovery lines must cover: the Driver runs
    the missing gate (or a new Verifier pass) and hands back again.
  - A CR sent back with a note saying the `--no-gate` does not hold: run the long gate, then hand
    back again without `--no-gate`.
- `skills/chantier/references/concepts.md`:
  - the command list gets `verdict`, `gate`'s new form and `handback --no-gate`;
  - the exit codes and output list (lines 163-170): `handback`'s new refusal is exit 2.
- **The steering session's check of `--no-gate`** (decision 9), in
  `skills/chantier/references/foreman.md` (next to "The user's boundaries", line 37, where the
  `ready <cr> <link>` ask is described) and in `chief-of-staff.md` (direct mode, "The Drivers",
  line 488, which points to the Foreman's card):
  - A ready hand-back with `no long gate: <reason>` is checked before the ask: read `$CHANTIER
    rules` and find the rule the reason quotes. It is legitimate when the rules say the project
    has no long gate, or exempt this CR (for an exemption by kind of change, such as docs only,
    check the PR's changed files on the forge: `gh pr diff --name-only`, `glab mr diff`).
  - Legitimate: the ask is `ready <cr> <link> no long gate: <reason>`, and the report shows it.
  - Not legitimate (the rules declare a long gate that covers this CR): send the CR back to a
    Driver with `take <cr> --note "long gate: <why the exemption does not hold>"`; no ask.
  - The rules say nothing about a long gate: this is the existing rule of `chief-of-staff.md`
    line 69, a question for the user (in Foreman mode the ask `question <cr> no long gate written
    down: <the Driver's reason>`), with the Chief of Staff's recommended answer and an offer to
    write it in `AGENTS.md`. An absent gate never means success.
- `chief-of-staff.md` line 69 is aligned: once the project's rules say there is no long gate or
  exempt a CR, `--no-gate` carries the rule and the steering session checks it as above.
- `chief-of-staff.md` lines 333-338 (the force-push check reads a gate pass at the local head):
  use the same "passed" rule as part 5.

**Docs: the good practice for gates** (decision 9). The user-facing home is the **README**,
because it is what a user of any project reads; `init.md` and the tutorial point to it, and the
cards keep only the roles' judgement.

- `README.md`, a new subsection **"### Your gates"** under "## Use", before "### Your own
  agents" (line 235). It says, for any project:
  - **The fast gate** (a short check): what the Coder runs after every round, and the Inspector
    may run to check a claim. It should take seconds to a minute: lint, type check, the tests
    near the change.
  - **The long gate**: the full check the Driver runs once before the PR with `chantier gate`,
    alone in the repository, and that `handback ready` requires at the PR's head (with the
    Verifier's `VERIFIED`). One command may serve as both.
  - **How to declare them in `AGENTS.md`**: one line each, with the exact commands, one command
    per item, never chained with `&&` or `;` (the Driver passes each as its own argument to
    `chantier gate`, so it runs the same way on every OS). For example:

    ```markdown
    - Fast gate (after each change): `npm run lint`, `npm test -- --changed`.
    - Long gate (before a pull request): `npm test`.
    - A change to the docs alone needs no long gate.
    ```

    An exemption (the last line) and a project with no long gate at all (`This project has no
    long gate: <why>`) are written there too: the Driver quotes that rule with `handback ready
    --no-gate`, and the Foreman (or the Chief of Staff steering) checks it. A rule that is not
    written is a question for the user, never a pass.
  - **How to have chantier declare them**: say "init" (the tour looks for both gates and proposes
    the exact `AGENTS.md` lines), or tell the Chief of Staff "our long gate is `<command>`" (it
    proposes the lines). Either writes them only on the user's yes.
  - One row added to the "Use" table (line 203): "our long gate is `npm test`" | the Chief of
    Staff proposes the exact `AGENTS.md` lines and writes them on your yes.
- `skills/chantier/references/init.md`, step 5 item 1 ("Getting started here", line 67): name the
  two gates explicitly. The tour checks whether the project's rules declare a fast gate and a
  long gate (or no long gate, or exemptions). When one is missing, it proposes the exact
  `AGENTS.md` lines in the form above, with its impact when missing (a long gate the Driver
  cannot run is a `--no-gate` the steering session must question). It points to the README's
  "Your gates". The glossary line (line 80) keeps "fast gate, long gate".
- `docs/tutorial-claude-code.md`, section 2 (lines 36-55): the example `AGENTS.md` uses the
  "Fast gate" and "Long gate" labels, one command per item (its `npm run lint && npm test --
  --changed` becomes two commands), and the paragraph after it links the README's "Your gates".
- The term stays **fast gate** (the cards', the tutorial's and the eval fixture's word); the
  README says "a short check" once to name what it is.

### 3. `order add` queues a CR on a running direct batch

- `commands.py` `order` (lines 1025-1102):
  - `add` on a running direct batch (not paused) no longer raises "a running direct batch is
    strict…". It queues the CR as it does in Foreman mode, and the Chief of Staff takes it when a
    slot frees.
  - `order qa` keeps its current behaviour, and so do `--release` and `--fix-for`.
- Cards:
  - `concepts.md` lines 70 and 114 ("running direct batch is strict");
  - `chief-of-staff.md` lines 499-502 and 513-516: a CR added while a direct batch runs is
    queued and taken when a slot frees, with no pause needed; `order qa` stays refused.
  - `init.md` line 45 ("no CR joins the batch while it runs") is aligned the same way.
- Tests and scenario:
  - `skills/chantier/scripts/cli/tests/test_structure.py`,
    `test_a_direct_batch_is_recorded_shown_and_strict` (line 295, assert at line 314): `add` is
    now accepted. Keep the test's other checks, and rename it if "strict" no longer holds.
  - `scenario/run_scenario.py` (`direct_batch`, line 907; the refusal check at line 984): `order
    add` on the running direct batch queues the CR. The scenario takes it at a free slot.

### 4. `cost` puts the steering session's own subagents on their own line

The problem is in `commands.py` (lines 1960-2280):

- `_kind` (line 2116) labels an agent with no parent "Driver".
- `_breakdown` prints `"{kind} {type}"`.
- So the Chief of Staff's own `Explore` subagent shows as "Driver Explore", and `_cost_groups`
  puts it under a Driver.

The change:

- An agent with no parent and no `agent` event tying it to a CR, the stack or a QA order is not a
  Driver. It goes on the steering session's own line:
  - "Chief of Staff's own subagents" in direct mode;
  - "Foreman's own subagents" in Foreman mode.

  Its tokens still count in the session's spend.
- **A QA driver keeps its own Driver line** (decision 11). Today nothing ties it to the batch: it
  has no CR, and `agents set` takes only a CR or `stack` (`commands.agents`, line 1233). So
  `agents set` also takes the QA order's id (`O-<k>`, the one `order qa` printed), logs the
  `agent` event with it, and the Foreman's card (`foreman.md` line 70, "An `order qa`") and the
  Chief of Staff's direct-mode lines record the QA driver's agent id that way after starting it.
  `_cost_groups` puts such an agent on a Driver line; `by="cr"` puts it under its QA folder.
- An agent started in a grill or specification turn goes to the grill line instead, by the
  window CR-165 introduced (`GRILL_NAMES`, `_grill_use`, `usage(split=True)`), as the
  spec-writers already do (`costs.is_spec_writer`).
- `_kind`, `_breakdown`, `_cost_groups` (both `by="driver"` and `by="cr"`) and `_cost_summary`
  follow this. The steering share and the orchestration ratio that the pause report prints
  (CR-165) count the new line as steering.

### 5. `gate` runs several commands the same way on every OS

- `cli.py`: `gate` takes `cr` and `command nargs="+"`, so the form is `gate <cr> "<cmd>"
  ["<cmd>"...]`.
- `commands.py` `gate` (line 1634):
  - Under one `_LongGateLock`, it runs each argument in order, each in the platform's shell as
    today (`shell=True`).
  - It stops at the first failure.
  - It logs one `gate` event per command run (`result`, `head`, `command`).
  - It writes the logs to `work/gates/<ts>.log`, one log per run, with each command's section
    marked.
  - It prints one line per command (`pass <cmd> at <head>` or `FAIL <cmd> at <head>`) and the
    log path.
  - A failure exits 4, as now.
  - Commands after a failure are not run and are not logged as passed.
- **"Passed at a head"**, used by `handback`, by `ship`'s existing check and by the Chief of
  Staff's force-push check: the last `gate` invocation at that head passed every command it was
  given.
  - To tell invocations apart, the events of one invocation share a field, for example
    `run=<ts>`.
  - `ship`'s current check ("a pass gate event at the short head") is aligned on this rule.
- Cards: `driver.md` line 35, `worker.md` line 75 (the Verifier's gate) and `concepts.md` show
  the new form and say "one command per argument, never a `;` or `&&` chain".
- The scenario's gate checks (`run_scenario.py` lines 521 and 558) and the `driver_round` helper
  use the new form. One step runs two commands and one step has the second command fail.

### 6. Every command accepts a CR's bare number

- `commands.py`: one normaliser, replacing `_cr_arg` (line 812, used only by `order`):
  - `165`, `CR-165` and `cr-165` all become `CR-165`;
  - anything else is left as it is (a stack id, an `O-k` order, a QA folder).
- It applies to every CR argument:
  - the commands `take`, `round`, `handback`, `note`, `log`, `handoff`, `gate`, `ship`,
    `verdict`, `release`, `cancel`, `agents`, `order` and `stack`;
  - the options `--fix-for` and `after`.

  Apply it once, where the arguments are parsed or in `_batch_cr` and `state.Batch.cr`, so that
  no command is missed.
- The error "unknown CR <id> in batch <batch>" names the normalised id.

### 7. The CLI prints the spec-writer's first prompt line

- `playbook.py` / `commands.py` `playbook` (line 1527): `playbook` (without `--batch`) prints the
  spec-writer's exact first prompt line, with the project root resolved:

  ```
  spec-writer prompt, first line: chantier spec-writer for the Chief of Staff, in the project <root>.
  ```

  This is the form given in `concepts.md` line 225. In a Griller-started setup, the line names
  whoever starts it, as `concepts.md` gives it.
- `chief-of-staff.md` (lines 130-140) and `griller.md` (line 15): copy the first line as
  `playbook` prints it, unchanged. Do not start a second spec-writer for the same CR while one
  runs. A refused start is fixed by copying the printed line, not by retrying variants.

### 8. A brief states only facts it can cite

- `chief-of-staff.md` and `foreman.md`: a brief (any prompt or message to an agent) states a past
  fact only with its source: a CR note, a file in the CR's folder, or an event in
  `events.jsonl`. A fact with no source is said as unknown.
- This is card text only, with no CLI change.

## Both hosts

`agents/` and `com.github.copilot/agents/` are not changed by this CR: every role change above is
in the cards. If the Driver finds an agent file that restates a changed rule (the gate form, the
verdict), it changes the role on both hosts together, with identical bodies.

## Out of scope

- Copilot gets no equivalent of the hook and no Driver check (decision 3).
- The Driver's check of the main checkout (decision 5).
- The hook does not guard (decision 10):
  - Bash or PowerShell writes;
  - a Driver's, the Chief of Staff's or the Foreman's own writes;
  - spec-writers or griller agents.
- A `chantier.yaml` setting for "no long gate" (decision 9: the rule lives in `AGENTS.md`).
- `order qa` on a running direct batch.
- Any other proof step made mandatory: a second Inspector after a fix, the Investigator, the
  Verifier's pass on the PR description (decision 8). These stay the Driver's judgement, beyond
  the two gates.
- The discarded retro point 7 (a prompt overriding a card), and the points not filed: 15
  (Auto-fix) and 17 (the BOM).
- The open inbox items `handback-after-rebase`, `heartbeat-odd-values` and `report-template`.
- Changing where the budget refuses (`rails.py`).

## Evidence

- `just check` passes on Linux, macOS and Windows. It covers `tests/test_structure.py`:
  - the direct-batch test updated for part 3;
  - the structure checks for the new `verdict` command and the `gate` form (parser and cards
    naming them).

  Keep these tests few and fast.
- `claude plugin validate .` and `claude plugin test .` pass, with `hooks/register.test.tsx`
  cases:
  - a worker spawned with a `worktree:` line, whose Write inside its worktree and inside its CR
    folder (`work/<role>/`, `evidence/`) is allowed;
  - that same worker's Write, Edit and NotebookEdit in the main checkout, which are denied with
    the message naming the allowed places;
  - that same worker's Bash call, which is not guarded;
  - a Windows path differing only by drive case or separators, which is judged the same;
  - a relative path, read against the spawn's `cwd`;
  - the main session, a Driver and an agent with no `chantier` prompt, which are not guarded;
  - a guard error on a recorded worker, which denies.
- `just scenario` passes on both forges:
  - `gate` with two commands passes, and a two-command gate whose second command fails stops
    there and logs no pass for it.
  - `handback ready` with no gate at the head is refused, naming the long gate. With the gate
    but no verdict, it is refused, naming the verdict.
  - After `verdict <cr> VERIFIED` and a passed gate, `handback ready` is accepted. Every
    existing `handback … ready` in the scenario first records a verdict.
  - `verdict <cr> VERIFIED` then `verdict <cr> "NOT VERIFIED"` at the same head: `handback
    ready` is refused; a later `verdict <cr> VERIFIED` there lets it through.
  - `handback ready --no-gate "<rule>"` with a verdict is accepted. The reason is in the
    `handback` event, on the printed line and in the CR's STATUS.md "Long gate" step.
    `--no-gate` with no verdict is refused; `--no-gate ""` is a usage error.
  - A verdict made before a new commit is not counted at the new head.
  - `take` and `handoff` print the two-gate checklist, with its marks following the events.
  - `order add` on a running direct batch queues the CR (line 984 updated).
  - `ship 165`, `gate 165 …`, `handback cr-165 ready` and `verdict 165 VERIFIED` all resolve to
    `CR-165`.
  - `playbook` prints the spec-writer's first line with the root resolved.
  - `agents set O-<k> <id>` after an `order qa` is accepted.
  - `cost` on a session with a subagent not tied to a CR shows it on the steering session's own
    line and not as "Driver …", and an agent recorded on a QA order on a Driver line. If the
    scenario cannot build such a session, a structure test on `_kind` and `_cost_groups` with
    crafted rows does.
- Card and docs text (the steering session's `--no-gate` check, the README's "Your gates",
  `init.md`, the tutorial) is reviewed by the Inspector against decision 9; the steering
  session's check is a judgement and has no CLI proof.
- The hook is shown as unproved in `hosts/claude-code.md` until a real batch shows a refused
  write.

## Open questions

None. Answers 7 to 12 settle Q1 to Q5 of the earlier version.
