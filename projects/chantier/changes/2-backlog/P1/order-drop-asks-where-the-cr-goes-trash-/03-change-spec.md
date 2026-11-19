# Change Specification: order drop names where the CR goes (trash, inbox or backlog)

## Goal

Today the only way out of a batch is `order drop`, which sends the CR to `6-trash/`. At
batch-28's end (2026-11-19), CR-381 and CR-382 were only postponed (the user merged them a week
later), yet they went to the trash and needed a `restore` and a `triage` to reach the backlog.

Wanted (`01-intent.md`, `02-answers.md` 1): taking a CR out of a batch names its destination, and
the Chief of Staff asks the user which one when the user has not said it:

- **trash**: the CR is cancelled (today's drop);
- **inbox**: to be looked at again;
- **backlog `P1`..`P4`**: postponed or handed off; the usual case for delegated work.

Whatever the destination, the CR keeps its work (worktree, branch, open PR). Its PR is closed only
when it goes to the trash.

## What changes

### 1. CLI: `order drop` takes a destination, required

`skills/chantier/scripts/cli/src/chantier/declare/orders.py`, `commands/orders.py`,
`commands/orders_apply.py` (`_drop`).

- New form: `order drop <cr> --note trash|inbox|P1|P2|P3|P4`. It uses `--note` for its value like
  `after`, `rounds` and `slots` do. The value is case-insensitive (`p2` reads as `P2`). The parser's
  `kind` and `--note` help texts name it ("drop: trash, inbox or P1..P4").
- `_normalise_args` turns the value into the destination folder: `trash` → `6-trash`, `inbox` →
  `1-inbox`, `P<n>` → `2-backlog/P<n>`. So the order's line to the Foreman reads, for example,
  `[chief-of-staff→foreman] order O-1: drop CR-103 2-backlog/P2`. The order record's `note` holds
  the same folder.
- With no `--note`, or with any other value, the order is refused with exit 1 (`EXIT_USAGE`) and
  nothing is recorded: `order drop <cr> --note trash|inbox|P1..P4: where the CR goes; ask the
  user when they have not said it`. No default: the CLI never chooses the destination.
- The record keeps the destination on the CR: a new optional `CrEntry` field
  (`core/records.py`), e.g. `left_to: str | None`, holding the destination folder (`6-trash`,
  `1-inbox` or `2-backlog/P<n>`). It is set when the order is recorded, for a live CR too (whose
  folder only moves at `cancel`, below). The CR's status stays `cancelled` for every destination:
  every path that reads `merged or cancelled` (the batch's end, `close`, the hub, `ensure_unclaimed`,
  the board) keeps working unchanged.
- A second drop of a CR that is already cancelled is still refused (exit 2), whatever the
  destination. A second drop of a live CR not yet cancelled replaces its destination: the record
  and the new order line carry the later word.
- The refusals already there stay: a merged CR (`cannot drop … already merged`).

### 2. CLI: the folder moves to its destination

`lifecycle/stages.py` (`trash_cr` and a new sibling for the other destinations), used by
`_drop` (a CR that is not live) and by `cancel` (`commands/release.py`, a live CR).

- **trash**: unchanged. The folder goes to `6-trash/<YYMMDD-HHMM>-<number>-<slug>/`, as
  `trash_cr` does today, and `restore` works on it as before.
- **inbox / backlog `P<n>`**: the folder goes to `1-inbox/<slug>/` or `2-backlog/P<n>/<slug>/`,
  named the way `restore` names a folder it brings back from a batch's trash (no date, no number;
  `commands/intake.py`, `_restored_name`). As `restore` does (`_remember`), it gets the line
  `formerly CR-<n> of batch-<m>` appended to its `01-intent.md` (or `notes.md` when there is no
  `01-intent.md`), and the number is written to `restored.json` so it is never given again. The
  folder moves whole: its `work/`, `evidence/` and STATUS files go with it. While the batch is
  open, `write_batch` keeps rewriting that CR's STATUS files where they now are, as it does for any
  CR "wherever they are". The planning folder's dashboard (`write_dashboard`) shows the item in its
  new stage, as after a `triage`.
