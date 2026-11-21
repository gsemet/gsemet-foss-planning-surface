# Board backlog: last column split into running batch and next batch

On the board's backlog page (Triage), the last column is split horizontally, as Jira does:
"running batch" on top, "next batch" (`3-ready`, as today) below. Both halves are always shown, in
every mode. A drop on "running batch" writes only factory-redefine's running-batch mark
(`work/running-batch`). The Chief of Staff, woken by the watcher, adds the CR with `order add`
once its specification is final. The board still never edits a batch.

This CR sits on top of `factory-redefine` (`depends.json`: `{"after": ["factory-redefine"]}`). That
CR ships the mark: the lifecycle function behind `triage <folder> --running-batch`, the file
`work/running-batch` (the time and the open batch's id), its clearing by every other `triage`, by
`abandon` and by `order add`, its stale reading, and `status`'s `running batch:` line. This CR calls
that function and changes none of its rules.

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
| running-lane-Q1 | A drop on "running batch" writes only the mark (`work/running-batch`), through factory-redefine's mark function. The Chief of Staff, woken by the watcher, adds the CR when its specification is final. The board never edits a batch. | 2, 3, 4 |
| running-lane-Q2 | A CR whose specification is already final joins at the Chief of Staff's next wake (`order add`), with one line to the user, for example "CR-431 added to batch-30 from the board". | 2, 4; open question 1 |
| running-lane-Q3 | With no open batch, the "running batch" half stays visible, greyed, and says "no running batch". A drop on it places the CR in `3-ready` and says so. | 1, 2 |
| running-lane-Q4 | The "running batch" half shows the marked CRs and the CRs in `1-pending`, each with its state ("waiting for its spec", "waiting for a slot"). Running CRs stay on the batch page. | 1, 2 |
| running-lane-Q5 | Grilled enough. The spec-writer runs, then the critic. Destination: the next batch (`3-ready`), with factory-redefine, this CR on top of it. | (this file) |

## Words used here

- **Open batch:** a batch folder whose record is not `closed`, whether it is running or paused, as
  factory-redefine defines it (factory-Q5: a paused batch stays the running batch until the user's
  `close`).
- **Marked CR:** a backlog CR (inbox or `2-backlog/P1`..`P4`) whose `work/running-batch` names the
  open batch. A stale mark (another batch's id) counts as no mark, as in factory-redefine.
- **Pending CR:** a CR of the open batch in `4-batch/1-pending/`: the record's row with state
  `queued`.

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
  - `css/views/triage.css` only places the halves (the bottom half's size as today's column).
- Both halves are drawn always: in every mode (parallel, series, stack), with or without a batch,
  in Foreman and in direct mode (park-live-Q8).

**Top half, "running batch"** (running-lane-Q4).

- **What it holds:**
  - the marked CRs (from the items' `running_batch` key, section 2), as Triage post-its built by
    `js/triage/postit.js`;
  - the pending CRs (the record's rows with state `queued`, from `state.data.batch.crs`, as the
    Kanban already reads them in `js/model/columns.js`), as item cards (`js/ui/card.js`), not
    draggable and not selectable.
- **Its state words**, one per card, in the card's meta line, words only (no new colour, size or
  icon):
  - a marked CR: "waiting for its spec";
  - a pending CR: "waiting for a slot".
- CRs that are working, blocked, handed back or merged are not shown here: they stay on the batch
  page (running-lane-Q4).
- **A marked CR is drawn once, in this half only.** It is left out of its own column (inbox or its
  priority row) while its mark names the open batch. See open question 2.
- **Its head:** the title "Running batch", the count of the cards it holds and the grill counts of
  its marked post-its.
- **Its sub-line:** with an open batch, the batch's id and state. Today's `triage.running` line
  moves here from the foot of `3-ready`.
- **With no open batch** (no batch folder, or the batch is `closed`; running-lane-Q3):
  - the half stays in place, greyed (a `column-*` variant of `css/components/column.css`, drawn
    from existing tokens only; DESIGN.md's token table changes only if a token is added);
  - its sub-line reads "no running batch";
  - its body has no card;
  - it stays a drop target (section 2).

**Bottom half, "next batch" (`3-ready`).**

- This is today's `3-ready` column, with the title "Next batch".
- Its sub-line stays `kanban.ready_sub` ("waits for the next batch").
- Its counts, its "The next batch is ready" button (`next-batch.json`, `js/triage/ready.js`) and its
  foot stay as today. The one change: the foot's running-batch line (`triage.running` /
  `triage.idle`) moves to the top half's sub-line.
- `3-ready` post-its are drawn here as today.

**Drops and the selection bar** (`js/triage/drag.js`, `js/triage/move.js`,
`js/triage/selection.js`, `js/model/triage.js`, `js/api/backlog.js`).

- The top half is a drop target named `running-batch` (`data-col="running-batch"`). Dropping a
  post-it or a group's handle on it calls `backlog.move` with `to: "running-batch"` (section 2).
- Dropping a marked post-it on the bottom half, on the inbox or on a priority row calls
  `backlog.move` with that column, as today. The server's move clears the mark (factory-redefine:
  every other `triage` of the folder clears it).
- A pending CR's card is not draggable and not selectable. Taking a CR out of the batch belongs to
  park-live-cr.
- The selection bar offers one more target, "→ Running batch" (`data-to="running-batch"`), next to
  the inbox, P1 to P4 and `3-ready`.
- `columnOf` and `moveTo` treat `running-batch` as a column. A post-it already marked for the open
  batch, dropped on the top half again, writes nothing, the same rule as a drop on an item's own
  column today.
- **Refusals** show as today's move refusals do (`js/triage/actions.js`, the toast with the
  server's `error`), and the post-it stays where it was. Example: an ungrilled CR is refused with
  factory-redefine's message, `<slug> is not grilled: grill it first`.
- **What the user sees after a drop:**
  - a drop with no open batch shows the server's line, `<slug> → 3-ready (no running batch)`, the
    way the client already shows a successful write's `lines`;
  - a marked CR moves to the top half at the next state push.

**Words** (`js/i18n/en-write.js` and `fr-write.js`, or the file that holds `triage.*` today; every
key in both languages, DESIGN.md "Words"):

- the top half's title: "Running batch" / "Batch en cours";
- the bottom half's title: "Next batch" / "Prochain batch";
- the top half's empty sub-line: "no running batch" / "aucun batch en cours";
- the two state words: "waiting for its spec" / "attend sa spec" and "waiting for a slot" /
  "attend un slot";
- the selection bar's target: "→ Running batch" / "→ Batch en cours";
- `kanban.ready_sub` stays.

**DESIGN.md.**

- Add a short section, "The last column of Triage", that says the following:
  - the last column holds two halves, "running batch" over "next batch", always drawn;
  - each half is a named lane of `js/ui/column.js`, with its head and its sub-line;
  - the top half is greyed with "no running batch" when no batch is open;
  - pending CRs are plain cards there, neither draggable nor selectable;
  - the state words are words only, with no new colour, size or icon.
- In the rule "**One card, one column, one chip.**", extend the lane sentence: "A lane has no dot
  and no name", except Triage's two named halves.
- Keep the Components table true if a class prefix or a builder changes (it should not: still
  `column`, `column-*`, `js/ui/column.js`).

### 2. The server: the `running-batch` target and the items' key

**`board/write_api.py`.**

- `COLUMNS` gains `"running-batch"`. `_move` accepts it as `to`. The refusal for any other value
  names it: `'to' is one of inbox, P1, P2, P3, P4, 3-ready, running-batch`.
- `_move_one` with `to == "running-batch"`. The folder is found with `backlog.backlog_folder` (the
  backlog only, as today). Then, by case:
  - **An open batch, folder in the inbox or `2-backlog/P1`..`P4`:**
    - calls factory-redefine's mark function, the same one `triage <folder> --running-batch` runs.
      It writes `work/running-batch` and moves no folder;
    - its refusals pass through unchanged, with their status (`grill it first` → 409);
    - the words are `<slug> → running batch <batch> (marked)`;
    - a folder whose mark already names the open batch writes nothing (`[]`, `""`), as a drop on
      its own column does.
  - **An open batch, folder in `3-ready`** (running-lane-Q2):
    - factory-redefine refuses the mark on a `3-ready` folder (factory-Q12: a `3-ready` CR is never
      marked), so the board does not call it;
    - it writes no file and moves no folder;
    - the write's journal line is the user's word: the words are
      `<slug> → running batch <batch> (in 3-ready: order add)`;
    - see open question 1.
  - **No open batch** (running-lane-Q3):
    - it moves the folder to `3-ready` with `backlog.move_item(repo, <rel>, "3-ready")`, as a drop
      on `3-ready` does today, and clears the mark the same way;
    - the line it returns is `<slug> → 3-ready (no running batch)`, and so are its words;
    - a folder already in `3-ready` writes nothing.
- **The journal action.**
  - A write whose words go to the running batch (the two open-batch cases) appends its `board@1`
    line with the action `running-batch`, not `move`.
  - A move with several items, some of them refused, keeps today's rule: refusals are listed, and
    the written ones make one line.
  - The no-open-batch case is an ordinary `move` line.
  - `_move` therefore passes `"running-batch"` as `kind` to `_answer` when `to == "running-batch"`
    and an open batch exists, and `"move"` otherwise.
- **No batch file is touched.** The board writes only the backlog folder's `work/running-batch` (a
  file in a backlog CR's folder, inside AGENTS.md's "edits the backlog (... files and folder
  moves)"), its own journal line and the `board@1` line. AGENTS.md's "it never edits a batch" holds
  and AGENTS.md does not change (running-lane-Q1).

