# Running batch or next batch: the factory mode removed

A CR grilled enough goes to the next batch (`3-ready`, the default) or, when a batch is open, to
the running batch (`4-batch/1-pending/`). The user picks at "grilled enough?" and at every
spec-writer start. Placing a CR in `1-pending` is the go, in every mode. A CR bound for the running
batch carries a mark (`triage --running-batch`) until its specification is final, then joins by
`order add`. The factory mode (`open --factory`, `order factory on|off`, the factory pause) is
removed. The board's lane for the running batch is the CR `board-running-batch-lane`, filed on top
of this one: this CR gives it the mark function it calls.

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
- This holds in every mode (parallel, series, stack): "même en mode séries ou parallel on peut
  avoir envie de mettre dans le batch en cours" (park-live-Q8).

## Decisions carried (02-answers.md)

| Answer | Decision | Where it lands below |
| --- | --- | --- |
| factory-Q1 | Factory is not a mode. At the spec-writer's start the user picks the running batch (`1-pending`) or the next batch (`3-ready`). The default is the next batch. | 1, 2, 3 |
| factory-Q2 | Placing a CR in `1-pending` is the go, in every mode. A Driver takes it when a slot frees. | 1, 3 |
| factory-Q3 | The user chooses in the grill (the "grilled enough?" question offers both) and on the board (the backlog page's last column split in two, always). The board's part is `board-running-batch-lane` (factory-Q9). | 1; Out of scope |
| factory-Q4 | With no open batch, the CR goes to `3-ready`. | 1, 2 |
| factory-Q5 | A batch's last CR leads to the ordinary pause, then the retro, then the close offer. Until the user's close, it stays the running batch, and a CR placed in `1-pending` starts it again. | 1, 3 |
| factory-Q6 | `open --factory` and `order factory on/off` are removed. Old records with `factory: on` stay readable. | 4 |
| factory-Q7 | A CR reaches `1-pending` when its specification is final (after the critic, when it runs). Until then it waits in its folder, marked for the running batch. | 1, 2 |
| factory-Q8 | Grilled enough: specify now. Spec critic: yes. | (this file) |
| Spec critic run | Fixes 3, 5, 6, 7 (no user question): the state `written`, not `specified`, and a CR added only when no critic runs and no open question remains; the factory test file, i18n key and test lines named; the server API and protocol schema; the three `#factory-mode` links and docs-sphinx-rtd. | 1, 2, 4, 6; Out of scope |
| factory-Q9 | Two CRs. This one keeps the factory mode's removal, the grill's destination, the running-batch mark and `status`. The board's backlog page with its last column split is `board-running-batch-lane`, on top of this one, with the former open questions 1 to 3. | Out of scope |
| factory-Q10 | Every spec-writer start asks the destination, with the same two options, not only the closing "grilled enough?". | 1 |
| factory-Q11 | "Grilled enough?" offers four options: next batch (recommended), running batch, back to the backlog, not yet. | 1 |
| factory-Q12 | The mark is refused for an ungrilled CR ("grill it first"). An automatable `3-ready` CR joins at once with `order add`. | 1, 2 |
| factory-Q13 | When the specification becomes final and `order add` is refused because a release started in the batch, the CR goes to `3-ready` and the user is told in one line. The batch closing: as factory-Q4. The writer not running: restart the server, the CR waits. | 1 |
| factory-Q14 | `open` with no CR stays: an ordinary batch, paused, that waits for its CRs in `1-pending`. | 1, 4 |
| factory-Q15 | A next spec-writer run on the same CR keeps the destination already recorded in `02-answers.md`; it asks only when none is recorded. | 1 |

## What changes

### 1. The grill: where the CR goes (cards)

These cards change: `skills/chantier/references/chief-of-staff.md`,
`skills/chantier/references/griller.md` and `skills/chantier/references/concepts.md`.

**The "grilled enough?" question** (`chief-of-staff.md`, the bullet "**"Grilled enough?"**" of
"Asking the user: a series", and "Shared understanding"; the Griller follows the same rule). Its
options become four, in the format of "Asking the user: a series" (factory-Q11):

- A. specify, for the next batch (`3-ready`) (recommended, the default);
- B. specify, for the running batch `<batch-id>` (`4-batch/1-pending/`);
- C. back to the backlog;
- D. not yet.

With no open batch (no batch, or a closed one), B is not offered and the CR is for the next batch
(factory-Q4): the options are next batch (recommended), back to the backlog, not yet. The card's
example `A. Specify (recommended)`, `B. Back to the backlog`, `C. Not yet` is replaced by the four
options.

**The destination at every spec-writer start** (factory-Q10). Every start of a spec-writer, by the
Chief of Staff or a Griller, asks the destination with the same two options (next batch,
recommended; running batch `<batch-id>`), in the same series format, when a batch is open. The
answer A or B of "grilled enough?" is that ask for the start it triggers; a start with no such
answer just before it (for example a CR grilled in an earlier session) asks it on its own. With no
open batch, nothing is asked: the CR is for the next batch. A next run on the same CR (after the
critic's fixes, or after open questions are answered) keeps the destination already recorded in
`02-answers.md` and asks only when none is recorded (factory-Q15).

**Recording.** The answer goes into `02-answers.md` at once, with the critic's yes or no as today,
for example `Destination: next batch (3-ready).` or `Destination: running batch batch-12.`

**The order at the start.** In `chief-of-staff.md`'s paragraph "On the user's word that a CR is
grilled enough, write `work/specifying` ...": write `work/specifying` first, then, for the running
batch, run `$CHANTIER triage <folder> --running-batch` (the mark, section 2), then start the
spec-writer. A CR bound for the next batch carries no mark.

**That answer is the user's word for the move.** The card keeps its rule "a CR moves to `3-ready`
only on the user's word". The destination chosen is that word, and for the running batch it is
also the go (factory-Q2). The specification is final when `03-change-spec.md` is written, no
spec-writer runs on it, its critic, when due, has run and been applied, and no open question
remains (its answers recorded and the specification rewritten) (factory-Q7; critic fix 3). Then:

- **Next batch:** the Chief of Staff, or the Griller that ran the grill, runs
  `$CHANTIER triage <folder> --ready`. No other question is asked.
- **Running batch:** the Chief of Staff runs `$CHANTIER order add --note <folder>` and handles the
  order as usual: in Foreman mode it relays the order line to the Foreman; in direct mode it takes
  the CR when a slot frees. No other question is asked. A Griller never runs `order`; see 2.
- **`order add` refused** (factory-Q13):
  - a release has started in the batch (rule B): the CR goes to `3-ready` (`triage <folder>
    --ready`, which clears the mark) and the user is told in one line, for example `<slug> goes
    to the next batch: a release started in <batch>`;
  - the batch closed while the CR was being specified: the same, as factory-Q4 (`triage --ready`,
    one line to the user);
  - the writer not running: the Chief of Staff restarts the server as the card already says for
    that refusal, and the CR waits, still marked, then joins with `order add`.

**A `3-ready` CR for the running batch** (factory-Q12). A `3-ready` CR is never marked. When the
user wants an automatable `3-ready` CR in the running batch, the Chief of Staff runs `order add
--note <folder>` at once. The same holds for a `3-ready` CR with a specification: it moved there
once final.

**Text to remove from `chief-of-staff.md`:**

- the section "Factory batches";
- the paragraph after the "Backlog and grill" code block, "In a factory batch ... `triage --ready`
  also joins the CR";
- "in a factory batch it joins the batch at once" in the spec-writer paragraph;
- the plan's "**Factory.**" paragraph in "Starting a batch";
- `--factory` in the `open` synopsis, and the sentence "with no folder it opens ... a factory batch
  (`--release` is refused then ...)". `open` with no folder still opens an ordinary paused batch
  with no CR, which waits for its CRs in `1-pending` (factory-Q14): the sentence says so;
- "(in a factory batch, by `triage --ready`)";
- the `order factory on|off` line of the order commands' block;
- the table row "the Foreman's `ready <batch>` at a factory batch's pause";
- the bullets "The pause of a factory batch" (Foreman mode) and "The pause of a factory batch
  (direct mode)";
- "except a factory batch" / "except in a factory batch" in the direct-mode rules (around the
  lines on `triage --ready` and "touch the running batch from backlog work").

**Text to replace in `chief-of-staff.md`:**

- The direct-mode rule becomes: `triage --ready` never joins the running batch. A CR joins it only
  by `order add`, from a destination the user chose.
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
  that pause), which waits for its CRs in `1-pending` (factory-Q14).
- Step 3: one sentence saying that a CR placed in `1-pending` before the close starts the paused
  batch again.

### 2. The mark and the CLI

The CLI lives in `skills/chantier/scripts/cli/src/chantier/`.

**New: `triage <folder> --running-batch`.** It is a fourth choice next to `--priority`, `--ready`
and `--inbox` (exactly one of the four; `TRIAGE_USAGE` and `declare/intake.py` name it). It runs on
the user's word, like every `triage`, and is role-free. Its work is one lifecycle function (next to
`move_item` in `lifecycle/backlog.py`, or in `lifecycle/stages.py`), which the board's lane
(`board-running-batch-lane`) will call: it writes the mark and touches no file under `4-batch/`.

