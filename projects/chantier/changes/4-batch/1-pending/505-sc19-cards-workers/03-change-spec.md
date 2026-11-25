# SC19: New cards: the workers, critics and review steps

Child 19 of 28 of the program `simplify-cards-and-prompts`. These rank above this specification,
in this order: the program's `03-change-spec.md`, its `02-answers.md` (answers 17 to 22) and its
`work/study-*.md`. Short ids such as F4, F5 and Q4 are the program's findings and questions, as the
Chief of Staff settled them in answer 22. The owner confirms answer 22 when they wake. This child
needs nothing beyond it.

This is the first of the five family children (19 to 23). Each one writes part of the target card
set as files that nothing loads. Child 24 swaps the set in.

## Goal

In the owner's words (answer 1): the cards are "far too heavy and detailed". Write "the smallest
possible cards, no behaviour lost", and use progressive disclosure to the full.

This child writes the new cards of 11 roles:

- the seven workers: coder, conflict-resolver, debugger, investigator, verifier, demo-explorer,
  spec-writer;
- the review step: inspector;
- the two critics: spec-critic, retro-critic;
- the board Griller (board-griller).

The new cards go in `skills/chantier/cards-next/`, beside the old ones. Each is within its byte
budget. Each carries only what the floor, the brief's facts, the host rows, a help topic or a
refusal do not already give. The child also writes a rule inventory of the old cards it replaces,
so that child 25 can check that nothing was lost.

## Place in the chain

- **Base: child 18's branch** (`sc18-roles-data-check`, CR-504) in the batch's single stack. The
  Driver rebases on it before the first push. Below it in the stack, and relied on here:
  - child 6 (CR-492): `just quiz <role> --cards <folder>` and its cases `evals/quiz/<role>/*.json`;
  - child 7 (CR-493): the topic format of `references/topics.json` and `chantier help`;
  - child 8 (CR-494): the host rows;
  - child 10 (CR-496): `chantier brief <role> [<unit>] --cards <folder>` and
    `skills/chantier/references/floor.md`;
  - child 18 (CR-504): `skills/chantier/roles.yaml`, whose `card` field names each role's card
    file: `<role>.md` for the workers and critics, `griller.md` for board-griller.

  If any of these is missing at the base (`brief` has no `--cards`, `floor.md` is absent, or
  `just quiz` is missing), the Driver stops and says so. There is no stand-in.
- **Depended on by:**
  - children 20 to 22, which add their families' cards and topics to the same folder and the same
    `cards-next/topics.json`;
  - child 22, which writes the Griller card around the section that this child writes (see
    section 2.3);
  - child 23, which owns the final `cards-next/topics.json`, the final `floor.md`, `concepts.md`,
    the templates (`pr-template.md` and the others) and `review-step.md`;
  - child 24, which swaps `cards-next/` in;
  - child 25, which takes this child's inventory draft as a seed.
