# Change Specification: hold a ready CR out of the stack

## Goal

In a stack batch, the user can say "keep this ready CR out of the stack, I merge it later" and
later "put it back". While held, the CR stays in the batch (it is not dropped, not cancelled, not
moved to another stage), but the stack driver's ordering and rebuild, the record's stack and the
forge's native stack all leave it apart. It goes back into the stack only on the user's word.

Seen in batch-28 (order O-25): the user asked to keep CR-381 and CR-382 out of the forge stack to
merge them a week later. `stack <cr>…` puts every CR it does not name on top, and
`forge-stack rebuild` stacks every CR of `chain()` with a PR, so #346 and #347 went back on top of
the new stack #355, the record kept listing them above the top, and the Foreman had to ask (A-39).

## Decisions carried from 02-answers.md

- Priority P1, specified together with its neighbour CR (`order-drop-asks-where-the-cr-goes-trash-`).
- Grilled enough: the intent is the grill; this CR joins batch-29 (factory, stack) once specified.
- The intent's long-term fix is the whole scope: a way to hold a ready CR out of the stack order so
  the stack driver's rebuild, the record and the forge stack leave it apart until the user puts it
  back. The intent names `order hold <cr>` or `stack --out <cr>` as examples; this specification
  picks the order form (below), because holding is the user's word, and the user's word goes
  through `order`.
- A held PR on the forge (settled by the Chief of Staff, 2026-11-20): it goes to draft and onto
  the default branch, so it cannot be merged with the PRs under it by accident; that is what the
  user did with #346 and #347 at batch-28's end.
- A release while a CR is held (settled by the Chief of Staff, 2026-11-20): the release stays
  last. A held CR blocks the release; when the user asks for a release with a CR held, the Chief
  of Staff says so and offers to unhold it, or to take it out of the batch to the backlog (the
  neighbour CR `order-drop-asks-where-the-cr-goes-trash-`).

## What changes

### 1. CLI: two new order kinds, `order hold <cr>` and `order unhold <cr>`

Files: `skills/chantier/scripts/cli/src/chantier/commands/orders_apply.py` (two handlers in
`HANDLERS`, both in `CR_ORDERS`), `declare/orders.py` (the `kind` help lists `hold` and `unhold`),
`commands/orders.py` (nothing special: both are applied at once, `applied: true`, recorded as any
order, `order` event with `order_kind` `hold` / `unhold`).

The record: `CrEntry` (`core/records.py`) gets one field, `held: str | None = None`, the id of the
`order hold` that holds it (`O-25`); unset when not held (`unset("held")`, as other optional
fields, so an old `batch.json` reads unchanged).

`order hold <cr>` refuses, nothing written, exit `EXIT_PRECONDITION`, each with one line naming
the cause:
- the batch is not a stack (`order hold: batch <b> is not a stack: only a stack has an order to
  hold a CR out of`);
- the CR is the release CR or a fix CR (the release is the top piece; a fix already sits outside
  the stack);
- the CR's status is not `ready` (`order hold: <cr> is <status>; only a CR handed back ready is
  held out of the stack`);
- the CR is already held (`<cr> is already held (order O-n)`);
- an open CR of the batch (not merged, not cancelled) has it in its `after`
  (`order hold: <cr2> depends on <cr>: it cannot stand in the stack without it`).

On success it sets `held`, sets `stacked` to False, logs a `hold` event on the CR, and prints:
`<cr> held out of the stack (order O-n): the Foreman takes the stack driver to take it out of the
forge stack; \`order unhold <cr>\` puts it back`.

`order unhold <cr>` refuses when the CR is not held. On success it unsets `held`, sets the CR's
`order` to one above the highest open non-release CR (it comes back on top, under the release, as
a CR added by `order add`), logs an `unhold` event, and prints `<cr> back in the stack, on top:
the Foreman takes the stack driver to place it`.

### 2. CLI: a held CR is outside the stack everywhere the stack is computed

