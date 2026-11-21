# A CR taken out of a batch can go to the next batch

`order drop` gains the destination `ready`: the CR's folder goes to `3-ready/`, the next batch,
with its number, its work and its open waits, as the inbox and the backlog do today. A started
CR (one a Driver has had) taken out of the batch goes to the backlog (P1 to P4), the next batch
or the trash, never the inbox. Its branch, worktree and PR stay, the PR as a draft; only the
trash closes its PR, as today.

## Goal, in the user's terms

From park-live-cr's grill (park-live-Q1): when the user takes a CR out of the batch, "it depends
on what the user asks": back to the backlog, to the trash, or to ready for the next batch, and
never to the inbox. CR-415 of batch-29 was dropped to P2 with its work because no "next batch"
destination existed. With factory-redefine, `3-ready` always means the next batch
(park-live-Q5/Q8), so a drop to `ready` never joins the running batch by itself.

## Decisions carried

| Answer (park-live-cr/02-answers.md) | Decision | Section |
| --- | --- | --- |
| park-live-Q1 | A CR taken out of the batch goes where the user says: the backlog, the trash or ready (the next batch), never the inbox. | 1, 2 |
| park-live-Q5, Q8 | No new folder: `3-ready` always means the next batch, `4-batch/1-pending/` the running one (factory-redefine's work, on which this CR depends). | 1; Out of scope |
| Fable 3 (accepted at park-live-Q11) | A CR taken out keeps its branch and PR, as a draft, for the backlog or the next batch; the trash closes its PR. | 3 |
| Fable 5 (accepted at park-live-Q11) | The "auto mode" caution is moot: `3-ready` is the next batch. | 1 |
| park-live-Q12 (A) | This CR ships apart: the `ready` destination and the destinations of a started CR. It does not wait for park-live-cr or hold-live-cr. | (this file) |
| park-live-Q13 (B) | P3 and P4 are allowed too: a started CR goes to any backlog row, the next batch or the trash; never the inbox. | 2 |
| park-live-Q14 (A) | Dragging a CR out of the running batch on the board: not now (an idea, no CR). | Out of scope |
| Critic fix 3 (destinations part) | `3-ready` is added to the drop destinations in `driver.md` and `foreman.md`. | 4 |

## Words

- **Started CR:** a CR that a `take` has handed to a Driver at least once. In the record: its
  status is `working`, `ready` or `blocked`, or it has `round > 0`, or a PR or a `head` recorded
  (a CR that came back to a batch with its former PR, `came_back.py`, is started though queued).
  A queued CR never taken is not started.

## What changes

The CLI lives in `skills/chantier/scripts/cli/src/chantier/`, the cards in
`skills/chantier/references/`.

### 1. The destination `ready`

`order drop <cr> --note ready` sends the CR to `3-ready/<number>-<slug>/`, exactly as a drop to
the inbox or the backlog does: the folder moves whole with its work, without a date, with
`formerly.json` (cr, batch, branch, worktree, PR, draft state), its open waits in `waits.json`,
the `formerly CR-<n> of batch-<m>` line in its note, and its number reserved. A drop of a live
(`working`) CR records the destination and `cancel` moves it, as today.

- `commands/orders.py`: `_DROP_FOLDERS` gets `"ready": "3-ready"`; `DROP_USAGE` reads
  `order drop <cr> --note trash|ready|P1..P4|inbox: where the CR goes (a started CR: never the
  inbox); ask the user when they have not said it`.
- `declare/orders.py`: the `order` help reads `drop (--note trash|ready|P1..P4|inbox)`.
- `lifecycle/moveout.py`, `move_out_cr`: the target is `paths["ready"]` for `3-ready`,
  `paths["inbox"]` for `1-inbox`, the backlog row otherwise. Docstrings of the module,
  `move_out_cr`, `check_drop_free` and `leave_batch` name `3-ready`. `check_drop_free` already
  tests the name in `3-ready` (`folder_taken`).
- `core/records.py`: the comments on `left_to` and `moved_to` name `3-ready`. `moved_to` already
  returns any non-trash `left_to`, so `status` (`⚪ dropped to 3-ready`), `history.py`, `close`'s
  kept list (`_kept`: worktree, branch and PR not offered for removal) and
  `forge_stack_apart.py` (`moved to 3-ready: left out, on main`) follow with no code change;
  the tests check it.
- `commands/release.py`, `cancel`'s refusal with no destination names
  `"order drop <cr> --note trash|ready|P1..P4"`.
- The way back is today's: `open`, or `order add --note 3-ready/<number>-<slug>` (after
  factory-redefine, the way an automatable `3-ready` CR joins the running batch), reads
  `formerly.json` (`commands/joining.py`, `came_back.py`): the CR keeps its number, and its
  branch and PR while the branch exists. No change there.
