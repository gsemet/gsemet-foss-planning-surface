# Park a live CR that waits on something outside the batch

A CR that waits on something outside the batch (the user's trial, an approval, an outside
pipeline or merge) stops holding a slot and the stack. The Foreman parks it without asking
(`park`), as soon as the outside wait is recorded, and tells the user in one line. A parked CR is
`blocked`: it holds no slot, it leaves the stack and the series order, and it stays red in the
batch on the board. Once its wait is cleared, the Foreman starts it again, on top. The user's
`order hold` also works on a live CR. Only the user takes a CR out of the batch (`order drop`,
with the new destination `ready`, the next batch). `close` and the release are refused while a CR
is blocked or held.

## Goal, in the user's terms

From the batch-29 retro (kept point 2). CR-415 waited on the user's phone trial with no Driver at
work. Yet it kept a slot and its place in the stack from 22:18 to 03:38, because `order hold`
takes only a ready CR. The slots were raised three times around it (O-68, O-70, O-73), and in the
end it was dropped to P2 with its work.

What the user accepted (park-live-Q11, all of the Fable advisor's choices): "the Foreman parks a
CR waiting on something outside without asking, frees its slot and tells the user; it stays red
in the batch on the board; it restarts alone on top of the stack when the wait ends; only the
user takes it out of the batch, and `order hold` works on a live CR; `close` and the release are
refused while a CR is blocked". In stack mode, the priority is "ne pas bloquer le reste du stack
pour livrer au max un stack mergeable" (park-live-Q2): not to block the rest of the stack, so as
to deliver as much of a mergeable stack as possible.

## Decisions carried (02-answers.md)

| Answer | Decision | Where it lands below |
| --- | --- | --- |
| Q1 | A CR taken out of the batch goes to P1, P2, the trash or ready (the next batch), never the inbox. The "auto mode" caution is moot (Fable 5, factory-redefine: `3-ready` always means the next batch). | 4 |
| Q2 | The human decides to take a CR out. The Foreman may deprioritize a blocked CR by parking it in the running batch, so that the rest of the stack stays mergeable. | 1, 2, 5 |
| Q3 (A) | The stack goes on without it: it is reordered, and the parked CR comes back on top when it resumes. | 2, 3 |
| Q4 (B) | `close` is refused while a blocked CR is in the batch: the user resumes it or sends it out (P1, P2, trash, ready). | 6 |
| Q6 (A) | Parking frees its slot. Its Driver ends; its worktree and PR stay. A new Driver takes it up once it is unblocked. | 1, 3 |
| Q7 (A) | The Foreman unblocks it once its wait is cleared (the answer recorded, or the hub's `wait-cleared@1`), and starts it again on top. | 3, 5 |
| Q5, Q8 | No new folder: `4-batch/1-pending/` is the running batch, `3-ready` the next one. That is factory-redefine's work; here, "ready" as a drop destination means `3-ready`. | 4; Out of scope |
| Q9 (A) | `blocked` is the state the Foreman sets and clears; `order hold` stays the user's act. | 1, 7 |
| Q10 | Grilled enough; specify after factory-redefine. Spec critic: yes. | (this file) |
| Fable 1 | Reuse the existing `blocked` state (it holds no slot). The Foreman sets it on a live CR. | 1 |
| Fable 2 | `order hold` is accepted on a live CR, with the same effect. Only the user releases it (`order unhold`). | 7 |
| Fable 3 | A CR taken out keeps its branch and PR (as a draft) for P1, P2 or the next batch. The trash closes its PR. | 4 |
| Fable 4 | The Foreman parks without asking, once the outside wait is recorded, and says so in one line. | 1, 5 |
| Fable 5 | The "auto mode" caution is moot. | 4 |
| Fable 6 | CRs that depend on a parked CR wait without a slot. The rest is restacked without it. | 2 |
| Fable 7 | When it comes back and no slot is free, it goes before the queued CRs. No round is counted. | 3, 5 |
| Fable 8 | No release while a CR is blocked: one question to the user, as for `close` (Q4). | 6 |

## Words

- **Parked:** a CR in `blocked` with `parked` set in its record (section 1). Every parked CR is
  blocked; a blocked CR the Foreman has not parked stays as it is today.
- **Outside wait:** a typed wait (`answer`, `approval`, `pipeline`, `merge`; `core/waits.py`) that
  no Driver of the batch can meet: the user's answer or trial, an approval, a pipeline or a merge
  outside the batch.

## What changes

The CLI lives in `skills/chantier/scripts/cli/src/chantier/`, the cards in
`skills/chantier/references/`.

### 1. `park`: the Foreman parks a CR (new command)

**New: `chantier park <cr> --epoch <n> [--wait <type>[=<ref>]]... [--note "<what it waits for>"]`**,
in `commands/park.py`, declared in a new `declare/park.py` (registered as the other declare
modules are). It is role-free like every command: the cards say who runs it (the Foreman; in
direct mode the steering Chief of Staff). It takes the batch's epoch like `take`.

It is accepted on a CR that is:

- `working` (a live CR, its Driver idle or waiting on the outside step); or
- `blocked` (handed back blocked by its Driver), so that it also leaves the stack.

It is refused, with exit precondition and nothing written:

- for any other status: `park: <cr> is <status>: only a working or blocked CR is parked`;
- for the release CR or a fix CR: `park: <cr> is the release CR|a fix CR: it is not parked`. The
  release has its own blocked hand-backs; a fix sits outside the stack;
- for a CR already parked: `<cr> is already parked (since <time>)`;
- for a held CR: `<cr> is held (order <O-n>): the user's hold, not a park`;
- with no outside wait (Fable 4): no open wait on the CR and no `--wait` given:
  `park: <cr> has no outside wait recorded: --wait answer=<question>|approval|pipeline|merge`.

`--wait` takes the types and defaults of `handback --wait` and `wait add` (`commands/waits.py`,
`resolve`), and adds the waits to the CR's `waits` before the park. `--note` defaults to the open
waits' text (`wait_view.what`).

What it does, in one write of the batch:

- `status` becomes `blocked`, with `blocked_reason` `parked: <note>`, and a new `CrEntry` field
  `parked: str | None` gets the time (`core/records.py`, next to `held`, with a comment). The
  reason's `parked:` prefix is what `STATUS.json`, `STATUS.md`, the board and the pane show in
  their existing `blocked` field. No field is added to `STATUS.json` or to the server's protocol.
- Its lease ends (`leases.end(c.lease)`): an old Driver's next command is `claim lost`.
- It leaves the stack as a held CR does (section 2): `stacked=False`, its own `start_on` unset,
  and the open CRs that started on its branch with no dependency on it get theirs unset
  (`orders_hold.hold`'s loop, moved into a shared helper).
- It logs `park` in `events.jsonl` with the waits' ids.
- It prints the line the Foreman sends up:
  `parked <cr>: waits for <waits>; its slot is free and the batch goes on without it; it comes
  back on top once the wait is cleared`.
  For a working CR with an agent recorded, a second line:
  `stop its Driver if it still runs, then \`agents set <cr> - --epoch <n>\``.

`park` changes no file under `4-batch/` but `batch.json` and `events.jsonl`. The CR's folder
stays in `2-actives/`; its worktree, branch and PR stay.

### 2. Out of the stack and the series order; the CRs that depend on it

`stacks.py` gets `is_parked(c)` (parked and not ended), and an `out_of_order(d, c)` that is true
for a held CR, a parked CR, and an open CR whose `after` names (directly or through other CRs) a
parked CR. The latter is computed, never stored (Fable 6).

- `chain`, `top_cr` and `next_merge` leave out every CR that is `out_of_order`, where they
  leave out `is_held` today. The stack is rebuilt without them (Q3): the existing `take stack`
  path, as for a hold.
- **Series:** `rails.series_predecessor` skips a parked CR, as it skips a cancelled one. Its
  successor no longer waits for it.
- **The CRs that depend on it** (Fable 6) stay as they are: a queued one waits without a slot,
  as today (`waits_for`: `blocked` is not met). A working one keeps its Driver and hands back as
  usual, then stays out of the stack until the parked CR is back. `status` names them on the
  parked CR's line (section 5).
- **The release** keeps waiting for the parked CR: `release_waits_for_all` still lists it, and
  `blocked` is not met (section 6).
- **`stack_due`** and the final-order take do not count a parked CR or its dependents, as for a
  held CR.
- `stacks.held_lines` gets a sibling `parked_lines` (section 5).

### 3. Coming back: on top, before the queued CRs

**`take <cr> --note "<why>" --epoch <n>` of a parked CR** (`commands/take_checks.py`,
`check_take_all`, next to `refuse_held`):

- **Refused while a wait is open** (Q7), exit precondition:
  `<cr> is parked, waiting for <w-ids and what>: \`wait <cr> clear <id> --epoch <n>\` first`.
- **Accepted once no wait is open.** It clears `parked` and sets `order` to one above every CR of
  the batch: on top, under the release, as `order unhold` does (Q3). Then it goes on as the
  take-back of any blocked CR: `working`, a new lease, no round counted (Fable 7), a free slot
  needed (`check_slot`). Its line ends `; back on top of the stack` in a stack batch, and
  `; back at the end of the series` in a series.

**Before the queued CRs** (Fable 7). This is a card rule for the Foreman, as for a `context:`
hand-back today ("a blocked CR holds no slot, so it takes the next free one"). `status` helps by
printing the cleared parked CR first (section 5). The CLI adds no refusal of a queued `take`.

Clearing the wait is today's `wait <cr> clear <id> --epoch <n>`, unchanged.

### 4. Taking a CR out of the batch: the user's word, `ready` as a destination

Only the user takes a CR out (Q2). The command stays `order drop <cr> --note <destination>`.

- **New destination `ready`** (Q1, Fable 5): `order drop <cr> --note ready` moves the CR's folder
  to `3-ready/` (the next batch). It keeps its number, `formerly.json` and its open waits
  (`waits.json`), exactly as for the inbox and the backlog.
  - `commands/orders.py`: `_DROP_FOLDERS` gets `"ready": "3-ready"`, and the usage line becomes
    `trash|inbox|ready|P1..P4`.
  - `lifecycle/moveout.py`: `move_out_cr` targets `paths["ready"]` for `3-ready`.
  - `CrEntry.left_to` and `moved_to` accept `3-ready`.
  - `declare/orders.py`: the help lists `ready`.
  - Drop is checked with the folder's name in `3-ready` too (`check_drop_free` already looks there).
- **A blocked or held CR never goes to the inbox** (Q1). `order drop <cr> --note inbox` of a CR
  that is `blocked` or held is refused, exit precondition:
  `<cr> has started: it goes to P1, P2, ready (the next batch) or the trash`. Q1 names P1 and P2
  only, so `P3` and `P4` are refused for it too, with the same text (open question 1).
- **The PR** (Fable 3). For P1, P2 or ready, the branch, worktree and PR stay. The PR is a draft:
  - in a stack, the rebuild by `take stack` does that, as today;
  - outside a stack, when the record says the PR is not a draft (`pr_draft` false), the drop line
    ends `; turn its PR to draft <link>`. The Foreman does it (`gh pr ready <n> --undo`,
    `glab mr update <n> --draft`) before `order done`; so does the Chief of Staff in direct mode.
    This is a second named exception in `foreman.md`'s "Never ... edit a PR", next to closing a
    trashed CR's PR.
  - The trash closes its PR, as today (`close_pr_clause`).
- **A live parked CR** needs no Driver stop: it is `blocked`. Its drop is applied at once, as for
  any CR that is not `working`.

### 5. What `status`, the Foreman and the Chief of Staff say

**`status`** (`commands/batch_status.py`, after `held_lines`) prints one line per parked CR, in
order:

- with an open wait:
  `parked: <cr> since <time>, waits for <w-ids and what>; out of the slots[ and the stack]` and,
  when some CRs depend on it, `; waiting with it: <cr>, ...`;
- with none (the wait cleared):
  `parked: <cr> wait cleared: take it back before any queued CR (\`take <cr> --note "<why>" --epoch <n>\`)`.

The CR's row keeps its `| blocked: parked: …` and `| waits: …` parts, as for any blocked CR.

**`foreman.md`:**

- **When to park** (Q2, Fable 4). A CR whose work waits on an outside step (the user's trial or
  answer, an approval, an outside pipeline or merge) is parked at once, with no question to
  anyone, once that wait is recorded:
  - a working CR whose Driver says it waits on such a step: the wait recorded (`park <cr>
    --wait …`), its Driver stopped, `agents set <cr> -`;
  - a CR handed back `blocked` with such a wait (`question:`, `approval:`, `waits:` with a typed
    `--wait`): `park <cr> --epoch <n>`.
  Then, in a stack, `take stack --note "park <cr>"` rebuilds the stack without it. Send the
  Chief of Staff the line `park` printed: `[foreman→chief-of-staff] parked <cr>: …`.
  A CR blocked on trouble in the work (`fix:`, `infra:`, `rounds:`, `context:`, `refused`) is not
  parked: those paths stay as they are.
- **Coming back** (Q7, Fable 7). On an order line `note <cr> wait cleared: …`, or when `status`
  shows `parked: <cr> wait cleared`: `take <cr> --note "wait cleared: <what>" --epoch <n>`, then a
  new CR Driver, before any queued CR. In a stack, the stack driver places it on top at its next
  take. No round is counted.
- **The final-order take** and **"A held CR"**: a parked CR and its dependents count as a held
  CR does; neither the final-order take nor `take <release>` starts while a CR is parked or held,
  and the ask is the same one (section 6).
- **The heartbeat's end:** a batch with only parked CRs left is a batch "blocked and not
  finished": the heartbeat ends as today, and the order line of a cleared wait wakes the Foreman.

**`chief-of-staff.md`:**

- **On `[foreman→chief-of-staff] parked <cr>: …`:** tell the user in one line, in their
  language: the CR's name, what it waits for, that its slot is free and that the batch goes on.
  Ask nothing (Fable 4).
- **A wait cleared** (the user's answer, or a `wait-cleared@1` line from the watcher): `wait <cr>
  clear <id> --epoch <n>`, then, in Foreman mode, `order note <cr> --note "wait cleared: <what>"`,
  whose order line wakes the Foreman. In direct mode, take the CR yourself, before any queued CR.
  This replaces "then the take-back path as for any blocked CR" for a parked CR in the paragraph
  on typed waits.
- **"Where a dropped CR goes":** add `ready` (the next batch, `3-ready`). A blocked or held CR is
  offered P1, P2, ready or the trash, never the inbox (Q1).
- **"Holding a CR out of a stack"** becomes "Holding a CR": a ready CR of a stack, as today, or a
  live CR in any mode (section 7).
- **Batch reports** (`status-layout.md`): a parked CR is named, with its wait, where held CRs are.

**`routing.md`:** the Foreman → Chief of Staff row gets `parked <cr>: <waits>; …` (the line
`park` prints, passed as it came).

**`driver.md`:** no change. A Driver that waits on an outside step hands back `blocked` with a
typed `--wait`, as today; the Foreman parks it.

### 6. `close` and the release, refused while a CR is blocked or held

**`close`** (Q4, `commands/closing.py`, `_close_target`). Today a batch with a blocked CR never
pauses, so `close` already refuses it, but with "`pause` first", and `pause` then names it among
"not merged". The refusal now names the CR and the user's choices. Before the "not paused"
refusal, when every CR of the batch is merged, cancelled, blocked or held, and at least one is
blocked or held, `close` refuses with exit precondition and deletes nothing:

```
cannot close <batch>: <cr> is blocked (<reason>)[, <cr> is held (order <O-n>)]: resume it
(its wait cleared, or `order unhold <cr>`), or send it out: `order drop <cr> --note
P1|P2|ready|trash`. Nothing was deleted.
```

**The batch's end** (`commands/endpause.py`). When the last other CR ends (`order merged`,
`handback released`, `cancel`, `order drop`) and only blocked or held CRs are left, the batch is
not paused (as today). The command prints one line for the Chief of Staff:
`<batch>: every other CR is merged or cancelled; <cr> is blocked|parked|held (<what it waits
for>): the batch stays open until it comes back or the user sends it out (\`order drop <cr>
--note P1|P2|ready|trash\`)`. The merged CRs' cleanup runs as today.

**The release** (Fable 8). The release already waits for a blocked CR (`waits_for`), so it never
starts while one is in the batch. `take <release>`'s refusal (`rails.check_take`) names a parked
or held CR with its reason: `<release> waits for <cr> parked (<waits>)`. The cards ask the user
once:

- `foreman.md`: the existing ask for a held CR becomes `the release waits: <cr> is parked|held
  (<what>)`, sent once per CR.
- `chief-of-staff.md`: say so, name the CR, and offer the user to wait for it, `order unhold`
  (held), or `order drop <cr>` with the destination the user names. Act on the user's answer only.

### 7. `order hold` of a live CR

`commands/orders_hold.py`, `hold` (Fable 2, Q9). It accepts a `working` CR, in every mode. A ready
CR is still accepted only in a stack, as today (open question 2).

- **Refusals kept:** the release or a fix CR; a CR already held.
- **Status:** a ready CR is refused outside a stack; any status other than `ready` or `working`
  is refused: `order hold: <cr> is <status>; only a live CR, or a ready CR of a stack, is held`.
- **Effect on a working CR:**
  - it becomes `blocked`, with `blocked_reason` `held: order <O-n>` and `held` set as today;
  - its lease ends; its slot is free at once;
  - in a stack it leaves the stack as a held CR does (the `start_on` loop);
  - its dependents follow section 2 (they wait out of the stack). The existing refusal "<cr>
    depends on <held>: it cannot stand in the stack without it" stays for a ready CR only.
- **The line:** `<cr> held (order <O-n>): it was live: the Foreman stops its Driver, then
  \`agents set <cr> - --epoch <n>\` and \`order done <O-n>\`; \`order unhold <cr>\` brings it back`.
  The order stays pending until the Foreman's `order done`, as the drop of a live CR does
  (`commands/orders.py`, the "needs the Foreman's hands" test).
- **`order unhold` of a CR held from live:** today's rule, on top. The line adds `: the Foreman
  takes it back (\`take <cr> --note "unhold: <O-n>"\`), before any queued CR`. `take` of a held
  CR stays refused until the unhold (`refuse_held`). Only the user releases a hold: the Foreman
  never unholds.
- `foreman.md`, "A held CR": a held live CR is stopped (Driver stopped, `agents set <cr> -`,
  `order done`), then, in a stack, `take stack --note "hold <cr>"`. After the unhold, it is taken
  back before the queued CRs.
- `declare/orders.py`: the help reads `hold|unhold (a live CR, or a ready CR of a stack, out of
  the slots and the stack, and back)`.

### 8. Docs

- `README.md` and `docs/use-cases-foreman.md`, `docs/use-cases-direct.md`: a short paragraph on a
  CR that waits outside the batch. It covers parked by the Foreman, the slot freed, back on top,
  taken out only by the user (P1, P2, ready, trash), and `close` and the release waiting for it.
  Place it where `order hold` or blocked CRs are described. If neither file has such a place, add
  it to `README.md` only.
- `docs/batch-lifecycle-texts.md` and `docs/batch-lifecycle.svg`: where they name a blocked CR or
  the close refusal, the parked CR is named the same way, the two files kept in step.
- `scenario/README.md`: the new step (Evidence).

## Out of scope

- The two ready folders and the factory mode's redefinition (Q5, Q8): `factory-redefine`, on
  which this CR depends. Here `ready` only names `3-ready` as a drop destination.
- **Dragging a CR out of `4-batch/1-pending/` on the board.** `factory-redefine`'s Out of scope
  lists it under this CR, but no answer here asks for it. The board "never edits a batch"
  (AGENTS.md), so it would need an AGENTS.md change (open question 3).
- The board's lane "running batch" / "next batch": `board-running-batch-lane`.
- New board views, keys or colours: a parked CR shows in the existing `blocked` (red) state and
  reason. The web client, the terminal client, `board/` and `hooks/register.tsx` are unchanged.
  So no pane screenshot is owed, and no `just mod`.
- A blocked CR's existing paths (`fix:`, `infra:`, `rounds:`, `context:`, `refused`, the release's
  blocked hand-backs, `waits: push`): unchanged.
- The hub and the interest registry: they already read the waits of the running batch's CRs, a
  parked CR's included. No change.
- An outside poller's `issue@1` lines: unchanged.

## Evidence

Every check runs the CLI's real commands on states the CLI itself built (`open`, `take`,
`handback`, `order`), and the card checks read the shipped cards at the head under test.

**Tests** (`skills/chantier/scripts/cli/tests/`, in-process, few and parametrized; `just test`
within its limit). Put them in a new `test_park.py`; extend `test_stack_hold.py`,
`test_order_drop_to.py` and the close tests.

- **`park` refusals** (parametrized; nothing written): queued, ready, merged and cancelled CRs;
  the release CR; a fix CR; a CR already parked; a held CR; no wait and no `--wait`.
- **`park` of a working CR** with `--wait answer=…`:
  - the CR is `blocked` with `parked:`, `parked` set and the wait recorded;
  - the lease is ended, so the old lease's next command is `claim lost`;
  - `held(d)` no longer counts it: the slot is free.
- **`park` of a blocked CR** that carries a wait: accepted with no `--wait`.
- **The stack:**
  - in a stack of three, parking the middle CR leaves it out of `chain`, `top_cr` and
    `next_merge`;
  - a CR that `after`-depends on it is out of `chain` too;
  - a CR that only started on its branch gets its `start_on` unset;
  - `status` prints the `parked:` line, with `waiting with it`.
- **Series:** a parked CR is skipped as the predecessor, and its successor's `take` is accepted.
- **Coming back:**
  - `take` of a parked CR with an open wait is refused (exit precondition, names `wait … clear`);
  - after `wait clear`, `take --note` is accepted, the CR's `order` is above every other CR's,
    `parked` is unset, and `round` is unchanged;
  - with no free slot, it is refused by `check_slot`;
  - `status` prints the `wait cleared: take it back before any queued CR` line.
- **`order hold` of a working CR**, in each mode (stack, series, parallel):
  - the CR is `blocked`, `held` is set, the lease is ended and the slot is free;
  - the order is pending until `order done`;
  - `take` is refused until `order unhold`, then accepted and the CR is on top;
  - `order hold` of a ready CR outside a stack is still refused;
  - a queued CR is refused with the new text.
- **`order drop --note ready`:** the folder lands in `3-ready/<number>-<slug>` with
  `formerly.json` and its open waits. On a blocked or held CR, `inbox`, `P3` and `P4` are refused
  (exit precondition, nothing moved), and `P1`, `P2`, `ready` and `trash` are accepted. Outside a
  stack, a non-draft PR adds `turn its PR to draft`.
- **`close`:** with every other CR merged and one parked (a second case: one held), it is refused
  with the new text and deletes nothing; after `order drop … --note P2` of that CR, the batch
  pauses and `close` is accepted.
- **The batch's end:** the `order merged` of the last other CR prints the "stays open" line,
  naming the parked CR.
- **The release:** `take <release>` with a parked CR in the batch is refused, and the message
  names it as parked.
- **The cards** (read from the repository at the head under test):
  - `foreman.md` names `park` and the `parked <cr>` line;
  - `routing.md`'s Foreman → Chief of Staff row names `parked <cr>`;
  - `chief-of-staff.md` names the `ready` destination and `wait cleared`.
  Add these to the existing card-content test that already reads these files, if one exists, and
  do not add a new file for them.

**Scenario** (`scenario/run_scenario.py`): a new step `park_live` in the `stack` unit, after
`stack_hold` (raise the unit's budget if the run shows it is needed):

1. Open a stack batch of three CRs, with 2 slots, and take the first two.
2. The second CR's Driver records an outside wait and `park` is run: its slot is free, and `take`
   of the third CR is accepted with no change to the slots.
3. `take stack` rebuilds the stack without the parked CR (the fake forge's PR bases show it).
4. The first and third CRs merge. The end prints the "stays open" line, and `close` is refused,
   naming the parked CR.
5. `wait clear`, then `take` brings it back on top, and it merges. The batch pauses and closes.
6. A second batch: `order hold` of a working CR frees its slot, and `order unhold` plus `take`
   brings it back. Then `order drop --note ready` sends a parked CR to `3-ready/`.

Update the step list (line 84) and `scenario/README.md`.

**Gates:**

- `just check` in the worktree.
- `just eval-dry-run` (the change is under the CLI's `src/`).
- The pipeline's `just scenario (ubuntu-latest)` job green at the PR's head (CLI, cards and
  scenario change).
- Windows coverage by `chantier gate` per AGENTS.md, when this CR is on top of its batch's stack.

**No host and default matrix:** the behaviour depends neither on the host nor on a configured
value.

## Open questions

1. **Destinations of other drops.** Q1 says a CR taken out goes to P1, P2, the trash or ready,
   never the inbox. This specification applies that to a blocked or held CR only, and so refuses
   P3 and P4 for it too. Should the restriction also hold for any drop of a started CR (working
   or ready), or should P3 and P4 stay allowed for a blocked CR?
2. **`order hold` of a ready CR outside a stack.** Fable 2 makes `order hold` accept a live CR,
   and this specification allows that in every mode, since the slot is the point. A ready CR
   holds no slot, so its hold stays stack-only, as today. Is that right, or should a ready CR be
   holdable in a series too?
3. **Dragging a CR out of `1-pending` on the board.** `factory-redefine` puts it in this CR's
   scope, but no answer here asks for it, and the board never edits a batch (AGENTS.md). Is it
   wanted? If so, it should be its own CR with the AGENTS.md change, or should it be dropped?
