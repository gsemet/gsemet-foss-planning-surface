# Stack batch frictions: restack line, true bases, carry, lease commands

Short name: `stack-frictions`. Destination: the next batch (3-ready). Repository:
`C:/Users/gaeta/Projets/chantier`. It touches the CLI (`skills/chantier/scripts/cli/src/chantier/`),
its tests, two cards (`driver.md`, `foreman-stack.md`) and one scenario check. It closes two inbox
items: `take-prints-the-old-worktree-base-after-` and `foreman-s-stack-lease-goes-stale-with-no`
(both folded in by `02-answers.md`; the Chief of Staff moves them to the trash once this CR's PR
is open).

## Goal

The user's words (2026-11-22, batch-30, a `stack` batch): four frictions slowed the stack. A
GitHub rebase merge left the next PR showing the merged CR's commits again. `take` printed wrong
bases. `ship` printed `off:` after a clean restack. Dead Drivers' leases blocked `ship` until
someone reclaimed them by hand. This CR makes the CLI say what the stack now owes, print true
bases, carry a clean restack, and name the exact command in each lease refusal. It adds no new
command and no new tool.

## Decisions carried (02-answers.md)

- **stack-frictions-D1:** `order merged` in a stack batch prints one line: a restack is owed, and
  who owes it. It is a printed line, not a new tool. CR-466's pre-authorised rebase and
  force-with-lease, and the stack driver's one-pass restack, stay as they are (section 1).
- **stack-frictions-D2:** fix `take`'s wrong bases, including after a reorder. This folds in
  `take-prints-the-old-worktree-base-after-` (section 2).
- **stack-frictions-D3:** `off:` where `carried:` belongs after a clean restack is a defect of
  the carry code (`commands/carry.py`): fix it (section 3).
- **stack-frictions-D4:** dead Drivers' claims block `ship`. The cards already let the steering
  session end a lease once the host shows its holder ended (`foreman.md`). What stays is that
  each refusal names the exact command. This folds in `foreman-s-stack-lease-goes-stale-with-no`
  (section 4).

## What changes

### 1. `order merged` names the restack the stack owes (D1)

**Where:** `_merged` in `skills/chantier/scripts/cli/src/chantier/commands/orders_apply.py` (359
lines). The new line is built by a small function in `commands/orders_merged.py` (38 lines), so
`orders_apply.py` stays under 400 lines.

**When it prints:** all of these hold:

- the batch's mode is `stack`;
- the merged CR is neither a release nor a fix, and was in the stack's chain (`stacks.chain`,
  read before the CR is marked merged);
- at least one CR of the chain above it, left open by this merge, has a PR recorded.

Otherwise nothing new prints: a parallel or series batch, a fix CR, the release, or nothing open
above.

**What it says:** one line, right after `merged <cr>: moved to 3-done`. The CRs are listed in
chain order, bottom first:

- With no stack driver recorded (`stack_agent` empty):
  `restack owed: <cr>, <cr> stood on <merged cr>'s branch; the stack driver restacks them in one pass: one \`take stack --epoch <n>\` once every CR this merge merged is recorded`
- With a stack driver recorded:
  `restack owed: <cr>, <cr> stood on <merged cr>'s branch; the stack driver <agent> restacks them in one pass: send it the note \`merged: <merged cr>\``

`--epoch <n>` is written as is, the form the CLI's other messages use. The line changes nothing
in the record and logs no event. The Chief of Staff relays `order merged`'s lines to the Foreman,
as its card already says. In direct mode it does the restack itself.

The line reflects `foreman-stack.md`'s "After a merge" rule ("one `take stack` for what remains
... or the note `merged:` to the one that runs"). The rebase itself stays the stack driver's
one-pass restack in `driver.md` ("After a partial merge"). The CLI runs no git for it.

### 2. `take`, `round` and `handoff` print the base of the CR's place (D2)

At main, `cr_facts`' `worktree:` line (`commands/facts.py`, `_base_of`) gives two kinds of wrong
base in a stack batch:

- **A stacked CR with a PR** prints its PR's base as read from the forge (`stacked_read`). After a
  reorder, or before `forge-stack rebuild`, that is the old base. The `stack` and `take stack`
  rows print the planned base (`_stack_ref`, `stack_base(..., planned=True)`) for the same CR, so
  the two outputs disagree.
