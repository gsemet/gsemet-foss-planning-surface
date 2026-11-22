# An ordered stack is checked as a git chain

In a stack or series batch, a CR the record places on another CR's branch (placed by `stack`, or
taken onto it), the release CR included, must have that CR's recorded head in its history. `ship`
refuses, recording nothing, a CR whose branch does not, and `stack --out-of-draft` refuses a CR
whose recorded head does not. The caller of the refused `ship` rebases. The stack driver checks the
chain with `git merge-base` before it concludes that no restack is needed and before it turns any
PR ready. Specification v4.

## Goal

From Studio's batch-07 retro (`intake/request.md`). The ordered stack CR-439..CR-445 was linear on
the forge only: the PRs' bases formed a chain, but CR-440, CR-442 and CR-444 had been cut from main.
`take CR-446` was refused. A first stack driver wrongly concluded that no restack was needed. Two
restacks followed and voided the gates and verdicts of five CRs (about +$15-25).

What the user wants (stack-chain-Q1..Q12 and the restatement): in a stack or series batch, each CR
the record places on another CR's branch (placed by `stack`, or taken onto it), and the release CR
on the top CR, starts from the recorded head of the CR below it. `ship` refuses otherwise and names
both CRs, before a gate or a verdict is paid on that head; whoever ran the refused `ship` owns the
branch and rebases it. `stack --out-of-draft` refuses the same broken chain, because in a stack the
stack driver may ship nothing (the incident's path); its refusal tells the stack driver to put the
PRs it just turned ready back to draft first. The stack driver checks with `git merge-base` before
it concludes "no restack needed" and before `gh pr ready`. The CLI restacks nothing (no git write),
reads no forge for this check, and has no flag that forces past either refusal: the rebase is the
fix.

## Decisions carried (02-answers.md)

| Answer | Decision | Where |
|---|---|---|
| Q1 A | Refused at `ship`: at each `ship` of a CR already stacked, the CLI refuses when its branch is not based on the head of the CR below. The message names both CRs: `CR-442: branch not based on CR-441's head`. | 1 |
| Q2 A | One card line: the stack driver checks with `git merge-base` that each branch starts from the head of the CR below before it concludes that no restack is needed. | 3 |
| Q3 A | Series batches as well as stack batches: wherever a CR is meant to start from another. | 1, 2 |
| Restatement | No git write and no flag to force past the refusal. | 1, 2 |
| Q4 A | Grilled enough. Destination batch-30, joined with `order add`. | Coordination |
| Q5 | The caller of the refused `ship` owns the branch (driver.md, "Who moves a branch") and rebases it: no route through the stack driver or the Foreman. One refusal message for both modes. The check reads the CR below's recorded head, so a stacked working CR is refused at its next `ship` each time the CR below shipped a new round or was rebased, and rebases then without waiting for the Foreman's note. driver.md's `rebase: mode <mode>` paragraph is fixed (its pre-rebase `ship` would be refused), and every other `ship` before a rebase in the cards is found and fixed. | 1, 3 |
| Q6 | One more refusal, at `stack --out-of-draft` only (`_check_out_of_draft`): a named CR whose recorded head does not hold its CR below's recorded head; same helpers, exclusions and `git cannot read` refusal; message ending `then stack --out-of-draft again; nothing recorded`; no flag; one card line in the stack driver's paragraph; one parametrized test; a scenario step if it costs one step. `stack <crs>`, `forge-stack`, `take stack` stay out of scope. | 2, 3, 4, 5 |
| Q7 | A CR taken onto another's branch and not placed yet is checked when its `start_on` is live (`stacks._live_start`); an unplaced CR with no live `start_on` stays unchecked. The wording "a CR the record places on another CR's branch (placed by `stack`, or taken onto it)" in "Words used here", section 1 and the Goal; the CR driver sentence names the first-ship case; tests split; existing test worlds made true to the chain. | Words, 1, 3, 4 |
| Q8 A | The CR below is read as `take` reads it, with `landed` (`journal.seen_merged`): a CR not merged, not cancelled and not seen merged. A CR seen merged counts as ended, so it is never the CR below. The same `landed` at `stack --out-of-draft`. A merge neither the record nor the journal holds: the refusal stands (no forge read at `ship`); the cards say: once the journal or the record holds the merge, `ship` again. One test. | Words, 1, 2, 3, 4 |
| Q9 A | A second `ship` message when the head holds `<remote>/<branch below>` but not the CR below's recorded head: `CR-442: CR-441's branch moved since its last ship (<rec7> -> <tip7>): it ships first, then ship again; nothing recorded`. The remote ref is read as it stands in the clone (no fetch); unreadable or absent: the first message. Reads only on the refusal path. The check itself stays on the recorded head. The card names both messages. One test case. `stack --out-of-draft` keeps one message. | 1, 3, 4 |
| Q10 A | The release CR is checked too, at `ship` and `stack --out-of-draft`: its CR below is the top CR (`start_base`'s release rule, `top_cr`, with Q8's `landed`), checked against that CR's recorded head with the same helpers and messages. `check_release_branch` at `take` stays as it is. "Neither a `release`" leaves the CRs checked; section 1 and Out of scope reworded; the Release driver's card gets the refusal sentence; one test case each (`ship`, `stack --out-of-draft`). | Words, 1, 2, 3, 4, Out of scope |
| Q11 C | Both: the stack driver card runs the `merge-base` check before `gh pr ready` (no PR turns ready on a chain not checked), and the `stack --out-of-draft` refusal's fix starts with `put <crs>' PRs back to draft, ...`, the PRs put back being the refused CR's and every one above it in the same call. The message says the words only; the forge commands (`gh pr ready --undo`, `glab mr update --draft`) stay in the card. Nothing to record with `stack --draft` (the refused call recorded nothing). The test's expected text follows. | 2, 3, 4 |
| Q12 A | On `<cr>'s branch moved since its last ship` with that CR below working: the stack driver ships it first only if it has no live Driver; otherwise it leaves the CR above to come (a draft, not turned out of draft) and hands back naming it (`<cr> to come: <cr below> not shipped at <tip7>`); the mergeable part below is handed back as usual; the Foreman takes the stack again after that Driver's `ship`. | 3 |
| Critic finding 4 (v2) | The card guard asserts that, in driver.md's `rebase: mode <mode>` paragraph, "rebase onto" comes before the first "`ship`" (today's text fails it). | 4 |
| Critic finding 5 (v2) | One named three-way git read (exit 0 / exit 1 / any other exit) for both checks; `carry._ancestor` is not used. | 1, 2 |
| Critic finding 3 (v3) | The second `ship` message only when the remote tip is not an ancestor of the CR below's recorded head (a recorded head never pushed, or pushed then overtaken by nothing, gets the first message). | 1, 4 |
| Critic finding 4 (v3) | The "forge shows it merged" sentence reads: once the journal or the record holds the merge (`status` shows it merged), `ship` again; in the CR driver's, Release driver's and stack driver's paragraphs. | 3 |
| Critic finding 5 (v3) | "Words used here": the stack driver's card has `stack` name only CRs with a PR; `delivery.py`'s `stack` itself never checks `pr`. | Words |
| Critic finding 6 (v3) | The scenario helpers `push()` / `ship()` / `driver_round()` rebase every CR onto `origin/main`; they rebase onto the CR's recorded base instead. | 5 |

