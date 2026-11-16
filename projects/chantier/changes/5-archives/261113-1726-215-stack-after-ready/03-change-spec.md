# Change Specification: work on a stack after it is ready

## Goal

Once a stack is ready, the work on it (inserting a change, restacking what remains after a
merge, keeping the record right) is manual, refused, or leaves the record wrong. Batch-15 showed
five failures. After this CR:

- `forge-stack` rebuilds the native stack on GitHub from the record, so inserting a change or
  restacking after a merge is one CLI command, with no raw `gh api` call.
- The record follows the stack's order: a stacked CR's base is the CR under it, whatever its
  `after`.
- The stack driver never runs `take stack`: the Foreman runs it and passes its output, and the
  stack driver reads the stack again with a read-only command.
- `ship` names the PR body lines whose SHA a restack made stale.
- One merge action by the user leads to one restack at most, and none when the whole stack
  merged.

Source: the batch-15 retro (`.agents/changes/5-archives/261113-1149-213-stack-merges-in-one-go/retro.md`,
lines on the stack driver id race, Test plan SHAs, native stack insertion and `order after`),
merged into one CR on the user's word. This CR has no `02-answers.md`: no decision of the user's
beyond the request is carried, and the choices below are those the request left open that change
nothing the user sees.

## Facts (GitHub REST stacks API)

