# SC24: Swap in the new cards; remove the old set

Child 24 of 28 of the program `simplify-cards-and-prompts`. These rank above this specification,
in this order: the program's `03-change-spec.md`, its `02-answers.md` (answers 17 to 22) and its
`work/study-*.md`. Short ids (F2, F18, F19, Q4, ...) are the program's findings and questions, as
the Chief of Staff settled them in answer 22. The owner confirms answer 22 when they wake; this
child needs nothing beyond it.

Issue: none (a child of the program; no tracker issue).

## Goal

This child is the swap the program calls "the highest risk" (answers 14 and 17; F2, F18, F19).
Children 19 to 23 wrote the new card set, unloaded, in `skills/chantier/cards-next/`. In one PR,
this child:

- makes that set the only one: `cards-next/` becomes `references/`, and the old files go;
- switches every CLI line, hook message, wrapper sentence, test and doc that names an old file;
- makes `take`, `take stack` and `order qa` hand the Driver's start to `brief`;
- adds the switched-lines test (F18), so that a stale card name cannot come back.

After this child, every role starts from `chantier brief <role>` (F19). There is no `cards:`
switch and no second card set; a rollback is a git revert (answer 14).

## Place in the chain

- **Base: child 23's branch** (`sc23-cards-host-and-shared`, CR-509), in the batch's single stack.
  The Driver rebases on it before the first push. Relied on below it:
  - child 6 (CR-492): `just quiz <role> --cards <folder|ref> --against <baseline>`, the baseline,
    and the rule that the quiz builds every boot from `brief` once the startup manifest is gone;
  - child 7 (CR-493): `references/topics.json`, `load_topics`, `section`, `chantier help`;
  - child 8 (CR-494): `references/hosts/*.json`, `src/host_rows.py`, `docs/proofs/`;
  - child 10 (CR-496): `chantier brief`, the brief file, the short prompt, `references/floor.md`,
    `tests/test_brief.py`;
  - child 17 (CR-503): the launcher `skills/chantier/scripts/chantier.py`, `launch.launcher_line`,
    `launch.launcher_rule`;
  - child 18 (CR-504): `skills/chantier/roles.yaml`, `src/roles_data.py`,
    `scripts/roles_check.py` (`just roles`);
  - children 19 to 23 (CR-505 to CR-509): every file of `cards-next/`, and their inventories
    `<their CR folder>/evidence/cards-inventory-<family>.md`.

  If any of these is missing at the base, the Driver stops and says so. Examples: `brief` has no
  `--cards`; `roles.yaml` is absent; `cards-next/floor.md`, `cards-next/topics.json` or one of
  `cards-next/skills/*-SKILL.md` is absent. There is no stand-in. Child 17 is the one named
  exception (decision D9).
- **Depended on by:** children 25 to 28, above it in the stack:
  - child 25 re-reads the set after the swap;
  - child 26 turns this child's file-and-heading pins into rule ids and freezes the sizes it reached;
  - child 28 runs the real campaign on it.
- **Merge:** with children 19 to 28, as one unit, after child 28's campaign (the program's merge
  rule; F11).

## Decisions carried

| Source | Decision | Where here |
| --- | --- | --- |
| Answer 14 (Q16) | One card set. The old files are removed in this PR, with no `cards:` switch. A rollback is a git revert | sections 1 and 2 |
| Answers 17 and 18 | Total rewrite in one pass; the review is child 25's | out of scope |
| Answer 15 (Q14) | A rule lives in one place. A piece is loaded at its moment | D2, D3; section 4 |
| Answer 16 (Q13) | Trial history leaves the cards: stories go to `docs/proofs/` or `docs/incidents.md` | section 8 |
| Answer 22, F2 | Children 19 to 23 write unloaded; child 24 swaps | the whole child |
| Answer 22, F4 | Quiz pass rule: no case scores 0 of 3 that the old cards passed. The spend plan is printed first | evidence 6 |
| Answer 22, F6 | Handed back validated, with the Known gap "real run not done (child 28)" | Handback |
| Answer 22, F11 | A typed merge wait on child 28's PR | Handback |
| Answer 22, F17 | An unproved claim is marked "unproved" | section 5; matrix |
| Answer 22, F18 | Every CLI line that names a removed card is switched, with a test | sections 3 and 6 |
| Answer 22, F19 | The three roles with no parent (Chief of Staff, Griller, Foreman) boot by running `brief <role>` | sections 2, 3.4 and 4 |
| Answer 22, F20 | The seconds added to `just test` are stated | evidence 9 |
| Answer 22, Q4 | A file above its target is listed in Known gaps with its size; only the owner raises a target | evidence 7 |
| Program, child 24 | Scope, depends on 23, evidence, must-nots, risk, no AGENTS.md change | the whole specification |
| Program, pending item `driver-checkpoint-and-a-ready-restart-br` | "Child 10 absorbs the brief file; child 24 makes `take` print it" | section 3.1 |
| Program, pending item `driver-context-second-cut` | Absorbed by children 10, 20 and 24: the Driver's start becomes its brief | section 3.1 |
| `02-answers.md` of this CR | Specified from the program. No separate critic. Destination: running batch batch-31 | this specification as written |

Decisions this specification takes, where the program leaves the means open:

