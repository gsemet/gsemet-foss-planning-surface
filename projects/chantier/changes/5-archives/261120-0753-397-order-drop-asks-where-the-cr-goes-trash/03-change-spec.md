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

Whatever the destination, the CR keeps its work (worktree, branch, open PR), and its PR is closed
only when it goes to the trash. A CR moved to the inbox or the backlog keeps its number: its folder
carries it, and no other CR is ever given it.

This CR stops at the drop. Coming back under that number, with the branch and the PR, is the CR
`1-inbox/order-drop-come-back-same-number-branch-pr` (answer 10). It reads the `formerly.json`
written here (section 2).

## What changes

### 1. CLI: `order drop` takes a destination, required

`skills/chantier/scripts/cli/src/chantier/declare/orders.py`, `commands/orders.py`,
`commands/orders_apply.py` (`_drop`).

- **The form:** `order drop <cr> --note trash|inbox|P1|P2|P3|P4`. It uses `--note` for its value,
  as `after`, `rounds` and `slots` do. The value is case-insensitive (`p2` reads as `P2`). The
  parser's `kind` and `--note` help texts name it ("drop: trash, inbox or P1..P4").
- **Normalised to a folder:** `_normalise_args` turns the value into the destination folder:
  `trash` → `6-trash`, `inbox` → `1-inbox`, `P<n>` → `2-backlog/P<n>`.
  - The order's line carries that folder, e.g. `[chief-of-staff→foreman] order O-1: drop CR-103
    2-backlog/P2`.
  - The order record's `note` holds the same folder.
- **No default:** with no `--note`, or with any other value, the order is refused with exit 1
  (`EXIT_USAGE`) and nothing is recorded: `order drop <cr> --note trash|inbox|P1..P4: where the CR
  goes; ask the user when they have not said it`. The CLI never chooses.
- **A release CR or a fix CR** (`kind` `release` or `fix`, as `forge_stack.py` reads it) leaves only to the trash
  (answer 5). Another destination is refused with exit 2 (`EXIT_PRECONDITION`) and nothing
  recorded: `<cr> is a release CR|a fix CR: it leaves the batch only to the trash (--note trash)`.
- **The record:** a new optional `CrEntry` field (`core/records.py`), `left_to: str | None`, holds
  the destination folder (`6-trash`, `1-inbox` or `2-backlog/P<n>`).
  - It is set when the order is recorded, for a live CR too (whose folder only moves at `cancel`,
    section 3).
  - The CR's status becomes `cancelled` for every destination. So every path that reads "merged or
    cancelled" keeps working: the batch's end, `close`, the hub, `ensure_unclaimed` and the board.
- **A held CR** (answer 7): the drop unsets `held`, the field the neighbour CR-394 (batch-29, `order
  hold`) adds, the same way `order unhold` does (`unset("held")`). A held CR's PR is already a draft
  on the default branch, so its drop needs no `take stack`. The order is `applied`, unless the CR is
  live. The CLI's output says so: `<cr> was held: no stack driver needed`. This part reads CR-394's
  field: see "Dependencies".
- **A second drop:**
  - Of a CR already cancelled: still refused (exit 2), whatever the destination.
  - Of a live CR not yet cancelled: it replaces the destination, and the record and the new order
    line carry the later word.
- **A merged CR:** its refusal stays.
- **A trash drop outside a stack** (the batch's mode is not `stack`) of a CR that has a PR (answer
  3):
  - The order's line ends with `; close its PR <link>`, e.g. `[chief-of-staff→foreman] order O-1:
    drop CR-103 6-trash; close its PR https://github.com/o/r/pull/346`.
  - In direct mode `order drop` prints the same clause in its own output.
  - For a live CR, `cancel` prints it again (section 3).
  - The CLI runs no forge command itself.
  - In a stack the stack driver closes it (section 6), and the line has no clause.

### 2. CLI: the folder moves to its destination, its number reserved

`lifecycle/stages.py` (`trash_cr`, and a new sibling for the other destinations), used by `_drop`
(a CR that is not live) and by `cancel` (`commands/release.py`, a live CR).

