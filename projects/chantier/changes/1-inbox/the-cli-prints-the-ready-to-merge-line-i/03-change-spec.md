# `status` prints the ready line and the batch state; reload rules

Short name: `ready-line`. Destination: batch-31. Repository: `C:/Users/gaeta/Projets/chantier`.
This change touches the CLI (`skills/chantier/scripts/cli/src/chantier/`), its tests, the
startup manifest, the cards (`skills/chantier/references/`) and one scenario step.

## Goal

The user, 2026-11-23: "be sure important rules are reloaded at compaction and the CLI prints the
batch states (mode, slots...) so the agent does not forget."

In batch-31 the Chief of Staff wrote its ready-to-merge lines by hand. They had no colour icon
(🟢), named links instead of the PR's URL, and gaps not quoted next to each link. After a
compaction it lost the batch's state. `status-layout.md` is read by the `status` action and
before each report, not at a reload. The fix:

1. `status` prints the ready line of each CR, and the agent copies it (ready-line-Q1).
2. `status` prints one complete `batch:` line with the batch's state (ready-line-Q2).
3. After a compaction, the Chief of Staff and the Foreman read a short piece of rules
   (ready-line-Q3).

## Decisions carried (02-answers.md)

- **ready-line-Q1 (A):** the ready line is printed by `status`, one line per CR, for a CR ready
  to merge or a PR in draft (with "do not merge" and what it waits for). The line has the label's
  icon, the full PR link, each gap, "do not merge before X" when a step is owed, and the local gate
  line.
- **ready-line-Q2 (A):** one complete `batch` line with the shape, slots, steering, rounds limit,
  budget, who owes the local gate, and who merges.
- **ready-line-Q3 (A):** the reload of the Chief of Staff and the Foreman reads a short piece of
  rules: the report layout, the ready words, the shape rule, and who merges.
