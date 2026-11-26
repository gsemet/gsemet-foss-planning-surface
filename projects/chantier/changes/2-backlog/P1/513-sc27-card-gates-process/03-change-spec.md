# SC27: The retro ladder, the approval reminder, the measure's place

Child 27 of 28 of the program `simplify-cards-and-prompts`. These rank above this specification,
in this order: the program's `03-change-spec.md` ("Child 27", "Rules for every child", the merge
rule), its `02-answers.md` (answers 9 and 17 to 22) and its `work/study-behaviour.md` section 5
(the M rules). One Driver, one PR, in the running stack batch (batch-31). Code read: `origin/main`
at `8a960d34` (chantier 0.15.1), plus the specifications of the children below it. Short forms:

- `src/` is `skills/chantier/scripts/cli/src/chantier/`;
- `tests/` is `skills/chantier/scripts/cli/tests/`;
- `references/` is `skills/chantier/references/` (after child 24's swap, the only card set).

Issue: none (a child of the program; no tracker issue).

## Goal

The owner's words (answers 1 and 9): the cards are the residue of dozens of retros, each adding a
small correction; the rewrite must not grow back. Child 26 makes the measurable rules pytest
gates (budgets, history lint, rule ids). This child adds the process gates that pytest cannot
hold, so that a later card change keeps the budgets and the measure:

- **M5, the retro-fix ladder.** A retro point says where its fix lands (`home:`), how often the
  problem was seen (`count:`) and why it cannot be code (`why not code:`). The Retro critic drops a
  point without them; `chantier validate` reports one, read-only.
- **M6 and F13, a frequency floor for prose.** A PR that adds card text quotes the measure line it
  rests on, or the owner's line quoting the user's words from the CR's `02-answers.md`; the
  Inspector judges it.
- **M10 and M14, the S-list answered.** A new `evals/results/behaviour-accepted.md` holds the
  accepted stumbling; the measure flags an accepted line whose rate has doubled; after each
  release retro the Chief of Staff files or answers every line.
- **M11 and F13, ownership.** A CI step warns, on a pull request, when the floor or the budgets
  change without the owner's approval line. It is a reminder: it never fails a job.
- **M7's place.** The release claims carry `just behaviour` for the version, newer than the last
  card change, or say why there is none.

## Place in the chain

- **Base: child 26's branch** (`sc26-card-gates-pytest`), in the batch's single stack. The Driver
  rebases on it before the first push. Relied on below it, and the Driver stops and says so if
  one is missing at the base (no stand-in):
  - child 5 (CR-491): `evals/kit/behaviour.py`, `just behaviour`, the results files
    `evals/results/behaviour-<date>-v<X.Y.Z>.json` and `.md` (or the date-first form if
    `evals-rework` merged), their keys (`cards_commit`, `roles.<role>.cli.usage_errors`,
    `roles.<role>.cli.refusals`, `roles.<role>.tool_not_in_list`, `s_list`, `regressions`), the
    dry-run case `behaviour` and its fixture `evals/kit/behaviour-fixture/`;
  - child 6 (CR-492): `just quiz` and its case files (a new rule's quiz case goes there);
  - child 7 (CR-493): `references/topics.json` and the topics;
  - child 16 (CR-502): `chantier retro draft`, its point format and its draft markers
    (`<!-- chantier retro draft:` ... `<!-- end of chantier retro draft -->`);
  - children 19, 21, 22 (CR-505, 507, 508) and child 24 (the swap): `references/retro-critic.md`,
    `references/inspector.md`, the topics `inspector-audit` and `release-chief`, the Foreman's
    `retro` topic;
  - child 26: `references/floor.md`'s ids, `references/budgets.json`, `references/rules.json`,
    `tests/test_card_budgets.py`, the M3 lint and the M4 registry test. Its specification is
    written in parallel with this one; this file uses only what the program fixes for child 26
    (file names, M1, M3, M4, M8, M13). Where child 26's specification fixes a detail (a field
    name, a test name), the Driver follows child 26's.
- **Depended on by:** child 28 (`cards-real-run`), the top of the stack. Child 28 files or
  accepts its campaign's S-list through this child's file (M10) and asks a budget raise with this
  child's line (M11).
- **Merge:** with children 19 to 28 as one unit, after child 28's campaign (the program's merge
  rule; F11). This child records a typed merge wait on child 28.