**`hub/journal.py` and `hub/schemas.py`.**

- `WAKING_ACTIONS` gains `"running-batch"`, so the line wakes the Chief of Staff's watcher.
- `board_text` keeps its sentence for every action but `running-batch`. For `running-batch` it says
  `board wrote (running-batch): <text>; for the Chief of Staff: the user's go for the running batch:
  \`order add --note <folder>\` once its specification is final`.
- `board@1`'s model does not change: `action` is an open string (the module docstring says so).
  `schemas.json` and `just journal-schemas` are not touched. The Driver checks it at the head: if
  `tests/test_event_types.py` fails, the model changed and that is a defect, not a new entry.

**`board/backlog.py`.**

- Each backlog item carries `running_batch`: the open batch's id when the item's
  `work/running-batch` names it, else `null`. A stale mark, or no open batch, gives `null`.
- The value is read with factory-redefine's reading of the mark, through the store (`PlanStore`),
  like the item's other fields. `backlog_items` gets the open batch's id from its caller
  (`board/state.py`), which already reads the batch.
- `grill_of` keeps its words (factory-redefine's Out of scope).

**`board/state.py`.** Nothing else: the pending CRs are the batch's rows the state already carries
(`batch.crs`, state `queued`).

**The server's published API.**

- `board/api/protocol.py`: `MoveArgs.to` stays a `str` (the target is checked by `write_api.py`).
  If the Driver changes the model (for example to an enumeration), it runs `just protocol-schema`
  and commits `board/api/protocol.json`. Otherwise `protocol.json` does not change. The Driver
  checks that the file at the head is the recipe's output either way.
- `docs/server-api.md`:
  - the `backlog.move` row (line 86) says `the items moved to \`to\` (the inbox, a priority,
    \`3-ready\`), or \`running-batch\`: marked for the open batch, or noted for it from \`3-ready\`;
    with no open batch, moved to \`3-ready\``;
  - the paragraph on backlog writes (line 99) adds that a `running-batch` write appends a
    `board@1` line with the action `running-batch`;
  - wherever the document lists a backlog item's keys, it adds `running_batch` (the open batch's
    id, or `null`). If it lists none, one sentence after the `backlog.move` table says so.

