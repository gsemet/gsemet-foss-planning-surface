# SC09 + SC10: AGENTS.md: roles are data, the CLI advises and refuses; `chantier brief` writes a role's whole start prompt

This CR carries children 9, 10 of the program `simplify-cards-and-prompts` in ONE Driver, ONE PR, in this order, as the owner asked on 2026-11-25 ("regroupe les CR entre elles pour en faire des plus grosses"). Each part below is the full Change Specification of one child, unchanged: do them in order, one after the other, commit by commit. Where a part says "child N's branch", "on child N" or "waits for child N" and child N is another part of this CR, it means the earlier part of this same branch, not another PR. The gates of the parts are all owed, run once at the PR's head (the strictest part decides which long gate). If the context runs short, hand back with the exact state at about 100k tokens: parts done, parts left. The answers of every part are appended to this folder's `02-answers.md`.


---

# PART 1 of 2: SC09: AGENTS.md: roles are data, the CLI advises and refuses

Child 9 of 28 of the program CR `simplify-cards-and-prompts` (its `03-change-spec.md`, "Child 9",
and its `02-answers.md` answers 11 and 17 to 22 rank above this file). One Driver, one PR, in the
running stack batch (batch-31). Code read: `origin/main` at `8a960d34`. The change is one
paragraph of the repository's root `AGENTS.md`; no code, card, test or hook changes.

## Goal

The owner's words (answers 11, 22 F7): the tools this program adds (`brief`, `help --for`, `next`,
`msg steering`, `judge`, `roles.yaml`) would contradict four sentences of `AGENTS.md` as they
stand: "the parent ... names the card in its prompt", "the CLI (`rails.py`) says what it refuses",
"The CLI knows no role", and nothing yet says that the CLI's advice never decides. One child,
before the brief child, rewrites them: roles are data the CLI reads; the CLI advises with `next`,
refuses with its rails, and never decides a merge or a take-back; `judge` only words the ask.
Children 10 to 14 and 18 then cite these sentences instead of each rewording the rule.

## Place in the chain

- **Base:** child 8's branch (`sc08-host-rows-and-proofs`, the CR's recorded `chantier/*`
  branch), the previous CR of the stack. Child 8 adds its own `host` line to `AGENTS.md`'s named
  exceptions (in the long "The CLI's scope" bullet); this child does not touch that line and
  rebases over it with no overlap (the edited paragraph is a different bullet, lines 43 to 49 at
  `8a960d34`).
