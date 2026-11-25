# SC19 + SC20: New cards: the workers, critics and review steps; New cards: the CR, stack, QA and release Drivers

This CR carries children 19, 20 of the program `simplify-cards-and-prompts` in ONE Driver, ONE PR, in this order, as the owner asked on 2026-11-25 ("regroupe les CR entre elles pour en faire des plus grosses"). Each part below is the full Change Specification of one child, unchanged: do them in order, one after the other, commit by commit. Where a part says "child N's branch", "on child N" or "waits for child N" and child N is another part of this CR, it means the earlier part of this same branch, not another PR. The gates of the parts are all owed, run once at the PR's head (the strictest part decides which long gate). If the context runs short, hand back with the exact state at about 100k tokens: parts done, parts left. The answers of every part are appended to this folder's `02-answers.md`.


---

# PART 1 of 2: SC19: New cards: the workers, critics and review steps

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


---

# PART 2 of 2: SC20: New cards: the CR, stack, QA and release Drivers

Child 20 of 28 of the program `simplify-cards-and-prompts`. The program's `03-change-spec.md`
("Common to children 19 to 23", "Child 20"), its `02-answers.md` (answers 17 to 22) and
`work/study-*.md` rank above this file. Where they say more than this file, they win. Child 19's
specification (`1-inbox/sc19-cards-workers/03-change-spec.md`) fixes where the new files live, the
budgets and the proof method for the whole family of card children. It was not written when this
file was written. This file follows the program's text on those three points. If child 19's
specification says otherwise, child 19's wins, and the Driver follows it without asking.

## Intent

Write the four Driver cards of the target card set, with their help topics, in
`skills/chantier/cards-next/`, a folder that nothing loads. The cards are for the CR driver, the
stack driver, the QA driver and the release driver.

Today the four Drivers share `skills/chantier/references/driver.md` (54,955 bytes on `origin/main`
8a960d34) and 16 pieces of about 82 KB. Study-fable-v2 measured what they read at the start: the
CR driver 44 KB (n=279), the stack driver 56 KB, the release driver 28 KB, and no run of the QA
driver. The target is a card of 4, 4, 3 and 2 KB, plus the floor and one host row. Every rare case
moves to a help topic, a `next:` line, a refusal or `--help`.

## Place in the chain

- **Base:** child 19's branch, the batch's stack top when this child joins (program rule F16).
- **Builds on:**
  - child 1: `chantier push`;
  - child 6: the quiz cases and the baseline of the old cards;
  - child 7: the topic format and today's Driver topics;
  - child 8: host capabilities and rows;
  - child 10: `brief` with `--cards`, and the floor;
  - child 12: `next` and the `next:` lines;
  - child 13: `msg steering`;
  - child 18: `roles.yaml`;
  - child 19: `cards-next/`, its `floor.md`, and the first `cards-next/topics.json` if child 19
    writes one.
- **Next:** child 21 (the Foreman) builds on this branch. Child 21 adds the Foreman's side to the
  shared topics this child starts (`lease`, `refused-push`).
- **Later children:**
  - child 23 writes the shared cards this child's cards link to (`concepts.md`, `pr-template.md`,
    `release-template.md`, `forges/`), the final `topics.json` and the final `floor.md`;
  - child 24 swaps the set in and points each Driver role at its own card;
  - child 25 reviews every removed rule.
- **Merge:** under the program's merge rule (answers 14 and 22: F2, F11, Q8).
  - The merge waits for the owner.
  - Children 19 to 28 merge as one unit, in order, in one sitting, with no session started in
    between.
  - They merge only after child 28's campaign has passed.
  - The Driver records `$CHANTIER wait <cr> merge <child 28's PR>`. If child 28's PR does not
    exist yet, it records the wait on child 28's CR with a `--note` that says so, and the steering
    session updates it.

## Decisions carried