- **With an open batch** and a grilled CR, it writes the mark `work/running-batch` in the CR's
  folder: one line, the time and the open batch's id. It moves no folder. It prints
  `<slug> marked for the running batch <batch>: it joins once its specification is final (\`order add --note <folder>\`)`.
  It accepts a folder in the inbox or `2-backlog/P1`..`P4`.
- **An ungrilled CR** (factory-Q12): a folder with neither `work/specifying` nor `03-change-spec.md`
  (the cards write `work/specifying` before the mark, section 1). Refused with exit precondition:
  `<slug> is not grilled: grill it first`.
- **A `3-ready` folder** (factory-Q12): no mark. Refused with exit precondition:
  `<slug> is in 3-ready: \`order add --note <folder>\` joins it now`.
- **With no open batch** (no batch folder, or the batch is closed): refused with exit
  precondition: `no open batch: <slug> goes to the next batch (\`triage <folder> --ready\`)`
  (factory-Q4).
- **Clearing the mark.** Any other `triage` of that folder (`--ready`, `--priority`, `--inbox`)
  removes it (the user changed the destination), and so do `abandon` and `order add` of the folder.
  `order add` moves the folder into `4-batch/1-pending/` and deletes `work/running-batch` from it.
- **A stale mark** is a mark whose batch id is not the open batch. The CLI treats it as no mark,
  and `status` names it (below).

