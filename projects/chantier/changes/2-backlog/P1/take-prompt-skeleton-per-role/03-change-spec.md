# Change Specification: `take` prints each Driver role's prompt skeleton

## Goal

In batch-22 the Chief of Staff gave the release Driver a `writes:` line (its CR folder), though
`foreman.md` says a release driver never gets one. The write guard then refused the Driver's writes
in its worktree, and with no Agent tool it was lost and had to be taken back. The user's fix
(`02-answers.md`, take-skeleton-Q1): `take` prints the **whole prompt skeleton** for the CR's
Driver role. That is its first line, the card to name and the other template lines, with no
`writes:` line for a release, stack or QA Driver. `take stack` prints the stack driver's
(take-skeleton-Q3) and `order qa` the QA driver's (take-skeleton-Q4). The steering session (the
Foreman, or the Chief of Staff in direct mode) copies the skeleton and fills it in, so it no longer
rebuilds a Driver's prompt from memory.

This changes what `take` prints and how every Driver is started (the spec critic's note in
`02-answers.md`).

## Where it came from

- `intake/request.md`: retro of batch-22, kept point
  (`5-archives/batches/batch-22.md`, line 57). P1, on the user's word.
- `02-answers.md`, take-skeleton-Q1 to Q4.

## Today

- `take <cr>` (`skills/chantier/scripts/cli/src/chantier/commands/driver.py`, `take`) prints
  `took …`, then `cr_facts` (`commands/facts.py`), then the refresh lines. `cr_facts` prints the
  facts (`cli:`, `cards:`, `specification:`, `folder:`, `worktree:`, `clone:`, `archive:`, `PR:`,
  `rounds:`, status lines, gate boxes, `team:` and `ci:` lines). It also prints each **worker's**
  opening lines (`worker_prompt_lines` in `plugin_files.py`, read from the agent files whose
  description says `Started by a Driver.`). It prints nothing for the Driver's own prompt.
- The `archive:` line prints the path `archive_path` returns (`plugin_files.py`), relative to the
  project's repository (`.agents/changes/5-archives/<stamp>-<name>/`). The write guard
  (`hosts/claude-code.md`, "The write guard") reads `writes: <absolute folder>; <absolute folder>`.
- `take stack` (`_take_stack`) prints the stack lines (`stack_lines`: the chain line, then one row
  per CR) and nothing for the stack driver's prompt.
- `order qa` (`commands/orders.py`, `order`; `orders_apply.py`, `_qa`) prints the order's line
  `[chief-of-staff→foreman] order O-<k>: qa …` and `QA folder: <folder>; the Foreman starts its QA
  driver, …`, and nothing for the QA driver's prompt. `foreman.md` (line 185-191) has the Foreman
  write it by hand: "copy the first line, …, then the card, the CLI, the default branch and the
  user's note".