- **trash:** unchanged. The folder goes to `6-trash/<YYMMDD-HHMM>-<number>-<slug>/`, and `restore`
  works on it as before.
- **inbox / backlog `P<n>`:** the folder goes to `1-inbox/<number>-<slug>/` or
  `2-backlog/P<n>/<number>-<slug>/`, its batch name (`381-<slug>`) with no date. It moves whole:
  `work/`, `evidence/` and the STATUS files go with it. Then:
  - **`formerly.json`** in the folder records where the CR came from: `{"cr": "CR-381", "batch":
    "batch-28", "branch": "<branch>", "worktree": "<path>", "pr": "<link or null>", "pr_draft":
    <true|false|null>}`. This CR only writes it. The come-back CR reads it and deletes it.
  - **The `formerly` line:** `formerly CR-381 of batch-28` is appended to `01-intent.md` (or to
    `notes.md` when there is no `01-intent.md`), for a person reading the folder.
  - **The number is reserved:** it is written to `restored.json` (the max that `next_cr_number`
    reads, `core/batch.py`). So no other CR ever gets it, after the batch's close too.
  - **Validation:** `formerly.json` joins the CR folder's layout. Add it to
    `lifecycle/layout_check.py` `CR_FILES` and to concepts.md's "Change Request" tree, so
    `validate` reports no gap for it.
  - **STATUS files and dashboard:** while the batch is open, `write_batch` keeps rewriting the CR's
    STATUS files where they now are, as it does for any CR "wherever they are". The dashboard
    (`write_dashboard`) shows the item in its new stage, as after a `triage`.
- **A name already taken:** the destination already holds that name, by the same test as
  `restore`'s `_check_free` (a folder of that name in `1-inbox`, `2-backlog/P1..P4` or `3-ready`,
  or a CR of the open batch with that slug).
  - The drop is refused with exit 2 before anything changes, naming the folder in the way.
  - A live CR is checked when the order is recorded, and again at `cancel` before the move.
- **The command's output names the destination:** `dropped CR-103 to 2-backlog/P2: <folder>`, or
  `cancelled CR-103 to 1-inbox; stopped …`. A trash drop keeps today's words.
- **`3-ready` is not a destination:** a factory batch would take the CR again on its own.

### 3. CLI: `cancel` follows the destination of the drop

`commands/release.py` (`cancel`), `declare/release.py`.

- **The move:** `cancel <cr> --epoch <n>` moves the folder to the CR's `left_to` (section 2),
  instead of always to `6-trash`.
- **No destination recorded** (no `order drop` before it): refused with exit 2 and nothing changes.
  The message: `cancel <cr>: no destination recorded; the Chief of Staff's "order drop <cr> --note
  trash|inbox|P1..P4" names it`. `cancel` takes no destination of its own.
- **Already cancelled:** `cancel` of a CR already cancelled keeps today's behaviour. Its `left_to`
  is there.
- **The PR clause:** a trash, outside a stack, with a PR, prints `close its PR <link>`.
- **The rest is unchanged:** it stops the gate and the processes, and the batch's end follows.

### 4. CLI: `close`, the batch's record and the final pages

`commands/closing.py` (`_to_remove`, `_closing`), `history.py` (`cr_entry`, `archive_of`),
`status/write.py` (`write_final_pages`).

- **`close`'s removal line** lists only the worktrees and branches of the CRs whose `left_to` is
  `6-trash`.
- **A line of its own for the CRs moved to the inbox or the backlog,** which is not a removal:
  `kept, moved out with their work: CR-381 (2-backlog/P2/381-<slug>) worktree <path> branch
  <branch> PR <link or none>; …` (or `none`). Nothing on it is removed. The folder is the recorded
  `path`; when that path no longer exists (triaged or added again since), it reads `(moved since
  from 2-backlog/P2)` (answer 9).
- **In `batch-NN.json`** (`history.py`), the entry of a CR moved to the inbox or the backlog has
  `"archive": null` and `"to": "<left_to>"`. A trashed CR keeps its archive path, with `"to":
  "6-trash"`, and a merged CR has no `to`. The result stays `dropped` for every cancelled CR.