- **Depends on it:**
  - child 10 (`brief-prompts`) builds on this branch; its own AGENTS.md change (the `brief` line,
    `chantier/briefs/` in the git folder's write list) leaves the role sentences to this child;
  - child 11 states "AGENTS.md: none beyond child 9";
  - child 12 (`next`) and child 14 (`judge`) cite the wording "advises with `next` ... never
    decides a merge or a take-back" and "`judge` only words the ask";
  - child 13 (`msg steering`) and child 18 (`roles.yaml`) rely on "the CLI knows roles only as
    data (`skills/chantier/roles.yaml`, ...)": child 18 adds no AGENTS.md line because of it.
- The wording below is therefore binding for those children: change it only by an answer of the
  owner.

## Decisions carried

| Source | Decision | Here |
| --- | --- | --- |
| Answer 22, F7 | One child before the brief child rewrites the four AGENTS.md sentences: roles are data the CLI reads; the CLI advises with `next`, refuses with rails, never decides a merge or a take-back; `judge` only words the ask | the whole CR |
| Answer 11 (simplify-cards-Q11) | `next` is advice for the choice of the CR and the wording; safety steps are refusals, not advice; the CLI words the ask to the user (the Foreman may add one sentence) | sentences 2 and 4 below |
| Program child 9, Scope | The three "Becomes:" texts and the `judge` sentence; tests reading these sentences updated if any | "What changes" |
| Program child 9, Must not | No other AGENTS.md rule changed; no tool added; no card edited | "Out of scope" |
| Program child 9, Risk | No long gate (docs only); the wording binds every later child | "Gates", "Place in the chain" |
| Answer 22, F20 | The PR states the seconds its tests add to `just test` | "Evidence" |
| Answer 22, F9 | Project roles are a later CR: `roles.yaml` holds the plugin's roles only | the sentence names `skills/chantier/roles.yaml`, no project key |
| Answer 14 / merge rule (answer 22, Q8) | Nothing merges while the owner sleeps; the child is presented as ready | "Gates" |

## What changes

One file: `AGENTS.md` at the repository root. One bullet: the one that starts "A role's contract
lives in `skills/chantier/references/`" (lines 43 to 49 at `8a960d34`).

### Today (verbatim)

```
- A role's contract lives in `skills/chantier/references/` (the cards), never in an agent file
  or in the CLI: the parent that starts an agent names the card in its prompt. A card says what
  the role judges; the CLI (`rails.py`) says what it refuses; a user's project rules rank above
  both. The CLI knows no role; two named exceptions: the cost code knows the two specification
  agents by their agent type (`spec-writer`, `spec-critic`), to put them on the grill line, and the surface
  server knows the board's Griller (`board-griller`), to start it with its brief and read its
  `[griller→board]` line (below).
```

### After (the text to commit)

```
- A role's contract lives in `skills/chantier/references/` (the cards), never in an agent file
  or in the CLI. The CLI reads the roles as data (each role's card, wrapper, first line and kind)
  and prints a role's brief whole: the parent starts an agent with the short prompt `brief`
  prints, which names the brief file holding the card. A card says what the role judges; the CLI
  refuses with its rails (`rails.py`), advises with `next` and its `next:` lines, and never
  decides a merge or a take-back: `judge` only words the ask to the user, the steering session
  decides, and the user's yes merges. A user's project rules rank above both. The CLI knows roles
  only as data (`skills/chantier/roles.yaml`, read by `brief`, `help --for` and `msg steering`);
  two named exceptions: the cost code knows the two specification
  agents by their agent type (`spec-writer`, `spec-critic`), to put them on the grill line, and the surface
  server knows the board's Griller (`board-griller`), to start it with its brief and read its
  `[griller→board]` line (below).
```

How each of the four sentences maps:

1. "the parent that starts an agent names the card in its prompt" becomes "The CLI reads the
   roles as data (each role's card, wrapper, first line and kind) and prints a role's brief
   whole: the parent starts an agent with the short prompt `brief` prints, which names the brief
   file holding the card." The opening clause ("A role's contract lives in ... (the cards), never
   in an agent file or in the CLI") is kept: the program's "a role's contract lives in the cards"
   says the same, and the CLI reading roles as data does not put a contract in it.
2. "A card says what the role judges; the CLI (`rails.py`) says what it refuses" becomes "A card
   says what the role judges; the CLI refuses with its rails (`rails.py`), advises with `next` and
   its `next:` lines, and never decides a merge or a take-back". "A user's project rules rank
   above both" is kept unchanged, as its own sentence.
3. "The CLI knows no role; two named exceptions: ..." becomes "The CLI knows roles only as data
   (`skills/chantier/roles.yaml`, read by `brief`, `help --for` and `msg steering`); two named
   exceptions: ...". The two exceptions (the cost code's `spec-writer` and `spec-critic`, the
   surface server's `board-griller`) are kept word for word.
4. Answer 11, added inside sentence 2: "`judge` only words the ask to the user, the steering
   session decides, and the user's yes merges."

The Driver may re-wrap the lines (the file wraps near 100 columns, and the exception lines are
already longer); it changes no word of the "After" text but by a reply to a Verifier finding that
cites this specification.

### Kept as is, on purpose

- `AGENTS.md`, the surface server's paragraph inside "The CLI's scope": "it takes its dependencies
  like the rest of the CLI and knows no role but the board's Griller" (line 133 at `8a960d34`).
  It describes the surface server, which reads no role data and knows only the board's Griller;
  it agrees with sentence 3 and is another rule (Must not).
- Every other `AGENTS.md` line, child 8's `host` line included.

### Tests

None reads these sentences. Checked on `origin/main`: `git grep -n -i "knows no role\|role's
contract lives\|says what it refuses\|what the role judges" origin/main` finds them only in
`AGENTS.md`, `CONTRIBUTING.md:100` and `:122`, `references/hosts/claude-code.md:630` and four
docstrings in `src/` (`commands/__init__.py`, `driver_prompt.py`, `plugin_files.py`), and no file
under `skills/chantier/scripts/cli/tests/`. The Driver runs the same grep at its base (child 8's
head) and states the result in the PR; it changes no test and adds none (the program asks for
none).

The tests that read the shipped `AGENTS.md` as it ships, at the head under test, must still pass
unchanged; the edited bullet holds none of their phrases:

- `tests/test_board_running_lane.py` ("action `running-batch`", "writes no file in the CR's
  folder");
- `tests/test_gate_refusals.py` ("`chantier gate <cr> scenario`" and the long gate's line);
- `tests/test_launch_modes.py` ("when the session's project is chantier" and the stale-build
  sentence, once);
- `tests/test_board_read_key.py` (no "the board's key", no "revokes the key");
- `tests/test_command_names.py` (no `chantier board` old form).

## Out of scope

- Any other `AGENTS.md` rule, the surface server's "knows no role but the board's Griller"
  included (program, Must not).
- A tool, a command, a flag, `roles.yaml` itself (child 18), `brief` (child 10), `next`
  (child 12), `msg steering` (child 13), `judge` (child 14): this child names them only.
- Any card under `skills/chantier/references/`, `references/hosts/claude-code.md:630` included,
  and the wrappers in `agents/` and `com.github.copilot/agents/` (program, Must not; the card
  rewrite is children 19 to 24).
- The docstrings in `src/` that say "the CLI knows no role" (`commands/__init__.py:14`,
  `driver_prompt.py:149`, `plugin_files.py:174`, `:276`, `:385`): code comments in files that
  children 10 and 18 rewrite when the role data lands.
- `CONTRIBUTING.md:100` ("The CLI knows no role: the cards hold each role's contract, and the
  Foreman and the Drivers write the prompts"): the program scopes this child to `AGENTS.md`
  ("docs only: AGENTS.md"); see open question 2.
- A test that guards the new wording: the program does not ask for one.
- A version change (`just version` only, and not in this child).

## Gates

- **Before the first push:** `just check` in the worktree, at the rebased head it pushes.
  `just eval-dry-run` is not owed (nothing under `src/` or `evals/kit/`). `just mod` is not owed
  (no `hooks/` or `types/` change).
- **Long gate:** none owed for this child's own change: `AGENTS.md` is a docs-only change (program
  Risk; AGENTS.md: "a change to the docs ... alone needs none").
- **Stack's top:** in this stack batch only the CR on top owes the local Windows
  `chantier gate <cr> scenario` run, "a docs-only top included". If this CR is the stack's top
  when it is presented as ready, it owes that run at its head; when child 10 joins on top, the
  run moves to child 10.
- **Merge:** nothing merges while the owner sleeps; the CR is presented as ready, and the owner
  merges, in order, after child 8 (merge rule, answers 14 and 22 Q8).

## Evidence

- The diff: `AGENTS.md` only, one bullet, matching the "After" text above (re-wrapping aside).
  `git diff --stat <base>...HEAD` in the PR shows one file.
- `just check` passes at the pushed head (lint, test, release-notes).
- The grep of "Tests" above, run at the base, and its result in the PR.
- `just test` seconds (F20): the PR's Deliverables state the seconds this child adds, measured
  before (at the base) and after (at the head) on the same machine. Expected: 0 s, since no test
  is added or changed; the two measured durations are given anyway.
- The PR quotes, as the owner's word, to be confirmed at wake:
  - answer 11: "`next` is advice for the choice of the CR and the wording; the safety steps are
    refusals, not advice; the CLI words the ask to the user and the Foreman may add one
    sentence."
  - answer 22, F7: "one child before the brief child rewrites the four AGENTS.md sentences (roles
    are data the CLI reads; the CLI advises with `next`, refuses with rails, never decides a merge
    or a take-back; `judge` only words the ask)."
- The PR's Known gaps name open question 1 (below) while it is unanswered: until children 10 to
  18 land, and until child 24 switches `take`, `round` and `handoff` to `brief`, the new text
  names commands and a file that do not exist yet at this child's head.
- No host or default matrix: the change does not depend on the host or on a configured value.

## Cost

`just test`: +0 s expected. No scenario step. One short Driver round.

## Open questions

1. **An intermediate `main` that names tools not yet there.** Children 1 to 18 may each merge,
   in order, once the owner says so. After this child merges and before children 10 to 18 do,
   `AGENTS.md` names `brief`, `help --for`, `next`, `msg steering`, `judge` and
   `skills/chantier/roles.yaml`, none of which exists yet, and says the parent starts an agent with
   `brief`'s short prompt, while `take`, `round` and `handoff` keep printing the old prompts until
   child 24. An agent that reads `AGENTS.md` on that `main` may run a command that does not exist.
   The program places this child before the brief child (F7) and words the text in the present
   tense. This specification keeps that wording and the program's merge order, with the gap in
   Known gaps. Should the owner rather hold child 9's merge until children 10 to 18 can merge
   with it, or have the sentences worded so they hold at every step (for instance "as each
   lands")?
2. **`CONTRIBUTING.md:100`.** It says "The CLI knows no role: the cards hold each role's contract,
   and the Foreman and the Drivers write the prompts", which this child's sentences 1 and 3
   contradict once the tools land. Align it here (one more docs file, still no long gate), or
   leave it to the swap (child 24) or the read-and-compare review (child 25)? This specification
   leaves it out, as the program scopes the child to `AGENTS.md`.


---

# PART 2 of 2: SC10: `chantier brief` writes a role's whole start prompt

Child 10 of 28 of the program `simplify-cards-and-prompts`. The program's `03-change-spec.md`, its
`02-answers.md` (answers 17-22) and its `work/study-*.md` rank above this specification. Decisions
cited as F1, F10, F19 are the program's findings, carried as the program decided them.

## Goal

An agent of any role starts from one short prompt and one file. The CLI writes that file, the
role's **brief**: its card whole, the floor (the ten rules no role may break), the facts of its
unit, the host rows it needs, and one closing line. The short prompt the parent pastes is the
filled first line, the hook's `writes:` and `worktree:` lines when the role gets them, and
`Read <the brief file> whole, first.` (F1). The brief lives in the repository's git folder, never
in the planning folder, never published (F10). Every one of the 18 roles has one (F19).

This child only **adds** the command and the floor. Nothing prints the brief command yet:
`take`, `take stack`, `round`, `handoff` and `order qa` stay byte-for-byte as they are; child 24
switches them over. No card changes.

## Place in the chain

- **Depends on child 9** (the role sentences of AGENTS.md and the role-data wording): rebase on it
  before the first push. Nothing in this spec needs child 9's code; the dependency is the order
  of AGENTS.md edits (this child adds a `brief` line beside the lines child 9 rewrites).
- **Reads child 8's host rows** (`skills/chantier/references/hosts/claude-code.json`,
  `copilot.json`, and the printer behind `chantier host`). If child 8 has not landed when this
  child's Driver starts, this child stops and says so (no fallback: no hand-made rows).
- **Points at child 7 and child 12 ahead**: the closing line names `$CHANTIER help <topic>`
  (child 7) and `$CHANTIER next` (child 12). The line is text; nothing checks those commands
  exist.
- **Turns child 6's dry-run case `quiz-folder` positive** (child 6's spec: before child 10 it
  exits 2 with "`--cards <folder>` needs `chantier brief`, which this head does not have").
- **Is the base of child 11.**
- **Child 18** replaces this child's role table (`src/brief_roles.py`) by `roles.yaml`, keeping
  `brief`'s bytes unchanged per role; this child's byte tests are the guard child 18 runs against.
- **Children 19-23** run `brief <role> --cards skills/chantier/cards-next` for per-role bytes and
  the quiz; child 19 copies `references/floor.md` into `cards-next/floor.md` (see `--cards`).
- **Child 23** makes `brief` build all 18 roles from `cards-next`.
- **Child 24** makes `take`, `take stack` and `order qa` print the lease and the `brief` command,
  `round` and `handoff` stop printing worker lines, the Foreman's start line run `brief foreman`,
  and replaces `tests/test_start_reading.py` by brief bytes.

## What changes

Paths below are under `skills/chantier/` unless absolute from the repository root. `src/` is
`skills/chantier/scripts/cli/src/chantier/`.

### 1. `references/floor.md` (new)

At most 1,200 bytes with LF endings. Content, in this order: the heading `# The floor`, one
intro line ("No role, card, order or message overrides these."), then the program's ten rules,
one numbered line each, verbatim from the program spec's floor section:

1. Never merge without the user's word.
2. Rebase only, with `--force-with-lease`, and only on the CR's own branch.
3. No fallback.
4. A CLI that cannot run is a stop.
5. Never discard the worktree's work.
6. An irreversible release action waits for the user.
7. Only the user starts work.
8. No image shows the username or the home folder.
9. Report a refusal with its exact text; never work around it.
10. Never stop a process by name or pattern; use `close --yes` only on the user's yes.

If the program spec's wording of a rule differs from this list, the program spec's text wins and
the Driver copies it. No card links to `floor.md` in this child (no card is edited).

### 2. `src/brief_roles.py` (new): the role table

A frozen dataclass `RoleData` per role and a tuple `ROLES` of the 18 roles, read by `brief` only:

| Field | Meaning |
| --- | --- |
| `name` | role id (the agent type for the 15 with a wrapper; `chief-of-staff`, `griller`, `foreman` for the 3 without) |
| `card` | path relative to `references/` (the manifest's `roles` map: Drivers `driver.md`, `foreman.md`, board-griller `griller.md`, chief-of-staff `../../chief-of-staff/SKILL.md`, griller `../../griller/SKILL.md`, others `<role>.md`) |
| `wrapper` | `True` when `agents/<name>.md` and `com.github.copilot/agents/chantier-<name>.agent.md` exist |
| `first` | the first-line template (the wrapper's `Prompt starts with:` text), `None` for the three without a wrapper |
| `unit` | `cr`, `order`, `stack`, `folder` or `none` |
| `writes` | `none`, `worktree` (`writes: <wt>; <CR folder>`) or `cr-folder` (`writes: <CR folder>`, with the archive path as `driver_table()` gives it) |
| `rows` | the capability ids of the host rows it gets (section 5) |

Units, by role:

| Unit | Roles |
| --- | --- |
| CR id | cr-driver, release-driver, coder, conflict-resolver, debugger, inspector, investigator, verifier |
| `O-k` (an order id) | qa-driver |
| `stack` | stack-driver |
| CR folder in `1-inbox`, `2-backlog/P1..P4` or `3-ready` | spec-writer, spec-critic, board-griller |
| none | retro-critic, demo-explorer, chief-of-staff, griller, foreman |

The Drivers' `card`, `writes`, team and rewrites come from `driver_prompt.driver_table()`, not a
second copy: `brief_roles` reads it for the four Drivers. A test (section 8) checks the table
against the shipped wrappers and `references/startup-manifest.json` so the two cannot drift. The
CLI keeps knowing no role outside this table and the existing named exceptions; the table is
data `brief` prints, not a rule the CLI applies (AGENTS.md line, section 9).

### 3. `src/declare/brief.py` and `src/commands/brief.py` (new): the command

```
chantier brief <role> [<unit>] [--lease N] [--epoch N] [--cards <folder>]
```

Declared with `registry.add_command(sub, "brief", "commands.brief:brief", HELP, BATCH_EPOCH)`
(so `--batch` comes with the scope); register the module in `cli.py`'s declare import list. Its
own `--lease` argument (not `registry.add_lease`, whose help says the lease renews: `brief`
never renews).

Behaviour:

- **Read-only on the record and the planning folder.** `Repo.find(cwd, project, readonly=True)`
  as `access.py` does; reads with `read_batch` and `find_cr_batch`; takes no lifecycle lock;
  records nothing; appends no journal line; prints no watcher line. Its one write is the brief
  file (below).
- **Role**: one of the 18 names; any other exits 2 with `unknown role '<x>'; roles: <list>`.
- **Unit**: as the table above. A missing unit for a role that has one gives the **role-only
  brief**: card, floor, the facts reduced to `CLI ($CHANTIER): …` and `Repository: <root>`,
  host rows, closing line; no `writes:` or `worktree:` line in the short prompt. A unit given to a
  role whose unit is `none` exits 2. A CR id not in the batch, an `O-k` not an open QA order, a
  folder outside `1-inbox`/`2-backlog`/`3-ready` each exits 2 with one line naming it.
- **`--lease N`**: required with a unit for the four Drivers (cr-driver, release-driver: the
  CR's lease; stack-driver: the stack's; qa-driver: the order's). Checked read-only with
  `leases.lease_of(record, unit)`: absent or different exits 2 with
  `lease <N> is not <unit>'s live lease`; never renewed, never taken. Refused (exit 2) for any
  other role.
- **`--epoch N`**: accepted for `foreman` and `chief-of-staff` only; any other role exits 2.
- **Host**: the batch record's host when there is a batch, else `plugin_files.detect_host()`.
- **`--cards <folder>`**: the card is read from `<folder>/<basename of the role's card>` (so
  `<folder>/driver.md` for a Driver, `<folder>/SKILL.md` is **not** used: chief-of-staff and
  griller read `<folder>/chief-of-staff.md` and `<folder>/griller-skill.md`, since `griller.md`
  is board-griller's card) and the floor from
  `<folder>/floor.md`; a missing file exits 2 naming its path. The role table, the Driver table,
  the wrappers' first lines and the host rows always come from the shipped files. (Open
  question Q1 asks the owner to confirm this naming for the two skill roles.)

#### The brief file

Path: `<repo.git_dir>/chantier/briefs/<batch or "none">/<unit or "none">-<role>.md`, where a
folder unit is its folder's name and `O-k` and `stack` are written as such. `repo.git_dir` is the
git common dir, the same folder `hub/state.py` uses (the project's in-project mode, the surface's
in external mode). Written with `core/files.write_file` (atomic rename, UTF-8, LF). It is
overwritten at each run.

Content, in this order, each part separated by one blank line:

1. The card, whole, as its bytes are (first, so a reader that stops early has read it).
2. `=== floor` then `floor.md`'s body.
3. `=== facts` then the facts lines (below).
4. `=== host rows: <host>` then the role's rows, printed by child 8's printer for that host.
5. The closing line: ``$CHANTIER next` says what is due; `$CHANTIER help <topic>` when a line
   names one.``

**Byte-stable**: two runs on the same state give the same bytes. No clock-relative value (no
"in 12 min", no age, no timestamp other than those stored in the record) appears in the file;
lines of the reused builders that hold such a value are left out of the brief, and the test
names each one left out.

#### The facts, per role

Reuse the existing builders; extract code, never copy it:

- **cr-driver, release-driver**: `driver_prompt.driver_prompt_lines(row, d, block)` with the
  block `driver._cr_driver_block(repo, batch, c, facts)` builds, lease text from
  `leases.driver_line`, **minus** the heading, the first line, the `Read …startup-core…` line,
  the `Card:` line and the Note. The `Steering:` placeholder becomes
  `Steering: <who> (host means: the host rows below)`. `Team:` and its `<review steps>`
  placeholder stay as `take` prints them.
- **stack-driver, qa-driver**: the same, with the block builders **extracted** from
  `driver._take_stack` (stack lines, timing lines, `lease: stack N (…)`) and from
  `orders._qa_skeleton` (`QA folder: …; order O-k`, `default branch: …`) into functions both the
  old caller and `brief` call. `take stack` and `order qa` print the same bytes as before (the
  existing tests and the scenario prove it).
- **The six workers**: the `facts.cr_facts(...)` lines before the worker blocks (title, `cli:`,
  `cards:`, project instructions, specification, folder, scratch, `worktree: …`, PR, status,
  gate), the role's own `plugin_files.contract_lines` when the configured agent is generic, and
  the line `writes: <worktree>; <CR folder>`. Not the worker prompt lines of other roles.
- **spec-writer, spec-critic, board-griller**: `CLI ($CHANTIER): …`, `Repository: <root>`,
  `CR folder: <abs path>`, and `Specification: <abs 03-change-spec.md>` when it exists.
- **retro-critic, demo-explorer**: CLI, Repository, and the batch when `--batch` names one.
- **foreman**: CLI with `--batch <b>`, Repository, batch, epoch (from `--epoch`, else the
  record's), the team and timing lines, the `Needs` line, as step 4 of
  `chief-of-staff-batch-start.md` lists them.
- **chief-of-staff, griller**: from `plugin_files.chief_prompt_lines` the CLI, Repository,
  planning folder, project instructions and host lines.

#### The short prompt (stdout, nothing else)

1. The filled first line (the wrapper's template with `<cr>`, `"<title>"`, `<batch>`,
   `<folder>`, `<root>` filled). None for the three roles without a wrapper.
2. `writes: <abs paths separated by "; ">` **at column 0**, when the role's `writes` is not
   `none` and a unit is given (`hooks/register.tsx`'s `writesOf` reads `/^writes:(.*)$/m`).
3. The exact `worktree: <wt> branch <b> <base>` line of `cr_facts`, when the unit has one
   (`worktreeOf` reads `/^\s*worktree:\s+(.+?)\s+branch\s/m`), including its
   `; not created yet…` suffix when that is what `cr_facts` prints.
4. `Read <abs brief path> whole, first.`

The first line keeps `, in the project <root>.`, which `rootOf` reads. Exit 0.

### 4. `driver_prompt.py`, `driver.py`, `orders.py`, `facts.py`, `plugin_files.py`

Only extractions of the block builders named above, with no change to any output. No new
behaviour in `take`, `take stack`, `round`, `handoff`, `handback` or `order qa`.

### 5. Host rows per role

The capability ids are child 8's, read from `references/hosts/claude-code.json` and
`copilot.json`:

| Roles | Rows |
| --- | --- |
| chief-of-staff, foreman | all rows |
| griller | start a child, ending, compacting, reloading |
| cr-driver, release-driver, stack-driver, qa-driver | message steering, start a child, ending, compacting, write guard |
| the six workers, spec-writer, spec-critic, retro-critic, demo-explorer | ending |
| board-griller | none (the part is printed with the single line `none`) |

A row marked `untested` keeps its mark as child 8 prints it.

## Out of scope

- Any change to what `take`, `take stack`, `round`, `handoff`, `handback` or `order qa` print
  (child 24).
- Any edit of an existing card, wrapper or `startup-manifest.json` (children 19-23; this child
  reads them).
- `roles.yaml` (child 18), `help <topic>` (child 7), `next` (child 12), the host files (child 8).
- Any change to the hook's logic in `hooks/register.tsx` (only a test case is added).
- Writing a brief anywhere in the planning folder; publishing or cleaning briefs (Q3).
- Making the CLI read `startup-manifest.json` at run time beyond the check in section 8.

## Acceptance evidence

All checks read the shipped files from the repository at the head under test (cards, wrappers,
`floor.md`, the host JSON files, `hooks/register.tsx`); a prepared text is used only for the
refusal of a missing `--cards` file, paired with the shipped-folder case.

1. **`tests/test_brief.py` (new)**, parametrized over the 18 roles x 2 hosts (`CHANTIER_HOST`
   `claude` and `copilot`), on the `world`/`stack_world` fixtures (a batch with a taken change
   CR, a release CR, a stack, an open QA order, a CR folder in `3-ready`):
   - the file's path is under `repo.git_dir/chantier/briefs/`, and a snapshot of the planning
     folder (names, sizes, bytes) is unchanged by the run;
   - the file starts with the shipped card's bytes and holds `floor.md`'s body exactly once;
   - two runs give the same bytes;
   - the short prompt's first line equals the wrapper's `Prompt starts with:` template, filled
     (both hosts' wrappers), and is absent for the three roles without one;
   - the `writesOf` and `worktreeOf` regexes, extracted by the test from the shipped
     `hooks/register.tsx`, give on the short prompt the same paths as on `take`'s skeleton with
     its indent removed (cr-driver) and on `cr_facts`' "worker writes line" (workers);
   - for cr-driver, release-driver, stack-driver and qa-driver, the facts part equals the lines
     `take` / `take stack` / `order qa` print, minus the lines the spec removes (named in the test);
   - each role's `rows` ids exist in both host JSON files;
   - the role table matches the shipped wrappers (existence, first line, "Your card is") and
     the manifest's `roles` map;
   - `floor.md` is at most 1,200 bytes, LF only, and holds the ten rule lines;
   - refusals exit 2 with their line: unknown role, unit on a no-unit role, wrong lease,
     `--lease` on a non-Driver, `--epoch` on a role other than foreman and chief-of-staff,
     missing `--cards` file (prepared folder), CR folder outside the three folders;
   - `--cards skills/chantier/references` gives the same bytes as no `--cards` for every role
     whose card's basename is in that folder.
   Seconds added to `just test`: target about 5 s on the user's Windows machine; the Driver
   measures before and after and states both numbers in the PR (the AGENTS.md budget is 30 s
   above 18.5 s).
2. **`hooks/register.test.tsx`**: one case feeds `spawn($, prompt, {cwd})` the short prompt of
   `brief cr-driver` (built from the shipped first-line template, a column-0 `writes:` line and
   a `worktree:` line, as the test's WRITES/TREE_LINE constants do) and asserts the agent is
   write-guarded to those paths and starts in its worktree. `just mod` is owed (a change under
   `hooks/`).
3. **Scenario**: in `scenario/run_scenario.py`, in `scenario()` (unit `parallel`), right after
   the first change-CR `Foreman.take`, a helper `check_brief_driver` runs
   `brief cr-driver <cr> --lease <n>` (with `World.chantier(..., lease=False)` so the lease is
   not added twice), checks the four short-prompt lines and the file's location under the git
   folder, and the Driver of that CR is started from that short prompt. One Coverage bullet in
   `scenario/README.md`: "`brief` writes a Driver's brief in the git folder and its short prompt
   starts the Driver (unit: parallel)" (`test_scenario_coverage.py` requires the `(unit: …)`).
4. **Eval dry run**: child 6's case `quiz-folder` becomes positive: `brief coder --cards
   skills/chantier/references` on the repository root, boot text read from the file the last
   line names, exit 0. If `--project <repo root>` fails in `Repo.find` for the quiz's call, the
   Driver adjusts the quiz's call and the PR says how. `just eval-dry-run` is owed (a change
   under `src/` and `evals/kit/`).
5. **Host and default matrix** (one line per cell):
   - claude, shipped defaults: briefs for 18 roles; the `writes:` line guards through the hook
     (test 2).
   - copilot, shipped defaults: briefs for 18 roles; rows marked untested as child 8 prints
     them; Copilot has no hook, so the `writes:` line is inert there; unproved in a real Copilot
     session.
   - claude, configured agent for a role: the worker's brief carries its contract lines (test 1
     with a configured generic agent).
   - copilot, configured: the same facts; unproved in a real session.
6. **Gates**: `just check`; `just eval-dry-run`; `just mod`; the long gate `just scenario
   (ubuntu-latest)` green at the PR's head; the local `chantier gate <cr> scenario` per the
   batch's shape (AGENTS.md).

## AGENTS.md change

- In the write list's git-folder sentence ("…in the repository's git folder
  (`chantier/server.json`, …)"), add: "and the role briefs `brief` writes
  (`chantier/briefs/<batch>/<unit>-<role>.md`), overwritten at each run, never published".
- A named-exception line beside `access`: "`brief`: writes one role's start brief (its card,
  the floor, its unit's facts, its host rows) in the git folder and prints the short prompt that
  points at it; it reads the record and the planning folder only and records nothing; built on
  the user's answer simplify-cards-Q22 (F1, F10, F19) and the measured start readings (a Driver
  44 KB, the Foreman 144 KB)." The line names no roles and no `roles.yaml` (child 9 owns the
  role sentences).
- `docs/planning-folder.md`, beside its `access` mention: one line that `brief` writes in the
  git folder, not the planning folder.

## Open questions

- **Q1 (`--cards` naming for the two skill roles)**: with `--cards <folder>`, chief-of-staff and
  griller have no card in `references/` (their cards are the two skills' `SKILL.md`), and
  `griller.md` there is board-griller's card. Default specified: `<folder>/chief-of-staff.md`
  and `<folder>/griller-skill.md`; children 19-23 name their files so. Confirm or choose.
- **Q2 (path collisions on a shared surface)**: in external mode the git folder is the
  surface's, so two projects with the same batch name and CR id write the same brief path.
  Default proposed: add the project's name as a first folder
  (`chantier/briefs/<project>/<batch>/…`). Confirm.
- **Q3 (briefs pile up)**: the briefs stay in the git folder after a batch. Default: never
  cleaned by chantier (the batch's end cleanup is a named git exception and is not widened).
  Confirm, or ask that the end cleanup remove the batch's brief folder.
- **Q4 (through a profile)**: `brief` run through a profile's `cli.run` writes the file on the
  server's machine and prints a path there, unreadable by a local agent. Default: allowed like any
  other command (the paths are the server's, as for worktrees). Confirm, or refuse `brief`
  through a profile like `gate`.