### 3. The CLI's other surfaces

- No new command and no new flag. The board calls factory-redefine's function in-process, as it
  calls `move_item` today.
- `status` is unchanged: factory-redefine's `running batch: <n> CRs marked, not joined` line
  already names the CRs the board marked.

### 4. The Chief of Staff on the board's line (cards)

**`skills/chantier/references/chief-of-staff.md`**, in "*A watcher's end:*", next to the sentence
"A `board wrote (...)` line ... no tool call, no action", and the same in "*The pull path:*".

- A `board wrote (running-batch): ...` line is the user's destination for the running batch. For
  the running batch, the destination is also the go (factory-Q2). The Chief of Staff:
  - reads the CR's folder (named in the line);
  - **if the specification is final**, as factory-redefine defines it (`03-change-spec.md`
    written, no `work/specifying`, its critic run and applied when due, no open question left), or
    if the CR is in `3-ready` (automatable or specified): runs `$CHANTIER order add --note <folder>`
    with no further question. It handles the order as usual: in Foreman mode it sends the order's
    line to the Foreman; in direct mode it takes the CR when a slot frees. Then one line to the
    user: `<CR-id> added to <batch> from the board` (running-lane-Q2);
  - **otherwise**: one line to the user, `<slug> marked for <batch> from the board: it joins once
    its specification is final`. When the specification becomes final, factory-redefine's rule
    applies: `order add --note <folder>`. `status`'s `running batch:` line keeps the CR in view
    meanwhile;
  - **`order add` refused**: factory-redefine's rules (factory-Q13) apply unchanged.