- **Any other CR of the chain** prints `start_base`, which goes through `stacks.stack_start`.
  Rule 1 there returns the CR's recorded `start_on` while the CR that owns that branch is open.
  After a reorder (`stack <crs>`, `order mode --note stack`'s `reorder`) the owner may sit above the CR,
  and the base printed is the branch the worktree started on, not the CR's place.

The change:

- **One base for the line.** In a stack batch, for a CR of the chain (the release included, a fix
  CR not), the `base <ref>` of the `worktree:` line is `stack_base(d, c, repo, planned=True,
  landed=landed)`. That is the base the CR's row in `stack` / `take stack` prints, with the CRs
  the forge shows merged (`landed`) read as ended. A fix CR, and every CR of a parallel or series
  batch, keeps `start_base` as today.
- **`start_on` follows the order.** In `stacks.stack_start`, rule 1 (`_live_start`) holds only
  while the CR that owns `start_on` also sits below the CR in `chain`. When the order puts it
  above (or takes it out of the chain), rule 1 no longer applies and the next rules give the base
  as they do today:
  - a CR not placed with an open dependency gets its highest open dependency's branch;
  - a queued CR gets the start candidate;
  - a taken CR with neither gets the base a queued CR would get. That is the nearest CR below it
    in `chain` with a PR, when that CR is handed back `ready`, else the default branch. This rule
    is new for a taken CR whose `start_on` no longer holds; today rule 2 always gives the default
    branch.

  The recorded `start_on` itself is not rewritten. `stacks.py` has 398 lines: what the change
  adds moves an existing helper out (for instance `held_lines` into `stack_apart.py` or a new
  module), so the file stays at 400 lines or fewer.
- **The forge's base stays visible.** The forge read that AGENTS.md names for `take`, `round` and
  `handoff` (`stacked_read`, a stacked CR with a PR) still runs once per CR printed. Its result
  goes after the base, separated by `; `:
  - read, and equal to the place: nothing is added;
  - read, and different: `; PR on <ref>`, with `<ref>` written as `_ref` writes a base
    (`origin/main` for the default branch);
  - read failed: `; PR base ? (not read from <link>: <the forge's text, one line>)`. This keeps
    the `base ? (not read from <link>: …)` text that AGENTS.md quotes.

  For example: `worktree: <path> branch chantier/cr-12-x base chantier/cr-11-y; PR on origin/main`.
- **The `Rewrites:` line** (`driver_prompt.py`, `_WORKTREE_LINE`, `base ([^\s;]+)`) reads the
  first token after `base`. It therefore names the place's base, never the forge's. A `?` can no
  longer be that token in this line, so the `m[3] != "?"` branch there is unused for these CRs;
  leave it for safety.
- **`_landed_line`** (the `base: not <cr>'s branch ...` line) compares the record-alone base
  with the landed base. It uses the same base function as the `worktree:` line (`stack_base`,
  planned, for a chain CR), so the two lines never disagree.
- `_carried_lines` (`facts.py`) already falls back on `stack_base`. It does not change.

**Card, `driver.md`.** The paragraph that ends the "rebase:" rules today says: "(for a stacked CR
with a PR, the base `take` prints is the PR's own base on the forge; `base ? (not read from
<link>: …)` means the read failed, so read the base on the forge yourself)". It now says:

- the `base` that `take` prints is the CR's place in the stack, as the record orders it;
- `; PR on <ref>` after it says the PR's base on the forge is still another branch. The place
  wins: rebase onto the place. The PR's base is the stack driver's to set (`forge-stack
  rebuild`), or yours on a `note rebase: stacked on …`, as the next paragraph says;
- `; PR base ? (not read …)` says the read failed and changes nothing for the rebase.

The paragraph that starts "In a stack batch the `base` that `take` prints may be another CR's
branch" gets one clause: after a reorder the base follows the new order, not the branch the
worktree started on.

### 3. A clean restack carries (D3)

**The defect.** `carry_check` → `_changed` (`commands/crs.py`) compares two lists of exact
patch-ids (`git patch-id --verbatim`):

- the judged commits, `g.base..g.head`, where `g.base` is the base recorded at the gate or
  verdict (`head_base` at that time);
- the new commits, `head_base..head`.

`head_base` (`commands/carry.py`) picks the nearest candidate tip under the head: the CR's
bases, the default branch, and every other CR's branch tips, remote and local. Suppose the CR
below moved on after this CR started on it: its Driver pushed again, or the stack driver
restacked it. Then no candidate tip is the real fork point, and the gate records a lower base,
often the default branch. The judged list then holds the CR below's commits as well as the CR's
own. After a clean restack onto the CR below's new tip (or onto `origin/<default>` once that CR
is merged by a rebase merge), the new list holds only the CR's own commits. `ship` prints
`off: the pass at <sha7> does not carry: the rebase changed the patch (own commits: N at … above
…, M at … above …)` where `carried:` belongs.

**The fix.** Count the CR's own commits the same way at the judged head and at the new head,
both against the new base:

- the judged own commits are the commits of `head_base..g.head` (by SHA);
- leave out of them each commit whose exact patch-id appears among the commits of
  `g.head..head_base`, which the new base holds as rewritten copies (a rebase merge, a restacked
  CR below);
- compare that list, in order, with `head_base..head`'s patch-ids, as today.

`g.base` stays required: a pass or verdict that recorded no base still does not carry, with
today's reason. The merge-commit checks stay (`_merges` on `g.base..g.head` and on
`head_base..head`). The old-git check stays. Git does the proof, not the Driver's word. The rule
lives in `crs.py`'s `carry_check` / `_changed`, which `ship_carry` (`carry.py`), `handback`'s
check (`driver_checks.py`) and the gate box (`facts.py`, `_carried_lines`) all call, so the three
agree. The `carried:` and `off:` texts (`carry.py`, `_lines`) do not change.

**First, reproduce.** Before the fix, the Driver writes the two cases below as failing tests at
main. If either already carries at main, the Driver traces batch-30's path (the `ship` of #421
and #430 after a rebase merge) until it finds the case that prints `off:`, fixes that cause
instead, and names it in the PR.

A real change still never carries: a commit of the CR added, edited, dropped by hand or folded,
or a CR below cancelled (its commits now count as the CR's own). Each keeps today's `off:` reason.

### 4. Each lease refusal names the exact command (D4)

**Where:** `core/leases.py` (306 lines), in three messages. Each keeps its current opening, which
`test_access.py` and `access` read, and adds the command. `<unit>` is the CR, `stack` or the QA
order; `--epoch <n>` is written as is.

- **`check_free`, a not confirmed lease** (`take <cr>`, `take stack`, a QA driver's restart).
  Today it ends with "check with the host that its Driver ended, then take it with --reclaim".
  It now ends with "check with the host that its Driver ended, then", followed by:
  - for a CR: `` `take <cr> --reclaim --note "resume: lease not confirmed" --epoch <n>` ``;
  - for the stack: `` `take stack --reclaim --epoch <n>` ``;
  - for a QA order: `` `agents set <O-k> <id> --reclaim --epoch <n>` ``.

  This is the case of the Foreman's stack lease that goes stale with no stack driver running:
  `foreman.md` already allows that `--reclaim` with no word from the user, and the refusal now
  hands over the line.
- **`check_free`, a live lease.** Today: "take it again with --reclaim only on the user's word".
  It now reads:

  ```
  <unit> is held: lease <n> live until <hh:mm:ss>; once the host shows its holder ended,
  `agents set <unit> - --epoch <n>` ends it; `take <unit> --reclaim ...` only on the user's word
  ```

  For the stack: `take stack --reclaim --epoch <n>`. For a QA order: the `agents set ...
  --reclaim` form.
- **`require` and `claim`, with `ended_ok`** (the stack driver's `ship <cr>`, and `stack` /
  `forge-stack` on the stack unit). The CR's lease is not ended and no `--lease` is given. Today
  the refusal is only `ship <cr> needs --lease <n> (the number take printed)`. It keeps that
  opening and adds, by the lease's state:
  - live: `; <cr>'s lease <n> is live until <hh:mm:ss>: its Driver ships it; once the host shows that Driver ended, \`agents set <cr> - --epoch <n>\` ends the lease and \`ship\` with no --lease is accepted`
  - not confirmed: `; <cr>'s lease <n> not confirmed since <hh:mm> (<m> min ago): once the host shows its Driver ended, \`take <cr> --reclaim --note "resume: lease not confirmed" --epoch <n>\` starts a new Driver, which ships it`

  A refusal with no `ended_ok` (a Driver's own command run without its number) keeps today's
  text.

The CLI still knows no role. It names the commands and the host check; the cards say who runs
them, and `foreman.md`'s lease bullet already does. No card changes for this section.
`agents set <unit> -` still ends only a live lease (see the open question).

## Files

- `skills/chantier/scripts/cli/src/chantier/commands/orders_apply.py` (`_merged`) and
  `commands/orders_merged.py` (the restack line).
- `skills/chantier/scripts/cli/src/chantier/commands/facts.py` (`_base_of`, `_landed_line`).
- `skills/chantier/scripts/cli/src/chantier/stacks.py` (`_live_start` / `stack_start` rule 1 and
  the taken-CR rule; one helper moved out to stay at 400 lines or fewer).
- `skills/chantier/scripts/cli/src/chantier/commands/crs.py` (`carry_check`, `_changed`) and, if
  needed, `commands/carry.py`.
- `skills/chantier/scripts/cli/src/chantier/core/leases.py` (`check_free`, `require`, `claim`).
- Tests, in new files only: `test_carry_ship.py` has 397 lines, `test_stack_base.py` 400 and
  `test_leases.py` 373. Existing tests that assert the old texts are updated in place, with no
  line added: `test_leases.py` line 70 ("then take it with --reclaim"). Every `.py` file stays at
  400 lines or fewer (`CONTRIBUTING.md`).
- `scenario/run_scenario.py`: the check "a PR on the default branch is printed as the remote's
  default branch" (`handoff` after `forge_base(w, link, "main")`). It now expects the place's
  base followed by `; PR on origin/main`. The `base ? (not read from <link>: …)` check after it
  still holds: the text is kept.
- `skills/chantier/references/driver.md`: the stacked-CR base sentence and one clause (section 2).
- `skills/chantier/references/foreman-stack.md`, "After a merge", the "A restack" bullet: one
  clause, "`order merged` prints `restack owed: …` when one is owed".
- Not touched: `agents/`, `com.github.copilot/agents/`, `AGENTS.md`, `concepts.md`,
  `foreman.md`, the web client, `hooks/`, `types/`.

### Overlaps: CR-471 and CR-474

- **CR-471** (`slim-cards`) cuts `driver.md` and `foreman.md` into `<role>-<moment>.md` pieces.
  It moves no text of `foreman-stack.md`. After it, the Driver finds the `driver.md` text by
  searching `skills/chantier/references/driver*.md` for "the base `take` prints is the PR's own
  base on the forge" and for "In a stack batch the `base` that `take` prints may be another CR's
  branch". It edits the text wherever it now lives and changes no manifest action. If CR-471's
  check that every rule is reached reads a list of rules, the edited sentences keep their place
  in it. `foreman.md` is not edited here.
- **CR-474** (`ready-line`) edits `status` (`commands/batch_status.py`, a new
  `status/ready_line.py`, some functions moved to `commands/batch_status_orders.py`). This CR
  changes no `status` line and no file CR-474 names, so there is no conflict. If CR-474's owed-step
  clause reads a lease or restack state, it reads the record, which this CR does not change.
- Both come first. This CR rebases onto main after them and runs its checks there.

## Out of scope

- A new tool or command that rebases or force-pushes for the stack (D1: a printed line only).
  The CLI runs no git for the restack.
- A new line showing the stack's shape in `take`'s output. The place's base on the `worktree:`
  line, and the `stack` / `take stack` rows, are the shape. The request's "shape shows only at
  `ship`" is answered by the true base (D2).
- Changing what `ship` prints for its own base (`recorded <pr> (base <x>, …)`), the forge reads
  of `ship` and `forge-stack`, or `status`.
- Ending a not confirmed lease without `--reclaim` (the open question).
- Detecting the forge's merge method (rebase, squash, merge commit): the restack line prints for
  any recorded merge of a chain CR with open PRs above it.

## Evidence

Checks (`just test`, in-process, on a prepared state; new test files, parametrized and fast):

1. **Restack line.** `order merged <bottom cr>` in a stack batch of three CRs with PRs prints the
   `take stack --epoch <n>` form, naming the two CRs above in order. With `stack_agent` recorded,
   it prints the `note merged:` form naming the agent. No line in these cases:
   - a parallel batch, and a series batch;
   - a fix CR merged in a stack batch;
   - the last open CR merged (nothing above);
   - the CR above has no PR.
2. **Bases.** All in a stack batch:
   - (a) A taken CR with `start_on` = CR-A's branch; `stack` then orders it below CR-A. `handoff`
     prints the base of its new place (the default branch, or the ready CR now below it with a
     PR), not CR-A's branch. The `Rewrites:` line of a `take --note` names that base.
   - (b) A stacked CR with a PR whose forge base (the test's `read_base` stub) is the old base
     prints `base <place>; PR on <old ref>`.
   - (c) The forge base equal to the place: nothing is added.
   - (d) A failed read: `base <place>; PR base ? (not read from <link>: …)`, on one line.
   - (e) For every CR of the chain, the base `handoff` prints equals the base its `stack` row
     prints.
   - (f) A fix CR with an `after`, and a series batch's CR, print what they print at main.
3. **Carry.** Each case is written failing first, at main (section 3):
   - (a) B started on A's tip, A then gets one more commit (pushed), B's gate records a base
     lower than A's old tip, B is rebased cleanly onto A's new tip: `ship B` prints `carried:
     long gate and verdict from <sha7> (clean rebase onto <A's branch>)` and no `off: … does not
     carry`.
   - (b) A merged by a rebase merge: A's commits cherry-picked onto main, origin/main moved, A
     recorded merged. B is rebased with `git rebase --onto origin/main <A's old tip>`: `ship B`
     carries, onto `origin/main`.
   - (c) The real changes (`_added`, `_edited`, `_cancelled` in `test_carry_ship.py`) still give
     `off: … the rebase changed the patch …` with today's counts.
   - (d) `handback ready` after (a) is accepted on the carried pass and verdict (the same rule,
     through `driver_checks.py`).
4. **Lease refusals.**
   - `take <cr>` on a not confirmed lease names `take <cr> --reclaim --note "resume: lease not
     confirmed" --epoch <n>`; `take stack` names `take stack --reclaim --epoch <n>`; a QA
     restart names `agents set <O-k> <id> --reclaim --epoch <n>`.
   - On a live lease: `agents set <unit> - --epoch <n>` and "only on the user's word".
   - `ship <cr>` with no `--lease` while the CR's lease is live, and while it is not confirmed:
     each names its command.
   - After `agents set <cr> - --epoch <n>` on a live lease, `ship <cr>` with no `--lease` is
     accepted.
   - `test_access.py`'s expected openings still match.

Gates: `just check`, and `just eval-dry-run` (a change under the CLI's `src/`), in the worktree
at the rebased head; the long gate `scenario` (`just scenario (ubuntu-latest)` green at the PR's
head), and the local `scenario` run when this CR is on top of its batch's stack (AGENTS.md).
`hooks/` and `types/` are not touched, so `just mod` is not owed.

No host or default matrix: nothing here depends on the host or on a configured value. The forge
read is the existing one (GitHub with `gh`, GitLab with `glab`), unchanged.

## Open question

1. **End a not confirmed lease with `agents set <unit> -`?** Today `agents set <unit> - --epoch
   <n>` ends only a live lease. A not confirmed one stays until `take ... --reclaim`, which starts
   a new lease. So the stack driver cannot `ship` a CR whose Driver ended late, without a new
   Driver being started for it. The Foreman's stack lease that went stale also still needs
   `take stack --reclaim` (now named in the refusal). Should `agents set <unit> -`, recorded
   after the host reported the agent's end, also end a not confirmed lease? That would make both
   frictions go away. This specification does not do it (D4 keeps only the named commands).