- **ready-line-Q4 (A):** specified for the running batch, batch-31.
- **ready-line-Q5 (A):** the "do not merge before X (who)" clause is printed for every open step
  the record shows (a local gate not passed at the CR's head, an open order on the CR), naming who
  owes it: its Driver, the Foreman or the Chief of Staff (section 1).
- **ready-line-Q6 (A):** the `batch:` line lists the ready CRs whose local gate is still open; it
  does not print the per-shape rule, which stays in the cards (section 2).
- **ready-line-Q7 (A):** if the Chief of Staff's reload does not fit the 12,544-byte limit after
  CR-471, `status`'s `batch:` line prints `rules: <path>/reload-rules.md (reread after a
  compaction)`, as the stack shape line does for `foreman-stack.md`, with no counted bytes; the
  Driver does not hand back blocked for that ("The byte limit", below).

## What changes

### 1. The ready line in `status` (CLI)

**Where:** a new module, `skills/chantier/scripts/cli/src/chantier/status/ready_line.py`, called
from `status()` in `skills/chantier/scripts/cli/src/chantier/commands/batch_status.py`. Its lines
come right after the CR rows (`_cr_row`), before `stack_line(d)`. They are printed on every
`status` call, with or without `--refresh`, in Foreman and direct mode, for every shape.

**Which CRs:** each CR whose record `status` is `ready` (handed back ready), in the CR rows' order
(`c.order`). There is no line for a CR that is queued, working, blocked, merged or dropped. Its row
and its `label` already say its state.

**The line's shape** (English, plain text, one line; `<…>` are filled from the record):

```
ready: <icon> <word> <CR-n> <slug> <PR link>[ do not merge: waits for <what>][ gaps: <gap>; <gap>][ do not merge before <X> (<who>)][ | local gate <CR-n> at <sha7>: <result>]
```

- `<icon> <word>`: the icon and the state word of the CR's `label`, taken from the same functions
  (`status/words.py`'s `READY_ICON` and `stack_words.ready_word`, as `state_label` uses them).
  They are never computed another way: 🟢 `ready to merge`, 🟤 `PR in draft`, 🟣 `ready locally`.
- `<CR-n> <slug>`: the CR's id and its folder's slug (the folder name after its `<n>-` prefix),
  so the agent names the CR by number and slug (`status-layout.md`, "A CR's name").
- `<PR link>`: the full URL the record holds (`c.shown_pr()`), never shortened or named. A CR
  ready locally prints `no PR yet` in its place.
- `do not merge: waits for <what>`: only for 🟤, with `<what>` from `stack_words.draft_waits`
  (the same words as the `label`'s `waits for`).
- `gaps: …`: the gaps of the CR's last `handback ready` event (`events.jsonl`). This is the text
  after `gaps: ` in its `note`, as `driver.md` makes a Driver write it (`… gaps: <gap>; <gap>`,
  also after `; ` in a draft's text). It is copied unchanged. With no gaps, the segment is absent
  and the line says nothing about gaps.
- `do not merge before <X> (<who>)`: one clause for each open step of the record listed below,
  whoever owes it (ready-line-Q5). With none, the clause is absent.
  - The CR's long gate at its recorded head is not `passed`, `carried`, `exempt` or `waived`
    (`status/gate.py`'s `gate_view` state is `none`, `queued`, `running` or `failed`). Then `<X>` is
    `its local gate passes at <sha7>`. `<who>` is `its Driver` while the CR's Driver is live (an
    agent is recorded, not in `stopped_agents` and not ended with no hand-back, as
    `_working_tail` reads it). Otherwise `<who>` is `the Foreman` in Foreman mode and `the Chief
    of Staff` in direct mode.
  - An order on this CR is open (`OrderRecord.done` is empty, `o.cr == c.id`). Then `<X>` is
    `O-<k> <kind> is done`, and `<who>` is `the Foreman` in Foreman mode and `the Chief of Staff`
    in direct mode.
- `local gate <CR-n> at <sha7>: <result>`: the CR's long gate at its head, from `gate_view`, in
  the clause words of `foreman.md`'s ask lines. The mapping:
  - `passed` gives `passed`;
  - `carried` gives `passed (carried from <sha7>)`;
  - `failed` gives `failed`;
  - `none`, `queued` and `running` give `not run` (with ` (queued)` or ` (running)` appended);
  - `exempt` gives `exempt: <rule>`;
  - `waived` gives the gate text (`waived → CR-k (#n)` or `waived → follow-up <folder>`).

  `<sha7>` is the CR's recorded head, first seven characters. With no head, the clause is absent.

Examples, with the fields of batch-31:

```
ready: 🟢 ready to merge CR-470 slim-session-start-md-split-by-role-forg https://github.com/gsemet/chantier/pull/447 gaps: no screenshot of the pane from a real session | local gate CR-470 at 1a2b3c4: exempt: AGENTS.md: …
ready: 🟤 PR in draft CR-466 own-cr-branch-rebase-and-force-push-pre- https://github.com/gsemet/chantier/pull/443 do not merge: waits for its turn out of draft do not merge before its local gate passes at 5d6e7f8 (the Foreman) | local gate CR-466 at 5d6e7f8: not run
```

The CLI prints English words. The Chief of Staff says the line in the user's language, but keeps
the icon, the link, the ids and each gap's text unchanged (section 3).

### 2. The `batch:` line in `status` (CLI)

The line goes in the same new module and is printed as the second line of `status`, right after
the existing first line (`_batch_line`). The first line does not change: the scenario parses it
(`split(" live ")`) and `status-layout.md`'s header copies from it.

```
batch: shape <shape>; slots <live>/<slots>; steering <who>; rounds <n>[ (CR-k <m>, …)]; budget <spent> of $<budget>|budget none (spent <spent>); local gate owed: <CR-n> (<who>), …|none; merges: the user
```

- `shape`: `shape_word(d.mode)`.
- `slots`: `len(held(d))` and `d.slots`, the same figures as the first line's `live`.
- `steering`: `steering_word(d.steering)`.
- `rounds`: the batch's limit, `(d.settings or BatchSettings()).max_rounds`. In parentheses go
  the CRs granted another limit (`c.rounds`, from `order rounds`), each with its own.
- `budget`: `spent_text(d)` and `d.budget_usd`, or `budget none (spent <spent>)` with no budget.
- `local gate owed`: each CR in `ready` whose long gate at its head is open (the first clause of
  section 1's list), with its `<who>` from the same rule. With none, `none`. It is the same fact
  as the ready lines', so the two never disagree.
- `; rules: <skill folder>/references/reload-rules.md (reread after a compaction)`: only when the
  reload addition does not fit the byte limit (ready-line-Q7, "The byte limit" below).
- `merges: the user`: fixed. The Chief of Staff and the Foreman never merge
  (`chief-of-staff.md`, "Never merge for the user").

It shows only what the CLI holds. The CLI does not read the project's rules. Whether a project's
rules ask a CR for a local run by shape (CR `own-gate`) stays a card's judgement over the gate's
words. That is why the line names the ready CRs whose gate at their head is open, and not a rule
(ready-line-Q6).

### 3. The cards

- **`skills/chantier/references/reload-rules.md` (new):** a short piece, at most about 2,500
  bytes, with a `#` title and four bullets. Each bullet restates its rule in one or two sentences
  and names the section that holds it in full. The full rules stay where they are. No rule moves.
  - **Reports:** before a report, read `status-layout.md` whole and run `status --refresh`. Copy
    the header from `status`'s first line and its `batch:` line. Copy each icon from `label`.
  - **The ready words:** say "ready to merge" only for 🟢, "PR in draft" with "do not merge" and
    what it waits for, and "ready locally" for a CR with no PR. "Ready" alone is never used. The
    icon is the present state. Copy the `ready:` line of `status` for each CR you name to the user:
    its icon, its full link, each gap, its `do not merge` clauses and its local gate clause
    (`chief-of-staff.md`, "The words to the user").
  - **The shape:** read it on the `batch:` line. In a stack, read `foreman-stack.md` (the
    `batch:stack` reading) and the shape line's `alone asks`. Who owes a local gate follows the
    project's rules and `driver.md`'s long-gate rule, read against the gate words `status` prints.
  - **Who merges:** the user only. Never merge for the user. A merge the user makes is recorded
    with `order merged` (`chief-of-staff.md`, "The words to the user").
- **`skills/chantier/references/startup-manifest.json`:** one action, `"reload:rules":
  ["reload-rules.md"]`, outside `reload`. The `reload` list does not change, so the piece is not
  counted in the reload budget. Only the manifest line is counted.
- **`skills/chantier/references/session-start.md`, "5. Reload":** one short sentence. After the
  reload, the Chief of Staff and the Foreman read the manifest's `reload:rules` before their next
  act. Keep it as short as it can be: this section is counted in the reload budget.
- **`skills/chantier/references/foreman.md`, opening:** in "again after a compaction: reread only
  those startup sections", add "and the manifest's `reload:rules` reading". This opening is not
  in the Foreman's counted boot.
- **`skills/chantier/references/chief-of-staff.md`, "While it runs", "The words to the user":**
  one sentence. `status` prints a `ready:` line for each CR handed back. The line said to the
  user is that line in the user's language, with its icon, its full PR link (never a named link),
  each gap next to the link, its `do not merge` clauses and its local gate clause. Nothing in it is
  judged. In the plain-ask bullet ("quote each gap of the ask next to the PR's link"), add that the
  `ready:` line carries the same gaps from the hand-back. When the ask and the line disagree, say
  both and ask the Foreman (`asks`). The rule "say 'you can merge' only after the `ready-to-merge`
  line reached you" stays: the `ready:` line is the words, the ask is the moment.
- **`skills/chantier/references/status-layout.md`, "The rules of every report":** one bullet.
  The batch's state in the header is copied from `status`'s first line and `batch:` line. A CR
  named in **Notes** or **For you** as ready to merge or in draft is written from its `ready:`
  line. The skeleton and the columns do not change.
- **`CONTRIBUTING.md`:** add `reload-rules.md` to the list of `references/` files (near line 64),
  as "the rules re-read after a compaction".

`agents/` and `com.github.copilot/agents/` do not change: the agent files only name their card.

### 4. Size and layout

- `commands/batch_status.py` has 400 lines today, the most a file may hold (`CONTRIBUTING.md`,
  "File: at most 400 lines"). The new code goes in `status/ready_line.py`. `batch_status.py` only
  gains the import and the two calls. To stay at or under 400, it moves an existing helper out
  with no change in behaviour (for instance `_order_lines` and `_late_suffix`, or
  `_stack_driver_lines`, into `status/ready_line.py` or a module of their own).
- Every new or changed `.py` file, tests included, stays at or under 400 lines.
  `test_startup_manifest.py` and `test_plugin_files.py` are at 400. Nothing is added to them.
  New checks go in new files.

### Order and rebase on batch-31's siblings

**This CR comes last** of the batch's CRs that touch these files: after `dynamic-port`
(`long-gate-webui-check-starts-a-second-bo`), after `own-gate` and after CR-471 (`slim-cards`).
It starts once those three are merged (or dropped), rebased onto that head, and its PR's base is
the default branch at that head.

CR-466 (`own-branch-push`, 2-actives), CR-471 (`slim-cards`, 2-actives, blocked on the
12,544-byte limit) and CR `own-gate` (`local-long-gate-rule-outside-a-stack-and`, inbox, for
batch-31) touch the same files. CR-471 splits `chief-of-staff.md`, `foreman.md` and `driver.md`
into pieces read by new `startup-manifest.json` actions and keeps the manifest under its byte
limit. CR `own-gate` rewrites the local-gate wording of the same cards, including "The words to
the user" and the plain-ask bullet. CR-466 adds refused-rebase sections to the same three cards.

`dynamic-port` changes the long gate's webui check (a second board on a free port); this CR does
not touch that code, but the scenario step it adds sits in the same `scenario/run_scenario.py`,
so it rebases on it too. This CR rebases on each of them as it lands. After the rebase, the Driver finds each place by
its words ("The words to the user", "quote each gap", "again after a compaction", "5. Reload",
"The rules of every report"), wherever CR-471 put it. It adds its sentences in the piece where the
rule now lives, and keeps CR-471's file split, its manifest form and its moments list. If CR-471
adds one, the `reload:rules` action is also named in each entry card's list of moments, as
CR-471's test asks. `reload-rules.md`'s shape bullet takes `own-gate`'s per-shape wording if it
has landed.

**The byte limit.** The Chief of Staff's reload is at 12,515 of the 12,544 bytes on `main`
(CR-471's measure). This CR adds to the counted reload only the manifest's `reload:rules` line and
the one sentence in "5. Reload". It is measured at the rebased base and at the head
(`startup-bytes` lines of `test_startup_manifest.py`). The limit is not raised. If the addition
does not fit after CR-471, the Driver shortens its own sentence first. If it still does not fit
(ready-line-Q7), the Driver does not hand back blocked:

- it drops the counted additions, first the sentence in "5. Reload", then, if still needed, the
  manifest's `reload:rules` line;
- `status`'s `batch:` line ends with `; rules: <skill folder>/references/reload-rules.md (reread
  after a compaction)`, the path built as `stack_shape.shape_line` builds its `foreman-stack.md`
  one (`skill_dir().as_posix()`). `status` is already read at every reload ("5. Reload": `seat`,
  `status`), so the pointer reaches the Chief of Staff and the Foreman with no counted byte;
- `foreman.md`'s opening and `reload-rules.md` stay (neither is counted); the opening names the
  `batch:` line's `rules:` pointer instead of the action when the action was dropped;
- the tests follow the form shipped: the shipped-files test checks the action and the sentence, or
  the pointer on the `batch:` line (an in-process `status` check) and `foreman.md`'s mention of it;
- the PR says which form shipped and quotes the `startup-bytes` figures that decided it.

## Out of scope

- No change to `status`'s first line, the CR rows, `STATUS.md`, `STATUS.json`, the board, the
  pane, `live` or the watcher's lines. The ready line and the `batch:` line are `status` only.
- No change to `asks`, `handback`, `ship`, `gate` or the Foreman's ask format (`foreman.md`'s
  `asks` line list).
- The CLI does not read the project's rules (AGENTS.md). It does not decide who owes a local run
  by shape. That is CR `own-gate`'s card rule.
- No change to `status-layout.md`'s skeleton or columns, including the CR table's `[PR](url)`
  column.
- No change to `agents/`, `com.github.copilot/agents/`, `hooks/` or `types/`, so no `just mod`.

## Evidence

- **Tests, in-process on a prepared state** (new file
  `skills/chantier/scripts/cli/tests/test_ready_line.py`, parametrized, fast, under 400 lines):
  - A batch with one CR per case. Each prints its `ready:` line with the exact icon and word, and
    the line is checked against the CR's `label` (`state_label`), so the two never disagree. The
    cases:
    - 🟢 ready to merge (`pr_draft=False`, on the default branch);
    - 🟤 PR in draft (with `do not merge: waits for …`);
    - 🟣 ready locally (`no PR yet`).
  - A `handback ready` event whose note ends with `gaps: a; b` gives ` gaps: a; b` on the line. A
    note with no gaps gives no `gaps` segment.
  - The local gate clause for each `gate_view` state: passed, carried, failed, none, exempt and
    waived.
  - `do not merge before`:
    - a head with no gate pass and no live Driver gives `(the Foreman)` in Foreman mode and
      `(the Chief of Staff)` in direct mode;
    - a live Driver gives `(its Driver)`;
    - an open order on the CR gives `O-<k> <kind> is done`;
    - none of these gives no clause.
  - The `batch:` line is the second line of `status`, in Foreman and direct mode and for each
    shape. It has the rounds limit with a CR's own grant, the budget and `budget none`,
    `local gate owed: none` and with a CR, and `merges: the user`. The first line is unchanged.
  - No `ready:` line for a queued, working, blocked, merged or dropped CR.
- **Tests on the shipped files** (a new file, for instance
  `skills/chantier/scripts/cli/tests/test_reload_rules.py`). They read the cards and the manifest
  from the repository as shipped, at the head under test, not from a copy:
  - `startup-manifest.json` has the action `reload:rules` naming `reload-rules.md`, and `reload`
    does not list it.
  - `reload-rules.md` exists and holds the four rules' key words (`status-layout.md`, `ready:`,
    `do not merge`, `batch:`, `foreman-stack.md`, `order merged`).
  - `session-start.md`'s "5. Reload" and `foreman.md`'s opening name `reload:rules`.
  - `chief-of-staff.md`'s "The words to the user" (or the piece where CR-471 moved it) names the
    `ready:` line.

  The existing `test_startup_manifest_measures_every_real_role_and_host` keeps every role's
  reload at or under 12,544. The PR quotes the Chief of Staff's and the Foreman's `startup-bytes`
  lines before and after.
- **Scenario** (`scenario/run_scenario.py`, after CR-101's `handback ready`, near "a hand-back
  writes the state and prints the line to send"): one check that `status` prints a line starting
  `ready: ` with `CR-101` and `pr101`'s full URL, and a second line starting `batch: shape ` that
  ends with `merges: the user`.
- **Gates:** `just check` in the worktree at the pushed head, and `just eval-dry-run` (a change
  under the CLI's `src/`). The long gate is the pipeline's `just scenario (ubuntu-latest)` job,
  green at the PR's head. The local run follows the project's rule for batch-31's shape (AGENTS.md,
  as CR `own-gate` leaves it).
- **The PR's Deliverables** quote one real `status` output from the worktree on a prepared batch,
  showing a 🟢 and a 🟤 `ready:` line and the `batch:` line.

## Open questions

None: the user's answers ready-line-Q5, Q6 and Q7 settled the three questions of the first draft.