## Words used here

- **Landed:** `journal.seen_merged(journal.read(repo.store, repo.changes)[0], d)`, the CRs of the
  batch the forge hub saw merged, read exactly as `commands/driver.py` (`take`) and
  `commands/facts.py` (`cr_facts`) read it. A CR of `landed` reads as ended everywhere below (Q8).
- **The CR below** of a CR `c` in an ordered batch: the CR of the batch, other than `c`, that is not
  `merged`, not `cancelled` and not seen merged (not in `landed`), and whose branch is `c`'s base as
  the record gives it today, with `landed`:
  - in a **stack** batch, `stacks.stack_base(d, c, repo, landed=landed)`. For a CR placed by
    `stack` (`stacked`), this is the branch of the nearest CR under it in `chain` that is not in
    `landed`, and the default branch when there is none. For a CR not placed yet whose `start_on`
    is live (`stacks._live_start(d, c, landed)`), `stack_base` goes through `stack_start`, whose rule
    1 returns that `start_on`: the CR below is the CR that owns that branch. For the release CR,
    `stack_base` goes through `start_base`'s release rule: the top CR (`top_cr(d, landed)`);
  - in a **series** batch, `stacks.start_base(d, c, repo, landed)`: for a CR that is not the
    release, the branch of `rails.series_predecessor` while that CR is open and not in `landed`,
    else the default branch; for the release CR, the top CR's branch (`top_cr(d, landed)`).
  When the base is the default branch, or a branch no such CR owns, `c` has no CR below and nothing
  is checked. Read through these functions, never by a copy of their rules. That way the base rules
  that park-live-cr (CR-430) and hold-live-cr (CR-431) change apply to this check with no further
  edit.
  `stack_base` takes no `landed` today: it gains a keyword `landed: frozenset[str] = frozenset()`.
  It passes it to `stack_start` and `start_base`, and its stacked rule skips the CRs of `landed`
  when it takes the CR under `c` in `chain`. With the default, every existing caller reads what it
  reads today.
