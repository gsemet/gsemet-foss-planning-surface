# Change Specification: order drop names where the CR goes (trash, inbox or backlog)

## Goal

Today the only way out of a batch is `order drop`, which sends the CR to `6-trash/`. At
batch-28's end (2026-11-19), CR-381 and CR-382 were only postponed (the user merged them a week
later), yet they went to the trash, needed a `restore` and a `triage` to reach the backlog, and
lost their CR number on the way.

Wanted (`01-intent.md`, `02-answers.md`): taking a CR out of a batch names its destination, and the
Chief of Staff asks the user which one when the user has not said it:

- **trash**: the CR is cancelled (today's drop);
- **inbox**: to be looked at again;
- **backlog `P1`..`P4`**: postponed or handed off; the usual case for delegated work.

Whatever the destination, the CR keeps its work (worktree, branch, open PR). Its PR is closed only
when it goes to the trash. A CR moved to the inbox or the backlog keeps its number. When it joins a
later batch it comes back under that number, with its branch and its PR.

## What changes

### 1. CLI: `order drop` takes a destination, required

`skills/chantier/scripts/cli/src/chantier/declare/orders.py`, `commands/orders.py`,
`commands/orders_apply.py` (`_drop`).

- **New form:** `order drop <cr> --note trash|inbox|P1|P2|P3|P4`. It uses `--note` for its value,
  as `after`, `rounds` and `slots` do. The value is case-insensitive (`p2` reads as `P2`). The
  parser's `kind` and `--note` help texts name it ("drop: trash, inbox or P1..P4").
- **The value becomes a folder:** `_normalise_args` turns it into the destination folder: `trash`
  → `6-trash`, `inbox` → `1-inbox`, `P<n>` → `2-backlog/P<n>`. The order's line to the Foreman
  carries it, e.g. `[chief-of-staff→foreman] order O-1: drop CR-103 2-backlog/P2`, and the order
  record's `note` holds the same folder.
- **No default:** with no `--note`, or with any other value, the order is refused with exit 1
  (`EXIT_USAGE`) and nothing is recorded. The message: `order drop <cr> --note trash|inbox|P1..P4:
  where the CR goes; ask the user when they have not said it`. The CLI never chooses the
  destination.
- **The record keeps it:** a new optional `CrEntry` field (`core/records.py`), `left_to: str |
  None`, holds the destination folder (`6-trash`, `1-inbox` or `2-backlog/P<n>`). It is set when
  the order is recorded, for a live CR too, whose folder only moves at `cancel` (section 3). The
  CR's status becomes `cancelled` for every destination. So every path that reads "merged or
  cancelled" keeps working unchanged: the batch's end, `close`, the hub, `ensure_unclaimed` and the
  board.
- **A second drop:** of a CR already cancelled, still refused (exit 2), whatever the destination.
  Of a live CR not yet cancelled, it replaces the destination: the record and the new order line
  carry the later word.
- The refusal of a merged CR stays.
- **A trash drop outside a stack** (the batch's mode is not `stack`) of a CR that has a PR: the
  order's line to the steering session ends with `; close its PR <link>`, e.g.
  `[chief-of-staff→foreman] order O-1: drop CR-103 6-trash; close its PR
  https://github.com/o/r/pull/346`. In direct mode, `order drop` prints the same clause in its own
  output. The CLI runs no forge command itself. In a stack the stack driver closes it (section 6),
  and the line has no clause.

### 2. CLI: the folder moves to its destination, and a CR moved out keeps its number

`lifecycle/stages.py` (`trash_cr`, and a new sibling for the other destinations), used by `_drop`
(a CR that is not live) and by `cancel` (`commands/release.py`, a live CR).

- **trash:** unchanged. The folder goes to `6-trash/<YYMMDD-HHMM>-<number>-<slug>/`, and `restore`
  works on it as before (it still takes the number off; restore is not changed).
- **inbox / backlog `P<n>`:** the folder goes to `1-inbox/<number>-<slug>/` or
  `2-backlog/P<n>/<number>-<slug>/`: the batch folder's name (`381-<slug>`), with its number and no
  date. The folder moves whole: `work/`, `evidence/` and the STATUS files go with it.
  - **What it writes in the folder:** `formerly.json`, the CR's record outside the batch:
    `{"cr": "CR-381", "batch": "batch-28", "branch": "<branch>", "worktree": "<path>", "pr": "<link
    or null>"}`. It also appends the line `formerly CR-381 of batch-28` to `01-intent.md` (or to
    `notes.md` when there is no `01-intent.md`), for a person reading the folder.
  - **The number stays reserved:** the number is written to `restored.json` (the max kept by
    `next_cr_number`, `core/batch.py`). So no other CR ever gets it, even after the batch's close.
  - **Validation:** `formerly.json` joins the CR folder's layout. Add it to
    `lifecycle/layout_check.py` `CR_FILES` and to concepts.md's "Change Request" tree, so
    `validate` reports no gap for it.
  - **STATUS files and dashboard:** while the batch is open, `write_batch` keeps rewriting that CR's
    STATUS files where they now are, as it does for any CR "wherever they are". The planning
    folder's dashboard (`write_dashboard`) shows the item in its new stage, as after a `triage`.
- **A name already taken:** the destination already holds that name (a folder of that name in
  `1-inbox`, `2-backlog/P1..P4` or `3-ready`, or a CR of the open batch with that slug; the same
  test as `restore`'s `_check_free`). The drop is refused with exit 2 (`EXIT_PRECONDITION`) before
  anything changes, and the message names the folder in the way. For a live CR the order checks the
  name when it is recorded, so the user hears of a clash at once, and `cancel` checks it again
  before the move.
- **Output:** the command names the destination: `dropped CR-103 to 2-backlog/P2: <folder>` (a CR
  that is not live), `cancelled CR-103 to 1-inbox; stopped …` (`cancel`). A trash drop keeps
  today's words (`dropped CR-103: <path>`, `cancelled CR-103; stopped …`).
- **Not a destination:** `3-ready`, because a factory batch would take the CR again on its own.

### 3. CLI: `cancel` follows the destination of the drop

`commands/release.py` (`cancel`), `declare/release.py`.

- `cancel <cr> --epoch <n>` moves the folder to the destination recorded by the drop (`left_to`),
  as section 2 says, instead of always to `6-trash`.
- With no destination recorded (no `order drop` before it), `cancel` is refused with exit 2 and
  nothing changes: `cancel <cr>: no destination recorded; the Chief of Staff's "order drop <cr>
  --note trash|inbox|P1..P4" names it`. `cancel` takes no destination of its own: the destination
  is the user's word, carried by the order.
- **Trash, outside a stack, with a PR:** `cancel` prints `close its PR <link>` too (section 1).
- The rest is unchanged: it stops the gate and the processes, and the batch's end follows when this
  was the last CR.

### 4. CLI: a CR that comes back gets its number, its branch and its PR

`commands/opening.py` (`add_cr`), used by `open`, `order add` and the factory's `triage --ready`.

When the folder that joins holds `formerly.json`:

- **The number:** the CR takes the number from `formerly.json` (`CR-381`), not
  `next_cr_number`. Its batch folder is `1-pending/381-<slug>`.
- **The same batch:** when the open batch still holds that CR, cancelled, with `left_to` set (it
  is re-added to the batch it left), that entry is reopened instead of adding a second one. Its
  status becomes `queued`, `left_to`, `agent` and `phase` are cleared, `round` goes to 0, and
  `path` is the new folder. Its notes and cost stay.
- **A refusal:** the open batch holds that number for another live CR, which only a broken record
  can do. The join is refused with exit 3 (`EXIT_CONFLICT`) and nothing moves.
- **Its branch:** the CR's branch still exists in the clone or main checkout (`core/git.py`
  `branch_exists`).
  - **Yes:** `branch`, `worktree` and `pr` are taken from `formerly.json`. The output says `CR-381
    joins with its branch <branch> and PR <link>` (or `and no PR`).
  - **No (gone):** the CR starts fresh under the same number. The branch is named the usual way
    (`chantier/<batch>/cr-381-<title>`), the worktree is `<worktrees>/<batch>-CR-381`, and `pr` is
    none. The output says `CR-381 joins fresh: its branch <branch> is gone`.
- **`formerly.json` is deleted** once the record holds the CR again. A later move out writes it
  anew.
- **A folder without `formerly.json`** (a trashed CR restored, any other item) joins as today, under
  a new number.

`take`'s facts already print the CR's branch, worktree and `PR:`. The Driver's part is in its card
(section 6).

### 5. CLI: `close`, status words and the stack's checks

- **`close`** (`commands/closing.py`, `_to_remove`, `_closing`): today it lists every cancelled
  CR's worktree and branch "to remove on the same word". From now on it lists only the CRs whose
  `left_to` is `6-trash`. The CRs moved to the inbox or the backlog get a line of their own, which
  is not a removal: `kept, moved out with their work: CR-381 (2-backlog/P2) worktree <path> branch
  <branch> PR <link or none>; …` (or `none`). Nothing on that line is removed.
- **The end-of-batch cleanup** (`endpause.py`, merged CRs only): unchanged.
- **Status label** (`status/words.py`, `label`): a cancelled CR reads `⚪ dropped` when it went to
  the trash (as today). Otherwise it reads `⚪ dropped to 1-inbox` or `⚪ dropped to
  2-backlog/P<n>`. The label is in STATUS.md, STATUS.json and `status`.
  - **It changes what the CR board pane draws**, so AGENTS.md's pane rule applies: the PR's
    Deliverables carry one screenshot of the pane from a real Claude Code session at the PR's head.
    Until then the PR names the Known gap "no screenshot of the pane from a real session".
- **The stack's checks** (`commands/forge_stack.py` `_dropped` and check 2,
  `commands/forge_stack_gh.py` `held_outside`): the PR of a CR moved to the inbox or the backlog is
  named apart from a trashed one.
  - Trash: `…, dropped: close it`, as today.
  - Other destinations: `…, moved to <destination>: draft, on <default branch>`, e.g. `it also held
    #346 of CR-381, moved to 2-backlog/P2: draft, on main`.
  - A moved PR is not "foreign" in check 2.
- **`history.py`:** the result stays `dropped`. The entry gains the destination (`"to":
  "2-backlog/P2"`).
- **The event log:** `b.log` of the drop and of `cancel` carries `to=`.

### 6. Cards

Both hosts read the same cards. The agent files (`agents/`, `com.github.copilot/agents/`) do not
change.

- **`skills/chantier/references/chief-of-staff.md`:**
  - **Steering block:** `order drop CR-104 --note trash|inbox|P1..P4   # where it goes, with its
    work; its number kept unless trash`.
  - **Asking for the destination** (a new rule beside it): the user's word that takes a CR out of
    a batch ("drop", "take it out", "postpone", "remove from the batch") names where it goes. When
    it does not, ask once, in the user's language, before the order: trash (cancelled), inbox (to
    look at again), or backlog P1..P4 (postponed or handed off; the usual case for delegated work).
    Never choose for the user. A word that already says it needs no question ("cancel it" → trash;
    "postpone it, P2" → `P2`).
  - **Direct mode:** a trash drop line ending `close its PR <link>` is yours. Close it (`gh pr
    close <n>`, `glab mr close <n>`, no `--delete-branch`, no comment) before you mark the order
    done.
  - **"Dropping a CR from a stack":** what to tell the user depends on the destination.
    - Trash: as today (its PR is closed).
    - Inbox or backlog: its commits come out of the PRs above it, and its PR goes to draft on the
      default branch. Its branch and worktree stay and are not offered for removal at `close`. The
      folder is at `<destination>/<number>-<slug>`, and the CR comes back under its number with its
      branch and PR when the user adds it again.
  - **Table D** (close while something runs): "drop it (`order drop <cr> --note …`, with the
    destination the user names)".
  - **The `close` offer:** show the user the `kept, moved out with their work` line, and remove
    nothing from it.
  - **A CR that comes back:** `order add` of a folder with `formerly.json` prints `joins with its
    branch …` or `joins fresh: its branch … is gone`. Tell the user which.