**`status`** (`commands/batch_status.py`, and the no-batch path) gets one line when marked CRs
exist:
`running batch: <n> CRs marked, not joined: <folder> (specifying|written), ...`. Here
`specifying` means a `work/specifying` exists and `written` means `03-change-spec.md` exists with
no `work/specifying` (critic fix 3: `written`, not `specified`, since a written specification may
still wait for its critic or its open questions). When a CR is `written`, the line ends with
`: \`order add --note <folder>\` once no critic runs and no open question remains`. A stale mark
gets its own line:
`running batch: <folder> marked for <old-batch>, which is closed: \`triage <folder> --ready\``.

**The Griller (`griller.md`).**

- **Section "Never":** remove its exception "(one exception: in a factory batch your
  `triage --ready` ... records an `add` order itself ...)". A Griller never runs `order`.
- **The grill's close and the spec-writer's start:** the four options and the destination asked at
  every start, as section 1; the Griller runs `triage --running-batch` after writing
  `work/specifying` for a CR bound for the running batch.
- **Section "Telling the Chief of Staff":**
  - Remove the factory paragraph.
  - For a CR marked for the running batch, the line `[griller→chief-of-staff] <slug> specified` is
    no longer optional. The Griller sends it once the specification is final (section 1).
  - With no live Chief of Staff, the Griller tells the user. The Chief of Staff then finds the CR
    on `status`'s `running batch:` line and adds it after reading its `03-change-spec.md`.
  - For a CR bound for the next batch, the Griller runs `triage --ready` itself once the
    specification is final (the user's destination answer is the word).
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
  rule `factory=bool(args.factory or not args.items)`. An `open` with no CR stays allowed
  (factory-Q14): an ordinary paused batch, which sets nothing factory.
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
  - the web client (read `clients/web/DESIGN.md` first and keep it true, AGENTS.md):
    - `steeringFactoryWord` in `js/model/semantics.js`, and its uses in `js/views/batch.js` and
      `js/views/home-batch.js` (back to `steeringWord`);
    - the i18n keys `batch.factory_on` and `batch.no_cr_yet_factory` in `js/i18n/en-batch.js` and
      `fr-batch.js`, and the branches `batch.factory ? 'batch.no_cr_yet_factory' :
      'batch.no_cr_yet'` in `js/views/batch.js` (line 127) and `js/views/home-batch.js` (line
      69), which keep `batch.no_cr_yet` alone (critic fix 5).

**The server's published API** (critic fix 6). The `factory` key that `board/state.py` drops is
named neither in `docs/server-api.md` nor in `board/api/protocol.json` (checked at this
specification: neither file has the word), so this CR changes neither and owes no
`just protocol-schema`. The Driver checks it again at the head: if the protocol's models change,
it runs `just protocol-schema` and updates `docs/server-api.md`. The new `backlog.move` target and
the items' `running_batch` key are the board's (`board-running-batch-lane`, Out of scope).

### 5. Docs

- **`README.md`:** the section "Factory mode" is replaced by a short section "Running batch or next
  batch" (anchor `#running-batch-or-next-batch`). It covers the choice at "grilled enough?" and at
  every spec-writer start, the default (the next batch), `1-pending` as the go, and the ordinary
  pause, retro and close.
- **`docs/use-cases.md`, `docs/use-cases-direct.md`, `docs/use-cases-foreman.md`:** the factory
  sentences become the same behaviour, and their three links `[Factory mode](../README.md#factory-mode)`
  (`docs/use-cases.md` line 43, `docs/use-cases-direct.md` line 75, `docs/use-cases-foreman.md`
  line 110) point to `../README.md#running-batch-or-next-batch` with the new section's name
  (critic fix 7).
- **`docs/batch-lifecycle-texts.md` and `docs/batch-lifecycle.svg`:**
  - Remove "a factory batch: no close offered;" and "a factory batch: `order factory off`,".
  - "or, in a factory batch, `triage --ready`" becomes "or `order add`, from the destination the
    user chose".
  - Keep the two files in step as the repository's checks require.
- **`scenario/README.md`:** the factory bullet (lines 247-251) is rewritten for the new steps
  (Evidence).
- **`docs/release-notes/2026-11-19-v0.14.0/`:** unchanged (history; its link is pinned to the
  `v0.14.0` tag).

## Out of scope

- **The board's lane** (factory-Q9): `board-running-batch-lane` (`1-inbox/board-running-batch-lane`,
  after this CR in its `depends.json`) holds the backlog page's last column split into "running
  batch" over "next batch", always shown; a drop on "running batch" that calls this CR's mark
  function (section 2); the server's `backlog.move` target and the items' `running_batch` key,
  with `docs/server-api.md` and `just protocol-schema` (critic fix 6); the Chief of Staff's reading
  of that drop's `board wrote` line; and the former open questions 1 to 3 (the drop and AGENTS.md's
  "never edits a batch", the drop of a CR already specified, the drop with no open batch). This CR
  ships the mark function and its CLI command only.
