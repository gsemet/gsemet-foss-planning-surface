# Running batch or next batch: the factory mode removed

A grilled CR goes to the next batch (`3-ready`, the default) or, when a batch is open, to the
running batch (`4-batch/1-pending/`). The choice is made when the spec-writer starts. Placing a CR
in `1-pending` is the go, in every mode. The factory mode (`open --factory`, `order factory on|off`,
the factory pause) is removed. The board's backlog page (Triage) splits its last column into
"running batch" over "next batch", always.

## Goal, in the user's terms

The user's words (factory-Q1, 2026-11-21): "En fait c'est pas un mode du batch. C'est un mode du
planning avant. En mode normal, on grille et quand c'est prêt par défaut on prépare le prochain
batch. Il y a juste l'option en plus d'envoyer directement au batch en cours s'il y a un batch en
cours. C'est donc pas un mode spécial, c'est juste que quand une CR est suffisamment grillée, au
moment de lancer le spec writer il faut demander si c'est à rajouter au batch en cours (donc vers
pending) ou pour le prochain (ready)."

In English:

- There is no factory mode, and no other special mode.
- When a CR is grilled enough, at the spec-writer's start, the user is asked where it goes:
  - the next batch (`3-ready`), which is the default;
  - or the running batch (`4-batch/1-pending/`), when a batch is open.
- `3-ready` always means the next batch. `4-batch/1-pending/` is the running batch.
- On the board's backlog page, the user can place a CR in either one, in every mode (parallel,
  series, stack): "même en mode séries ou parallel on peut avoir envie de mettre dans le batch en
  cours" (park-live-Q8).

## Decisions carried (02-answers.md)

