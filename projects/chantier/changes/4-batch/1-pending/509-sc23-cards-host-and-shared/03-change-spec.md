# SC23: New shared cards, host topics, topics.json and SKILL.md texts

Child 23 of 28 of the program `simplify-cards-and-prompts`. These rank above this specification,
in this order: the program's `03-change-spec.md`, its `02-answers.md` (answers 17 to 22) and its
`work/study-*.md`. Short ids such as F4, F5 and Q4 are the program's findings and questions, as the
Chief of Staff settled them in answer 22. The owner confirms answer 22 when they wake. This child
needs nothing beyond it.

This is the last of the five family children (19 to 23). It follows child 19's specification
(CR-505, `sc19-cards-workers`) for where the new files live, the budgets, the rule inventory and
the proof method. It adds no second method. What child 19 writes for "the 11 roles" applies here to
the shared files, the host topics and the four `SKILL.md` texts.

## Goal

In the owner's words (answer 1): the cards are "far too heavy and detailed". Write "the smallest
possible cards, no behaviour lost", and use progressive disclosure to the full.

This child closes the new card set in `skills/chantier/cards-next/`, which nothing loads until
child 24's swap. It writes:

- the shared files: `concepts.md`, the templates and layouts (`pr-template.md`,
  `release-template.md`, `status-layout.md`, `titles.md`, `ticket-summary-example.md`),
  `routing.md`, `init.md`, `review-step.md`, `sync-checkout.md` and `forges/`;
- the host topics: what stays of `hosts/claude-code.md` and `hosts/copilot.md` once their rows are
  child 8's data (`hosts/*.json`) and their history is in `docs/proofs/`;
- the final `cards-next/topics.json`, merging the four families' entries with its own;
- the final `cards-next/floor.md`;
- the four `SKILL.md` texts as they will be after the swap, in `cards-next/skills/`: one line
  naming the launcher (child 17) and, for the Chief of Staff and the Griller, one line that runs
  `brief <role>` and reads the brief file (F19);
- a rule inventory of every old file it replaces, plus a completeness table proving that every file
  of today's `references/` and the four `SKILL.md` is covered by one family's inventory.

## Place in the chain

