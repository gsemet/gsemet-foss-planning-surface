# `order hold` of a live CR, in every batch mode

The user's `order hold` today takes only a CR handed back ready, in a stack. With this change it
also takes a live (`working`) CR, in every mode (parallel, series, stack). The CR becomes `blocked`
and held. Its lease ends and its slot is free at once. It leaves the stack and the series order.
The CRs that depend on it (a series successor already started on it included) wait with it, out
of the order. It stays in the batch, red on the board, until the user's `order unhold` releases it;
it then comes back on top (in a series, after the CRs already started), its dependents above it,
and is taken back before any queued CR. No release starts while a CR is held. Dropping a held CR
that has dependents has their Drivers take its commits out of their branches.

Spec v3 (run 3): takes in the spec critic's run on v2 (fixes 1 to 10, none needing the user) and
hold-live-cr-Q2 (dropping a held CR that has dependents), and copies the "Shared with
hold-live-cr" section of park-live-cr's specification v6 word for word. v2 (run 2) took in
hold-live-cr-Q1, answers 3 and 4 and park-live-cr's critic run 2.

## Goal, in the user's terms

From the batch-29 retro (park-live-cr, kept point 2): CR-415 waited on the user's phone trial with
no Driver at work, yet kept a slot and its place in the stack for five hours, because `order hold`
takes only a ready CR. The user accepted the Fable advisor's choice 2 (park-live-Q11, all choices):
"`order hold` is accepted on a live CR, same effect, released by the user only". At park-live-Q12
the user split the work in three CRs; this one is "(2) `hold-live-cr`: `order hold` of a live CR in
every mode", and it "does not wait for (1)" (park-live-cr).

## Decisions carried

The grill is park-live-cr's (`../park-live-cr/02-answers.md`); this CR's own `02-answers.md` points
there and holds its own answers (hold-live-cr-Q1, Q2, entries 3 and 4).