| Source | Decision | Where in this CR |
| --- | --- | --- |
| Answer 1 | No role is added, removed or merged, and no role's responsibility changes | the four cards keep today's duties |
| Answers 14, 17; F2 | Total rewrite, written beside the old set, nothing loaded until the swap | `cards-next/` only |
| Answer 8; F3 | The refused-push route stays for good: the Driver hands back, the steering session runs the push | topic `refused-push` |
| F21 | `chantier push` is a Driver's one way to publish its branch. It never retries a refused `git push`, and a refused `chantier push` is never followed by a raw push | CR, stack and release cards; topic `refused-push` |
| Q6 | The steering session keeps the plain `git push --force-with-lease` | named in topic `refused-push` as the steering session's step, not the Driver's |
| F5 | A rule that protects the user or the repository lives in the floor, the card or a refusal, never in a topic alone. The cap on nevers gives way before such a rule | each card's nevers |
| Answers 4, 13; F8 | `msg steering anomaly|blocked|note`. With no watcher it prints `not delivered` and exits non-zero. Then the Driver uses its host means or the hand-back | CR, stack and release cards |
| Answer 11 | `next` is advice. Safety steps are refusals | cards point to `next:` lines; no step lists |
| Answer 10 | A rare incident rule with no CLI trigger becomes a topic with `review_by` set to the next minor version | `topics.json` rows |
| Q4 | Budgets are targets. A card or topic above its target is listed in Known gaps with its size | evidence |
| M3 | No dates, batch names or trial stories in a card or topic | all files |
| F17 | An unproved claim is marked "unproved" | all files |
| F20 | The child states the seconds it adds to `just test` | evidence |
| Pending item `driver-card-leads-left-by-role-cards-sti` | Three leads carried as card lines or topics | section 4 |
| Pending item `release-drafts-are-a-worker-s-job-not-th` | The release driver's card is written as the release driver works today. That item changes it after the swap | out of scope |
| Pending item `driver-context-second-cut` | Absorbed here for the Drivers' cards and topics. Prompts, manifest, `take` and `handoff` go to children 10 and 24 | section 1 |

## What changes

All files are new, under `skills/chantier/cards-next/`. Sizes are LF bytes. No existing file
changes.

### 1. Four Driver cards

One file per role. There is no shared Driver card: study-fable 4.2 sets one boot per role (card,
floor and host row), and a shared card would load the other three roles' text.

| File | Role (`roles.yaml` name) | Target |
| --- | --- | --- |
| `cards-next/cr-driver.md` | `cr-driver` | 4 KB (4,096) |
| `cards-next/stack-driver.md` | `stack-driver` | 4 KB (4,096) |
| `cards-next/release-driver.md` | `release-driver` | 3 KB (3,072) |
| `cards-next/qa-driver.md` | `qa-driver` | 2 KB (2,048) |

Each card has the five parts of the common rules, in this order:
1. the role's goal;
2. what it owns;
3. its nevers;
4. how it ends;
5. its reply format.