- **D1. `take`, `take stack` and `order qa` print the `brief` command, not the brief.** In place
  of the Driver's prompt skeleton, they print the lease line, then one line holding the exact
  command: `brief: $CHANTIER brief <role> <unit> --lease <n> --batch <b>`, with every value filled.
  The steering session runs it and passes its stdout, unchanged, as the Driver's whole prompt.
  `take` itself writes no brief file, so AGENTS.md's sentence on the briefs ("the role briefs
  `brief` writes") stays true. This follows the program's words "print the lease and the `brief`
  command". Open question 1 offers the other reading.
- **D2. One source for a role's card: `roles.yaml`.** The Driver table in `concepts.md`
  (`### A Driver's prompt`) keeps its columns, because `driver_row` reads them. Its `Card` cells
  become each Driver's own file (`cr-driver.md`, `release-driver.md`, `stack-driver.md`,
  `qa-driver.md`). A test asserts that each cell equals `roles.yaml`'s `card` for that role. The
  CLI reads the card from `roles.yaml` only; `driver_prompt_lines` no longer prints a `Card:` line.
- **D3. Worker starts go through `brief`.** `cr_facts` drops the workers' opening lines and the
  "worker writes line", because each worker's short prompt carries its own `writes:` line. In their
  place it prints one line naming the command:
  `workers: $CHANTIER brief <role> <cr> --batch <b> (roles: <names>)`. The names are the
  `roles.yaml` roles whose `started_by` is a Driver, in file order.
- **D4. The launcher.** Child 17 left two choices to this child. On both, this child does the same
  thing:
  - `plugin_files.cli_command` prints the launcher form (`launch.launcher_line(<plugin root>)`,
    with `--project` when the planning is external), so the `cli:` fact, the briefs and the
    `SKILL.md` texts type one form;
  - the old forms' allow rules (dev, sync, check, plugin) stay in `RECOMMENDED_ALLOW` and in the
    P10 samples, because the hub, the watcher and a user's existing settings may still type them.
    Their removal is a later CR's.
  - Child 17's open question on the launcher's overhead is still open. This child switches
    whatever the figure, as child 17's specification says, and reports the figure.
- **D5. Historical records keep their words.** In `docs/release-notes/**` and `evals/results/**`, a
  relative link to a removed file becomes a link to the same file at the last released tag before
  the swap (`https://github.com/gsemet/chantier/blob/v<X.Y.Z>/<path>`). The v0.13.0 release notes
  already do this. Their sentences are not reworded.
- **D6. Wrapper sentences that name the startup core change.** Each wrapper body today says "Read
  the startup core first, and your card's `## Startup core` section when it has one". The program
  removes the startup core, so that sentence names a removed file (F18). It changes on both hosts,
  identically, beside the first-line and card-path edits that `just roles` checks (section 2).
- **D7. The board Griller's fixed brief keeps its shape.** `src/board/griller.py`'s `BRIEF` keeps
  naming the Griller card's section "Started from the board". It drops the host-card line. It adds
  no file, so AGENTS.md's description ("a fixed brief that names the Griller card, the CR's folder
  and the CLI") stays true. Open question 2 asks whether it should also name the floor.
- **D8. Defaults of the siblings' open questions, applied here unless the owner answered them
  before this child starts.** Where the owner answered otherwise, the Driver applies the answer,
  and the PR's Autonomous decisions name it.
  - **sc10-Q1:** the skill roles' cards are `chief-of-staff.md` and `griller-skill.md`.
  - **sc19-Q1:** the board Griller's brief bytes are reported as they are. Child 22 already split
    the files: `griller.md` holds only the board section.
  - **sc20-Q1:** the staging folders end here, because `roles.yaml` now names each Driver's own
    card.
  - **sc20-Q2:** a new worktree for each release attempt, no `reset --hard`.
  - **sc21-Q1:** the stack line as child 21 worded it.
  - **sc22-Q2:** no CLI change. The Chief of Staff's card runs `brief foreman --epoch <n>` in
    direct mode. If the owner chose the alternative, `brief chief-of-staff --epoch <n>` on a direct
    batch appends `=== foreman`, then the Foreman's card and facts, before the floor, and
    `tests/test_brief.py` gains that case.
  - **sc09-Q2:** `CONTRIBUTING.md:100` is aligned here, as part of the docs fixes.
