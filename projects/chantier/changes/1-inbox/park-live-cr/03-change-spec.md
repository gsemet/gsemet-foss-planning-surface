# The Foreman parks a CR stuck on an outside wait

A CR that waits on something outside the batch (the user's trial or answer, an approval, an
outside pipeline or merge) stops holding a slot and the stack. The Foreman parks it without asking
(`park`), once the outside wait is recorded, and tells the user in one line. A parked CR is
`blocked`: it holds no slot, it leaves the stack and the series order, the CRs that depend on it
(a series successor already started on it included) wait with it, and it stays red in the batch on
the board. Once its wait is cleared, the Foreman takes it back, on top, before any queued CR.
`close`, the batch's end and the release wait for it: the user resumes it or sends it out.

Spec v4 (run 4). The user split the first CR in three (park-live-Q12): this CR is part (1). `order
hold` of a live CR is `hold-live-cr`; the `ready` drop destination and the destinations of a
started CR are `drop-to-next-batch` (both in `1-inbox/`). v4 takes in entry 18 (where a parked CR
may be dropped) and nothing else.

## Goal, in the user's terms

From the batch-29 retro (kept point 2). CR-415 waited on the user's phone trial with no Driver at
work. Yet it kept a slot and its place in the stack from 22:18 to 03:38, because nothing could
take a live CR out of the slots. The slots were raised three times around it (O-68, O-70, O-73),
and in the end it was dropped to P2 with its work.

What the user accepted (park-live-Q11, the Fable advisor's choices; the part kept here at
park-live-Q12): "the Foreman parks a CR waiting on something outside without asking, frees its
slot and tells the user; it stays red in the batch on the board; it restarts alone on top of the
stack when the wait ends; ... `close` and the release are refused while a CR is blocked". In stack
mode, the priority is "ne pas bloquer le reste du stack pour livrer au max un stack mergeable"
(park-live-Q2): not to block the rest of the stack, so as to deliver as much of a mergeable stack
as possible.

## Decisions carried (02-answers.md)