File `skills/chantier/scripts/cli/src/chantier/stacks.py`:
- `chain()` leaves out a held CR (as it leaves out a fix CR). This alone carries the hold to
  `stack_top`, `waived_gate`/`validating_cr`/`validated_ids` (a stack waiver's validating top),
  `stack_base` (the CR above a held one sits on the CR below it), `stack_due`,
  `commands/facts.py:stack_lines` (what `stack` with no CR and `take stack` print), and
  `commands/forge_stack.py:_plan` (so `forge-stack create|rebuild|show` neither stack it nor
  expect it).
- `top_cr()` and `next_merge()` leave out a held CR too (the release starts on the top CR of the
  stack, not on a held one; the next merge of the stack is not the held one).
- `start_on_for()` and the `earlier` search there leave out a held CR (a new CR never starts on a
  held CR's branch).

File `commands/delivery.py:stack`: `stack <cr>…` naming a held CR is refused, nothing written:
`<cr> is held out of the stack (order O-n): \`order unhold <cr>\` first`. The `rest` it places
above already excludes held CRs through `chain()`.

File `commands/orders_reorder.py:reorder` (a mode switch): leaving a stack unsets every `held`
(there is no stack order to be out of any more); its output names each, `<cr>: no longer held
(the batch leaves the stack)`. A switch to a stack finds none held.

File `commands/driver.py:take`: `take <cr>` of a held CR (a new round) is refused:
`<cr> is held out of the stack (order O-n): \`order unhold <cr>\` first`.

### 3. CLI: the forge stack leaves the held PR apart, on the default branch

Files `commands/forge_stack.py`, `commands/forge_stack_gh.py`, `commands/forge_stack_gitlab.py`:
- `_plan` returns, beside the rows and the dropped PRs, the held PRs (number to CR id), read from
  the record: each open CR with `held` and a PR.
- `unstack`/`held_outside` name a held PR found in a stack apart from a dropped or foreign one:
  `it also held #347 of CR-382, held out of the stack: left out`; never "close it".
- `_rebuild` and `_create`, after the unstack phase and before the create call, retarget each held
  PR whose base is not the project's default branch to the default branch (the same `retarget`
  call, one line per PR: `#347 base <old> -> main (held out of the stack)`). A held PR is never
  in the stack created. On GitLab, the same retarget of the held MR, nothing to unstack.
- `_show`'s second check (the stack holds every PR of the stack as it stands, and no other)
  reports a held PR still in the forge stack as its own failing line: `check 2: #347 of CR-382 is
  held out of the stack and still in stack #355: \`forge-stack rebuild\``.

This keeps the cards' rule "never retarget a PR by hand": the held PR moves to the default branch
only through `forge-stack`.

### 4. CLI: `status`, the batch's end and the release

- `status` (the Foreman's and the Chief of Staff's view; `commands/batch_status.py`, through
  `commands/facts.py`) prints one line per held CR, after the stack lines:
  `held: <cr> (order O-n) out of the stack, PR <link> on <default branch>: \`order unhold <cr>\`
  puts it back`. No `STATUS.json` field and nothing the CR board pane draws changes (so no pane
  screenshot is owed); `STATUS.md`, when it lists the CRs, may carry the same word `held` after
  the CR's status.
- A held CR is `ready`, not ended: `all_merged` (`rails.py`) is unchanged, so the batch does not
  end while a CR is held. The user ends that by `order unhold` (then the merge), by merging the
  held PR on the default branch (`order merged <cr>` is accepted for a held CR and unsets `held`;
  its PR is on the default branch), or by taking the CR out of the batch (the neighbour CR's
  `order drop` with its destination; a drop of a held CR unsets `held` like any other field of a
  cancelled CR, nothing else here).
- The release CR is unchanged: it merges last, after every other CR is merged or cancelled
  (`check_merged`), so a held CR blocks the release's merge (settled, 2026-11-20). No CLI change
  here: the Chief of Staff's card carries what to say (section 5).

### 5. Cards

- `skills/chantier/references/chief-of-staff.md`: the user's word to keep a ready CR of a stack out
  of the stack (merge it later, not now) is `$CHANTIER order hold <cr>`; the word to put it back
  is `$CHANTIER order unhold <cr>`. The user's word to take a CR out of the batch is the drop (the
  neighbour CR), not a hold; when the user's word does not say which (out of the stack only, or
  out of the batch), the Chief of Staff asks. A held CR is named in the batch reports as held, and
  at the batch's end the Chief of Staff tells the user the batch stays open while a CR is held.
  When the user asks for the release (or the release's merge) while a CR is held, the Chief of
  Staff says that the held CR blocks the release, names it, and offers two ways out: unhold it
  (`order unhold <cr>`, then it is stacked and merged as any ready CR), or take it out of the
  batch to the backlog (`order drop` with the backlog destination, the neighbour CR
  `order-drop-asks-where-the-cr-goes-trash-`); it acts on the user's answer only.
- `skills/chantier/references/foreman.md`: on an `order hold` or `order unhold` in `status`, take
  the stack driver (`take stack --note "hold <cr>"` / `"unhold <cr>"`), then `order done <O-n>`
  once its hand-back is in. A held CR is never taken for a round.
- `skills/chantier/references/driver.md`, section "Stack driver", one paragraph **A CR held out of
  the stack** next to "A CR dropped from the stack": the PRs above the held CR go to draft first;
  its commits come out of the branches above (by the stack driver for a CR with no live Driver,
  by its Driver on a rebase note for a working CR, as for a drop); the held CR's branch is rebased
  on `origin/<default branch>` and pushed with the Push bullet's rewrite form, and `ship`ped; its
  PR goes to draft (`gh pr ready --undo`, `glab mr update --draft`, then `stack --draft <cr>`);
  `stack <cr>…` orders the rest; `forge-stack rebuild` dissolves the stack, moves the held PR to
  the default branch and makes the stack without it; read back (five checks), the mergeable part
  turned ready again, and the local gate at the mergeable top as the section already asks. A held
  CR at the top of the stack has nothing above it: only its own rebase, draft and the rebuild. On
  `unhold`, the CR comes back on top: it is a ready CR that joins, handled as "A draft that turns
  ready to merge" (ordered below the drafts, rebased, `rebuild`, turned ready, `stack
  --out-of-draft`). The final-order take orders only the CRs of `chain` (held CRs apart). A clean
  rebase carries the CR's gate and verdict as any clean restack; a conflict goes to a
  `conflict-resolver` and the verifier/inspector rule of the section.
- `skills/chantier/references/concepts.md`, "Stack": one sentence, **A CR held out of the stack**
  (`order hold`): a ready CR the user merges later; it stays in the batch, `ready`, outside
  `chain`, its PR a draft on the default branch, until `order unhold` puts it back on top; the
  batch and the release wait for it (the Chief of Staff offers to unhold it or to move it to the
  backlog when the user asks for the release).

`agents/` and `com.github.copilot/agents/` do not change.

## Out of scope

- Taking a CR out of the batch (trash, inbox or backlog, the destination of `order drop`): the
  neighbour CR `2-backlog/P1/order-drop-asks-where-the-cr-goes-trash-`. A held CR stays in the
  batch, `ready`; this CR adds no destination and no stage move.
- Holding a CR in a series or a parallel batch (refused, section 1), and holding a CR that is not
  `ready` (working, blocked, queued).
- Any change to the CR board pane, `STATUS.json`, the web board or the forge hub.
- A schedule (a date to put it back): the user's word puts it back.

## Evidence

Tests (`skills/chantier/scripts/cli/tests/`, in-process, parametrized, kept few; a new
`test_stack_hold.py` or cases added to `test_rail_refusals.py` and `test_mode_switch.py`):
- `order hold` refusals, each with nothing written (`batch.json` and `events.jsonl` byte-equal
  before and after), one parametrized test: a parallel batch, a series batch, the release CR, a
  fix CR, a working CR, a queued CR, an already held CR, a CR another open CR depends on.
  `order unhold` of a CR not held refused the same way.
- `order hold` on a ready CR of a stack: `held` set to the order id, `stacked` False, the order
  recorded `applied`, a `hold` event; `chain`, `stack_top`, `top_cr`, `next_merge`,
  `stack_base` of the CR above it (now on the CR below), and `stack` with no CR leave it out; the
  `status` output carries the `held:` line.
- `stack <held cr>` and `take <held cr>` refused, nothing written.
- `order unhold`: `held` unset, `order` above the highest open non-release CR, back in `chain` on
  top under the release.
- `order mode --note parallel` from a stack with a held CR: `held` unset, named in the output.
- `order merged <held cr>` accepted, `held` unset.
- `forge-stack rebuild` with the fake forge (`forge_world.py` / `scenario/fake_gh.py`): a stack
  holding a held PR in the middle and one at the top; the rebuild unstacks, retargets the held
  PRs to the default branch, creates the stack without them, and names each `held out of the
  stack: left out`; `forge-stack show` on a stack still holding a held PR prints the check 2 line.

Scenario (`scenario/run_scenario.py`, unit `stack`, and its README's list): one step in the stack
unit: two ready CRs stacked, `order hold` on the top one, a scripted stack-driver take that runs
`forge-stack rebuild`; the fake forge's stack holds the other CR's PR only, the held PR is on the
default branch and a draft, `status` prints the `held:` line; `order unhold`, a take, the held CR
back on top of the forge stack. The README names the step with its unit and its tests, as the
coverage test (`test_scenario_coverage.py`) asks.

Gates: `just check`, `just eval-dry-run` (a change under the CLI's `src/`), and the pipeline's
`just scenario (ubuntu-latest)` green at the PR's head (a CLI and cards change); `just test`
within its time budget.

No host or default matrix: nothing here depends on the host or on a configured value.

## Open questions

None: the two questions of the first draft are settled in `02-answers.md` and carried above.