## Hand-over notes addressed to child 27, gathered

Every note the program and the specified children leave for this child. Each is carried in the
section named.

| # | From | Note | Here |
| --- | --- | --- | --- |
| 1 | Program, child 27 (answer 9: M5) | The Retro critic asks each point for `home:`, `count:`, `why not code:` and drops a point that lacks them; `validate` checks those fields in a `retro.md`, read-only | sections 1, 2 |
| 2 | Child 16 (CR-502), "Depends on this child" and section 3 | `validate` reads the point format child 16 fixed: `- [<tag>] <problem> (events …): <fix>` then `  - home: `, `  - count:`, `  - why not code:`; the `home:` rungs are `CLI`, `refusal`, `next: or state line`, `help topic`, `card line` | section 1 |
| 3 | Child 16, answer 2 (sc16-Q1, Chief of Staff under the owner's autonomy) | `close` stays unchanged; child 27's `validate` flags an unfilled draft | section 1 |
| 4 | Program, child 27 (M6, F13); child 5 "Depends on it" | The Inspector checks that a card diff quotes "a key and count from the behaviour results" (child 5's key names), or carries the owner's line, which quotes the user's words as recorded in the CR's `02-answers.md` | section 3 |
| 5 | Program, child 27 (M10); child 5 decisions table and out of scope | `evals/results/behaviour-accepted.md`, re-asked when a rate doubles; filing or accepting the S-list is this child's | section 4 |
| 6 | Program answer 9 (M14), study-behaviour M14 | "Tool not in the role's list" lines are answered like S-list lines; an accepted one carries why the tool is withheld | section 4 |
| 7 | Program, child 27 (M11, F13) | A reminder step of `ci.yml`, `pull_request` only, on `ubuntu-latest`; it warns and never fails; proved on a throwaway PR the Driver opens and closes unmerged, recording its link | sections 5, 8 |
| 8 | Program, child 27 (M7); child 5 section 2 and out of scope | "Before a release: the claims" and `docs/release-process.md` list `just behaviour` for the version, newer than the last card change (child 5's `cards_commit`), regressions answered, or "no measure: <reason>" | section 6 |
| 9 | Program "What changes", AGENTS.md | AGENTS.md gains the release claims' behaviour measure | section 7 |
| 10 | Program merge rule; F6, F11 | A typed merge wait on child 28; the Known gap "real run not done (child 28)" | "Handback" |
| 11 | Program Q4; child 24 evidence 7 | Only the owner raises a card's target; a card's growth fits its frozen limit or waits for the owner's line | section 3, "Card budgets" |
| 12 | Program child 26 (M4, M13) | A new never/must/only/always sentence carries an `[R-nnn]` id with a `rules.json` row and a check; tests pin ids, not prose | section 3, "Rule ids" |
| 13 | Program "Rules for every child" (F20) | The added `just test` seconds are stated | "Gates and evidence" |

No other specified child (1 to 26, as read in `4-batch/1-pending/` and `1-inbox/`) addresses a
note to child 27.

## Decisions carried

| Source | Decision | Here |
| --- | --- | --- |
| Answer 9 (M5) | The retro-fix ladder: CLI, refusal, `next:` or state line, help topic, card line; a point carries `home:`, `count:`, `why not code:`; the Retro critic drops a point without them; `validate` checks them, read-only | sections 1, 2 |
| Answer 9 (M6), study-behaviour M6 | A card line is added only for a stumble seen in at least 5 runs or 2 % of the role's runs in the last measure, or for a rule of kind floor; the PR body quotes the measure line; the Inspector judges | section 3 |
| Answer 22, F13 | The CI step stays a reminder; its proof uses a throwaway PR; the Inspector checks that the approval line quotes the user's words from `02-answers.md` | sections 3, 5, 8 |
| Answer 9 (M11), study-behaviour M11 | The floor file and `budgets.json` change only with "Floor change approved: <user>, <date>" or "Budget change approved: <user>, <date>" in the PR body; the user writes the line, a Driver cannot | sections 3, 5, 7 |
| Answers 3 and 9 (M10), study-behaviour M10 | A usage error or refusal above 2 % of a role's runs is a CLI bug; each S-list line is filed as an inbox item or answered "accepted stumbling" in `evals/results/behaviour-accepted.md`; re-asked when its rate doubles; the Chief of Staff files after the release retro | section 4 |
| Answer 9 (M14) | "Tool not in the role's list" is answered the same way, an accepted line carrying why the tool is withheld | section 4 |
| Answer 9 (M7) | The release claims list `just behaviour` for the version; the measure is newer than the last card change, its regressions answered, or the claims file says "no measure: <reason>" | section 6 |
| sc16 answer 2 (Q1) | `close` unchanged; `validate` flags an unfilled draft | section 1 |
| Answer 22, Q4 | Only the owner raises a card's target | section 3, "Card budgets" |
| Answer 22, F6, F11 | Handed back validated, with the gap "real run not done (child 28)" and a typed merge wait on child 28 | "Handback" |
| Answer 22, F17 | An unproved claim is marked "unproved" | sections 5, 8 |
| Answer 22, F20 | The added `just test` seconds are stated | "Gates and evidence" |
| Program, child 27, Must not | No Driver writes the owner's approval line; the CI step never fails a job | sections 3, 5; "Must not" |
| Program, child 27, Risk | The long gate is owed (cards); the CI job is proved by its first run; the throwaway PR is a forge write the Driver does and records | "Gates and evidence", section 8 |

Two readings of this specification, each the smallest that makes a program sentence work:

- **"Re-asked when its rate doubles"** needs something that sees the doubling: `behaviour.py`
  reads the accepted file and marks such a line `re-ask` (section 4). It changes nothing else of
  child 5's output.
- **"The Chief of Staff ... answers it there"**: the Chief of Staff writes no file in the code
  repository, so its answers reach `behaviour-accepted.md` through one evals-only inbox CR per
  measure (section 4), which owes no long gate (AGENTS.md).

## What changes

### 1. `chantier validate` checks the retro (M5), read-only

- **New module `src/lifecycle/retro_check.py`:**
  - `RUNGS = ("CLI", "refusal", "next: or state line", "help topic", "card line")`, the five
    rungs, in the ladder's order (child 16's list).
  - A pure function `retro_point_findings(text: str, rel: str) -> list[Finding]` (`Finding`
    from `src/lifecycle/layout_check.py`, severity `gap`, path `rel`). It reads the text line by
    line:
    - **A point** is a line that starts `- [` and holds `] ` (a tagged retro line, as
      `foreman`'s retro form and child 16's draft write it). Its fields are the lines below it
      that start with whitespace then `- `, up to the next line that does not start with
      whitespace. An untagged line (the "no problem" line, an author's plain line) is not a
      point and needs no field.
    - **A field** is `home:`, `count:` or `why not code:`, matched case-sensitively after the
      `- `. Its value is the text after the colon, stripped. A value that is empty, or that is
      wholly one `<...>` placeholder, is empty.
    - **Per point**, at most one finding, naming every fault of that point:
      `line <n>: point "<the point's text, first 60 characters, … when cut>": <faults> → fill
      home:, count: and why not code:, or drop the point`. The faults, in this order, joined by
      `; `: `no home:` / `no count:` / `no why not code:` (missing or empty), and `home: "<v>"
      is not one of CLI, refusal, next: or state line, help topic, card line` when the value does
      not start with one of `RUNGS` (case-insensitive; text after the rung, such as
      ``help topic `retro` ``, is allowed). A point whose tag is the placeholder `[<tag>]` also
      gets the fault `tag not chosen`.
    - **The draft marker.** For each line that starts `<!-- chantier retro draft:`, one finding:
      `line <n>: an unfilled retro draft → judge, tag and fill each point, or delete it, then
      delete the two draft marker lines`. This is sc16 answer 2: `close` is unchanged, `validate`
      flags it.
  - `retro_findings(repo: Repo) -> list[Finding]`: reads `4-batch/retro.md` through
    `read_retro(repo.store, stage_layout(repo)["batches"])` (`src/core/batch_records.py`); none
    when it returns `None`; else `retro_point_findings(text, <the file's path as other findings
    show it>)`.
- **`src/commands/validate.py`**, `findings()`: add `*retro_findings(repo)` to `found`. The
  counts line and the exit codes are unchanged: these are gaps, so a retro alone never makes
  `validate` exit 3.
- **`src/declare/validate.py`**: the summary gains, before "exit 0 with gaps": "the batch's
  `retro.md` (a point without `home:`, `count:` or `why not code:`, an unfilled draft: gaps)".
- **What is not checked:** a closed batch's record (`5-archives/batches/batch-NN.md`, written
  before the ladder existed), a release CR's own `work/retro.md` (another format, the release
  driver's) and `retro-dropped.md`. Nothing is written; no new exit code; no new command.

### 2. The Retro critic's card (M5)

In `references/retro-critic.md` (child 19's card, swapped in by child 24):

- **Input:** each point comes with its three fields as its author wrote them.
- **Judging:** before the three questions, a point with no `home:`, `count:` or `why not code:`,
  or with an empty one, is dropped: `<n>. drop: no home:/count:/why not code:`. A point whose
  `home:` is `card line` keeps only when its `count:` names the measure it read (the results file
  and the count) and meets M6's floor (at least 5 runs or 2 % of the role's runs), or the line is
  a rule of kind floor, and when its `why not code:` says why the four rungs above cannot hold the
  fix (study-behaviour M5).
- The card still writes nothing; its reply lines (`keep`, `merge with`, `drop`, the last line)
  are unchanged.

The Foreman's `retro` topic and the Chief of Staff's direct-mode retro already frame each point
with the three fields through `retro draft` (children 16, 21, 22); they are not changed here.

### 3. The Inspector checks a card diff (M6, F13)

- **`references/inspector.md`**: one line: a diff that adds text to a `*.md` under
  `references/`, or that touches `references/floor.md` or `references/budgets.json`, is judged
  by the card-diff check of the `inspector-audit` topic; a fault there is blocking.
- **`references/topics/inspector-audit.md`**, a new short section "Card diff":
  - **Which diffs.** Added or grown text in a `*.md` under `references/` (a card or a topic).
    A pure deletion, a move with no new text, and a change to a data file other than
    `budgets.json` are not judged here.
  - **The measure line.** The PR body quotes, for the added text, a line of a results file of
    `evals/results/` (child 5): the file name, the key (for example
    `roles.cr-driver.cli.refusals` and its template) and the count. The Inspector reads that file
    at the PR's head: the key holds that count, and the count meets M6's floor (at least 5 runs,
    or 2 % of that role's `runs`), or the added text is a rule of kind `floor` in
    `rules.json`. A missing, unreadable or wrong quote is blocking.
  - **Or the owner's line.** In place of the measure line, the body may carry the owner's
    approval. For `floor.md` or `budgets.json` it is required (M11): `Floor change approved:
    <user>, <date>` or `Budget change approved: <user>, <date>`. Every such line quotes, after
    it, the user's words as `02-answers.md` of the PR's CR records them, with the answer's id
    (in this specification only, an example: `Budget change approved: <user>, <date>: "<the
    user's words>" (<cr>-Q<n>)`; the topic holds no date, user name or CR id, M3). The Inspector reads the CR's `02-answers.md`: no answer of the user holding
    those words is blocking. An agent copies the user's recorded words; it never writes an
    approval the user did not give (F13; M11: "A Driver cannot").
- **Card budgets (Q4).** The three files this child grows (`retro-critic.md`, `inspector.md`,
  the topics `inspector-audit` and `release-chief`) have limits frozen by child 26 in
  `budgets.json`. The added text fits each file's limit, and the sum's constant: the Driver
  shortens other text of the same file to make room, without removing an `[R-nnn]` id or a
  floor or kind-a rule. If a file cannot fit, the Driver does not touch `budgets.json`: it hands
  back `blocked question:` naming the file, its size and the limit it needs, for the owner's
  "Budget change approved" line (which the Chief of Staff records in this CR's `02-answers.md`).
  No new `*.md` is added under `references/`, so `budgets.json` needs no new row.
- **Rule ids (M4, M13).** Each new or reworded sentence with "never", "must", "only" or "always"
  in those files carries an `[R-nnn]` id (a new number, never a retired one, M12) with its row in
  `references/rules.json`: card, kind (`role` here), check. The check of the Retro critic's drop
  rule and of the Inspector's card-diff rule is a new quiz case of child 6 for that role (a
  judgement no pytest sees); the row of `validate`'s check names the pytest node of section 9.
  No test pins a card phrase longer than 40 characters (M13).

### 4. The S-list answered (M10, M14)

- **New `evals/results/behaviour-accepted.md`**, UTF-8, LF:

  ```
  # Accepted stumbling

  Lines of `just behaviour`'s S-list (a usage error or refusal above 2 % of a role's runs) and
  of its "tool not in the role's list", answered "accepted stumbling" instead of an inbox item
  (study-behaviour M10, M14). The measure marks a line `re-ask` when its rate reaches twice the
  rate below; it is then answered again.

  | Role | Kind | Template | Rate | Measure | Why accepted |
  | --- | --- | --- | --- | --- | --- |
  ```

  - `Kind` is `usage_error`, `refusal` or `tool_not_in_list`; `Template` is the S-list's
    normalised template, byte for byte, or the tool's name; `Rate` the rate when accepted (a
    percentage, one decimal); `Measure` the results file name it was read in; `Why accepted`
    one line (for a tool: why the role does not get it, for example the Inspector has no `Write`
    on purpose).
  - It ships with the header and no row: child 28's campaign and later measures add rows.
- **`evals/kit/behaviour.py`** (child 5's tool), one addition:
  - it reads `<out>/behaviour-accepted.md` when present (a table it cannot parse: exit 2
    naming the file and the line);
  - the lines to answer are the `s_list` entries and every `roles.<role>.tool_not_in_list`
    entry (its rate: count divided by the role's `runs`, as a percentage);
  - each gets `answer`: `accepted` (a row with the same role, kind and template whose `Rate`
    is more than half the current rate), `re-ask` (such a row, current rate at least twice
    its `Rate`) or `open` (no row);
  - the JSON gains `to_answer: [{role, kind, template, runs, rate, answer, accepted_rate}]`
    (additive; `"schema"` stays 1); the Markdown gains a section "To answer" listing the `open`
    and `re-ask` lines, or "none";
  - `regressions` and every other figure are unchanged.
- **`evals/kit/dry_run.py`**, case `behaviour`: a staged `evals/kit/behaviour-fixture/accepted.md`
  (copied into `<tmp>` first) with one row below double and one at double; the check asserts
  `accepted` and `re-ask` on those two lines and `open` on another. `expected.json` gains the
  `to_answer` figures, worked out by hand in the PR.
- **The Chief of Staff's `release-chief` topic** (`references/topics/release-chief.md`), after
  the release retro: for the release's measure (section 6), each `open` or `re-ask` line of "To
  answer" is either filed as an inbox item (`$CHANTIER file "<title>"`, the line in its request:
  a tool bug, answer 3) or proposed to the user as accepted stumbling with a one-line why; the
  accepted lines go together into one inbox item, `behaviour-answers-v<X.Y.Z>`, whose PR adds
  their rows. Nothing is accepted without the user's word.
- `evals/README.md`'s kit table: the `kit/behaviour.py` row names the accepted file and "To
  answer".

### 5. The approval reminder in CI (M11, F13)

- **New `scripts/card_approval.py`**, standard library only (it runs with the runner's
  `python3`, no uv), UTF-8:
  - `WATCHED = {"skills/chantier/references/floor.md": "Floor", "skills/chantier/references/budgets.json": "Budget"}`;
  - `approval(body: str, word: str) -> bool`: a line of the body matching
    `^[ \t>*-]*<word> change approved: [^,\n]+, \d{4}-\d{2}-\d{2}` (multiline);
  - `reminders(changed: list[str], body: str | None) -> list[str]`: one GitHub annotation per
    watched file in `changed` whose word has no approval line:
    `::warning file=<path>,title=<word> change not approved::<path> changed; the PR body has no
    "<word> change approved: <user>, <date>" line. Only the user gives it (AGENTS.md); this step
    does not fail.`;
  - `main()`: reads the payload at `$GITHUB_EVENT_PATH` (`pull_request.body`, `null` read as
    empty), the changed files from `git diff --name-only HEAD^1 HEAD` (the PR's merge commit
    against its base), prints each reminder, then one plain line
    `card approval: <k> reminder(s)` or `card approval: floor and budgets untouched, or approved`.
    Any exception is caught and printed as `::warning title=card approval not checked::<text>`.
    It always exits 0.
- **`.github/workflows/ci.yml`**, a new job beside `check`, `scenario` and `eval-dry-run`:

  ```yaml
  card-approval:
    name: card approval reminder (ubuntu-latest)
    if: github.event_name == 'pull_request'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 2
      # A reminder only (M11): it warns when the floor or the budgets change with no approval line, never fails
      - name: Floor and budget approval lines
        continue-on-error: true
        run: python3 scripts/card_approval.py
  ```

  - The body is read from the event payload by the script, never interpolated into the shell
    (no `${{ github.event.pull_request.body }}` in `run:`).
  - The workflow's `on:` and `permissions:` are unchanged. The job is not a required check.
- **Its environment.** GitHub's hosted `ubuntu-latest` runner: `python3` and `git` of the image;
  no uv, no cache, no `gh`, no credentials beyond the read-only `GITHUB_TOKEN` (unused); the
  checkout is the PR's merge ref (`refs/pull/<n>/merge`) at depth 2, so `HEAD^1` is the base
  branch's tip, also for a PR stacked on another CR's branch. Absent locally: the event payload,
  the merge ref and the annotation rendering. The pytest of section 9 proves the script on a
  prepared payload and file list; only the first CI run proves the `if:`, the depth-2 diff and
  the annotation's display (unproved until then; section 8 proves them).
- **A known limit.** `pull_request` runs on opened, synchronize and reopened, not on an edit of
  the body: a line added to the body clears the warning at the next push (open question 1).

### 6. The measure's place in the release (M7)

- **`evals/README.md`**, "Before a release: the claims", a new bullet after "The release
  notes":
  - **The behaviour measure.** At the version PR's head (the version already `X.Y.Z`),
    `just behaviour --since <the previous tag's date>` writes `evals/results/behaviour-…-vX.Y.Z`
    `.json` and `.md`, committed with the claims. It counts when its `cards_commit` equals
    `git log -1 --format=%h -- skills/chantier/references` at that head (newer than the last
    card change) and each line of its `regressions` is answered under the claims table (an inbox
    item's folder name, or a row of `behaviour-accepted.md`). The claims file then holds, under
    its table, one line: `Behaviour: <the .md file name>, cards at <cards_commit>, regressions:
    none` (or `answered`), or `Behaviour: no measure: <reason>`. Its "To answer" lines go to the
    Chief of Staff after the release retro (M10).
- **`docs/release-process.md`**: in the paragraph that names the claims file (section "Release
  notes"), one sentence: the version PR also carries the release's behaviour measure, or the
  claims file's `Behaviour: no measure: <reason>` line, as `evals/README.md` "Before a release:
  the claims" says.
- No script checks the `Behaviour:` line (out of scope).

### 7. AGENTS.md

Two changes. The text at `origin/main` is quoted; children 1, 9 and 16 edit other bullets of the
file below this child, not these two.

- **A new bullet**, right after the bullet "A change to what the CR board pane draws ... See
  [CONTRIBUTING.md](CONTRIBUTING.md)." and before "No fallback: ...":

  > - A PR that adds text to a card or a help topic (`skills/chantier/references/**/*.md`)
  >   quotes in its body the measure line it rests on (an `evals/results/behaviour-*.json` file,
  >   its key and count: a stumble seen in at least 5 runs or 2 % of the role's runs, or a rule
  >   of kind floor) or the user's approval line; a PR that changes `references/floor.md` or
  >   `references/budgets.json` carries "Floor change approved: <user>, <date>" or "Budget change
  >   approved: <user>, <date>", quoting the user's words as the CR's `02-answers.md` records
  >   them. Only the user gives that line: no agent writes one the user did not give. The
  >   Inspector judges both; the `card approval reminder` job of `ci.yml` warns on a pull request
  >   that lacks the line and never fails. A retro point carries `home:` (CLI, refusal, `next:`
  >   or state line, help topic, card line), `count:` and `why not code:`; `chantier validate`
  >   reports one without them.

- **The `release:` line** of `## chantier`. Old:

  > - release: [CONTRIBUTING.md](CONTRIBUTING.md), "Release", and [docs/release-process.md](docs/release-process.md); the claims before a release: [evals/README.md](evals/README.md), "Before a release: the claims"

  New:

  > - release: [CONTRIBUTING.md](CONTRIBUTING.md), "Release", and [docs/release-process.md](docs/release-process.md); the claims before a release, the version's `just behaviour` measure included (newer than the last card change, or `no measure: <reason>`): [evals/README.md](evals/README.md), "Before a release: the claims"

- No named-exception line: `validate` is already named in the CLI's scope ("a read-only check
  of a planning folder"), and this child adds no command, no git write and no network use.

### 8. The throwaway PR (the CI step's proof)

After this CR's own PR is pushed, and before the hand-back:

1. From this CR's worktree head, a branch `probe/sc27-card-approval` with one commit that
   changes `skills/chantier/references/budgets.json` (one limit lowered by 1 byte, so the file
   stays valid).
2. `git push -u origin probe/sc27-card-approval` (a new branch, no force; `chantier push`
   serves only the CR's recorded branch). Then `gh pr create --draft --base <this CR's branch>
   --head probe/sc27-card-approval --title "probe: card approval reminder (do not merge)"`,
   with a body holding no approval line.
3. When `card approval reminder (ubuntu-latest)` has run: `gh pr checks <n>` and the run's
   annotations (`gh run view <run id>`) show the `Budget change not approved` warning, and the
   job's conclusion is success.
4. `gh pr close <n> --delete-branch`, unmerged.
5. The PR's Deliverables record the probe PR's link, the run's link, the warning's text as shown
   and the job's conclusion. A failure of steps 1 to 3 is handed back with its text; there is no
   other route.

This is the program's named forge write for this child (Risk); the Driver opens nothing else.
This CR's own PR is the negative case: unless section 3's budget fallback touched
`budgets.json`, its run shows no warning (recorded too).

### 9. Tests

All new tests are in-process, parametrized and on small inputs.

- **`tests/test_validate.py`**, one parametrized test of the retro check, on prepared
  `4-batch/retro.md` texts in a planning folder built as the file's other tests build theirs
  (`build`, the `chantier` fixture), both cells (`repo`, `surface`):
  - a point with the three fields filled and `home: help topic `retro``: no retro line, exit 0;
  - each of the three fields missing, and each empty or `<...>`: one gap naming the fault;
  - `home: elsewhere`: the "is not one of" fault;
  - `[<tag>]`: `tag not chosen`;
  - a draft block exactly as child 16's `retro draft` writes it (the bytes taken from
    `retro_draft`'s text function, not retyped): the draft-marker gap and one gap per point;
  - an untagged "no problem" line: nothing;
  - no `retro.md`: nothing.

  Each case asserts exit 0 (gaps only), the counts line and that the folder's bytes are
  unchanged (`snapshot`).
- **New `tests/test_card_approval.py`**: imports `scripts/card_approval.py` by path
  (`importlib.util`), parametrized over (changed files, body): neither file changed; `budgets.json`
  without a line (one warning, naming the path); with `Budget change approved: owner,
  2026-01-02` (none); with the line quoted (`> `) or bulleted (`- `) (none); `floor.md` with only
  a Budget line (one Floor warning); both files, no body (`null`: two warnings); a malformed date
  (a warning). One case runs `main()` with a prepared `GITHUB_EVENT_PATH` and a patched diff
  that raises: one `card approval not checked` warning and exit 0. These prepared payloads stand
  for the runner's event, which no local run has.
- **The shipped workflow**, in the same file: `.github/workflows/ci.yml` read from the
  repository at the head (with `ruamel.yaml`, the CLI's YAML reader): the `card-approval` job
  exists with `if: github.event_name == 'pull_request'`, `runs-on: ubuntu-latest`, checkout
  `fetch-depth: 2`, a step with `continue-on-error: true` running `python3
  scripts/card_approval.py`, and no `${{ github.event.pull_request.body }}` in any `run:`.
- **The shipped cards and docs**, by id and file (M13): the Retro critic's and the Inspector's
  new `[R-nnn]` ids are in their files and in `rules.json` (child 26's registry test covers
  this once the rows exist); `evals/results/behaviour-accepted.md` exists with the table header
  above (a test reads the shipped file).
- `tests/test_command_names.py` reads `evals/README.md` and AGENTS.md: the new text names only
  existing subcommands (`validate`, `file`).

## Out of scope

- A failing CI gate on the approval line, or any check of its quote in CI (F13: a reminder; the
  Inspector judges the quote).
- Rerunning the reminder on a body edit (open question 1).
- A check of the `Behaviour:` line in `scripts/release_notes.py` or elsewhere.
- Running `just behaviour`, `just quiz` or a campaign in this child (child 28 runs them); a quiz
  run is not owed for the new quiz cases.
- A gate requiring `just quiz` on later card changes (open question 2).
- `close` refusing an unfilled draft (sc16 answer 2: `close` unchanged).
- Checking archived batch records, a release CR's `work/retro.md` or `retro-dropped.md`.
- Moving "tool not in the role's list" into child 5's `s_list` key, or changing `regressions`.
- Any Driver card or topic: the Inspector's finding and the CI warning name the line to a Driver.
- Raising any card's limit, or touching `budgets.json`, without the owner's line.
- New commands, journal types, hook changes, version edits.

## Must not

- Let a Driver (or any agent) write an owner's approval line the user did not give, in a PR body,
  a card, `02-answers.md` or the probe PR.
- Make the CI step fail a job (the script exits 0; the step is `continue-on-error`).
- Interpolate the PR body into a shell command.
- Write anything from `validate`.
- Merge the probe PR, push to a branch other than this CR's and the probe branch, or force any
  push.

## Gates and evidence

- `just check` and `just eval-dry-run` (changes under `src/` and `evals/kit/`) in the worktree at
  the rebased head before the first push.
- The long gate `just scenario (ubuntu-latest)` is green at the PR's head (cards change). The
  local Windows `chantier gate <cr> scenario` is owed only while this CR is the stack's top; it
  moves to child 28 when that CR joins.
- The CI job: section 8's probe, recorded; this PR's own run without warning (unless the budget
  fallback applied).
- The tests of section 9 pass; each check that guards a shipped file (`ci.yml`, the cards,
  `rules.json`, `behaviour-accepted.md`) reads it from the repository at the head under test; the
  prepared texts (retro texts, payloads) stand only for inputs no shipped file holds, each paired
  with a shipped check.
- **The added `just test` seconds**, measured before (at the base) and after (at the head) on
  the same machine, under the PR's Deliverables. Expected: under 1 s (about 14 validate cases on
  small folders and about 10 pure-function cases).
- The card sizes after the change, against their `budgets.json` limits, in the Deliverables.
- No host or default matrix: the validate check, the script and the docs act the same on both
  hosts and with any configuration; the two cards are host-neutral text.
- No `hooks/` or `types/` change: `just mod` is not owed.

## Handback

- Validated, with the Known gap "real run not done (child 28)" until child 28's results are in.
- A typed merge wait: `$CHANTIER wait <cr> merge <child 28's PR>`, so the `handed back:` line
  prints `do not merge: waits for …`.
- If section 3's budget fallback applied: the Known gap names each file over its limit, and the
  owner's "Budget change approved" line is awaited.

## Risk

- The long gate is owed (cards).
- A CI job change, proved only by its first run (section 8).
- The probe PR is a forge write (a pushed branch, a draft PR, its close and branch deletion); the
  Driver does it once and records the link.
- The cards' frozen limits may leave no room (section 3, "Card budgets"): then the CR waits for
  the owner.
- The quote check is the Inspector's judgement; an Inspector that misses a missing quote lets an
  unapproved card line through to the owner's merge, where the CI warning (for the floor and the
  budgets) is the second look.

## Open questions

1. **The reminder after a body edit.** `ci.yml`'s `pull_request` trigger does not run on a body
   edit, so after the user adds an approval line the warning stays until the next push (a re-run
   reuses the old body). Should the step move to its own workflow file triggered also on
   `edited` (the program says "a step of `ci.yml`"), or is the stale warning acceptable? Until
   you answer: `ci.yml`, no `edited` trigger.
2. **A quiz gate for later card changes.** The program's gates are child 26's pytest and this
   child's process rules; neither asks a later PR that changes a role's card to run `just quiz`
   for that role (it costs model spend). Should AGENTS.md's new bullet also require it? Until
   you answer: no.