- **Merge:** with children 19 to 28 as one unit (the program's merge rule; F11).

## Decisions carried

| Source | Decision | Where here |
| --- | --- | --- |
| Answer 1 | Smallest possible cards, no behaviour lost, progressive disclosure | sections 2 and 4 |
| Answer 3 (Q6) | No stumbling on the common path. Free stumbling on rare cases | common path in the card, rare cases in topics (section 2.4) |
| Answer 10 (Q10) | A rare incident rule with no CLI trigger becomes a help topic for one release, with its reads measured | topics with `review_by: "0.16.0"` (section 2.4) |
| Answer 12 (Q12) | Roles from outside are review steps, critics and workers, so these cards are the model an outside role copies | the card shape (section 2.1) |
| Answer 14 (Q16) | One card set. The old cards are removed at the swap, with no switch | `cards-next/` is unloaded until child 24; `references/` is untouched |
| Answer 15 (Q14) | A card is one short file, a rule lives in one place, a piece is loaded at its moment | section 2.1; no rule written twice |
| Answer 16 (Q13) | Trial history leaves the cards | no date, batch, model or trial story in a new file (M3) |
| Answers 17 and 18 | Total rewrite in one pass, then a read-and-compare review | the inventory draft (section 3) |
| Answer 22, F2 | New cards and topics are written beside the old ones as files nothing loads, one CR per family. The families merge with the swap as one unit | section 5; Merge |
| Answer 22, F4 | Quiz pass rule: no case scores 0 of 3 that the old cards passed. The spend cap is printed first | Acceptance evidence 4 |
| Answer 22, F5 | A rule that protects the user or the repository lives only in the floor, the role's card or a refusal. It is never in a topic alone and never "inferable". The cap on nevers gives way before such a rule | section 2.2; inventory column `kind` |
| Answer 22, F6 | Handed back validated, with the Known gap "real run not done (child 28)" | Handback |
| Answer 22, F11 | A typed merge wait on child 28 | Handback |
| Answer 22, F17 | An unproved claim is marked "unproved" | the cards; section 6 |
| Answer 22, F20 | State the seconds added to `just test` | Acceptance evidence 7 |
| Answer 22, Q4 | A card above its target is listed in Known gaps with its size. Only the owner raises a target | Acceptance evidence 2 |
| Program, common to 19 to 23 | `cards-next/` mirrors the target layout of `references/`. Card content: goal, ownership, about five nevers, ending, reply format. The budgets. Topics in `cards-next/topics/`, listed in `cards-next/topics.json`. The evidence: brief bytes, quiz, row list. No edit to `references/`, the CLI or the hook | sections 1 to 5 |
| Program, child 19 | Scope, depends on 18, each card's bytes against its target, long gate owed, no AGENTS.md change | the whole specification |
| Program, child 22 | The Griller card keeps a section named "Started from the board", because AGENTS.md and `src/board/griller.py` name it | section 2.3 |
| Child 10 | Child 19 copies `references/floor.md` into `cards-next/floor.md` | section 1 |
| `02-answers.md` of this CR | Specified from the program. No separate critic. Destination: running batch batch-31 | this specification as written |

## What changes

Paths are from the repository root. `src/` is `skills/chantier/scripts/cli/src/chantier/`.
"Today's card" means the file at this child's base. Its content at `origin/main` 8a960d34 is
summarised in section 4. One KB is 1,000 bytes, the way child 10 reads the floor's "1.2 KB" as
1,200 bytes. Sizes are LF bytes, measured as `git show HEAD:<path> | wc -c` so that a CRLF
checkout cannot change them.

### 1. The files this child adds

All of them are new, UTF-8 with no BOM, with LF endings:

| Path | Role or use | Budget |
| --- | --- | --- |
| `skills/chantier/cards-next/coder.md` | coder | 1,500 |
| `skills/chantier/cards-next/conflict-resolver.md` | conflict-resolver | 1,500 |
| `skills/chantier/cards-next/debugger.md` | debugger | 1,500 |
| `skills/chantier/cards-next/investigator.md` | investigator | 1,500 |
| `skills/chantier/cards-next/demo-explorer.md` | demo-explorer | 1,500 |
| `skills/chantier/cards-next/spec-writer.md` | spec-writer | 1,500 |
| `skills/chantier/cards-next/spec-critic.md` | spec-critic | 1,500 |
| `skills/chantier/cards-next/retro-critic.md` | retro-critic | 1,500 |
| `skills/chantier/cards-next/inspector.md` | inspector | 2,000 |
| `skills/chantier/cards-next/verifier.md` | verifier | 3,000 |
| `skills/chantier/cards-next/griller.md` | board-griller: only its `## Started from the board` section (section 2.3) | 2,000 for that section |
| `skills/chantier/cards-next/floor.md` | the floor, byte-identical to `references/floor.md` at the base | 1,200 (child 10's) |
| `skills/chantier/cards-next/topics/<name>.md` | this family's topics (section 2.4) | 1,500 each |
| `skills/chantier/cards-next/topics.json` | the topic index, child 7's format, this family's entries | none |

**Why these names.** They match what `brief <role> --cards <folder>` reads: `<folder>/<basename
of the role's card>` from `roles.yaml`'s `card` field, and `<folder>/floor.md` (child 10). They
also match the target layout, where the card names do not change. The topics go one level down,
as the program sets.

**`topics.json`.** It uses child 7's format: `{"version": 1, "topics": {"<name>": {"readings":
[...], "roles": [...], "trigger": "...", "review_by": "X.Y.Z"?}}}`.
- Readings are relative to `cards-next/` (child 7's are relative to `references/`). A reading is a
  `topics/<name>.md` file, or a `file#heading` with a level-2 heading. It is never an `@action`.
