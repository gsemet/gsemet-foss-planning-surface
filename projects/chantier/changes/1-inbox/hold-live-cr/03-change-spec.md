# `order hold` of a live CR, in every batch mode

The user's `order hold` today takes only a CR handed back ready, in a stack. With this change it
also takes a live (`working`) CR, in every mode (parallel, series, stack). The CR becomes `blocked`
and held. Its lease ends and its slot is free at once. It leaves the stack and the series order.
It stays in the batch, red on the board, until the user's `order unhold` releases it; it then comes
back on top and is taken back before any queued CR. No release starts while a CR is held.

## Goal, in the user's terms

From the batch-29 retro (park-live-cr, kept point 2): CR-415 waited on the user's phone trial with
no Driver at work, yet kept a slot and its place in the stack for five hours, because `order hold`
takes only a ready CR. The user accepted the Fable advisor's choice 2 (park-live-Q11, all choices):
"`order hold` is accepted on a live CR, same effect, released by the user only". At park-live-Q12
the user split the work in three CRs; this one is "(2) `hold-live-cr`: `order hold` of a live CR in
every mode", and it "does not wait for (1)" (park-live-cr).

## Decisions carried

The grill is park-live-cr's (`../park-live-cr/02-answers.md`); this CR's own `02-answers.md` points
there.

| Answer | Decision | Where |
| --- | --- | --- |
| Q9 (A) | `order hold` stays the user's act. The Foreman never holds and never unholds. | 1, 2, 8 |
| Q6 (A), applied to a hold through Fable 2 ("same effect") | The held CR frees its slot: its Driver ends, its worktree and PR stay, a new Driver takes it up after the unhold. | 1, 2, 8 |
| Q3 (A) | The stack goes on without it, rebuilt; it comes back on top. | 1, 3 |
| Fable 2, Q11/Q12 | `order hold` is accepted on a live CR, in every mode. Only the user's `order unhold` releases it. | 1, 2 |
| Fable 6 | The CRs that depend on a held CR wait without a slot; the rest is restacked without them. | 3 |
| Fable 7 | Coming back with no free slot, it goes before the queued CRs. No round is counted. | 2, 8 |
| Fable 8 | No release while a CR is held: one question to the user. | 6, 8 |
| Q12 (A) | Three CRs; this one does not wait for park-live-cr. | Out of scope; "Shared with park-live-cr" |
| Critic run v1, fixes 2, 5, 6, 7, 8 | Applied below (sections 3, 4, 5, 6, 7). | 3-7 |
| Critic, open question 2 dropped | A ready CR outside a stack holds no slot: its hold stays stack-only, as today. | 1 |

## Words