- `POST /repos/{o}/{r}/stacks` with `pull_requests[]` bottom to top creates a stack.
- `GET /repos/{o}/{r}/stacks` and `GET /repos/{o}/{r}/stacks/{n}` read them.
- `POST /repos/{o}/{r}/stacks/{n}/add` appends PRs on top (the first one's base must be the top
  PR's head branch).
- `POST /repos/{o}/{r}/stacks/{n}/unstack` removes PRs from the stack; the stack is dissolved
  when none is left.
- A PR's base cannot change while it is in a stack.

The current docstring of `skills/chantier/scripts/cli/src/chantier/forge_stack.py` says the API
"offers no way to add a PR to a stack or to dissolve one": that is wrong and is fixed here.

## What changes

### 1. `forge-stack rebuild` (from `forge-stack-insert`)

File: `skills/chantier/scripts/cli/src/chantier/forge_stack.py`; parser in `cli.py`
(`choices=["create", "show", "rebuild"]`, help text updated).

`$CHANTIER forge-stack rebuild [--batch <b>]` makes the forge's stack match the record, whatever
changed (an insertion, a reorder, a partial merge):

1. The plan, as `create` builds it (`_plan`): every open CR of the batch's stack, in `take stack`
   order, the release last; refused (exit 2) as `create` is when a CR has no PR recorded, the
   batch is not a stack, or a link is not GitHub.
2. Every open stack on the forge that holds any PR of the plan (`GET .../stacks`, as `show` finds
   them) is dissolved: `POST .../stacks/{n}/unstack` until the forge reads it back as gone or
   not open. A stack that holds a PR not in the plan as well is dissolved the same way, and the
   output names that PR (it stays a plain PR).
3. Each PR whose base on the forge (`GET .../pulls/{n}`, `base.ref`) is not the base the record
   gives (`_stack_base(d, c, repo, planned=True)` from `commands.py`: the CR under it, the first on
   the default branch) is retargeted (`PATCH .../pulls/{n}` with `base=<branch>`).
4. One new stack is created, bottom to top (`POST .../stacks`), as `create` does.
5. It is read back with the checks of `show`. The PRs are drafts at this point by design (the
   stack driver turns them ready after), so check 4 (drafts) is printed as a line to act on, not
   a failure: exit 0 when checks 1, 2, 3 and 5 hold.

Output: one line per action taken (`unstacked #<n>`, `#<pr> base <old> -> <new>`,
`stack #<n> <top link> (PRs bottom to top: …)`), then the read-back lines. Any forge refusal
stops at once, prints what was already done and the forge's exact text, exit 4. `rebuild` is
idempotent: run again after a failure, it finds no stack (or the one left), retargets what is
still off, and creates the stack. It writes no file. It changes no branch and pushes nothing: the
stack driver rebases and pushes before it.

Choice (changes nothing the user sees): one command, `rebuild`, rather than an `insert` beside
it. An insertion in the middle has no API (only an append on top exists), and the release sits on
top of most stacks, so an insertion is a rebuild anyway; one path covers the insertion, the
reorder and the partial merge. `add` is not used. The stack's number changes on every rebuild, as
it already does today when the stack driver re-creates it; the user gets the new link in the
`stack-ready` ask as before.

`create` stays as it is (exit 4 with the forge's text when the PRs are already stacked); its
message adds: `forge-stack rebuild` replaces a stack.

Docstring of `forge_stack.py`: names `create`, `show` and `rebuild`, and the four endpoints above
plus the PR base change, and says that a PR's base cannot change while it is in a stack, which is
why `rebuild` dissolves first.

### 2. The record follows the stack's order (from `order-after-ready-cr`)

File: `skills/chantier/scripts/cli/src/chantier/commands.py`.

Choice (changes nothing the user sees): `stack` (the recorded order) sets the base; `order after`
keeps refusing a CR that is not queued. The stack's order is already the record of each PR's
place, and `stack` already refuses an order that puts a CR below one of its `after`, so the CR
under a stacked CR is always at or above its last open dependency.

- `_stack_base`: for a CR that `stack` marked (`stacked`), the base is its place in the chain (the
  CR under it, the first on the default branch), even when it has an `after`. A CR with an `after`
  not yet marked keeps today's base (its last open dependency). A release keeps its base: the top
  CR under it by the recorded order (`_top_cr`). `_start_base` (where a CR starts) is unchanged.
- The case seen in batch-15 must hold: a CR inserted with `order add`, then
  `stack <…> <new> <release>` (or below any CR), gives `take stack`, `handoff <release>`, `ship`
  and `forge-stack rebuild` the new CR's branch as the base of the CR above it. The Driver
  reproduces it in the scenario before changing the code, and fixes the cause it finds if it is
  not (only) the `after` branch of `_stack_base`.
- `order after` on a CR that is not queued, in a stack batch: the message adds `; in a stack, its
  place and base are set by \`stack\``.

### 3. The stack driver does not run `take stack` (from `stack-driver-take-race`)

Choice (changes nothing the user sees): both halves of the request's alternative, as one rule:
the Foreman runs `take stack` (its card already says so) and passes the output in the prompt, and
the stack driver reads the stack again with `stack` and no CR, which writes nothing. The read-only
form is needed because the stack driver changes the order itself (`stack <cr>…`) during an
insertion and must read the result.

- `cli.py`: `stack`'s `crs` becomes `nargs="*"`; help: `the stack's order, as its driver set it;
  with no CR, print the stack as it stands (writes nothing)`.
- `commands.stack` with no CR: the same lines `take stack` prints (the chain line, then one line
  per CR with status, worktree, branch, base and PR), no epoch, no lock taken for writing, no
  event, no reopen. Share the line-building code with `take` rather than copy it.
- `take stack` refused because a stack driver is recorded: the message adds `(a stack driver
  reads the stack with \`stack\`, which changes nothing)`.

### 4. `ship` names stale SHAs in the PR body (from `stale-test-plan-shas`)

File: `commands.py`, `ship`.

After the checks it makes today, `ship` reads `<CR folder>/work/pr-body.md` when it exists (the
file the Driver posts, [pr-template](../../../../../skills/chantier/references/pr-template.md)) and,
for each line that names a hex token of 7 to 40 characters which resolves to a commit in the
worktree (`git rev-parse --verify --quiet <tok>^{commit}`) and is not an ancestor of the new head
(`git merge-base --is-ancestor`), prints
`off: pr-body.md line <n> names <sha7>, not in <head7>'s history: <the line, trimmed to 120 characters>`.
A line that says `STALE` or `carried from` is not listed (the template's own marks). Read-only git
only. It is an `off:` line like the others: logged in the `ship` event's `off`, never a refusal,
and `handback` is not changed by it.

The stack driver keeps `work/pr-body.md` as the posted body: after a restack it runs `ship`, fixes
the lines named (carried or judged again, as its card says), posts the file, and runs `ship` again
until no such line remains, before it turns the PR ready.

### 5. One merge, one restack at most (from `stack-merge-restack-cost`)

Cards only. A user's merge on GitHub of a PR in a native stack merges it with every PR under it in
one action; whatever one action merged needs one restack, and a whole stack merged needs none.

- `chief-of-staff.md`, "A stack batch": after one merge action of the user, record `order merged`
  for every CR it merged, bottom first, all before telling the Foreman, in one message.
- `foreman.md`, the stack batch paragraph: "again after a merge" becomes: once every CR merged by
  one action of the user is recorded, one `take stack` for what remains; none when nothing of the
  stack remains open. "On an `order merged`", **Stack**: the same.
- `driver.md`, "Stack driver", the partial-merge paragraph: one restack for what remains: each PR
  rebased once on the one under it (the first on `origin/<default branch>`), pushed once with
  `--force-with-lease`, `ship`ped once, heavy CI once at the top, then one `forge-stack rebuild`
  (no manual retarget: `rebuild` retargets the first PR to the default branch).

### Cards (all of them in `skills/chantier/references/`)

- `driver.md`, "Stack driver":
  - "The stack is what `take stack` prints" becomes: the stack is what your prompt gives from
    `take stack`; `$CHANTIER stack` with no CR prints it again at any time and changes nothing.
    You never run `take stack`.
  - "Making the stack": unchanged for a first stack. Any later change to a stack already on the
    forge (an insertion, a restack after a merge, a reorder) is `$CHANTIER forge-stack rebuild`
    after the rebases and pushes, not a retarget by hand (a PR's base cannot change while it is
    stacked). A `rebuild` refused (by the forge or the permission check) is an `anomaly` with the
    exact text, as today; no other means.
  - "Inserting into a ready stack", step 3: `$CHANTIER forge-stack rebuild` (it dissolves the
    stack, retargets the PRs, re-creates and reads it back); step 2 adds `ship`'s stale-SHA lines
    to fix before the PRs turn ready.
  - The restack paragraph: the stale-SHA lines of `ship`, as in section 4.
- `foreman.md`: the `take stack` bullet says the order: `take stack`, its output in the stack
  driver's prompt, the start, then `agents set stack <id>`; the stack driver never runs `take
  stack`. The insertion sequence names `forge-stack rebuild`. Section 5's merge rule.
- `chief-of-staff.md`: section 5's rule. A stack driver's or Foreman's `anomaly` on a refused
  `forge-stack rebuild` reaches the user as an ask with the exact text; on the user's yes the
  Chief of Staff runs `$CHANTIER forge-stack rebuild` itself (no raw `gh api`).
- `concepts.md`, **Stack**: "the stack is updated on the forge (re-created if the forge cannot
  insert)" becomes "rebuilt on the forge (`$CHANTIER forge-stack rebuild`)"; the partial-merge
  sentence adds "one restack for one merge action"; the `$CHANTIER` paragraph keeps "no forge
  command beyond `forge-stack`" (the retarget is inside it).
- `agents/` and `com.github.copilot/agents/`: no change unless an agent file names `take stack`
  or `forge-stack` for the stack driver; if one does, both hosts together, bodies identical.

### Docs

`scenario/README.md` lists the new scenario steps. `evals/SCORECARD.md` is not touched.

## Out of scope

- An `insert` action, and the use of `POST .../stacks/{n}/add`.
- GitLab: the stack stays a chain; `rebuild` is GitHub only, refused on a GitLab link as
  `create` and `show` are.
- `order after` on a CR that is not queued.
- The CLI turning PRs to draft or ready, rebasing or pushing: the agents keep that.
- Reading the PR body from the forge: `ship` reads `work/pr-body.md` only.
- A rail refusing `rebuild` while PRs are ready (the cards keep the drafts-first rule).
- The force-push permission route (its own retro item).

## Evidence

- `just check` passes (Linux, macOS, Windows).
- `just scenario` passes with new steps in `scenario/run_scenario.py`, section 13a and the stack
  section (around the existing `forge-stack` checks); `scenario/fake_gh.py` gains
  `POST .../stacks/{n}/unstack` (removes the given PRs, dissolves when none left),
  `GET .../pulls/{n}` and `PATCH .../pulls/{n}` (refused with an HTTP 422 text while the PR is in
  an open stack, as the forge does):
  1. `forge-stack rebuild` after an insertion (`order add`, `stack a new b r`, a PR shipped for
     the new CR): the old stack is unstacked, `b`'s PR is retargeted to the new CR's branch, a new
     stack is created bottom to top, the release on top; `show` then prints only the drafts line,
     or exits 0 with no drafts.
  2. `rebuild` after a partial merge: the first remaining PR is retargeted to `main`, one stack is
     created.
  3. `rebuild` stopped by a forge refusal mid-way (exit 4, the forge's text and what was done),
     then run again: it completes.
  4. `rebuild` refused on a GitLab link, on a parallel batch, and with a CR with no PR (exit 2).
  5. A stacked CR with an `after` takes its stack place as base (`take stack`, `ship`,
     `handoff`); the release's base is the CR just under it after an insertion below it.
  6. `stack` with no CR prints the same lines as `take stack`, with a stack driver recorded, and
     writes nothing (`batch.json` and `events.jsonl` unchanged); `take stack` refused then names
     `stack`.
  7. `ship` after a rebase whose old head is named in `work/pr-body.md`: an `off:` line naming
     that line; a `carried from` line and a `STALE` line are not named; with the body fixed, none.
  8. `order after` on a ready CR in a stack batch: refused, the message names `stack`.
- The docstring of `forge_stack.py` names the four endpoints and the base rule.
- `tests/test_structure.py` (if it lists CLI commands or actions): updated for `rebuild`.
- No CI job is added or changed.

## Open questions

None. The choices above (`rebuild` only; `stack` sets the base; both halves of the `take stack`
fix; the merge rule in the cards) change nothing the user sees beyond what the request asks.