- **`write_final_pages`** skips a CR whose `left_to` is `1-inbox` or `2-backlog/P<n>`. No STATUS
  file saying the cost is final is written into an inbox or backlog folder.
- **The end-of-batch cleanup** (`endpause.py`, merged CRs only): unchanged.

### 5. CLI: status words, the forge stack, the allow rules

- **The label** (`status/words.py`, `label`): a cancelled CR reads `⚪ dropped` when it went to the
  trash (today's word). Otherwise it reads `⚪ dropped to 1-inbox` or `⚪ dropped to 2-backlog/P<n>`.
  It is in STATUS.md, STATUS.json and `status`.
  - **It changes what the CR board pane draws,** so AGENTS.md's pane rule applies: one screenshot
    of the pane from a real Claude Code session at the PR's head, captioned with the head's SHA
    (seven characters), in the PR's Deliverables. Until it is there, the PR's Known gaps names "no
    screenshot of the pane from a real session".
- **The forge stack** (`commands/forge_stack.py`, `forge_stack_gh.py`, `forge_stack_gitlab.py`;
  answers 3 and 7):
  - **Reading the record:** `_plan` returns, beside the trashed PRs (`_dropped`, now only
    cancelled CRs with `left_to` `6-trash` or no `left_to`), the moved-out PRs. Those are cancelled
    CRs with a PR and a `left_to` of `1-inbox` or `2-backlog/P<n>`, number to (CR id, destination).
    A held CR dropped to the backlog is a moved-out PR like any other.
  - **The messages:** `held_outside` and check 2 name a moved-out PR apart, e.g. `it also held #346
    of CR-381, moved to 2-backlog/P2: left out, on main`. A moved-out PR is never "foreign" and
    never "close it". Trashed PRs keep `…, dropped: close it`.
  - **The retarget:** `_rebuild` and `_create`, after the unstack and before the create, retarget
    each moved-out PR whose base is not the default branch to the default branch. They use the same
    `retarget` call as the neighbour CR-394's held PRs, one line per PR: `#346 base <old> -> main
    (moved to 2-backlog/P2)`. On GitLab, the same retarget of the MR.
  - **Never stacked:** a moved-out PR is never in the stack created.
  - **No retarget by hand:** the cards' rule "never retarget a PR by hand" stays true. The PR moves
    to the default branch only through `forge-stack`.
- **The allow rules** (`commands/permissions.py`, `SAMPLES`, group `batch`; answer 4): add `gh pr
  close 12` → `gh pr close*`, `gh pr reopen 12` → `gh pr reopen*`, `glab mr close 12` → `glab mr
  close*`, and `glab mr reopen 12` → `glab mr reopen*`. They then appear in preflight's P10 and in
  `RECOMMENDED_ALLOW`.
- **The event log:** `b.log` of the drop and of `cancel` carries `to=`.

### 6. Cards

Both hosts read the same cards. The agent files (`agents/`, `com.github.copilot/agents/`) do not
change.

- **`skills/chantier/references/chief-of-staff.md`:**
  - **Steering block:** `order drop CR-104 --note trash|inbox|P1..P4   # where it goes, with its
    work; a release or fix CR: trash only`.
  - **The question** (a new rule beside it): the user's word that takes a CR out of a batch
    ("drop", "take it out", "postpone", "remove from the batch") names where it goes.
    - When it does not, ask once, in the user's language, before the order: trash (cancelled),
      inbox (to look at again), or backlog P1..P4 (postponed or handed off; the usual case for
      delegated work).
    - Never choose for the user.
    - A word that already says it needs no question ("cancel it" → trash; "postpone it, P2" →
      `P2`).
    - A word that only keeps a ready CR out of the stack is CR-394's `order hold`, not a drop.
  - **Direct mode:** a drop line ending `close its PR <link>` is yours. Close it (`gh pr close
    <n>`, `glab mr close <n>`, no `--delete-branch`, no comment), then mark the order done.
  - **"Dropping a CR from a stack":** what to tell the user depends on the destination.
    - Trash: as today (its PR is closed).
    - Inbox or backlog: its commits come out of the PRs above it, and its PR goes to draft and onto
      the default branch, by the rebuild. Its branch and worktree stay and are not offered for
      removal at `close`. The folder is at `<destination>/<number>-<slug>` and keeps its number.
    - A held CR: nothing to rebuild.
  - **Table D** (close while something runs): "drop it (`order drop <cr> --note …`, with the
    destination the user names)".
  - **The `close` offer:** show the `kept, moved out with their work` line and remove nothing on
    it.
  - **The restart line** (today lines 1545-1546, answer 2). Replace "stop orphan processes with
    `$CHANTIER cancel`" with: a relaunched CR's stale long gate is stopped with `$CHANTIER gate
    <cr> --stop` by its new Driver. `cancel` follows only a drop the user ordered (`order drop <cr>
    --note …`): never use it to stop processes of a CR that goes on.
- **`skills/chantier/references/foreman.md`:**
  - **Cancelling a dropped live CR:** `cancel` moves it to the destination its drop order recorded,
    and the Foreman never chooses one. A `cancel` refused for a missing destination goes up to the
    Chief of Staff as an ask.
  - **Closing the PR, a named exception** to "never … edit a PR": a drop order whose line ends
    `close its PR <link>` (a trash drop outside a stack; after `cancel` for a live CR) is closed by
    the Foreman (`gh pr close <n>`, `glab mr close <n>`, no `--delete-branch`, no comment) before
    `order done`.
  - **"A drop in the stack":** the note carries the destination: `drop: <cr> to <destination>`. A
    held CR's drop needs no `take stack`: `order done` at once.
- **`skills/chantier/references/driver.md`, stack driver, "Removing a dropped CR":**
  - Steps 1 to 4 apply to every destination. The `forge-stack rebuild` of step 4 now retargets a
    moved-out PR on the default branch itself.
  - Step 5 (close the PR) applies to a trashed CR only.
  - For a CR moved to the inbox or the backlog, step 5 becomes: turn its PR to a draft (`gh pr
    ready --undo`, `glab mr update --draft`). No close, no comment, no rebase of its branch, no
    retarget by hand.
  - A `drop: <cr>` note with no destination (an older Foreman) means trash.
- **`skills/chantier/references/concepts.md`:**
  - **Lifecycle:** "`6-trash/…` (dropped, with its work …)" becomes "or, on `order drop`,
    `6-trash/…` (cancelled), or `1-inbox/<number>-<slug>/` or `2-backlog/P<n>/<number>-<slug>/`
    (taken out of the batch, keeping its number, with `formerly.json`), always with its work; a
    release or fix CR leaves only to the trash".
  - **The "Change Request" tree:** `formerly.json` (where a CR taken out of a batch came from).
  - **The stack bullet "A CR dropped from the stack":** its PR is closed when it goes to the trash.
    Otherwise it goes to draft and the rebuild puts it on the default branch.

### 7. Docs

The lines that say `order drop` sends a CR to `6-trash/` now name the three destinations:
`docs/planning-folder.md` (the tree and its text), `docs/cr-folder-lifecycle-texts.md`,
`docs/cr-lifecycle-texts.md`, `docs/cr-lifecycle-simple-texts.md`, and the matching text label in
their SVGs (`cr-folder-lifecycle.svg`, `cr-lifecycle.svg`, `cr-lifecycle-simple.svg`). The new
text: "order drop → 6-trash/, 1-inbox/ or 2-backlog/Pn/, with its work". No other drawing change.

## Dependencies

The held part (section 1, "A held CR"; foreman.md's "no `take stack`") reads and unsets CR-394's
`held` field (`4-batch/1-pending/394-retro-batch-28-hold-a-ready-cr-out-of-th`, batch-29). This CR
therefore lands after CR-394: a real dependency, which `order after` records when it joins
batch-29. The retarget of section 5 reuses the `retarget` path that CR-394 extends for its held
PRs.

## Decisions carried from 02-answers.md

| Decision | Where |
| --- | --- |
| 1 (and intent): the destination is asked, trash, inbox or backlog; backlog for delegated, trash for cancelled | sections 1, 6 |
| Intent: the work is kept; the PR closed only for the trash | sections 2, 4, 5, 6 |
| Spec q.1: the number kept and never given again; the come-back part is in the new CR (10) | section 2 |
| Spec q.2: branch and PR picked up when it comes back | the new CR (10) |
| Spec q.3: a trash drop outside a stack, the steering session closes the PR, prompted by the drop's line; no CLI forge write | sections 1, 3, 6 |
| Spec q.4 and 3: a moved-out PR goes to draft (stack driver) and onto the default branch (`forge-stack rebuild` from the record); no retarget by hand | sections 5, 6 |
| 10: split; `formerly.json` written here, with `pr_draft` | section 2, Goal |
| 1: the route for a moved-out PR merged later: in the new CR, because only there do `order add` and `order merged` record it under its own number and PR | the new CR |
| 2: call sites listed; the restart line rewritten | Evidence, section 6 |
| 4: close and reopen in the allow rules | section 5 |
| 5: release and fix CRs, trash only | section 1 |
| 6, 8: the reopen's fields; reopening a closed PR | the new CR |
| 7: `held` cleared at the drop; no `take stack`; `_dropped` reads `left_to` | sections 1, 5, 6 |
| 9: `archive` null with `to`; "moved since"; no final pages in the backlog | section 4 |

## Out of scope

- **Holding a CR in the batch but out of the stack** (`order hold`/`unhold`, a ready CR kept apart
  from `stack` and `forge-stack rebuild` until the user puts it back): the neighbour CR-394
  (`retro-batch-28-hold-a-ready-cr-out-of-th`). This CR takes a CR **out of the batch** and decides
  where its folder goes. It adds no hold. It only clears `held` at the drop and shares the
  retarget path.
- **Coming back:** the same number at `add_cr`, the same branch and PR, the same-batch reopen and
  its field reset, consuming `formerly.json`, the Driver's pick-up and reopen of a PR, and the route
  for a PR the user merges later. All of it is in `1-inbox/order-drop-come-back-same-number-branch-pr`.
  Until that CR lands, a moved-out folder that joins a batch gets a new number, as any folder does
  today.
- **`3-ready` as a destination.**
- **Series and parallel batches:** a moved-out PR there is left as it is.
- **Recording a later merge** of a moved-out CR's PR by the hub or the board (the CR is
  `cancelled`).
- **Removing later** the worktree and branch of a CR moved out.
- **Unchanged commands:** `restore`, `triage`, `abandon`.
- **The web board:** it shows the new label through STATUS.json.

## Evidence

No host or default/configured dependency, so no matrix.

**Tests** (`skills/chantier/scripts/cli/tests/`, in-process, few and parametrized; keep `just test`
within its budget):

- **Refusals** (`test_rail_refusals.py`):
  - `order drop <cr>` with no `--note`, and with `--note P5`, `ready` and `3-ready`: each exits 1
    and leaves `batch.json` byte for byte unchanged.
  - A release CR and a fix CR dropped with `--note P2`: each exits 2, unchanged; with `--note
    trash`, accepted.
  - `cancel <cr> --epoch 1` on a live CR with no drop order: exits 2 and moves nothing.
  - The existing `cancel <cr>` without `--epoch` (line 136): unchanged, still the epoch refusal.
- **Each destination** (`test_batch_end.py`): parametrize the `drop` and `cancel` cases (line 59)
  over `trash`, `inbox` and `P2`.
  - For each:
    - the folder lands in `6-trash/<stamp>-<n>-<slug>`, `1-inbox/<n>-<slug>` or
      `2-backlog/P2/<n>-<slug>`;
    - `status` is `cancelled` and `left_to` is that folder;
    - the worktree and branch still exist;
    - the batch still pauses when this was its last CR.
  - For inbox and P2 also:
    - `formerly.json` holds `cr`, `batch`, `branch`, `worktree`, `pr` and `pr_draft`;
    - `01-intent.md` ends with the `formerly` line;
    - `restored.json` holds `<n>`, and an item opened after it gets a number above `<n>`.
- **A clash:** with `2-backlog/P2/<n>-<slug>` already there, `order drop <cr> --note P2` exits 2
  and moves nothing. For a live CR it is refused at the order.
- **The PR clause:** a trash drop of a CR with a PR in a parallel batch: the order line ends with `;
  close its PR <link>`. The same in a stack batch: no clause. A drop to P2: no clause.
- **`close`** (no `--yes`), with one CR trashed and one moved to P2:
  - The removal line names only the trashed one.
  - The `kept, moved out with their work` line names the other with its folder, worktree, branch
    and PR. Once that folder is triaged elsewhere, it reads `moved since from 2-backlog/P2`.
  - With `--yes`: in `batch-NN.json`, the moved CR has `archive: null, to: 2-backlog/P2` and the
    trashed one has `to: 6-trash`, and no final-cost STATUS file is written into the backlog folder.
- **The labels** (`test_stack_label.py` or the label's test): `⚪ dropped` and `⚪ dropped to
  2-backlog/P2`, from a real drop, never from a hand-built record.
- **The forge stack** (`test_board_prs.py`'s `forge_world.py` fixture or the forge-stack tests), one
  trashed and one moved CR with PRs in the stack:
  - `rebuild` prints `dropped: close it` for the first, and for the second `moved to 2-backlog/P2:
    left out, on main` and a retarget line `#n base <old> -> main (moved to 2-backlog/P2)`;
  - the moved PR is not in the created stack;
  - check 2 does not call it foreign;
  - GitLab: the same retarget.
- **A held CR dropped to P2:** `held` is unset, the output says `no stack driver needed`, the order
  is applied, and `forge-stack` names its PR `moved to …`. This test lands with or after CR-394's
  field.
- **The allow rules** (`test_cli_units.py` or the permissions test): the four new patterns are in
  `RECOMMENDED_ALLOW` and in P10's block, for GitHub and GitLab.
- **`validate`** (`test_validate.py`): a folder holding `formerly.json` gives no gap.
- **Bare call sites, updated** (each gains `--note trash`, or an `order drop <cr> --note trash`
  before a bare `cancel`):
  - `test_batch_end.py`: 73, 74, 140, 225;
  - `test_factory.py`: 143.
  - `test_board_times.py` 75 and 84 build events only: unchanged.

**Scenario** (`scenario/run_scenario.py`):

- **Bare `order drop` calls**, each gains `--note trash` unless a check below moves it elsewhere:
  1089, 1957, 1958, 2791, 7207, 7212, 7218, 7222, 7292, 7310, 7339, 7478 (a fix CR: trash), 7736,
  8220.
- **Bare `cancel` calls with no drop before them**, each preceded by `order drop <cr> --note trash`:
  2644, 3485, 4030, 4129, 4490, 4670, 5605 (both), 7685.
  - 626 (the fake Foreman, after a drop order) and 1174 (a CR already cancelled) keep their
    `cancel` as it is.
- **Step 5:** `order drop CR-103 --note trash` keeps every existing check (the trash path under the
  date, `⚪ dropped` in its STATUS.md). The order line now carries `6-trash`.
- **A move to the backlog,** at 2791: the CR added to the running direct batch is dropped with
  `--note P3`:
  - it lands in `2-backlog/P3/<n>-<slug>` with `formerly.json`;
  - its STATUS.md says `⚪ dropped to 2-backlog/P3`;
  - the next CR added gets a number above `<n>`.
- **`close`** (near 3793): the trashed CR's line still names its worktree and branch.

Each check reads the shipped cards and CLI at the head under test.

**Gates:**

- `just check`;
- `just eval-dry-run` (a CLI `src/` change);
- `just scenario (ubuntu-latest)` green at the PR's head;
- the pane screenshot of section 5 in Deliverables, or its Known gap named.