- The Driver's prompt is written by hand from `concepts.md`, "Starting an agent" (template, first
  line table), and `foreman.md` line 169: "A CR Driver's prompt holds `writes: <the take's
  folder:>` (…); a stack, release or QA driver gets none". `chief-of-staff.md` ("The Drivers",
  around line 1408) sends the Chief of Staff in direct mode to the Foreman's card.
- The CLI knows no role (AGENTS.md). It learns roles from the plugin's files: the agent files'
  `Prompt starts with:` and `Started by …` text, and `Your card is` in a worker's body.

## What changes

### 1. The card: one table of Driver prompts (`skills/chantier/references/concepts.md`)

In "Starting an agent", right after the prompt template, add a subsection **"A Driver's
prompt"** with one table. It is the only source of which template lines each Driver's prompt
holds. The CLI reads it (section 3), and `foreman.md` and `chief-of-staff.md` point to it:

| Driver | Started after | Card | `writes:` | `Team:` |
| --- | --- | --- | --- | --- |
| `cr-driver` | `take <cr>`, a CR of kind `change` or `fix` | `driver.md` | the CR folder, then the absolute archive path when `take` prints one | yes |
| `release-driver` | `take <cr>`, a CR of kind `release` | `driver.md` | none | none |
| `stack-driver` | `take stack` | `driver.md` | none | yes |
| `qa-driver` | `order qa` | `driver.md` | none | none |

Rules stated under the table, in the card's words:

- Every Driver's prompt holds the opening lines, `CLI ($CHANTIER):`, the lines its command
  printed for it (section 2), `Steering:`, `Needs:` when the playbook gives the role some, and
  `Note:`. It holds `writes:` and `Team:` only where the table says so.
- `writes: none` means the prompt has **no** `writes:` line: the guard would refuse the Driver's
  worktree writes ([host's reference](https://github.com/gsemet/chantier/blob/main/skills/chantier/references/hosts/claude-code.md)).
- Every path on a `writes:` line is absolute: the CR folder as `folder:` prints it, and the archive
  as `<worktree>/<archive path>` (take-skeleton-Q2).
- `take`, `take stack` and `order qa` print this skeleton, filled in where they can (section 2).
  The steering session copies it whole and fills in each `<…>` left. It adds no template line the
  skeleton does not print and drops none it prints.

The template's comment on the `writes:` line (line 434) and the one on `Team:` (line 436) say
"see "A Driver's prompt"" for Drivers; the `writes:` comment says "the absolute archive path". The
text about workers stays as it is.

Keep the column headers, the role names in backticks, the kind words (`change`, `fix`,
`release`), the commands (`take stack`, `order qa`) and the words `none` and `yes` exactly as
above. A structure test reads them (section 5).

### 2. What `take`, `take stack` and `order qa` print

Each prints one block for the Driver the table's "Started after" names: `take <cr>` after the facts
(and before the refresh lines `fresh`), for the CR's kind; `take stack` after the stack lines;
`order qa` after its `QA folder:` line (and before the refresh lines). Each block starts with a
heading, then the prompt lines, each with two leading spaces.

**Heading.** `<role> prompt (copy it whole, without the two leading spaces, and fill each <…>; add
no line and drop none):`. When the table gives the role no `writes:` line, the heading says so:
`release-driver prompt (no writes: line: this Driver gets none; copy it whole, …):`, and likewise
for `stack-driver` and `qa-driver`. A reader who copies only part of it still sees the rule.

#### 2a. The CR and release Driver (`take <cr>`)

The shape, for a CR Driver on Claude Code steered by the Foreman:

```text
cr-driver prompt (copy it whole, without the two leading spaces, and fill each <…>; add no line and drop none):
  chantier cr-driver for CR-5 "<title>" of batch batch-23, in the project <root>.
  Read <skill>/references/startup-core.md, the host core, role core, and the short startup section named by <skill>/references/startup-manifest.json; defer the rest until an action names it.
  Read <skill>/references/driver.md;
  the project's rules rank above them: run `$CHANTIER rules` first and read what touches your work.
  <the role's contract lines, as printed>   (only when the playbook starts the role as a generic agent)
  CLI ($CHANTIER): <the cli: line above, after "cli: ">
  <the other lines above, from "cards:" on, as printed>
  writes: <folder>[; <worktree>/<archive path>]
  Steering: the Foreman <the host's means, from its reference's row "A Driver messages its steering session", and the steering session's id when the host gives one>
  Team: <the team: lines above, as printed, then the review steps>
  Needs: <as printed>                (only when the batch's playbook gives the role skills or tools)
  Note: <why the CR is with it>
```

The release Driver's block has the same shape with neither `writes:` nor `Team:`.

#### 2b. The stack driver (`take stack`, take-skeleton-Q3)

The stack-driver block has its own shape. It carries the stack rows as `take stack` printed them
above, not the facts of one CR:

```text
stack-driver prompt (no writes: line: this Driver gets none; copy it whole, …):
  chantier stack-driver for the stack of batch batch-23, in the project <root>.
  Read <skill>/references/startup-core.md, … (as in 2a)
  Read <skill>/references/driver.md;
  the project's rules rank above them: run `$CHANTIER rules` first and read what touches your work.
  <the role's contract lines, as printed>   (only when the playbook starts the role as a generic agent)
  CLI ($CHANTIER): <cli_command(repo)> <command> --batch batch-23
  <the stack's chain line and one row per CR, as printed above>
  Steering: the Foreman <the host's means, …>
  Team: <the team: lines, as playbook --batch batch-23 resolves them>
  Needs: <as printed>                (only when the batch's playbook gives the role skills or tools)
  Note: <why the stack is with it>
```

- The stack rows are the lines `stack_lines` returns, the same text `take stack` printed above
  the block, each with the block's two leading spaces.
- `Team:` is filled by the CLI from `playbook --batch <batch>`: the batch's recorded playbook, as
  `team_lines(d.playbook)` prints it for `take <cr>`. The review steps that follow them in the
  template stay a `<…>` for the steering session.

#### 2c. The QA driver (`order qa`, take-skeleton-Q4)

```text
qa-driver prompt (no writes: line: this Driver gets none; copy it whole, …):
  chantier qa-driver for <folder> of batch batch-23, in the project <root>.
  Read <skill>/references/startup-core.md, … (as in 2a)
  Read <skill>/references/driver.md;
  the project's rules rank above them: run `$CHANTIER rules` first and read what touches your work.
  <the role's contract lines, as printed>   (only when the playbook starts the role as a generic agent)
  CLI ($CHANTIER): <cli_command(repo)> <command> --batch batch-23
  QA folder: <folder>; order O-<k>
  default branch: <the project's default branch>
  Steering: the Foreman <the host's means, …>
  Needs: <as printed>                (only when the batch's playbook gives the role skills or tools)
  Note: <the order's --note text>
```

- `<folder>` is the QA folder exactly as the `QA folder:` line of `order qa` prints it, on the
  first line and on the `QA folder:` line, with the order's id. These are the lines `foreman.md`
  names today for this prompt: the card, the CLI, the default branch and the user's note.
- `default branch:` is the project's default branch as the CLI already resolves it
  (`repo.config["default_branch"]`, else `core/git.py`, `default_branch`).
- `Note:` holds the order's `--note` text (`order qa` refuses an empty one), so the QA block
  leaves only the host's means on `Steering:` to fill.
- The block is part of the output the Chief of Staff gets from `order qa`. In Foreman mode the
  Chief of Staff sends the Foreman the order's line and this block together (section 4); in
  direct mode (a paused direct batch, the only one `order qa` accepts) it starts the QA driver
  itself from the block.

#### 2d. Common rules

- **Filled by the CLI:**
  - the first line, from the role's agent file (`Prompt starts with:`), with `<cr>`, `<title>`,
    `<folder>`, `<batch>` and `<root>` filled in as `worker_prompt_lines` does;
  - `<skill>` in both `Read` lines (`skill_dir()`);
  - the card's file name, from the table;
  - the `CLI ($CHANTIER):` value (`cli_command(repo)` plus `<command> --batch <batch>`, as in the
    `cli:` line);
  - on a CR Driver's `writes:` line (take-skeleton-Q2), the absolute `folder:` path and, when
    `archive_path` returns one, `; ` then the archive as an absolute path, the CR's worktree
    joined with the archive path (`<worktree>/<archive path>`, forward slashes, as `folder:`
    prints its path). The `archive:` facts line itself is unchanged;
  - the "who" of `Steering:`: `the Foreman` for a batch whose `steering` is `foreman`, `the Chief
    of Staff` for `direct`;
  - the stack driver's `Team:` lines (2b);
  - `Note:` with the `--note` text of `take`, `take stack` or `order qa` when one is given;
    otherwise the placeholder stays;
  - the `Needs:` line, as `playbook --batch` would print it for the role, when the playbook gives
    the role skills or tools. Otherwise the line is not printed.
- **Left as `<…>` for the steering session:** the host's means on `Steering:` (shared files and the
  CLI name no host tool; the host's reference does), the CR Driver's `Team:` content, the review
  steps after the stack driver's team lines, and `Note:` with no `--note`.
- **Generic agent.** When the batch's playbook starts the Driver role as a generic agent
  (`start: generic`), the block holds that role's contract lines, as `contract_lines` prints them
  for workers today, each with the block's two leading spaces. They go right after the opening
  lines (the first line, the two `Read` lines and the project's rules line) and before
  `CLI ($CHANTIER):`, where `concepts.md`, "Starting an agent" (lines 407-409), puts them. They
  are never printed after the block: copying the block whole, adding no line and dropping none,
  is the whole prompt. When the role runs its own agent file, no contract line is printed.
- **Lines left out per the table:** `writes:` and `Team:` are not printed for a role whose cell
  says `none`. The release and QA Drivers' blocks have neither. The stack driver's has `Team:` and
  no `writes:`.
- **Unchanged:** the facts lines, the workers' opening lines and the `team:` lines that `take`
  prints today (a CR Driver still copies the workers' lines from its own prompt); the stack lines
  `take stack` prints; the order line and `QA folder:` line of `order qa`. `round` and `handoff`
  print no Driver skeleton: a Driver never starts a Driver. `take` stays on the list of commands
  with no ten-line limit (`concepts.md`, line 389); `order qa` joins it if that list would
  otherwise hold it to ten lines.
- A role named in the table with no agent file on the host, or a CR kind no row names, is a CLI
  error (exit 2) that names the missing role or kind and says the plugin's files are out of step.
  It is never a fallback to another role (AGENTS.md, "No fallback"). Nothing is recorded when this
  error fires (no take, no order, no QA folder): check before the state changes.

### 3. How the CLI learns the table (`plugin_files.py`)

The CLI knows no role, so it reads the table from `concepts.md` in the installed skill
(`skill_dir() / "references" / "concepts.md"`), the way it reads the agent files today. Add one
function next to `worker_prompt_lines`, for instance `driver_prompt_lines(host, root, started_by,
batch, steering, body, writes, team, note, resolved)`. It finds the "A Driver's prompt" table,
picks the row whose "Started after" cell matches (`take <cr>` with the CR's kind among the kinds
named, `take stack`, or `order qa`), and builds the block from the lines its caller gives (the CR
facts, the stack rows, or the QA lines). The agent file it reads for the first line is the row's
role on the batch's host (`_agent_files(host)`). `driver.py` calls it from `take` and
`_take_stack`, and `orders.py` from `order` for `qa`; not from `cr_facts` (which `round` and
`handoff` share).

The names above are a suggestion; the behaviour is the spec. Within the 2026-11-14 test budget
(AGENTS.md), parsing the table on each call is acceptable; no cache is needed.

### 4. Cards that start Drivers

- `skills/chantier/references/foreman.md`, "Your means", the `take` bullet (line 169). Replace the
  hand-built rules ("the prompt starts with the role's first line, copied from "Starting an
  agent", unchanged …", "A CR Driver's prompt holds `writes: …`; a stack, release or QA driver
  gets none", "Every Driver's prompt you write … holds the `Steering:` line") with: start the
  Driver from the skeleton `take` (or `take stack`) printed, copied whole, each `<…>` filled in
  (the `Steering:` means from the host's reference); add no `writes:` line the skeleton does not
  print, and drop none it prints; see [concepts](https://github.com/gsemet/chantier/blob/main/skills/chantier/references/concepts.md), "A Driver's prompt". The
  `playbook --batch` agent-and-model sentences stay as they are.
- `foreman.md`, `order qa` bullet (lines 185-191). Replace "copy the first line, `chantier
  qa-driver for <folder> …`, then the card, the CLI, the default branch and the user's note in its
  prompt" with: start the `qa-driver` from the skeleton `order qa` printed, which the Chief of Staff
  sends with the order's line, copied whole, its `Steering:` means filled in. The rest of the
  bullet (the slot, `agents set O-<k>`, `order done`, the ask) stays.
- `skills/chantier/references/chief-of-staff.md`:
  - "The Drivers" (around line 1408): the same sentence as the `take` bullet, for the Drivers the
    Chief of Staff starts in direct mode, and the QA driver from the `order qa` skeleton.
  - Where an order's line is sent to the Foreman (the table row at line 30, "Steering" at line
    934): for `order qa`, send the order's line and the `qa-driver prompt` block it printed,
    together, as printed.
- `skills/chantier/references/driver.md`, lines 73-75: the sentence on a CR Driver's own
  `writes:` line points to [concepts](https://github.com/gsemet/chantier/blob/main/skills/chantier/references/concepts.md), "A Driver's prompt", and says the archive path
  is absolute: "`writes: <CR folder>` (and `; <absolute archive path>` when `take` prints one)"
  (take-skeleton-Q2).
- `skills/chantier/references/hosts/claude-code.md`, "The write guard" (line 494-495): "a CR
  Driver's holds its CR folder, then the absolute archive path when `take` prints one"
  (take-skeleton-Q2). `hosts/copilot.md` changes only if it states the same rule.

No agent file changes (`agents/`, `com.github.copilot/agents/`). Their bodies stay identical
across hosts.

## Decisions carried from `02-answers.md`

- take-skeleton-Q1: `take` prints the whole prompt skeleton for the CR's Driver role: its first
  line, the card to name, and, for a release, stack or QA Driver, no `writes:` line. The skeleton
  is ready to give to the Driver. Carried in sections 1 and 2.
- take-skeleton-Q2: the skeleton prints the archive as an absolute path, `<worktree>/<archive
  path>`; the CLI test checks it; `driver.md` and `hosts/claude-code.md` say "absolute". Carried in
  sections 1, 2d, 4 and Evidence 2.
- take-skeleton-Q3: the stack-driver block has its own shape; it carries the stack rows as printed;
  its `Team:` is filled from `playbook --batch`. Carried in section 2b.
- take-skeleton-Q4: `order qa` also prints the `qa-driver` skeleton. Carried in sections 1, 2c, 3
  and 4.

## Out of scope

- Who chooses the Driver's agent and model. That stays with `playbook --batch`, as today. The
  skeleton is the prompt only.
- The write guard (`hooks/register.tsx`) and its tests. `hooks/` and `types/` are not changed, so
  `just mod` is not needed.
- The workers' opening lines and their prompts.
- The eval kit's audit (`evals/kit/audit.py`, J12). A check that a release, stack or QA Driver's
  prompt holds no `writes:` line is not added here.
- Filling in the host's means on `Steering:` from the CLI.
- A skeleton printed by `status` for an open QA order.

## Evidence

Checks, run by the Driver before the PR (`just check` on the Driver's machine; the CI runs it on
Linux, macOS and Windows):

1. **Structure test** (`skills/chantier/scripts/cli/tests/test_plugin_files.py`, one parametrized
   test). The "A Driver's prompt" table in `concepts.md` parses. Every role in it has an agent
   file on both hosts whose description is `Started by the steering session` and whose first line
   is the one the role's prompt must start with. Every card it names exists under `references/`.
   The kinds `change`, `fix` and `release` are each named exactly once. `take stack` and
   `order qa` are each named once.
2. **CLI test** (`tests/test_cli_runs.py`, extending the existing take and `order qa` runs,
   parametrized over the cases, kept fast):
   - `take CR-101` on a `change` CR prints a `cr-driver prompt` block. Its first line is
     `chantier cr-driver for CR-101 "<title>" of batch …, in the project <root>.`. It has a
     `  writes: <folder>` line with the same path as the `folder:` line. On an external surface
     that prints `archive: in the PR at <path>` (the existing external-surface test), the line is
     `  writes: <folder>; <worktree>/<path>`, and that second path is absolute
     (`Path(...).is_absolute()`) and ends with the `archive:` line's path (take-skeleton-Q2). It
     has a `  Steering: the Foreman` line and a `  Team:` line.
   - `take` on a `release` CR prints a `release-driver prompt (no writes: line …` block with no
     line starting `  writes:` and none starting `  Team:`.
   - `take stack` in a stack batch prints a `stack-driver prompt (no writes: line …` block with no
     `  writes:` line, the stack's chain line and each CR row of the output above it, each with two
     leading spaces, and one `  Team:` line holding the batch's `team:` lines when its playbook
     configures roles (take-skeleton-Q3).
   - `order qa --note "test it"` prints a `qa-driver prompt (no writes: line …` block after its
     `QA folder:` line: its first line names the QA folder as that line prints it, it has a
     `  default branch:` line, `  Note: test it`, and no `  writes:` and no `  Team:` line
     (take-skeleton-Q4).
   - A direct batch prints `  Steering: the Chief of Staff`. A `--note` given to `take` shows on
     `  Note:`.
   - A row whose role has no agent file (the test's own copy of the plugin files, with one file
     removed) is refused with exit 2, and nothing is recorded.
   - `just test` stays within its limit (AGENTS.md: at most 30 s above 18.5 s).
3. **Scenario** (`scenario/run_scenario.py`). After each `take` (`Foreman.take`, around line 476),
   check the printed skeleton: for a target CR of kind `release`, no `  writes:` line in its
   block. For `stack`, no `  writes:` line and the stack rows in the block. For any other CR, one
   `  writes:` line naming the CR's folder, with an absolute archive path when the run prints an
   `archive:` line. After the `order qa` run (around line 6138), the `qa-driver prompt` block has
   no `  writes:` line. The scenario's release runs (`release`, `release_last`,
   `release_on_stack`, …), its stack run and its QA run cover all four. `just scenario` passes
   before the PR (the pipeline's `just scenario (ubuntu-latest)` job, green at the PR's head).
   This change touches the CLI and the cards, so the long gate applies.
4. **Reading proof** for the PR's Deliverables: the output of `take` for a change CR, a release CR,
   `take stack` and `order qa` from the scenario's run, as text.

## Open questions

None. The Chief of Staff settled the last one (2026-11-17): in Foreman mode the Chief of Staff sends
the Foreman the order's line and the `qa-driver prompt` block together (section 4); `status` does
not print the block.