- **D9. If child 17 handed back blocked**, or its PR's Known gaps say "the launcher leaves the CLI
  running after its stop on <system>":
  - child 23's `SKILL.md` texts keep today's `$CHANTIER` paragraph (child 23's fallback text),
    and those texts are copied as they are;
  - `cli_command` is unchanged;
  - no launcher row is added to P10;
  - the PR's Known gaps say "launcher not switched: <reason>".

  Child 17's specification says the cards must not switch while that gap stands.

## Hand-over checklist

Every note that a sibling specification leaves to child 24, gathered in one list. The PR's
Internal references reproduce this list, ticking each item with the commit that does it.

| # | From | What child 24 does | Here |
| --- | --- | --- | --- |
| 1 | sc06 (CR-492) | After the swap, the quiz builds every boot from `brief` (manifest absent). The dry-run case that walks the old manifest and checks it against `test_start_reading.py`'s `AFTER` table becomes a check of `brief`'s boot. `--cards <ref>` of a pre-swap head (whose tree holds the manifest) keeps working for child 28's comparison | section 7; evidence 6 |
| 2 | sc06 | Run `just quiz` on every role with `brief`'s output, against child 6's baseline | evidence 6 |
| 3 | sc07 (CR-493) | Swap `cards-next/topics.json` into `references/topics.json`; every CLI `help <name>` still resolves; docs links fixed | sections 1 and 8; evidence 4 |
| 4 | sc08 (CR-494) | The host cards' history leaves the cards: what child 23 did not carry goes to `docs/proofs/` (already) or `docs/incidents.md`; the host topics link `docs/proofs/` | sections 1 and 8 |
| 5 | sc09 (CR-495) | AGENTS.md's role sentences, ahead of the code since child 9, become true here (`take`, `round`, `handoff` switch to `brief`). `CONTRIBUTING.md:100` is aligned | sections 3 and 8 |
| 6 | sc10 (CR-496) | `take`, `take stack` and `order qa` print the lease and the `brief` command. `round` and `handoff` drop the workers' opening lines. The Foreman's start runs `brief foreman` | sections 3.1 to 3.4 |
| 7 | sc10 | `tests/test_start_reading.py` is replaced by a per-role test of `brief`'s bytes. `test_brief.py`'s check against `startup-manifest.json` goes | section 6 |
| 8 | sc10 | `driver_prompt_lines` loses its heading, `Read …startup-core…`, `Card:` and `Note` lines where `brief` already strips them (one builder, no strip list left) | section 3.1 |
| 9 | sc15 (CR-501) | `foreman-conflict.md` is removed with the old set | section 1 |
| 10 | sc04 (CR-490) | The hook's reload message changes (in the `reloadLine` function, apart from child 4's scratch-write code) | section 5 |
| 11 | sc17 (CR-503) | One `SAMPLES` row `("batch", "any", f"{launcher_line(<plugin root>)} status", launcher_rule(<plugin root>))`, filled by `fill_rule` and `fill_sample` | section 3.6 |
| 12 | sc17 | The launcher's line in `hosts/claude-code.md`'s allow table and JSON block. `host-allow-rules` drops "unproved" for it | section 3.6 |
| 13 | sc17 | `permissions.py`: a broad `uv run --script * *` in `PROBES` reads "replaced by" the launcher's rule; `_stale` learns the launcher form | section 3.6 |
| 14 | sc17 | Old forms' rules kept or dropped; `cli_command`'s form; no switch while a process is left | D4, D9 |
| 15 | sc18 (CR-504) | Edit `roles.yaml`'s `card`, `first` and `reply` together with the wrappers; `just roles` passes; its checks 7 and 8 read the swapped `references/` | section 2 |
| 16 | sc19 (CR-505) | `griller.md` holds the board section; `test_command_names.py` now scans the moved folder (no `chantier board` there); the `MOVED_OUT` phrase check is converted | sections 1 and 6 |
| 17 | sc19 | Board Griller's brief bytes reported (sc19-Q1) | D8; evidence 7 |
| 18 | sc20 (CR-506) | Each Driver role points at its own card (`cr-driver.md`, `release-driver.md`, `stack-driver.md`, `qa-driver.md`); the staging folders end; topic names the CLI prints are kept | D2; section 2 |
| 19 | sc21 (CR-507) | `stack_shape.shape_line()` drops its `rules: …/foreman-stack.md` and prints ``shape: stack: read `$CHANTIER help stack` now and after each compaction``, in `brief foreman` and `status --refresh` | section 3.5 |
| 20 | sc21 | Convert `test_came_back.py`, `test_stack_shape.py`, `test_reload_rules.py`, `test_role_cards_split.py`, `test_startup_manifest.py`, `test_stack_chain_cards.py`, `test_rebase_rules.py`, `test_release_tag.py` and `moved_rules.tsv` | section 6 |
| 21 | sc22 (CR-508) | `roles.yaml`: `griller` → `griller-skill.md`, `chief-of-staff` → `chief-of-staff.md`; `griller.py`'s `BRIEF` names `griller.md`, "Started from the board"; no `session-start*.md` and no `titles.md` stays | sections 1, 2 and 3.7 |
| 22 | sc22 | sc22-Q2 default (no CLI change) | D8 |
| 23 | sc23 (CR-509) | Copy `cards-next/skills/<skill>-SKILL.md` to `skills/<skill>/SKILL.md`; check its `chantier-version:` line with `scripts/version.py` | section 4 |
| 24 | sc23 | The stories with inventory home `incidents file` (all five inventories) go to `docs/incidents.md` | section 8 |
| 25 | sc23 | `concepts.md`'s Driver table and `"Change Request"`, `hosts/*.json`, `topics.json` and the allow block are read by the CLI and tests after the swap: each is checked at this head | evidence 3, 4 and 5 |

## What changes

Paths are from the repository root. `src/` is `skills/chantier/scripts/cli/src/chantier/`;
`tests/` is `skills/chantier/scripts/cli/tests/`. Line numbers are from `origin/main` 8a960d34.
The Driver finds each line again at the base, where children 1 to 23 may have moved it.

### 1. The swap of the card files

- `git rm -r skills/chantier/references`, then `git mv skills/chantier/cards-next
  skills/chantier/references`, in one commit. The two are one step: no commit holds both sets or
  neither set.
- Leaves nothing behind:
  - **`cards-next/skills/`** is not kept under `references/`: its four files go to the four
    `SKILL.md` (section 4), and the folder is removed.
  - **`cards-next/`** does not exist at head.