- **`skills/chantier/references/foreman.md`:**
  - **Cancelling a dropped live CR:** `cancel` moves it to the destination its drop order recorded,
    and the Foreman never chooses one. A `cancel` refused for a missing destination goes up to the
    Chief of Staff as an ask.
  - **Closing the PR, a named exception** to "never … edit a PR": a drop order that ends `close its
    PR <link>` (a trash drop outside a stack; after `cancel` for a live CR) is closed by the Foreman
    (`gh pr close <n>`, `glab mr close <n>`, no `--delete-branch`, no comment) before `order done`.
  - **"A drop in the stack":** the note to the stack driver carries the destination: `drop: <cr> to
    <destination>`.
- **`skills/chantier/references/driver.md`:**
  - **Stack driver, "Removing a dropped CR":** steps 1 to 4 are unchanged for every destination.
    - Step 5 (close the PR) applies to a CR dropped to the trash only.
    - For a CR moved to the inbox or the backlog, step 5 becomes:
      1. Turn its PR to a draft (`gh pr ready --undo`, `glab mr update --draft`).
      2. Retarget it on the default branch (`gh pr edit <n> --base <default>`, `glab mr update <n>
         --target-branch <default>`).
      3. Rebase its branch onto the default branch in its worktree (`git -C <worktree> rebase --onto
         origin/<default> <the branch under it>`).
      4. Push with `--force-with-lease`.
    - A rebase conflict: `rebase --abort`, push nothing for it, leave it in draft and retargeted,
      and name it in the hand-back. Its next Driver rebases it when it comes back.
    - No comment and no close.
    - A `drop: <cr>` note with no destination (an older Foreman) means trash.
  - **CR Driver, the worktree bullet:** a CR that comes back from a batch shows a `PR:` at its
    first take.
    - Use its branch: its recorded worktree if it is there, else `git -C <main checkout> worktree
      add <path> <branch>`.
    - Rebase it on the base `take` names, and ship to that same PR. Never open a second PR.
    - A recorded PR found closed on the forge: reopen it (`gh pr reopen <n>`, `glab mr reopen
      <n>`) when its branch exists. Otherwise hand back blocked with the question.