| Answer | Decision | Where |
| --- | --- | --- |
| Q9 (A) | `order hold` stays the user's act. The Foreman never holds and never unholds. | 1, 2, 8 |
| Q6 (A), applied to a hold through Fable 2 ("same effect") | The held CR frees its slot: its Driver ends, its worktree and PR stay, a new Driver takes it up after the unhold. | 1, 2, 8 |
| Q3 (A) | The stack goes on without it, rebuilt; it comes back on top. | 1, 2, 3 |
| Fable 2, Q11/Q12 | `order hold` is accepted on a live CR, in every mode. Only the user's `order unhold` releases it. | 1, 2 |
| Fable 6 | The CRs that depend on a held CR wait without a slot; the rest is restacked without them. | 3 |
| Fable 7 | Coming back with no free slot, it goes before the queued CRs. No round is counted. | 2, 8 |
| Fable 8 | No release while a CR is held: one question to the user. | 6, 8 |
| Q12 (A) | Three CRs; this one does not wait for park-live-cr. | Out of scope; "Shared with park-live-cr" |
| Critic run v1, fixes 2, 5, 6, 7, 8 | Applied below (sections 3, 4, 5, 6, 7). | 3-7 |
| Critic, open question 2 dropped | A ready CR outside a stack holds no slot: its hold stays stack-only, as today. | 1 |
| hold-live-cr-Q1 (A) | A series successor already started on the held CR is out of the order with it, as a dependent: its Driver goes on, it is not merged before the held CR comes back (replaces v1's "goes on as specified"). "Started on" is read from the `start_on` recorded at its take (critic run v2, fix 1). | Words; "Shared with park-live-cr"; 2, 3, 4, 8 |
| Shared with park-live-cr's critic runs 2 and 3 | One `out_of_order` definition; one base rule for a dependent with several open dependencies (it replaces v1's `_nearest_open`); `apart_owner` follows the base rule's candidate; forge-stack's `waiting` covers the dependents of any apart CR; the series `start_on` recorded at the take. | "Shared with park-live-cr"; 3 |
| hold-live-cr-Q2 (A) | Dropping a held CR that has dependents, in a series or parallel batch: the Foreman has the dependents' Drivers rebase to take its commits out (the note `rebase: <cr> dropped`); they go on. In a stack the stack driver's removal stays. | "Shared with park-live-cr" (`order drop` of an apart CR); 1b; 8; Evidence |
| Answers 3 and 4 (from drop-to-next-batch-Q2 and the user's correction) | A held CR may be dropped to any destination `order drop` takes, on the user's decision: P1-P4, `3-ready`, the trash; never the inbox (answer 4 supersedes answer 3's "inbox included"). | Out of scope |

### The spec critic's fixes applied here (run on v2)

1. The series clause of `out_of_order` holds only for a successor that started on the apart CR (or
   on a dependent of it), read from `start_on`, now recorded at the take in a series batch too:
   "Shared with park-live-cr" (park-live-cr v6's wording, which settles it); section 4; the Series
   test.
2. `handback` of a held CR is refused, tested: section 1. `driver.md`'s "`handback` would be `claim
   lost`" is replaced by the refusal (a blocked CR's `handback` skips the lease check today, so the
   old Driver's `handback` would have been accepted): section 8.
3. The pending-order test of `_record_order` reads `kind == "hold"` with the CR's status `blocked`
   after the apply (a hold from ready leaves the CR `ready`): section 1, tested.
4. `depends.json` no longer names `factory-redefine` (a shared file, not a need): its sentence is
   gone; the one that lands second rebases.
5. `driver.md`:1281-1284 (the `unhold: <cr>` paragraph) and `foreman.md`:414-416 (the "A held CR"
   bullet) get the live case: a CR held from live comes back `blocked` and is taken back `working`,
   then joins as a working CR does: section 8.
6. The stack driver's step 3 of "A CR held out of the stack" (rebase onto the default branch) is
   skipped for a CR held from live, whatever its worktree: section 8.
7. Section 8 names `chief-of-staff.md`:1075, `driver.md`:762-763 (`order hold` added to the
   `claim lost` causes) and `foreman.md`:418.
8. Section 9: no `README.md` or use-case change; `concepts.md` carries it.
9. The closing note of the shared section says "Q15 is park-live-Q15 (here hold-live-cr-Q1), Q16 is
   park-live-Q16 (here hold-live-cr-Q2)"; the extra sentences stand outside the copied block.
10. The Foreman's and the Chief of Staff's bullets: the freed slot is filled, and a held CR is
    dropped, only after the hold's `order done`: section 8.

## Words

- **Open:** not merged and not cancelled.
- **Held:** a CR whose record carries `held` (the hold's order id) and that is open (`is_held`,
  unchanged). A held CR is either `ready` (held from ready, stack only, as today) or `blocked`
  (held from live, this CR).
- **Apart:** an open CR that is held or parked (parked: park-live-cr): it stands outside the stack
  and the series order, its PR on the default branch.
- **Dependent:** an open CR that is not apart and that waits with an apart CR (its **apart
  owner**), by the shared definition below: its `after` names an apart CR, directly or through
  other open CRs, or (series) its recorded `start_on` names the branch of an apart CR or of another
  dependent (hold-live-cr-Q1). A dependent's PR keeps its base on its dependency's branch.
- **Out of order:** apart or a dependent. Computed on each call, never stored (Fable 6). It is what
  every reader of the stack's and the series' order skips (section 3).

## Shared with park-live-cr

hold-live-cr and park-live-cr (both in `1-inbox/`) share this paragraph word for word, as
park-live-cr's specification v6 writes it; neither changes it alone. Whichever of the two CRs
lands first records the series `start_on`, adds the helpers below to `rails.py` and moves the
readers of `is_held` onto them; the second one widens its tests and adds no reader. Both edit the
same functions (`stacks.py`, `rails.series_predecessor`, `rails.check_take`, `status/words.step`,
`status/words.phase_text`, `status/views._now_next`, `commands/forge_stack_apart.py`,
`commands/orders_drop.drop`): the one that lands second rebases onto the other; neither depends on
the other.

**The fact recorded at the take.** `start_on` (`core/records.py`), today recorded at a CR's first
take in a stack batch only (`stacks.start_on_for`, called by `take` in `commands/driver.py`), is
recorded in a series batch too: the branch that `start_base`'s series rule gives at that take, the
branch of `series_predecessor` when that CR is open, else none (the default branch). It is the
branch the CR started on; the series clause below reads it, never the present order. A series
batch's `start_base` does not read it (its series rule is unchanged); after a change of mode to a
stack, `stack_start`'s rule 1 reads it with the same meaning.

**The definition** (in `rails.py`, which `stacks.py` imports, never the reverse; `is_held` moves
there and `stacks.py` re-exports it for its importers):

- `is_held(c)`: today's (held and open). `is_parked(c)`: `parked` set and open. `apart(c)`:
  `is_held(c) or is_parked(c)`.
- `out_of_order(crs, c, mode)`: false for a CR that is not open; true when `apart(c)`; true when
  one of `c`'s open `after` CRs is `out_of_order` (so: "an open CR whose `after` names an apart CR,
  directly or through other open CRs"); and, in a series batch only, true when `c` has left
  `queued` (it is `working`, `ready` or `blocked`), its `start_on` names the branch of an open CR
  `x`, and `x` is `out_of_order` (Q15: a successor that started on an apart CR or on a dependent of
  it). A series CR that started on a CR still in the order is not a dependent, even when the CR
  before it in the present order is out of order; nor is a queued successor: it has no `start_on`
  yet, and `series_predecessor` gives it the CR before the out-of-order ones. The recursion ends:
  `after` is acyclic, and the CR a `start_on` names was taken before the CR that names it.
- `series_predecessor(crs, c)`: today's rule (the nearest CR before `c` in the order that is
  neither a release nor a fix and not cancelled; a merged one counts), also skipping every CR `x`
  with `out_of_order(crs, x, "series")`.
- A dependent's **candidates**, in this order: in a series batch, the open CR whose branch its
  `start_on` names; then its open `after` CRs, in the order of `after`.
- `apart_owner(crs, c, mode)`: for an apart CR, itself; for a dependent, the `apart_owner` of the
  last out-of-order CR among its candidates (the base rule's candidate), recursively. Every
  message about a dependent names it with its kind: `parked <p>` or `held <p> (order <O-n>)`.

**The base rule** for a dependent, one rule whatever its number of open dependencies, before the
series and stack rules of `stacks.start_base` and `stacks.stack_base`: its base is the branch of
the **last out-of-order CR among its candidates**. There is always one (that is what makes it a
dependent). Why not the dependency highest in the stack (`_nearest_open`): a dependency still in
the stack merges or is placed below, and the apart CR comes back on top of every open CR, so the
apart CR's branch, or a dependent's above it, ends up holding the others' work; a base in the
stack would leave the apart CR's commits out of the dependent's branch. An apart CR's own base is
the default branch, as a held CR's is today.

**forge-stack's `waiting`** covers the dependents of any apart CR, held or parked: their PRs are
left out of the native stack, not retargeted, and named apart, never as foreign PRs.

**`order drop` of an apart CR** (`commands/orders_drop.drop`) unsets `held` or `parked`, so a
dropped CR never reads held or parked. With no dependent, it prints today's line, `<cr> was
held|parked: no stack driver needed`. With dependents, it names them instead, with who takes the
dropped commits out of their branches (park-live-Q16, hold-live-cr-Q2): `<cr> was held|parked; waiting with it:
<cr>, ...: <tail>`, where `<tail>` is, in a stack batch, the stack driver's removal, `the stack
driver takes it out of their branches (\`take stack --note "drop: <cr> to <destination>"\`)`, and,
in a series or parallel batch, the Foreman's rebase note to their Drivers, `their Drivers rebase
to take its commits out (the Foreman's note \`rebase: <cr> dropped\`)`. With `held` or `parked` unset,
the dropped CR is no longer apart, so its dependents leave `out_of_order` (unless another apart CR
holds them) and take their base again by the series, stack or default rule. In a series or parallel batch, the Foreman
sends each dependent that has a Driver or a branch the note `rebase: <cr> dropped`: a working one
as a note to its Driver (`[foreman→driver <dep>] note rebase: <cr> dropped`), one handed back ready
or blocked by `take <dep> --note "rebase: <cr> dropped"`; a queued one needs none (its first take
starts on its new base). Its Driver rebases its branch onto the base `take` or `handoff` names,
leaving out the dropped CR's commits, and goes on (`driver.md`, "CR driver: re-takes"). In a stack
batch, the stack driver's removal stays as it is.

Notes to the copied section, outside it. Q15 is park-live-Q15 (here hold-live-cr-Q1), Q16 is
park-live-Q16 (here hold-live-cr-Q2). If this CR lands first, `is_parked(c)` reads the `parked`
field, which no command sets yet: it is always false until park-live-cr lands; this CR then writes
the series `start_on`, the helpers, the readers, the drop line and `driver.md`'s `rebase: <cr>
dropped` paragraph (section 8), and park-live-cr widens them. Here, the return on top is section 2,
the readers, `waiting` included, are section 3, and the drop of a held CR is section 1b.
park-live-cr's specification v1, section 7 ("`order hold` of a live CR"), moved here.

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
    Driver's next leased command is `claim lost`. `held(d)` (`rails.py`) no longer counts it, so
    its slot is free at once;
  - it leaves the stack and the order as a held ready CR leaves the stack: `stacked=False`, its own
    `start_on` unset, and every open CR whose `start_on` names the branch of the held CR or of one
    of its dependents, and that is not itself a dependent, gets its `start_on` unset (today's loop
    of `orders_hold.hold`, widened from "its branch" and moved into a shared helper in `stacks.py`
    that park-live-cr's `park` calls too; whichever lands first moves it). A dependent keeps its
    `start_on`: its base is given by the shared base rule;
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
  next to "not the drop of a live CR". `_record_order` runs after the hold is applied, so the test
  reads `args.kind == "hold" and b.cr(cr).status == "blocked"` (a hold from live leaves the CR
  `blocked`; a hold from ready leaves it `ready`, and that order stays applied as today) (critic
  run v2, fix 3). A pending order already stops the automatic pause (`core/endblockers.py`),
  unchanged.
- **`handback` of a held CR** (critic run v2, fix 2). A blocked CR can be handed back with no lease
  check today (`commands/driver.py`, `_handback_locked`, `was_blocked`), so the stopped Driver's
  `handback`, or anyone's, could take a held CR out of its hold. After `live_cr`, before the
  `was_blocked` branch, a held CR (`is_held`, held from live or from ready) is refused, exit
  precondition, nothing written:
  `handback: <cr> is held (order <O-n>): only the user's \`order unhold <cr>\` releases it`.
- `declare/orders.py`: the help reads `hold|unhold (a live CR, or a ready CR of a stack, out of the
  slots and the order, and back)`.

### 1b. `order drop` of a held CR that has dependents (hold-live-cr-Q2)

`commands/orders_drop.drop`, as the shared section's "`order drop` of an apart CR" writes it: the
hold is unset; with no dependent, today's line `<cr> was held: no stack driver needed`; with
dependents (computed before the hold is unset, `apart_owner` the dropped CR), `<cr> was held;
waiting with it: <cr>, ...: <tail>`, the tail naming the stack driver's removal in a stack batch,
the Foreman's `rebase: <cr> dropped` note to their Drivers in a series or parallel batch. Once the
hold is unset, the dependents are no longer out of order (unless another apart CR holds them) and
take their series, stack or default base again. The drop of a live CR keeps its pending order
(today's `applied` test); a CR held from live is `blocked`, not live, so its drop is applied at
once unless the hold's own order is still pending (the card's rule, section 8: the Chief of Staff
drops a held CR only after the hold's `order done`).

### 2. `order unhold` of a CR held from live

`commands/orders_hold.py`, `unhold`:

- As today: `held` unset. Its new `order`: in a stack or a parallel batch, one above every CR of the
  batch, under the release, as today (in a parallel batch the order only sorts). In a series batch
  (where every held CR is held from live), the shared return placement of park-live-cr: above every
  CR that has left `queued` (the release aside) and below the queued ones, which move up by as many
  places, their order kept.
- For a `blocked` CR (held from live): `blocked_reason` becomes `unheld: order <O-m>`. The CR stays
  `blocked`: it holds no slot until its take.
- Its open dependents (computed before `held` is unset: `out_of_order` with this CR as their
  `apart_owner`) then take the places right above it, in the order of `chains_kept`
  (`commands/orders_reorder.py`) over their present orders, so that no CR stands below one of its
  `after` and a series successor stands right above it again (hold-live-cr-Q1; the same as
  park-live-cr's return); in a series, still below the queued CRs. The line then ends `; its
  dependents above it: <cr>, ...`.
- The line, for that CR:
  `<cr> unheld (order <O-m>): back on top; the Foreman takes it back before any queued CR
  (\`take <cr> --note "unhold: <O-m>" --epoch <n>\`)[, then the stack driver places it]`.
  In a series batch, `back on top` reads `back in the series after its started CRs`. The ready case
  keeps today's line.
- Its take is today's take-back of a blocked CR (`rails.check_take`): `--note` required, a free
  slot needed (`check_slot`), no round counted. `take` of a held CR stays refused until the unhold
  (`stacks.refuse_held`); its text becomes mode-neutral:
  `<cr> is held (order <O-n>): only the user's \`order unhold <cr>\` releases it`.

### 3. The shared predicates and the readers of `is_held` (critic fix 2; critic run 2)

The predicates are the shared ones ("Shared with park-live-cr"): `is_held`, `is_parked`, `apart`,
`out_of_order(crs, c, mode)`, `series_predecessor`, a dependent's candidates, `apart_owner`, in
`rails.py` (`stacks.py` re-exports `is_held` for its importers), and the series `start_on` recorded
at the take. `crs` is the batch's CR list and `mode` the batch's mode, as `waits_for` takes them.

Each reader of `is_held` is named here, with what it reads after this change. Where a reader speaks
of a dependent, it names its apart owner (`apart_owner`, the apart owner of the base rule's
candidate) with its kind (`held <p> (order <O-n>)`, or `parked <p>` once park-live-cr is in):

| Reader | Reads | Why |
| --- | --- | --- |
| `stacks.chain`, `stacks.top_cr`, `stacks.next_merge` | `out_of_order` | Neither a held CR nor its dependents stand in the stack or the series' merge order (Q3, Fable 6). A ready dependent in a series is not the next merge (hold-live-cr-Q1). `stack_due` and `held_lines` follow `chain`. |
| `stacks.start_on_for` (called by `take`, `commands/driver.py`) | in a series batch, the branch of an open `series_predecessor` | The fact recorded at the take: the series clause of `out_of_order` reads it, never the present order (critic run v2, fix 1). |
| `stacks._live_start`, `stacks.start_base` (the `held_owner` test) | `out_of_order` (of the owner) | A CR does not start on an out-of-order CR's branch unless it is its dependent. |
| `stacks.start_base`, `stacks.stack_base` (the CR's own `is_held` test) | `apart` | An apart CR's base is the default branch, as a held CR's is today. |
| `stacks.start_base`, `stacks.stack_base`, for a dependent | the shared base rule | Before the series and stack rules: the branch of the last out-of-order CR among its candidates. It is never the default branch. It replaces v1's `_nearest_open`. |
| `rails.series_predecessor` | the shared definition | Section 4. |
| `stacks.held_lines` | `is_held` | Section 7. |
| `stacks.refuse_held`, `stacks.held_text` | `is_held` | The hold itself and its way back. |
| `commands/driver.py`, `_handback_locked` | `is_held` | The held refusal (section 1, critic run v2, fix 2). |
| `stack_words._forge_case` (an owner held) | `out_of_order` | A PR on an out-of-order CR's branch reads `other`. |
| `stack_words._ready_word` | `out_of_order` | A dependent reads `PR in draft`: it never reads ready to merge. |
| `stack_words.draft_waited`, `draft_clause` | `is_held` for the CR; `apart_owner` for a dependent | A held CR: `held_text`, as today. A dependent with a held owner: `waits with held <p> (order <O-n>): \`order unhold <p>\``. |
| `commands/delivery.py`, `stack <crs>` refusal and `_check_out_of_draft` | `out_of_order` | A held CR: today's refusal. A dependent is refused too: `<cr> waits with held <p> (order <O-n>): it stays out of the stack until <p> is back`. |
| `commands/forge_stack_apart.held` | `apart` | Only an apart CR's PR is moved to the default branch, reason `(held out of the stack)` for a held one. |
| `commands/forge_stack_apart`, new `waiting` | `out_of_order` and not `apart` | The PR of a dependent of any apart CR, held or parked: left out of the native stack, not retargeted (it keeps its base by the shared rule: on the default branch its diff would show the held CR's commits), and named apart in the rebuild's lines and in check 2 as `#n of <cr> waits with held <p>: left out of the stack` (`parked <p>` for a parked owner), never as a foreign PR. |
| `commands/orders_drop.drop` | `is_held`, `apart_owner` | It unsets the hold, as today; the line with or without dependents (section 1b, hold-live-cr-Q2). |
| `commands/orders_hold.hold`, `unhold` | `is_held`, `apart_owner` | The hold itself; the unhold's placement and dependents (section 2). |
| `commands/orders_reorder.release_holds` | `is_held`, and section 5 | Critic fix 6. |

**The CRs that wait with it** (Fable 6, hold-live-cr-Q1) keep their status. A queued one waits
without a slot, as today, because `blocked` is not met in `waits_for`. A working one keeps its
Driver and hands back as usual; it stays out of the stack and the series' merge order until the
held CR is back: its PR stays a draft (`PR in draft`), it is never `next_merge`, and
`stack --out-of-draft` refuses it. This holds for a series successor already started on the held CR
(hold-live-cr-Q1): its Driver goes on; it is not merged before the held CR comes back.

### 4. Series: `series_predecessor` skips out-of-order CRs (critic fix 5; hold-live-cr-Q1)

`rails.series_predecessor` is the shared one: it skips every out-of-order CR, as it skips a
cancelled one. A queued successor of a held CR (not started, no `start_on` yet) is not a dependent:
it no longer waits for the held CR, its `take` is accepted once the CR before the out-of-order ones
is met, its `start_on` recorded at that take is that CR's branch, and its base is that CR's branch
(`start_base`, series branch). A successor whose recorded `start_on` names the held CR's branch (it
was taken while the held CR was still in the order) is a dependent (hold-live-cr-Q1): out of the
order with it, its base the held CR's branch by the shared base rule, and so on for a CR whose
`start_on` names that successor's branch. `board/crs.py` reads the same function, so it follows
with no change of its own.

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
- `phase_text` (`status/words.py`, the phase every surface copies), before its `waits for the
  user` branch: a blocked held CR reads `held (order <O-n>)`; a blocked CR whose reason starts with
  `unheld:` reads `to take back` (it waits for the Foreman, not the user).
- `severity` is unchanged: a blocked CR is red, so a held live CR stays red in the batch, as the
  user accepted at Q11.

The step, the phase and the now and next lines change what the CR board pane draws (AGENTS.md). The
PR's Deliverables therefore carry one screenshot of the pane from a real Claude Code session at the
PR's head, captioned with its seven-character SHA, with a held live CR shown. Until it is there,
the PR's Known gaps names "no screenshot of the pane from a real session". `hooks/register.tsx` and
`types/` are unchanged, so `just mod` is not owed. `STATUS.md` and the board read the same view and
need no change of their own. No field is added to `STATUS.json` or to the server's protocol.

### 8. Cards

**`foreman.md`**, "A held CR" (`foreman.md`:414-416, today under the stack batch bullet) becomes a
bullet of its own, for every mode (critic run v2, fixes 5, 7, 10):

- On an `order hold` of a working CR (in `status`, or on the order's line): stop its Driver. Send
  `[foreman→driver <cr>] stop hold: <O-n>` and wait for its `stopped` line, or for its end, then run
  `agents set <cr> - --epoch <n>`. In a stack, then take the stack driver
  (`take stack --note "hold <cr>"`). Then `order done <O-n>`. Only then fill the freed slot (a
  queued CR's take, a new Driver): the old Driver is stopped first. Never take a held CR for a
  round. Never unhold. A ready CR held in a stack keeps today's path (the stack driver, then `order
  done`).
- On an `order unhold` of a CR held from live: it comes back `blocked`. `take <cr> --note "unhold:
  <O-m>" --epoch <n>` (it turns `working`), then a new CR Driver, before any queued CR (a blocked
  CR holds no slot, so it takes the next free one). No round is counted. In a stack it then joins
  as a working CR does ("A working CR placed on another"): no `take stack --note "unhold <cr>"`
  for it; the stack driver places it on top at its next take. A ready CR unheld in a stack keeps
  today's `take stack --note "unhold <cr>"`.
- The release and the final-order take (`foreman.md`:418): neither starts while a CR is held, in
  any mode (the CLI refuses the release). Send one ask per held CR, `the release waits: <cr> is
  held (order <O-n>)` (today's text loses "out of the stack"). A CR held while the release is
  working: let the release hand back, `note` it stale, and once the hold ends (the CR unheld and
  handed back ready, or dropped), `take <release> --note "redo: <cr> held"`.
- The dependents of a held CR (a series successor already started on it included): a queued one
  waits; a working one goes on; none is placed in the stack or merged until the held CR is back.
  At the unhold they stand above it (the CLI reorders them).
- Dropping a held CR that has dependents (hold-live-cr-Q2; the same bullet as park-live-cr's,
  written by whichever lands first): the line `order drop` prints names them. In a stack, `take
  stack --note "drop: <cr> to <destination>"`, as today. In a series or parallel batch, send each
  dependent with a Driver or a branch the note `rebase: <cr> dropped`, by the usual path (read
  `status` first: `working`, `[foreman→driver <dep>] note rebase: <cr> dropped`; `ready` or
  `blocked`, `take <dep> --note "rebase: <cr> dropped"`); a queued one needs none. They go on.

**`driver.md`:**

- In the notes (`ping`, `stop`): `stop hold: <O-n>` means the CR is held by the user. Stop your long
  gate (`gate <cr> --stop`) and every background task. Commit nothing new and push nothing. Your
  lease has already ended and the CR is held: record nothing (a leased command reads `claim lost`,
  and `handback` is refused while the CR is held; critic run v2, fix 2). Reply
  `[driver <cr>→foreman] stopped: held; worktree clean` or `…; worktree dirty: <files>`, and end.
  The uncommitted work stays in the worktree for the next Driver.
- `driver.md`:762-763, the `claim lost` causes: add `order hold` to the list (`cancel`, `order
  drop`, `order hold`, `agents set <cr> -`) (critic run v2, fix 7).
- "CR driver: re-takes": a take with `unhold: <O-m>` resumes the CR as a `resume:` does (`handoff
  <cr>` for where it stands, the worktree as the stopped Driver left it). In a stack, the CR is now
  on top: rebase onto the branch its `start` line names before the next `ship`. In the same
  section, the paragraph **a note `rebase: <cr> dropped`** (hold-live-cr-Q2; park-live-cr's section
  4 writes the same paragraph, whichever lands first): a held or parked CR this CR waited with was
  dropped out of the batch, in a series or parallel batch; rebase the branch onto the base `take`
  or `handoff` names, leaving out the dropped CR's commits (those of its branch that are not on
  that base), retarget the PR to that base if it was elsewhere, push with `--force-with-lease`,
  `ship`, and go on with the CR's work as before; a conflict is a `conflict-resolver` as for any
  rebase.
- "A CR held out of the stack" (stack driver), for a CR held from live:
  - step 2 skips each CR above that depends on the held CR (out of the stack with it: it keeps the
    held CR's commits);
  - step 3 (rebase the held CR's branch on the default branch) is skipped, whatever its worktree
    (critic run v2, fix 6): a CR held from live is never rebased by the stack driver; its worktree
    may hold its stopped Driver's work, and its next Driver rebases it at its return. Its PR goes to
    a draft and to the default branch by the rebuild, its branch as it stands.
- `driver.md`:1281-1284, the `unhold: <cr>` paragraph (critic run v2, fix 5): it stays for a CR held
  from ready. A CR held from live comes back `blocked` and is taken back `working` by the Foreman:
  it joins as a working CR does ("A working CR placed on another", `foreman.md`): the next `take
  stack` prints it `not on its place`, the Foreman sends its Driver `note rebase: stacked on <cr
  below>`, and the stack driver orders it on top, its dependents above it, as they hand back.

**`chief-of-staff.md`**, "Holding a CR out of a stack" (line 1312) becomes "Holding a CR":

- On the user's word to hold a CR: `order hold <cr>`, for a ready CR of a stack (as today) or a
  live CR in any mode (its slot is freed and its Driver stopped by the Foreman). If it is unclear
  whether the user means out of the order or out of the batch, ask.
- `order unhold <cr>` is the user's word only. Tell the user in one line what the hold did (the CR,
  its slot freed, the batch going on without it).
- A word to drop a CR that is held: run `order drop` only once the hold's order is done (`status`
  shows no pending hold order for it); until then, say so to the user in one line and drop it at
  the Foreman's `order done` (critic run v2, fix 10).
- Batch reports name each held CR. At a batch's end, tell the user that the batch stays open while
  a CR is held. On the release blocked by a held CR, today's ask applies, in every mode.
- In direct mode, the Chief of Staff does the Foreman's part (stop the Driver, `agents set`,
  `order done`, then the freed slot; the take after the unhold; the `rebase: <cr> dropped` notes).
- `chief-of-staff.md`:1075 ("A word that only keeps a ready CR out of the stack is `order hold`,
  not a drop"): becomes "A word that only keeps a CR out of the order for now (a ready CR of a
  stack, or a live CR in any mode) is `order hold`, not a drop" (critic run v2, fix 7).

**`concepts.md`**, "A CR held out of the stack" (line 294): a live CR can be held too, in every
mode. It turns `blocked`, frees its slot, and leaves the stack and the series order with the CRs
that depend on it. It comes back on top on the user's `order unhold`, and no release starts while a
CR is held.

**`routing.md`:** the Foreman → Driver row gets `stop hold: <O-n>` and `rebase: <cr> dropped`. The
Driver → Foreman row gets `stopped: held; worktree clean|dirty: <files>`.

### 9. Docs

- No `README.md` or use-case change (critic run v2, fix 8): `concepts.md` carries the hold of a live
  CR (section 8).
- `scenario/README.md`: the new case (Evidence).

## Out of scope

- The Foreman's `park`, the named `close` refusal and the batch's-end line for a blocked or held CR:
  park-live-cr. Here `close` keeps today's behaviour: a batch with a held live CR is not paused
  (`blocked` is not ended, and the hold order stays pending until `order done`), so `close` refuses
  it with "pause first".
- The destinations `order drop` takes (drop-to-next-batch: never the inbox; P1-P4, `3-ready`, the
  trash, on the user's decision; answers 3 and 4). `order drop` of a held CR keeps its destinations
  here (it unsets the hold; section 1b adds only the line with dependents) and takes whatever
  destinations drop-to-next-batch gives it.
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
test`'s limit). Extend `test_stack_hold.py`, `test_stack_base.py`, `test_order_drop_to.py` (the
drop cases), and `test_rail_refusals.py` for the release:

- **`order hold` refusals** (parametrized, nothing written): a queued CR, a blocked CR, a ready CR
  in a parallel and in a series batch (the new ready text), the release CR, a fix CR, a CR already
  held.
- **`order hold` of a working CR, in each mode** (parametrized: parallel, series, stack):
  - the CR is `blocked`, with `held` set and `blocked_reason` `held: order <O-n>`;
  - the old lease's next leased command is `claim lost`;
  - `handback` of the held CR (with the old lease, and with none, `ready` and `blocked`) is
    refused with the held text, the record unchanged (critic run v2, fix 2);
  - `held(d)` no longer counts it, and a queued CR's `take` is accepted with no change to the slots;
  - the order is pending (`applied` false) until `order done`, while a hold of a ready CR in a
    stack is applied at once (critic run v2, fix 3: the test reads `blocked` after the apply);
  - `take` of the CR is refused with the new mode-neutral text;
  - `order unhold` sets `unheld:`, its order is above every other CR's (in a stack and a parallel
    batch), and `take --note "unhold: …"` is accepted with its `round` unchanged;
  - with no free slot, that take is refused by `check_slot`.
- **The shared definition** (parametrized over `out_of_order`, `apart_owner` and the base rule; the
  same cases as park-live-cr's, a held CR as the apart one): a CR `after` the held CR, one `after`
  that one, and a CR `after` both an in-stack CR and the held one: all three out of order,
  `apart_owner` the held CR; the third's base is the held CR's branch whatever the order of its
  `after` (the in-stack CR is never a base), and with two out-of-order dependencies, the last one
  in the order of `after`; with those two waiting with two different apart CRs, `apart_owner` is
  the last one's apart owner, the CR the base rule picks; messages read `held <p> (order <O-n>)`.
- **The stack:** in a stack of three with the middle CR working, its hold leaves it out of `chain`,
  `top_cr` and `next_merge`. A CR whose `after` names it is out of `chain` too: its base is the
  held CR's branch, it reads `PR in draft`, and `stack <it>` and `stack --out-of-draft <it>` are
  refused naming the held CR. A CR that only started on its branch gets its `start_on` unset.
  `forge-stack rebuild` (the fake forge) moves only the held PR to the default branch.
- **Series** (fix 5; hold-live-cr-Q1; critic run v2, fix 1), a series of four, the second held while
  working:
  - the third queued at the hold: its `take` is accepted once the first is ready; after that take
    its `start_on` is the first's branch, it is not out of order, its base is the first's branch,
    and it is `next_merge` once the first merges and it is ready;
  - the third taken while the second was still working (its `start_on` the second's branch), then
    the second held: the third is `out_of_order` (`apart_owner` the second), not `next_merge` even
    once ready, reads `PR in draft`, `stack --out-of-draft <third>` is refused with `waits with
    held <second> (order <O-n>)`, its base stays the second's branch, and the fourth's predecessor
    skips both;
  - after `order unhold <second>` in that second case, with the fourth still queued: the second's
    order is above every CR that has left `queued` and below the queued fourth, the third right
    above the second, the fourth above both, the line reading `back in the series after its started
    CRs; its dependents above it: <third>`.
- **forge-stack `waiting`**: `forge-stack rebuild` and its check 2 (the fake forge) name a
  dependent's PR `#n of <cr> waits with held <p>: left out of the stack`, not foreign, and leave its
  base unchanged.
- **`order drop` of a held live CR** (hold-live-cr-Q2), to the trash, after the hold's `order
  done`: with no dependent, `held` unset and the line `was held: no stack driver needed`; with a
  dependent in a stack batch, the line naming the dependent and `take stack --note "drop: <cr> to
  <destination>"`, without "no stack driver needed"; with a dependent in a series batch and in a
  parallel one (parametrized), the line naming the dependent and the Foreman's note `rebase: <cr>
  dropped`, with neither "no stack driver needed" nor `take stack`; the dependent is then no longer
  out of order and its base is its series or default base.
- **Leaving a stack** (fix 6): `order mode parallel` on a stack with one held ready CR and one held
  live CR lets the ready one go and keeps the live one held, `blocked`, with a unique order.
- **The release** (fix 7): `take <release>` with a held CR in the batch (a held ready CR of a
  stack, and a held live CR of a parallel batch) is refused with the new text, nothing written. A
  working release's `resume:` take is accepted.
- **`status` and the views** (fix 8): `status` prints the `held: … was working` line with `waiting
  with it`, in a parallel batch. `step` reads `Held`, then `Unheld` after the unhold, and
  `phase_text` reads `held (order <O-n>)`, then `to take back`. The CR's view has the new `now` and
  `next` lines and `severity` red.
- **The cards** (read from the repository at the head under test), added to `test_plugin_files.py`
  (the test that already reads these cards; no new file): `foreman.md` names `stop hold:`,
  `unhold:` and `rebase: <cr> dropped`; `driver.md` names `stop hold:`, `stopped: held` and
  `rebase: <cr> dropped`, and its `claim lost` causes name `order hold`; `chief-of-staff.md`'s
  "Holding a CR" names a live CR; `routing.md` names `stop hold:`.

**Scenario** (`scenario/run_scenario.py`): a new case `hold_live` in the `stack` unit, after
`stack_hold` (raise the unit's budget of 750 s only if the run shows the need), added to the
`UNITS` list (line 84) and to `CASES`:

1. A stack batch of three CRs with 2 slots: take the first two.
2. `order hold` of the second, working: its slot is free, the old lease gets `claim lost`, and
   `order done` follows `agents set <cr> -`; then `take` of the third is accepted.
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

None: hold-live-cr-Q1 closed v1's one question, hold-live-cr-Q2 the drop of a held CR with
dependents (park-live-cr v5's risk), and the critic's run on v2 needed no user.