- A name already taken in the destination (a folder of that name in `1-inbox`, `2-backlog/P1..P4`
  or `3-ready`, or a CR of the open batch with that slug: the same test as `restore`'s
  `_check_free`) refuses with exit 2 (`EXIT_PRECONDITION`) before anything changes, naming the
  folder in the way. For a live CR the order checks the name when it is recorded, so the user hears
  of a clash at once, and `cancel` checks it again before the move.
- The command's output names the destination: `dropped CR-103 to 2-backlog/P2: <folder>` (a CR not
  live), `cancelled CR-103 to 1-inbox; stopped …` (`cancel`). A trash drop keeps today's words
  (`dropped CR-103: <path>`, `cancelled CR-103; stopped …`).
- `3-ready` is not a destination: a factory batch would take the CR again on its own.

### 3. CLI: `cancel` follows the destination of the drop

`commands/release.py` (`cancel`), `declare/release.py`.

- `cancel <cr> --epoch <n>` moves the folder to the destination the CR's drop order recorded
  (`left_to`), instead of always `6-trash`.
- When the CR has no destination recorded (no `order drop` before it), `cancel` is refused with
  exit 2 and nothing changes: `cancel <cr>: no destination recorded; the Chief of Staff's
  "order drop <cr> --note trash|inbox|P1..P4" names it`. `cancel` takes no destination of its
  own: the destination is the user's word, carried by the order.
- The rest is unchanged: it stops the gate and the processes, the status becomes `cancelled`,
  and the batch's end follows when it was the last CR.

### 4. CLI: the work is kept, and `close` keeps it apart

`commands/closing.py` (`_to_remove`, `_closing`).

- Today `close` lists every cancelled CR's worktree and branch "to remove on the same word". From
  now on it lists only the CRs whose destination is `6-trash`. A CR moved to the inbox or the
  backlog gets a line of its own, which is not a removal: `kept, moved out with their work: CR-381
  (2-backlog/P2) worktree <path> branch <branch> PR <link or none>; …` (or `none`). The Chief of
  Staff removes nothing from that line.
- The end-of-batch cleanup (`endpause.py`, merged CRs only) is unchanged.

### 5. CLI: status words and the stack's checks name the destination

- `status/words.py` (`label`): a cancelled CR reads `⚪ dropped` when it went to the trash (as
  today) and `⚪ dropped to 1-inbox` or `⚪ dropped to 2-backlog/P<n>` otherwise. This label is in
  STATUS.md, STATUS.json and `status`. **It changes what the CR board pane draws**: AGENTS.md's
  pane rule applies (one screenshot of the pane from a real Claude Code session at the PR's head in
  Deliverables, or the Known gap "no screenshot of the pane from a real session").
- `commands/forge_stack.py` (`_dropped`, check 2) and `commands/forge_stack_gh.py`
  (`held_outside`): a PR of a CR moved to the inbox or the backlog is named apart from a trashed
  one. Trash: `…, dropped: close it` (today). Other destinations: `…, moved to <destination>: leave
  it open`, e.g. `it also held #346 of CR-381, moved to 2-backlog/P2: leave it open`.
- `history.py`: the result stays `dropped`. The entry gains the destination, e.g. `"to":
  "2-backlog/P2"`, so the batch's record says where each dropped CR went.
- `b.log` of the drop and of `cancel` carries the destination (`to=`).

### 6. Cards

Both hosts read the same cards. The agent files (`agents/`, `com.github.copilot/agents/`) do not
change.