- **docs-sphinx-rtd** (`2-backlog/P3/docs-sphinx-rtd`): its specification names the README's
  "Factory mode" section and the `#factory-mode` anchor (its lines 60, 71, 130, 143-145, 165). It
  must follow the renamed section "Running batch or next batch" (critic fix 7); that CR's own
  specification is updated before it runs, not by this CR.
- drop-to-next-batch (`1-inbox/drop-to-next-batch`) and hold-live-cr (`1-inbox/hold-live-cr`),
  which depend on this CR: taking a CR out of the running batch (to `3-ready`, or held). park-live-cr
  (`1-inbox/park-live-cr`, no dependency): the parked `blocked` state and `close` refused with a
  blocked CR. Dragging a CR out of `1-pending` on the board: not now, an idea with no CR
  (park-live-Q14).
- The Kanban view, the home page's backlog block and the terminal client (`clients/tui/`): they
  keep reading `3-ready` as the next batch. The board's `grill_of` (`board/backlog.py`) keeps its
  words.
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
  - with an open batch and `work/specifying` in the folder, it writes `work/running-batch` with the
    batch id and moves nothing;
  - with neither `work/specifying` nor `03-change-spec.md`, it is refused (exit precondition,
    `grill it first`);
  - on a `3-ready` folder, it is refused (exit precondition, the message names `order add`) and
    writes no mark;
  - with no open batch, it is refused (exit precondition, the message names `triage --ready`);
  - `--ready`, `--priority`, `--inbox`, `abandon` and `order add` each clear the mark;
  - `order add` leaves no `work/running-batch` in `1-pending`;
  - a stale mark (another batch id) shows on `status`'s stale line.