- **A CR the record places on another CR's branch** (the CRs checked): a CR that is not a `fix`,
  not held (`stacks.is_held`; with CR-430/CR-431, not `apart`) and not ended, and:
  - the **release** CR, in a stack or series batch, when it has a CR below (the top CR); a release
    with no open CR under it sits on the default branch and has none (Q10);
  - in a **stack** batch, a CR that is not the release and is either placed by `stack` (`stacked`,
    by `stack <cr>…`), or taken onto another CR's branch and not placed yet, with its `start_on`
    live (`stacks._live_start(d, c, landed)`: the CR that owns that branch is neither ended, nor in
    `landed`, nor held). A CR not placed yet with no live `start_on` (none recorded, or its owner
    merged, cancelled, seen merged or held) is not checked: its place comes from the stack driver's
    next `stack` or from its Driver's `rebase:` note;
  - in a **series** batch, a CR that is not the release and has a CR below. Series has no `stacked`
    flag. Its CRs sit on their predecessor from their first take (`start_base`'s series rule), so
    every CR with an open predecessor is placed on it (Q3).
- **The head of the CR below:** the full SHA in that CR's `head` field, recorded by its last
  `ship`. It is the head the restack notes already name (`restack: on <cr below> <its head7>`) and
  the head `check_release_branch` reads. Because it is the recorded head, a CR above is refused at
  its next `ship` each time the CR below shipped a new head (a new round, a rebase), until it is
  rebased onto it (Q5). When the CR below has no recorded head (never shipped), nothing is checked.
  That is the case of a CR below with no PR, and in the normal flow no stacked CR or series
  successor sits on one: the stack driver's card has `stack` name only CRs with a PR ("Order every
  CR of the stack with a PR", "You open no PR (a CR with none is an anomaly)"), and a series CR is
  taken once its predecessor is `ready`. `delivery.py`'s `stack` itself never checks `pr`, so a CR
  `stack` placed on a CR with no PR is possible against the card; this CR does not add that check
  (out of scope), and such a CR is simply not checked until the CR below ships.
- **The ancestry read:** one new read-only function in
  `skills/chantier/scripts/cli/src/chantier/core/git.py`, beside `git` and `branch_exists`, e.g.
  `is_ancestor(older: str, newer: str, cwd: Path | str) -> bool | None`. It runs `git merge-base
  --is-ancestor <older> <newer>` with the same environment as `git()` (`GIT_TERMINAL_PROMPT=0`, no
  pager) and returns True on exit 0, False on exit 1, and None on any other exit (a commit or a ref
  git cannot read: git exits 128). Both checks use it, and only it. They do not use
  `commands/carry._ancestor`, which reads every non-zero exit as "not an ancestor"; that function
  and its callers stay as they are.
- **No live Driver** (Q12): as the stack driver's card reads it in "Who moves a branch": a CR handed
  back `ready`, or `blocked`. A `working` CR has a live Driver.

## What changes

### 1. `ship` refuses a CR whose branch does not hold the head of the CR below (CLI)

Files: `skills/chantier/scripts/cli/src/chantier/commands/delivery.py` (`ship`),
`skills/chantier/scripts/cli/src/chantier/stacks.py` (`stack_base` gains `landed`, as "Words used
here" says, and a new read-only helper, e.g. `chain_below(d, c, repo, landed) -> CrEntry | None`,
that returns the CR below of a CR the record places on another CR's branch, per "Words used here",
or None), `skills/chantier/scripts/cli/src/chantier/core/git.py` (the ancestry read). Place
`chain_below` beside `stack_base` and `off_place`, not beside `stack_due` (see Coordination).

- In `ship`, after the existing reads and **before** the `RenderedBatch` write, where
  `_refuse_foreign` is called today: when the batch's mode is `stack` or `series`, read `landed`
  (one journal read, only in those modes). When `chain_below(d, c, repo, landed)` returns a CR and
  that CR has a recorded head, run the ancestry read `is_ancestor(<below.head>, <head>, cwd=<the
  CR's worktree>)`. `<head>` is the worktree's `HEAD`, the head `ship` would record. Every git call
  here is read-only, like every other git call in `ship`.
- True: `ship` goes on as today.
- False (not an ancestor): refuse with `EXIT_PRECONDITION` and record nothing (no `touch`, no
  `ship` event, no `carry` event, no lease claim written). The words depend on the remote tip of
  the branch below, read on this refusal path only (Q9, critic finding 3 on v3): `<tip>` is
  `<remote>/<below.branch>`, with `<remote>` the project's `repo.config["remote"]`, read as it
  stands in the clone (the CLI fetches nothing). Two reads, in this order:
  1. `is_ancestor(<tip>, <head>, cwd=<the worktree>)`: does the head hold the branch below's remote
     tip?
  2. only when (1) is True, `is_ancestor(<tip>, <below.head>, cwd=<the worktree>)`: is the remote
     tip already in the CR below's recorded head?
  - The **second message** only when (1) is True and (2) is False: the head holds the remote tip,
    and that tip is not in the recorded head, so the CR below moved past its recorded head on the
    remote and has not shipped there. `<rec7>` is the CR below's recorded head and `<tip7>` the
    remote tip (`git rev-parse <remote>/<branch below>`, read-only), both short:

    `CR-442: CR-441's branch moved since its last ship (1a2b3c4 -> 5d6e7f8): it ships first, then ship again; nothing recorded`

  - The **first message** in every other case: (1) False or None (the head does not hold the
    remote tip, or the ref is absent or unreadable), or (2) True or None (the remote tip is an
    ancestor of the recorded head: a recorded head never pushed, whose remote tip is older, gets
    this one, since a rebase onto that recorded head is the fix). For both modes (Q5). It starts
    with Q1's words and names both CRs, the short head of the CR below, the branch below and the
    fix:

    `CR-442: branch not based on CR-441's head 1a2b3c4: rebase onto chantier/batch-30/CR-441, push, ship again; nothing recorded`

  In both, the CR ids, the short SHA(s), the branch below (first message) and the clause `nothing
  recorded` are mandatory. The rest of the wording is the Driver's to fit to the line limit.
- None (git cannot read the head of the CR below, e.g. the commit is missing from the clone):
  refuse with `EXIT_PRECONDITION` and record nothing: `CR-442: git cannot read CR-441's head
  1a2b3c4: fetch, then ship again; nothing recorded`. This is not read as "based" and not skipped: a
  check that cannot run does not pass.
- A CR below that the forge merged but neither the record nor the journal holds as merged is still
  the CR below. The refusal stands as written: the CLI reads no forge at `ship` (Q8). The cards say
  what to do (section 3).
- No flag skips the check: `--conflict` does not, and no new option is added.
- The release CR is checked the same way, against the top CR's recorded head, with the same
  messages (Q10). The release's own `take` check (`driver_checks.check_release_branch`, called from
  `commands/take_checks.check_take_all`) stays unchanged: it proves at `take` that the top branch
  holds the CRs under it, and this check proves at each `ship` that the release's branch holds the
  top CR's recorded head. A fix CR and a held CR are not checked.
