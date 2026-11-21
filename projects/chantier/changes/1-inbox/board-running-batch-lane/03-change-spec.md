# Board backlog: last column split into running batch and next batch

On the board's backlog page (Triage), the last column is split horizontally, as Jira does:
"running batch" on top, "next batch" (`3-ready`, as today) below. Both halves are always shown, in
every mode. A drop on "running batch" writes only factory-redefine's running-batch mark
(`work/running-batch`), or, for a `3-ready` CR, only a journal line. The Chief of Staff, woken by
the watcher, adds the CR with `order add` once its specification is final, and writes the board's
destination into the CR's `02-answers.md`. The board still never edits a batch.

This CR sits on top of `factory-redefine` (`depends.json`: `{"after": ["factory-redefine"]}`). That
CR ships the mark:

- the lifecycle function behind `triage <folder> --running-batch`;
- the file `work/running-batch` (the time and the open batch's id);
- the mark's clearing by every other `triage`, by `abandon` and by `order add`;
- its stale reading;
- `status`'s `running batch:` line.

This CR calls that function and changes none of its rules.

## Goal, in the user's terms

The user's words (park-live-Q8): "dans la page backlog, il faut une division horizontale de la
dernière colonne (comme Jira) pour pouvoir dire soit dans le batch en cours ou dans le prochain
(met ça tout le temps, même en mode séries ou parallel)".

In English: on the backlog page, the last column is split horizontally (as in Jira), so the user
can say whether a CR goes in the running batch or in the next one. Both halves are always there,
in series and parallel mode too.

## Decisions carried (02-answers.md)

| Answer | Decision | Where it lands below |
| --- | --- | --- |
| running-lane-Q1 | A drop on "running batch" writes only the mark (`work/running-batch`), through factory-redefine's mark function. The Chief of Staff, woken by the watcher, adds the CR when its specification is final. The board never edits a batch. | 2, 4 |
| running-lane-Q2 | A CR whose specification is already final joins at the Chief of Staff's next wake (`order add`), with one line to the user, for example "CR-431 added to batch-30 from the board". | 2, 4 |
| running-lane-Q3 | With no open batch, the "running batch" half stays visible, greyed, and says "no running batch". A drop on it places the CR in `3-ready` and says so. | 1, 2 |
| running-lane-Q4 | The "running batch" half shows the marked CRs and the CRs in `1-pending`, each with its state. Running CRs stay on the batch page. | 1, 2 |
| running-lane-Q5 | Grilled enough. The spec-writer runs, then the critic. Destination: the next batch, with factory-redefine. | (this file) |
| running-lane-Q6 | A `3-ready` CR dropped on "running batch" leaves a journal line only. The Chief of Staff runs `order add` at its next wake, and the card moves then. | 1, 2, 4 |
| running-lane-Q7 | A marked CR is drawn once, in the "running batch" half only. It leaves its inbox or priority row. | 1 |
| running-lane-Q8 | A grilled CR whose spec-writer has not started is refused (factory-redefine's refusal kept), with a clear message on the board: "the grill is not finished". | 1, 2 |
| running-lane-Q9 | One clause in AGENTS.md names the `3-ready` drop's `board@1` line (action `running-batch`, no file written), which the Chief of Staff turns into `order add`. | 3 |
| running-lane-Q10 | The latest word wins. When it reads the board's line, the Chief of Staff writes the drop into `02-answers.md`: "Destination: running batch batch-30 (board, 14:02)", or "next batch (board)". | 4 |
| running-lane-Q11 | A marked CR whose specification is written has its own words, "spec written: joins soon". So there are three states: waiting for its spec, spec written, waiting for a slot. | 1 |
| running-lane-Q12 | A single post-it of a group dropped on "running batch" leaves its group, as any move out of the group's column does today. | 2 |
| running-lane-Q13 | Grilled enough. This revision, then the critic again. Destination: the next batch, with factory-redefine. | (this file) |
| running-lane-Q14 | A marked CR moved by the board back to the inbox or a priority row: the Chief of Staff, reading the board's line, writes `Destination: back to the backlog (board)` into `02-answers.md`; the last destination written stays true (Q10). | 4 |
| Spec critic run, fix 5 | The top half's sub-line has its own i18n key ("{batch} · {state}", both languages). The spec says whether `triage.running` and `triage.idle` are removed. | 1 |
| Spec critic run, fix 6 | `docs/web-board.md` line 163 ("writes in the backlog only ... never in a batch") names the mark among the backlog's writes. | 5 |
| Spec critic run, fix 7 | The scenario's no-open-batch step is dropped. The in-process test is named as its cover. | Evidence |
| Spec critic run 2, fix 1 | A drop of a marked CR on its folder's own column clears the mark, writes `<slug> → <column>; running-batch mark cleared`, and is tested. | 1, 2, Evidence |
| Spec critic run 2, fix 2 | The `3-ready` drop on "running batch" keeps the CR's group (it writes no file in the CR's folder). The AGENTS.md clause says it writes no file in the CR's folder and appends only its journal lines. | 1, 2, 3, Evidence |
| Spec critic run 2, fix 3 | `board_text` of a `move` line with `→ 3-ready` also ends "for the Chief of Staff: write its destination, act on nothing else"; the `running-batch` text adds "(at once for a CR in `3-ready`)"; a plain `→ 3-ready` line is tested. | 2, Evidence |
| Spec critic run 2, fix 4 | Section 4 also edits `griller.md` and chief-of-staff.md's final-spec paragraph: the destination acted on is the last `Destination:` line; a Griller whose CR carries a mark for the open batch sends `<slug> specified` and runs no `triage`. | 4 |
| Spec critic run 2, fix 5 | The mark's clearing lives in `lifecycle/backlog.py:move_item`, moved there if factory-redefine shipped it in the command. | 2 |
| Spec critic run 2, fix 6 | DESIGN.md's "One card, one column, one chip" rule gains a lane sentence; the comment at `js/ui/column.js` line 9 follows. | 1 |

## Words used here

- **Open batch:** a batch folder whose record is not `closed`, whether it is running or paused, as
  factory-redefine defines it (factory-Q5: a paused batch stays the running batch until the user's
  `close`).
- **Marked CR:** a backlog CR (inbox or `2-backlog/P1`..`P4`) whose `work/running-batch` names the
  open batch. A stale mark (another batch's id) counts as no mark, as in factory-redefine.
- **Pending CR:** a CR of the open batch in `4-batch/1-pending/`: the record's row with state
  `queued`.
- **Grilled, for the mark:** factory-redefine's test: the folder has `work/specifying` or
  `03-change-spec.md`.

## What changes

### 1. The web client: the last column split in two

Read `skills/chantier/scripts/cli/src/chantier/clients/web/DESIGN.md` first and keep it true
(AGENTS.md).

**Layout** (`js/views/triage.js`, `js/triage/columns.js`, `js/ui/column.js`,
`css/components/column.css`, `css/views/triage.css`).

- The page keeps its three columns: Inbox, Backlog (P1 to P4), and the last column, which today is
  `3-ready` alone. The last column becomes one column, built by `js/ui/column.js`, whose body holds
  two halves, one over the other:
  - top: "running batch";
  - bottom: "next batch".
- Each half is a part of the column, built by `js/ui/column.js` like the Backlog column's rows.
  Unlike a row, a half has a name in its head (the half's title), its count and its grill counts,
  and its own one-line grey sub-line.
  - `column.js` gains that variant (a lane with a name and a sub-line).
  - Its classes stay under the `column-*` prefix.
  - Its style lives in `css/components/column.css` only.
  - `css/views/triage.css` only places the halves (the bottom half is sized as today's column).
- Both halves are drawn always: in every mode (parallel, series, stack), with or without a batch,
  in Foreman and in direct mode (park-live-Q8).

**Top half, "running batch"** (running-lane-Q4, Q7, Q11).

- **What it holds:**
  - the marked CRs (from the items' `running_batch` key, section 2), as Triage post-its built by
    `js/triage/postit.js`, grouped as in any column when their group is marked whole;
  - the pending CRs (the record's rows with state `queued`, from `state.data.batch.crs`, as the
    Kanban already reads them in `js/model/columns.js`), as item cards (`js/ui/card.js`), not
    draggable and not selectable.
- **A marked CR is drawn once, in this half only** (running-lane-Q7). It is left out of its inbox
  or priority row while its mark names the open batch.
- A `3-ready` CR dropped here is not marked (section 2). It stays drawn in the bottom half until
  the Chief of Staff's `order add` places it in `1-pending`, and the card moves then
  (running-lane-Q6).
- **Its state words**, one per card, in the card's meta line, words only (no new colour, size or
  icon). There are three (running-lane-Q11):
  - a marked CR with `work/specifying`: "waiting for its spec";
  - a marked CR with `03-change-spec.md` and no `work/specifying`: "spec written: joins soon";
  - a pending CR: "waiting for a slot".
  The client reads the first two from the item's `grill` key (`specifying`, `specified`), which
  `board/backlog.py` already sends.
- CRs that are working, blocked, handed back or merged are not shown here: they stay on the batch
  page (running-lane-Q4).
- **Its head:** the title "Running batch", the count of the cards it holds and the grill counts of
  its marked post-its.
- **Its sub-line** (critic fix 5):
  - with an open batch: its own key, `triage.running_lane`, "{batch} · {state}" (for example
    `batch-30 · paused`), in both languages;
  - with no open batch (no batch folder, or the batch is `closed`; running-lane-Q3): its own key,
    `triage.no_running`, "no running batch".
- **With no open batch:**
  - the half stays in place, greyed (a `column-*` variant of `css/components/column.css`, drawn
    from existing tokens only; DESIGN.md's token table changes only if a token is added);
  - its body has no card;
  - it stays a drop target (section 2).

**Bottom half, "next batch" (`3-ready`).**

- This is today's `3-ready` column, with the title "Next batch".
- Its sub-line stays `kanban.ready_sub` ("waits for the next batch").
- Its counts, its "The next batch is ready" button (`next-batch.json`, `js/triage/ready.js`) and its
  foot stay as today, with one change: the foot loses its running-batch line. `readyFoot` in
  `js/triage/columns.js` no longer reads `ctx.batch`.
- **`triage.running` and `triage.idle` are removed** (critic fix 5), from `en-write.js` and
  `fr-write.js`, with their one use in `js/triage/columns.js`. The top half's two new keys replace
  them.
- `3-ready` post-its are drawn here as today.

**Drops and the selection bar** (`js/triage/drag.js`, `js/triage/move.js`,
`js/triage/selection.js`, `js/model/triage.js`, `js/api/backlog.js`).

- The top half is a drop target named `running-batch` (`data-col="running-batch"`). Dropping a
  post-it or a group's handle on it calls `backlog.move` with `to: "running-batch"` (section 2).
  - A single post-it of a group dropped there leaves its group, as a move out of the group's column
    does today (running-lane-Q12). The server does it, as for a lone post-it today (section 2).
    One exception: a `3-ready` post-it dropped there keeps its group, since that drop writes no
    file in the CR's folder (critic run 2, fix 2).
  - A group dragged by its handle stays a group, as today's whole-group moves do.
- Dropping a marked post-it on the bottom half, on the inbox or on a priority row calls
  `backlog.move` with that column, as today. The server's move clears the mark (factory-redefine:
  every other `triage` of the folder clears it). This includes the row its folder is in (its own
  column): the drop clears the mark and moves no folder (critic run 2, fix 1; section 2).
- A pending CR's card is not draggable and not selectable. Taking a CR out of the batch belongs to
  park-live-cr.
- The selection bar offers one more target, "→ Running batch" (`data-to="running-batch"`), next to
  the inbox, P1 to P4 and `3-ready`.
- `columnOf` treats a marked CR as being in `running-batch`, so `moveTo` sends nothing for a CR
  already marked for the open batch, and does send a move to the row its folder is in (which
  clears the mark). That is the same rule as a drop on an item's own column today.
- **Refusals** show as today's move refusals do (`js/triage/actions.js`, the toast with the
  server's `error`), and the post-it stays where it was. A grilled CR whose spec-writer has not
  started gets the server's message (section 2): `<slug>: the grill is not finished: finish it,
  then drop it here again` (running-lane-Q8).
- **What the user sees after a drop:**
  - a drop with no open batch shows the server's line, `<slug> → 3-ready (no running batch)`, the
    way the client already shows a successful write's `lines`;
  - a `3-ready` drop shows `<slug>: the Chief of Staff adds it to <batch>`;
  - a marked CR moves to the top half at the next state push.

**Words** (`js/i18n/en-write.js` and `fr-write.js`, which hold `triage.*` today; every key in both
languages, DESIGN.md "Words"):

- the top half's title: "Running batch" / "Batch en cours";
- the bottom half's title: "Next batch" / "Prochain batch";
- `triage.running_lane`: "{batch} · {state}" in both;
- `triage.no_running`: "no running batch" / "aucun batch en cours";
- the three state words:
  - "waiting for its spec" / "attend sa spec";
  - "spec written: joins soon" / "spec écrite : arrive bientôt";
  - "waiting for a slot" / "attend un slot";
- the selection bar's target: "→ Running batch" / "→ Batch en cours";
- `triage.running` and `triage.idle` removed;
- `kanban.ready_sub` stays.

The server's lines and refusals are shown as they come, as today.

**DESIGN.md.**

- Add a short section, "The last column of Triage", that says the following:
  - the last column holds two halves, "running batch" over "next batch", always drawn;
  - each half is a named lane of `js/ui/column.js`, with its head and its sub-line;
  - the top half is greyed with "no running batch" when no batch is open;
  - a marked CR is drawn there only;
  - pending CRs are plain cards there, neither draggable nor selectable;
  - the three state words are words only, with no new colour, size or icon.
- In the rule "**One card, one column, one chip.**", add one lane sentence after the column's
  (critic run 2, fix 6): "A lane, built by the same module (`lane(parts)`), sits in a column's body
  and has no dot: a Backlog lane's head is its priority chip, its count and its grill counts;
  Triage's last column holds two named lanes, "Running batch" over "Next batch", each with its
  name, count, grill counts and own grey sub-line."
- The comment at the top of `js/ui/column.js` (line 9, "A lane has no dot and no name: its head is
  `chip` ..., `count` and `states`.") follows: a lane has no dot; a Backlog lane's head is `chip`,
  `count` and `states`; a named lane (Triage's last column) has `name`, `count`, `states` and its
  own `sub`.
- Keep the Components table true if a class prefix or a builder changes (it should not: still
  `column`, `column-*`, `js/ui/column.js`).

### 2. The server: the `running-batch` target and the items' key

**`board/write_api.py`.**

- `COLUMNS` gains `"running-batch"`. `_move` accepts it as `to`. The refusal for any other value
  names it: `'to' is one of inbox, P1, P2, P3, P4, 3-ready, running-batch`.
- `_move_one` with `to == "running-batch"`. The folder is found with `backlog.backlog_folder` (the
  backlog only, as today). Then, by case:
  - **An open batch, folder in the inbox or `2-backlog/P1`..`P4`, grilled:**
    - it calls factory-redefine's mark function, the same one `triage <folder> --running-batch`
      runs. The function writes `work/running-batch` and moves no folder;
    - the words are `<slug> → running batch <batch> (marked)`;
    - a folder whose mark already names the open batch writes nothing (`[]`, `""`), as a drop on
      its own column does.
  - **An open batch, folder in the inbox or a priority row, not grilled** (running-lane-Q8):
    - the server checks the folder with factory-redefine's own test (neither `work/specifying` nor
      `03-change-spec.md`) before calling the mark function;
    - it refuses with 409 and the message `<slug>: the grill is not finished: finish it, then drop
      it here again`, and writes nothing;
    - the mark function's own refusal (`grill it first`) stays unchanged for the CLI and remains
      the backstop.
  - **An open batch, folder in `3-ready`** (running-lane-Q2, Q6):
    - factory-redefine refuses the mark on a `3-ready` folder (factory-Q12: a `3-ready` CR is never
      marked), so the board does not call it;
    - it writes no file in the folder and moves no folder;
    - its `board@1` line is the user's word. The words are
      `<slug> → running batch <batch> (in 3-ready: order add)`;
    - the line it returns is `<slug>: the Chief of Staff adds it to <batch>`.
  - **No open batch** (running-lane-Q3):
    - it moves the folder to `3-ready` with `backlog.move_item(repo, <rel>, "3-ready")`, as a drop
      on `3-ready` does today, which clears a mark too;
    - the line it returns is `<slug> → 3-ready (no running batch)`, and so are its words;
    - a folder already in `3-ready` writes nothing.
- **Groups** (running-lane-Q12). With `alone` (a single post-it, not a group's drag), a written
  `running-batch` write takes the item out of its group with `change_group(repo, [target], None)`,
  as `_move_one` does today after a move. This holds for the mark and the no-batch move. The
  `3-ready` journal-only case keeps the group: it writes no file in the CR's folder, so not its
  `summary.json` either (critic run 2, fix 2). A group dragged whole keeps its group.
- **A marked CR dropped on its own column** (critic run 2, fix 1). Today `_move_one` returns at
  once when `before == to` (`write_api.py` line 137, "a drop on the item's own column writes
  nothing"). That early return now holds only for a folder with no mark naming the open batch. A
  marked CR dropped on the column its folder is in (the inbox or its priority row) goes to
  `backlog.move_item`, which clears the mark and moves no folder; the words are
  `<slug> → <column>; running-batch mark cleared`, and the `board@1` line is a `move` line. A
  stale mark (another batch's id) counts as no mark here, as everywhere: that drop writes nothing.
- **Where the clearing lives** (critic run 2, fix 5). The mark's clearing lives in
  `lifecycle/backlog.py:move_item`, so the CLI's `triage` and the board share one rule. If
  factory-redefine shipped it in the `triage` command instead, this CR moves it into `move_item`,
  with its behaviour unchanged. `move_item` removes `work/running-batch` from the folder on every
  move. For a folder already in `to` that carries a mark, it removes the mark and moves no folder
  (`move_backlog_item` would refuse with `already holds`, so `move_item` does not call it then);
  for a folder already in `to` with no mark, it keeps today's refusal. The CLI follows: `triage
  <folder> --priority P2` on a marked CR already in `P2` clears the mark and moves nothing.
- **The words of a move that clears a mark.** A move of a marked CR to `3-ready`, the inbox or a
  priority row, its own column included, says so in its words: today's words, then
  `; running-batch mark cleared`. Example: `<slug> → 3-ready (specified); running-batch mark
  cleared`. The Chief of Staff reads it (section 4).
- **The journal action.**
  - A write in one of the two open-batch cases that writes (the mark, or the `3-ready` line)
    appends its `board@1` line with the action `running-batch`, not `move`.
  - The no-open-batch case is an ordinary `move` line.
  - A move with several items, some of them refused, keeps today's rule: refusals are listed, and
    the written ones make one line.
  - `_move` therefore passes `"running-batch"` as `kind` to `_answer` when `to == "running-batch"`
    and a batch is open, and `"move"` otherwise.
- **No batch file is touched.** The board writes only:
  - the backlog folder's `work/running-batch`, which is a file in a backlog CR's folder, inside
    AGENTS.md's "edits the backlog (... files and folder moves)";
  - the group change, in the CR's `summary.json` as today (never for the `3-ready` journal-only
    case);
  - its own journal line and the `board@1` line.

  AGENTS.md's "it never edits a batch" holds. The one AGENTS.md change is section 3's clause.

**`hub/journal.py` and `hub/schemas.py`.**

- `WAKING_ACTIONS` gains `"running-batch"`, so the line wakes the Chief of Staff's watcher.
- `board_text` keeps its sentence for every action except `running-batch`. For `running-batch` it
  says `board wrote (running-batch): <text>; for the Chief of Staff: the user's go for the running
  batch: write its destination, then \`order add --note <folder>\` once its specification is
  final (at once for a CR in \`3-ready\`)`.
- `board_text` of a `move` line whose text says `running-batch mark cleared`, or whose text has
  `→ 3-ready` (a plain move to `3-ready`, the no-open-batch drop included), ends instead with
  `for the Chief of Staff: write its destination, act on nothing else` (critic run 2, fix 3).
- `board@1`'s model does not change: `action` is an open string (the module docstring says so).
  `schemas.json` and `just journal-schemas` are not touched. If `tests/test_event_types.py` fails
  at the head, the model changed, and that is a defect, not a new entry.

**`board/backlog.py`.**

- Each backlog item carries `running_batch`: the open batch's id when the item's
  `work/running-batch` names it, else `null`. A stale mark, or no open batch, gives `null`.
- The value is read with factory-redefine's reading of the mark, through the store (`PlanStore`),
  like the item's other fields. `backlog_items` gets the open batch's id from its caller
  (`board/state.py`), which already reads the batch.
- `grill_of` keeps its words (factory-redefine's Out of scope).

**`board/state.py`.** Nothing else changes: the pending CRs are the batch's rows the state already
carries (`batch.crs`, state `queued`).

**The server's published API.**

- `board/api/protocol.py`: `MoveArgs.to` stays a `str` (the target is checked by `write_api.py`).
  - If the Driver changes the model (for example to an enumeration), it runs
    `just protocol-schema` and commits `board/api/protocol.json`. Otherwise `protocol.json` does
    not change.
  - Either way, the Driver checks that the file at the head is the recipe's output.
- `docs/server-api.md`:
  - the `backlog.move` row (line 86) says: `the items moved to \`to\` (the inbox, a priority,
    \`3-ready\`), or \`running-batch\`: marked for the open batch, or, from \`3-ready\`, a journal
    line only; with no open batch, moved to \`3-ready\``;
  - the paragraph on backlog writes (line 99) adds that a `running-batch` write appends a
    `board@1` line with the action `running-batch`;
  - a backlog item's keys get `running_batch` (the open batch's id, or `null`). If the document
    lists no item keys, one sentence after the `backlog.move` table says so.

### 3. AGENTS.md and the CLI's other surfaces

**AGENTS.md** (running-lane-Q9). The board bullet's sentence "and each write it makes to the
backlog also appends one `board@1` line to that project's `forge-journal.jsonl`, which the Chief of
Staff's watcher reads" gains one clause:

- "; a drop of a `3-ready` CR on the running batch writes no file in the CR's folder and appends
  only its journal lines (its `board@1` line, action `running-batch`, which the Chief of Staff
  turns into `order add`)".

Nothing else in AGENTS.md changes. The `work/running-batch` mark is a backlog file, so it is
already inside "edits the backlog (... files and folder moves)".

**The CLI.**

- No new command and no new flag. The board calls factory-redefine's function in-process, as it
  calls `move_item` today.
- `status` is unchanged: factory-redefine's `running batch: <n> CRs marked, not joined` line
  already names the CRs the board marked.

### 4. The Chief of Staff on the board's line (cards)

**`skills/chantier/references/chief-of-staff.md`**, in "*A watcher's end:*", next to the sentence
"A `board wrote (...)` line ... no tool call, no action", and the same in "*The pull path:*".

- **The destination, latest word first** (running-lane-Q10). When it reads a board line that sets a
  CR's destination, the Chief of Staff writes it into the CR's `02-answers.md` at once. The latest
  word wins over a destination already recorded there, from the grill or from an earlier board
  line. The forms:
  - a `board wrote (running-batch): ...` line: `Destination: running batch <batch> (board,
    <HH:MM>)`, where the time is the line's own time `t`, in the user's local time;
  - a `board wrote (move): ...` line that moves a CR to `3-ready` (`→ 3-ready`, with or without
    `running-batch mark cleared`, including the no-open-batch drop): `Destination: next batch
    (board)`;
  - a `board wrote (move): ...` line that moves a marked CR to the inbox or a priority row (its
    words end with `running-batch mark cleared`, running-lane-Q14): `Destination: back to the
    backlog (board)`.

  It writes a destination only in a folder that has a `02-answers.md`, and creates none.
- **A `board wrote (running-batch): ...` line** is the user's destination for the running batch,
  and for the running batch it is also the go (factory-Q2). After writing the destination, the
  Chief of Staff:
  - reads the CR's folder (named in the line);
  - **if the CR is in `3-ready`** (a journal-only line, running-lane-Q6), **or its specification
    is final** as factory-redefine defines it (`03-change-spec.md` written, no `work/specifying`,
    its critic run and applied when due, no open question left):
    - runs `$CHANTIER order add --note <folder>` with no further question;
    - handles the order as usual: in Foreman mode it sends the order's line to the Foreman; in
      direct mode it takes the CR when a slot frees;
    - then tells the user in one line: `<CR-id> added to <batch> from the board`
      (running-lane-Q2);
  - **otherwise**:
    - one line to the user: `<slug> marked for <batch> from the board: it joins once its
      specification is final`;
    - when the specification becomes final, factory-redefine's rule applies:
      `order add --note <folder>`;
    - `status`'s `running batch:` line keeps the CR in view meanwhile;
  - **`order add` refused**: factory-redefine's rules (factory-Q13) apply unchanged.
- The other `board wrote` lines keep "one line, no tool call, no action", except the destination
  write above.

**The final-spec paragraph of `chief-of-staff.md`** (critic run 2, fix 4): factory-redefine's
paragraph "That answer is the user's word for the move ... Then: Next batch ... Running batch ...".
It gains one sentence: the destination acted on is the last `Destination:` line of the CR's
`02-answers.md`, whether the grill wrote it or a board line did (running-lane-Q10, Q14). So:

- `Destination: next batch ...`: `triage <folder> --ready`, as factory-redefine says;
- `Destination: running batch <batch> ...`: `order add --note <folder>`, as factory-redefine says;
- `Destination: back to the backlog (board)`: no `triage` and no `order`; the CR stays in its
  inbox or priority row (the user's move put it there).

**`skills/chantier/references/griller.md`**, section "Telling the Chief of Staff" (critic run 2,
fix 4), on top of factory-redefine's version of it:

- The destination the Griller acts on is the last `Destination:` line of `02-answers.md`, as for
  the Chief of Staff above.
- A Griller whose CR carries a mark for the open batch (`work/running-batch` naming it, written by
  the grill's `triage --running-batch` or by a board drop) sends `[griller→chief-of-staff] <slug>
  specified` once the specification is final and runs no `triage`, even when its grill recorded
  the next batch.

**The "rescan" row** (line 48) adds: "a `running-batch` write, a move to `3-ready`, or a move that
clears a running-batch mark: act as at a watcher's end". This covers a Chief of Staff whose watcher and pull path both did not run.

No agent file changes (the cards hold the contract; AGENTS.md).

### 5. Docs

- **`docs/web-board.md`, "Triage":**
  - The first bullet becomes: drag a post-it between **Inbox**, a priority, **Running batch** and
    **Next batch** (`3-ready`).
  - A new bullet says what the last column's two halves are:
    - "Running batch" is always shown;
    - it holds the CRs marked for the open batch ("waiting for its spec", "spec written: joins
      soon") and those in `1-pending` ("waiting for a slot");
    - a drop there writes only the mark, or a journal line for a `3-ready` CR, and the Chief of
      Staff adds the CR once its specification is final;
    - a CR whose grill is not finished is refused;
    - with no open batch it is greyed and a drop goes to `3-ready`.
  - The paragraph "Each change is written at once ..." keeps "a running batch's CRs are never
    written", and names the mark among the backlog's writes.
  - The Triage screenshots (`docs/web-board/triage-pc.png`, and the phone ones that show Triage)
    are retaken with `just docs-screenshots` (by hand, as the recipe says). If the Driver cannot
    run it, the PR's Known gaps names it.
- **`docs/web-board.md`, line 163** (critic fix 6): "It writes in the backlog only (the inbox, the
  priorities, `3-ready`), never in a batch: file an idea, move items between those places, ..."
  names the mark. It becomes "..., move items between those places or mark one for the running
  batch (`work/running-batch`, in the CR's own folder), ...". "never in a batch" stays.
- **`docs/planning-folder.md`:** the `board@1` row (line 142) names `running-batch` among the
  waking actions (`new`, `move`, `edit`, `running-batch`).
- **`README.md`:** factory-redefine's section "Running batch or next batch" gets one sentence: on
  the board, the backlog page's last column holds the same choice.

## Out of scope

- Everything factory-redefine ships:
  - the mark function, `triage --running-batch` and its refusals;
  - the mark's clearing and the stale mark;
  - `status`'s `running batch:` line;
  - the grill's four options and the destination at each spec-writer start;
  - the factory mode's removal.
- park-live-cr: taking a CR out of the running batch, dragging a CR out of `1-pending`, the
  `blocked` state.
- The Kanban view, the Home page's backlog block and the terminal client (`clients/tui/`): they
  keep reading `3-ready` as the next batch (factory-redefine's Out of scope).
- The CR board pane (`hooks/register.tsx`) and `STATUS.json`: not touched, so no pane screenshot
  and no `just mod`.

## Evidence

Every check reads the shipped files at the head under test: the web client's files, the cards,
AGENTS.md and the docs, read from the repository. The server's answers come from real states built
by the CLI's commands (`file`, `triage`, `open`, `order add`, and factory-redefine's
`triage --running-batch`). No prepared text stands in for a shipped file.

**Tests** (`skills/chantier/scripts/cli/tests/`, in-process, few and parametrized; `just test`
within its limit). Extend `test_triage_moves.py` or `test_board.py` (the write routes) and
`test_board_journal.py`.

- `backlog.move` with `to: "running-batch"`, one parametrized test over these states:
  - an open batch and an inbox CR with `work/specifying`:
    - it writes `work/running-batch` naming the batch and moves no folder;
    - it answers 200;
    - it appends one `board@1` line with the action `running-batch` and `wakes: true`;
  - the same CR dropped again: nothing written, no journal line;
  - an open batch and a CR with `02-answers.md` but neither `work/specifying` nor
    `03-change-spec.md`: 409 with `the grill is not finished`, and nothing written;
  - an open batch and a `3-ready` CR:
    - it answers 200, writes no file and leaves the folder in `3-ready`;
    - it appends one `board@1` line with the action `running-batch`, whose text names
      `order add`;
  - no open batch, and the same for a closed batch: the folder moved to `3-ready`, the line
    `<slug> → 3-ready (no running batch)`, and a `board@1` line with the action `move`. This is
    the cover for the no-open-batch drop (critic fix 7);
  - a paused batch counts as open: the mark is written;
  - a single grouped CR dropped (`items` of one): marked and out of its group. A `group` move keeps
    the group on every member;
  - a single grouped `3-ready` CR dropped (`items` of one): journal line only, and it keeps its
    group (critic run 2, fix 2).
- A marked CR moved by `backlog.move` to `3-ready`, to the inbox or to `P2`:
  - no `work/running-batch` is left;
  - the words end with `running-batch mark cleared`.
- A marked CR in `P2` moved by `backlog.move` to `P2` (its own column; critic run 2, fix 1):
  - no `work/running-batch` is left and the folder stays in `P2`;
  - the words are `<slug> → P2; running-batch mark cleared`, and one `board@1` `move` line is
    appended;
  - the same with a stale mark: nothing written, no journal line.
- `triage <folder> --priority P2` on a marked CR already in `P2` clears the mark and moves nothing
  (the clearing lives in `move_item`; fix 5).
- `'to'` with an unknown value: 400, and the message lists `running-batch`.
- `board/backlog.py`: an item's `running_batch` is the open batch's id when marked, and `null`
  when not marked, when the mark is stale, and with no open batch.
- `board_text`:
  - a `running-batch` line names `order add --note` and the destination;
  - a `running-batch` line says `at once for a CR in \`3-ready\``;
  - a `move` line with `running-batch mark cleared` names the destination;
  - a plain `move` line with `→ 3-ready` (for example `<slug> → 3-ready (specified)`) ends with
    `write its destination, act on nothing else` (critic run 2, fix 3);
  - any other line keeps "act on nothing".
- The shipped files, read from the repository:
  - `js/triage/columns.js` builds a drop target `running-batch` and no longer calls
    `triage.running` or `triage.idle`;
  - `js/triage/selection.js` offers `data-to="running-batch"`;
  - `en-write.js` and `fr-write.js` both have `triage.running_lane`, `triage.no_running` and the
    three state words, and neither has `triage.running` nor `triage.idle`;
  - `AGENTS.md` names the `board@1` line with the action `running-batch` and says the drop
    writes no file in the CR's folder;
  - `griller.md` and `chief-of-staff.md` name the last `Destination:` line.
- `tests/test_board_design.py` passes: DESIGN.md's token table and `tokens.css` agree, and the
  component rules hold for the new column variant.
- `tests/test_event_types.py` passes unchanged (no `board@1` model change).

**Scenario** (`scenario/run_scenario.py`, `board_writes`, beside its `backlog.move` checks; the
scenario's batch is open there):

1. A backlog CR carrying `work/specifying` is moved with `to: "running-batch"` over the protocol.
   Then:
   - `work/running-batch` exists and names the batch;
   - `project.state` shows the item with `running_batch: <batch>`;
   - `forge-journal.jsonl` gains one `board@1` line with the action `running-batch`;
   - `status` lists the CR on its `running batch:` line.
2. A grilled CR whose spec-writer has not started, moved the same way, is refused (409, `the grill
   is not finished`) and writes nothing.
3. The marked CR moved back to `P2`: its mark is gone.

The no-open-batch drop has no scenario step (critic fix 7): `board_writes` runs while the
scenario's batch is open. Its cover is the in-process test above (no open batch, and a closed
batch). `scenario/README.md` lists the new checks.

**Gates.**

- `just check` in the worktree.
- `just eval-dry-run` (the change is under the CLI's `src/`).
- The pipeline's `just scenario (ubuntu-latest)` job green at the PR's head (the CLI, the cards
  and the scenario change).
- Windows coverage by `chantier gate`, per AGENTS.md, when this CR is on top of its batch's stack.
- The PR's Deliverables hold two screenshots of the Triage page with the split column, from the
  PR's head: one with an open batch, one greyed with none. They are taken from a board served by
  the head (`just docs-screenshots` or by hand).

**No host and default matrix:** the behaviour does not depend on the host or on a configured value.

## Open questions

None.