| Answer | Decision | Where it lands below |
| --- | --- | --- |
| Q1 | A CR taken out goes to P1, P2, the trash or ready, never the inbox. | Out of scope: `drop-to-next-batch`. Here the cards and refusals name the existing `order drop` only. |
| Q2 | The human decides to take a CR out. The Foreman may deprioritize a blocked CR in the running batch, so the rest of the stack stays mergeable. | 1, 2, 6 |
| Q3 (A) | The stack goes on without it: it is reordered; it comes back on top when it resumes. | 2, 3, 4 |
| Q4 (B) | `close` is refused while a blocked CR is in the batch: the user resumes it or sends it out. | 7 |
| Q5, Q8 | No new folder; `3-ready` is the next batch, `4-batch/1-pending/` the running one. | Out of scope: `factory-redefine`, `drop-to-next-batch`. |
| Q6 (A) | Parking frees its slot. Its Driver ends; its worktree and PR stay. A new Driver takes it up once it is unblocked. | 1, 3 |
| Q7 (A) | The Foreman unblocks it once its wait is cleared (the answer recorded, or the hub's `wait-cleared@1`), on top. | 3, 6 |
| Q9 (A) | `blocked` is the state the Foreman sets and clears; `order hold` stays the user's act. | 1; the hold of a live CR is `hold-live-cr`. |
| Q10, Q11 | Grilled enough; specify now. Spec critic: yes. | (this file) |
| Q12 (A) | Three CRs; this one is the park, its return, the stack and series around it, and `close`, the batch's end and the release refused while a CR is blocked. The other two do not wait for this one. | Out of scope; "Shared with hold-live-cr" |
| Q13 (B) | P3 and P4 allowed for a started CR too. | Out of scope: `drop-to-next-batch`. |
| Q14 (A) | No board drag of a CR out of the running batch now; an idea for later, no CR. | Out of scope |
| Q15 (A) | A series successor already started on the parked CR waits with it, as a dependent: out of the order, its Driver goes on, it is not merged before the parked CR comes back. | Words; "Shared with hold-live-cr"; 2, 3 |
| Entry 17 | (Superseded by entry 18: the inbox for a started CR.) | - |
| Entry 18 | `order drop` never sends a CR out of a batch to the inbox, started or not: P1-P4, `3-ready`, the trash; a parked CR is no exception. | 6, 7, Out of scope: wherever a parked CR's drop is named, the destinations `order drop` takes (drop-to-next-batch: never the inbox; P1-P4, `3-ready`, the trash). |
| Fable 1 | Reuse the existing `blocked` state (it holds no slot); the Foreman sets it on a live CR. | 1 |
| Fable 2 | `order hold` accepted on a live CR. | Out of scope: `hold-live-cr`. |
| Fable 3 | A CR taken out keeps its branch and PR (draft) for P1, P2 or the next batch; the trash closes its PR. | Out of scope: `drop-to-next-batch`. While parked, in the batch, its branch, worktree and PR stay (1, 4). |
| Fable 4 | The Foreman parks without asking, once the outside wait is recorded, and says so in one line. | 1, 6 |
| Fable 5 | The "auto mode" caution is moot. | Out of scope |
| Fable 6 | CRs that depend on a parked CR wait without a slot; the rest is restacked without it. | 2 |
| Fable 7 | Back with no free slot: it goes before the queued CRs; no round counted. | 3, 6 |
| Fable 8 | No release while a CR is blocked: one question to the user, as for `close`. | 7 |

### The spec critic's fixes applied here

Run 1 (v1): (1) `handback` of a parked CR refused: section 1, tested. (2) The readers of `is_held`
read the new predicates: section 2, reader by reader. (3) `driver.md`: a `park: <cr>` note handled
as `hold:`, the dirty worktree case named, the return handled as a `working` CR joining: section 4;
`driver.md` in the card checks (the `3-ready` destinations are `drop-to-next-batch`'s). (4) On
return, the parked CR's open dependents take orders above it, chains kept: section 3, tested. (5)
`rails.series_predecessor` skips every out-of-order CR: section 2, tested with the successor's
`take` in series mode. (7) `take <release>` refused over a parked CR; a CR parked while the release
is taken: the release is taken back with `redo:`: section 7, tested. (8) The pane rule: section 5,
Evidence. Fix 6 (`release_holds`) is `hold-live-cr`'s; `release_holds` reads `held` only, so a
parked CR stays parked across a mode change.

Run 2 (v2):

1. One `out_of_order` definition shared with hold-live-cr, a dependent being "an open CR whose
   `after` names an apart CR, directly or through other open CRs" (plus Q15's series successor);
   each dependent reader names its apart owner, held or parked: "Shared with hold-live-cr",
   section 2.
2. One base rule for a dependent with several open dependencies: "Shared with hold-live-cr".
3. forge-stack's `waiting` covers the dependents of any apart CR, held or parked: section 2.
4. Done by the Chief of Staff (the pointers in `factory-redefine` and `board-running-batch-lane`).
5. Went to the user: answered at Q15, carried.
6. `close` and `left_open` give each CR its own way back (parked, held, other blocked): section 7.
7. In `park`, the held refusal is checked before the status refusal: section 1, tested.
8. The open-wait refusal is in `check_take_all` (read-only, so `access` answers it too); clearing
   `parked` and the reordering are in `take`'s write: section 3, tested.
9. `phase_text` gets a parked branch: section 5, in the pane test.
10. The `agents set <cr> -` line for any parked CR with an agent recorded, and in the Foreman's
    blocked-case bullet: sections 1, 6.
11. The batch reports point to `chief-of-staff.md`'s held-CR line; the release refusal is quoted by
    mode: sections 6, 7.

## Words

- **Parked:** a CR in `blocked` whose record has `parked` set (section 1). Every parked CR is
  blocked; a blocked CR the Foreman has not parked stays as it is today.
- **Outside wait:** a typed wait (`answer`, `approval`, `pipeline`, `merge`; `core/waits.py`) that
  no Driver of the batch can meet.
- **Open:** not merged and not cancelled.
- **Apart:** an open CR that is held or parked: it stands outside the stack and the series order,
  its PR on the default branch.
- **Dependent:** an open CR that is not apart and that waits with an apart CR (its **apart
  owner**), by the shared definition below. A dependent's PR keeps its base on its dependency's
  branch.
- **Out of order:** apart or a dependent. Computed on each call, never stored (Fable 6).

## Shared with hold-live-cr

hold-live-cr (`1-inbox/hold-live-cr`) defines the same notions for held CRs; its specification
v2 holds a copy of this paragraph (v3's, unchanged in v4). Whichever of the two CRs lands first adds the helpers below to `rails.py` and moves
the readers of `is_held` onto them; the second one widens its tests and adds no reader. Both edit
the same functions (`stacks.py`, `rails.series_predecessor`, `rails.check_take`,
`status/words.step`, `status/words.phase_text`, `status/views._now_next`,
`commands/forge_stack_apart.py`): the one that lands second rebases onto the other; neither
depends on the other.

**The definition** (in `rails.py`, which `stacks.py` imports, never the reverse; `is_held` moves
there and `stacks.py` re-exports it for its importers):

- `is_held(c)`: today's (held and open). `is_parked(c)`: `parked` set and open. `apart(c)`:
  `is_held(c) or is_parked(c)`.
- `series_before(crs, c)`: today's `series_predecessor` body, unchanged (the nearest CR before
  `c` in the order that is neither a release nor a fix and not cancelled; a merged one counts).
- `out_of_order(crs, c, mode)`: false for a CR that is not open; true when `apart(c)`; true when
  one of `c`'s open `after` CRs is `out_of_order` (so: "an open CR whose `after` names an apart CR,
  directly or through other open CRs"); and, in a series batch only, true when `c` has left
  `queued` (it is `working`, `ready` or `blocked`) and `series_before(crs, c)` is open and
  `out_of_order` (Q15: the series successor already started on an apart CR, and in turn one
  started on that successor). A queued successor is not a dependent: it is not started, and
  `series_predecessor` gives it the CR before the out-of-order ones. The recursion ends: `after`
  is acyclic and `series_before` goes down the order.
- `series_predecessor(crs, c)`: the nearest CR before `c` that `series_before` would count and
  that is not `out_of_order(crs, x, "series")`.
- `apart_owner(crs, c, mode)`: for an apart CR, itself; for a dependent, the apart CR it waits
  with: the first found walking its open `after` CRs in their order, then (series) its
  `series_before`, recursively. Every message about a dependent names it with its kind: `parked
  <p>` or `held <p> (order <O-n>)`.

**The base rule** for a dependent, one rule whatever its number of open dependencies, before the
series and stack rules of `stacks.start_base` and `stacks.stack_base`: its base is the branch of
the **last out-of-order CR among its candidates**, the candidates being, in this order, its
`series_before` (series batch only, when that CR is open) and then its open `after` CRs in the
order of `after`. There is always one (that is what makes it a dependent). Why not the dependency
highest in the stack (`_nearest_open`): a dependency still in the stack merges or is placed below,
and the apart CR comes back on top of every open CR (section 3), so the apart CR's branch, or a
dependent's above it, ends up holding the others' work; a base in the stack would leave the apart
CR's commits out of the dependent's branch. An apart CR's own base is the default branch, as a held
CR's is today.

**forge-stack's `waiting`** covers the dependents of any apart CR, held or parked (section 2).

## What changes

The CLI lives in `skills/chantier/scripts/cli/src/chantier/`, the cards in
`skills/chantier/references/`.

### 1. `park`: the Foreman parks a CR (new command)

**New: `chantier park <cr> --epoch <n> [--wait <type>[=<ref>]]... [--note "<what it waits for>"]`**,
in `commands/park.py`, declared in a new `declare/park.py` (registered as the other declare
modules are). It is role-free like every command; the cards say who runs it (the Foreman; in
direct mode the steering Chief of Staff). It takes the batch's epoch like `take`. It is part of the
CR lifecycle (AGENTS.md, "The CLI's scope").

Accepted on a CR that is:

- `working` (a live CR, its Driver idle or waiting on the outside step); or
- `blocked` (handed back blocked by its Driver), so that it also leaves the stack.

Refused, exit precondition, nothing written, checked in this order, first refusal raised (critic
run 2, fix 7: the held refusal before the status refusal, so a held CR, `ready` today and
`blocked` once hold-live-cr lands, always reads as held):

1. a held CR: `park: <cr> is held (order <O-n>): the user's hold, not a park`;
2. any status but `working` and `blocked`: `park: <cr> is <status>: only a working or blocked CR is
   parked`;
3. the release CR or a fix CR: `park: <cr> is the release CR|a fix CR: it is not parked` (the
   release has its own blocked hand-backs; a fix sits outside the stack);
4. a CR already parked: `park: <cr> is already parked (since <time>)`;
5. no outside wait (Fable 4): no open wait on the CR and no `--wait` given:
   `park: <cr> has no outside wait recorded: --wait answer=<question>|approval|pipeline|merge`.

`--wait` takes the types and defaults of `handback --wait` and `wait add` (`commands/waits.py`,
`resolve`, `add_to_cr`) and adds the waits to the CR entry's `waits` before the park.

What it does, in one write of the batch:

- `status` becomes `blocked`; a new `CrEntry` field `parked: str | None` gets the time
  (`core/records.py`, next to `held`, with a comment).
- **The reason, the earlier one kept:** `blocked_reason` becomes `parked: <note>`. `--note`
  defaults, for a CR that was `blocked`, to its earlier `blocked_reason` (so `question: which
  colour?` becomes `parked: question: which colour?`), and for a working CR to the open waits' text
  (`wait_view.what`, joined by `; `). The `park` event keeps the earlier reason whole (`was`).
- Its lease ends (`leases.end(c.lease)`): an old Driver's next command is `claim lost`.
- It leaves the stack: `stacked=False`, its own `start_on` unset, and every open CR whose
  `start_on` names the branch of the parked CR or of one of its dependents, and that is not itself
  a dependent, gets its `start_on` unset (the loop of `orders_hold.hold`, moved into a shared
  helper in `stacks.py` that both call).
- It logs `park` in `events.jsonl`, with the waits' ids and `was`.
- It prints the line the Foreman sends up:
  `parked <cr>: waits for <waits>; its slot is free and the batch goes on without it[; waiting
  with it: <cr>, ...]; it comes back on top once the wait is cleared`.
  For any parked CR with an agent recorded, working or blocked (critic run 2, fix 10), a second
  line: `stop its Driver if it still runs, then \`agents set <cr> - --epoch <n>\``.
  In a stack batch, a third: `stack: \`take stack --note "park: <cr>"\``.

`park` writes nothing under `4-batch/` but `batch.json` and `events.jsonl` (and the views they
render). The CR's folder stays in `2-actives/`; its worktree, branch and PR stay.

**`handback` of a parked CR.** A blocked CR can be handed back `ready` with no lease today
(`commands/driver.py`, `_handback_locked`, `was_blocked`), so a parked CR could leave its park that
way. After `live_cr`, a parked CR is refused, exit precondition, nothing written:
`handback: <cr> is parked (since <time>): take it back first (\`take <cr> --note "wait cleared:
<what>" --epoch <n>\`)`.

### 2. Out of the stack and the series order; its dependents

**The predicates** are the shared ones ("Shared with hold-live-cr"). `crs` is the batch's CR list
and `mode` the batch's mode, as `waits_for` takes them.

**The readers**, one by one. Where a reader speaks of a dependent, it names its apart owner
(`apart_owner`) with its kind, parked or held (critic run 2, fix 1):

| Where | Today | Now |
| --- | --- | --- |
| `stacks.chain`, `top_cr`, `next_merge` | leave out `is_held` | leave out `out_of_order`. `stack_due` and `held_lines` follow `chain`. A ready dependent in a series is not the next merge (Q15). |
| `stacks._live_start` | owner not held | owner not `out_of_order` |
| `stacks.start_base`, `stack_base` (the CR's own test) | a held CR: the default branch | an `apart` CR: the default branch; a dependent: the shared base rule, before the series and stack rules |
| `stacks.start_base` (`held_owner`) | owner held | owner `out_of_order` |
| `rails.series_predecessor` | skips release, fix, cancelled | the shared definition: also skips every `out_of_order` CR, so a queued successor no longer waits for a parked CR or its dependents |
| `rails.waits_for` | `<id> <status>` | a parked CR reads `<id> parked`, so the release's refusal and `status`'s `waits for` name it so (section 7) |
| `stack_words._forge_case` | a held owner: `other` | an `out_of_order` owner: `other` |
| `stack_words._ready_word` | held: `PR in draft` | `out_of_order`: `PR in draft` (a ready dependent never reads ready to merge) |
| `stack_words.draft_waited`, `draft_clause` | held: `held_text` | a parked CR: `parked (<waits>): back once its wait is cleared`; a dependent: `waits with parked <p> (<waits>): back once its wait is cleared`, or with a held owner `waits with held <p> (order <O-n>): \`order unhold <p>\`` |
| `commands/delivery.py`, `stack <crs>` and `_check_out_of_draft` | refuse a held CR | also refuse a parked CR (`<cr> is parked out of the stack (since <time>): it comes back with \`take\``) and a dependent (`<cr> waits with parked <p>\|held <p> (order <O-n>): it stays out of the stack until <p> is back`) |
| `commands/forge_stack_apart.held` | held PRs to the default branch, `(held out of the stack)` | `apart` PRs; a parked one's reason reads `(parked out of the stack)` |
| `commands/forge_stack_apart` (new `waiting`, critic run 2, fix 3) | - | the PR of a dependent of any apart CR, held or parked: left out of the native stack, not retargeted (it stays on its base by the shared rule), and named apart in the rebuild's lines and in check 2 as `#n of <cr> waits with parked <p>\|held <p>: left out of the stack`, never as a foreign PR |
| `commands/orders_drop.drop` | unsets `held` | also unsets `parked`, with the line `<cr> was parked: no stack driver needed`, so a dropped CR never reads parked |
| `commands/orders_reorder.py` | `release_holds` reads `held` | no change: a parked CR stays parked when the batch leaves a stack; `reorder` keeps its chains; `series_predecessor` skips it |

**The CRs that wait with it** (Fable 6, Q15) keep their status. A queued one waits without a slot,
as today (`waits_for`: `blocked` is not met). A working one keeps its Driver and hands back as
usual; it stays out of the stack and the series' merge order until the parked CR is back: its PR
stays a draft (`PR in draft`), it is never `next_merge`, and `stack --out-of-draft` refuses it.
This holds for a series successor already started on the parked CR (Q15): its Driver goes on; it
is not merged before the parked CR comes back. `status` names them on the parked CR's line
(section 5).

**The release** keeps waiting for the parked CR: `release_waits_for_all` still lists it, and
`blocked` is not met (section 7).

### 3. Coming back: on top, before the queued CRs

**`take <cr> --note "<why>" --epoch <n>` of a parked CR**, in two parts (critic run 2, fix 8):

- **The refusal, read-only,** in `commands/take_checks.py`, `check_take_all`, right after
  `refuse_held`, so that `access` (which calls `check_take_all` with `read_only=True`) answers it
  too. While a wait is open (Q7), exit precondition:
  `<cr> is parked, waiting for <w-ids and what>: \`wait <cr> clear <id> --epoch <n>\` first`.
- **The write,** in `take` (`commands/driver.py`), after `check_take_all` and before `b.touch`,
  once no wait is open: it clears `parked` and sets `order` to one above every CR of the batch but
  the release (Q3). Then each open dependent takes the places above it, in the order of
  `chains_kept` (`commands/orders_reorder.py`) over their present orders, so that no CR stands
  below one of its `after` and a series successor stands right above it again (critic run 1, fix
  4; Q15). Then it goes on as the take-back of any blocked CR: `working`, a new lease, no round
  counted (Fable 7), a free slot needed (`check_slot`). Its line ends `; back on top of the stack`
  in a stack batch, `; back at the end of the series` in a series, with `; its dependents above
  it: <cr>, ...` when it has any.

**Before the queued CRs** (Fable 7): a card rule for the Foreman, as for a `context:` hand-back
today ("a blocked CR holds no slot, so it takes the next free one"). `status` helps by printing a
cleared parked CR first (section 5). The CLI adds no refusal of a queued `take`.

Clearing the wait is today's `wait <cr> clear <id> --epoch <n>`, unchanged.

### 4. The stack driver: `park:` and the return (`driver.md`)

In "Stack driver", after "A CR held out of the stack", a paragraph **"A parked CR."** Taken with a
note `park: <cr>`, it is handled as `hold: <cr>`, steps 1, 2, 4, 5 and 6, with two differences:

- **Step 3 is skipped: a parked CR's own branch is never rebased by the stack driver.** Its
  worktree may hold its stopped Driver's uncommitted work (the dirty worktree case): no stash, no
  commit, no rebase there. Its PR goes to a draft and to the default branch by the rebuild
  (`parked out of the stack`), its branch as it stands; its next Driver rebases it at its return.
- **Its dependents** stay on their base (the shared rule): they are not rebased and not named in
  `stack <cr>…` (the CLI refuses them); the rebuild leaves their PRs out (`waits with parked
  <p>`). A working dependent's Driver goes on.

**The return.** A parked CR taken back is a `working` CR that is not placed yet: it joins as any
working CR does ("A working CR placed on another", `foreman.md`): the next `take stack` prints it
`not on its place`, the Foreman sends its Driver `note rebase: stacked on <cr below>`, and the
stack driver orders it on top, its dependents above it, as they hand back. `stack --out-of-draft`
refuses it until then.

`driver.md`, "CR driver": no change. A Driver that waits on an outside step hands back `blocked`
with a typed `--wait`, as today; a parked CR's old Driver reads `claim lost` and stops.

### 5. What `status`, the pane and the board show

**`status`** (`commands/batch_status.py`, after `held_lines`): `stacks.parked_lines` prints one
line per parked CR, in order, in every mode:

- with an open wait:
  `parked: <cr> since <time>, waits for <w-ids and what>; out of the slots[ and the stack]` and,
  when it has dependents, `; waiting with it: <cr>, ...`;
- with none (the wait cleared), printed before the other `parked:` lines:
  `parked: <cr> wait cleared: take it back before any queued CR (\`take <cr> --note "wait cleared:
  <what>" --epoch <n>\`)`.

The CR's row keeps its `| blocked: parked: …` and `| waits: …` parts, as for any blocked CR.

**The pane's words** (`status/words.py`, `status/views.py`):

- `step`: a CR whose `blocked_reason` starts with `parked:` reads `Parked` (before the `ASKING`
  test).
- `phase_text` (critic run 2, fix 9): a parked branch first, before the `waits for the user` test:
  with an open wait, `parked: waits for <the waits' what, joined by "; ">`; with none, `parked:
  wait cleared`. (Today a parked CR would read `waits for the user` even when it waits for a
  pipeline.)
- `_now_next`: a parked branch, before `waits_on`. With an open wait: now is the reason (`parked:
  <the earlier reason or the waits>`), next is `Its wait cleared, the Foreman takes it back on top.`
  With none: now is `Parked: its wait is cleared.`, next is `The Foreman takes it back, before any
  queued CR.`
- `severity` is unchanged: red, as any blocked CR.

These change what the CR board pane draws (`STATUS.json`'s step, phase, now and next fields). By
AGENTS.md, the PR's Deliverables carry one screenshot of the pane from a real Claude Code session
running the PR's head, captioned with the head's SHA (seven characters), or its Known gaps name
"no screenshot of the pane from a real session". `hooks/` and `types/` are not touched: `just mod`
is not owed.

**The board** (web and terminal clients, `board/`): no change. A parked CR shows in the existing
`blocked` state (red) with its `parked: …` reason; no field is added to `STATUS.json` or to the
server's protocol. No drag out of the running batch (Q14).

### 6. The cards

**`foreman.md`:**

- **When to park** (Q2, Fable 4). A CR whose work waits on an outside step (the user's trial or
  answer, an approval, an outside pipeline or merge) is parked at once, with no question to
  anyone, once that wait is recorded:
  - a working CR whose Driver says it waits on such a step: `park <cr> --wait … --epoch <n>`, its
    Driver stopped, `agents set <cr> - --epoch <n>`;
  - a CR handed back `blocked` with such a wait (`question:`, `approval:`, `waits:` with a typed
    `--wait`): `park <cr> --epoch <n>`, then, when `park` prints the `agents set` line (an agent
    still recorded), `agents set <cr> - --epoch <n>` once its Driver has ended (critic run 2, fix
    10).
  Then, in a stack, `take stack --note "park: <cr>"`. Send the Chief of Staff the line `park`
  printed: `[foreman→chief-of-staff] parked <cr>: …`.
  A CR blocked on trouble in the work (`fix:`, `infra:`, `rounds:`, `context:`, `refused`) is not
  parked: those paths stay as they are.
- **The CRs that wait with it** (Fable 6, Q15): a working dependent, a series successor already
  started on it included, keeps its Driver; its PR stays a draft and it is not merged before the
  parked CR comes back.
- **Coming back** (Q7, Fable 7). On an order line `note <cr> wait cleared: …`, or when `status`
  shows `parked: <cr> wait cleared`: `take <cr> --note "wait cleared: <what>" --epoch <n>`, then a
  new CR Driver, before any queued CR. In a stack it joins as a working CR (section 4). No round is
  counted.
- **The final-order take:** a parked CR and its dependents count as a held CR does (out of it), and
  a queued CR whose dependency is parked is one "whose dependency is blocked".
- **The release** (section 7): neither the final-order take nor `take <release>` starts while a CR
  is parked; one ask per CR: `the release waits: <cr> is parked (<what it waits for>)`. A CR parked
  while the release is working or ready: once it is back and handed back ready, `take <release>
  --note "redo: <cr> back from park"`.
- **The heartbeat's end:** a batch with only parked or blocked CRs left is "blocked and not
  finished": the heartbeat ends as today, and the order line of a cleared wait wakes the Foreman.

**`chief-of-staff.md`:**

- **On `[foreman→chief-of-staff] parked <cr>: …`:** tell the user in one line, in their language:
  the CR's name, what it waits for, that its slot is free and that the batch goes on. Ask nothing
  (Fable 4).
- **A wait cleared** (the user's answer, or a `wait-cleared@1` line from the watcher), in the
  paragraph on typed waits: for a parked CR, `wait <cr> clear <id> --epoch <n>`, then, in Foreman
  mode, `order note <cr> --note "wait cleared: <what>"`, whose order line wakes the Foreman; in
  direct mode, take the CR yourself, before any queued CR. This replaces "then the take-back path
  as for any blocked CR" for a parked CR.
- **The batch's end, `close` and the release** with a parked or blocked CR (section 7): name the CR
  and what it waits for, give its way back as the CLI's line names it, and offer the user to wait
  for it or to send it out (`order drop <cr> --note <destination>`, the destinations `order drop` takes (drop-to-next-batch: never the inbox; P1-P4, `3-ready`, the trash)). Act on the
  user's answer only.
- **Batch reports** (critic run 2, fix 11): in "Holding a CR out of a stack", next to "Name each
  held CR in the batch reports", the same for a parked CR, with what it waits for; and next to
  "No release starts while a CR is held", the same for a parked CR, its way back being its wait
  cleared, then `take`.

**`routing.md`:** the Foreman → Chief of Staff row gets `parked <cr>: <waits>; …` (the line `park`
prints, passed as it came).

**`driver.md`:** section 4.

### 7. `close`, the batch's end and the release, while a CR is blocked

**Each CR's way back** (critic run 2, fix 6), one text written once in `endpause.py`
(`way_back(c)`) and used by `close` and `left_open`:

- a parked CR with an open wait: `<cr> is parked (<waits>): its wait cleared (\`wait <cr> clear
  <id> --epoch <n>\`), then \`take <cr> --note "wait cleared: <what>" --epoch <n>\``;
- a parked CR whose wait is cleared: `<cr> is parked, its wait cleared: \`take <cr> --note "wait
  cleared: <what>" --epoch <n>\``;
- a held CR (ready today, or blocked once hold-live-cr lands): `<cr> is held (order <O-n>): the
  user's \`order unhold <cr>\``;
- any other blocked CR: `<cr> is blocked (<reason>): take it back (\`take <cr> --note "<why>"
  --epoch <n>\`)`.

**`close`** (Q4, `commands/closing.py`, `_close_target`). Today a batch with a blocked CR never
pauses, so `close` refuses it with "`pause` first", and `pause` then names it among "not merged".
Now, after `check_idle` and before the "not paused" refusal: when every CR of the batch is merged,
cancelled, blocked or held, and at least one is not ended, `close` refuses, exit precondition,
nothing deleted:

```
cannot close <batch>: <way back of each CR left, joined by "; ">; or send it out (`order drop
<cr> --note <destination>`). Nothing was deleted.
```

`<destination>`, here and in `left_open`'s line: the destinations `order drop` takes (drop-to-next-batch: never the inbox; P1-P4, `3-ready`, the trash).

**The batch's end** (`commands/endpause.py`). The ending commands (`handback` in
`commands/driver.py`, `order merged` and `order drop` in `commands/orders.py`, `cancel` in
`commands/release.py`) call `end_of_batch` only when every CR has ended. New in `endpause.py`:
`left_open(d)`, called by the same commands when a CR ended in this command and every CR not ended
is blocked or held (at least one). It pauses nothing and cleans nothing, and prints one line for
the Chief of Staff:
`<batch>: every other CR is merged or cancelled; <way back of each CR left, joined by "; ">: the
batch stays open until it comes back or the user sends it out (\`order drop <cr> --note
<destination>\`)`.

**The release** (Fable 8). The release already waits for every open CR (`release_waits_for_all`),
and `blocked` is not met in any mode, so `take <release>` is refused while a CR is parked. With
section 2's `waits_for`, `rails.check_take`'s refusal names it, its end by mode as today (critic
run 2, fix 11):

- in a stack or series batch: `<release> waits for <cr> parked: it starts once each is handed
  back ready or merged`;
- in a parallel batch: `<release> waits for <cr> parked: it starts once each is merged or
  cancelled`.

A CR parked while the release is working or ready: the release's PR stays a draft (the stack
driver's step 1), and the Foreman takes the release back with `redo:` once that CR is back and
ready (section 6); `check_take` already refuses that take-back while the CR is unmet.

### 8. Docs

- `README.md`, `docs/use-cases-foreman.md`, `docs/use-cases-direct.md`: a short paragraph on a CR
  that waits outside the batch: parked by the Foreman, its slot freed, its dependents (a started
  series successor included) waiting with it, back on top once its wait is cleared, and `close`
  and the release waiting for it. Place it where blocked CRs are described; with no such place, in
  `README.md` only.
- `docs/batch-lifecycle-texts.md` and `docs/batch-lifecycle.svg`: where they name a blocked CR or
  the close refusal, the parked CR is named the same way, the two files kept in step.
- `scenario/README.md`: the new step (Evidence).

## Out of scope

- **`order hold` of a live CR**, in every mode, and `release_holds` keeping the hold of a CR that is
  not ready (critic run 1, fixes 6 and 7's held case): `hold-live-cr` (park-live-Q12). This CR
  keeps `order hold` as it is and reads `is_held` through `apart` and `out_of_order` without
  changing what a hold does; the way-back text of a held CR (section 7) is the only held line it
  writes.
- **Where a CR taken out of the batch goes**: the `ready` drop destination (`3-ready`, the next
  batch), the destinations of a started CR, a parked one included (the destinations `order drop` takes (drop-to-next-batch: never the inbox; P1-P4, `3-ready`, the trash); Q1, Q13,
  entry 18), its PR turned to draft (Fable 3), and the `3-ready` destinations in
  `driver.md` and `foreman.md`: `drop-to-next-batch` (park-live-Q12). Here the cards and lines
  name `order drop <cr> --note <destination>` as it stands.
- The two ready folders and the factory mode's redefinition (Q5, Q8): `factory-redefine`.
- **Dragging a CR out of the running batch on the board** (Q14): not now. The user says it in a
  message; it is an idea for later, with no CR.
- The board's "running batch" / "next batch" lane: `board-running-batch-lane`.
- New board views, keys or colours; the web client, the terminal client, `board/` and
  `hooks/register.tsx` are unchanged.
- A blocked CR's existing paths (`fix:`, `infra:`, `rounds:`, `context:`, `refused`, the release's
  blocked hand-backs, `waits: push`): unchanged, but for their way-back line at `close` and the
  batch's end (section 7).
- The hub and the interest registry: they already read the waits of the running batch's CRs, a
  parked CR's included.

## Evidence

Every check runs the CLI's real commands on states the CLI itself built (`open`, `take`,
`handback`, `park`, `order`), and the card checks read the shipped cards at the head under test.

**Tests** (`skills/chantier/scripts/cli/tests/`, in-process, few and parametrized; `just test`
within its limit). A new `test_park.py`; extend `test_stack_hold.py`, `test_stack_base.py`,
`test_batch_end.py` and the close tests.

- **`park` refusals** (parametrized; nothing written): queued, ready, merged and cancelled CRs; the
  release CR; a fix CR; a CR already parked; no wait and no `--wait`; and a held ready CR, whose
  refusal is the held text, not `is ready` (the held check first, critic run 2, fix 7).
- **`park` of a working CR** with `--wait answer=…`: the CR is `blocked` with `parked: …`, `parked`
  set and the wait recorded; the old lease's next command is `claim lost`; `rails.held(d)` no
  longer counts it; with an agent recorded, the `agents set` line is printed.
- **`park` of a blocked CR** that carries a wait: accepted with no `--wait`; `blocked_reason` reads
  `parked: <the earlier reason>`, and the `park` event's `was` holds it; with an agent still
  recorded, the `agents set` line is printed (fix 10).
- **`handback ready` of a parked CR** (no lease): refused, exit precondition, the record unchanged.
- **The shared definition** (parametrized over `out_of_order`, `apart_owner` and the base rule): a
  CR `after` a parked CR, one `after` that one (through another open CR), and a CR `after` both an
  in-stack CR and a parked one: all three out of order, `apart_owner` the parked CR; the third's
  base is the parked CR's branch whatever the order of its `after` (the in-stack CR is never a
  base), and with two out-of-order dependencies, the last one in the order of `after`; a held CR in
  place of the parked one gives the same results, its messages reading `held <p> (order <O-n>)`.
- **The stack** (a stack of three, the middle one parked, one CR `after`-depending on it, one that
  only started on its branch): the parked CR and its dependent are out of `chain`, `top_cr` and
  `next_merge`; the other's `start_on` is unset; `stack_base` gives the parked CR the default
  branch and the dependent the parked CR's branch; `stack <crs>` and `stack --out-of-draft` refuse
  both with their texts (the dependent's naming `parked <p>`); a ready dependent reads `PR in
  draft`; `status` prints the `parked:` line with `waiting with it`; `forge_stack_apart` lists the
  dependent's PR in `waiting`, not retargeted, and check 2 does not read it as foreign.
- **Series** (critic run 1, fix 5; Q15): a series of four, the second parked. A queued third is
  given the first as predecessor and its `take` is accepted once the first is ready. In a second
  case the third was taken while the second was ready, then the second was taken back and parked:
  the third is a dependent (`out_of_order`, `apart_owner` the second), its base stays the second's
  branch, it is not `next_merge` once ready (`PR in draft`), and the fourth's predecessor skips
  both.
- **Coming back:** `take` of a parked CR with an open wait is refused (names `wait … clear`), and
  `access <cr>` on the same state names the same refusal (fix 8); after `wait clear`, `take --note`
  is accepted, the CR's `order` is above every other CR's but the release's and its dependents'
  orders are above it with their chains kept, the series successor right above it (critic run 1,
  fix 4; Q15), `parked` is unset and `round` unchanged; with no free slot `check_slot` refuses it;
  `status` prints the `wait cleared: take it back before any queued CR` line first.
- **`order drop` of a parked CR** to the trash: `parked` unset, the line `was parked` printed.
- **The pane's words:** `step` reads `Parked`; `phase_text` gives `parked: waits for …` and
  `parked: wait cleared` (fix 9); `_now_next` gives the two parked pairs (open wait, cleared).
- **`close`** (parametrized over the way back, fix 6): every other CR merged and one CR left
  parked with an open wait, parked with its wait cleared, held, or blocked on another reason (say
  `infra:`): refused, each text naming that CR's own way back, nothing deleted; after `order drop
  … --note P2` of that CR, the batch pauses and `close` is accepted.
- **The batch's end:** the `order merged` of the last other CR prints the "stays open" line naming
  the parked CR and its way back, and the batch is not paused.
- **The release:** `take <release>` with a parked CR is refused, the message naming it `parked`,
  in a stack batch (`handed back ready or merged`) and in a parallel one (`merged or cancelled`).
- **The cards** (read from the repository at the head under test): `foreman.md` names `park` and
  the `parked <cr>` line; `routing.md`'s Foreman → Chief of Staff row names `parked <cr>`;
  `chief-of-staff.md` names `wait cleared` for a parked CR and a parked CR next to the held-CR line
  of "Holding a CR out of a stack"; `driver.md` names `park: <cr>`. Add them to the existing test
  that reads these cards (`test_plugin_files.py`), no new file.

**Scenario** (`scenario/run_scenario.py`): a new case `park_live` in the `stack` unit, after
`stack_hold` (raise the unit's budget only if the run shows it is needed):

1. Open a stack batch of four CRs, one `after` the second, with 2 slots, and take the first two.
2. The second CR's Driver records an outside wait and `park` runs: its slot is free, and `take` of
   the third CR is accepted with no change to the slots; the fourth (its dependent) stays queued.
3. `take stack` rebuilds the stack without the parked CR (the fake forge's PR bases show it on the
   default branch).
4. The first and third CRs merge. The ending command prints the "stays open" line, and `close` is
   refused, naming the parked CR and its way back.
5. `wait clear`, then `take` brings it back on top; it and its dependent merge. The batch pauses
   and closes.

Update the `stack` unit's case list (line 84) and `scenario/README.md`.

**Gates:**

- `just check` in the worktree.
- `just eval-dry-run` (the change is under the CLI's `src/`).
- The pipeline's `just scenario (ubuntu-latest)` job green at the PR's head (CLI, cards and
  scenario change).
- Windows coverage by `chantier gate` per AGENTS.md, when this CR is on top of its batch's stack.
- The pane screenshot, or its absence named in Known gaps (section 5).

**No host and default matrix:** the behaviour depends neither on the host nor on a configured
value.

## Open questions

None. (v1's question 1 is answered at park-live-Q13 and goes to `drop-to-next-batch`; question 2
is dropped with the hold; question 3 is answered at park-live-Q14; critic run 2's finding 5 at
park-live-Q15; entry 17 is superseded by entry 18, carried.)