| Answer | Decision | Where it lands below |
| --- | --- | --- |
| factory-Q1 | Factory is not a mode. At the spec-writer's start the user picks the running batch (`1-pending`) or the next batch (`3-ready`). The default is the next batch. | 1, 2, 3 |
| factory-Q2 | Placing a CR in `1-pending` is the go, in every mode. A Driver takes it when a slot frees. | 2, 3 |
| factory-Q3 | The user chooses on the board (the backlog page's last column, always split in two) and in the grill (the "grilled enough?" question offers both). | 1, 5 |
| factory-Q4 | With no open batch, the CR goes to `3-ready`. | 1, 2, 4 |
| factory-Q5 | A batch's last CR leads to the ordinary pause, then the retro, then the close offer. Until the user's close, it stays the running batch, and a CR placed in `1-pending` starts it again. | 3, 4 |
| factory-Q6 | `open --factory` and `order factory on/off` are removed. Old records with `factory: on` stay readable. | 4 |
| factory-Q7 | A CR reaches `1-pending` when its specification is final (after the critic, when it runs). Until then it waits in its folder, marked for the running batch. | 2, 4 |
| factory-Q8 | Grilled enough: specify now. Spec critic: yes. | (this file) |

## What changes

### 1. The grill: where the CR goes (cards)

These cards change: `skills/chantier/references/chief-of-staff.md`,
`skills/chantier/references/griller.md` and `skills/chantier/references/concepts.md`.

**The "grilled enough?" question.** It is the closing question of the full restatement ("Shared
understanding" in `chief-of-staff.md`; the Griller follows the same rule).

- **With an open batch** (running or paused, not closed), the question offers where the CR goes, in
  the format of "Asking the user: a series":
  - A. specify, for the next batch (`3-ready`), recommended (the default);
  - B. specify, for the running batch `<batch-id>` (`4-batch/1-pending/`);
  - the existing "not yet" path.
- **With no open batch,** the question does not offer the running batch: the CR is for the next
  batch (factory-Q4).
- **Recording.** The answer goes into `02-answers.md` with the critic's yes or no, as today (for
  example `Destination: next batch (3-ready).` or `Destination: running batch batch-12.`).

**That answer is the user's word for the move.** The card keeps its rule "a CR moves to `3-ready`
only on the user's word". The destination chosen at "grilled enough?" is that word, and for the
running batch it is also the go (factory-Q2). Once the specification is final, after the critic
when it runs and after its open questions have been answered and the spec rewritten (factory-Q7):

- **Next batch:** the Chief of Staff, or the Griller that ran the grill, runs
  `$CHANTIER triage <folder> --ready`. No other question is asked.
- **Running batch:** the Chief of Staff runs `$CHANTIER order add --note <folder>` and handles the
  order as usual: in Foreman mode it relays the order line to the Foreman; in direct mode it takes
  the CR when a slot frees. No other question is asked. A Griller never runs `order`; see 2.
- **If the batch closed while the CR was being specified,** the CR goes to `3-ready` instead
  (factory-Q4): `triage --ready`, and the user is told in one line.

**The running-batch mark.** Between the spec-writer's start and the final specification, a CR bound
for the running batch carries the mark (section 2), set at the start with
`triage <folder> --running-batch`. A CR bound for the next batch carries no mark.

**Text to remove from `chief-of-staff.md`:**

- the section "Factory batches";
- the paragraph after the "Backlog and grill" code block, "In a factory batch ... `triage --ready`
  also joins the CR";
- "in a factory batch it joins the batch at once" in the spec-writer paragraph;
- the plan's "**Factory.**" paragraph in "Starting a batch";
- `--factory` in the `open` synopsis, and the sentence "with no folder it opens ... a factory batch
  (`--release` is refused then ...)". `open` with no folder still opens a paused batch with no CR:
  see open question 5;
- "(in a factory batch, by `triage --ready`)";
- the `order factory on|off` line of the order commands' block;
- the table row "the Foreman's `ready <batch>` at a factory batch's pause";
- the bullets "The pause of a factory batch" (Foreman mode) and "The pause of a factory batch
  (direct mode)";
- "except a factory batch" / "except in a factory batch" in the direct-mode rules (around the
  lines on `triage --ready` and "touch the running batch from backlog work").

**Text to replace in `chief-of-staff.md`:**

- The direct-mode rule becomes: `triage --ready` never joins the running batch. A CR joins it only
  by `order add`, from a destination the user chose (the grill or the board).
- "New work for the paused batch is `order add`" stays. Add one sentence there and in the pause's
  close offer: until the user's `close`, the paused batch is still the running batch, and a CR
  placed in `1-pending` (by `order add`) starts it again at the next `take` (factory-Q5).

**`concepts.md`.**

- "Lifecycle": `3-ready/` stays "waiting for the next batch". Add that `4-batch/1-pending/` is "the
  running batch, not started", where a CR arrives by `open` or `order add`, the latter from the
  destination the user chose.
- "`3-ready`": add that it always means the next batch.
- "Batch lifecycle" step 1: remove the factory sentences ("A **factory** batch ... turns the
  factory off."). Keep the batch opened with no CR (paused, no cost, no retro, no close offer at
  that pause).
- Step 3: one sentence saying that a CR placed in `1-pending` before the close starts the paused
  batch again.

### 2. The mark and the CLI

The CLI lives in `skills/chantier/scripts/cli/src/chantier/`.

**New: `triage <folder> --running-batch`.** It is a fourth choice next to `--priority`, `--ready`
and `--inbox` (exactly one of the four; `TRIAGE_USAGE` and `declare/intake.py` name it). It runs on
the user's word, like every `triage`, and is role-free.

- **With an open batch,** it writes the mark `work/running-batch` in the CR's folder: one line, the
  time and the open batch's id. It moves no folder. It prints
  `<slug> marked for the running batch <batch>: it joins once its specification is final (\`order add --note <folder>\`)`.
  It accepts a folder in the inbox, `2-backlog/P1`..`P4` or `3-ready`.
- **With no open batch** (no batch folder, or the batch is closed), it is refused with exit
  precondition: `no open batch: <slug> goes to the next batch (\`triage <folder> --ready\`)`
  (factory-Q4; see open question 3 for the board).
- **Clearing the mark.** Any other `triage` of that folder (`--ready`, `--priority`, `--inbox`)
  removes it (the user changed the destination), and so do `abandon` and `order add` of the folder.
  `order add` moves the folder into `4-batch/1-pending/` and deletes `work/running-batch` from it.
- **A stale mark** is a mark whose batch id is not the open batch. The CLI treats it as no mark,
  and `status` names it (below).

**`status`** (`commands/batch_status.py`, and the no-batch path) gets one line when marked CRs
exist:
`running batch: <n> CRs marked, not joined: <folder> (specifying|specified), ...`. Here
`specifying` means a `work/specifying` exists and `specified` means `03-change-spec.md` exists with
no `work/specifying`. When a CR is `specified`, the line ends with
`: \`order add --note <folder>\` once its specification is final`. A stale mark gets its own line:
`running batch: <folder> marked for <old-batch>, which is closed: \`triage <folder> --ready\``.

**The Griller (`griller.md`).**

- **Section "Never":** remove its exception "(one exception: in a factory batch your
  `triage --ready` ... records an `add` order itself ...)". A Griller never runs `order`.
