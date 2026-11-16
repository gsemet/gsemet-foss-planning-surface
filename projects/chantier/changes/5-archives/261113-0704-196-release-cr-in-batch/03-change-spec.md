# A release CR asked in a batch is a normal CR of that batch

## Goal

The user (2026-11-12): "Si une CR de release est demandée dans un batch, elle est typiquement mise
en dépendance de tous les autres CR et donc ne pourra pas démarrer tant que le reste de la stack
est prête. Ça doit faire partie d'une possibilité normale et documentée et apparaissant dans
docs/batch-pace.svg."

A batch can run fully on its own (overnight, say) and deliver, in the morning, a complete PR
stack whose top PR is the release PR with its release notes. The user reviews the work and the
release together, can still fix the release PR, and merges the whole stack from the bottom up.
That merge is the go: the Release driver is started again and follows the project's release
procedure. chantier never names the steps of that procedure (a tag, a forge release, a
publication…): it knows only that there is a procedure to follow, and that the release PR, when
the procedure has one, is the top of the stack.

## Words used in this specification

- **Shared release:** a release CR that is not alone in its batch (`rails.alone()` is false: some
  CR other than a fix was in the batch).
- **Ordered batch:** a batch whose mode is `stack` or `series`.
- **The stack under the release:** the other CRs of the batch, fix CRs excepted, that are not
  merged or cancelled.
- **Top CR:** the last of the stack under the release in its order (`order`, which `stack`
  rewrites in a stack batch and `open` / `order add` set in a series).
- **Release PR:** the PR the project's procedure opens for the release (a version PR in
  chantier's own procedure). A procedure may have none.
- **The grant:** the explicit release grant the user gives with `order grant` ("auto"), as today.

## The behaviour

### Every release, in every mode

1. A release CR is a CR of its batch. It waits for every other CR of the batch, the ones added
   later too; the CLI keeps that list (`after`), as today, and `order after` stays refused on it.
2. **No version confirmation, ever.** The release no longer waits for `order confirm` before it
   starts. The version is the one the release CR's grill settled; when the grill left it open,
   the Release driver picks the best version from its context (the changes it ships, the
   project's versioning rules) and says why in the release PR's description (with no release PR,
   in its draft notes) and in a `note`. It never asks for the version.
3. A cancelled CR never holds the release back (as today); a blocked or working one keeps it
   waiting.
4. A release alone in its batch starts when taken, on the default branch, and its PR is ready on
   the default branch. Rules 5 to 11 below hold for it as for any release.
5. **Who merges the release PR:** the user. In an ordered batch, with the rest of the stack, from
   the bottom up, the release PR last; in a parallel batch or alone, once it is the only open PR
   of the batch. The steering session merges a release PR only under the grant, and then only
   once every other CR of the batch is merged or cancelled and the PR's base is the default
   branch. An approval (`order approve`) never lets it merge a release PR.
6. **The go:** the merge of the release PR (the user's, or the steering session's under the
   grant) is the go for the rest of the procedure. On the user's merge, the steering session
   starts the Release driver again, and it follows the project's procedure to its end with no
   further go from chantier; a go is asked only where the project's procedure itself asks for
   one (`handback blocked approval: <step>`, answered with `order approve`, or covered by the
   grant).
7. **A procedure with no release PR:** chantier waits until every other CR of the batch is merged
   (alone: none to wait for), then asks the user whether to run the release procedure (the user
   is back and interacting then). The Release driver may start before (rules 12 and 20) to
   prepare the drafts the user reviews; it then hands back waiting. The user's yes is recorded
   with `order confirm` (below), and it is the go for the rest of the procedure, as the merge is
   in rule 6.
8. **No irreversible step before the merge.** Until every other CR of the batch is merged or
   cancelled, and while an unmerged release PR is recorded, `release go` answers no, whatever
   the approvals say. The grant lifts only the second wait (rule 5: the steering session's merge
   under the grant); nothing lifts the first. After the merge: rule 6 or 7.
9. **Its gates:** what the project's procedure names, at the release PR's pushed head, and the
   forge's checks green there. No Verifier verdict. chantier adds no gate of its own.
10. **How it reads while it waits for the merge:** as a `ready` CR (its PR open and green,
    waiting for the merge), never as a blocked one.
11. **`order add` once the release has started stays refused** (the user declined the advisor's
    recommendation): a CR added after a release CR complicates the batch. The exception is the
    urgent fixes of a release that went wrong: `order add --fix-for <release-cr>`, as today.
    Afterwards comes a retro, which may feed the same batch or the next; the batch is normally
    paused at that point. Before the release starts, `order add` is accepted and the new CR goes
    under the release, as today.

### Ordered batch (stack or series): the release on top

12. **When it starts:** once a single branch holds all the work it ships, which is when every
    other CR is `ready` or `merged` (or cancelled) and the top CR's branch holds the recorded
    head of every other open CR of the stack under it. In a stack batch that means the stack
    driver has stacked them first.
13. **Where it starts:** on the top CR's branch (`take` and `handoff` print it as `base`; `ship`
    records it). With no CR left open under it, on the default branch.