- The check runs whoever calls `ship`: a CR driver, the stack driver for a CR it moved, a QA
  driver, a Release driver. The caller owns the branch it ships and rebases it on a refusal (Q5;
  driver.md, "Who moves a branch"): there is no route through the stack driver or the Foreman. The
  lease rules of `ship` are unchanged.
- `ship`'s docstring names the new refusals. `declare/delivery.py` (the `ship` help text) names them
  in one clause if that help lists `ship`'s refusals; otherwise it is unchanged.

Consequences the cards must state (section 3):

- During a restack, the CR below is shipped at its new head before the CR above it is shipped.
  Bottom up is already the order the stack driver's card gives ("Go on from the first CR, bottom
  up"). It becomes required: shipping the CR above first is refused (the second message when the
  CR above is already rebased onto the pushed branch below), because the CR below's recorded head
  is still the old one. The release, the top piece, is shipped last.
- A working CR placed on another CR's branch is refused at its next `ship` (its first one
  included) each time the CR below shipped a new head since the CR's branch was cut or last
  rebased. Its Driver rebases then, without waiting for the Foreman's `rebase:` note (Q5).
- A `ship` meant to record a forge change before a rebase (a PR put back to draft, then `ship`,
  then the rebase) is refused when the branch is not yet on the CR below: the `ship` comes after
  the rebase and push, and records the draft state and the new base at once.

### 2. `stack --out-of-draft` refuses a CR whose recorded head does not hold the CR below's (CLI)

File: `skills/chantier/scripts/cli/src/chantier/commands/delivery.py` (`_record_drafts`,
`_check_out_of_draft`), with the helpers of section 1.

- `_record_drafts` reads `landed` once, as section 1 does, and passes the `Repo` and `landed` to
  `_check_out_of_draft`. After the existing checks of every named CR (held, handed back ready with
  a PR, no draft under it, and the refusals CR-430/CR-431 add there), the chain check runs over the
  named CRs **bottom up** (their order in `chain`, the release CR last, Q10). For each: when
  `chain_below(d, c, repo, landed)` returns a CR and both that CR and the named CR have a recorded
  head, run the same ancestry read, `is_ancestor(<below.head>, <c.head>, cwd=<the repository>)`,
  with the recorded head of each, in the repository (the main checkout or the project's clone; a CR
  worktree shares its objects). The exclusions are those of section 1 (a fix, a held CR; a CR with
  no CR below, a CR below seen merged, or a CR below with no recorded head). The first CR that
  fails is the one refused.
- False: refuse with `EXIT_PRECONDITION`, nothing written (no `pr-draft` touch or event for any
  named CR, the existing refusals' behaviour). One message only (Q9: it compares two recorded
  heads, so it has no second message). Its fix starts by putting back to draft the PRs the stack
  driver has just turned ready on the forge (Q11): `<crs>` is the refused CR and every CR named in
  the same call that sits above it in `chain` (the release included when named), in chain order,
  comma-separated:

  `CR-442: branch not based on CR-441's head 1a2b3c4: put CR-442, CR-443' PRs back to draft, rebase onto chantier/batch-30/CR-441, push, ship, then stack --out-of-draft again; nothing recorded`

  Mandatory: the CR ids, the short head, `put <crs>' PRs back to draft` first in the fix, the branch
  below, `then stack --out-of-draft again` and `nothing recorded`. The message names no forge
  command (the CLI names no forge there; the card does). The rest of the wording is the Driver's to
  fit to the line limit.
- None: `CR-442: git cannot read CR-441's head 1a2b3c4: fetch, then stack --out-of-draft again;
  nothing recorded`.
- No flag skips it. `stack --draft` is not checked (a PR going back to draft is never a risk), and
  nothing is to be recorded with it after this refusal: the refused call recorded no PR out of
  draft (Q11).
- The docstrings of `_record_drafts` and `_check_out_of_draft` name the new refusal; the `stack`
  help text names it in one clause if it lists `--out-of-draft`'s refusals.

### 3. The cards (`skills/chantier/references/driver.md`, and one clause in `foreman.md`)

Places are found by their text; the line numbers in parentheses are today's, for orientation.