- **`skills/chantier/references/concepts.md`:**
  - **Lifecycle:** "`6-trash/…` (dropped, with its work …)" becomes: "or, on `order drop`,
    `6-trash/…` (cancelled), or `1-inbox/<number>-<slug>/` or `2-backlog/P<n>/<number>-<slug>/`
    (taken out of the batch, with `formerly.json`), always with its work; a CR taken out keeps its
    number and comes back under it, with its branch and PR when the branch still exists".
  - **The "Change Request" tree:** `formerly.json`.
  - **The stack bullet "A CR dropped from the stack":** its PR is closed when it goes to the trash.
    Otherwise it goes to draft on the default branch.

### 7. Docs

The lines that say `order drop` sends a CR to `6-trash/` now name the three destinations. The
files:

- `docs/planning-folder.md` (the tree and its text);
- `docs/cr-folder-lifecycle-texts.md`, `docs/cr-lifecycle-texts.md` and
  `docs/cr-lifecycle-simple-texts.md`;
- the matching text label in their SVGs (`cr-folder-lifecycle.svg`, `cr-lifecycle.svg`,
  `cr-lifecycle-simple.svg`).

The new wording: "order drop → 6-trash/, 1-inbox/ or 2-backlog/Pn/, with its work". No other
drawing change.

