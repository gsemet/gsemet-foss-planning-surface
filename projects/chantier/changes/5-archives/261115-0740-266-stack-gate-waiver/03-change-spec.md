# Change Specification: the stack's one long gate, and a long-gate waiver recorded per CR

Origin: verbal (the user, 2026-11-14). No tracker issue.

Grill: `1-inbox/gate-rules/02-answers.md` (GR-Q1, the split and its defaults) and
`1-inbox/fast-scenario/02-answers.md` (Scen-Q1, the four rules; Scen-Q5, the plan). Source text:
`1-inbox/fast-scenario/00-absorbed.md` (`gate-priority`, `long-gate-defaults`). It also covers
draft 4 of `.agents/changes/batch-17-issue-drafts.md`: "A long-gate waiver is recorded per CR"
(CR-228 thought its gate was waived, and the follow-up gate on main was left to memory).

Split from `gate-rules` (GR-Q1): that CR keeps rules 1-3 (the next merge first, early push, clean
rebase); this one takes rule 4 and draft 4.

## Starting point

This CR starts from main once `gate-rules` is merged (and, before it, `baseline-and-legacy` and
`fast-scenario`): the queue's next-merge order, the early push for a PR that exists, and the
carried pass over a clean rebase (`gate_from` on the `handback` event) are in place, and
`scenario/run_scenario.py` is split into units.

## Goal

The user's words: "j'aime bien cette idee que l'utilisateur accepte dans le cas d'une stack de
désactiver d'eventuelle gate longue. il faudra que ca apparaisse dans la status, le mod, la ui
webview".

In batch-17 a waiver lived in briefs and in memory: CR-228 believed its gate was waived, and
nobody filed the follow-up gate on main.

The principle: a waiver is a recorded fact on each CR it covers, never a note in a brief.

## The rule (Scen-Q1, carried as decided)

4. **Stack.** The user can choose, at the go or during the run, one long gate on the stack's top
   PR only. The lower PRs are ready to merge once CI is green, the Verifier says VERIFIED and
   they are handed back. This shows in `chantier status` (the text, `STATUS.md` and
   `STATUS.json`), in the CR board pane (`hooks/register.tsx`) and in the web board. Each CR says
   whether its long gate was waived, and which PR carries the stack's validating gate.

Draft 4 adds: the waiver and its scope are recorded as an order on each CR they cover, and the
follow-up is filed when the waiver is given.

## What changes

All CLI paths are under `skills/chantier/scripts/cli/src/chantier/`.

**Rule 2 (from `gate-rules`).** The early push for a PR that exists also applies when the rebase
needs a long gate because the CR is the top of a waived stack.

### The waiver, recorded per CR

**The order.** A new order kind is recorded on the user's word by the Chief of Staff, since
orders are the user's word (`declare/orders.py`, `commands/orders.py`, `orders_apply.py`).
Draft 4 said "the Foreman records". Recording through `order` keeps the user's word as the
source, and the CLI applies it per CR.