- `roles` names role ids from `roles.yaml`.
- `trigger` says when to read the topic: the situation, or the first words of the CLI line that
  meets it.
- Children 20 to 22 add their entries to the same file. Child 23 makes it final.

### 2. What each card holds

#### 2.1 Shape (common to the 11)

Each card holds, in this order and nothing more:

1. The `#` title: the role's name.
2. The goal, in one or two sentences.
3. What the role owns: its inputs and the one file it writes, by path pattern (for example
   `<work folder>/coder/r<n>.md`).
4. Its own nevers. About five is the target. The cap gives way before a rule that protects the
   user or the repository (F5).
5. How it ends.
6. Its reply format.
7. At most one line naming its topics: `Rare cases: \`$CHANTIER help <topic>\` (<trigger>)`.

What is left out, because it reaches the role another way (the inventory gives each item's home):

- What the brief's `=== facts` block gives: the CR, the worktree, the work folder, the PR, the
  gate, the `writes:` line, and "the project's rules rank above the card; run `$CHANTIER rules`
  first" (child 10's facts and `plugin_files.worker_prompt_lines` print it). So no "Your prompt
  gives…" paragraph.
- What the floor gives (rules 1 to 10): among them no fallback, a CLI that cannot run is a stop,
  report a refusal with its exact text, never stop a process by name or pattern, never discard
  the worktree's work, and no image showing the username or the home folder.
  - "No fallback" is written today in 7 worker cards (study-fable-v2 section 3, kind f). Floor
    rule 10 is in `coder.md:33` and `conflict-resolver.md:28`. None of these stays in a card.
- What the host rows give (`ending`, child 8).
- Anything about the cores, the manifest or startup sections. This ends the conflict between
  `role-core.md` and the worker wrappers (study-fable-v2 section 3, kind f).
- Dates, batch names, trial stories, models and "proved on" notes (M3, answer 16). An unproved
  behaviour keeps the one word "unproved" (F17).

What must not be in any file of `cards-next/`:
- the phrase `Read this short role contract at boot`. `tests/test_startup_manifest.py`'s
  `MOVED_OUT` scans every `*.md` under `skills/`;
- a `# chantier-agent:` version line;
- the old command `chantier board`. `tests/test_command_names.py` does not scan this folder, but
  child 24 moves the folder to where it does.

#### 2.2 What each card keeps

The kind-a rules (protecting) below stay in the card. They are not in the floor, so no topic may
hold them alone (F5). Reply formats the Driver or the CLI parses stay byte-for-byte as today, as
the code block in today's card. The fields the CLI reads (`Head:`, `verdict`) and the Inspector's
JSON keys are load-bearing.

- **Every worker that writes in a worktree** (coder, conflict-resolver, debugger, investigator,
  verifier, inspector):
  - never commit, push, rebase or merge (conflict-resolver has its rebase exception, below);
  - never create a worktree;
  - never run `git stash`, because the stash is shared by every worktree;
  - a write the guard refuses outside `writes:`: fix the path, never write it another way.

  Inspector, investigator before round 1, and debugger write no worktree file; each card says so
  in one line.
- **coder:**
  - tests and probes of the board's write paths use a scratch planning folder, never the live one,
    and it is removed at the end;
  - never silence a failing gate;
  - `r<n>.md` with each checklist item marked `done` or `open: <why>`;
  - the four-line reply block, at most ten lines.
- **conflict-resolver:**
  - may stage (`git add -- <path>`, never `-A`) and run `git rebase --continue`;
  - never a merge, never `--rebase-merges`, never `--exec` or `-x`;
  - always `git -C <worktree>`, never git in the main checkout;
  - never resolve with a whole side (`-X ours`, `--theirs`). Two product intents in conflict are a
    question for the Driver;
  - no new BOM before continuing;
  - `conflicts.md` holds each hunk, its choice and the fast-gate line (a missing line is out of
    format);
  - reply at most ten lines.
- **debugger:**
  - a diagnosis, not a fix;
  - CI artifacts go under `<CR folder>/work/scratch/artifacts-<run id>/`;
  - the scratch planning folder rule;
  - `diagnosis.md` holds the repro, the cause with its evidence, and the place to fix;
  - after two failed fixes, test the premise.
- **investigator:**
  - read only before round 1;
  - `investigation.md` holds the entry points, the smallest change, the risks, the questions only
    the user can answer, and the evidence plan;
  - the project's rules on evidence rank above the plan.
- **inspector** (2,000):
  - writes nothing;
  - judges at the pushed head and names its SHA;
  - a check red on the default branch is not the CR's;
  - a diff touching `hooks/` needs `just mod` in the gate record, else it is blocking;
  - a check guarding a shipped file must read the file as shipped;
  - cannot judge: `FIX-REQUIRED`;
  - the JSON reply with its exact keys and caps (items at most 300 characters, `minor` at most 5,
    reply under 3,000 characters).

  The audit lists go to a topic: the host and default matrix cells, the `git range-diff`
  carry-over, and the `pr-body.md` audit against the PR template and `02-answers.md`. The card
  names that topic.
- **verifier** (3,000):
  - the scratch project under `work/scratch`, made with `git init` and passed with `--project`.
    Never point the prompt's `$CHANTIER` at it, and never at the live planning folder;
  - `gate` only for the long gate with no pass at head, one name per argument;
  - `verify.md` with its `Head:` line, then `$CHANTIER verdict <cr> VERIFIED|"NOT VERIFIED"`,
    which is refused until `Head:` matches;
  - look at every screenshot for the username or the home folder (a check on others' images;
    floor rule 8 covers the role's own);
  - the reply block (`VERIFIED | NOT VERIFIED`, `Head:`, `Proof:`, at most six `Failed:` lines).

  These go to topics: the PR description pass, the delta assessment, the matrix probe
  (`matrix-r<n>.md`), the before-and-after on a detached base worktree (`before-after.md`), the
  patch-id carry, and the Windows long-path stop.
- **demo-explorer:**
  - started by the Chief of Staff with no CR;
  - reads the PRs, then the CRs, then the code, in a detached worktree outside the repository,
    removed at the end;
  - writes only `demo/demo.md` in `4-batch/`, in the user's language;
  - reply: the path and the questions.
- **retro-critic:**
  - the three questions (real and measured; changes an outcome; already covered);
  - writes nothing;
  - the reply lines `<n>. keep|merge with <m>|drop: <why>` and `kept <k>, dropped <d>`.
- **spec-critic:**
  - its inputs;
  - the four finding kinds (intent, inconsistency, claim, bundle);
  - writes nothing;
  - the numbered reply with draft questions of at most 4 options.
- **spec-writer:**
  - started only on the user's word that the CR is grilled enough;
  - no worktree, round or slot;
  - never commits, pushes or opens a PR;
  - writes only `03-change-spec.md` and the summary (`summary lint`, then `summary set`);
  - every decision of `02-answers.md` is carried, none dropped and none invented. An open point is
    a question, not a decision;
  - a check guarding a shipped file reads it at the head under test;
  - the reply: the path and the open questions.

  These go to a topic: the CI-job environment paragraph, the host and default matrix rule, and the
  `issue:` line placement.

Every judgment line of today's cards that is not listed above gets a row in the inventory and a
home there.

#### 2.3 The board Griller

`roles.yaml` gives board-griller the card `griller.md`. `src/board/griller.py`'s fixed `BRIEF` and
AGENTS.md name that card's section "Started from the board". Child 22 owns the Griller card.

So this child writes `cards-next/griller.md` holding the `#` title `# Griller` and one section,
`## Started from the board`, within 2,000 bytes. Child 22 writes the Griller's own text around it
and keeps that section's heading and content, changing only what its own family needs.

The section keeps, worded so the board's limits stay exact:

- headless, with no seat, watcher or hub;
- it grills only the named CR (inbox, `2-backlog/P1`...`P4` or `3-ready`);
- it reads only the project, the planning folder and the plugin's skill folder;
- it writes only in that CR's folder;
- it runs only the four commands `$CHANTIER rules`, `access`, `summary lint <folder>` and
  `summary set <folder>`, the last two on that CR's folder. These are the four that AGENTS.md says
  "the Griller card's 'Started from the board' names";
- no spec-writer, no filing, triage, abandon or restore, no labels, no issue drafts, and no
  `[griller→chief-of-staff]` line;
- it ends with the exact line `[griller→board] grilled enough: <next batch|running batch>`, which
  `src/board/griller.py`'s `GRILLED` regex reads;
- its cost is in no batch.

How it grills is in the Griller card (child 22) and not repeated here.

#### 2.4 Topics

Rare cases and procedures leave the cards for topic files. Each is at most 1,500 bytes, is named
in `topics.json`, and is named from the card's "Rare cases" line. The expected set (the Driver may
merge or split topics within the budgets, and records the final list in the PR):

| Topic | Roles | Holds |
| --- | --- | --- |
| `worker-shell` | the seven workers, inspector | one command per call (a chain passes the allow rules only if every part does); no leading assignment; no `sleep` and no background shell; read before overwriting, and edit rather than rewrite; UTF-8 with no BOM, and PowerShell 5.1's `Out-File` and `Set-Content -Encoding utf8` add one; a file that has a BOM keeps it; notes in `<work folder>/<role>/`, proof in `evidence/`, raw logs in `*.log` or `work/gates/`, never in published files; English text except a ticket comment, plan or demo |
| `verifier-scratch` | verifier | how to build and pass the scratch project; the Windows long-path stop |
| `verifier-description` | verifier | the PR description pass: renders, is consistent, has Known gaps, no username image, role names per the PR template; the Review box read through `log <cr>` |
| `verifier-delta-matrix` | verifier | the delta assessment, patch-id carry and the matrix probe (`matrix-r<n>.md`, no verdict) |
| `verifier-before-after` | verifier | the detached base worktree and `before-after.md` |
| `inspector-audit` | inspector | the matrix cells, the `range-diff` carry, and the `pr-body.md` audit against the PR template and `02-answers.md` |
| `spec-writer-extras` | spec-writer | the CI-job environment, the matrix rule, the `issue:` line |

- A topic that holds an answer-10 rare rule (an incident rule with no CLI trigger) carries
  `review_by: "0.16.0"`, the minor after 0.15.1. If the base's version is no longer 0.15.x, it is
  the next minor of that version. Each such rule is marked in the inventory.
- A kind-a rule never goes to a topic alone (F5). When the Driver is unsure whether a rule
  protects the user or the repository, it treats it as kind a and keeps it in the card.
- A topic links to `pr-template.md` and `concepts.md` by their target names, which are child 23's
  files. Each such forward link is listed in the PR (see Acceptance evidence 5).

### 3. The inventory draft (seed of child 25)

The draft is a Markdown table in this CR's folder: `<CR folder>/evidence/cards-inventory-workers.md`.
It lives in the planning folder, not the repository, as CR-471's `work/tables.md` does. Child 25
finds it by the CR id, and the PR links it. Children 20 to 23 use the same name with their family
(`cards-inventory-<family>.md`).

- **Sources covered:**
  - today's ten cards `coder.md`, `conflict-resolver.md`, `debugger.md`, `investigator.md`,
    `demo-explorer.md`, `spec-writer.md`, `spec-critic.md`, `retro-critic.md`, `inspector.md` and
    `verifier.md`;
  - the `## Started from the board` section of `griller.md`.

  Out of these sources, and left to their children: the rest of `griller.md` (child 22),
  `review-step.md`, `concepts.md`, the templates and the cores `startup-core.md` and
  `role-core.md` (child 23 and child 25).
- **One row per rule**, sentence-level: each sentence that states a behaviour, a never, a path, a
  format or an exception. Pure transitions get no row. The columns are child 25's: `id` (`W-nnn`,
  a draft id that child 26 replaces), `role`, `trigger`, `behaviour`, `source` (`file:line` at
  this child's base), `kind` (a to f, study-fable section 3), `new home`, `check`.
  - `new home` is one of: `card <file>`, `floor <n>`, `refusal <command or hook, its message
    start>`, `next: line`, `topic <name>`, `facts` (the brief's facts), `host row <id>`,
    `proof file`, `incidents file`, `inferable`.
  - `check` names what proves the row: a quiz case id, a test, a refusal's test, or "child 25".
- **Two lists at the end, for the owner** (as child 25 will give):
  - every kind-a row with its home. Each home is a card, the floor or a refusal (F5);
  - every row judged `inferable`. None of them is kind a.

### 4. Today's cards, summarised (the reading at `origin/main` 8a960d34)

Card sizes in bytes against the target, from `startup-manifest.json`'s `roles` map:

| Role | Today | Target |
| --- | --- | --- |
| coder | 4,609 | 1,500 |
| conflict-resolver | 3,893 | 1,500 |
| debugger | 3,682 | 1,500 |
| demo-explorer | 3,422 | 1,500 |
| inspector | 6,044 | 2,000 |
| investigator | 3,554 | 1,500 |
| retro-critic | 2,901 | 1,500 |
| spec-critic | 3,729 | 1,500 |
| spec-writer | 3,254 | 1,500 |
| verifier | 14,581 | 3,000 |
| board-griller | `griller.md` 10,757 (the section only is the target) | 2,000 |

- Measured reads (study-fable-v2, section 2.3): verifier 17.5 KB, inspector 6.0 to 10.9 KB, coder
  4.6 to 8.4 KB.
- The board Griller and the demo explorer have no run seen.

The Driver re-measures every figure at its base. The base figures are the ones the PR gives.

### 5. Keeping the new files unloaded until the swap

- No file outside `skills/chantier/cards-next/` names `cards-next/` as a path to read. That
  covers `startup-manifest.json`, `references/topics.json`, `roles.yaml`, any `SKILL.md`, the
  wrappers in `agents/` and `com.github.copilot/agents/`, `src/`, `hooks/` and `scripts/`.
  - Children 6 and 10 may name it as a `--cards` argument in usage text or docs. That is an
    argument, not a load.
- No change to `roles.yaml`, the wrappers, `src/`, `hooks/`, `references/` (the floor is copied,
  not moved), `scripts/version.py` or any test.
- `help` reads only `references/topics.json` (child 7). The new `cards-next/topics.json` is
  therefore not served until child 24.
- No test is added. No test reads `cards-next/` on purpose. The two tests that glob all of
  `skills/**/*.md`, `test_startup_manifest.py::test_moved_rule_is_gone_from_where_it_was` (the
  phrase in section 2.1) and `test_role_cards_split.py` (whose `_linking_files` reads
  `references/`, `skills/*/SKILL.md`, `CONTRIBUTING.md`, `evals/README.md` and `docs/`, not
  `cards-next/`), stay green with the new files present.
- The package build (`uvx --from <plugin root>`) may carry the folder as data. Nothing reads it.

## Out of scope

- Any edit to `references/`, `roles.yaml`, a wrapper, a `SKILL.md`, `src/`, `hooks/`, a test,
  AGENTS.md or a version.
- The cards of the Drivers (child 20), the Foreman (child 21), the Chief of Staff and the Griller's
  own text (child 22), and `review-step.md`, `concepts.md`, the templates, `routing.md`,
  `init.md`, `forges/`, the host topics, the final `floor.md` and the final `topics.json`
  (child 23).
- The swap, the CLI output switches and the test conversions (child 24).
- The committed inventory `docs/proofs/cards-inventory.md`, restoring rows with no home, and the
  grouped inferable quiz cases (child 25).
- Rule ids, `rules.json`, budget and M3 lints (child 26).
- A real run (child 28).
- Raising any budget: only the owner does that (Q4).

## Acceptance evidence

Each item is recorded in the PR or under `<CR folder>/evidence/`, from the head pushed.

1. **The files.** The PR lists the files under `skills/chantier/cards-next/`. Two commands run at
   head and are quoted:
   - `git diff --stat <base>..HEAD` shows changes under that folder only;
   - `git show HEAD:skills/chantier/cards-next/floor.md | cmp - <(git show HEAD:skills/chantier/references/floor.md)`
     (or its PowerShell equivalent) shows no difference.
2. **Bytes against the budgets.** A table with one row per role: today's card bytes, the new card
   bytes (for board-griller, its section's bytes), the target, and "within" or "over by N".
   - Every card is read from git at head (`git show HEAD:<path> | wc -c`), never from a prepared
     copy.
   - Every topic file is at most 1,500 bytes.
   - A card over its target is listed in Known gaps with its size (Q4).
3. **Brief bytes.** For each of the 11 roles, `brief` is run against the old and the new cards:
   - the old: `$CHANTIER brief <role> <unit>` (the old cards at the base);
   - the new: `$CHANTIER brief <role> <unit> --cards <worktree>/skills/chantier/cards-next`;
   - each run on each host that child 10's `brief` selects;
   - the units are child 10's: this CR's id for the worker roles and the inspector, this CR's
     folder for spec-writer, spec-critic and board-griller, none for retro-critic and
     demo-explorer.

   The table sets each role's two brief sizes beside study-fable-v2's declared boot (for example
   verifier 24,030, inspector 15,484, coder 14,000, board-griller 19,748). Each new brief builds
   with exit 0: a missing file exits 2.
4. **Quiz under F4.** For each role of this family that has cases under `evals/quiz/<role>/` at the
   base (at least coder, conflict-resolver, debugger, verifier and demo-explorer, from child 6's
   seeds), run `just quiz <role> --cards skills/chantier/cards-next --against <child 6's baseline>`.
   - The spend plan line is printed first, under the default `--max-usd` cap of 10.
   - Pass: no case scores 0 of 3 that the old cards passed.
   - A failing case brings its rule back into the card (within budget, else Known gaps), and the
     case is run again.
   - Unproved: a Driver may be unable to start the headless host CLI. If it is refused, the
     Driver hands back with the cards written and says so. The Chief of Staff runs the quiz. There
     is no workaround (child 6's Risk).
   - Quiz boots come from `brief` and do not include topics. A case whose rule moved to a topic
     is therefore a real test that the rule was rediscoverable or inferable.
5. **Links.** Every relative link in the new files is listed with its target:
   - it resolves inside `cards-next/` at head; or
   - it is a forward link to a file a later family child writes (`pr-template.md`, `concepts.md`,
     `review-step.md`), named with that child.
   - No link points into `references/`.
6. **The inventory.** `<CR folder>/evidence/cards-inventory-workers.md` (section 3) is complete:
   - every rule sentence of the sources has a row, and the Driver states how it walked them
     (file by file, line by line);
   - no row has an empty `new home`;
   - every kind-a row's home is a card, the floor or a refusal (F5);
   - no `inferable` row is kind a;
   - each reply format is unchanged: a diff of each old reply block against the new one is empty.
7. **`just test`.** 0 s added: no test is added or changed. The Driver records the `just test` time
   at the base and at head on the same machine.
8. **Unloaded.** `git grep -n "cards-next" HEAD -- . ':(exclude)skills/chantier/cards-next'` is
   quoted. Every line it shows is usage text or a doc naming the folder as a `--cards` argument,
   never a default path a loader reads (section 5).
9. **Gates.**
   - Before the first push, `just check` at the rebased head. `just eval-dry-run` is not owed: no
     change under `src/` or `evals/kit/`.
   - The long gate `just scenario (ubuntu-latest)` green at the PR's head (a card change).
   - The local Windows run `chantier gate <cr> scenario` is owed only by the stack's top child.
   - `just mod` is not owed: no change to `hooks/` or `types/`.

## Handback

- Handed back validated, with the Known gap "real run not done (child 28)" (F6), and any card over
  its target with its size (Q4).
- The typed merge wait `$CHANTIER wait <cr> merge <child 28's PR>` is recorded once child 28's PR
  exists. Until then, the PR's Known gaps say "do not merge: merges with children 19 to 28 as one
  unit, after child 28's campaign". Nothing merges while the owner sleeps.

## Risk

- Low on the running product: nothing loads the new files until child 24.
- A wrong cut here only shows at child 24's swap and child 28's run. The quiz (item 4) and the
  inventory (item 6) are the guards before them.
- The long gate is owed. No AGENTS.md change. No `just mod`.

## AGENTS.md change

None.

## Open questions

1. **Board-griller's boot at the swap.** Child 10's `brief` puts the whole card file in the brief.
   Once child 22 writes the Griller's text around the section, the board Griller's brief will
   carry the whole Griller card (about 4 KB) plus its 2,000-byte section, not 2 KB. Here the
   budget is measured on the section, and the brief bytes are reported as they are. Should the
   board Griller's 2 KB budget cover its whole brief? If so, child 22 or child 24 must make
   `brief board-griller` print the section only, a CLI change none of them carries today.
