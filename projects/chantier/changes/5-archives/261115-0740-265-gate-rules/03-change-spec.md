# Change Specification: three long-gate rules (the next merge first, early push, clean rebase)

Origin: verbal (the user, 2026-11-14). No tracker issue.

Grill: `1-inbox/fast-scenario/02-answers.md` (Scen-Q1, the four rules; Scen-Q5, the three-CR
plan) and this CR's `02-answers.md` (GR-Q1, the split). Source text:
`1-inbox/fast-scenario/00-absorbed.md` (`gate-priority`, `long-gate-defaults`). This is the third
of three CRs: `baseline-and-legacy`, then `fast-scenario`, then this one.

**The split (GR-Q1).** This CR keeps rules 1-3. Rule 4 (the stack's one gate) and draft 4 of
`.agents/changes/batch-17-issue-drafts.md` (the waiver recorded per CR, the Long gate column on
every surface) moved to `1-inbox/stack-gate-waiver/`, which comes after this one.

## Starting point

This CR starts from main once `baseline-and-legacy` and `fast-scenario` are merged. That means
the long gate is green on main, the legacy readers are gone (`open_repo` is `Repo.find`), and
`scenario/run_scenario.py` is split into units (`gates`, `stack`, ...), run 4 at a time, with
the README coverage contract and the "Adding a case" rule. If `scenario/run_scenario.py` has no
`UNITS` table when the Driver starts, the Driver stops and says so. Restructuring the scenario
is not this CR's work.

## Goal

The user's words: "que l'on revoit ensemble les règles par défaut d'exécution des Gates
longues".

Batch-17 lost hours between finished work and the user's merges:

- The PR the user was waiting for queued behind another CR's gate.
- A rebased PR was pushed only after its gate, so CI started late. CR-237 lost about an hour.
- A clean rebase onto a docs-only change ran the full gate again.

The principle: what unblocks the user's next merge goes first.

## The three rules (Scen-Q1, carried as decided)

1. **Order.** The PR the user merges next takes first place in the long-gate queue. A gate that
   is already running is never stopped.
2. **Push early.** After a rebase, a PR that already exists is pushed at once and kept in draft,
   so CI runs while its gate waits. It leaves draft once the long gate and CI have both passed at
   the same head. A new PR still waits for its long gate (`AGENTS.md`).
3. **Clean rebase.** A rebase with no conflict runs no new long gate: green CI at the new head
   is enough. A rebase with a conflict runs the gate.

Rule 4 (the stack's one gate) is `stack-gate-waiver`'s.

## What changes

All CLI paths are under `skills/chantier/scripts/cli/src/chantier/`.

### Rule 1: the next merge first in the queue

**Behaviour.** In a stack or series batch, the CR the user merges next is the first CR of the
batch's order that is not merged or cancelled. A fix CR and the release CR do not count. In a
stack that is the bottom of `stacks.chain`; once that CR is merged and its children are
restacked on main, the next one takes the place. A waiting gate of that CR goes ahead of every
other waiting gate. A running gate is never touched.

**The queue.** `commands/gate_queue.py` `ordered` sorts in three steps:

1. the tickets of the next merge;
2. the tickets marked by `gate --first`;
3. arrival order.

The next merge is read from the batch's `batch.json` at each pass of the waiting loop
(`gate_lock.py` `_acquire` already reads the queue once a second). The function stays
read-only, like the rest of `ordered`. `queued_crs`, `gate_state` (`gate queued behind …`) and
`move_first` use the same order.

**A parallel batch.** No CR is "next" by the record, so nothing changes automatically (GR-Q1:
the spec's default). The Foreman's existing `gate <cr> --first --epoch <n>` keeps its
critical-path use and gains one more: the CR the user has said they merge next (an order note,
an ask's answer).

**Cards.**

- `concepts.md`, the long gate paragraph: "the others in arrival order" becomes "the next merge's
  first, then those moved first, then arrival order", with the definition above.
- `driver.md`, the long gate bullet: the same wording.
- `foreman.md`, the `gate --first` bullet: the parallel-batch use. In a stack or series batch,
  `--first` is no longer needed for the next merge.
- `declare/gate.py`: the help text loses "first come first served" and names the order.

### Rule 2: push early for a PR that exists

**Behaviour.** This is the default for every batch, with no `chantier.yaml` key. It applies when
a CR Driver rebases a CR whose PR already exists (a `rebase:` note, a restack, a taken-back CR),
and the rebase needs a long gate (a conflict, by rule 3; `stack-gate-waiver` adds the top of a
waived stack). The Driver then:

1. turns the PR to draft if it is not one already;
2. pushes at once with `--force-with-lease`;
3. runs `ship <cr> <link> --draft`;
4. starts the long gate and the CI watch side by side, as the `ci: beside the long gate` mode
   does today.

The PR leaves draft (`gh pr ready`, `glab mr update --ready`, then `ship` without `--draft`)
only once the gate has passed and CI is green at that same head. A PR that does not exist yet
still waits for its gate before its first push, unless the project chose `ci: beside_gate: true`
(unchanged).

**Cards.**

- `driver.md`: the "Rebase first, so the long gate passes on the head you push" bullet, the long
  gate bullet, the "rebase: merged" paragraph of "CR driver" and the outcomes list of the "CI"
  bullet. Rule 2 reuses the outcomes the `ci: beside the long gate` mode already defines: a red
  CR job stops the gate, a failed gate stops the watch, and both done leads to the Verifier.
- `chief-of-staff.md`, the force-push judgement (step 2): for a branch whose PR is recorded
  (`handoff` prints it), no gate pass at the local head is the rule's order, not a slip. Skip the
  gate check there, as for the `ci:` line. `push refused <branch>: no long gate passed at <sha>`
  stays for a branch with no PR yet.
- `driver.md`'s matching exception line under "A force push the host refuses" changes to match.

**The CLI.** No new refusal. `ship` already accepts a head with no gate pass and prints `off: no
long gate passed at <sha>`. For a CR with a recorded PR, that line reads as expected, not as a
slip. `handback ready` keeps refusing a head with no gate pass (or a carried one, rule 3).

### Rule 3: a clean rebase carries the gate

**Behaviour.** The CLI proves "no conflict" from git itself, not from the Driver's word. At
`handback <cr> ready`, when no gate passed at the PR's head, the CLI looks at the CR's latest
passed gate head. Call it G, and call the current base B (`origin/<base>`). The pass carries
when both hold:

- replaying G's commits onto B is clean and gives exactly the head's tree:
  `git merge-tree --write-tree --merge-base <merge-base G B> B G` exits 0, and the tree it
  prints equals `git rev-parse <head>^{tree}`;
- the head's commits are G's commits rebased, with no commit added, removed or edited by hand.
  Equal trees after a clean replay prove this for the tree. The commit count from the merge-base
  must also match.

In that case the hand-back is accepted. The `handback` event records `gate_from=<G>`, and the
printed line says `long gate carried from <G7> (clean rebase onto <base>)`. In every other case
(a conflict, a resolved conflict, a commit added, a replay that is not clean) the hand-back is
refused as today: `no long gate passed at <head>`. The refusal gains one clause: `(the pass at
<G7> does not carry: <the rebase changed the patch | the replay conflicts>)`.

**What is still needed.** CI green at the new head is the Driver's to read, and the Verifier is
given the move, as today: the CLI reads no forge. A `VERIFIED` verdict at the new head is still
required. A stack driver's clean restack carries in the same way.

**Where.** `commands/driver_checks.py` `handback_refusals` and a new helper beside `gate_passed`
in `commands/crs.py`; `commands/driver.py` `handback` (the event field and the line).

**Git version.** `git merge-tree --write-tree` needs git 2.38 or later. When git is older, the
CLI says so in the refusal and carries nothing: no other method (no fallback).

**Cards.**

- `driver.md`: the "rebase: merged" paragraph, the `note rebase:` paragraph and the stack-driver
  restack. After a clean rebase the Driver runs no long gate. It pushes, `ship`s, reads CI and
  gives the Verifier the move. With a conflict-resolver in the rebase it runs the long gate,
  with rule 2's early push.
- `concepts.md`: the long gate paragraph gets "a pass carries over a clean rebase, which the CLI
  checks".
- The Review box's existing `carried from <sha7>` wording is unchanged.

**The eval kit.** `evals/kit/audit.py`'s C7 check (a passed gate or a `no_gate` hand-back at
each ready CR's head) also accepts a `handback` event with a `gate_from`. Otherwise an eval with
a carried pass fails falsely. `evals/SCORECARD.md`'s C7 row says the same. (`stack-gate-waiver`
adds the waiver.)

## The scenario and the tests

New cases join existing units, following `fast-scenario`'s "Adding a case" rule (no new unit),
and each maps to a coverage bullet of `scenario/README.md`.

- **`gates` unit:**
  - in a stack batch, a later CR's waiting gate goes ahead of an earlier waiting one when it is
    the next merge, and the running gate is not stopped (`status` shows `gate queued behind …`
    in the new order);
  - a clean rebase onto a moved main: `handback ready` is accepted with no new gate, and the
    event has `gate_from` (`stack-gate-waiver`'s Long gate column then shows `carried from`);
  - a rebase with a resolved conflict: refused with the "does not carry" clause.
- **pytest**, in-process and parametrized, in new files under
  `skills/chantier/scripts/cli/tests/` (400 lines per file, 50 per function at most):
  - `ordered`'s three-step order on a prepared queue and `batch.json`;
  - the carry check's refusal text with a git older than 2.38 (mocked version).

## Evidence (done when)

1. The scenario cases above pass in their units. `just scenario` (both forges) is green on the
   user's Windows machine at the PR's head, and is this CR's long gate (`AGENTS.md`: a CLI, card
   and scenario change).
2. `just check` passes on Linux, macOS and Windows.
3. A search of the cards, `README.md`, `CONTRIBUTING.md` and `docs/` finds no "arrival order" or
   "first come first served" left that contradicts rule 1, and no line that has a clean rebase
   run the gate.

## Out of scope

- The work of `baseline-and-legacy` and `fast-scenario`, done before this CR.
- Rule 4 and draft 4: the stack's one gate, the waiver order, the `gate_waiver` record, the
  `gate` object and the Long gate column in status, the pane and the web board
  (`stack-gate-waiver`).
- Reading CI in the CLI: CI stays the Driver's and the Verifier's.
- A change to `ci: beside_gate` for a new PR, or to `long_gate.parallel`.
- The other batch-17 drafts (1-3, 5-15).
- A CI job: none added or changed.

## Risks

- Rule 3 errs toward running the gate: `merge-tree` replays the whole range at once, while
  `git rebase` applies commit by commit. In the rare case where the two give different trees, the
  pass does not carry and the gate runs. The reverse (a carried pass after a real conflict) cannot
  happen: a conflict makes `merge-tree` exit non-zero.
- Rule 1 reads `batch.json` once a second in each waiting gate. Each read is small, and it
  happens only while a gate waits.

## Decided (GR-Q1)

1. **Rule 4 is its own CR**: `stack-gate-waiver`, after this one.
2. **Rule 1 in a parallel batch**: automatic ordering stays with stack and series batches; in a
   parallel batch the Foreman moves a gate first (`gate --first`) on the user's word that they
   merge that CR next.