- **Dependency on factory-redefine.** Today, `triage --ready` and the factory batch make a
  `3-ready` CR join the running batch. After factory-redefine, nothing joins from `3-ready` by
  itself, so a CR dropped to `ready` waits for the next batch. This CR is built on top of
  factory-redefine (`depends.json`: `after: factory-redefine`).

### 2. A started CR never goes to the inbox

`commands/orders_drop.py`, `drop`, before anything changes (next to the release/fix refusal):
`order drop <cr> --note inbox` of a started CR (Words) is refused, exit precondition, nothing
written and no order recorded:

```
<cr> has started: it goes to the backlog (P1..P4), the next batch (ready) or the trash, never the inbox
```

P1 to P4, `ready` and `trash` stay accepted for it (park-live-Q13). The inbox stays accepted for a
CR not started (a queued CR never taken, as the direct-mode scenario drops today). A release or a
fix CR still goes only to the trash (today's refusal, checked first). The test of "started" is
one helper, `has_started(c: CrEntry) -> bool`, in `orders_drop.py`.

### 3. The branch and the PR (Fable 3)

- **The trash:** unchanged. Outside a stack the order line (and `cancel`'s, for a live CR) ends
  `; close its PR <link>`; in a stack the stack driver closes it.
- **The backlog or `ready`:** the branch, worktree and PR stay, the PR as a draft.
  - In a stack: unchanged, the stack driver's "Removing a dropped CR" turns it to a draft and the
    rebuild retargets it onto the default branch.
  - Outside a stack, when the record says the PR is out of draft (`pr_draft is False`), the order
    line ends `; turn its PR to draft <link>` (and so does `cancel`'s line, for a live CR). In
    `lifecycle/moveout.py`, `close_pr_clause` becomes `pr_clause(batch, cr)`, which returns the
    close clause for the trash, the draft clause for any other destination of a CR whose PR is
    out of draft, and `""` otherwise (in a stack, with no PR, or with the draft state not
    out of draft). Its callers (`orders_drop.py`, `release.py`'s `cancel`) take the new name; in
    direct mode `drop` prints the clause as its own line, as it does for the close clause.
  - `formerly.json` records `"pr_draft": null` (not read) when the draft clause was printed, so
    that a CR coming back does not hold a stale "out of draft"; the next Driver reads the forge.
    Otherwise it records `pr_draft` as today.
  - Who turns it: the Foreman (`gh pr ready <n> --undo`, `glab mr update <n> --draft`, no
    comment) before the order's `order done`, after `cancel` for a live CR; in direct mode the
    Chief of Staff. This is a second named exception in `foreman.md`'s "Never ... edit a PR".

### 4. Cards

- **`chief-of-staff.md`, "Where a dropped CR goes":** the choices become the trash (cancelled),
  the next batch (`ready`, `3-ready`), the backlog P1..P4 (postponed or handed off), or, for a CR
  not started only, the inbox (to look at again). A CR that has started (a Driver has had it) is
  never offered the inbox. "Only the trash closes its PR" stays; add that the backlog and the
  next batch keep it as a draft, and that a drop line ending `turn its PR to draft <link>` is the
  Foreman's in Foreman mode and yours in direct mode (`gh pr ready <n> --undo`, `glab mr update
  <n> --draft`), then `order done`. The command block's line becomes
  `$CHANTIER order drop CR-104 --note trash|ready|P1..P4|inbox   # where it goes, with its work; a started CR: never the inbox; a release or fix CR: trash only`.
- **`chief-of-staff.md`, "Dropping a CR from a stack":** "Inbox or backlog" becomes "Backlog,
  next batch (`3-ready`) or, for a CR not started, inbox".
- **`chief-of-staff.md`**, the held-CR bullet and table row D: the `order drop` they name keeps
  "with the destination the user names"; no other change.
- **`foreman.md`:** "A drop in the stack" lists `6-trash`, `3-ready`, `1-inbox` or
  `2-backlog/P<n>`; the "Never ... edit a PR" exception gets the draft clause next to the close
  clause (section 3); the "Orders are the user's word" bullet's `cancel` keeps "you never choose
  one".
- **`driver.md`, "Removing a dropped CR":** the destination list adds `3-ready`; step 5 reads "For
  a CR moved to the inbox, the backlog or the next batch (`3-ready`), turn its PR to a draft".
- **`concepts.md`:** the planning tree's `formerly.json` line and the CR lifecycle paragraph (line
  ~189) add `3-ready/<number>-<slug>/` as a drop destination, and say a started CR never goes to
  the inbox.

The Copilot and Claude Code agent files are not touched (the contract is in the cards).

### 5. Docs

Where they list the drop's destinations (`6-trash/, 1-inbox/ or 2-backlog/Pn/`), add `3-ready/`
(the next batch), and say a started CR never goes to the inbox, each text file kept in step with
its SVG:

- `docs/cr-folder-lifecycle-texts.md` and `docs/cr-folder-lifecycle.svg` (description and the
  `order drop →` label);
- `docs/cr-lifecycle-simple-texts.md` and `docs/cr-lifecycle-simple.svg`;
- `docs/cr-lifecycle-texts.md` and `docs/cr-lifecycle.svg`;
- `docs/planning-folder.md` (the `order drop` paragraph);
- `scenario/README.md` (the new checks, Evidence).

## Out of scope

- park-live-cr (the Foreman parks a stuck CR; `close` and the release refused while one is
  blocked) and hold-live-cr (`order hold` of a live CR): separate CRs (park-live-Q12). This CR
  neither waits for nor changes them; their texts that list drop destinations follow this one
  when they land.
- factory-redefine (the two ready meanings, the factory mode's redefinition), on which this CR
  depends; the board's "running batch" / "next batch" lane (`board-running-batch-lane`).
- Dragging a CR out of the running batch on the board (park-live-Q14: not now, an idea, no CR).
- The drop of a CR not started: unchanged, the inbox stays allowed for it.
- The board, the web and terminal clients, `hooks/register.tsx` and the `STATUS.json` fields: no
  change (`dropped to 3-ready` comes from the existing `moved_to` text). No pane screenshot is
  owed, no `just mod`.

## Evidence

Every check runs the CLI's real commands on states the CLI built (`open`, `take`, `ship`,
`handback`, `order`), in-process; the card checks read the shipped cards from the repository at
the head under test.

**Tests** (`skills/chantier/scripts/cli/tests/`, few and parametrized, `just test` within its
limit), extending `test_order_drop_to.py` (its `FOLDERS` map gains `"ready": "3-ready"`) and
`test_came_back.py`:

- `order drop <cr> --note ready` of a ready CR with a PR: the folder lands in
  `3-ready/<number>-<slug>/` with its work, `formerly.json` and its open waits (`waits.json`);
  `left_to == "3-ready"`; STATUS.md says `dropped to 3-ready`; `close`'s kept list names its
  worktree, branch and PR.
- The same for a live CR: the order records `3-ready`, `cancel` moves it there.
- A drop to `ready` whose name is already in `3-ready` is refused at the order (exit
  precondition), as for the inbox.
- **Started CRs and the inbox** (parametrized over a working, a ready, a blocked CR, and a queued
  CR that came back with a PR): `--note inbox` is refused, exit precondition, with the new text,
  nothing moved and no order recorded; `P1`, `P4`, `ready` and `trash` are accepted. A queued CR
  never taken is still accepted to the inbox.
- A release or fix CR to `ready` is refused with today's text.
- **The PR clause:** outside a stack, a ready CR with `pr_draft` False dropped to `P2` or `ready`
  gets `; turn its PR to draft <link>` on the order line, and its `formerly.json` holds
  `"pr_draft": null`; with `pr_draft` True, or in a stack, no clause; the trash still gets
  `close its PR`. A live CR's `cancel` line carries the draft clause.
- `order add --note 3-ready/<number>-<slug>` in the same batch brings it back under its number,
  as the same entry, with its branch and PR (`test_came_back.py`).
- **The cards:** `chief-of-staff.md`, `foreman.md` and `driver.md` name `3-ready` among the drop
  destinations, and `chief-of-staff.md` says a started CR never goes to the inbox; added to the
  existing card-content test that reads these files, not a new file.

**Scenario** (`scenario/run_scenario.py`, `direct_batch`, unit as today): after the CR that came
back by `order add`, and before its drop to the trash, drop it to `ready`: it lands in
`3-ready/<number>-<slug>/` with `formerly.json` and `⚪ dropped to 3-ready` in its STATUS.md; then
`order add --note <that folder>` brings it back under its number. Then the drop to the trash, as
today. Update `scenario/README.md` (the line on the CR dropped to the backlog P3).

**Gates:**

- `just check` in the worktree, at the rebased head pushed.
- `just eval-dry-run` (the change is under the CLI's `src/`).
- The pipeline's `just scenario (ubuntu-latest)` job green at the PR's head (CLI, cards and
  scenario change).
- Windows coverage by `chantier gate` per AGENTS.md, when this CR is on top of its batch's stack.

**No host and default matrix:** the behaviour depends neither on the host nor on a configured
value.

## Open questions

1. **The inbox for a CR not started.** park-live-Q1 and Q13 speak of a CR taken out after it
   started. This specification keeps the inbox allowed for a queued CR never taken (as the
   direct-mode scenario drops one today) and refuses it for a started CR only (Words). Should the
   inbox be refused for every drop out of a batch instead?