- `skills/chantier/references/chief-of-staff.md`:
  - Steering block: `order drop CR-104 --note trash|inbox|P1..P4   # where it goes, with its work;
    the PR is closed only for trash`.
  - A new rule beside it. The user's word to take a CR out of a batch ("drop", "take it out",
    "postpone", "remove from the batch") names where it goes. When it does not, ask once, in the
    user's language, before the order: trash (cancelled), inbox (to look at again) or backlog P1..P4
    (postponed or handed off; the usual case for delegated work). Never choose for the user. A
    word that already says it ("cancel it" → trash; "postpone it, P2" → `P2`) needs no question.
  - "Dropping a CR from a stack": what to tell the user depends on the destination. Trash: as today
    (its PR is closed). Inbox or backlog: its commits come out of the PRs above it, its PR stays
    open as it is, its branch and worktree stay and are not offered for removal at `close`, and the
    folder is at `<destination>/<slug>`.
  - Table D (close while something runs): "drop it (`order drop <cr> --note …`, with the
    destination the user names)".
  - The `close` offer: the `kept, moved out with their work` line is shown to the user, and nothing
    in it is removed.
- `skills/chantier/references/foreman.md`: the line on cancelling a dropped live CR. `cancel` moves
  it to the destination its drop order recorded. The Foreman never chooses one: a `cancel` refused
  for a missing destination goes up to the Chief of Staff as an ask. "A drop in the stack": the
  `drop: <cr>` note sent to the stack driver carries the destination (`drop: <cr> to
  <destination>`).
- `skills/chantier/references/driver.md`, stack driver, "Removing a dropped CR": steps 1 to 4
  unchanged. Step 5 (close the PR) applies only to a CR dropped to the trash. For a CR moved to the
  inbox or the backlog, the PR is left open as it is: no close, no comment, no change of its base
  or draft state. The note reads `drop: <cr> to <destination>`; a note with no destination (an
  older Foreman) means trash.
- `skills/chantier/references/concepts.md`:
  - Lifecycle: "`6-trash/…` (dropped, with its work …)" becomes "or, on `order drop`, `6-trash/…`
    (cancelled), `1-inbox/<slug>/` or `2-backlog/P<n>/<slug>/` (taken out of the batch), always
    with its work, the latter two without date or number and with a line `formerly CR-<n> of
    batch-<m>`".
  - The stack bullet "A CR dropped from the stack": its PR is closed only when it goes to the
    trash.

### 7. Docs

The lines that say `order drop` sends a CR to `6-trash/` now name the three destinations:
`docs/planning-folder.md` (the tree and its text), `docs/cr-folder-lifecycle-texts.md`,
`docs/cr-lifecycle-texts.md`, `docs/cr-lifecycle-simple-texts.md`, and the matching text label in
their SVGs (`cr-folder-lifecycle.svg`, `cr-lifecycle.svg`, `cr-lifecycle-simple.svg`): "order
drop → 6-trash/, 1-inbox/ or 2-backlog/Pn/, with its work". No other drawing change.

## Decisions carried from 02-answers.md

- The destination is asked: trash, inbox or backlog (answer 1) → sections 1 and 6 (required
  value; the Chief of Staff asks).
- Backlog for delegated tasks, trash for cancelled ones (answer 1) → the wording of the question
  in the Chief of Staff's card.
- The work is kept whatever the destination; the PR is closed only for the trash (intent) →
  sections 2, 4, 5 and 6.
- Priority P1, joins batch-29 once specified (Chief of Staff, 2026-11-20): no effect on the content.

## Out of scope

- **Holding a CR in the batch but out of the stack** (a ready CR kept apart from `stack` and
  `forge-stack rebuild` until the user puts it back): that is the neighbour CR
  `2-backlog/P1/retro-batch-28-hold-a-ready-cr-out-of-th`. This CR takes a CR **out of the batch**
  and decides where its folder goes. It adds no `hold` order and no option to `stack` or
  `forge-stack`.
- `3-ready` as a destination (section 2).
- Recording a merge, made later, of the open PR of a CR moved to the inbox or the backlog: the CR is
  `cancelled` in the record, so the hub does not read its PR and the board records nothing for it.
- Removing, later, the worktree and branch of a CR moved out: they stay, and `close` names them as
  kept.
- `restore`, `triage` and `abandon`: unchanged.
- The web board: it never edits a batch. It shows the new label through STATUS.json and needs no
  change of its own.

## Evidence

No host or default/configured dependency: no matrix.

Tests (`skills/chantier/scripts/cli/tests/`, in-process, few and parametrized; keep `just test`
within its budget):