- **Stack driver**, a new paragraph right after the paragraph that starts **"Who moves a branch."**
  (before the paragraph that starts "Order the stack's CRs"), in substance (Q2, Q6, Q9, Q10, Q11,
  Q12):
  - **"Check the chain."** Before you conclude that a CR needs no restack, and before you turn any
    PR ready (`gh pr ready`, `glab mr update --ready`), check with `git -C <its worktree> merge-base
    --is-ancestor <head of the CR below> <its head>`, for each CR of the stack from the bottom, the
    release last, the head of the CR below read from `$CHANTIER stack`. Exit 0: it starts from the
    CR below. Exit 1: it needs a restack (or, for a working CR, its Driver's rebase). Any other exit:
    git cannot read a head; fetch and check again, never read it as "based". Matching PR bases on
    the forge prove nothing about the branches.
  - Then ship the CRs you move bottom up: `ship` refuses a CR whose branch does not hold the
    recorded head of the CR below (`branch not based on <cr>'s head`: rebase onto the branch it
    names), and a CR below is recorded at its new head only once it is shipped.
  - `<cr below>'s branch moved since its last ship (<rec7> -> <tip7>)`: that CR is not shipped at
    its new head. With no live Driver (handed back `ready`, or `blocked`), ship it first, then the
    CR above. When it is `working`, its branch and its `ship` are its Driver's: leave the CR above
    to come (its PR a draft, not turned out of draft), hand back the mergeable part below it as
    usual, and name it in the hand-back's tail: `<cr> to come: <cr below> not shipped at <tip7>`
    (one per such CR). The Foreman takes the stack again after that Driver's `ship`.
  - `stack --out-of-draft` refuses the same broken chain on the recorded heads, after you have
    already turned the PRs ready on the forge: put back to draft the PRs the refusal names (`gh pr
    ready --undo`, `glab mr update --draft`; nothing to record with `stack --draft`, the refused
    call recorded nothing), restack, push, `ship`, then `stack --out-of-draft` again.
  - A CR below the forge shows merged that the refusal still names: the record does not hold that
    merge yet. Once the journal or the record holds the merge (`status` shows it merged), `ship`
    again.
- **Stack driver: the hand-back line** (the paragraph "Green and checked: `[stack→foreman]
  hand-back ready to merge <stack link> <cr>=<link>…[ local gate …]`", ~1146): its tail admits
  the Q12 clause, `[ <cr> to come: <cr below> not shipped at <tip7>]…`, after the local gate tail.
- **Stack driver: "Making the stack."** and **the final-order take**: the sentences that turn the
  mergeable part ready ("Then turn every PR of the mergeable part ready (`gh pr ready`)", ~1076;
  "turn the mergeable part ready and `stack --out-of-draft`", ~1042), and the other `stack
  --out-of-draft` steps of the stack driver's section (insertion step ~1218, drop ~1249, hold
  ~1273, the release ~1122), each say "after the chain check" once, or point to it, so that no PR
  turns ready on a chain not checked (Q11).
- **Stack driver: "Who moves a branch."** The sentence on a working CR's Driver ("that Driver
  rebases once before its next push and `ship`s") adds: or at once when its `ship` is refused
  `branch not based on`, without waiting for the note.
- **Stack driver: the release CR** (the sentence "Restack it like any PR above (rebase onto the CR
  under it, push with `--force-with-lease`, `ship`, ...") adds: shipped last, after the top CR is
  shipped at its new head; `ship` refuses it otherwise (Q10).
- **Stack driver: bottom up where `ship` runs over several CRs.** The restack after a partial merge
  (its step 3, "then `ship` each one once"), the insertion (its step 2, "`ship` each one moved")
  and the drop's removal ("Removing a dropped CR", its step 3, "`ship` each one") say "bottom up" for
  those `ship`s.
- **CR driver: re-takes** (or "CR driver: ship and proof", wherever the Driver judges a `ship`
  refusal reads best), the **refusal sentence**, which names the first-ship case and both messages
  (Q5, Q7, Q8, Q9):
  - a `ship` refused with `branch not based on <cr>'s head` (your first `ship` included, on a
    branch taken onto another CR's branch that has shipped a new head since) means the CR below
    moved under you. You own your branch: rebase onto the branch the refusal names at once, without
    waiting for a `rebase:` note, as for a `rebase: stacked on <cr below>` note (in a series batch,
    the predecessor's branch), push with `--force-with-lease`, and `ship` again. This is a move:
    "CR driver: moves and conflicts" applies;
  - a `ship` refused with `<cr>'s branch moved since its last ship (<rec7> -> <tip7>)` means you
    are already on its branch, and that CR has not shipped its new head: do not rebase again; wait
    for its `ship` (its Driver's, or the stack driver's, bottom up), then `ship` again;
  - if the forge shows the CR the refusal names already merged, the record does not hold that merge
    yet: once the journal or the record holds the merge (`status` shows it merged), `ship` again.
- **Release driver**, in its bullets (beside "Your PR: you open it as the base says"), the same
  refusal sentence for the release CR (Q10): in an ordered batch the CR below is the top CR. A
  `ship` refused `branch not based on <top cr>'s head`: rebase onto the branch it names, push with
  `--force-with-lease`, `ship` again (`--conflict` by the `ship --conflict` rule, "Means: carries,
  conflicts and the early push"). `<top cr>'s branch moved since its last ship`: wait for that CR's
  `ship`, then `ship` again. A top CR the forge shows merged: once the journal or the record holds
  the merge (`status` shows it merged), `ship` again.
- **The stack batch paragraph** of "CR driver: re-takes" ("that branch is the stack driver's, never
  rebased by you but on a note", ~939): add "or on a `ship` refused `branch not based on`".
- **The `rebase: mode <mode>` paragraph** (starts "A CR taken (or a `note`) with `rebase: mode
  <mode>`", ~946-953): its pre-rebase `ship` goes. Put the PR to draft on the forge first (`gh pr
  ready --undo`, `glab mr update --draft`), rebase onto the base `take` printed, retarget the PR,
  push with `--force-with-lease`, then `ship` (`--conflict` by the rule above): that one `ship`
  records the draft state and the new base. Say why in a clause: a `ship` before the rebase is
  refused (`branch not based on`) when the new mode puts the CR on another CR's branch. In the new
  text, "rebase onto" comes before the paragraph's first "`ship`" (the guard of section 4 reads it).
- **The other `ship`s that follow a forge change** ("CR driver: ship and proof", the sentence "A
  change of a PR's base or draft state on the forge is followed by `ship <cr> <link>`", ~203; "Means:
  carries, conflicts and the early push", its first bullet, the same rule, ~484): add one clause to
  each: a `ship` refused `branch not based on` there means rebase first, as that refusal says, then
  `ship`. The Driver searches the cards (`driver.md`, `foreman.md`, and the others under
  `skills/chantier/references/`) for any other `ship` prescribed before a rebase on a CR placed on
  another CR's branch, and fixes each the same way. The `carries` refusal's "draft, then `ship`"
  (~539-546) applies to a PR on the default branch, which has no CR below: no change.
- **`foreman.md`, one clause** (Q12), in the stack rules' "**Each later take,**" list (~387-391,
  "a CR got its first PR ..., a working CR rebased onto its place ..."): add "a CR the stack
  driver's hand-back named `to come: <cr below> not shipped at <tip7>`, once `<cr below>`'s `ship`
  records a new head". Nothing else in `foreman.md`'s stack rules changes: the Foreman's existing
  notes (`rebase: stacked on <cr below>`, a series `rebase:` note) still carry the move; a Driver
  refused at `ship` no longer waits for them. If CR-438 has moved those rules into
  `foreman-stack.md` first, the clause goes there, at the same list (see Coordination).
- `agents/` and `com.github.copilot/agents/` are unchanged (the contract lives in the cards).

### 4. Tests (`skills/chantier/scripts/cli/tests/`)

One new file, `test_stack_chain.py`, built on `stack_world.py` / `batch_helpers.py` as the other
stack tests are, parametrized and fast. It calls the CLI in-process on states the CLI built (`open`,
`take`, `stack`, `ship`) with real git commits in the worktrees.

The ancestry read: one parametrized case per outcome on a real repository (an ancestor: True; not
one: False; an unknown SHA: None).

`ship`:

- a stack batch, A and B stacked (`stack A B`), B's branch cut from main: `ship B` exits 2, the
  message holds `B: branch not based on A's head <A7>` and `nothing recorded`, and the record is
  unchanged (B's `head`, `pr`, `pr_base` and the event count are the same as before the call);
- the same after B is rebased onto A's branch and pushed: `ship B` records as today;
- A shipped again at a new head (A amended and pushed), B not rebased: `ship B` is refused with the
  first message, naming A's new head;
- Q9: A amended and pushed but not shipped again, B rebased onto A's new remote tip and pushed:
  `ship B` exits 2 with `A's branch moved since its last ship (<A rec7> -> <A tip7>)` and `nothing
  recorded`, record unchanged; the same state with the `<remote>/<A's branch>` ref deleted from the
  clone: the first message;
- critic finding 3 (v3): A committed at a new head and shipped (recorded) but not pushed, so A's
  remote tip is an ancestor of A's recorded head, B rebased onto that remote tip: `ship B` is
  refused with the **first** message (`branch not based on A's head <A rec7>`), not the second;
- a stack CR not placed yet, taken onto A's branch (a live `start_on`), its branch cut from main:
  `ship` refused the same way (Q7);
- a series batch, B's predecessor A open, B's branch cut from main: refused the same way;
- Q10: the release CR of a stack batch, its branch holding the top CR's old head after the top CR
  shipped a new head: `ship <release>` refused naming the top CR; after the release is rebased onto
  the top CR's branch: recorded;
- Q8: A seen merged (a `merged@1` line for A's batch, CR and recorded PR link, appended through the
  journal's one append function, `hub/journal.append`, as the hub writes it), A still `working` or
  `ready` in the record, B rebased onto the default branch: `ship B` records; the same state with
  no journal line: refused with the first message (the refusal stands with no forge read);
- not checked (each `ship` records): a stack CR not placed yet with no `start_on` recorded; a stack
  CR not placed yet whose `start_on` owner is merged, and one whose owner is held (Q7); the first CR
  of the stack (base the default branch); a release with no open CR under it; a fix CR; a held CR;
  a series CR whose predecessor is merged;
- the head of the CR below unknown to git (a recorded `head` that is not a commit of the clone):
  refused with `git cannot read`, nothing recorded.

If the "recorded but not pushed" state of the critic-finding-3 case cannot be built with `ship` (if
`ship` needs the head on the remote), the case edits A's recorded `head` in the test world to a
local commit above A's pushed tip, named in the test as a prepared state.

`stack --out-of-draft`, one parametrized test (Q6, Q8, Q10, Q11): A, B and C stacked and handed
back ready with PRs, B's recorded head not holding A's recorded head: `stack --out-of-draft A B C`
exits 2 with `B: branch not based on A's head <A7>`, `put B, C' PRs back to draft` (B and every
named CR above it, not A) and `then stack --out-of-draft again; nothing recorded`, and `batch.json`
and `events.jsonl` unchanged (A not recorded out of draft either); `stack --out-of-draft A B` names
only B's PR; the case with B's recorded head on A's: accepted; A seen merged in the journal (B's
recorded head off A's): B accepted; the release CR ready with a PR, its recorded head off the top
CR's: refused naming the top CR and the release's PR; and the `git cannot read` case.

A guard on the shipped card, read from the repository at the head under test (not a copy):
`driver.md`'s "Stack driver" section holds `merge-base --is-ancestor`, `branch not based on`,
`branch moved since its last ship`, `not shipped at`, `PRs back to draft` (or the card's chosen
words for putting the refused PRs back, as long as `gh pr ready --undo` is named in the same
paragraph) and `stack --out-of-draft again`; its "Release driver" section holds `branch not based
on`; the stack driver's, CR driver's and Release driver's sections each hold `status` shows it
merged (the critic finding 4 sentence, matched on "holds the merge"); and in its `rebase: mode
<mode>` paragraph (found by its opening text, "A CR taken (or a `note`) with `rebase: mode"), the
first occurrence of "rebase onto" comes before the first occurrence of "`ship`" (today's text, "put
the PR to draft first (`gh pr ready --undo`, `glab mr update --draft`, `ship`), rebase onto ...",
fails it). In the stack driver's new "Check the chain" paragraph, `merge-base` comes before `gh pr
ready` (Q11). Add it to an existing card test if one already reads `driver.md` sections
(`test_came_back.py` reads `driver.md`), else to `test_stack_chain.py`. The `foreman.md` (or
`foreman-stack.md`) clause is guarded by its words `not shipped at`, read the same way from the
file that holds the Foreman's stack rules at the head under test.

Existing tests that ship, or turn out of draft, a stacked, taken-onto, series or release CR whose
branch was cut elsewhere (in `test_carry_ship.py`, `test_stack_*.py`, `test_release_*.py`,
`stack_world.py`, and others the Driver finds) are made true to the chain: each such branch is
rebased onto the CR below before its `ship`, as a real restack would do, and the test worlds'
recorded heads form the chain. The check is never weakened to keep an old test green. `just test`
stays within its budget (AGENTS.md).

### 5. The scenario (`scenario/run_scenario.py`, `scenario/README.md`)

**The helpers first** (critic finding 6 on v3). Today `push(w, cr_id)` (~861) always runs `git
rebase --quiet origin/main` in the CR's worktree; `ship(w, cr_id, title, base="main")` (~870) and
`driver_round(w, cr_id, filename, content, base="main")` (~883) call it, and their `base=` only
picks the target of a new PR (`open_pr`). So every scenario CR shipped through them is rebased off
any CR below, and the new check refuses its `ship`. The fix: `push()` rebases onto the CR's
recorded base, not `origin/main`:

- `push(w, cr_id, base: str | None = None)` rebases onto `origin/<base>`; with no `base`, onto the
  CR's recorded base read from the record (`w.cr(cr_id)`): its `pr_base` when recorded, else its
  `start_on` when recorded, else `main`. A series CR at its first ship with neither recorded gets
  the predecessor's branch from the `ship()` / `driver_round()` caller's `base=`.
- `ship()` and `driver_round()` pass their `base=` through to `push()` when the caller gave one,
  and otherwise let `push()` read the recorded base. Their default `base="main"` becomes `None`
  for the rebase (the PR target of a new PR stays `main` when nothing else is given, as today).
- The Driver checks each existing call of the three helpers: a CR on the default branch reads as
  today (base `main`), so the steps of unordered batches are unchanged.

In `stack_batch` (section 13), after `w.chantier("stack", one, two, three)` and the two
`forge_base` retargets, the scenario today ships `three` while its branch was cut from main
(`w.chantier("ship", three, w.cr(three)["pr"])`). It becomes the proof step:

- `ship three` exits 2, naming `three`, `two` and `two`'s short head, with `branch not based on`.
  Check that nothing was recorded (three's `head` and the last `ship` event unchanged).
- Then `restack(w, two, one)` and `restack(w, three, two)` (the existing helper, ~8173: rebase onto
  the CR below, push with a lease, `ship`), bottom up. The ship bases the following checks read
  stay as they are today (`three` on `two`'s branch, `one` on `main`).

`stack --out-of-draft` (the section that checks its refusals): add one refused call on a broken
chain, nothing written, its message holding `PRs back to draft`, only if a state with a CR's
recorded head off its CR below's is at hand there in one step; otherwise the parametrized test of
section 4 is its proof, and the PR says so.

Every other scenario step that ships, or turns out of draft, a stacked, taken-onto, series or
release CR not based on the CR below (the release of the step that checks "a release starts on the
top CR's branch" included) is made true to the chain the same way (the helpers' recorded base, or
`restack`), not by weakening the check. The scenario's README names the new checks in section 13's
description if that description lists `ship`'s checks.

## Evidence

- `just check` green (Linux, macOS, Windows per AGENTS.md); `just eval-dry-run` in the worktree
  (the change is under the CLI's `src/`).
- `just test`: `test_stack_chain.py` as in section 4, and the card guards read `driver.md` and the
  Foreman's stack rules as they ship at the head under test.
- `just scenario (ubuntu-latest)` green at the PR's head (a change to the CLI, the cards and the
  scenario). In section 13, the refused `ship` with its message and the record unchanged, then the
  bottom-up restack and the accepted ships.
- The PR body quotes one real refusal line from the scenario's output.
- No host or default matrix: the checks depend on neither the host nor a configured value (the
  remote's name is read from the project's configuration as every other remote read is, and only
  changes which message is chosen).

## Out of scope

- Any git write by the CLI, and any fetch: `ship` and `stack --out-of-draft` restack nothing,
  fetch nothing and change nothing on a refusal.
- A forge read for this check: a merge neither the record nor the journal holds is not seen (Q8).
- A flag or an order to force past either refusal; a `stack --draft` to record after the
  `stack --out-of-draft` refusal (Q11).
- Checking at `stack <crs…>`, at `forge-stack create|rebuild`, or at `take stack` (Q6). `stack
  <crs>` sets the order before the restack it calls for, so its CRs are not on the chain yet by
  design; `forge-stack` follows `stack --out-of-draft`'s ground on the forge (the PRs' bases, the
  five checks), and reaches the forge, not the record's heads; `take stack` is the Foreman's handing
  of a stack to be restacked, where a broken chain is the stack driver's work, which its card's
  `merge-base` line and the `stack --out-of-draft` refusal now guard.
- A `pr` check in `delivery.py`'s `stack` (the card keeps that rule).
- A change to `check_release_branch` or to the release's `take` (Q10: it stays as it is).
- A stack CR not placed yet with no live `start_on` (Q7).
- Commits a branch holds beyond the CR below (another CR's commits, a dropped CR's): the existing
  `_foreign_crs` refusal, the hold and drop removals and the PR-body checks keep that ground.
- Parallel batches, fix CRs.
- `commands/carry._ancestor` and its callers (they keep their two-way read).
- `foreman.md`'s stack rules beyond the one Q12 clause, and the new `foreman-stack.md` card beyond
  carrying that clause.

## Coordination with batch-30

This CR joins batch-30 (a stack batch) on top of the stack (`order add`). It depends on none of the
CRs in it; whichever lands later rebases onto the other. The overlaps, found by text (the CRs are in
`4-batch/2-actives/` and `4-batch/1-pending/` of the planning folder):

- **CR-430 park-live-cr and CR-431 hold-live-cr** (`2-actives/430-park-live-cr`,
  `2-actives/431-hold-live-cr`). Both change the base rules in `stacks.py` (`start_base`,
  `stack_base`, `chain`, `top_cr`: `is_held` becomes `out_of_order` / `apart` from `rails.py`, which
  `stacks.py` re-exports). Both add refusals to `_check_out_of_draft` (a parked CR, a dependent).
  Both add stack driver paragraphs in `driver.md` after "A CR held out of the stack" and edit "CR
  driver: re-takes" (`rebase: <cr> dropped`). This CR reads the base only through `stack_base` /
  `start_base`, `top_cr`, `_live_start` and `is_held`, so their rules apply to the check unchanged.
  Re-apply after either lands: rebase. If `apart(c)` exists, exclude `apart(c)` instead of
  `is_held(c)` from the CRs checked. Keep `stack_base`'s new `landed` keyword through their edits of
  `stack_base`. Put this CR's ancestry check after their refusals in `_check_out_of_draft`. Keep
  this CR's `driver.md` paragraph right after "Who moves a branch." (a different spot from theirs).
  Put its re-takes sentence after the paragraphs they add. Their hold and park steps that turn PRs
  out of draft get this CR's "after the chain check" pointer where they call `stack
  --out-of-draft`. Their tests that ship a dependent or a CR above a held or parked one must still
  pass: a dependent sits on the apart CR's branch, which holds that CR's recorded head.
- **CR-428 drop-to-next-batch** (`2-actives/428-drop-to-next-batch`). It edits `driver.md`'s
  "Removing a dropped CR" destination list (`3-ready` added) and the orders code. No shared
  function. A drop's removal (`rebase --onto`, push, `ship`, bottom up) passes the check as written;
  this CR's "bottom up" in that list's step 3 and its "after the chain check" in step ~1249 are a
  few words beside its edit. Re-apply: rebase, nothing to adapt.
- **CR-438 stack-shape-guard** (`1-pending/438-stack-shape-guard`, queued in the batch). It adds
  functions to `stacks.py` beside `stack_due` (`shape_blockers`, `shape_line`), changes the
  scripted Foreman (`Foreman.turn`) and adds checks in `stack_batch` (step 13) of
  `scenario/run_scenario.py`, around the same `stack one two three` call this CR's proof step
  follows. It moves the Foreman's stack rules from `foreman.md` into the new `foreman-stack.md` and
  leaves the stack driver's card out of scope. This CR's one Foreman clause (Q12, in "Each later
  take") goes where that list lives when this CR lands: `foreman.md` if CR-438 has not landed,
  `foreman-stack.md` if it has; whichever lands second carries it over, and the card guard reads
  the file that holds the list. Re-apply, whichever lands second: rebase. Keep both CRs' new
  `stacks.py` functions, which sit in different places (this one beside `stack_base`/`off_place`).
  In `stack_batch`, keep both CRs' added steps; CR-438's checks that read the shape line after
  `stack one two three` come before or after this CR's refused `ship three` and restack, as the
  Driver orders them, and its `asks ready-to-merge` checks need no `ship`. If CR-438's new steps
  ship a stacked CR, or turn one out of draft, that CR must be on the chain (restack first; the
  helpers of section 5 rebase onto the recorded base).

## Open questions (for the Chief of Staff)

None. The spec critic's six findings on v3 are applied: Q11 and Q12 as decided, and findings 3-6
as written above.
