# A CR taken out of a batch goes to the backlog, ready or the trash

`order drop` gains the destination `ready`: the CR's folder goes to `3-ready/`, the next batch,
with its number, its work and its open waits, as the backlog does today. It loses the inbox: no CR
taken out of a batch goes to the inbox, started or not; `--note inbox` is refused for every drop.
The destinations are P1 to P4, `ready` and the trash, on the user's word. Later, `triage` and the
board move the folder freely. Its branch, worktree and PR stay, the PR as a draft; only the trash
closes its PR, as today.

## Goal, in the user's terms

From park-live-cr's grill (park-live-Q1): when the user takes a CR out of the batch, "it depends
on what the user asks": back to the backlog, to the trash, or to ready for the next batch, and
never to the inbox. The user's last word (02-answers.md entry 3): "Il n'y a pas de raison de
mettre en inbox quand on a déjà planifié une CR, qu'elle ait été prise par un Driver ou non." So
one simple rule, with no "started" test. CR-415 of batch-29 was dropped to P2 with its work
because no "next batch" destination existed. With factory-redefine, `3-ready` always means the
next batch (park-live-Q5/Q8), so a drop to `ready` never joins the running batch by itself.

## Decisions carried

| Answer | Decision | Section |
| --- | --- | --- |
| park-live-Q1 | A CR taken out of the batch goes where the user says: the backlog, the trash or ready (the next batch), never the inbox. | 1, 2 |
| park-live-Q5, Q8 | No new folder: `3-ready` always means the next batch, `4-batch/1-pending/` the running one (factory-redefine's work, on which this CR depends). | 1; Out of scope |
| Fable 3 (accepted at park-live-Q11) | A CR taken out keeps its branch and PR, as a draft, for the backlog or the next batch; the trash closes its PR. | 3 |
| Fable 5 (accepted at park-live-Q11) | The "auto mode" caution is moot: `3-ready` is the next batch. | 1 |
| park-live-Q12 (A) | This CR ships apart: the `ready` destination and the drop's destinations. It does not wait for park-live-cr or hold-live-cr. | (this file) |
| park-live-Q13 (B) | P3 and P4 are allowed too: any backlog row, the next batch or the trash. | 2 |
| park-live-Q14 (A) | Dragging a CR out of the running batch on the board: not now (an idea, no CR). | Out of scope |
| Critic fix 3 (destinations part) | `3-ready` is added to the drop destinations in `driver.md` and `foreman.md`. | 4 |
| drop-to-next-batch-Q1 (A) | The inbox for a CR never taken: superseded by entry 3. | 2 |
| drop-to-next-batch-Q2 | No "started" rule, no `has_started`; later moves (`triage`, the board) are the user's free choice, the inbox included. Its "inbox at the drop" is superseded by entry 3. | 2 |
| 02-answers.md entry 3 (the user's correction of Q2) | `order drop` never sends a CR to the inbox, started or not: P1-P4, `3-ready`, trash; `--note inbox` refused for every CR. | 1, 2 |

## What changes

The CLI lives in `skills/chantier/scripts/cli/src/chantier/`, the cards in
`skills/chantier/references/`.

### 1. The destination `ready`

`order drop <cr> --note ready` sends the CR to `3-ready/<number>-<slug>/`, exactly as a drop to
the backlog does: the folder moves whole with its work, without a date, with `formerly.json` (cr,
batch, branch, worktree, PR, draft state), its open waits in `waits.json`, the
`formerly CR-<n> of batch-<m>` line in its note, and its number reserved. A drop of a live
(`working`) CR records the destination and `cancel` moves it, as today.

- `commands/orders.py`: `_DROP_FOLDERS` becomes
  `{"trash": TRASH, "ready": "3-ready", "p1".."p4": "2-backlog/P<n>"}` (no `"inbox"`); `DROP_USAGE`
  reads `order drop <cr> --note trash|ready|P1..P4: where the CR goes (ready: the next batch);
  ask the user when they have not said it`.
- `declare/orders.py`: the `order` help (line 19) reads `drop (--note trash|ready|P1..P4)`; the
  `--note` help (line 29) reads `drop: trash, P1..P4 or ready (the next batch, 3-ready), where the
  CR goes (the user's word; never a default)`.
- `lifecycle/moveout.py`, `move_out_cr`: the target is `paths["ready"]` for `3-ready`, the backlog
  row for `2-backlog/P<n>`; its `1-inbox` branch stays only to read a `left_to` recorded before
  this change (a live CR whose drop to the inbox was ordered in a running batch, then moved by
  `cancel`). Docstrings of the module, `move_out_cr`, `check_drop_free` and `leave_batch` name
  `3-ready`. `check_drop_free` already tests the name in `3-ready` (`folder_taken`).
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
  branch and PR while the branch exists. No change there; a folder the user later moved to the
  inbox by `triage` or the board comes back the same way.
- **Dependency on factory-redefine.** Today, `triage --ready` and the factory batch make a
  `3-ready` CR join the running batch. After factory-redefine, nothing joins from `3-ready` by
  itself, so a CR dropped to `ready` waits for the next batch. This CR is built on top of
  factory-redefine (`depends.json`: `after: factory-redefine`).

### 2. The drop never goes to the inbox (entry 3)

`order drop <cr> --note inbox` is refused for every CR (queued or live, taken or never taken,
with or without a PR), in `_drop_folder` (`commands/orders.py`), before anything is written and
before any order is recorded, exit usage (the same code as an unknown destination word), with:

```
order drop never sends a CR to the inbox: P1..P4, ready (the next batch) or trash
```

There is no "started" test and no `has_started` helper. A release or a fix CR still goes only to
the trash (today's refusal in `orders_drop.py`, unchanged; `--note inbox` for it now meets the
inbox refusal first). The name-in-use refusal (`check_drop_free`) applies to `3-ready` and the
backlog rows, as today.

Later moves stay free (drop-to-next-batch-Q2): once the CR's folder is in the backlog or
`3-ready`, `triage` and the board move it, on the user's word, to any folder they move a CR to
today, the inbox included. No code change there.

### 3. The branch and the PR (Fable 3)

- **The trash:** unchanged. Outside a stack the order line (and `cancel`'s, for a live CR) ends
  `; close its PR <link>`; in a stack the stack driver closes it.
- **The backlog or `ready`:** the branch, worktree and PR stay, the PR as a draft.
  - In a stack: unchanged, the stack driver's "Removing a dropped CR" turns it to a draft and the
    rebuild retargets it onto the default branch.
  - Outside a stack, when the record says the PR is out of draft (`pr_draft is False`), the order
    line ends `; turn its PR to draft <link>` (and so does `cancel`'s line, for a live CR). In
    `lifecycle/moveout.py`, `close_pr_clause` becomes `pr_clause(batch, cr)`, which returns the
    close clause for the trash, the draft clause for any other destination of a CR outside a
    stack whose PR is out of draft, and `""` otherwise (in a stack, with no PR, or with the draft
    state not out of draft). Its callers (`orders_drop.py`, `release.py`'s `cancel`) take the new
    name; in direct mode `drop` prints the clause as its own line, as it does for the close
    clause.
  - `formerly.json` records `"pr_draft": null` (not read) for every drop to a destination other
    than the trash whose recorded `pr_draft` is False, inside or outside a stack (in a stack the
    stack driver turns it, outside the order line asks for it), so that a CR coming back does not
    hold a stale "out of draft"; the next Driver reads the forge. Otherwise it records `pr_draft`
    as today.
  - Who turns it: the Foreman (`gh pr ready <n> --undo`, `glab mr update <n> --draft`, no
    comment) before the order's `order done`, after `cancel` for a live CR; in direct mode the
    Chief of Staff. This is a second named exception in `foreman.md`'s "Never ... edit a PR".

### 4. Cards

- **`chief-of-staff.md`, "Where a dropped CR goes" (line ~1069):** the choices become the trash
  (cancelled), the next batch (`ready`, `3-ready`) or the backlog P1..P4 (postponed or handed
  off); the inbox is not one of them, for any CR (a CR already planned has no reason to go back
  to the inbox); a later move of its folder, the inbox included, is `triage` or the board on the
  user's word. "Only the trash closes its PR" stays; add that the backlog and the next batch keep
  it as a draft, and that a drop line ending `turn its PR to draft <link>` is the Foreman's in
  Foreman mode and yours in direct mode (`gh pr ready <n> --undo`, `glab mr update <n> --draft`),
  then `order done`. "A CR moved to the inbox or the backlog keeps its number" (line ~1076)
  becomes "A CR moved to the backlog or the next batch (`3-ready`) keeps its number". The command
  block's line becomes
  `$CHANTIER order drop CR-104 --note trash|ready|P1..P4   # where it goes, with its work; never the inbox; a release or fix CR: trash only`.
- **`chief-of-staff.md`, "Dropping a CR from a stack" (line ~1307):** "Inbox or backlog" becomes
  "Backlog or next batch (`3-ready`)".
- **`chief-of-staff.md`**, lines ~1206 and ~1510 ("dropped to the inbox or the backlog"): become
  "the backlog or the next batch (`3-ready`)".
- **`chief-of-staff.md`**, the held-CR bullet and table row D: the `order drop` they name keeps
  "with the destination the user names"; no other change.
- **`foreman.md`:** line ~220 ("those of a CR moved to the inbox or the backlog stay") becomes
  "the backlog or the next batch (`3-ready`)"; "A drop in the stack" (line ~469) lists `6-trash`,
  `3-ready` or `2-backlog/P<n>`; the "Never ... edit a PR" exception gets the draft clause next to
  the close clause (section 3); the "Orders are the user's word" bullet's `cancel` keeps "you
  never choose one".
- **`driver.md`, "Removing a dropped CR" (line ~1220):** the destination list reads `6-trash`,
  `3-ready` or `2-backlog/P<n>` (a `1-inbox` note from an older Foreman is read as the backlog's
  case: the PR to a draft); step 5 reads "For a CR moved to the backlog or the next batch
  (`3-ready`), turn its PR to a draft".
- **`concepts.md`:** the planning tree's `formerly.json` line and the CR lifecycle paragraph (line
  ~189) name `2-backlog/P<n>/` and `3-ready/<number>-<slug>/` as the drop's non-trash
  destinations, not `1-inbox/`, and say that `order drop` never sends a CR to the inbox.

The Copilot and Claude Code agent files are not touched (the contract is in the cards).

### 5. CLI docstrings

Where a docstring names the drop's destinations as "the inbox or the backlog" (or "trash, inbox or
backlog"), it names "the backlog or the next batch (`3-ready`)" instead: `commands/came_back.py:1`,
`commands/closing.py:176`, `commands/forge_stack.py:54`, `commands/forge_stack_apart.py:35`,
`history.py:35`, `status/write.py:53` (the comment), `commands/release.py:117` (`cancel`),
`commands/orders_drop.py:1` and `:15`, `commands/forge_stack_gh.py:92` (`held_outside`: "those of
CRs moved to the backlog or the next batch (`3-ready`)"); and `declare/orders.py:29` (section 1).

### 6. Docs

Where they list the drop's destinations (`6-trash/, 1-inbox/ or 2-backlog/Pn/`), they become
`6-trash/, 2-backlog/Pn/ or 3-ready/` (the next batch), each text file kept in step with its SVG:

- `docs/cr-folder-lifecycle-texts.md` and `docs/cr-folder-lifecycle.svg` (description and the
  `order drop →` label);
- `docs/cr-lifecycle-simple-texts.md` and `docs/cr-lifecycle-simple.svg`;
- `docs/cr-lifecycle-texts.md` and `docs/cr-lifecycle.svg`;
- `docs/planning-folder.md` (the `order drop` paragraph);
- `evals/SCORECARD.md`, row C16: its parenthesis reads "to `2-backlog/Pn/` or `3-ready/` with
  `P1`..`P4`, `ready`" (no `1-inbox/`, no `inbox`);
- `scenario/README.md` (the new checks, Evidence).

## Out of scope

- park-live-cr (the Foreman parks a stuck CR; `close` and the release refused while one is
  blocked) and hold-live-cr (`order hold` of a live CR): separate CRs (park-live-Q12). This CR
  neither waits for nor changes them; their texts that list drop destinations follow this one
  when they land.
- factory-redefine (the two ready meanings, the factory mode's redefinition), on which this CR
  depends; the board's "running batch" / "next batch" lane (`board-running-batch-lane`).
- Dragging a CR out of the running batch on the board (park-live-Q14: not now, an idea, no CR).
- `triage` and the board's later moves of a dropped CR's folder: unchanged, free, the inbox
  included (Q2).
- The board, the web and terminal clients, `hooks/register.tsx` and the `STATUS.json` fields: no
  change (`dropped to 3-ready` comes from the existing `moved_to` text). No pane screenshot is
  owed, no `just mod`.

## Evidence

Every check runs the CLI's real commands on states the CLI built (`open`, `take`, `ship`,
`handback`, `order`), in-process; the card checks read the shipped cards from the repository at
the head under test.

**Tests** (`skills/chantier/scripts/cli/tests/`, few and parametrized, `just test` within its
limit), changing `test_order_drop_to.py` and extending `test_came_back.py`. The existing inbox
cases change to the new rule:

- The module docstring (line 1) reads `order drop <cr> --note trash|ready|P1..P4`.
- `FOLDERS` (line ~21): `"inbox": "1-inbox"` is replaced by `"ready": "3-ready"`.
- `test_a_drop_with_no_known_destination_is_refused_and_records_nothing` (lines 31-43): `"ready"`
  leaves its refused words (they stay `None`, `P5`, `3-ready`), and it asserts
  `"trash|ready|P1..P4" in err`.
- `test_a_release_or_fix_cr_leaves_the_batch_only_to_the_trash` (line ~47): the case
  `("fix", "inbox", 2)` becomes `("fix", "ready", 2)`, so it still meets the fix refusal.
- `test_a_dropped_cr_goes_where_the_order_names_with_its_work` (line ~70): `dest` over `trash`,
  `ready`, `p2` (no `inbox`), `live` over False/True: a ready CR with a PR dropped to `ready` lands
  in `3-ready/<number>-<slug>/` with its work, `formerly.json` and its open waits (`waits.json`);
  `left_to == "3-ready"`; STATUS.md says `dropped to 3-ready`; `close`'s kept list names its
  worktree, branch and PR; for a live CR the order records `3-ready` and `cancel` moves it there.
- `test_a_drop_to_a_name_in_use_is_refused_at_the_order` (line ~119): parametrized over `p2` and
  `ready`, the name already used in the destination folder; refused at the order (exit
  precondition).
- `test_validate_reads_a_formerly_json_in_a_cr_folder_as_part_of_its_layout` (line ~170): drops
  to `ready` instead of `inbox`.
- **New, the inbox refusal**, parametrized over a queued CR never taken, a `working` CR and a
  `ready` CR with a PR: `order drop <cr> --note inbox` exits usage with the new text, the
  record's bytes unchanged (no order, no `left_to`) and nothing moved.
- **The PR clause:** outside a stack, a ready CR with `pr_draft` False dropped to `P2` or `ready`
  gets `; turn its PR to draft <link>` on the order line, and its `formerly.json` holds
  `"pr_draft": null`; in a stack, no clause on the order line but `formerly.json` still holds
  `"pr_draft": null`; with `pr_draft` True, no clause and `pr_draft` recorded as today; the trash
  still gets `close its PR`. A live CR's `cancel` line carries the draft clause.
- `order add --note 3-ready/<number>-<slug>` in the same batch brings it back under its number,
  as the same entry, with its branch and PR (`test_came_back.py`).
- **The cards:** `chief-of-staff.md`, `foreman.md` and `driver.md` name `3-ready` among the drop
  destinations and do not name `1-inbox` among them, and `chief-of-staff.md` says the drop never
  sends a CR to the inbox; added to the existing card-content test that reads these files, not a
  new file.

**Scenario** (`scenario/run_scenario.py`, `direct_batch`, unit as today; it drops no CR to the
inbox today): after the CR that came back by `order add`, and before its drop to the trash, drop
it to `ready`: it lands in `3-ready/<number>-<slug>/` with `formerly.json` and
`⚪ dropped to 3-ready` in its STATUS.md; then `order add --note <that folder>` brings it back
under its number. Then the drop to the trash, as today. Update `scenario/README.md` (the line on
the CR dropped to the backlog P3, ~129).

**Gates:**

- `just check` in the worktree, at the rebased head pushed.
- `just eval-dry-run` (the change is under the CLI's `src/`).
- The pipeline's `just scenario (ubuntu-latest)` job green at the PR's head (CLI, cards and
  scenario change).
- Windows coverage by `chantier gate` per AGENTS.md, when this CR is on top of its batch's stack.

**No host and default matrix:** the behaviour depends neither on the host nor on a configured
value.

## Open questions

None.
