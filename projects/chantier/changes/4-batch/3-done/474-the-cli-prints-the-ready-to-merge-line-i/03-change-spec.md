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

1. `status` prints one line for each CR handed back, and the agent copies it (ready-line-Q1).
2. `status` prints one complete `batch:` line with the batch's state (ready-line-Q2).
3. After a compaction, the Chief of Staff and the Foreman read a short piece of rules
   (ready-line-Q3).

## Decisions carried (02-answers.md)

- **ready-line-Q1 (A):** `status` prints one line per CR, for a CR ready to merge or a PR in
  draft (with "do not merge" and what it waits for). The line has the label's icon, the full PR
  link, each gap, the steps still owed, and the gate clause. Q8, Q10 and Q11 refine it.
- **ready-line-Q2 (A):** one complete `batch` line: shape, slots, steering, rounds limit, budget,
  who owes the gate, who merges. Q6 and Q9 refine it.
- **ready-line-Q3 (A):** the reload of the Chief of Staff and the Foreman reads a short piece of
  rules: the report layout, the ready words, the shape rule, who merges.
- **ready-line-Q4 (A):** specified for the running batch, batch-31.
- **ready-line-Q5 (A):** one owed-step clause for every open step the record shows (the long
  gate not passed at the CR's head, an order on the CR not yet applied), each naming who owes
  it: its Driver, the Foreman or the Chief of Staff.
- **ready-line-Q6 (A):** the `batch:` line lists the ready CRs whose gate at their head is still
  open. It does not print the per-shape rule, which stays in the cards.
- **ready-line-Q7 (A):** if the counted reload does not fit the 12,544-byte limit after CR-471,
  `status`'s `batch:` line prints `rules: <path>/reload-rules.md (reread after a compaction)`, as
  the stack shape line does for `foreman-stack.md`. That costs no counted bytes. The Driver does
  not hand back blocked for that ("The byte limit", below).
- **ready-line-Q8 (A):** the line shows what the CLI records. Its clause is named `long gate`
  (the `chantier gate` run the record holds), not "local gate". The Chief of Staff adds the local
  run the project's rules owe from the Foreman's ask (`local gate <cr> at <sha7>: …`). When the
  two differ, the ask wins. The cards say so.
- **ready-line-Q9 (A):** `merges: the user`, plus `; under the grant: the release/fix PR (steering
  session)` when the record holds a release grant. `reload-rules.md` says the same.
- **ready-line-Q10 (A):** the line's prefix is `handed back:`. It is never said to the user, and
  the cards say so.
- **ready-line-Q11 (A):** a step still owed reads `owed before the merge: <X> (<who>)`. The user
  may still merge, and that merge is recorded as any merge (`order merged`). This replaces the
  first draft's "do not merge before". A PR in draft keeps its own `do not merge: waits for …`.
- **ready-line-Q12 (A):** only orders not yet applied hold a ready CR's merge. An order the CLI
  applied, which waits for `order done`, adds no clause.
- **ready-line-Q13 (A):** where a Driver's end cannot be read (on Copilot), the clause names the
  steering role (the Foreman, or the Chief of Staff in direct mode). The Copilot case is marked
  unproved.

## What changes

### 1. The `handed back:` line in `status` (CLI)

**Where:** a new module, `skills/chantier/scripts/cli/src/chantier/status/ready_line.py`, called
from `status()` in `skills/chantier/scripts/cli/src/chantier/commands/batch_status.py`. Its lines
come right after the CR rows (`_cr_row`) and before `stack_line(d)`. They are printed on every
`status` call, with or without `--refresh`, in Foreman and direct mode, for every shape.

**Which CRs:** each CR whose record `status` is `ready` (handed back ready), in the CR rows'
order (`c.order`). A CR that is queued, working, blocked, merged or dropped gets no line: its row
and its `label` already say its state.

**The line's shape.** English, plain text, one line; `<…>` are filled from the record. After
the link, each segment is separated by ` | `. Several owed clauses in one segment are separated
by `; `.

```
handed back: <icon> <word> <CR-n> <slug> <PR link>[ | do not merge: waits for <what>][ | gaps: <gap>; <gap>][ | owed before the merge: <X> (<who>)[; <X> (<who>)]][ | long gate <CR-n> at <sha7>: <result>]
```

- **`handed back:`** is a prefix for the agent. It is never said to the user (Q10).
- **`<icon> <word>`:** the icon and state word of the CR's `label`, from the same functions
  (`status/words.py`'s `READY_ICON` and `stack_words.ready_word`, as `state_label` uses them).
  They are never computed another way: 🟢 `ready to merge`, 🟤 `PR in draft`, 🟣 `ready locally`.
- **`<CR-n> <slug>`:** the CR's id and its folder's slug (the folder name after its `<n>-`
  prefix), so the agent names the CR by number and slug (`status-layout.md`, "A CR's name").
- **`<PR link>`:** the full URL the record holds (`c.shown_pr()`), never shortened or named. A
  CR ready locally prints `no PR yet` in its place.
- **`do not merge: waits for <what>`:** only for 🟤. `<what>` comes from
  `stack_words.draft_waits`, the same words as the `label`'s `waits for`.
- **`gaps: …`:** the gaps of the CR's last `handback ready` event (`events.jsonl`): the text
  after `gaps: ` in its `note`, as `driver.md` makes a Driver write it (`… gaps: <gap>; <gap>`,
  or after `; ` in a draft's text), copied unchanged. With no gaps, the segment is absent and the
  line says nothing about gaps.
- **`owed before the merge: <X> (<who>)`:** one clause for each open step below (Q5, Q11). With
  none, the segment is absent. The user may merge anyway, and that merge is recorded as any merge.
  - **The long gate:** the CR's long gate at its recorded head is not `passed`, `carried`,
    `exempt` or `waived` (`status/gate.py`'s `gate_view` state is `none`, `queued`, `running` or
    `failed`). `<X>` is `its long gate passes at <sha7>`.
  - **An order:** an order on this CR is open and not yet applied (`o.cr == c.id`, `o.done`
    empty, `o.applied` false or None). `<X>` is `O-<k> <kind> is applied`. An applied order
    waiting for `order done` adds no clause (Q12).
  - **`<who>`, for both:**
    - for the long gate, `its Driver` while the host shows the CR's Driver live. On Claude Code
      that means an agent is recorded and is neither reported stopped (the reading of
      `commands/activity.py`'s `stopped_agents`, extended to a ready CR's agent) nor ended (the
      reading of `batch_status.py`'s `_ended_unrecorded`);
    - otherwise, `the Foreman` in Foreman mode and `the Chief of Staff` in direct mode;
    - an order is always owed by the steering role;
    - on Copilot, where the record cannot read a Driver's end (both readings return nothing
      there), the long-gate clause names the steering role (Q13). That host path is unproved.
- **`long gate <CR-n> at <sha7>: <result>`:** the CR's long gate at its head, from `gate_view`
  (Q8):
  - `passed` gives `passed`;
  - `carried` gives `passed (carried from <sha7>)`;
  - `failed` gives `failed`;
  - `none`, `queued` and `running` give `not run`, with ` (queued)` or ` (running)` added;
  - `exempt` gives `exempt: <rule>`;
  - `waived` gives the gate text (`waived → CR-k (#n)` or `waived → follow-up <folder>`).

  `<sha7>` is the first seven characters of the recorded head. With no head, the segment is
  absent. The clause names what the record holds. The local run that a project's rules owe is in
  the Foreman's ask, not here (section 3).

Examples, with batch-31's fields:

```
handed back: 🟢 ready to merge CR-470 slim-session-start-md-split-by-role-forg https://github.com/gsemet/chantier/pull/447 | gaps: no screenshot of the pane from a real session | long gate CR-470 at 1a2b3c4: exempt: AGENTS.md: …
handed back: 🟢 ready to merge CR-468 board-server-notifies-when-a-cr-arrives https://github.com/gsemet/chantier/pull/446 | owed before the merge: its long gate passes at 9a8b7c6 (the Foreman); O-21 note is applied (the Foreman) | long gate CR-468 at 9a8b7c6: not run
handed back: 🟤 PR in draft CR-466 own-cr-branch-rebase-and-force-push-pre- https://github.com/gsemet/chantier/pull/443 | do not merge: waits for its turn out of draft | long gate CR-466 at 5d6e7f8: exempt: …
```

The CLI prints English words. The Chief of Staff says the line in the user's language. It keeps
the icon, the link, the ids and each gap's text unchanged, and drops the `handed back:` prefix
(section 3).

### 2. The `batch:` line in `status` (CLI)

This line also comes from the new module. It is printed as the second line of `status`, right
after the existing first line (`_batch_line`). The first line does not change: the scenario
parses it (`split(" live ")`) and `status-layout.md`'s header copies from it.

```
batch: shape <shape>; slots <live>/<slots>; steering <who>; rounds <n>[ (CR-k <m>, …)]; budget <spent> of $<budget>|budget none (spent <spent>); long gate owed: <CR-n> (<who>), …|none; merges: the user[; under the grant: the release/fix PR (steering session)][; rules: <skill folder>/references/reload-rules.md (reread after a compaction)]
```

- `shape`: `shape_word(d.mode)`.
- `slots`: `len(held(d))` and `d.slots`, the same figures as the first line's `live`.
- `steering`: `steering_word(d.steering)`.
- `rounds`: the batch's limit, `(d.settings or BatchSettings()).max_rounds`. The parentheses list
  each CR granted another limit (`c.rounds`, from `order rounds`) with its own.
- `budget`: `spent_text(d)` and `d.budget_usd`, or `budget none (spent <spent>)` with no budget.
- `long gate owed`: each ready CR whose long gate at its head is open (section 1's long-gate
  clause), with the same `<who>`. With none, `none`. It is the same fact as the `handed back:`
  lines, so the two never disagree (Q6).
- `merges: the user`: always printed. The Chief of Staff and the Foreman never merge for the
  user (`chief-of-staff.md`, "Never merge for the user").
- `; under the grant: the release/fix PR (steering session)`: only when `d.release` holds a
  grant (`autonomous` above 0 or `fixes` true). Under that grant the steering session merges the
  release PR or its fix PRs (Q9).
- `; rules: …`: only in the fallback of "The byte limit" below (Q7). The path is built the way
  `stack_shape.shape_line` builds its `foreman-stack.md` one (`skill_dir().as_posix()`).

The line shows only what the CLI holds. The CLI does not read the project's rules. Whether a
project's rules ask a CR for a local run by shape (CR `own-gate`) stays a card's judgement.

### 3. The cards

- **`skills/chantier/references/reload-rules.md` (new):** a short piece, at most about 2,500
  bytes, with a `#` title and four bullets. Each bullet restates its rule in one or two sentences
  and names the section that holds it in full. The full rules stay where they are; no rule moves.
  - **Reports:** before a report, read `status-layout.md` whole and run `status --refresh`. Copy
    the header from `status`'s first line and its `batch:` line. Copy each icon from `label`.
  - **The ready words:**
    - say "ready to merge" only for 🟢, "PR in draft" with "do not merge" and what it waits for,
      and "ready locally" for a CR with no PR. "Ready" alone is never used, and the icon is the
      present state;
    - for each CR you name to the user, copy its `handed back:` line from `status` with the
      prefix dropped: its icon, its full link, each gap, its `owed before the merge` clauses
      (the user may merge anyway; record it as any merge) and its long gate clause;
    - add the local run the Foreman's ask carries (`local gate <cr> at <sha7>: …`); when the ask
      and the line differ, the ask wins (`chief-of-staff.md`, "The words to the user").
  - **The shape:** read it on the `batch:` line. In a stack, read the manifest's `batch:stack`
    action and the shape line's `alone asks`. Who owes a local run follows the project's rules
    and `driver.md`'s long-gate rule.
  - **Who merges:** the user only; never merge for the user. Under a release grant, the steering
    session merges the release PR or its fix PRs, as the `batch:` line says. A merge the user
    makes is recorded with `order merged`.
- **`skills/chantier/references/startup-manifest.json`:** one action, `"reload:rules":
  ["reload-rules.md"]`, outside `reload`. The `reload` list does not change, so the piece itself
  is not counted. The manifest line is counted in every role's startup and reload ("The byte
  limit").
- **`skills/chantier/references/session-start.md`, "5. Reload":** one short sentence: after the
  reload, the Chief of Staff and the Foreman read the manifest's `reload:rules` before their next
  act. This section is counted in the reload budget.
- **`skills/chantier/references/foreman.md`, opening:** after "again after a compaction: reread
  only those startup sections", add "and the manifest's `reload:rules` reading". In the fallback,
  name the `batch:` line's `rules:` pointer instead. This opening is not in the Foreman's counted
  boot.
- **`skills/chantier/references/chief-of-staff.md`, "While it runs", "The words to the user":**
  - `status` prints a `handed back:` line for each CR handed back. The prefix is never said to the
    user.
  - The words said to the user are that line in the user's language: its icon, its full PR link
    (never a named link), each gap next to the link, its `do not merge: waits for` text on a
    draft, and its `owed before the merge` clauses. Those clauses tell the user what is still
    owed; the user may merge anyway, recorded as any merge.
  - Its `long gate` clause is what the record holds. The local run that the project's rules owe
    comes from the Foreman's ask (`local gate <cr> at <sha7>: …`), which the Chief of Staff adds.
    When the ask and the line differ, the ask wins.
  - Nothing in the line is judged.
  - In the plain-ask bullet ("quote each gap of the ask next to the PR's link"), add that the line
    carries the same gaps from the hand-back.
  - The rule "say 'you can merge' only after the `ready-to-merge` line reached you" stays: the
    line gives the words, the ask gives the moment.
- **`skills/chantier/references/status-layout.md`, "The rules of every report":** one bullet:
  - the batch's state in the header is copied from `status`'s first line and its `batch:` line;
  - a CR named in **Notes** or **For you** as ready to merge or in draft is written from its
    `handed back:` line, with the prefix dropped and the ask's local run added as above;
  - the skeleton and the columns do not change.
- **`CONTRIBUTING.md`:** add `reload-rules.md` to the list of `references/` files (near line 64)
  as "the rules re-read after a compaction".

`agents/` and `com.github.copilot/agents/` do not change: the agent files only name their card.

### 4. Size and layout

- `commands/batch_status.py` has 400 lines, the most a file may hold (`CONTRIBUTING.md`, "File:
  at most 400 lines"). It only gains the import and the two calls.
  - To stay at or under 400 lines, existing helpers move, with no change in behaviour, into a
    module of their own, never into `status/ready_line.py`. For instance, `_order_lines`,
    `_late_suffix` and `_stack_driver_lines` move to `commands/batch_status_orders.py`.
  - `_ended_unrecorded`, which the new module reads, moves into a shared module the same way if
    importing it from `batch_status.py` would make an import cycle.
- Every new or changed `.py` file, tests included, stays at or under 400 lines.
  `test_startup_manifest.py` is at 400 and `test_plugin_files.py` at 399. Nothing is added to
  either. New checks go in new files.

### Order and rebase on batch-31's siblings

**This CR comes last** of the batch's CRs that touch these files: after `dynamic-port`
(`long-gate-webui-check-starts-a-second-bo`), after `own-gate` and after CR-471 (`slim-cards`).
It starts once those three are merged (or dropped), rebased onto that head. Its PR's base is the
default branch at that head.

What the others change:

- **CR-471** (`slim-cards`) splits `chief-of-staff.md`, `foreman.md` and `driver.md` into pieces
  read by new `startup-manifest.json` actions, and keeps the manifest under its byte limit.
- **CR `own-gate`** (`local-long-gate-rule-outside-a-stack-and`) rewrites the local-gate wording
  of the same cards, including "The words to the user" and the plain-ask bullet.
- **CR-466** (`own-branch-push`) adds refused-rebase sections to the same three cards.
- **`dynamic-port`** changes the long gate's webui check. This CR does not touch that code, but
  its scenario step goes in the same `scenario/run_scenario.py`.

After the rebase, the Driver finds each place by its words, wherever CR-471 put it: "The words to
the user", "quote each gap", "again after a compaction", "5. Reload", "The rules of every
report". It adds its sentences in the piece where the rule now lives, and keeps CR-471's file
split, its manifest form and its moments list.

- If CR-471 adds a moments list to each entry card, the `reload:rules` action is named there too,
  as CR-471's test asks.
- If `own-gate` has landed, `reload-rules.md`'s shape bullet takes its per-shape wording.

**The byte limit.** The Chief of Staff's reload measures 12,527 bytes on Claude Code and 12,533 on
Copilot, of the 12,544-byte limit. This CR adds two counted things:

- the manifest's `reload:rules` line, counted in every role's startup and reload, since the
  manifest is in every role's required readings;
- the one sentence in "5. Reload", counted in every role's reload.

It is measured at the rebased base and at the head, by the `startup-bytes` lines of
`test_startup_manifest.py`, for every role and both hosts. The limit is not raised. If either
measure goes over the limit, the Driver does not hand back blocked (Q7). Instead:

- it drops the manifest line and the sentence together;
- `status`'s `batch:` line ends with the `rules:` pointer (section 2). `status` is already read
  at every reload ("5. Reload": `seat`, `status`), so the pointer reaches the Chief of Staff and
  the Foreman at no counted byte;
- `foreman.md`'s opening names the pointer, and `reload-rules.md` stays (neither is counted);
- the tests follow the form shipped (Evidence);
- the PR says which form shipped and quotes the `startup-bytes` figures that decided it.

## Out of scope

- No change to `status`'s first line, the CR rows, `STATUS.md`, `STATUS.json`, the board, the
  pane, `live` or the watcher's lines. The new lines are `status` only.
- No change to `asks`, `handback`, `ship`, `gate` or the Foreman's ask format (`foreman.md`'s
  `asks` line list).
- The CLI does not read the project's rules (AGENTS.md) and does not decide who owes a local run
  by shape. That is CR `own-gate`'s card rule.
- No change to `status-layout.md`'s skeleton or columns, including the CR table's `[PR](url)`
  column.
- No change to `agents/`, `com.github.copilot/agents/`, `hooks/` or `types/`, so no `just mod`.

## Evidence

- **Tests in-process on a prepared state:** a new file,
  `skills/chantier/scripts/cli/tests/test_ready_line.py`, parametrized, fast, under 400 lines.
  - **The icon and word:** a batch with one CR per case. Each prints its `handed back:` line with
    the exact icon and word, checked against the CR's `label` (`state_label`):
    - 🟢 ready to merge (`pr_draft=False`, on the default branch);
    - 🟤 PR in draft (with ` | do not merge: waits for …`);
    - 🟣 ready locally (`no PR yet`).
  - **Gaps:** a `handback ready` note ending `gaps: a; b` gives ` | gaps: a; b`. A note with no
    gaps gives no `gaps` segment.
  - **The long gate clause:** one case for each `gate_view` state (passed, carried, failed, none,
    exempt, waived), and the word `long gate`, never `local gate`.
  - **`owed before the merge`:**
    - a head with no pass and no live Driver gives `(the Foreman)` in Foreman mode and
      `(the Chief of Staff)` in direct mode;
    - on Claude Code, a live Driver gives `(its Driver)`;
    - on a `copilot` batch, the steering role is named (Q13);
    - an unapplied order gives `O-<k> <kind> is applied`, and an applied order not done gives
      none (Q12);
    - two open steps are joined by `; `;
    - none gives no segment;
    - no line holds `do not merge before`.
  - **The `batch:` line:**
    - it is the second line, in Foreman and direct mode and for each shape;
    - the rounds limit with a CR's own grant;
    - the budget, and `budget none`;
    - `long gate owed: none`, and with a CR;
    - `merges: the user`, and with a release grant
      `; under the grant: the release/fix PR (steering session)`;
    - the first line unchanged.
  - **No line** for a queued, working, blocked, merged or dropped CR.
- **Tests on the shipped files:** a new file, for instance
  `skills/chantier/scripts/cli/tests/test_reload_rules.py`. It reads the cards and the manifest
  from the repository as shipped, at the head under test, not from a copy.
  - **With the manifest form:**
    - `startup-manifest.json` has the action `reload:rules` naming `reload-rules.md`, and `reload`
      does not list it;
    - `session-start.md`'s "5. Reload" and `foreman.md`'s opening name `reload:rules`.
  - **With the fallback form:**
    - no `reload:rules` action;
    - `status`'s `batch:` line ends with the `rules:` pointer (checked in-process);
    - `foreman.md`'s opening names it.
  - **In both forms:**
    - `reload-rules.md` holds the four rules' key words: `status-layout.md`, `handed back:`,
      `owed before the merge`, `batch:`, `batch:stack`, `under the grant`, `order merged`;
    - `chief-of-staff.md`'s "The words to the user" (or the piece where CR-471 moved it) names
      the `handed back:` line, its prefix never said, and the ask winning on the local run.

  The existing `test_startup_manifest_measures_every_real_role_and_host` keeps every role's
  startup and reload at or under 12,544 on both hosts. The PR quotes the `startup-bytes` lines of
  the Chief of Staff and the Foreman, before and after.
- **Scenario:** in `scenario/run_scenario.py`, after CR-101's `handback ready`, near "a
  hand-back writes the state and prints the line to send". One check that `status` prints a line
  starting `handed back: ` with `CR-101` and `pr101`'s full URL, and a second line starting
  `batch: shape ` that holds `merges: the user`.
- **Host matrix (the Driver's-end reading):**
  - Claude Code: the reading is proved by `stopped_agents` and `_ended_unrecorded` as today, and
    by the in-process tests.
  - Copilot: the steering role is named by rule. Unproved on a real host.
- **Gates:**
  - `just check` in the worktree at the pushed head, and `just eval-dry-run` (a change under the
    CLI's `src/`).
  - The long gate is the pipeline's `just scenario (ubuntu-latest)` job, green at the PR's head.
  - The local run follows the project's rule for batch-31's shape (AGENTS.md, as CR `own-gate`
    leaves it).
- **The PR's Deliverables** quote one real `status` output from the worktree on a prepared batch,
  showing a 🟢 and a 🟤 `handed back:` line and the `batch:` line.

## Open questions

None. The user's answers ready-line-Q5 to Q13 settled the questions of the earlier drafts and the
critic's findings.