14. **Its place:** always the top of the stack or the last of the series. `take stack` lists it
    last, with the top CR's branch as its base; the stack driver restacks it like any PR above;
    `stack` refuses an order that puts a CR above it (the existing check on `after` does it, since
    the release's `after` names every other CR).
15. **Its PR:** follows the shared definition of "ready to merge": a draft while its base is not
    the default branch; ready once the stack under it is merged and it is retargeted to the
    default branch and green. "A release PR is no draft" holds only for a release whose base is
    the default branch.
16. **What it covers:** everything between the previous release and its own head: what the
    default branch holds since then, plus every CR under it. The procedure's commands run on the
    release branch, so a commit list or a count taken "since the previous tag" is taken at the
    release branch's head (before its version commit when the procedure says so). The version
    commit is the last commit of the stack: nothing merges after it before the procedure's next
    steps.
17. **A CR under it changes after the release PR is prepared:**
    - A move with no change of content (a restack, a rebase onto the default branch after a
      partial merge): the stack driver restacks the release PR like any PR above; its checks run
      again; its notes are carried.
    - A change of content (a CR under it gets a new round, or is dropped): the release goes back
      to a Release driver, which runs the procedure again from its first step on the new base and
      refreshes the same PR (version commit, count, notes, captures). The drafts the user edited
      are read again, never rewritten from scratch.
    - The steering session decides which case it is from the CR's log (`log <cr>`); when unsure,
      it is a change of content.
18. **A defect the release finds before the stack is merged:** it goes back to the CR that owns
    it when one does (a `note` and a `take <cr> --note`, as for any ready CR), and the release is
    redone after (rule 17). A defect that belongs to no CR of the batch is a fix CR (`order add
    --fix-for`, on the default branch, outside the stack, as today); the stack is restacked on
    the default branch once it merges, and the release is redone.
19. **A stack merged only in part:** the release stays on top of what remains and cannot merge or
    act until the rest is merged or dropped. Dropping a CR under it is a change of content.

### Parallel batch: prepared after the merges

20. In a parallel batch each PR is on the default branch and no branch holds all the work until
    it is merged, so the release starts once the others are merged or cancelled (today's timing,
    without the confirmation), on the default branch. Its merge and its go are rules 5 to 8, as
    in every mode.
21. When the user asks for a release in a parallel batch, the Chief of Staff explains clearly why
    the release cannot be prepared before the merges (no branch holds all the work until then)
    and recommends a stack batch instead. A parallel batch cannot be switched to a stack (`order
    mode` switches only a series), so the recommendation is for the batch being opened, or the
    next one.

### Both steerings, and batches already open

22. Direct mode follows the same rules, with the Chief of Staff as the steering session.
23. A batch opened before this change keeps running after it, with no migration by hand: the new
    CLI reads the record as it is. A `confirmed` field written by the older CLI gives no go (the
    procedure's word of rule 7 is a new field), and a release PR merged under the older CLI gives
    no go for the later steps (the merge of rule 6 is recorded in a new field): such a release
    goes on with an approval per step or the grant, as it would have.

## What changes, area by area

### CLI (`skills/chantier/scripts/cli/src/chantier/`)

Each line of `work/today-refusals.md` is answered here; field names are the implementer's.

**`rails.py`**

- `waits_for` (refusal 1): for a release, met is `ready`, `merged` or `cancelled` in an ordered
  batch, and `merged` or `cancelled` in a parallel one. The docstring says so.
- `needs_word`, `WORD` and the confirmation step of `waits_all` and `check_take` (refusal 3) go:
  no take is refused for a missing confirmation, and `status` never shows `waits for the user's
  confirmation`.
- `check_take`: for a release, the unmet check applies when it is taken from `queued`, `ready` or
  `blocked` (not only `queued`), so a release sent back for a change of content waits until the
  stack under it is ready again. Its message says "ready or merged" in an ordered batch, "merged
  or cancelled" in a parallel one.
- New rail on the branch (rule 12), for a release in an ordered batch with CRs open under it:
  `take` is refused (exit 2) unless the top CR's branch holds the recorded `head` of every other
  open CR of the stack under it (a read-only `git merge-base --is-ancestor <head> <top branch>`
  in the main checkout, or the clone with a planning surface; the CLI changes nothing). A CR
  with no recorded head refuses too. The message names the CR and its short head, and says the
  stack driver stacks the CRs first (`take stack`).
- `release_go` (gap 9), the same in every mode, in this order: `budget`; `fix`; then a new
  result, `merge`, while any other CR of the batch (fix CRs excepted) is not merged or cancelled
  (nothing lifts it), or while a release PR is recorded and not merged and no grant is active
  (the grant lifts this one only: the steering session's merge, rule 5). Then `go` because the
  release PR was merged (the merge recorded by `order merged`, rule 6), or `go` because of the
  procedure's word recorded by `order confirm` (rule 7). Then, as today: an approval, the grant,
  `ask`. The `go` text names the PR or the word. The log keeps each result, `merge` included.
- `release_merged`: records the merged PR in its own field (the go of rule 6), besides the
  `merged: <pr>` note it writes today.

**`commands.py`**

- `_chain` (refusal 5): in a stack batch it includes the release CR, always last (sorted after
  every other CR whatever its `order`); fix CRs stay out. Docstring updated.
- `_start_base` and `_stack_base` (refusal 6): a release in an ordered batch starts, and its PR
  sits, on the top CR's branch (the last open CR of the chain, fix CRs out); with none open, the
  default branch. In a parallel batch or alone, the default branch as today. A series' top CR is
  the last open CR of the order.
- `_facts` (refusal 6): the release's `after:` line no longer says "a release starts from the
  default branch"; it says it starts on the top CR's branch in an ordered batch, and on the
  default branch once the others are merged in a parallel one.
- `handback` (refusal 7): `handback <release> ready <link>` with an unmerged PR recorded means
  the release PR is prepared: it applies the same head, clean-tree, pushed and long-gate checks
  as a CR (`--no-gate` as for a CR), **no verdict check**, and sets the CR `ready`; its second
  line says the release PR waits for its merge. With no PR recorded (after `order merged`, or a
  procedure with no release PR), `ready <release link or tag>` means released, as today (3-done).
- `_apply_order`, `merged` on the release: refused (exit 2) while another CR of the batch (fix CRs
  excepted) is not merged or cancelled: "the release PR merges last".
- `_apply_order`, `confirm` (refusal 2): its meaning changes to the user's word to run the
  release procedure (rule 7). Accepted for any release, alone or not, in every mode, once every
  other CR of the batch is merged or cancelled and no unmerged release PR is recorded, whether
  the release has started or not. Refused before that (the message names the CRs still open, or
  the release PR, and says the word comes once they are merged). It writes the new field, never
  `confirmed`, and a `procedure:` note. Its usage line becomes `order confirm <release-cr> --note
  "<the user's word to run the release procedure>"`. Today's "alone" refusal goes.
- `_add_release` and `_release_tag` (refusal 11): no "`order confirm`" and no "then on the user's
  confirmation"; they say the release starts once every other CR is ready (stack, series) or
  merged (parallel), and that its PR is the user's to merge. `_join_release` keeps adding the new
  CR to the release's `after`; it voids the new procedure word when one was given (not
  `confirmed`).
- `_check_release_open` (refusal 8): the rule is unchanged (refused once the release has started,
  `--fix-for` accepted); its message no longer says the release "ships what was merged before
  it", it says it ships the work under it.
- `release start`: keeps the recorded PR (an attempt refreshes the same release PR; a Driver that
  opens another one records it with `ship`) and clears the head. A merged PR is already cleared
  by `release_merged`.
- `release` (`go`): prints the `merge` result as `no: <ids> not merged: every irreversible step
  waits for their merge` or `no: the release PR <pr> is the user's to merge`, exit 2.
- `order after` on the release (refusal 4) stays refused; its message is kept.

**`cli.py`**: the help of `open --release` (line 68), `order` `kind` and `--note` (lines 81-89) and
`order add --release` (line 92) say the new rules: no "on the user's word if it has company";
`confirm` is "the user's word to run the release procedure, once the other CRs are merged";
`approve` no longer names a release PR's merge.

`STATUS.json`'s schema and `types/` do not change (no `just mod`).

### Cards (`skills/chantier/references/`)

**`concepts.md`**

- "Ready to merge" (lines 9-11): a release PR follows the same rule; the user merges it, last of
  the batch (in a stack or a series with the rest, from the bottom up); the steering session
  merges it only under the grant.
- "Batch" (line 95): "A release CR and a fix CR sit outside a series and a stack" becomes: a fix
  CR sits outside, on the default branch; a release CR is the top of the series or the stack: it
  starts on the top CR's branch once every other CR is ready and the top branch holds them all,
  and its PR is the top PR.
- "Dependencies": a release's `after` is met by `ready` or `merged` in an ordered batch, by
  `merged` in a parallel one; a cancelled CR never holds it back.
- "Release CR" (lines 145-150): rewritten from the behaviour above: a CR of its batch, after every
  other one, prepared on top in an ordered batch, after the merges in a parallel one; no version
  confirmation; in every mode the merge of the release PR is the go (with no release PR, the
  user's word once the others are merged); every irreversible step waits for the merge. chantier
  names no step of the procedure. The grant (now: the steering session's merge of a release PR,
  and the steps the procedure asks a go for) and the fix CR keep their definitions otherwise.

**`driver.md`**

- "Push" (lines 62-64) and the draft rule (line 91): a Release driver opens its PR as the base
  says: ready on the default branch, a draft on another base, turned ready when the stack driver
  retargets it.
- "Stack driver" (lines 257-260): the release CR is the top piece: `take stack` lists it last;
  restack it like any PR above (rebase onto the CR under it, push with `--force-with-lease`,
  `ship`), its checks run again, no `verifier` and no `inspector` for it (it has no verdict); a
  release with no PR yet is no anomaly, leave it; keep it a draft until it is the first PR on the
  default branch. A fix CR is not in the stack.
- "Release driver" (lines 273-335):
  - Irreversible action: rewritten without naming a tag or a package: any step of the project's
    procedure that cannot be taken back or that others see (the procedure names them; the merge
    of a release PR is one).
  - The base: the one `take` printed (the top CR's branch in an ordered batch), and a new attempt
    resets onto that base, not the default branch (line 285-287).
  - The version: from the specification; none there, the Driver picks the best one from what it
    ships and the project's rules, and says why in the PR description and a `note`; it never
    asks.
  - In every mode: prepare the release PR (in an ordered batch on top, its notes covering the
    previous release to its own head), pass what the procedure names at the pushed head, CI
    green, then `handback ready <pr link>[ draft on <base>]: waits for the merge` (no `blocked
    merge:`, no verifier). `release go` answers `merge` until the release PR is merged.
  - After the merge, a new Release driver goes on from the procedure's next step; each `release
    go` answers `go` because of the merge; a step where the procedure itself asks the user's go is
    `handback blocked approval: <step>`.
  - A procedure with no release PR: prepare the drafts (`note --draft`) and hand back `blocked
    waits: the other CRs' merge, then the user's word to run the release procedure` (alone: the
    user's word only).
  - Lines 319-322 ("A release PR is the Foreman's to merge, so it is opened ready … `handback
    blocked merge:`") go: the release PR is the user's to merge, and the steering session merges
    it only under the grant (the card says how it then hands back).
  - Taken back with `redo: <cr> <why>` (rule 17): `release start`, rebuild on the new base, run
    the procedure from its first step, refresh the same PR, read the drafts again.

**`foreman.md`**

- Lines 49-52: a release PR is never yours to merge, except under the grant once every other CR
  is merged or cancelled and its base is the default branch; an approval never covers it.
- Lines 116-120: the release starts once the others are ready (ordered batch; in a stack, once
  the stack driver has stacked them: `take stack` first, then `take <release>`) or merged
  (parallel); no confirmation ask. On the merge of the release PR (`order merged`), start the
  Release driver again at once. With a release handed back `blocked waits: …, then the user's
  word…`, once the others are merged, ask `release <cr>: the batch is merged; run the release
  procedure?` and take it back on `order confirm`.
- Line 126: "A release CR and a fix CR are outside it" becomes: a fix CR is outside it; the
  release CR is its top.
- New lines for rules 17 and 18: deciding a move from a change of content from `log <cr>`, `note`
  on the release that it is stale, then `take <release> --note "redo: <cr> <why>"` once the
  stack under it is ready again; a defect of the release routed to its owning CR.

**`chief-of-staff.md`**

- "Releases" (lines 651-669): no "open it preferably alone"; a release joins the batch of the
  work it ships, best a stack batch; in a parallel batch, rule 21's explanation and
  recommendation. The version is grilled at filing when the user can; otherwise the Release
  driver picks it and says why; no "settle the rest at the end", no `order confirm` for the
  version. `report.md` and `conversation.md` are written when the release joins the batch and
  refreshed at each Progress report until the Release driver has prepared the release PR (no
  longer at `order confirm`). The user merges the release PR (with the whole stack in an ordered
  batch); record each merge with `order merged`; that merge starts the release procedure. With
  no release PR: once the other CRs are merged, ask the user whether to run the release
  procedure; the yes is `order confirm <release-cr> --note "<the user's word>"`. `order add`
  stays refused once the release started, `--fix-for` accepted for urgent fixes.
- Line 338 (the command list): the `order confirm` line says its new meaning.
- "auto" text (lines 671-692): names no tag or publication ("the irreversible steps of the
  procedure"); "auto" lets the steering session merge the release PR without the user, and covers
  the steps the procedure asks a go for; the `order confirm` word it never covers is the
  procedure's word. Its fix limit and budget do not change.
- "Steering a batch yourself" (line 555): unchanged rules, same text as the Foreman's for the
  release.

`agents/` and `com.github.copilot/agents/` hold no release rule: no change expected; if one is
made, both hosts together, bodies identical.

### The project's own release procedure (project rules for chantier)

- `CONTRIBUTING.md` "Release", step 1 (line 154): from an up-to-date `main` with green CI, or, for
  a release CR on top of a stack or a series, from the top CR's branch; the version is the
  release CR's, else the Driver's choice with its reason in the PR. Step 3: the user merges the
  version PR, last (in a stack from the bottom up); that merge starts the next steps. Lines
  129-134: the campaigns read the main checkout, so they run before the batch, or after the merge
  of everything under the version PR and before the user merges it.
- `docs/release-process.md`: lines 37-38, N is counted on the release branch before the version
  commit (the same number once merged by rebase); line 66 and "Which batch" (lines 133-139): the
  release joins the batch whose work it ships, best a stack batch, its version PR on top;
  `report.md` and `conversation.md` are written when it joins and refreshed until the version PR
  is prepared, not "at `order confirm`".

### Docs

- `docs/use-cases-foreman.md` "Make a release" (lines 109-132): say "release v1.4.0" with the work,
  best in a stack batch; the release waits for every other CR, starts once they are ready, and its
  PR is the top of the stack; you review the work and the release together and merge from the
  bottom up; that merge starts your release procedure; with no release PR in it, the Chief of
  Staff asks you after the merge. In a parallel batch, it is prepared after the merges, and your
  merge of its PR is the go there too. The grant table and line 131 say the grant lets the
  Foreman merge the release PR for you; an approval does not.
- `docs/use-cases-direct.md` "Make a release" (lines 111-114): the same.
- `README.md` lines 86-87: a fix CR sits outside a series and a stack; a release CR is their top.
- `docs/release-driver.svg` and `docs/release-driver-texts.md`: the "order confirm" item (svg
  line 105, texts line 104) and the footnote's target (svg line 224, texts line 155) say the new
  start (the others ready on top of a stack, or merged in a parallel batch; no confirmation). No
  redraw beyond the false text.
- `docs/cr-lifecycle.svg` and `docs/cr-lifecycle-texts.md`: "merges release PR on release go" (svg
  line 300, texts line 381) says that you merge the release PR, and the Foreman only under the
  grant. No redraw beyond the false text.
- `docs/batch-modes.svg` says nothing of the release: unchanged.
- `scenario/README.md` lines 77-83: the release list says the new checks.

### `docs/batch-pace.svg` (no companion texts file, none added)

- The frame "🚚 the release waits for every CR in here" (lines 64-66) and the release box outside
  it (lines 119-124) go.
- **batch-06 (the stack):** the release is a CR of the batch: a release-coloured box waits above
  the slots, with "waits for" arrows from the other CRs; it runs in a slot once they are ready;
  it is the top piece of the PR stack, merged by the user in the same bottom-up merge; after that
  merge, a release mark on main shows that the project's release procedure runs (no tag, no
  publication named).
- **batch-07 (parallel):** the release is drawn the same way, as a CR in a slot lane inside the
  batch with its "waits for" arrows, started after the merges; the user's merge of its PR, then
  the same release mark on main.
- The title, the legend and batch-08 stay. The caption of batch-07 may keep "the release last".
  The `<desc>` (line 3) says the same as the drawing: no "runs last, alone".
- The layout (widths, positions) is the implementer's; the width may grow.
- The PR shows the diagram rendered before and after, for the user's review.

### Scenario (`scenario/run_scenario.py`)

- Section 14 (`release`, parallel, lines 3040-3196): no `order confirm`; once the other CR is
  merged, the release is taken at once. The release PR's merge: `release go` refused with an
  `order approve` (the approval no longer covers it); the user's merge (`order merged`) is the go
  for the later steps with no approval. The fix flow stays. The grant flow: under the grant the
  Foreman merges the release PR (`release go` answers `go` for it) and the later steps go on.
- Section 14c (`release_last`, lines 3261-3378): the confirmation checks become the new rules:
  `order confirm` refused while CRs are open, accepted after (alone too); no "waits for the user's
  confirmation"; `order add` refused once the release started, `--fix-for` accepted.
- A new section: a stack batch with two CRs and a release (`open --mode stack --release 3`), see
  "Evidence".

## Out of scope

- A second release in a batch; a release that ships only part of a batch.
- Any change to "auto"'s fix limit (three under the grant) and budget; the release notes' content
  rules. The grant changes only as rule 5 and rule 8 say (an approval no longer covers a release
  PR's merge; the grant does).
- A new CLI command, or a renamed one (`release published` keeps its name; its help says the
  release is out by the project's procedure).
- A parallel batch switched to a stack; a release prepared before the merges in a parallel batch.
- Running tonight's batch: `work/today-refusals.md` "Routes for this batch" is the Chief of
  Staff's, not this CR's.

## Evidence

The CR passes `just check` (Linux, macOS, Windows) and `just scenario` (it changes the CLI and the
cards). `just mod` is not needed (no change to `hooks/` or `types/`); if the change touches them,
it passes `just mod` too.

New scenario section, each a `check` with the CLI's real output:

1. Stack batch, CR-a and CR-b queued, release CR-r: `take CR-r` refused (exit 2) naming each CR
   not ready; `status` shows no "confirmation".
2. CR-a and CR-b ready but not stacked (CR-b's branch does not hold CR-a's head): `take CR-r`
   refused, naming CR-a's short head and `take stack`.
3. Once stacked: `take CR-r` accepted; its facts print `base` = CR-b's branch; `take stack` lists
   CR-r last with CR-b's branch as base.
4. `stack CR-r CR-a CR-b` refused (CR-r would sit under CRs it waits for).
5. `release go CR-r --note "<a step>"` refused, exit 2, the `merge` text naming CR-a and CR-b,
   with an approval given and under a grant.
6. The release commit, gate, `ship` (base recorded = CR-b's branch), `handback CR-r ready <pr>
   draft on <base>: waits for the merge` accepted with no verdict; CR-r is `ready` in `status`
   and its STATUS icon is not red.
7. `order add --note <folder>` refused (started), `order add --fix-for CR-r` accepted (then
   dropped).
8. `order merged CR-r` refused while CR-a or CR-b is open; `order confirm CR-r` refused while they
   are open.
9. `order merged CR-a`, `order merged CR-b`: `release go CR-r` still refused (the release PR is the
   user's to merge) with an `order approve` given; under a grant (`releases=1 budget=5`) it
   answers `go` (the steering session's merge).
10. `order merged CR-r`: CR-r back to `queued`, taken by a new Release driver; `release go` answers
    `go` naming the merged PR, for two different steps, with no approval and no grant; `release
    published`, `handback ready <tag link>`: CR-r in `3-done`, the batch pauses.
11. A change of content: with the release prepared, CR-a taken back for a round: `take CR-r --note
    "redo: …"` refused until CR-a is ready again (and restacked), then accepted; `release start`
    keeps the PR recorded.
12. No release PR: a second stack batch where the release hands back `blocked waits: …`; `order
    confirm` refused before the other CRs' merge, accepted after; `release go` then answers `go`
    naming the word; no `confirmed` field written.
13. Series: a release in a series of two starts on the second CR's branch once both are ready.
14. Parallel: the release starts after the merges; its PR on the default branch; `release go`
    refused with an approval until `order merged <release>`, then `go` naming the merged PR.
15. Compatibility: a batch record with a release carrying `confirmed` (the older CLI's field) and
    a `merged: <pr>` note but no field of the new CLI: `release go` answers `ask`, not `go`.
16. Alone: `open --release 1` alone, taken at once, base the default branch; `order confirm`
    accepted before a release PR is recorded; once one is recorded, `release go` answers `merge`
    until `order merged`.

Docs checks, by the Verifier: the sentences quoted in `work/today-refusals.md` rows 12-18 and 21-23
are gone from the cards and docs named above (a `rg` with no match for "sit outside a series and
a stack", "A release CR and a fix CR are", "confirm the version", "at `order confirm`", "runs last,
alone", "the Foreman's to merge"); `docs/batch-pace.svg` is valid SVG and rendered to PNG before
and after, both images in the PR.

## Decisions carried from `02-answers.md`

Every answer is carried above: the release as a CR of its batch (rules 1, 14), what it waits for
(1, 3), when it starts (12, 20), where it stands (13, 14), its PR (15), what it covers (16), how it
reads (10), a CR changing under it (17), a defect before the merge (18), irreversible steps after
the merge (6, 8), who merges it (5), a release alone (4), direct mode (22), older batches (23),
scope and diagrams (areas above), the risk's rail in the CLI (8, `release_go`), checks that run
only on the default branch (`CONTRIBUTING.md` line), stale notes (17), partial merge (19), gates
(9). The user's own answers rank above the advisor's: no version confirmation and the Driver's
choice of version (2); the parallel timing and the Chief of Staff's explanation (20, 21); the
merge as the go and the Release driver started again (6); chantier naming no step of the
procedure, and the no-release-PR path (7); `order add` refused once the release started, urgent
fixes excepted (11). The Chief of Staff's last answer, from the user's rule: one rule in every
mode, the user's merge of the release PR is the go, and the steering session merges a release PR
only under an explicit grant (5, 6, 8, 20).

## Open questions

None.