A card holds nothing that is already in one of these:
- the floor (`cards-next/floor.md`: rebase only, no fallback, a CLI that cannot run, never discard
  the worktree's work, refusals verbatim, no process stopped by pattern);
- a topic;
- a CLI refusal;
- a `next:` line (round, gate, push, ship, verdict, handback: child 12);
- a command's `--help`;
- the host rows that `brief` adds (message steering, start a child, ending, compacting, write
  guard: child 8's capabilities `driver-hand-back`, `driver-messages-steering-direct`,
  `start-driver`, `end-turn-background`, `stop-own-background-task`, `compact`, `write-guard`,
  `driver-start-folder`).

A card names a capability by its id (`chantier host <id>`) and restates no row. A card names a
topic as `chantier help <topic>`, with the moment that sends the role there.

**`cr-driver.md`**, from `driver.md` "CR driver", "CR driver: ship and proof", "CR driver: the
closing" and the shared "Means:" sections:

- *Goal:* take one CR from its specification to a green PR, proved at its pushed head, and hand
  it back.
- *Owns:*
  - git and the forge for its own CR branch, by the project's rules;
  - the worktree's commits;
  - `<work folder>/pr-body.md`, its notes and, when `take` prints an archive path, the archive.

  Every change to a project file goes through a `coder`. Its own reading of code is an
  `investigator` or a `debugger`. The `Team:` review steps run in order.
- *Steps:* one line saying that `chantier next <cr> --lease <n>` and the `next:` line at the end of
  each command give the next step. The card lists no step order that `next` gives.
- *Lines no tool carries, kept short:*
  - every `APPROVE` is noted at once, with its `head`, before any other step;
  - a box of `pr-body.md` cites only a recorded note;
  - a gap is written in the body's Known gaps first;
  - the PR is opened as a draft, from `pr-template.md` (child 23) or the project's own template;
  - the body is a file, posted from that file;
  - the evidence plan is the Driver's;
  - the closing at 115,000 tokens or more is a `context: closing:` hand-off (topic `closing`).
- *Nevers*, from five, more where F5 asks:
  1. edit no project file itself, the shell included;
  2. publish the branch only with `chantier push <cr> --lease <n>`, and never retry a refused push
     by another means (F21; topic `refused-push`);
  3. never call the host's hand-back before `$CHANTIER handback` is accepted;
  4. never `git stash`, never `git add -A`, never a merge commit (rebase only: floor 2);
  5. never comment on, close or reopen an issue;
  6. never turn a PR ready on a base other than the default branch.

  Each of these protects the repository or the user, so the cap gives way before it (F5).
- *End:* background tasks stopped first (`chantier host stop-own-background-task`), then
  `handback ready|blocked`, then the host's hand-back, whose first line is the line `handback`
  printed. The reasons and forms of a hand-back are in `handback --help` and topic
  `handback-other`.
- *Reply format:* the one line `handback` printed, unchanged.

**`stack-driver.md`**, from "Stack driver" and the four `stack-driver-*` pieces:

- *Goal:* one native stack on the forge, read back as ready to merge, with its mergeable part
  ready and the drafts on top.
- *Owns:* the order of the stack (`stack <cr>…`), and the rebase and push of every CR with no live
  Driver (`chantier push <cr> --lease <n> --unit stack`, one command per branch). It also owns
  `forge-stack`, the turning ready of the mergeable part, and heavy CI at the top.
- *Nevers:*
  1. never rebase or push a `working` CR's branch;
  2. open no PR;
  3. edit no project file;
  4. never a loop or a script over branches;
  5. never read matching forge bases as proof of the chain. Check with
     `merge-base --is-ancestor`, and an exit code other than 0 or 1 is not "based".
- *Topics:* `stack-restack`, `stack-make`, `stack-joins`, `stack-changes`, `lease`,
  `refused-push`, `conflicts`.
- *End and reply:* `[stack→foreman] hand-back …` through the host's hand-back, after
  `forge-stack show` passed its five checks (topic `stack-make`).

**`release-driver.md`**, from "Release driver" and the four `release-driver-*` pieces:

- *Goal:* run one release CR by the project's own procedure, adding nothing from habit.
- *Owns:*
  - the version (from the specification; otherwise from its own pick, explained in the PR and a
    note, never asked);
  - the release PR, ready on the default branch and a draft on any other base;
  - `phase <cr> release "<step>"` at each step;
  - `release start|go|published`.
- *Nevers:*
  1. no irreversible action without `release go` for that action (floor 6);
  2. never fix code, and start no children: a defect becomes `<work folder>/fix-<n>.md` and
     `handback blocked fix:`;
  3. never undo half-done irreversible work: `blocked question:` says what is out;
  4. never post the announcement thread;
  5. publish only with `chantier push`.
- *Lead 1:* the line on the typed `pipeline` wait (section 4).
- *Topics:* `release-notes`, `release-ship`, `release-merged`, `release-end`, `lease`,
  `refused-push`.
- *End and reply:* the line `handback` printed.

**`qa-driver.md`**, from "QA driver":

- *Goal:* use the project as its user would, at the head of the default branch, and report what
  breaks.
- *Owns:* a detached worktree of its own, removed at its end. It also owns the work folder:
  `04-result.md` (one finding per bullet, with steps, expected and actual, or "No findings.") and
  `evidence/`.
- *Lease:* `lease O-k renew --lease <n>` at each wake, and `lease O-k hold` before a long test
  (topic `lease`).
- *Nevers:*
  1. never test an unmerged PR;
  2. never fix, and start no children;
  3. report nothing it has not reproduced;
  4. keep no screenshot that fails the look (floor 8; topic `pr-extras`).
- *End and reply:* `[qa→foreman] qa done <folder> <n> findings` through the host's hand-back. The
  QA driver cannot send `msg steering` (child 13).

### 2. Driver topics

Each topic is one file, `cards-next/topics/<name>.md`, with a target of 1.5 KB (1,536 bytes). Each
gets one row in `cards-next/topics.json`, in child 7's format:
- `version` 1;
- `readings` relative to `cards-next/`;
- `roles` from `roles.yaml`;
- `trigger` quoting the CLI line's start in backticks where a line names the topic;
- `review_by` optional, as `X.Y.Z`.

If child 19 has written `cards-next/topics.json`, this child adds its rows to it. If not, it
creates the file with `version` 1 and the `paths` key of child 7's file. Child 23 finalizes it.

Rule for names: every Driver topic name in child 7's table stays, so `help --for <role>` and any
CLI line that names one (`help lease`, `help refused-push`) still resolves after the swap. A topic
too big for its target may be split into new names. The old name then stays as the row whose
`readings` list the parts.

| Topic | Roles | Substance (source on `origin/main`) |
| --- | --- | --- |
| `lease` | D | renew, `hold` (45 min by default, 90 at most), `not confirmed`, `claim lost` (stop at once, record nothing more), `take --reclaim` (`driver-session.md`, "the lease"). Child 21 adds the steering side as a second reading |
| `refused-push` | D | section 3 below (`driver-refused.md`) |
| `retake` | `cr-driver` | a first `take` that shows a `PR:` link; carried verdicts; `at <head7> (carried from <sha7>)` (`driver-retake.md`) |
| `restart` | D | a `take` note `resume:`, `rebase:`, `context:` (`driver.md`, "a Driver started again") |
| `checkpoints` | D | checkpoint commits and their messages (`driver-session.md`) |
| `steering-messages` | D | `msg steering` kinds and what wakes the steering session (answer 4); the host means when `not delivered`; `inbox` (`driver-session.md`) |
| `trouble` | D | a worker that fails, escalation, a remote command that fails, stopping a long gate, a git command in the wrong place (`driver-trouble.md`, 13,350 bytes: split, see the naming rule) |
| `ci` | D | the forge's checks as the only source, the head first, "no CI" seen in two looks a minute apart, the note's form, a failure log saved under the work folder; with leads 2 and 3 (section 4) (`driver.md`, "CI"; `driver-trouble.md`, "CI beside the long gate", "CI lists no check") |
| `conflicts` | D | a carry, a conflict, the early push, `ship --conflict`, a move after a judgment (`driver-conflicts.md`) |
| `handback-other` | D | hand-backs out of the ordinary, `--wait`, `blocked waits:`, `--no-gate` (`driver-handback-other.md`) |
| `closing` | `cr-driver` | the four closing steps and their notes, and the 115,000 and 130,000 token rules (`driver.md`, "CR driver: the closing") |
| `pr-extras` | D | the archive in the PR, images and the look, GitLab forms (`driver-pr-extras.md`) |
| `matrix` | `cr-driver` | the matrix probe, the board's write paths (`driver-matrix.md`) |
| `stack-restack` | `stack-driver` | the restack pass, `restack:` notes, resuming (`stack-driver-restack.md`, "Recording a restack", "Resuming") |
| `stack-make` | `stack-driver` | making the stack, the five checks, the final-order take (`stack-driver-make.md`) |
| `stack-joins` | `stack-driver` | a join, a draft turning ready, a merge, a deadline (`stack-driver-joins.md`) |
| `stack-changes` | `stack-driver` | an insertion, a drop, a hold, a park, a conflict, heavy CI (`stack-driver-changes.md`) |
| `release-notes` | `release-driver` | the notes, the drafts, the PR body (`release-driver-notes.md`) |
| `release-ship` | `release-driver` | the release PR; a `ship` refused in an ordered batch (`release-driver-ship.md`) |
| `release-merged` | `release-driver` | after the merge (`release-driver-merged.md`) |
| `release-end` | `release-driver` | the end (`release-driver-end.md`) |

`D` stands for `cr-driver`, `stack-driver`, `qa-driver` and `release-driver`, limited to the
roles the topic serves (the QA driver gets `lease`, `trouble` and `pr-extras` only).

**`review_by`.** Answer 10 sets it to the next minor version after the version in
`.claude-plugin/plugin.json` on the base (`X.(Y+1).0`). It goes on each topic that only holds rare
incident rules with no CLI trigger: the `trouble` parts on a git command in the wrong place and on
stopping a long gate, `matrix`, and the GitLab-forms part of `pr-extras`. The PR lists which rows
carry it and why.

No rule that F5 names (the floor's rules, and the nevers above) lives in a topic alone. A topic
may repeat the command form of a never, but never the never itself.

### 3. The refused-push route (answer 8, F3, F21), topic `refused-push`

The Driver's side, written for `chantier push` (child 1):

- **`chantier push` exits 4** (`push <cr>: git refused the push of <branch>; nothing recorded`,
  then git's text): the remote moved or refused.
  1. `note <cr> "refused: chantier push <cr> -> <git's exact text>"`.
  2. Never retry, and never run a raw `git push` (F21).
  3. Hand back `blocked refused <exact text>` (floor 9).
- **The host refuses the command** (`chantier push`, or `git rebase` before it), with the work
  committed:
  1. `note <cr> "refused: <exact command> -> <host's exact text>"`.
  2. `note <cr> "next after push: <steps>"`.
  3. `handback <cr> blocked waits: push <branch> <expected remote sha> <local sha>`. For a rebase,
     the hand-back is `waits: rebase <branch> <base>`.
  4. Send the line `handback` printed, and end.

  The steering session runs the plain `git push --force-with-lease` (Q6). That side is children
  21 and 22's, and child 21 adds it as a second reading of this row.
- **A fresh Driver** reads the `push:` answer in its `take` notes:
  - `pushed`: go on from the `next after push` note;
  - `push failed`, or `push refused … no long gate`: as the note says;
  - any other refusal: `blocked refused <exact text>`.
- The ladder: Driver, steering session, Chief of Staff, user.

The topic quotes the triggers `` `push <cr>: git refused the push` `` and a host's refusal of
`chantier push`. The cards name it in their push never.

### 4. The three leads (`1-inbox/driver-card-leads-left-by-role-cards-sti`)

1. **The typed `pipeline` wait for a long run on main.** One line in `release-driver.md`: a step
   that waits for a long pipeline on the default branch is recorded as a typed wait, either
   `handback <cr> blocked <reason> --wait pipeline=<sha>` or
   `wait <cr> add pipeline --ref <sha> --link <PR link> --note "<text>"` when the release driver
   goes on with other steps. It never polls. `release-merged` gives the details.
2. **Read a project guideline by section, not whole.** One line in each of the three pushing
   Driver cards' "owns" part: after `$CHANTIER rules`, read the first instruction file whole, and
   any other guideline only by the section that touches the step (Grep the heading, then Read with
   an offset and a limit).
3. **Wait only in a background shell.** One line in `cr-driver.md` and `stack-driver.md` (and in
   topic `ci`): a long wait (CI, a long gate's end) is one command in a background shell, followed
   by `lease <unit> hold --lease <n>`, then the end of the turn (`chantier host
   end-turn-background`), so the command's end wakes the Driver. Topic `ci` adds: "A Monitor tool
   used from a subagent is unproved; use the background shell" (F17).

### 5. Evidence helpers, outside the repository

`brief` (child 10, read through `roles.yaml` since child 18) with `--cards <folder>` reads
`<folder>/<the role's card file>`. On the base, that card file is `driver.md` for all four
Drivers. Child 24 points them at the four new files. Until then, the Driver builds one staging
folder per Driver role in the session's scratch folder, never in the repository:
- `driver.md`, a copy of `cards-next/<role>.md`;
- `floor.md`, a copy of `cards-next/floor.md`;
- `topics/` and `topics.json`, copied from `cards-next/`.

It runs `brief` and `quiz` with `--cards <staging folder>`. This is the program's single method
(`brief`/`quiz --cards`), fed with this family's files. The PR's Internal references name the
staging step. See question 1.

## Out of scope (must not)

- Any edit to `skills/chantier/references/`, the CLI (`src/`), `hooks/`, `types/`, the wrappers in
  `agents/` and `com.github.copilot/agents/`, the four `SKILL.md`, `roles.yaml` or
  `startup-manifest.json` (common rules; child 24 points the card paths).
- The shared cards and templates in `cards-next/` (`concepts.md`, `pr-template.md`,
  `release-template.md`, `forges/`), the host topics, the final `topics.json` and the final
  `floor.md`: these are child 23's. This child links to them by their target names.
- The Foreman's and the Chief of Staff's sides of the refused-push route and of `lease`: children
  21 and 22.
- New quiz cases or any change under `evals/` (child 25 writes cases for rows it finds uncovered).
- The release-drafts pending item: it changes the release card after the swap.
- Removing any old file: child 24.
- Any change to what a role is responsible for (answer 1).

## Acceptance evidence

All of it in the PR, at its pushed head.

1. **Bytes.** A table of LF bytes per new file (`wc -c` after `tr -d '\r'`, or the Python
   equivalent), against each target. Each file above its target goes in Known gaps with its size
   (Q4).
2. **Boot per role.** The bytes of `brief <role> --cards <staging folder for role>` for
   `cr-driver`, `stack-driver`, `release-driver` and `qa-driver`. They stand beside the old start
   readings (44, 56 and 28 KB, and "no run" for QA, from study-fable-v2) and beside the boot
   targets (6, 6, 5 and 4 KB, study-fable 4.2).
3. **Quiz under F4.** For each role, `just quiz <role> --cards <staging folder> --against
   evals/results/quiz-<date>-baseline-old-cards-<role>.json --save cards-next-<role>`, with the
   default cap (`--max-usd 10`) and `--plan` printed first.
   - No case may score 0/3 that the old cards passed.
   - It must show the `cr-driver` cases whose `rules` hold `floor-1`, `floor-2`, `floor-5` and
     `floor-9`.
   - A role with no case (likely `qa-driver`) is reported "no case".
   - If a Driver cannot run headless `claude -p`, it hands back with the commands and the staging
     folders, and the Chief of Staff runs them (child 6's risk). The Known gap names it until then.
4. **Links.** Every relative link and `chantier help <topic>` name in the new files resolves
   inside `cards-next/`. The exceptions are the files child 23 writes, listed by name in the PR. A
   short script run from the scratch folder prints the check, and its output goes in the PR.
5. **`topics.json`.** It loads with child 7's loader pointed at it: `load_topics(path)`, the
   tests' path form. Every reading exists, every role is in `roles.yaml`, and every `review_by`
   matches `X.Y.Z`.
6. **Rule rows for child 25.** A list in the PR (and in `evidence/cards-inventory-drivers.md` of the CR folder) of
   the old rules the family covers. Each rule of `driver.md` and of the 16 pieces gets a row:
   - its source line;
   - where it went: card, topic, floor, refusal, `next:` line, `--help`, or "inferable" with its
     reason;
   - never "inferable" for an F5 rule.
7. **The leads.** The three lines of section 4, quoted with their file and line.
8. **Gates.** `just check` green. The long gate `just scenario (ubuntu-latest)` green at the PR's
   head (a card change owes it). The local `chantier gate <cr> scenario` is owed only if this CR is
   the top of the stack, by AGENTS.md's stack rule. `just eval-dry-run` and `just mod` are not owed
   (no change under `src/`, `evals/kit/`, `hooks/` or `types/`).
9. **`just test`: 0 seconds added.** No test file changes, and no test reads `cards-next/` (on
   `origin/main` no test globs the cards folder; `test_board_read_key.py` reads only
   `references/*.md`). The PR states the measured `just test` time before and after.
10. **The merge wait** on child 28, recorded.
11. **Known gaps:** at least "real run not done (child 28)", each file above its target, and the
    staging step for `brief`/`quiz` until child 24.

## Risk

- Long gate owed. No AGENTS.md change. No `just mod`.
- Quiz spend falls on the user's machine, capped at $10 per call and printed first. Four roles
  cost at most $40 if each call reaches its cap.
- Headless `claude -p` from a Driver is unproved (child 6). See the fallback in evidence item 3.
- The cuts are deep (about 137 KB down to about 13 KB of cards plus topics). A rule cut without a
  home is caught by child 25's review, so the row list (evidence 6) must be complete.
- The release driver's new attempt today runs `git reset --hard <base>` in its worktree, which
  floor 5 forbids in general. See question 2.

## AGENTS.md

None.

## Open questions

1. sc20-Q1 (scope, method): `brief --cards <folder>` reads `<folder>/driver.md` for every Driver
   role until child 24 changes `roles.yaml`. That makes the staging folders of section 5 needed.
   Should an earlier child (10 or 18) make `--cards` prefer `<folder>/<role>.md` when it exists, so
   that children 20 and 23 run `--cards skills/chantier/cards-next` as written? Default if
   unanswered: staging folders in scratch; child 24 points the paths.
2. sc20-Q2 (behaviour, risk): today the release driver starts a new attempt with
   `git -C <worktree> reset --hard <base>`, and floor 5 says never discard the worktree's work.
   Should the new card require a new worktree for each attempt (`git worktree add` on the base,
   the old one removed by the steering session), keeping the floor without an exception? Or should
   it keep `reset --hard` as a named exception in the release card? Default if unanswered: a new
   worktree per attempt, no exception, with the change named in the PR for child 25.