- `order waive stack --note "<the user's words>"`: one long gate on the stack's top only. The
  CLI writes a `gate_waiver` (the order's id, `scope: stack`, the note) on every open CR of
  `stacks.chain` that is not a release or fix CR. A CR added later to the stack (`order add`,
  which goes on top) gets the same waiver while the stack's waiver stands. It is refused in a
  batch that is not in stack mode.
- `order waive <cr> --note "<the user's words>" --follow-up <folder>`: a waiver of one CR's long
  gate, with nothing in the batch to validate it (batch-17's case). `--follow-up` names the
  backlog folder (`1-inbox`, `2-backlog/P*`, `3-ready`) of the CR that runs the long gate on main
  afterwards. The order is refused when the option is missing or the folder does not exist. The
  Chief of Staff files that CR first (`$CHANTIER file`), at the waiver, as draft 4 asks. One
  follow-up may serve several waived CRs.
- `order waive stack|<cr> --note -`: withdraws the waiver. The CR needs its long gate again
  before `handback ready`. A CR already handed back stays as it is: its record shows the waiver
  it was handed back under.
- The order is recorded and listed like the others (`status`'s order lines, `order done`).

**The record.** `core/records.py` `CrEntry` gains `gate_waiver: {order, scope, note,
follow_up} | None`. The CR that validates a stack's waiver is not stored. It is derived when
read: the top of `stacks.chain` under the release (`stacks.top_cr`'s rule restricted to the
chain). That CR is never covered while it is the top: its long gate is required, and when a new
CR joins on top, the validation moves to it.

**`handback ready`** (`driver_checks.py`):

- A CR with a `gate_waiver` that is not the stack's top hands back with no gate pass and no
  `--no-gate`. The printed line and the `handback` event say `long gate waived (O-<k>):
  validated by CR-<top>'s gate` (stack scope) or `long gate waived (O-<k>): follow-up <folder>`
  (CR scope).
- The head, clean, pushed and `VERIFIED` checks stay.
- The top CR of a waived stack needs its gate (or a carried pass) as any CR does. A fix found
  by the top's gate goes on the top PR or a PR above it (the user's batch-17 rule).
- `--no-gate "<rule>"` keeps its meaning: an exemption by the project's rules, checked by the
  steering session. A waiver is not a project rule.

**`take` and `handoff`** (`commands/driver.py`, `commands/facts.py`) print one `gate:` line, so
a Driver never guesses:

- a covered CR: `gate: waived (O-<k>, <scope>): run no long gate; validated by CR-<top>`, or
  `follow-up <folder>`;
- the stack's top: `gate: this CR's long gate validates the stack (CR-a, CR-b, …)`.

**Display.** These are the same facts on every surface. `status/views.py` `_row` and `cr_view`
gain one `gate` object:

```
"gate": {
  "state": "none" | "queued" | "running" | "passed" | "carried" | "failed" | "waived" | "exempt",
  "head": "<sha7>" | null,            // the pass, or the carried-from head
  "waiver": "<the order's note>" | null,
  "validated_by": {"cr": "CR-k", "pr": "<url>" | null} | null,   // a covered CR
  "validates": ["CR-a", "CR-b"]                                   // the waived stack's top; else []
}
```

Its sources:

- `queued` and `running`: `gate_lock.gate_state`.
- `passed` and `failed`: the last `gate` events at the CR's head.
- `carried`: the `handback` event's `gate_from`.
- `exempt`: `--no-gate`.
- `waived`: `gate_waiver`.

The surfaces:

- **`chantier status`** (the text, `commands/batch_status.py`) and **`STATUS.md`**
  (`status/markdown.py` `_rows_markdown`): a "Long gate" column, using the same words in both:
  - `passed abc1234`
  - `carried from abc1234`
  - `queued`
  - `running`
  - `failed abc1234`
  - `waived → CR-k (#n)`
  - `validates CR-a, CR-b`
  - `exempt: <rule>`
  - `-`

  The CR's "Long gate" step (`_step_entries`) shows `waived (O-<k>): validated by CR-k (#n)` or
  `carried from <sha7>`, beside today's `waived: <reason>` for `--no-gate`, which becomes
  `exempt: <reason>`. In `status-layout.md`, the paused report's "What the batch did not prove"
  lists each waived CR with its validating CR, or with its follow-up when nothing validates it.
- **`STATUS.json`**: the `gate` object on each CR row and in each CR's `STATUS.json`, read by
  the pane and the board.
- **The CR board pane** (`hooks/register.tsx`, the batch table and the CR page; `types/index.d.ts`
  `ChantierRow` and the CR view type; `hooks/register.test.tsx`): the same "Long gate" column and
  step, with the same words. A change to `hooks/` and `types/` passes `just mod`. Per `AGENTS.md`,
  the PR's Deliverables carry one screenshot of the pane from a real Claude Code session running
  the PR's head, captioned with the head's SHA. Until that screenshot is there, Known gaps says
  "no screenshot of the pane from a real session".
- **The web board** (`board/web/js/`: `model/semantics.js`, the batch view's PR card
  `views/batch-pr-card.js` and `views/batch.js`, the CR panel; `i18n/en.js` and `fr.js` for the
  words): each CR card shows the long gate's word, and a covered CR links to the PR of the CR
  that validates it. Per `CONTRIBUTING.md`, the docs screenshots are retaken
  (`just docs-screenshots`) when the board's drawing changes.

**Cards.**

- `chief-of-staff.md`:
  - the go of a stack batch offers the choice "one long gate on the top PR only" and records it
    with `order waive stack`. During the run, the user's word records it the same way;
  - a waiver of one CR, or of every CR of a batch (one order per CR), is recorded only with
    `order waive <cr> --follow-up <folder>`, after filing the follow-up;
  - the batch plan's gate count leaves out covered CRs and counts the stack's top;
  - the stack's merge offer names the validating CR and whether its gate passed.
- `foreman.md`:
  - the hand-back check: a waived hand-back is checked against the recorded order, not against
    the rules;
  - the ask carries `long gate waived: validated by CR-k` or `follow-up <folder>`;
  - nothing about a waiver goes in a Driver's brief except what `take` prints.
- `driver.md`: a CR whose `take` or `handoff` prints `gate: waived` runs no long gate and hands
  back with no `--no-gate`. The stack's top runs it.
- `concepts.md`: "Order, ask, hand-back" and the long gate paragraph: what a waiver is, who
  records it, where it shows.
- `status-layout.md`: the column, the step and the report line. `routing.md` changes if a
  hand-back or ask line's text changes.
- The agent files (`agents/`, `com.github.copilot/agents/`) do not change: the cards hold the
  contract.

**The eval kit.** `evals/kit/audit.py`'s C7 check (a passed gate, a `no_gate` hand-back or, from
`gate-rules`, a `gate_from` at each ready CR's head) also accepts a `handback` event with a
waiver. Otherwise an eval of a waived stack fails falsely. `evals/SCORECARD.md`'s C7 row says the
same.

## The scenario and the tests

New cases join existing units, following `fast-scenario`'s "Adding a case" rule (no new unit),
and each maps to a coverage bullet of `scenario/README.md`.

- **`gates` unit:** after a clean rebase (`gate-rules`' case), `STATUS.md` shows `carried from`.
- **`stack` unit:**
  - `order waive stack`: a lower CR hands back ready with no gate, while the top is refused
    without its gate;
  - `take` prints the two `gate:` lines;
  - `status`, `STATUS.md` and `STATUS.json` show `waived → CR-k` and `validates …`;
  - an `order add` on top moves the validation to the new CR;
  - `order waive stack --note -` makes the lower CR need its gate again.
- **pytest**, in-process and parametrized, in new files under
  `skills/chantier/scripts/cli/tests/` (400 lines per file, 50 per function at most):
  - `order waive stack` refused outside stack mode;
  - `order waive <cr>` refused without `--follow-up`, or with a folder that does not exist;
  - the `gate` object's state for each source on a prepared record.

## Evidence (done when)

1. The scenario cases above pass in their units. `just scenario` (both forges) is green on the
   user's Windows machine at the PR's head, and is this CR's long gate (`AGENTS.md`: a CLI, card
   and scenario change).
2. `just check` passes on Linux, macOS and Windows; `just mod` passes (`hooks/`, `types/`).
3. The pane screenshot from a real session at the PR's head, captioned with its SHA, is in
   Deliverables, or is named in Known gaps until it is there.
4. The web board shows the column and the link: the retaken docs screenshots
   (`just docs-screenshots`), and one capture of a waived stack in the PR body.
5. `evals/kit/audit.py` C7 passes on the scenario's record of a waived stack (run once, its
   output in the PR body).

## Out of scope

- The work of `gate-rules` (rules 1-3), done before this CR.
- Reading CI in the CLI: CI stays the Driver's and the Verifier's.
- A change to `ci: beside_gate` for a new PR, or to `long_gate.parallel`.
- The other batch-17 drafts (1-3, 5-15), including draft 14 (the stack's merge line carrying
  each CR's gaps), though it sits next to the merge offer above.
- A CI job: none added or changed.

## Risks

- Under a stack waiver the user may merge a lower PR before the top's gate passes. If the top's
  gate then fails, main holds the failure until the fix on the top PR merges. The user accepted
  this in batch-17. The merge offer names the validating CR and its gate's state so the user
  sees it.

## Decided (GR-Q1)

1. **Its own CR**, after `gate-rules`.
2. **A follow-up for a stack waiver**: none. A follow-up CR is filed only for a waiver that
   nothing in the batch validates (`order waive <cr>`); for a stack waiver, the top's gate is the
   validation.