## Decisions carried from 02-answers.md

| Decision (source) | Where |
| --- | --- |
| The destination is asked: trash, inbox or backlog; backlog for delegated tasks, trash for cancelled ones (answer 1) | sections 1 and 6 |
| The work is kept whatever the destination; the PR is closed only for the trash (intent) | sections 2, 5 and 6 |
| Spec question 1: a CR moved out keeps its number, its folder and the record carry it, it gets the same number back in a later batch, and the number is never given to another CR | sections 2 and 4 |
| Spec question 2: its new Driver picks up the existing branch and open PR, rebased; fresh only when the branch is gone | sections 4 and 6 |
| Spec question 3: a trash drop outside a stack, the steering session closes the PR, prompted by the drop's line; the CLI runs no forge write | sections 1, 3 and 6 |
| Spec question 4: a PR moved out of a stack goes to draft and onto the default branch | sections 5 and 6 |
| Priority P1, joins batch-29 once specified | no effect on the content |

## Out of scope

- **Holding a CR in the batch but out of the stack** (a ready CR kept apart from `stack` and
  `forge-stack rebuild` until the user puts it back): that is the neighbour CR
  `2-backlog/P1/retro-batch-28-hold-a-ready-cr-out-of-th`. This CR takes a CR **out of the batch**
  and decides where its folder goes. It adds no `hold` order and no option to `stack` or
  `forge-stack`. Only the end state of the PR (draft, on the default branch) is shared with it.
- `3-ready` as a destination (section 2).
- A PR moved out of a series or parallel batch: it is left as it is (answer 4 covers a stack).
- Recording a later merge of the open PR of a CR moved out: the CR is `cancelled` in the record,
  so the hub does not read its PR and the board records nothing for it.
- Removing, later, the worktree and branch of a CR moved out: they stay, and `close` names them as
  kept.