- **Base: child 22's branch** (`sc22-cards-chief-and-griller`) in the batch's single stack. The
  Driver rebases on it before the first push. Below it in the stack, and relied on here:
  - child 6 (CR-492): `just quiz <role> --cards <folder> --against <baseline>`;
  - child 7 (CR-493): `references/topics.json`, its format, `chantier help`, and
    `load_topics(path)` and `section(path, heading)` in `src/commands/help.py`;
  - child 8 (CR-494): `references/hosts/claude-code.json` and `copilot.json`, `src/host_rows.py`
    (`load_rows`, `UNTESTED`), and `docs/proofs/claude-code.md` and `copilot.md`;
  - child 10 (CR-496): `chantier brief <role> [<unit>] --cards <folder>` and
    `references/floor.md`;
  - child 17 (CR-503): the launcher `skills/chantier/scripts/chantier.py` and
    `launcher_line(root)` / `launcher_rule(root)` in `src/launch.py`;
  - child 18 (CR-504): `skills/chantier/roles.yaml`;
  - children 19 to 22 (CR-505, CR-506, CR-507, `sc22-cards-chief-and-griller`): the family cards
    and topics in `cards-next/` (`driver.md`, `foreman.md`, `chief-of-staff.md`,
    `griller-skill.md`, `griller.md`, the workers' cards, `floor.md`, `topics/`, `topics.json`) and
    their inventories `<their CR folder>/evidence/cards-inventory-<family>.md`.

  If any of these is missing at the base (`brief` has no `--cards`, `cards-next/floor.md` or a
  sibling card named above is absent, `references/topics.json` or `references/hosts/*.json` is
  absent), the Driver stops and says so. There is no stand-in. Child 17 is the one exception the
  program names: if its trial failed or it handed back blocked, see section 6.
- **Depended on by:**
  - child 24, which swaps `cards-next/` in (it copies `cards-next/skills/<skill>-SKILL.md` to
    `skills/<skill>/SKILL.md`; see "For child 24");
  - child 25, which takes this child's inventory and completeness table as seeds;
  - child 26, which freezes the budgets and lints the set this child closes.
- **Merge:** with children 19 to 28 as one unit (the program's merge rule; F11).

## Decisions carried

| Source | Decision | Where here |
| --- | --- | --- |
| Answer 1 | Smallest possible cards, no behaviour lost, progressive disclosure | sections 2 to 5 |
| Answer 3 (Q6) | No stumbling on the common path. Free stumbling on rare cases | common path in the files, rare parts in topics |
| Answer 10 (Q10) | A rare incident rule with no CLI trigger becomes a help topic for one release | topics with `review_by: "0.16.0"` |
| Answer 14 (Q16) | One card set. The old files are removed at the swap, with no switch | `cards-next/` unloaded; `references/` untouched |
| Answer 15 (Q14) | A rule lives in one place; a piece is loaded at its moment | sections 2 to 4; no rule written twice |
| Answer 16 (Q13) | Trial history leaves the cards | no date, batch, model or trial story (M3); stories go to `docs/proofs/` (already) or the incidents file (child 24) |
| Answers 17 and 18 | Total rewrite in one pass, then a read-and-compare review | section 7 |
| Answer 22, F2 | Beside the old ones, unloaded, one CR per family, merged with the swap | section 8; Merge |
| Answer 22, F4 | Quiz pass rule: no case scores 0 of 3 that the old cards passed. Spend cap printed first | Acceptance evidence 5 |
| Answer 22, F5 | A rule that protects the user or the repository lives only in the floor, a role's card or a refusal | section 7; inventory column `kind` |
| Answer 22, F6 | Handed back validated, with the Known gap "real run not done (child 28)" | Handback |
| Answer 22, F11 | A typed merge wait on child 28 | Handback |
| Answer 22, F17 | An unproved claim is marked "unproved" | every file; section 3 (Copilot) |
| Answer 22, F19 | The prompt and the `SKILL.md` run `brief <role>`; the agent reads the brief file | section 6 |
| Answer 22, F20 | State the seconds added to `just test` | Acceptance evidence 9 |
| Answer 22, Q4 | A file above its target is listed in Known gaps with its size. Only the owner raises a target | Acceptance evidence 3 |
| Program, common to 19 to 23 | Layout mirrors `references/`; budgets; topics in `cards-next/topics/`; brief bytes, quiz, row list; no edit to `references/`, the CLI or the hook | sections 1 to 8 |
| Program, child 23 | Scope, depends on 22, every link inside `cards-next/` resolves, `brief` for all 18 roles builds from `cards-next/`, long gate owed, no AGENTS.md change | the whole specification |
| Program, child 17 | Child 23 writes the `SKILL.md` launcher line and the host topic that holds the launcher's allow rule; if child 17 is blocked, today's paragraph stays until the owner decides | section 6; section 3 |
| Program, pending items | `session-start-split-fix-citation-re-read` and `driver-context-second-cut`: re-read after the swap | `pr-template.md` and `concepts.md` cut here; the re-read is child 25's |
| Child 19 | Inventory file, columns, `new home` values, closing lists, forbidden phrases, unloaded check | sections 7 and 8; Acceptance evidence |
| `02-answers.md` of this CR | Specified from the program. No separate critic. Destination: running batch batch-31 | this specification as written |

## What changes

Paths are from the repository root. `src/` is `skills/chantier/scripts/cli/src/chantier/`. "Today's
file" means the file at this child's base; sizes quoted below are from `origin/main` 8a960d34 and
the Driver re-measures them at the base. One KB is 1,000 bytes. Sizes are LF bytes, measured as
`git show HEAD:<path> | wc -c`.

### 1. The files this child adds or edits

All under `skills/chantier/cards-next/`:

| File | From today's | Today's bytes | Target |
| --- | --- | --- | --- |
| `concepts.md` | `references/concepts.md` | 73,286 | none set (open question 1); each section read by a topic at most 1,500, but for `### A Driver's prompt` |
| `pr-template.md` | `references/pr-template.md` | 16,801 | none set (open question 1) |
| `release-template.md` | `references/release-template.md` | 12,155 | none set (open question 1) |
| `status-layout.md` | `references/status-layout.md` | 17,475 | none set (open question 1) |
| `titles.md` | `references/titles.md` | 2,684 | a topic's 1,500 if it becomes one |
| `ticket-summary-example.md` | `references/ticket-summary-example.md` | 1,422 | may fold into a topic |
| `routing.md` | `references/routing.md` | 5,016 | none set (open question 1) |
| `init.md` | `references/init.md` | 10,041 | none set (open question 1) |
| `review-step.md` | `references/review-step.md` | 3,950 | a review step's card, 1.5 KB (the program's "other workers and critics"), reply block unchanged |
| `sync-checkout.md` | `references/sync-checkout.md` | 4,801 | a topic's 1,500 if it becomes one |
| `forges/github.md`, `forges/gitlab.md` | `references/forges/` | 739, 744 | unchanged or smaller |
| `hosts/claude-code.json`, `hosts/copilot.json` | `references/hosts/*.json` (child 8) | as at base | byte-identical copies |
| `hosts/claude-code.md` | `references/hosts/claude-code.md` | 109,857 | its Allow rules section only (section 3) |
| `topics/host-*.md` | `references/hosts/*.md` | (part of the above) | 1,500 each |
| `topics/<name>.md` (others) | the shared files' rare parts | — | 1,500 each |
| `topics.json` | children 19 to 22's entries | — | final (section 4) |
| `floor.md` | `references/floor.md` | ≤ 1,200 | byte-identical (section 5) |
| `skills/chantier-SKILL.md`, `skills/chief-of-staff-SKILL.md`, `skills/griller-SKILL.md`, `skills/status-SKILL.md` | the four `SKILL.md` | 3,537, 3,664, 3,223, 3,644 | section 6 |

A shared file not carried is named in the completeness table (section 7) with its reason and is
removed by child 24.

The Driver may also edit a sibling's file in `cards-next/` for two reasons only, each listed in the
PR with its line:

- a link fix (a forward link to a file this child names differently, or one that no longer
  resolves);
- a kind-a rule (F5) from this child's own sources whose home must be a role's card, not a shared
  file or a topic.

For each role whose card it changes, it re-runs that role's quiz (Acceptance evidence 5).

### 2. The shared files

The shape follows child 19's section 2: the common path stays in the file, a rare part becomes a
topic in `cards-next/topics/` listed in `topics.json`, and no rule is written twice (a rule the
floor, the brief's facts, a host row, a refusal or a CLI `next:` line already gives is cut).

#### 2.1 `concepts.md`

Today a 73 KB mix of glossary, agent-starting rules, escalation and numbered rules. The new file
is a short glossary plus the parts the CLI and the sibling cards read; the rest goes to topics, a
role's card (kind a), or is cut as given elsewhere.

It must keep, verbatim where stated:

- **`### A Driver's prompt`**, with the same header row (`| Driver | Started after | Card |
  \`writes:\` | \`Team:\` | \`Rewrites:\` |`) and four rows in the same column order and cell
  syntax, because `driver_prompt.driver_table()` reads `skill_dir()/references/concepts.md` after
  the swap, finds `DRIVER_TABLE_TITLE = "### A Driver's prompt"`, parses `|` rows until the next
  `#` line, skips the `Driver` header and separators, and `driver_row` reads cells 1 to 5
  (backticked `started` forms `take <cr>` with kinds `change`/`fix`/`release`, `take stack`,
  `order qa`; card; writes; Team; Rewrites `own branch`/`batch branches`/`none`). The card cell
  stays `driver.md`. A short intro sentence may stay; nothing else in that section.
- **The "Change Request (CR)" entry**, because `lifecycle/layout_check.py`'s `LAYOUT_GAP` names
  `concepts.md, "Change Request"`.
- **Every heading another file links to**: the sibling cards' and topics' links to `concepts.md`
  (child 19 names forward links to it), and the four `SKILL.md` texts. The Driver lists them first
  (`git grep -n "concepts.md" HEAD -- skills/chantier/cards-next`) and keeps each target heading.
- **"A CR's summary"** entry and any glossary word a CLI line prints as a term to look up.

The `## Startup core` heading goes: the brief replaces the startup core (child 10). The numbered
rules either move to the floor's ten (already there: cut), to a role's card (kind a), to a topic,
or are cut with their row in the inventory saying where they are given.

#### 2.2 Templates and layouts

- **`pr-template.md`**: keep the template's section headings in their order (Summary, Issues
  References, Deliverables, Blast radius, Autonomous decisions, Known gaps, Changes, Human
  decisions, Impacts, Test plan, Internal references), because the Drivers fill them and the
  Inspector and Verifier check them; keep "Scope and precedence" (the project's own template ranks
  above). "The audit" and "A customised version" may become topics. AGENTS.md names "Known gaps"
  and "Deliverables": both headings stay word for word.
- **`release-template.md`**: keep the notes' rules the Release Driver applies on the common path;
  "Visible evidence", "The thread" and "Where they go" may become topics (release topics of child
  7 such as `release-notes` exist: link, do not duplicate).
- **`status-layout.md`**: keep the rules of every report and the Progress, Completion and Cost
  tables (the owner's report format); "Tips" may become a topic.
- **`titles.md`**: the Chief of Staff's and the Foreman's title rules. Fold into
  `chief-of-staff.md` (child 22) or a topic if child 22 already carries them; else keep it.
- **`ticket-summary-example.md`**: keep or fold into the topic that teaches `summary set`.

#### 2.3 `routing.md`, `init.md`, `review-step.md`, `sync-checkout.md`, `forges/`

- **`routing.md`**: the message table between roles. Keep the table; cut a row that the CLI's
  commands now print (`msg`, `next:` lines) only with the inventory naming the command.
- **`init.md`**: the seven sections of `chantier init` guidance. The common path stays; rare
  branches become topics.
- **`review-step.md`**: the generic review-step card. Its reply JSON (keys `verdict`, `head`,
  `blocking`, `minor`, `confidence`; caps of 300 characters per item, at most 5 minor items, under
  3,000 characters) is unchanged byte for byte. Its target is 1.5 KB (a review step is a worker or
  critic for the budgets); over target goes in Known gaps.
- **`sync-checkout.md`**: becomes the `sync` topic's reading if child 7's `sync` topic does not
  already point at it; else it stays a file and the topic links it. At most 1,500 bytes either
  way.
- **`forges/github.md`, `forges/gitlab.md`**: kept, smaller only if a line is given elsewhere. Each
  link (for example `../../../../docs/forge-connectors.md`) must resolve from the target location
  `skills/chantier/references/forges/`, which is the same depth as `cards-next/forges/`.

### 3. The host files

Child 8 turned the host capabilities into rows (`hosts/claude-code.json`, `hosts/copilot.json`)
read by `chantier host` and the brief, and moved the trial history to `docs/proofs/`. What stays of
the two host cards here:

- **The JSON rows**: `cards-next/hosts/claude-code.json` and `copilot.json` are byte-identical
  copies of `references/hosts/*.json` at the base, because `host_rows.load_rows` reads
  `skill_dir()/references/hosts/<file>` after the swap. No row is added or changed here.
- **`cards-next/hosts/claude-code.md`**: only its "Allow rules" section (today lines 236 to 432 at
  `origin/main`), with the table and the JSON block, because
  `tests/test_cli_runs.py::test_the_allow_rules_json_block_lists_exactly_what_preflight_checks`
  ties them to `src/allow_samples.py`'s P10 samples, and `preflight.py`, `permissions.py` and
  `allow_samples.py` name this file. Its sentences around the table are cut to what a reader needs
  to add the rules. Child 24 adds the launcher's row to the table and the JSON block with the P10
  sample (the program's child 17 entry); this child does not.
- **The host topics**: the rest of both host cards becomes `topics/host-*.md`, each at most 1,500
  bytes, using a `{"claude": ..., "copilot": ...}` reading map where the two hosts differ. The
  expected set, which the Driver may merge or split as the content asks:
  - `host-configuration` (who reads it, prerequisites, Windows PowerShell 5.1);
  - `host-allow-rules` (pointing at `hosts/claude-code.md`; includes the launcher's allow rule,
    `launcher_rule(root)`, marked "unproved" until child 24's P10 row exists, and the Copilot
    equivalent marked untested);
  - `host-auto-mode` (Auto mode, what stays refused);
  - `host-compact` (compacting and the reload after it: run the brief again);
  - `host-write-guard`;
  - `host-sessions` (classes of session, surfaces and options, sessions of one repository);
  - `host-for-you` (the "For you" block);
  - `host-auto-fix` (auto-fix events);
  - `host-turn-end` (the Foreman's turn-end notice) and `host-driver-silence` (a Driver's silence);
  - `host-foreman-worktree` (a Foreman in a worktree asks) and `host-reuse-foreman`.

  These are the sections child 8 left without a row and to this child. Rules around tools that did
  not fit in a row's `means` are placed here or in a role's card (kind a).
- **Copilot**: carried only where content is irreducible to a row. Every Copilot claim not proved
  is marked "unproved" (F17); every Copilot row stays `untested`.
- **Stories and dated trial text** are not carried: either already in `docs/proofs/` (child 8) or
  listed for child 24's incidents file, with their inventory home `proof file` or `incidents file`.
- `"What the docs do not say"` and similar meta sections: their facts go to a topic or a row; their
  history to the proofs.

### 4. The final `topics.json`

`cards-next/topics.json` in child 7's format (`{"version": 1, "paths": ..., "topics": {...}}`),
readings relative to `cards-next/`, never an `@action`.

- It merges the entries children 19 to 22 added with this child's (shared-file and host topics).
  Duplicate names are resolved to one entry; a reading named twice is one reading.
- It holds every topic name the CLI source prints as `help <name>` at the base. The Driver lists
  them with `git grep -n "help [a-z-]*" HEAD -- skills/chantier/scripts/cli/src` and checks each
  (among them `lease`, `refused-push`, `stack-merge`, `merge`, `watcher`, `board`).
- It holds every name in `references/topics.json` at the base (child 7's list: lease, checkpoints,
  steering-messages, restart, trouble, conflicts, handback-other, pr-extras, refused-push, retake,
  matrix, stack-restack, stack-make, stack-joins, stack-changes, release-notes, release-ship,
  release-merged, release-end, stack, stack-merge, merge, hold, lost-driver, conflict-check,
  release, retro, grill, batch-start, steering, ready-to-merge, batch-end, direct,
  release-procedure, writer, watcher, board, sync), or lists each rename in the PR. A name the CLI
  prints is never renamed.
- Every reading resolves under `cards-next/`: a file exists, a `file#heading` names an existing
  level-2 heading, both sides of a host map resolve.
- Every `roles` entry is a role name of `roles.yaml`.
- The answer-10 rare topics carry `review_by: "0.16.0"`.

### 5. The final `floor.md`

`cards-next/floor.md` stays byte-identical to `references/floor.md` at the base (child 19 copied
it). No eleventh rule is added here: a rule this child finds floor-level goes to Known gaps for the
owner, with its home meanwhile in a role's card (kind a).

### 6. The four `SKILL.md` texts

Kept as `cards-next/skills/<skill>-SKILL.md` (chantier, chief-of-staff, griller, status), flat
files, so that no host discovers a nested `SKILL.md` before the swap (that a nested file would be
discovered is unproved; the flat name avoids the question). Child 24 copies each to
`skills/<skill>/SKILL.md`.

Each keeps:

- its frontmatter (`name`, `icon`, `color`, `description`) unchanged;
- its title;
- the `chantier-version: X.Y.Z` line equal to the base's `__version__`. `scripts/version.py` does
  not scan `cards-next/`; child 24's copy brings the line under its targets.

Each replaces today's long `$CHANTIER` paragraph and `## Startup core` with:

- **one launcher line**, built from `launcher_line(root)` (child 17):
  `uv run --script "<plugin root>/skills/chantier/scripts/chantier.py" [--project <folder>] <command>`,
  with `--project` when the planning lives on an external surface, and `--sync` at the moments
  AGENTS.md names (a session's start, a batch's start, after a merge that changes `uv.lock`), with
  its fixed lines (`in sync`, `synced`, `sync pending: held by …`, `plugin mode: no sync (only
  chantier's own checkout syncs)`) and the exit 127 line when uv is missing;
- for **chief-of-staff** and **griller**, one line: run `$CHANTIER brief chief-of-staff` (resp.
  `brief griller`) and read the file its last line names, whole, first; the Chief of Staff keeps
  the mode word line (`foreman` / `direct`) and the `watch: not running` rule only if child 22's
  card does not already carry them; the reload is "run the brief again" (it replaces the reload via
  `session-start.md` "5. Reload" and `reload-rules.md`);
- for the **router** (`chantier`): ask which role, or behave as the Chief of Staff when a live
  Chief of Staff holds the seat; it runs no brief of its own (open question 2);
- for **status**: its steps unchanged in behaviour (changes nothing; `status --refresh`, `status`,
  `cost`; icons from STATUS.md), with the layout linked as
  `../chantier/references/status-layout.md`.

Links in these texts are written for their target place (`skills/<skill>/`). The link check
(Acceptance evidence 6) maps `../chantier/references/` to `cards-next/` and `./` to the target
folder.

**If child 17 failed or handed back blocked**: the texts keep today's `$CHANTIER` paragraph,
minus its mentions of the startup manifest, and the PR's Known gaps say so; the brief line is still
written. No host topic claims a launcher allow rule.

### 7. The inventory and the completeness table

`<CR folder>/evidence/cards-inventory-host-and-shared.md`, in child 19's form: ids `H-001` and up;
columns `id, role, trigger, behaviour, source (file:line at base), kind (a–f), new home, check`;
`new home` one of `card <file>`, `floor <n>`, `refusal <cmd, msg start>`, `next: line`,
`topic <name>`, `facts`, `host row <id>`, `proof file`, `incidents file`, `inferable`; the two
closing lists (kind-a rows with their homes, each a card, the floor or a refusal; inferable rows,
none of kind a).

Its sources: every file of section 1's "From today's" column, plus the files no family claims:
`references/startup-core.md`, `role-core.md`, `host-core-claude-code.md`, `host-core-copilot.md`,
`reload-rules.md` (which the floor and the brief replace) and `startup-manifest.json`. For the
manifest, a table maps each action (for example `deliver` → `pr-template.md`, `release` →
`release-template.md`, `status` → `status-layout.md`, `route` → `routing.md`, `sync` →
`sync-checkout.md`, `chief-of-staff` → `titles.md`) to its new home: a brief part, a topic, a link
in a card, or cut with a reason.

**The completeness table** (same file, its own section): one row per file under
`skills/chantier/references/` at the base, recursive, and per `skills/*/SKILL.md`: the inventory
that covers it (`workers`, `drivers`, `foreman`, `chief-and-griller`, `host-and-shared`) and its
fate (carried as `<cards-next path>`, split into topics `<names>`, or not carried, removed by child
24). No file is left without an inventory. A file another family claimed and did not inventory is
a finding in Known gaps, not silently inventoried twice.

### 8. Keeping the new files unloaded until the swap

As child 19's section 5, unchanged: no file outside `cards-next/` names it as a path to read; no
change to `roles.yaml`, the wrappers, `src/`, `hooks/`, `references/`, `scripts/version.py` or any
test. The new files must not contain the phrase "Read this short role contract at boot"
(`test_startup_manifest.py` scans `skills/**/*.md`), a `# chantier-agent:` line, or
`chantier board`. `cards-next/skills/*-SKILL.md` are not discovered as skills (section 6).

## Out of scope

- Any edit to `references/`, `roles.yaml`, a wrapper, a live `SKILL.md`, `src/`, `hooks/`, a
  test, AGENTS.md or a version.
- The families' own cards (children 19 to 22), but for the two kinds of edit section 1 allows.
- `session-start.md` (child 22's).
- The swap, the CLI line switches (`facts.py`, `preflight.py`, `driver_prompt.py`, `ready_line.py`,
  `board/griller.py`), the launcher's P10 row and allow sample, the hook's compaction message,
  `tests/test_card_names.py`, the test conversions and the incidents file (child 24).
- The committed inventory `docs/proofs/cards-inventory.md` and the post-swap re-reads of the
  pending items (child 25).
- Rule ids, `budgets.json`, M3 lint (child 26).
- A real run (child 28).
- A new host row, a changed `mark`, an eleventh floor rule, or any raised budget (owner only, Q4).

## Acceptance evidence

Each item is recorded in the PR or under `<CR folder>/evidence/`, from the head pushed.

1. **The files.** The PR lists the files added or changed under `skills/chantier/cards-next/`,
   with each sibling-file edit and its reason (section 1). `git diff --stat <base>..HEAD` shows
   changes under that folder only.
2. **Byte-identical copies.** At head, quoted (or the PowerShell equivalent):
   - `git show HEAD:skills/chantier/cards-next/floor.md | cmp - <(git show HEAD:skills/chantier/references/floor.md)`;
   - the same for `hosts/claude-code.json` and `hosts/copilot.json`.
3. **Bytes.** A table, one row per file of section 1: today's bytes, new bytes, target, "within"
   or "over by N" (or "no target"). Every topic file at most 1,500 bytes; `review-step.md` against
   1,500. A file over target is in Known gaps with its size (Q4).
4. **Brief for all 18 roles.** For each role of `roles.yaml` (cr-driver, release-driver,
   stack-driver, qa-driver, coder, conflict-resolver, debugger, inspector, investigator, verifier,
   spec-writer, spec-critic, board-griller, retro-critic, demo-explorer, chief-of-staff, griller,
   foreman), run `$CHANTIER brief <role> <unit> --cards <worktree>/skills/chantier/cards-next`
   with child 10's units (a CR id for Drivers and workers, `O-1` for qa-driver, `stack` for
   stack-driver, a CR folder for spec-writer, spec-critic and board-griller, none for the rest),
   on each host `brief` selects. Each exits 0. The table sets each new brief's bytes beside the old
   brief's (same command without `--cards`) and study-fable-v2's declared boot.
5. **Quiz under F4**, only for each role whose card this child changed (section 1) and that has
   cases under `evals/quiz/<role>/`: `just quiz <role> --cards skills/chantier/cards-next
   --against <child 6's baseline>`, the spend plan line printed first under the default
   `--max-usd 10`. Pass: no case scores 0 of 3 that the old cards passed. If the headless host CLI
   is refused, the Driver hands back with the files written and says so; the Chief of Staff runs
   it. If no card was changed, the PR says "no quiz owed".
6. **Links.** Every relative link in every file under `cards-next/` (all families, not only this
   child's) is listed with its target, and each resolves inside `cards-next/` at head (the
   `SKILL.md` texts under section 6's mapping, `forges/` links to `docs/` from the target depth).
   No forward link remains; no link points into `references/`.
7. **`topics.json`.** A throwaway script, not committed, run at head and quoted with its output:
   `load_topics(Path("skills/chantier/cards-next/topics.json"))` from `src/commands/help.py`
   loads; for every topic, every reading resolves (`section(path, heading)` for a `#heading`, both
   sides of a host map); the CLI's `help <name>` list and child 7's names are all present (or
   renames listed, none of a CLI name); every role is in `roles.yaml`.
8. **The Driver table.** A throwaway call of `driver_prompt`'s parser on
   `cards-next/concepts.md` (for example by pointing it at the file's text) returns the same four
   rows, cell for cell, as on `references/concepts.md`; `"Change Request"` is present
   (`git grep -n "Change Request" HEAD -- skills/chantier/cards-next/concepts.md`).
9. **`just test`.** 0 s added: no test is added or changed. Times at base and head on the same
   machine.
10. **The inventory and completeness table** (section 7): every rule sentence of the sources has a
    row, the Driver says how it walked them; no empty `new home`; kind-a homes are a card, the
    floor or a refusal; no inferable row is kind a; the reply block of `review-step.md` diffs empty;
    every file of `references/` and every `SKILL.md` has a row in the completeness table.
11. **Unloaded.** `git grep -n "cards-next" HEAD -- . ':(exclude)skills/chantier/cards-next'` is
    quoted; every line is usage text or a doc naming `--cards`. `git grep -n "Read this short role
    contract at boot\|# chantier-agent:\|chantier board" HEAD -- skills/chantier/cards-next` shows
    nothing.
12. **Gates.**
    - Before the first push, `just check` at the rebased head. `just eval-dry-run` is not owed (no
      change under `src/` or `evals/kit/`).
    - The long gate `just scenario (ubuntu-latest)` green at the PR's head (a card change).
    - The local Windows `chantier gate <cr> scenario` only if this child is the stack's top.
    - `just mod` is not owed.

The matrix (program): Claude Code with the shipped defaults is the measured column; Copilot shows
in the host maps and the brief's host rows, marked untested.

## Handback

- Handed back validated, with the Known gap "real run not done (child 28)" (F6), any file over
  target with its size (Q4), and, if child 17 was blocked, "launcher line not written: today's
  paragraph kept".
- The typed merge wait `$CHANTIER wait <cr> merge <child 28's PR>` is recorded once child 28's PR
  exists. Until then, the PR's Known gaps say "do not merge: merges with children 19 to 28 as one
  unit, after child 28's campaign". Nothing merges while the owner sleeps.

## Risk

- Low on the running product: nothing loads `cards-next/` until child 24.
- High on the swap: `concepts.md`'s Driver table, the allow-rules block, the host JSON and
  `topics.json` are read by the CLI and tests after the swap. Acceptance evidence 2, 7 and 8 check
  each before child 24.
- The largest cut of the program (the host card, about 110 KB, and `concepts.md`, about 73 KB): a
  rule lost here only shows at child 25's review and child 28's run. The inventory and the
  completeness table are the guards.
- The long gate is owed. No AGENTS.md change. No `just mod`.

## AGENTS.md change

None.

## For child 24

- `roles.yaml`'s `card` for chief-of-staff and griller must become `chief-of-staff.md` and
  `griller-skill.md` at the swap: a `SKILL.md` that runs `brief` cannot also be the card `brief`
  reads (today `../../chief-of-staff/SKILL.md` and `../../griller/SKILL.md`).
- Copy `cards-next/skills/<skill>-SKILL.md` to `skills/<skill>/SKILL.md` and check its
  `chantier-version:` line against `scripts/version.py`.
- Add the launcher's row to `hosts/claude-code.md`'s allow table and JSON block with its P10
  sample, and drop "unproved" from `host-allow-rules` then.
- The stories listed with home `incidents file` in this child's inventory.

## Open questions

1. **Byte targets for the shared files.** The program sets budgets for role cards and topics but
   none for `concepts.md`, `pr-template.md`, `release-template.md`, `status-layout.md`,
   `routing.md` and `init.md`. This child cuts them and reports their bytes as "no target". Should
   the owner set targets before child 26 freezes `budgets.json`, or should child 26 freeze them at
   the sizes this child reaches?
2. **The router's boot.** The router `SKILL.md` (`chantier`) runs no brief here: it only asks the
   role or behaves as the Chief of Staff (whose brief it then runs). If the owner wants every
   `SKILL.md` to run a brief, a router role would need a `roles.yaml` entry and a card, which no
   child carries.