- **Held:** a CR whose record carries `held` (the hold's order id) and that is not merged or
  cancelled (`is_held`, unchanged). A held CR is either `ready` (held from ready, stack only, as
  today) or `blocked` (held from live, this CR).
- **Out of order:** a CR that is held, or an open CR whose `after` names a held CR, directly or
  through other CRs. It is computed and never stored. It is what every reader of the stack's and
  the series' order skips (section 3).

## Shared with park-live-cr

park-live-cr (`1-inbox/park-live-cr`) adds the Foreman's `park` and defines the same `out_of_order`
notion, widened to parked CRs and their dependents. Whichever of the two CRs lands first adds
`out_of_order` and moves the readers of section 3 onto it. The second one widens its test, with no
new reader. park-live-cr's specification v1, section 7 ("`order hold` of a live CR"), moves here.
Its next run drops that section and points to this CR. Both CRs edit the same functions
(`stacks.py`, `rails.series_predecessor`, `rails.check_take`, `status/words.step`,
`status/views._now_next`). The one that lands second rebases onto the other; neither depends on the
other.

This CR depends on `factory-redefine` (`depends.json`, carried from the split). That CR rewrites the
lines of `commands/orders.py` that this CR touches (the `applied` test of `_record_order`, and the
factory branches around it), so this CR is coded on top of it.

## What changes

The CLI lives in `skills/chantier/scripts/cli/src/chantier/`, the cards in
`skills/chantier/references/`.

### 1. `order hold` accepts a working CR, in every mode

`commands/orders_hold.py`, `hold`:

- **Mode.** The refusal "batch … is not a stack" is now raised only for a `ready` CR. A working CR
  is accepted in parallel, series and stack batches.
- **Refusals kept, in this order:** the release CR or a fix CR (today's texts); a CR already held
  (`<cr> is already held (order <O-n>)`).
- **Status.** Accepted: `working` in any mode; `ready` in a stack only (today's rule, with today's
  dependents refusal "<x> depends on <cr>: it cannot stand in the stack without it", kept for a
  ready CR only). Any other status, and a ready CR outside a stack, is refused, exit precondition,
  nothing written:
  `order hold: <cr> is <status>; only a live CR, or a ready CR of a stack, is held`
  (for a ready CR outside a stack: `order hold: <cr> is ready in a <mode> batch: a ready CR holds no
  slot; only a stack holds a ready CR out of its order`).
- **Effect on a working CR**, in one write of the batch:
  - `status` becomes `blocked`, with `blocked_reason` `held: order <O-n>`, and `held` is set to the
    order id (as today);
  - its lease ends (`leases.end(c.lease)`, as `orders_drop.drop` does for a live CR): the old
    Driver's next command is `claim lost`. `held(d)` (`rails.py`) no longer counts it, so its slot
    is free at once;
  - in a stack it leaves the stack as a held ready CR does: `stacked=False`, its `start_on` unset,
    and every open CR whose `start_on` is the branch of an out-of-order CR (itself or one of its
    dependents) gets its `start_on` unset (today's loop, widened from "its branch");
  - it logs `hold` in `events.jsonl` with the order id, and `from: working`.
- **Effect on a ready CR in a stack:** unchanged.
- **The line**, for a working CR:
  `<cr> held (order <O-n>): it was live; its slot is free: the Foreman stops its Driver, then
  \`agents set <cr> - --epoch <n>\`[, takes the stack driver (\`take stack --note "hold <cr>"\`)]
  and \`order done <O-n>\`; \`order unhold <cr>\` brings it back`
  The bracketed part is printed in a stack only. With no agent recorded, the "stops its Driver ...
  `agents set`" part is left out.
- **The order stays pending** until the Foreman's `order done`, as the drop of a live CR does:
  `commands/orders.py`, `_record_order`, the `applied` test, gets "nor the hold of a working CR"
  next to "not the drop of a live CR". The test reads the CR's status before the hold is applied
  (it is `working` then). A pending order already stops the automatic pause
  (`core/endblockers.py`), unchanged.
- `declare/orders.py`: the help reads `hold|unhold (a live CR, or a ready CR of a stack, out of the
  slots and the order, and back)`.

### 2. `order unhold` of a CR held from live

`commands/orders_hold.py`, `unhold`:

- As today: `held` unset, and `order` set to one above every CR of the batch: on top, under the
  release (in a series, at the end of the series; in a parallel batch the order only sorts).
- For a `blocked` CR (held from live): `blocked_reason` becomes `unheld: order <O-m>`. The CR stays
  `blocked`: it holds no slot until its take.
- The line, for that CR:
  `<cr> unheld (order <O-m>): back on top; the Foreman takes it back before any queued CR
  (\`take <cr> --note "unhold: <O-m>" --epoch <n>\`)[, then the stack driver places it]`.
  The ready case keeps today's line.
- Its take is today's take-back of a blocked CR (`rails.check_take`): `--note` required, a free
  slot needed (`check_slot`), no round counted. `take` of a held CR stays refused until the unhold
  (`stacks.refuse_held`); its text becomes mode-neutral:
  `<cr> is held (order <O-n>): only the user's \`order unhold <cr>\` releases it`.

### 3. `out_of_order` and the readers of `is_held` (critic fix 2)

`out_of_order(crs, c)` is added to `rails.py`, next to `series_predecessor`. `stacks.py` imports
from `rails.py`, never the reverse, so `is_held` moves there too, and `stacks.py` re-exports it for
its current importers. It is true for a held CR, and for an open CR (not merged or cancelled) whose
`after` names an out-of-order CR (the closure, computed on each call).

Each reader of `is_held` is named here, with what it reads after this change:

| Reader | Reads | Why |
| --- | --- | --- |
| `stacks.chain`, `stacks.top_cr`, `stacks.next_merge` | `out_of_order` | Neither a held CR nor its dependents stand in the stack or the series' merge order (Q3, Fable 6). |
| `stacks._live_start`, `stacks.start_base` (the `held_owner` test) | `out_of_order` (of the owner) | A CR does not start on an out-of-order CR's branch unless it depends on it. |
| `stacks.start_base`, `stacks.stack_base` (the CR's own `is_held` test) | `is_held` | A held CR's base is the default branch, as today. |
| `stacks.stack_base`, `stacks.start_base`, for a dependent of a held CR | new branch | Its base is the branch of its nearest open dependency (`_nearest_open`), whatever its `stacked`. It is never the default branch. |
| `stacks.held_lines` | `is_held` | Section 5. |
| `stacks.refuse_held`, `stacks.held_text` | `is_held` | The hold itself and its way back. |
| `stack_words._forge_case` (an owner held) | `out_of_order` | A PR on an out-of-order CR's branch reads `other`. |
| `stack_words._ready_word` | `out_of_order` | A dependent of a held CR reads `PR in draft`. |
| `stack_words.draft_waited`, `draft_clause` | `is_held` for the CR; then, for a dependent, the held CR it depends on | A dependent's clause reads `it waits on <held cr> (<pr>)`. |
| `commands/delivery.py`, `stack <crs>` refusal | `out_of_order` | A dependent of a held CR is refused too: `<cr> is out of the stack: <held> is held (order <O-n>): \`order unhold <held>\` first`. |
| `commands/delivery.py`, `_check_out_of_draft` | `out_of_order` | Same text. |
| `commands/forge_stack_apart.held` | `is_held` | Only a held CR's PR is moved to the default branch. A dependent keeps its PR's base, the held CR's branch: on the default branch, its diff would show the held CR's commits. It is left out of the forge stack because `chain` leaves it out. |
| `commands/orders_drop.drop` | `is_held` | It unsets the hold, as today. |
| `commands/orders_hold.hold`, `unhold` | `is_held` | The hold itself. |
| `commands/orders_reorder.release_holds` | `is_held`, and section 5 | Critic fix 6. |

Every CR that depends on a held CR stays as it is (Fable 6). A queued one waits without a slot, as
today, because `blocked` is not met in `waits_for`. A working one keeps its Driver, hands back as
usual, and stays out of the stack until the held CR is back.

`stack_due` and the final-order take do not count an out-of-order CR, since they read `chain`.

### 4. Series: `series_predecessor` skips held CRs (critic fix 5)

`rails.series_predecessor` skips every out-of-order CR, as it skips a cancelled one. In a series,
the successor of a held CR no longer waits for it. Its `take` is accepted once the CR before the
held one is met, and its base is that CR's branch (`start_base`, series branch). `board/crs.py`
reads the same function, so it follows with no change of its own.

### 5. Leaving a stack keeps a live CR's hold (critic fix 6)

`commands/orders_reorder.release_holds` (called by `order mode` when a batch leaves a stack) lets
go only the holds of `ready` CRs, as today: those exist only in a stack. A held CR that is not
`ready` (held from live) keeps its `held`, its `blocked` status and its reason. Its order still
takes a unique one above all, as today. The line for it:
`<cr>: still held (order <O-n>): it was live; only \`order unhold <cr>\` releases it`.

### 6. No release over a held CR (critic fix 7)

`rails.check_take`: for the release CR, taken from `queued`, or taken back from `ready` or
`blocked`, when any CR of the batch is held, the take is refused before the `waits for` refusal,
exit precondition:

```
<release> waits for <cr> held (order <O-n>)[, <cr> held (order <O-m>)]: only the user's
`order unhold <cr>` or `order drop <cr>` lets it start
```

The resume of a working release (`--note "resume: …"`) is not refused: it keeps its slot.

This holds in every mode. A held ready CR in a stack used to count as met for the release
(`waits_for`, met is `ready` in an ordered batch); the card asked the Foreman not to take the
release then. The CLI now refuses it. A CR held while the release is already taken (working or
ready) makes the release stale. That is a card rule (section 8): the release is redone with
`redo:` once the hold ends.

### 7. What `status`, `STATUS.*` and the pane show (critic fix 8)

**`status`** (`commands/batch_status.py`, which calls `stacks.held_lines`): `held_lines` is no
longer stack-only. It prints one line per held CR, in order:

- a held ready CR of a stack: today's line;
- a held CR that was live:
  `held: <cr> (order <O-n>), was working, out of the slots[ and the stack]: only the user's
  \`order unhold <cr>\` brings it back` and, when open CRs depend on it, `; waiting with it: <cr>,
  ...`;
- an unheld CR still `blocked` is not a held CR. Its row reads `| blocked: unheld: order <O-m>`,
  and no extra line is printed.

**The CR's step and its now and next lines** (`status/words.step`, `status/views._now_next`).
These are `STATUS.json` fields that the pane draws (`step`, `now`, `next`, and `label`, which
contains `step`):

- `step`: a blocked held CR reads `Held` (from `is_held`, before the `blocked_reason` word test).
  A blocked CR whose reason starts with `unheld:` reads `Unheld`. `ASKING` is unchanged.
- `_now_next`, before the generic `blocked` branch:
  - held: now `Held by the user (order <O-n>): out of the slots[ and the stack].`, next
    `The user's \`order unhold\`, through the Chief of Staff.`;
  - unheld: now `Unheld (order <O-m>): back on top, to take back.`, next
    `A Driver takes it back, before any queued CR.`
- `severity` is unchanged: a blocked CR is red, so a held live CR stays red in the batch, as the
  user accepted at Q11.

The step and the now and next lines change what the CR board pane draws (AGENTS.md). The PR's
Deliverables therefore carry one screenshot of the pane from a real Claude Code session at the PR's
head, captioned with its seven-character SHA, with a held live CR shown. Until it is there, the
PR's Known gaps names "no screenshot of the pane from a real session". `hooks/register.tsx` and
`types/` are unchanged, so `just mod` is not owed. `STATUS.md` and the board read the same view and
need no change of their own. No field is added to `STATUS.json` or to the server's protocol.

### 8. Cards

**`foreman.md`**, "A held CR" (today under the stack batch bullet) becomes a bullet of its own,
for every mode:

- On an `order hold` of a working CR (in `status`, or on the order's line): stop its Driver. Send
  `[foreman→driver <cr>] stop hold: <O-n>` and wait for its `stopped` line, or for its end, then run
  `agents set <cr> - --epoch <n>`. In a stack, then take the stack driver
  (`take stack --note "hold <cr>"`). Then `order done <O-n>`. Never take a held CR for a round.
  Never unhold.
- On an `order unhold` of a CR held from live: `take <cr> --note "unhold: <O-m>" --epoch <n>`, then
  a new CR Driver, before any queued CR (a blocked CR holds no slot, so it takes the next free
  one). No round is counted. In a stack, the stack driver places it on top at its next take.
- The release and the final-order take: neither starts while a CR is held (the CLI refuses the
  release). Send one ask per held CR, `the release waits: <cr> is held (order <O-n>)`. A CR held
  while the release is working: let the release hand back, `note` it stale, and once the hold ends
  (the CR unheld and handed back ready, or dropped), `take <release> --note "redo: <cr> held"`.
- The dependents of a held CR: a queued one waits; a working one goes on; neither is placed in the
  stack until the held CR is back.

**`driver.md`:**

- In the notes (`ping`, `stop`): `stop hold: <O-n>` means the CR is held by the user. Stop your long
  gate (`gate <cr> --stop`) and every background task. Commit nothing new and push nothing. Your
  lease has already ended, so record nothing: `handback` would be `claim lost`. Reply
  `[driver <cr>→foreman] stopped: held; worktree clean` or `…; worktree dirty: <files>`, and end.
  The uncommitted work stays in the worktree for the next Driver.
- "CR driver: re-takes": a take with `unhold: <O-m>` resumes the CR as a `resume:` does (`handoff
  <cr>` for where it stands, the worktree as the stopped Driver left it). In a stack, the CR is now
  on top: rebase onto the branch its `start` line names before the next `ship`.
- "A CR held out of the stack" (stack driver), for a CR held from live:
  - step 2 skips each CR above that depends on the held CR (out of the stack with it: it keeps the
    held CR's commits);
  - step 3 (rebase the held CR's branch on the default branch) runs only when its worktree is clean.
    With uncommitted changes there, skip it: the PR stays a draft until the unhold, and the stack
    driver's report names it.

**`chief-of-staff.md`**, "Holding a CR out of a stack" becomes "Holding a CR":

- On the user's word to hold a CR: `order hold <cr>`, for a ready CR of a stack (as today) or a
  live CR in any mode (its slot is freed at once and its Driver stopped by the Foreman). If it is
  unclear whether the user means out of the order or out of the batch, ask.
- `order unhold <cr>` is the user's word only. Tell the user in one line what the hold did (the CR,
  its slot freed, the batch going on without it).
- Batch reports name each held CR. At a batch's end, tell the user that the batch stays open while
  a CR is held. On the release blocked by a held CR, today's ask applies, in every mode.
- In direct mode, the Chief of Staff does the Foreman's part (stop the Driver, `agents set`,
  `order done`, the take after the unhold).

**`concepts.md`**, "A CR held out of the stack": a live CR can be held too, in every mode. It turns
`blocked`, frees its slot, and leaves the stack and the series order with the CRs that depend on
it. It comes back on top on the user's `order unhold`, and no release starts while a CR is held.

**`routing.md`:** the Foreman → Driver row gets `stop hold: <O-n>`. The Driver → Foreman row gets
`stopped: held; worktree clean|dirty: <files>`.

### 9. Docs

- `README.md` and `docs/use-cases-foreman.md`, `docs/use-cases-direct.md`: where `order hold` is
  described, add that it takes a live CR in every mode and frees its slot. If neither use-case file
  describes it, change `README.md` only.
- `scenario/README.md`: the new case (Evidence).

## Out of scope

- The Foreman's `park`, the named `close` refusal and the batch's-end line for a blocked or held CR:
  park-live-cr. Here `close` keeps today's behaviour: a batch with a held live CR is not paused
  (`blocked` is not ended, and the hold order stays pending until `order done`), so `close` refuses
  it with "pause first".
- The `ready` drop destination and the destinations of a started CR (P1..P4, the next batch, the
  trash; never the inbox): drop-to-next-batch (park-live-Q12, Q13). `order drop` of a held CR keeps
  today's destinations and behaviour (it unsets the hold).
- The hold of a queued or blocked CR (neither is live), and of a ready CR outside a stack. A ready
  CR holds no slot, so its hold stays stack-only (the critic dropped the question).
- Dragging a CR out of the running batch on the board (park-live-Q14: not now).
- The web client, the terminal client and `hooks/register.tsx`: no change of code. They draw the
  new `step` and `now`/`next` texts through the existing fields.
- The hub and the interest registry: unchanged.

## Evidence

Every check runs the CLI's real commands on states the CLI built (`open`, `take`, `handback`,
`order`). The card checks read the shipped cards from the repository at the head under test.

**Tests** (`skills/chantier/scripts/cli/tests/`, in-process, few and parametrized, within `just
test`'s limit). Extend `test_stack_hold.py`, and `test_rail_refusals.py` for the release:

- **`order hold` refusals** (parametrized, nothing written): a queued CR, a blocked CR, a ready CR
  in a parallel and in a series batch (the new ready text), the release CR, a fix CR, a CR already
  held.
- **`order hold` of a working CR, in each mode** (parametrized: parallel, series, stack):
  - the CR is `blocked`, with `held` set and `blocked_reason` `held: order <O-n>`;
  - the old lease's next command is `claim lost`;
  - `held(d)` no longer counts it, and a queued CR's `take` is accepted with no change to the slots;
  - the order is pending (`applied` false) until `order done`;
  - `take` of the CR is refused with the new mode-neutral text;
  - `order unhold` sets `unheld:`, its order is above every other CR's, and `take --note "unhold:
    …"` is accepted with its `round` unchanged;
  - with no free slot, that take is refused by `check_slot`.
- **The stack:** in a stack of three with the middle CR working, its hold leaves it out of `chain`,
  `top_cr` and `next_merge`. A CR whose `after` names it is out of `chain` too: its base is the
  held CR's branch, it reads `PR in draft`, and `stack <it>` and `stack --out-of-draft <it>` are
  refused naming the held CR. A CR that only started on its branch gets its `start_on` unset.
  `forge-stack rebuild` (the fake forge) moves only the held PR to the default branch.
- **Series** (fix 5): with three CRs in a series and the second held while working, the third's
  `take` is accepted once the first is ready, and its `start_base` is the first's branch.
- **Leaving a stack** (fix 6): `order mode parallel` on a stack with one held ready CR and one held
  live CR lets the ready one go and keeps the live one held, `blocked`, with a unique order.
- **The release** (fix 7): `take <release>` with a held CR in the batch (a held ready CR of a
  stack, and a held live CR of a parallel batch) is refused with the new text, nothing written. A
  working release's `resume:` take is accepted.
- **`status` and the views** (fix 8): `status` prints the `held: … was working` line with `waiting
  with it`, in a parallel batch. `step` reads `Held`, then `Unheld` after the unhold. The CR's
  view has the new `now` and `next` lines and `severity` red.
- **The cards** (read from the repository at the head under test), added to the card test that
  already reads the shipped references (`test_came_back.py`'s pattern, or the file that holds the
  closest card checks; no new file just for these): `foreman.md` names `stop hold:` and `unhold:`;
  `driver.md` names `stop hold:` and `stopped: held`; `chief-of-staff.md`'s "Holding a CR" names a
  live CR; `routing.md` names `stop hold:`.

**Scenario** (`scenario/run_scenario.py`): a new case `hold_live` in the `stack` unit, after
`stack_hold` (raise the unit's budget of 750 s only if the run shows the need), added to the
`UNITS` list (line 84) and to `CASES`:

1. A stack batch of three CRs with 2 slots: take the first two.
2. `order hold` of the second, working: its slot is free, `take` of the third is accepted, and the
   old lease gets `claim lost`. `order done` after `agents set <cr> -`.
3. `take stack --note "hold <cr>"` and `forge-stack rebuild`: the fake forge's bases show the held
   PR on the default branch and the stack without it.
4. `take <release>` is refused, naming the held CR.
5. `order unhold`, then `take --note "unhold: …"`: the CR is working again on top. It hands back
   ready and the batch goes on to its merge.
6. A parallel batch (or the same world in parallel mode): `order hold` of a working CR frees its
   slot, and `order unhold` with `take` brings it back.

`scenario/README.md` gets the case's line (unit: stack), with its test named as the neighbouring
lines do.

**Gates:**

- `just check` in the worktree.
- `just eval-dry-run` (the change is under the CLI's `src/`).
- The pipeline's `just scenario (ubuntu-latest)` job green at the PR's head (CLI, cards and
  scenario change).
- Windows coverage by `chantier gate` per AGENTS.md, when this CR is on top of its batch's stack.
- The pane screenshot in the PR's Deliverables (section 7), or its absence named in Known gaps.

**No host and default matrix:** the behaviour depends neither on the host nor on a configured
value.

## Open questions

1. **A series successor already started on the held CR's work.** In a series, a CR starts on the
   previous CR's branch once that CR is ready. If a ready CR is taken back to working, its
   successor may be working on top of its commits, and then the user may hold it. This
   specification skips the held CR as the predecessor (fix 5). The successor then keeps going with
   the held CR's commits in its branch, and its PR's base becomes the CR before the held one. Should
   such a successor be held out of the series order with it, like a CR that depends on it, or go on
   as specified?