- The other `board wrote` lines keep "one line, no tool call, no action".

**Keep both paths true:** the "rescan" row (line 48) adds "a `running-batch` write: act as at a
watcher's end", for a Chief of Staff whose watcher and pull path both did not run.

No agent file changes (the cards hold the contract; AGENTS.md).

### 5. Docs

- **`docs/web-board.md`, "Triage":**
  - The first bullet becomes: drag a post-it between **Inbox**, a priority, **Running batch** and
    **Next batch** (`3-ready`).
  - A new bullet says what the last column's two halves are:
    - "Running batch" is always shown;
    - it holds the CRs marked for the open batch ("waiting for its spec") and those in `1-pending`
      ("waiting for a slot");
    - a drop there writes only the mark, and the Chief of Staff adds the CR once its specification
      is final;
    - with no open batch it is greyed and a drop goes to `3-ready`.
  - The paragraph "Each change is written at once ..." keeps "a running batch's CRs are never
    written", and names the mark among the backlog's writes.
  - The Triage screenshot (`docs/web-board/triage-pc.png`, and the phone ones that show Triage)
    are retaken with `just docs-screenshots` (by hand, as the recipe says). If the Driver cannot
    run it, the PR's Known gaps names it.
- **`docs/planning-folder.md`:** the `board@1` row (line 142) names `running-batch` among the
  waking actions (`new`, `move`, `edit`, `running-batch`).
- **`README.md`:** factory-redefine's section "Running batch or next batch" gets one sentence: on
  the board, the backlog page's last column holds the same choice.

## Out of scope

- Everything factory-redefine ships: the mark function, `triage --running-batch`, its refusals,
  the mark's clearing, the stale mark, `status`'s `running batch:` line, the grill's four options,
  the destination at each spec-writer start, the factory mode's removal.
- park-live-cr: taking a CR out of the running batch, dragging a CR out of `1-pending`, the
  `blocked` state.