- **Section "Telling the Chief of Staff":**
  - Remove the factory paragraph.
  - For a CR marked for the running batch, the line `[griller→chief-of-staff] <slug> specified` is
    no longer optional. The Griller sends it once the specification is final.
  - With no live Chief of Staff, the Griller tells the user. The Chief of Staff then finds the CR
    on `status`'s `running batch:` line and adds it after reading its `03-change-spec.md`.
  - For a CR bound for the next batch, the Griller runs `triage --ready` itself once the spec is
    final (the user's destination answer is the word).
- **A Griller in a worktree** runs no `triage` (unchanged): the Chief of Staff places the files,
  then marks the CR or moves it to `3-ready` as the answer says.

**`routing.md`.**

- Griller → Chief of Staff: remove `<the order line>` (the factory `add`). Note that `<slug>
  specified` is required for a CR marked for the running batch.
- Foreman → Chief of Staff: remove "(also at a factory batch's pause)".

### 3. The go and the batch's end

- **Placing a CR in `1-pending` is the go** (factory-Q2), in every mode (parallel, series, stack),
  in Foreman and in direct mode.
  - The steering session takes it when a slot frees, as an `add` order is taken today.
  - The cards say so in `chief-of-staff.md` ("Only the user starts work" keeps its rule: the
    destination the user chose is that word) and in `foreman.md`.
  - The budget rule is today's `order add` rule, unchanged.
- **The batch's last CR** (`commands/endpause.py`): `_next_line` loses its factory branch. Every
  batch's end prints the ordinary
  `next: the retro (with its critic), then offer the close ...` line.
  - The retro, its critic, `final` (Foreman mode) and the close offer follow as for any batch
    (factory-Q5).
  - The `factory` parameter of `_next_line` goes away.
- **A CR placed in `1-pending` after that pause and before the close** (`order add`) starts the
  batch again at the next `take`. Today's rules for a paused batch already allow this; the cards
  and the CLI keep them.
  - **Retro:** the next pause adds its own retro section (concepts, "each later pause adds its own
    section").
  - **Foreman:** the Foreman gets the order's line as for any paused batch.
- **`foreman.md`:**
  - Remove the paragraph "In a factory batch (`status` says `factory: on`) ...".
  - Remove "(so is a factory batch at its pause, see below)".
  - Remove the sentences on `origin: "triage --ready"` and on the `factory` order.
  - The paragraph "An order that adds work leaves the paused batch paused ..." stays as is.
- **Host references:** `hosts/claude-code.md` and `hosts/copilot.md` drop "or a factory batch at
  its pause" from their heartbeat sentences.

### 4. Removed commands; old records stay readable

**`open --factory` is removed.**

- **Argument:** `declare/opening.py` loses the argument, so `--factory` is refused by the
  argument parser (exit usage).
- **`commands/opening_record.py`:** loses the `args.factory` refusal with `--release`, and the
  rule `factory=bool(args.factory or not args.items)`. An `open` with no CR no longer sets
  anything factory.
- **`commands/opening.py`:**
  - The brief's first bullet no longer writes `Factory: on|off.` (`Steering: <s>.` alone).
  - The open line loses `, factory`.
  - `FACTORY_NEXT` and the `3-ready holds ... not joined` lines go away.
  - The `opened` event loses `factory`.

**`order factory on|off` is removed.**

- `"factory"` leaves `ORDER_KINDS` and the apply table (`commands/orders_apply.py`, `_factory`).
  `order factory ...` now gets the existing `order kind: one of ...` refusal (exit usage).
- `commands/orders.py` loses `FACTORY_USAGE` and the factory branches (lines 55-56, 192, 208).
- `declare/orders.py` drops `factory on|off` from its help.

**`commands/factory.py` is deleted.**

- `no_cr_lines` moves to `commands/batch_status.py` (or next to it) without its factory branch,
  so it always prints `no CR yet: \`order add --note <folder> --batch <id>\` joins one`.
- `FACTORY_ON`, `factory_lines`, `not_joined_line`, `not_joined_text`, `ready_not_joined`,
  `set_factory` and `switch_factory` go away with their callers:
  - `batch_status.py`: the status line's ` factory: on`, and `factory_lines`;
  - `opening.py`.

**`commands/intake.py`:** `_join_factory` is deleted. `triage --ready` only moves the folder to
`3-ready`. `declare/intake.py` drops "in a factory batch it joins that batch".

**`commands/orders_apply.py`:** the "factory off: the release CR ... joined" line goes away. A
release CR joins as in any batch.

**Old records stay readable** (factory-Q6).

- **The record field.** `BatchRecord.factory` (`core/records.py`) is removed from the model. The
  base `Record` keeps unknown keys (`extra="allow"`), so a `batch.json` with `"factory": true`
  still reads, and is written back unchanged. Such a batch behaves as an ordinary batch.
- **Orders and events.** An old order of kind `factory` (always done) and an old `factory` event
  in `events.jsonl` still read. `status`, the board and `close` do not fail on them, and a done
  `factory` order is no cause to refuse `close`.
- **Briefs.** An old `brief.md` with `Factory: on.` is left as it is.
- **Display.** No output, view or file shows a factory word any more:
  - `status/markdown.py`: ` · factory: on` in `STATUS.md`;
  - `status/views.py`: the `factory` key of `STATUS.json`. The CR board pane
    (`hooks/register.tsx`) never read this key, so no pane screenshot is owed and no `hooks/` or
    `types/` file changes;
  - `core/surface_batches.py`: `, factory on`;
  - `board/state.py`: the `factory` key, lines 54 and 247;
  - the web client: `steeringFactoryWord` in `js/model/semantics.js`, its uses in
    `js/views/batch.js` and `js/views/home-batch.js` (back to `steeringWord`), and
    `batch.factory_on` in `js/i18n/en-batch.js` and `fr-batch.js`.

### 5. The board: the backlog page's last column split in two (web client)

Read `skills/chantier/scripts/cli/src/chantier/clients/web/DESIGN.md` first and keep it true
(AGENTS.md).

**Triage view.** In `js/views/triage.js` and `js/triage/columns.js`, the last column (today
`3-ready`) is split horizontally, as Jira does, into two lanes of one column, built by
`js/ui/column.js` like the Backlog column's lanes. It is always shown, in every mode, with or
without a batch (factory-Q3).

- **Top lane, "running batch" (`4-batch/1-pending/`).**
  - **What it shows:** the open batch's CRs not yet taken (the record's queued CRs, from the state
    the board already sends, as the Kanban reads them), and the backlog CRs marked for this batch,
    each with its grill state (`specifying`, `specified`).
  - **Its sub-line:** the batch's id and state (today's `triage.running` words). With no open
    batch, it reads "no open batch: a CR goes to the next batch", and a drop there is refused with
    the CLI's message (see open question 3).