- `status` prints the `running batch: ... marked, not joined` line with `specifying`/`written`.
- `open --factory` and `order factory on` are refused (exit usage).
- `open` with no CR is allowed, writes no `factory` key, and its brief has no `Factory:` token.
- `triage --ready` with an open batch joins nothing: the batch's CRs are unchanged.
- The last CR's end prints the ordinary `next: the retro ...` line, also for a batch opened with
  no CR.
- A prepared `batch.json` with `"factory": true` and a done `factory` order: `status` runs and
  prints no factory word, and `close` is not refused for that order.
- The board's shipped files: `js/model/semantics.js`, `js/views/batch.js` and
  `js/views/home-batch.js` contain no `steeringFactoryWord` and no `batch.no_cr_yet_factory`, and
  `js/i18n/en-batch.js` and `fr-batch.js` have neither `batch.factory_on` nor
  `batch.no_cr_yet_factory`.
- Update or remove the factory tests (critic fix 5):
  - `tests/test_factory.py`: deleted; the cases that still hold (a release CR joining, `status`
    and the files) move to the tests above or stay with the factory word removed;
  - `test_open_empty_batch.py`, lines 191-195 of
    `test_the_board_words_of_a_batch_with_no_cr_are_shipped`: assert that `'batch.no_cr_yet'`
    stays and that `'batch.no_cr_yet_factory'`, `'batch.factory_on'` and `steeringFactoryWord(`
    are gone; its other factory assertions too;
  - `test_batch_end.py::test_the_end_of_the_last_cr_of_a_factory_batch_waits_for_the_next_ready_cr`;
  - `test_came_back.py::test_triage_ready_of_a_moved_out_cr_joins_a_factory_batch_under_its_number`
    becomes `order add` of the moved-out CR getting its number back;
  - the factory assertions of `test_open_no_clone.py` and `test_opening_and_restore.py`;
  - `batch_helpers.py`'s factory helper (`open_factory`).
- The docs' links: the repository's link check reads `docs/use-cases*.md` and finds
  `#running-batch-or-next-batch` in `README.md`.

**Scenario** (`scenario/run_scenario.py`):

- `empty_batch` loses its factory checks. A batch opened with no CR is paused, with no `factory`
  key, no `Factory:` token and `no CR yet: \`order add ...\``.
- `factory_batch` (16e) is replaced by a step `running_batch`:
  1. A CR with `work/specifying` is marked with `triage --running-batch` while the batch is open;
     once its `03-change-spec.md` is written and the marker gone, `status` shows it `written`.
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