- The Kanban view, the Home page's backlog block and the terminal client (`clients/tui/`): they
  keep reading `3-ready` as the next batch (factory-redefine's Out of scope).
- The CR board pane (`hooks/register.tsx`) and `STATUS.json`: not touched, so no pane screenshot
  and no `just mod`.
- AGENTS.md: unchanged (the mark is a backlog file).

## Evidence

Every check reads the shipped files at the head under test: the web client's files, the cards and
the docs, read from the repository. The server's answers come from real states built by the CLI's
commands (`file`, `triage`, `open`, `order add`, and factory-redefine's
`triage --running-batch`). No prepared text stands in for a shipped file.

**Tests** (`skills/chantier/scripts/cli/tests/`, in-process, few and parametrized; `just test`
within its limit). Extend `test_triage_moves.py` or `test_board.py` (the write routes) and
`test_board_journal.py`.

- `backlog.move` with `to: "running-batch"`, one parametrized test over these states:
  - an open batch and an inbox CR with `work/specifying`: it writes `work/running-batch` naming
    the batch, moves no folder, answers 200, and appends one `board@1` line with the action
    `running-batch` and `wakes: true`;
  - the same CR dropped again: nothing written, no journal line;
  - an open batch and an ungrilled CR: 409 with `grill it first`, and nothing written;
  - an open batch and a `3-ready` CR: 200, no file written, the folder still in `3-ready`, one
    `board@1` line `running-batch` whose text names `order add`;
  - no open batch, and the same for a closed batch: the folder moved to `3-ready`, the line
    `<slug> → 3-ready (no running batch)`, a `board@1` line with the action `move`;
  - a paused batch counts as open: the mark is written.
- A marked CR moved by `backlog.move` to `3-ready`, to the inbox or to `P2` has no
  `work/running-batch` left.
- `'to'` with an unknown value: 400, and the message lists `running-batch`.
- `board/backlog.py`: an item's `running_batch` is the open batch's id when marked, and `null`
  when not marked, when the mark is stale, and with no open batch.
- `board_text` of a `running-batch` line names `order add --note`. Any other action keeps
  "act on nothing".
- The shipped web client's files, read from the repository:
  - `js/triage/columns.js` builds a drop target `running-batch`;
  - `js/triage/selection.js` offers `data-to="running-batch"`;
  - every new i18n key is present in both `en-*` and `fr-*` (the existing i18n completeness test
    covers it, if one exists; otherwise this test asserts the keys).
- `tests/test_board_design.py` passes: DESIGN.md's token table and `tokens.css` agree, and the
  component rules hold for the new column variant.
- `tests/test_event_types.py` passes unchanged (no `board@1` model change).

**Scenario** (`scenario/run_scenario.py`, `board_writes`, beside its `backlog.move` checks).

1. With the scenario's open batch, a backlog CR carrying `work/specifying` is moved with `to:
   "running-batch"` over the protocol. Then:
   - `work/running-batch` exists and names the batch;
   - `project.state` shows the item with `running_batch: <batch>`;
   - `forge-journal.jsonl` gains one `board@1` line with the action `running-batch`;
   - `status` lists the CR on its `running batch:` line.
2. An ungrilled inbox CR moved the same way is refused (409) and writes nothing.
3. The marked CR moved back to `P2`: its mark is gone.
4. Where the scenario has a step with no open batch (or after its close), a move with `to:
   "running-batch"` places the CR in `3-ready` with the `(no running batch)` line.

`scenario/README.md` lists the new checks.

**Gates.**

- `just check` in the worktree.
- `just eval-dry-run` (the change is under the CLI's `src/`).
- The pipeline's `just scenario (ubuntu-latest)` job green at the PR's head (the CLI, the cards
  and the scenario change).
- Windows coverage by `chantier gate`, per AGENTS.md, when this CR is on top of its batch's stack.
- The PR's Deliverables hold one screenshot of the Triage page with the split column, from the
  PR's head: one with an open batch, one greyed with none. They are taken from a board served by
  the head (`just docs-screenshots` or by hand).

**No host and default matrix:** the behaviour does not depend on the host or on a configured value.

## Open questions

1. **A `3-ready` CR dropped on "running batch".** factory-redefine refuses the mark on a `3-ready`
   CR (factory-Q12). This specification writes no file for that drop. The user's word lives only
   in its journal line (`board@1`, action `running-batch`), and the Chief of Staff runs
   `order add` at its next wake (running-lane-Q2). Until then the post-it stays in "next batch".
   The other way: the board writes a mark on a `3-ready` CR too, so that the top half shows it and
   `status` lists it, which changes factory-redefine's rule. Journal line only (recommended), or
   mark it?
2. **Where a marked CR is drawn.** This specification draws it once, in the "running batch" half
   only, and leaves it out of its inbox or priority row while it is marked. The other way: it
   stays in its row and the top half shows a copy. Once (recommended), or both?
3. **A CR grilled but whose spec-writer has not started** (it has `02-answers.md`, but neither
   `work/specifying` nor `03-change-spec.md`). factory-redefine's mark refuses it with "grill it
   first", so a drop on "running batch" is refused. Keep that refusal as it stands (recommended),
   or should this drop mark it, with the Chief of Staff then asking whether to start its
   spec-writer?