- **Removed, among the old files** (the program's list, and every old file that child 23's
  completeness table marks "not carried"):
  - `startup-manifest.json`, `startup-core.md`, `role-core.md`, `host-core-claude-code.md`,
    `host-core-copilot.md`, `reload-rules.md`;
  - the 32 pieces, among them the nine `chief-of-staff-*.md`, the seven `driver-*.md`, the eight
    `foreman-*.md` (with `foreman-conflict.md`), the four `release-driver-*.md` and the four
    `stack-driver-*.md`;
  - `session-start.md`, `session-start-chief-of-staff.md`, `session-start-griller.md`,
    `titles.md` (child 22);
  - `driver.md`, which is replaced by the four Driver cards (child 20);
  - `hosts/copilot.md`, unless child 23 carried it.

  The PR lists every removed path, set beside the completeness table's row that covers it. A file
  removed with no row is a stop.
- **Checks that the files went over unchanged:**
  - `references/floor.md`, `references/hosts/claude-code.json` and `copilot.json` are
    byte-identical to their state at the base (child 23's evidence 2 proved the copies equal);
  - `references/review-step.md`'s reply block is unchanged byte for byte.

### 2. `roles.yaml` and the wrappers

In `skills/chantier/roles.yaml` (child 18):

- **`card`:**
  - `cr-driver.md`, `release-driver.md`, `stack-driver.md`, `qa-driver.md` for the four Drivers;
  - `chief-of-staff.md` for chief-of-staff (today `../../chief-of-staff/SKILL.md`);
  - `griller-skill.md` for griller (today `../../griller/SKILL.md`);
  - `griller.md` stays board-griller's card;
  - the other roles keep `<role>.md`, or whatever their family named.

  A `SKILL.md` that runs `brief` cannot also be the card `brief` reads.
- **`reply`:** each role's `reply` names the swapped file and heading that hold its reply block,
  as the family cards wrote them. `just roles`' check 8 proves the file and heading exist.
- **`first`:** changes only where a family changed a role's first line (none is expected; the
  wrappers check the first line).

In the 15 wrappers, on both hosts (`agents/<role>.md` and
`com.github.copilot/agents/chantier-<role>.agent.md`), by hand, with identical bodies:

- "Your card is `<x>`" names the new basename (the four Drivers' wrappers, where they carry the
  line; `just roles`' check 5).
- **The startup sentence (D6).** "Read the startup core first, and your card's `## Startup core`
  section when it has one" becomes "Read the brief your prompt's last line names, whole, first
  (your card, the floor, your facts)".
- **The `Read`-line clause.** "read it first, before any other step, at the path your prompt's
  `Read` line gives" becomes "it opens that brief".
- **board-griller.** Its wrapper drops "Read the startup core first," and keeps "your card's
  `## Started from the board`" (the board run gets no brief file).
- **Kept:** every other line. Among them the `# chantier-agent:` version line, the refusal
  paragraph and the frontmatter.

`just roles --write <role>` prints the expected wrapper. The Driver compares it, writes by hand,
and runs `just roles` until it prints `roles: 18 roles, 15 wrappers on 2 hosts agree`.

### 3. The CLI outputs switched

#### 3.1 `take`, `take stack`, `order qa` (D1, D2)

- **`commands/driver.py`** (`take <cr>`, today `driver.py:106`; `take stack`) and
  **`commands/orders.py`** (`order qa`, today `orders.py:161`) no longer print
  `driver_prompt_lines(...)`. After their state lines (head, reopened, rows), they print:
  - the `lease:` line, as today;
  - `brief: $CHANTIER brief <role> <unit> --lease <n> --batch <b>`, where:
    - `<role>` is the Driver role from `driver_row`;
    - `<unit>` is the CR id, `stack`, or the order's `O-k`;
    - `$CHANTIER` is printed as `cli_command(repo)`'s value, so the line runs as printed;
  - the line `next: run it and pass its output, unchanged, as the Driver's whole prompt`;
  - their trailing `fresh` and `watch` lines, as today.
- `take --reclaim` and a replacement Driver's `take` print the same `brief:` line, with the new
  lease (the pending item: "`take` prints a ready brief file").
- **`driver_prompt.driver_prompt_lines`** stays the facts builder that `brief` uses. It loses:
  - the heading;
  - the first line (the short prompt prints it);
  - `Read {refs}/startup-core.md … startup-manifest.json …` (today lines 172 to 173);
  - the `Card:` line;
  - the `Note:` placeholder.

  `brief`'s list of stripped lines (child 10) goes empty and is removed: one builder, no strip.
  `driver_row` keeps reading the `concepts.md` table for the role, the agent file, `writes`,
  Team and Rewrites; its card comes from `roles_data` (D2).
- **The scenario's Foreman**, which today copies the skeleton, runs the printed `brief:` command
  and starts the Driver from its stdout (child 10's `check_brief_driver` becomes the path every
  Driver start takes).

#### 3.2 `round`, `handoff`, `facts` (D3)

`commands/facts.py`'s `cr_facts` (callers: `driver.py:184`, `driver.py:225`, `facts.py:311`):

- **The `cards:` line** (today `facts.py:140`: "cards: {skill}/references/ (driver.md,
  concepts.md; each worker's own card, named in its opening lines) …") becomes:
  "brief: `brief <role> <cr>` gives each role its card, the floor and its facts; the project's
  rules rank above them: `rules`".
- **Removed:** `worker_prompt_lines(...)` and the "worker writes line" block, replaced by D3's
  `workers:` line.
- **In `plugin_files.py`,** `worker_prompt_lines`, `WORKER_FIRST_LINE` and `WORKER_CARD_LINE` are
  removed if nothing else calls them. `chief_prompt_lines` (used by `rules`) is kept.

`brief`'s worker facts (child 10: "the `cr_facts` lines before the worker blocks") now take all of
`cr_facts`' lines but the `workers:` line.

#### 3.3 `driver:refused` and the Foreman's piece

`driver:refused` was a manifest action: it read `foreman-refused.md` too (18.0 KB). It ends with
the manifest. Two checks:

- the `refused-push` topic in the swapped `topics.json` names no Foreman reading;
- no CLI line names `foreman-refused.md` (`test_card_names.py`, section 6).

#### 3.4 The Foreman's start (F19)

The Foreman has no wrapper and no parent that runs `brief` for it.

- **What the swapped cards say.** The swapped `chief-of-staff.md` (or its topic `batch-start`)
  gives its start line: claim the epoch (`foreman set … --epoch <n>`), then run
  `$CHANTIER brief foreman --batch <b> --epoch <n>` and read the file it names whole. The Driver
  checks that the swapped cards say so.
- **CLI: `open`'s `next:` line** (`commands/opening.py:277` and `:334`) changes from "then start
  the Foreman" to "then start the Foreman: its first step is `brief foreman --batch <b> --epoch
  <n>`". The direct-mode text is unchanged.
- **CLI: `foreman set`** (`commands/seat.py`), on success, adds
  `next: $CHANTIER brief foreman --batch <b> --epoch <n>`, with the values filled.

#### 3.5 The stack line (`src/stack_shape.py`)

- **`shape_line()`** drops `; rules: {skill}/references/foreman-stack.md (reread after a
  compaction)` (today line 56) and returns two lines:
  - the facts line, unchanged otherwise (`shape stack: next …; stack driver: …; native stack: …;
    alone asks: …`);
  - child 21's line, ``shape: stack: read `$CHANTIER help stack` now and after each compaction``.
- **Printed by:**
  - `status --refresh`, as today (`commands/batch_status.py:311`);
  - `brief foreman`'s facts, on a stack batch.

#### 3.6 Preflight, permissions and the allow block

- **`commands/preflight.py:218`**, the P10 line. It says "the rules are in hosts/claude-code.md,
  "Capabilities and their commands"". It becomes the full path
  `{skill}/references/hosts/claude-code.md`, followed by the heading that holds the allow table
  after child 23's cut (`Allow rules`). `test_card_names.py` and a heading check pin the file and
  the heading.
- **`commands/allow_samples.py`:**
  - its docstring and comments name the kept file and heading;
  - one `SAMPLES` row, `("batch", "any", f"{launcher_line(<plugin root>)} status",
    launcher_rule(<plugin root>))`, filled by `fill_rule` and `fill_sample`;
  - its rule in `RECOMMENDED_ALLOW`, in the table's order.
- **`references/hosts/claude-code.md`:**
  - the launcher's row in the allow table;
  - its rules (`Bash(<launcher_rule>)`, `PowerShell(<launcher_rule>)`, as child 17 named them) in
    the JSON block.

  `test_cli_runs.py::test_the_allow_rules_json_block_lists_exactly_what_preflight_checks` passes
  unchanged in logic. The topic `host-allow-rules` drops "unproved" for that rule.
- **`commands/permissions.py`:**
  - a broad `uv run --script * *` (in `PROBES`) reads "replaced by" the launcher's rule;
  - `_stale` recognises the launcher form in a rule that names a moved plugin;
  - its comment on `hosts/claude-code.md`, "What not to add", names the topic or heading that now
    holds it.
- **Comments only** in `board/griller_host.py`, `playbook/models.py` and
  `playbook/timing_check.py`. Where they name a host-card section that is gone, they name the host
  row id (`references/hosts/*.json`) or the topic that holds it. Comments are not scanned by the
  test; the PR lists them.

#### 3.7 The board Griller and the batch line

- **`board/griller.py`'s `BRIEF`** (today lines 68 to 74). It keeps "Your card:
  {skill}/references/griller.md, its section "Started from the board" first;". It drops "your
  host's reference: {skill}/references/hosts/{host_file}.md." (D7). It then has no `{host_file}`
  field, and the caller stops passing one. The `GRILLED` regex is unchanged. The run's allow list
  (read-only on the plugin's skill folder) already lets it read `griller-skill.md`'s
  `## How you grill`, which `griller.md` names.
- **`status/ready_line.py:127`**, the batch line's `rules:` part, becomes
  `; rules: {skill}/references/floor.md (after a compaction, run your brief again)`.

### 4. The four `SKILL.md`

- Copy `cards-next/skills/chantier-SKILL.md`, `chief-of-staff-SKILL.md`, `griller-SKILL.md` and
  `status-SKILL.md` to `skills/chantier/SKILL.md`, `skills/chief-of-staff/SKILL.md`,
  `skills/griller/SKILL.md` and `skills/status/SKILL.md`.
- **Version lines.** Each `chantier-version:` line must equal `__version__`. `scripts/version.py`
  (lines 36 to 39) checks the four, and `just check` runs it. Never edit a version by hand: if the
  line differs, `just version <the base's version>` rewrites it.
- **Links.** Each link the texts hold (written for `skills/<skill>/`) resolves at head.
  `test_plugin_files.py::test_skill_and_references_links_resolve` covers it.
- **What the texts say.**
  - The Chief of Staff's and the Griller's texts run `brief chief-of-staff` and `brief griller`
    (F19).
  - The router's text runs no brief of its own: child 23's open question 2 stands, and its
    default (no router role) applies.
  - The reload is "run the brief again", replacing the `reload` argument's old reading of
    `session-start.md` "5. Reload".

### 5. The hook (`hooks/register.tsx`)

- **`reloadLine(role)`** (today line 28) no longer says "call your chantier skill again with the
  argument reload". It says:
  "after this compaction, run your brief again (`brief <role>` through your skill's launcher line;
  the Foreman with `--epoch <n>`) and read the file it names whole; the floor, in that brief,
  holds."
  - For `chief-of-staff` and `griller`, `<role>` is filled in.
  - For `chantier` (the router, or a Foreman), the text says "your role's brief".
- **Unchanged:**
  - the `session.compact` logic (main loop only, manual or auto, never a veto);
  - `ROLE_SKILLS`, `PANE_SKILLS` and the CR board pane.

  AGENTS.md's rule on the pane's screenshot is not triggered.
- **`hooks/register.test.tsx`.** The `TAIL` constant (today line 1079) and its cases change to the
  new text. One case asserts that the message names `floor` and no removed file.
- `just mod` is owed.

### 6. Tests

All checks read the shipped files at the head under test. A prepared text is used only for a
refusal, paired with the shipped case.

- **New: `tests/test_card_names.py` (F18).**
  - **The Python files.** It walks every `.py` under `src/` with `ast`. It collects every
    `ast.Constant` string, f-string constant parts included, docstrings included.
  - **The hook.** It reads `hooks/register.tsx` and collects every `'…'`, `"…"` and `` `…` ``
    literal with a regex.
  - **It fails on any of these:**
    1. a `references/<path>` whose `<path>` ends in `.md` or `.json` and is not a file under
       `skills/chantier/references/`;
    2. a literal naming a basename from the test's `REMOVED` tuple. That tuple holds every path
       this PR removes, as listed in the PR. A name is exempt only while a file of that name
       exists under `references/`;
    3. a `hosts/<name>.md` that is not under `references/hosts/`.
  - **A failure** names the file, the line and the stale name.
  - **The prepared case.** One case feeds the scanner a prepared source holding
    `f"{skill}/references/startup-core.md"` and asserts that it fails, naming it. It is paired
    with the shipped scan passing.
- **Replaced: `tests/test_start_reading.py`** becomes `tests/test_brief_bytes.py`. It is
  parametrized over the 18 roles on the `claude` host, on child 10's fixtures, and asserts:
  - the brief file's bytes are at or below the figure recorded for that role in its `BRIEF_BYTES`
    table (the head's measure, rounded up to the next 100 bytes);
  - the brief starts with the role's card from `roles.yaml`.

  Child 26 freezes these figures as budgets.
- **Changed: `tests/test_brief.py`** (child 10).
  - Its check against `startup-manifest.json` goes. The role table is checked against
    `roles.yaml` and the wrappers only.
  - The `--cards skills/chantier/references` case now compares against the swapped folder.
  - One case asserts that `take`'s `brief:` line, run as printed, exits 0 and prints the same
    short prompt as the direct call.
- **Converted to file-and-heading pins** (the program: "each phrase pin becomes a pin on a file
  and heading, until child 26").
  - **The tests:**
    - `test_role_cards_split.py`, `test_startup_manifest.py` (with its `MOVED_OUT` check and
      `moved_rules.tsv`), `test_session_start_split.py`, `test_stack_chain_cards.py`,
      `test_rebase_rules.py`, `test_reload_rules.py`, `test_release_template_card.py`,
      `test_came_back.py`, `test_stack_shape.py` and `test_release_tag.py`;
    - the card reads of `test_board_griller.py` (`hosts/copilot.md`, line 299),
      `test_board_read_key.py`, `test_board_restart.py`, `test_board_running_lane.py`,
      `test_cli_runs.py` (lines 77, 108 and 203), `test_cli_stop.py` (`startup-core.md` and its
      `CLI_STOP_CARDS`), `test_command_names.py` (it now scans the swapped `references/**/*.md`;
      line 55 reads `sync-checkout.md` or its topic), `test_driver_prompt.py` (lines 31, 71 and
      185), `test_event_audience.py`, `test_launch_modes.py` (lines 131 to 261),
      `test_plugin_files.py` (lines 245 to 371), `test_triage_moves.py` and `test_watcher_step.py`.
  - **How a pin is converted.** Each pin on a phrase in an old file becomes a pin that the rule's
    home exists. That home is the file and level-2 heading, or the topic name, that the family
    inventories' `new home` column gives for the rule. A pin whose rule's home is `floor <n>`
    asserts that line in `floor.md`. A pin whose home is `refusal`, `next: line` or `facts`
    asserts the CLI line, as the existing CLI tests do.
  - **Deletions.** A test whose subject no longer exists (the manifest's shape, the startup
    sections, the split pieces) is deleted. The PR names it, with the pin that replaces each of
    its rules or the inventory row saying the rule is given elsewhere.
- **New in `tests/test_driver_prompt.py`.** Each Driver row's `Card` cell in `concepts.md`'s table
  equals `roles.yaml`'s `card` (D2).
- **No test reads the planning folder.** The Driver copies the inventories' homes into the tests
  by hand.

### 7. The eval kit and the scenario

- **`evals/kit/audit.py`**, check J1 (today line 567). It asks the prompt to hold
  `references/<card>`. It becomes:
  - **a role that `brief` starts** (every role of `roles.yaml`): the prompt holds
    `/chantier/briefs/` and `-<role>.md whole, first.`;
  - **a review step** (a project role, not in `roles.yaml`): it keeps `references/review-step.md`;
  - **J1's `$CHANTIER rules` check** stays for review steps only. For a brief-started role, the
    brief's facts carry the rules line (`cr_facts`' "`rules`" fact, the Drivers' rules line).
- **`evals/kit/dry_run.py`.** Its fixtures (lines 290, 950 to 1085: `QA_BODY`, the retro-critic and
  qa-driver prompts) are rewritten as brief short prompts, keeping each J1 pass case and fail case.
  Child 6's manifest-walk case checks `brief`'s boot (hand-over 1).
- **`scenario/run_scenario.py`:**
  - lines 1234 and 1242 (the `cards:` fact and a worker's opening line) become the new `brief:`
    fact and D3's `workers:` line;
  - lines 7579 and 7610 (the stack line) become child 21's line;
  - each Driver start goes through the printed `brief:` command (section 3.1).
- **`scenario/README.md`.** The Coverage bullet "`take` prints the `brief` command and the Driver
  starts from its output (unit: parallel)" replaces child 10's bullet if that one becomes
  redundant.
- `just eval-dry-run` is owed (changes under `src/` and `evals/kit/`).

### 8. Docs

- **Links.** In `README.md`, `CONTRIBUTING.md` (lines 63 to 64, 100 and 172) and `docs/`
  (`docs/forge-connectors.md`, `docs/planning-modes.md`, `docs/release-process.md`,
  `docs/tutorial-claude-code.md`, `docs/use-cases.md`), and in `evals/README.md` (lines 173, 238,
  269 and 280) and `evals/ticket-summary/RUNBOOK.md`:
  - each link to or mention of a removed file names its new home: the card, the topic (as
    `chantier help <name>`), the floor or the brief;
  - historical records follow D5.
- **`CONTRIBUTING.md:100`** ("the cards hold each role's contract, and the Foreman and the Drivers
  write the prompts") becomes: "the cards hold each role's contract, and `brief` builds each
  prompt from them and the facts" (sc09-Q2).
- **`docs/incidents.md` (new).** One short entry per story whose inventory home is
  `incidents file`, across the five inventories:
  - the date, what happened and the rule it gave;
  - where that rule lives now (card and heading, topic, floor line or refusal).

  No story is copied twice. The stories already in `docs/proofs/` are linked, not copied.
- **`evals/README.md`.** Its links to `hosts/claude-code.md` name the kept section. Its Windows
  and host claims stay as they are.

## Out of scope (must not)

- Keeping two loaded card sets, or a `cards:` switch (program).
- Adding a role (program). `roles.yaml` keeps its 18 roles.
- Leaving a floor rule out of the floor; adding an eleventh rule. A floor-level find goes to Known
  gaps for the owner.
- Merging apart from children 19 to 28.
- **Rewriting card content.** The family cards' content is not rewritten. The only edits allowed
  are a link fix, or a sentence that names a removed file. Each is listed in the PR. A rule found
  missing goes to Known gaps for child 25.
- The read-and-compare review and `docs/proofs/cards-inventory.md` (child 25).
- Rule ids, `budgets.json`, the M3 lint, raising a target (children 26 and 27; Q4).
- The real campaign (child 28).
- `chief_prompt_lines` in `rules`, the hub, the watcher's lines, the board's pages.
- Removing the old launcher forms' allow rules (D4).
- A new host row or a changed `mark` (child 8's data).
- A version bump.

## Acceptance evidence

Each item is recorded in the PR or under `<CR folder>/evidence/`, from the head pushed.

1. **One set.**
   - `git ls-tree -r --name-only HEAD skills/chantier/cards-next` prints nothing.
   - `git ls-tree -r --name-only HEAD skills/chantier/references` equals child 23's
     `cards-next/` list, minus `skills/`; the PR quotes the diff of the two lists.
   - `git grep -n "cards-next" HEAD` prints only `--cards` usage text and docs naming the
     argument.
   - Every removed path is listed, each with its completeness-table row.
2. **The checklist.** The PR's Internal references hold the hand-over checklist, every row ticked
   with its commit, or marked "owner answered otherwise: <answer>".
3. **Read by the CLI after the swap.**
   - **The Driver table.** A throwaway call of `driver_prompt.driver_table()` at head is quoted.
     It returns four rows, and its `Card` cells equal `roles.yaml`'s.
   - **`"Change Request"`.** `git grep -n "Change Request" HEAD --
     skills/chantier/references/concepts.md` is non-empty (`LAYOUT_GAP`).
   - **The host rows.** `chantier host` on both hosts prints the rows of `references/hosts/*.json`.
   - **Unchanged files.** `cmp` on `floor.md` and the two JSON files against the base shows no
     difference.
4. **`help`.**
   - **The topics.** `chantier help` lists the topics. Every name the CLI prints as `help <name>`
     (`git grep -n "help [a-z-]*" HEAD -- skills/chantier/scripts/cli/src`) prints its readings
     with exit 0. The PR quotes the run for each name.
   - **The roles.** `help --for <role>` gives exit 0 for the 18 roles.
5. **`just roles`** prints `roles: 18 roles, 15 wrappers on 2 hosts agree`.
6. **Quiz under F4.**
   - `just quiz <role> --against <child 6's baseline>` on every role with cases under
     `evals/quiz/<role>/`. It runs on the working tree, so the boot is `brief`'s output (no
     manifest). Each run prints the spend plan line first, under the default `--max-usd 10`.
   - **Pass:** no case scores 0 of 3 that the old cards passed. The PR has a table: role, cases,
     old passes, new passes, regressions (must be 0), spend.
   - **If the headless host CLI is refused,** the Driver hands back with everything else done and
     says so; the Chief of Staff runs the quiz.
7. **Bytes.** One table, one row per role (18):
   - the old start reading's bytes: child 6's old-card boot at the base, `just quiz … --cards
     <base sha>`'s plan line or its boot dump;
   - the new brief file's bytes on the same fixture (`brief <role> <unit>`);
   - the program's starting figure where `study-fable-v2` gives one;
   - the role's card target, and "within" or "over by N".

   A card over its target is in Known gaps with its size (Q4). The board Griller's row shows its
   brief and its section's size (sc19-Q1).
8. **The switched-lines test.**
   - `test_card_names.py` passes at head.
   - Its prepared stale-name case fails as expected; the PR quotes the failure line.
   - The PR quotes the CLI lines changed in section 3, before and after.
9. **`just test` seconds.** `just test` timed at the base and at head, on the same machine, with
   both figures quoted.
   - `test_card_names.py` and `test_brief_bytes.py` are added.
   - Tests on removed pieces are deleted, among them most of `test_startup_manifest.py`,
     `test_session_start_split.py` and `test_start_reading.py`.
   - Expected: about 0 s net, at most +3 s. The AGENTS.md budget is 30 s above 18.5 s.
10. **Links.** A throwaway script, not committed, is quoted with its output. It lists every
    relative link in `skills/**/*.md`, `agents/`, `com.github.copilot/agents/`, `README.md`,
    `CONTRIBUTING.md`, `docs/**/*.md` and `evals/**/*.md`, and resolves each at head.
    - Result: none broken.
    - No link into `cards-next/` remains.
    - Each historical link rewritten under D5 is listed.
11. **The hook.** `just mod` passes, and the new `register.test.tsx` case passes. A transcript of
    one real Claude Code session at head is attached: after `/compact`, it shows the reload
    message naming the floor, then the session running `brief chief-of-staff`.
12. **Gates.**
    - Before the first push: `just check` and `just eval-dry-run` at the rebased head, and
      `just mod` (changes under `src/`, `evals/kit/` and `hooks/`).
    - The long gate `just scenario (ubuntu-latest)` is green at the PR's head.
    - The local Windows `chantier gate <cr> scenario` is owed only if this child is the stack's
      top when it is called ready. In the stack, children 25 to 28 sit above it, so it is not owed
      unless they are dropped.

**The host and default matrix:**

| Host | Defaults | Status |
| --- | --- | --- |
| Claude Code | shipped | The measured column: briefs for 18 roles, quiz, scenario, the hook's reload message, the session transcript of evidence 11 |
| Claude Code | a configured generic agent for a worker | Its brief carries the contract lines (child 10's case in `test_brief.py`) |
| Copilot | shipped | Briefs build for 18 roles (`test_brief.py`, both hosts). Rows stay `untested`. No hook, so the reload message and the `writes:` guard are inert there. Unproved in a real Copilot session (F17) |
| Copilot | configured | The same facts; unproved |

## Handback

- Handed back validated, with these Known gaps:
  - "real run not done (child 28)" (F6);
  - each card over its target, with its size (Q4);
  - if D9 applied, "launcher not switched: <reason>";
  - any quiz not run because the headless CLI was refused.
- The typed merge wait `$CHANTIER wait <cr> merge <child 28's PR>` is recorded once child 28's PR
  exists. Until then the PR's Known gaps say "do not merge: merges with children 19 to 28 as one
  unit, after child 28's campaign". Nothing merges while the owner sleeps.

## Risk

- **The highest in the program:** every role's contract changes at once. A rule lost in a family
  shows only here and in child 28's run. The guards:
  - the quiz under F4 (evidence 6);
  - the converted pins on the inventories' homes (section 6);
  - the switched-lines test (evidence 8).
- **The Driver start path changes for every batch** (`take` → `brief`). A wrong `brief:` line
  stops every Driver. The guards: `test_brief.py`'s new case (section 6) and the scenario, where
  every Driver starts this way.
- **The launcher becomes the typed form** (D4). A user's settings lacking its rule get one P10
  ask, as child 17 planned.
- The long gate is owed, and so are `just mod` (the hook) and `just eval-dry-run`.

## AGENTS.md change

None. Child 9 rewrote the role sentences, and this child makes them true. The rule naming
`register.tsx`'s pane is untouched; the pane does not change. D1 and D7 keep AGENTS.md's sentences
on the briefs and on the board Griller's fixed brief true.

## Open questions

1. **What `take` prints (behaviour).** The program says `take`, `take stack` and `order qa` "print
   the lease and the `brief` command (the short prompt of child 10)". This specification reads it
   as the command line, which the steering session then runs (D1): one more call per Driver start,
   and only `brief` writes a brief.
   - **The other reading:** `take` itself builds the brief file and prints the short prompt,
     saving that call. AGENTS.md would then need "and the briefs `take`, `take stack` and
     `order qa` write" beside `brief`.
   - **Default if unanswered:** D1.
2. **The board Griller and the floor (scope, risk).** The board Griller's run does not get a brief
   file. Its fixed `BRIEF` names `griller.md`'s section, the CR's folder and the CLI, not the
   floor. Its allow list is narrower than most floor rules: it writes only that CR's folder and
   runs four commands.
   - **Should `BRIEF` also name `{skill}/references/floor.md`?** That needs AGENTS.md's sentence
     "a fixed brief that names the Griller card, the CR's folder and the CLI" to add "and the
     floor".
   - **Default if unanswered:** no (D7). The PR's Known gaps say "the board Griller does not read
     the floor".