- **Bottom lane, "next batch" (`3-ready`).** Today's `3-ready` column: its counts, its "the next
  batch is ready" button (`next-batch.json`) and its foot, unchanged.
- **Drops and moves.**
  - Dropping a backlog post-it on the top lane runs the same function as
    `triage <folder> --running-batch`: the mark.
  - Dropping a marked post-it on the bottom lane, or on the inbox or a priority row, runs the
    matching `triage` move, which clears the mark.
  - A CR already in `4-batch/1-pending/` is shown but not draggable. Taking a CR out of the batch
    is park-live-cr's.
  - The selection bar offers the same two targets.

**Server.** In `board/write_api.py`:

- `COLUMNS` adds a `running-batch` target, which calls the lifecycle function behind
  `triage --running-batch` (no batch file is touched; the board still never edits a batch).
- Its journal words are `<slug> → running batch <batch> (marked)`, as a `board@1` `move` line
  (waking).

In `board/backlog.py`, each item carries the mark when it has one (`running_batch: <batch-id>`),
so the client can place it in the top lane.

**The Chief of Staff on that line** (`chief-of-staff.md`, "A watcher's end" and the "rescan" row).
A `board wrote (...) → running batch` line is the user's destination, and for the running batch
it is the go (factory-Q2). The Chief of Staff:

- reads the CR's folder;
- if its specification is final (written, no spec-writer running, no open question left), runs
  `order add --note <folder>` and handles the order as usual, with no further question;
- otherwise tells the user in one line that the CR joins once its specification is final.

The other `board wrote` lines keep "one line, no action".

**Words.** In `js/i18n/en-*.js` and `fr-*.js`:

- the two lane titles, "Running batch" / "Batch en cours" and "Next batch" / "Prochain batch";
- the no-open-batch line;
- `kanban.ready_sub` keeps "waits for the next batch".

### 6. Docs

- **`README.md`:** the section "Factory mode" is replaced by a short section "Running batch or next
  batch". It covers the choice at "grilled enough?" or on the board, the default (the next batch),
  `1-pending` as the go, and the ordinary pause, retro and close.
- **`docs/use-cases.md`, `docs/use-cases-direct.md`, `docs/use-cases-foreman.md`:** the factory
  sentences become the same behaviour.
- **`docs/batch-lifecycle-texts.md` and `docs/batch-lifecycle.svg`:**
  - Remove "a factory batch: no close offered;" and "a factory batch: `order factory off`,".
  - "or, in a factory batch, `triage --ready`" becomes "or `order add`, from the running batch's
    lane or the grill".
  - Keep the two files in step as the repository's checks require.
- **`scenario/README.md`:** the factory bullet (lines 247-251) is rewritten for the new steps
  (Evidence).
- **`docs/release-notes/2026-11-19-v0.14.0/`:** unchanged (history).

## Out of scope

- park-live-cr (`1-inbox/park-live-cr`), which depends on this CR: taking a CR out of the running
  batch, the `blocked` state, `close` refused with a blocked CR, and dragging a CR out of
  `1-pending` on the board.
- The Kanban view, the home page's backlog block and the terminal client (`clients/tui/`): they
  keep reading `3-ready` as the next batch.
- The spec-writer's own card, the specifying limit (`specifying.parallel`), the spec critic's
  criterion and the `order add` rules (budget, release rule B, refusals).
- Old release notes.

## Evidence

Every check reads the shipped files at the head under test: the cards, `README.md`, the docs, the
web client's files and the CLI's own output from real states built by the CLI's commands. The one
exception is a record with `"factory": true` (below). The real flow can no longer produce it, so it
is a prepared state, named as such and paired with `status` and `close` run on it.

**Tests** (`skills/chantier/scripts/cli/tests/`, in-process, few and parametrized; `just test`
within its limit):

- `triage --running-batch`:
  - with an open batch, it writes `work/running-batch` with the batch id and moves nothing;
  - with no open batch, it is refused (exit precondition, the message names `triage --ready`);
  - `--ready`, `--priority`, `--inbox`, `abandon` and `order add` each clear the mark;
  - `order add` leaves no `work/running-batch` in `1-pending`;
  - a stale mark (another batch id) shows on `status`'s stale line.