- `restore` (a trashed CR still comes back under a new number), `triage` and `abandon`: unchanged.
- The web board: it never edits a batch, and it shows the new label through STATUS.json.

## Evidence

No host or default/configured dependency, so no matrix.

**Tests** (`skills/chantier/scripts/cli/tests/`, in-process, few and parametrized; keep `just test`
within its budget):

- **Refusals** (`test_rail_refusals.py` or the closest file):
  - `order drop <cr>` with no `--note`, and with `--note P5`, `ready` and `3-ready`: each exits 1
    and leaves `batch.json` byte for byte unchanged.
  - `cancel <cr> --epoch 1` on a live CR with no drop order: exits 2 and moves nothing.
- **Each destination** (`test_batch_end.py`): parametrize the existing `drop` and `cancel` cases
  over `trash`, `inbox` and `P2`, and assert for each:
  - the folder lands in `6-trash/<stamp>-<n>-<slug>`, `1-inbox/<n>-<slug>` or
    `2-backlog/P2/<n>-<slug>`;
  - `status` is `cancelled` and `left_to` is that folder;
  - for inbox and P2: `formerly.json` holds the CR, the batch, the branch, the worktree and the PR;
    `01-intent.md` ends with the `formerly` line; `restored.json` holds `<n>`;
  - the worktree and branch still exist;
  - the batch still pauses when this was its last CR.
- **A clash:** with `2-backlog/P2/<n>-<slug>` already there, `order drop <cr> --note P2` exits 2
  and moves nothing. For a live CR it is refused at the order.
- **Coming back** (`test_opening_and_restore.py`): parametrize over the same batch and a later
  batch (close, then open), each with the branch kept and with the branch deleted:
  - the CR is `CR-<n>` again, in `1-pending/<n>-<slug>`;
  - with the branch kept: `branch`, `worktree` and `pr` come from `formerly.json`, and the output
    says `joins with its branch`;
  - with the branch deleted: a fresh branch name under the new batch, `pr` none, and the output
    says `joins fresh`;
  - same batch: one entry only, reopened `queued` with round 0;
  - `formerly.json` is gone from the folder;
  - an unrelated item filed afterwards gets a number above `<n>`.
- **The PR close line:** a trash drop of a CR with a PR, parallel mode: the order line ends with `;
  close its PR <link>`. The same in stack mode: no clause. A drop to P2: no clause.
- **`close`** (no `--yes`), one CR dropped to the trash and one to P2: the removal line names only
  the trashed one. The `kept, moved out with their work` line names the other, with its
  destination, worktree, branch and PR.
- **The labels** (`test_stack_label.py` or the label's existing test): `⚪ dropped` and `⚪ dropped
  to 2-backlog/P2`, from a real drop, never from a hand-built record.
- **`forge-stack` messages:** check 2 and `held_outside`, with one trashed and one moved CR whose
  PRs are in the stack (`forge_world.py`), give `dropped: close it` and `moved to 2-backlog/P2:
  draft, on main`. The moved PR is not counted as foreign.
- **`validate`:** a folder holding `formerly.json` gives no gap (`test_validate.py`).
- **Structure:** `test_scenario_coverage.py`, if it lists command forms, takes the new `--note` of
  `drop`.

**Scenario** (`scenario/run_scenario.py`):

- **Step 5:** `order drop CR-103 --note trash` keeps every existing check (the trash path under the
  date, `⚪ dropped` in its STATUS.md). The order line now carries `6-trash`.
- **A move to the backlog and back,** in the direct-mode step near line 2791: a queued CR dropped
  with `--note P3`, then brought back.
  - It lands in `2-backlog/P3/<n>-<slug>` with `formerly.json`, and its STATUS.md says `⚪ dropped
    to 2-backlog/P3`.
  - `order add --note 2-backlog/P3/<n>-<slug>` brings it back into the running batch as the same
    `CR-<n>`, one entry, `queued`.
- **The other drops:** the `order drop` calls near lines 1957-1958 and 2791 gain an explicit `--note
  trash`.
- **`close`** (near line 3793): the dropped CR's line still names its worktree and branch.

Each check reads the shipped cards and CLI at the head under test.

**Gates:**

- `just check`;
- `just eval-dry-run` (a CLI `src/` change);
- `just scenario (ubuntu-latest)` green at the PR's head (a CLI and cards change);
- the pane screenshot of section 5 in the PR's Deliverables, or its Known gap named.
