# Change Specification: who turns a dependent draft PR ready, once its dependency merges

## Goal

In a parallel batch, a CR with an `after` (its dependencies, `depends.json`) stands on the branch
of a dependency still open: its Driver hands back `ready <link> draft on <base>: waits for
<what>` and ends. When that dependency merges, nobody owns the next step today (left open by PR
69, CR-131). The owner is the **steering session** (the Foreman, or the Chief of Staff in direct
mode); the work is a Driver's.

## What changes (cards only; the CLI adds nothing)

### 1. `skills/chantier/references/foreman.md`

When an `order merged <dependency>` is recorded (the user's, or the Foreman's own with
`--epoch`), for each CR of the batch that was handed back ready as a draft waiting for that
dependency, and whose dependencies are now all merged, send it back to a Driver at once, as any
CR sent back: `take <cr> --note "rebase: <dependency> merged"` and a new CR Driver started with
that `take` output (it takes a slot; with none free it waits for one like any queued CR). A CR
still waiting for another open dependency is rebased onto that one instead and stays a draft:
the note says which. In a stack batch nothing changes: the stack driver already restacks after a
partial merge.

### 2. `skills/chantier/references/driver.md` (CR driver)

A CR taken with a note `rebase: <dependency> merged`: fetch, rebase the branch onto
`origin/<default branch>` (a `conflict-resolver` for a conflict that only needs resolving; one
that needs code is a round), retarget the PR to the default branch (`gh pr edit --base`, `glab mr
update --target-branch`), push with `--force-with-lease` (a refused one goes up as written), `ship`,
read CI (a red check is a round), and when green and mergeable turn the PR ready and `handback
ready <link>`. No new round of the coder when the rebase is clean and CI is green.

### 3. `skills/chantier/references/chief-of-staff.md`

"Steering a batch yourself" already points to the Foreman's card; check it says the same owner
rule applies in direct mode (one sentence if not).

## Evidence

Read the three cards: the rule is stated once in the Foreman card, the Driver knows what to do
with the note, and no card still says the question is open. `just check` passes; `just scenario`
passes (the scenario covers a parallel batch with `depends.json`; extend it only if it already
plays the dependency's merge).