- `status` prints the `running batch: ... marked, not joined` line with `specifying`/`specified`.
- `open --factory` and `order factory on` are refused (exit usage).
- `open` with no CR writes no `factory` key, and its brief has no `Factory:` token.
- `triage --ready` with an open batch joins nothing: the batch's CRs are unchanged.
- The last CR's end prints the ordinary `next: the retro ...` line, also for a batch opened with
  no CR.
- A prepared `batch.json` with `"factory": true` and a done `factory` order: `status` runs and
  prints no factory word, and `close` is not refused for that order.
- Board, `backlog.move` to `running-batch`:
  - it writes the mark and one `board@1` `move` line;
  - it is refused with no open batch;
  - it touches no file under `4-batch/`.
- The board's shipped files: `js/model/semantics.js`, `js/views/batch.js` and
  `js/views/home-batch.js` contain no `steeringFactoryWord`, and the i18n files have no
  `batch.factory_on`.
- Update or remove the factory tests:
  - `test_batch_end.py::test_the_end_of_the_last_cr_of_a_factory_batch_waits_for_the_next_ready_cr`;
  - `test_came_back.py::test_triage_ready_of_a_moved_out_cr_joins_a_factory_batch_under_its_number`
    becomes `order add` of the moved-out CR getting its number back;
  - the factory assertions of `test_open_empty_batch.py`, `test_open_no_clone.py` and
    `test_opening_and_restore.py`;
  - `batch_helpers.py`'s factory helper.

**Scenario** (`scenario/run_scenario.py`):

- `empty_batch` loses its factory checks. A batch opened with no CR is paused, with no `factory`
  key, no `Factory:` token and `no CR yet: \`order add ...\``.
- `factory_batch` (16e) is replaced by a step `running_batch`:
  1. A CR is marked with `triage --running-batch` while the batch is open, and `status` shows it
     `specified`.
  2. `order add` places it in `1-pending` and clears the mark, and the steering session takes it.
  3. Its end pauses the batch with the ordinary `next:` line (retro, then close offer).
  4. A second CR placed by `order add` before the close starts it again at the next `take`.
  5. `triage --ready` of a third CR leaves it in `3-ready`, not joined.
  6. `order factory on` is refused.
- The step list at line 115 and `scenario/README.md` are updated.

**Gates:**

- `just check` in the worktree.
- `just eval-dry-run` (the change is under the CLI's `src/`).
- The pipeline's `just scenario (ubuntu-latest)` job green at the PR's head (cards, CLI and
  scenario change).
- Windows coverage by `chantier gate` per AGENTS.md when this CR is on top of its batch's stack.

**No host and default matrix:** the behaviour does not depend on the host or on a configured value.

## Open questions for the user

1. **The board's drop on "running batch" and AGENTS.md.** AGENTS.md says the board "never edits a
   batch". This specification has the drop write the mark only (a backlog file and a `board@1`
   line), and the Chief of Staff then runs `order add` when the specification is final. The other
   way, the board places the CR in `1-pending` itself, needs AGENTS.md's board exception changed.
   Keep the mark (recommended)?
2. **A drop of a CR already specified** (for example from `3-ready`) on "running batch". The drop
   is the go (factory-Q2), so the Chief of Staff adds it at its next wake with no further question.
   Confirm?
3. **A drop on "running batch" with no open batch.** This specification refuses it with the
   message "no open batch: it goes to the next batch". The other way: the drop moves the CR to
   `3-ready` directly. Refuse (recommended), or move?
4. **A refused join.** Example: a release that has started refuses `order add` (rule B), for a CR
   marked for the running batch whose specification has just become final. Should the CR go to
   `3-ready` with the reason told to the user (recommended), or stay marked in its folder until the
   user decides?
5. **`open` with no CR.** It was the factory's way in. This specification keeps it as an ordinary
   paused batch with no CR: no retro and no close offer at that first pause, then the ordinary end
   after its CRs. Keep it, or remove it too?