- `test_rail_refusals.py` (or the closest existing file): `order drop <cr>` with no `--note`, and
  with `--note P5`, `--note ready` and `--note 3-ready`, each exits 1 and leaves `batch.json` byte
  for byte unchanged. `cancel <cr> --epoch 1` on a live CR with no drop order exits 2 and moves
  nothing.
- `test_batch_end.py`: parametrize the existing `drop` and `cancel` cases over `trash`, `inbox`
  and `P2`. For each, assert:
  - the folder lands in `6-trash/<stamp>-<n>-<slug>`, `1-inbox/<slug>` or `2-backlog/P2/<slug>`;
  - the CR's `status` is `cancelled` and its `left_to` is the destination folder;
  - for inbox and P2: `01-intent.md` ends with `formerly CR-<n> of batch-<m>`, and `restored.json`
    holds `<n>`;
  - the worktree and branch still exist;
  - the batch still pauses when it was the last CR.
- A clash: with `2-backlog/P2/<slug>` already present, `order drop <cr> --note P2` exits 2 and
  moves nothing. For a live CR it is refused at the order.
- `close` (no `--yes`), with one CR dropped to the trash and one to P2: the removal line names only
  the trashed one, and the `kept, moved out with their work` line names the other with its
  destination, worktree and branch.
- `test_stack_label.py` (or the label's existing test): the labels `⚪ dropped` and `⚪ dropped to
  2-backlog/P2` from a real drop, not from a hand-built record.
- `forge-stack` check 2 and `held_outside`: one trashed and one moved CR with PRs in the stack give
  `dropped: close it` and `moved to 2-backlog/P2: leave it open` (`forge_world.py` fixture).
- `test_scenario_coverage.py`, if it lists commands or forms: updated for the new `--note` of
  `drop`.

Scenario (`scenario/run_scenario.py`):

- Step 5: `order drop CR-103 --note trash` keeps every existing check (trash path under the date,
  `⚪ dropped` in its STATUS.md), and the order line now ends with `6-trash`.
- A new check in the same step, or in the direct-mode step near line 2791: a queued CR dropped with
  `--note P3`:
  - lands in `2-backlog/P3/<slug>` with the `formerly` line;
  - its STATUS.md says `⚪ dropped to 2-backlog/P3`;
  - `order add --note 2-backlog/P3/<slug>` brings it back into the running batch under a new
    number, which proves `ensure_unclaimed` still lets it in.
- The other `order drop` calls (lines ~1957-1958, ~2791) gain an explicit `--note trash`.
- Step `close` (near line 3793): the dropped CR's line still names its worktree and branch.

Each check reads the shipped cards and CLI at the head under test. Gates: `just check`; `just
eval-dry-run` (CLI `src/` change); `just scenario (ubuntu-latest)` green at the PR's head (CLI
and cards change). The pane screenshot of section 5 is due in the PR's Deliverables, or its Known
gap is named.

## Open questions

1. **The CR number.** The intent names "losing their CR number" as a cost. This specification only
   keeps the trace (`formerly CR-<n> of batch-<m>`, and the number never given again). When the CR
   joins a later batch, should it get its old number back (`CR-381`) instead of a new one? That
   changes `add_cr` and `next_cr_number`.
2. **Its existing branch and PR when it comes back.** A CR moved out keeps its branch and open PR.
   When it joins a batch again, should its new Driver pick up that branch and PR, or start fresh
   (today's `order add`, a new branch named after the new number, leaving the old PR to the user)?
3. **A trash drop outside a stack.** The intent says the PR is closed for the trash. Today only the
   stack driver closes a dropped CR's PR. Outside a stack nobody does, and the Foreman never edits a
   PR. Should someone close it outside a stack too (and who: the Chief of Staff on the drop, or a
   Driver), or does this CR keep today's behaviour there?
4. **The open PR of a CR moved out of a stack.** That PR still has the branch of the CR below it as
   its base. This specification leaves it as it is. Should it instead be retargeted on the default
   branch, or turned to a draft, so the user does not merge it into another CR's branch?
