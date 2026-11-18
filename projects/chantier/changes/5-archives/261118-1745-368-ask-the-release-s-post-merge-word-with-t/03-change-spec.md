# Ask the release's post-merge word with the merge go

## Goal

Today a release goes like this. The version PR is ready, the user merges it, and the Release
driver started at that merge hands back `blocked approval:` for the tag and the forge release
(CONTRIBUTING.md "Release" steps 4 and 5). The user says yes, and a second Release driver starts
to run them. This happened in v0.12.0 (CR-352) and v0.13.0 (CR-366): in CR-366, `order merged`
came at 16:02, the hand-back `blocked approval: just tag ...` at 16:03, `order confirm` "oui pour
les 2" at 16:08, and a second take at 16:08.

The user wants one question and one Release driver. When the version PR is offered to merge, the
Chief of Staff asks in the same message for the user's word on the irreversible steps that follow
the merge, each one named. The yeses are recorded before the merge. The one Release driver started
at the merge then runs every step the user said yes to, and asks only for the others.

## What the CLI does today, and its one change

The CLI already accepts the word before the merge:

- `order approve <release-cr> --note "<action>"` (`commands/orders_apply.py`, `_approve`) refuses
  only a CR that is not the batch's release CR (`orders_release.release_cr`) and an empty note. It
  accepts the word while the release PR is recorded and not merged, and appends it to the CR's
  `approvals` and to its notes (`approved: <note>`).
- `order confirm` is the wrong order for this word, and it refuses it: while `c.pr` is set it
  answers "the release PR ... is not merged: the word comes once it is merged". Its meaning stays
  "the user's word to run a procedure with no release PR".
- `order merged` on the release (`rails_release.release_merged`) clears `pr`, sets `merged_pr` and
  leaves `approvals` as they are. `handoff <release-cr>` (`commands/facts.py`, `_status_lines`)
  then prints `grant: ...; attempts <n>; approvals unused: <a>; <b>`, so the Driver started at the
  merge sees the user's yeses.
- After the merge, `release go` answers `go` because of `merged_pr`, for any action, and consumes
  no approval. Holding a step for the user's word after the merge stays the cards' judgement; the
  CLI does not enforce it.
- With the release PR recorded and no grant, `release go` answers `merge` before it reads any
  approval, so an approval never covers the version PR's merge.

**The one CLI change (in scope by the spec critic's finding, `02-answers.md`).** Under a live
grant ("auto": `grant.autonomous > grant.published`), with the release PR recorded and not merged,
`release_go` (`skills/chantier/scripts/cli/src/chantier/rails_release.py`, lines ~68-82) reaches
the `elif c.approvals:` branch before the `elif granted:` one. So the steering session's `release
go <cr> --note "merge <pr>"` spends the first approval the user gave for a post-merge step (its
`why` reads "the user approved: <tag step>"). That step then drops out of `approvals unused:` for
the Driver started at the merge.

The change: while `c.pr` is set (the release PR is recorded and not merged), the answer depends
on the grant alone. With no grant, the answer is `merge`, as today. Under a grant, the answer is
`go` with the grant's `why` ("the user allowed <n> releases without asking; <k> published"), and
no approval is read or spent. In code, `if c.pr and not granted: return merge` becomes a branch
on `c.pr` that answers from the grant, ahead of the `merged_pr` / `procedure` / `approvals` chain.
Everything else stays:
- the order of the other branches;
- the budget and `fix` refusals before them;
- an approval's spending when there is no PR recorded and none merged.

Update `release_go`'s docstring and the `commands/release.py` `release()` docstring if they say
otherwise. No new command and no new field.

## What changes

The cards are shared by both hosts. The agent files (`agents/`, `com.github.copilot/agents/`) hold
no contract and do not change.

### 1. `skills/chantier/references/chief-of-staff.md`, "Releases"

Add a paragraph after the sentence "The user merges the release PR (...); record each merge with
`order merged`; that merge starts the release procedure.":

- **When.** The release PR is offered to the user to merge. That happens at the `ready-to-merge
  <release-cr>` ask (a parallel or series batch), or at the complete `stack-ready-to-merge` whose
  top is the release PR (a stack batch).
- **What the ready line adds.** In that same message, ask the user's word for each irreversible
  step that the project's release procedure runs after the merge. Name each step on its own (for
  chantier: CONTRIBUTING.md "Release" step 4, `just tag`, and step 5, `gh release create vX.Y.Z
  --verify-tag ...`). The user may answer yes to all, yes to some, or nothing.
- **What the question leaves out.** It never asks about the merge itself, which stays the user's.
  It never asks about posting the announcement, which stays the user's and is never an agent's
  step.
- **Recording a yes.** Before `order merged`, record each yes with one `$CHANTIER order approve
  <release-cr> --note "<step>: user, <YYYY-MM-DD>: '<the user's words>'"`, one order per step.
  When the user answers and merges in one message, the approvals come first, then `order merged`.
  In Foreman mode, send all the lines to the Foreman in one message.
- **No word at the ready ask.** Nothing is recorded, and today's path stays. The Release driver
  started at the merge hands back `blocked approval: <step>`, the approval ask follows as the
  card already says, and the answer is `order approve`.
- **A release redone before its merge** (a `redo: <cr> <why>`, or a new attempt after a fix).
  - The yes already recorded still holds: it covers the steps after the merge, and the user's
    merge of the version PR stays their review of its content. Nothing is recorded again.
  - The next ready line for the version PR names the steps already approved (for example
    "already approved: `just tag`, `gh release create`") and asks only for the steps with no yes
    yet, so the user can still say "wait".
  - The approved steps come from `$CHANTIER handoff <release-cr>`'s `approvals unused:` line.
- **A "wait" on an approved step, said before the merge.**
  - Write it at once in the release CR's `02-answers.md`: one line with the date, the user's
    words and the step. This is not an order and not a take: an `order note` on a ready CR is a
    take, and the Driver would restart before the merge.
  - Then close the summary gap that the file's change opens ("A CR's summary").
  - When you record `order merged <release-cr>`, read that file. Right after the merge, in the
    same relay (and the same message to the Foreman), record one note per step: `$CHANTIER order
    note <release-cr> --note "wait: <step>: user, <YYYY-MM-DD>: '<the user's words>'"`.
- **A "wait" said after the merge.** It is recorded the same way, as an `order note ... "wait:
  …"`, at once.
- **"auto".** The "auto" tip and the approval question's "auto" answer stay as they are. Under a
  live grant, the steering session merges and there is no ready line to the user. Approvals
  already recorded before an "auto" stay whole: the grant's merge go spends none (the CLI change
  above), so the Driver started at the merge still sees them. The post-merge steps go under the
  grant anyway.

In the same file, align the line under "On an approval ask (`ask ... blocked <release-cr> approval:
<action>`)" if it needs it: the user's word for a post-merge step is always `order approve`,
before or after the merge. `order confirm` stays only for a procedure with no release PR. (In
CR-366 the Chief of Staff used `order confirm` after the merge. The CLI accepted it there only
because the merge had cleared `pr`.)

In the paragraph that starts "In every mode, a `ready-to-merge` ask is offered to the user as
mergeable now" (around line 1042), and in the complete-stack paragraph (around line 1104, "says
the stack is complete"), add one clause: "for the release PR, the same message asks the
post-merge word (Releases)".

### 2. `skills/chantier/references/foreman.md`

**The release bullet** (around line 297, "A Release driver takes the release CR ..."). After "On
the merge of the release PR (`order merged`), start the Release driver again at once.", add:

- The take note names the steps the user approved before the merge. Their list comes from the
  `approvals unused:` line of `$CHANTIER handoff <release-cr>`, for example `take <release-cr>
  --note "merged: <pr>; approved before the merge: <step>; <step>; the other irreversible steps
  wait for the user's word"`.
- With no approval, the note says the steps wait for the user's word, as today.
- A step with a `wait: <step>: …` note recorded after its approval (the CR's notes, in `handoff`)
  is named as held, not approved: for example `… approved before the merge: <step>; held (wait):
  <step>; …`. The Chief of Staff records the `wait:` notes right after `order merged`, in the
  same relay, so read `handoff` after every line of that relay.
- Under the grant, the Foreman's own `release go <cr> --note "merge <pr>"` no longer spends an
  approval. The list is the same whether the user or the Foreman merged.

**The orders bullet** ("Orders are the user's word", around line 164), or the same release bullet.
Add one rule:

- Take this case: an `order approve` on a release CR handed back `ready` whose release PR waits for
  its merge. It is not work for a Driver. Mark it `order done` at once, and do not take the CR: the
  PR stays as it is, ready.
- The approval waits in the record for the Driver started at `order merged`.
- An `order approve` on a release CR that is `blocked approval:` keeps today's path, a take with
  the note.

In direct mode, the Chief of Staff does this as the Foreman's work, as today.

### 3. `skills/chantier/references/driver.md`, "Release driver"

Rewrite the bullet "A release PR merged (...) needs no further go from chantier: ..." (around line
1191) so that it says:

- A release PR merged (on the forge, and `release go` answers `go` because of the merge) needs no
  further go from chantier.
- A step after the merge waits for the user's word when the procedure, the release CR's
  specification or the take note holds it for the user's approval.
- Each such step that an approval names runs without a hand-back. The approvals are in `handoff`'s
  `approvals unused:` line, the `approved:` notes and the take note. Under a grant they are there
  too: the merge under the grant spends none.
- A `wait: <step>: …` note later than the approval of the same step is stronger: that step is held
  as if never approved. (`approvals unused:` still lists it: the CLI keeps no withdrawal.)
- Run the procedure's steps in its order, approved ones included. At the first held step that no
  approval names, `handback blocked approval: <that step>[; <each later held step with no
  approval>]`. Steps already run are named in a `note`. A later held step that is already approved
  is not asked again.
- The publication bullet stays unchanged: a refusal by the host gives `handback blocked approval:
  publish: <the exact command>`, and the steering session gives the command to the user.

The bullet at the top of the section ("Under a grant ("auto"), it answers `go` for the steering
session's merge of the release PR ...") gains: "and spends no approval for it". The "Release
driver: the end" checklist is unchanged.

### 4. `scenario/run_scenario.py` and `scenario/README.md`

**The scripted Foreman** (`Foreman._order`, around lines 610-633, and `Foreman.candidates`,
around lines 635-657). Today it sends a pending `approve` on a `ready` CR back to a Driver
(`approve: <note>`). Change it to follow the card:

- An `approve` order on a release CR (`kind == "release"`) whose status is `ready` is marked
  `order done` at once.
- Such an order is not a candidate for a take.
- An `approve` on a `blocked` release keeps today's take.
- When `candidates` reads a queued CR's last note to find why it is back (`BACK_NOTES`), it skips
  `wait:` notes as it already skips `main checkout:` ones. So the release's take at the merge still
  reads `merged: …` when a `wait:` note follows it.

**The parallel release** (unit `release`, around lines 6703-6727). Today it records `order approve
rel --note "merge the release PR <pr>"`, marks the pending orders done by hand (lines 6709-6711),
then grants and lets the scripted Foreman merge under the grant. Before the change, the Foreman's
merge go spent that approval. Now:

- The hand loop that marks the orders done is removed where the scripted Foreman's new rule does
  that work.
- One added check: once the Foreman has merged under the grant (after line 6727),
  `w.cr(rel)["approvals"]` still holds the approval recorded before the grant, and the `release-go`
  event of the merge carries the grant's `why` ("allowed … without asking"), not "the user
  approved".

**The release on a stack** (`release_on_stack`, around lines 7088-7093). Today it approves `tag
v1.8.0`, checks the `merge` refusal, grants `releases=1`, and checks that `release go … tag`
answers `go:`. After the change, that `go` is the grant's: add to the check that its text says
"without asking", and that `w.cr(r)["approvals"] == [tag]` afterwards (nothing spent).

**The README.** Update the `release` coverage bullet (`scenario/README.md` lines 332-343). Add:
"an approval recorded while the release PR waits for its merge takes no Driver, is not spent by a
merge under the grant, and the Driver started at the merge sees it (`approvals unused:`); a
`wait:` note recorded right after the merge leaves the take at the merge reading `merged:`". Keep
the `(unit: release)` marker, which `skills/chantier/scripts/cli/tests/test_scenario_coverage.py`
reads.

### 5. A test of the answer

In `skills/chantier/scripts/cli/tests/test_rail_refusals.py` (or the test file that already
prepares a release CR, if one fits better), add one parametrized test. It calls the CLI in-process
on a prepared record (`write_record`): a release CR whose PR is recorded and not merged, every
other CR merged, the budget unspent, and one approval `tag vX`. For `release go <cr> --note "merge
<pr>"`:

- no grant: exit 2 (`EXIT_PRECONDITION`), text starts `no: the release PR`, and `approvals` stays
  `["tag vX"]`;
- grant `releases=1`: exit 0, the text says `without asking`, and `approvals` stays `["tag vX"]`.

The test is fast, with no git and no forge, and keeps `just test` within its budget.

## Decisions carried from `02-answers.md`

- The ready line for the version PR also asks the user's word for the irreversible steps after the
  merge (chantier: the tag and the forge release), each named, in the same message. Yes to all,
  some or none: §1.
- A yes is recorded before the merge, with the user's words and the date, with `order approve`,
  one per step, before `order merged`. The CLI accepts it. `order confirm` stays the word for a
  procedure with no release PR. Then `order merged` starts one Release driver that runs every
  approved step and asks only for the others: §1, §2, §3.
- With no word at the ready ask, today's path stays: the Release driver asks after the merge: §1,
  §3.
- A release redone before its merge (a `redo:`, a new attempt after a fix) keeps the yes already
  recorded. The next ready line names the steps already approved, so the user can still say
  "wait": §1.
- A "wait" given before the merge is written at once in the release CR's `02-answers.md`, with the
  date and the user's words, not as a take. The Chief of Staff reads that file when it records
  `order merged`, and only then writes `order note <release-cr> --note "wait: <step>: user,
  <date>: '<words>'"`, in the same relay. The take at the merge names the step as held, and the
  Release driver treats a later `wait:` note as stronger than an earlier approval of the same
  step: §1, §2, §3.
- Approvals recorded before an "auto" stay whole. Under a live grant, `release_go` lets the release
  PR's merge go before any approval is read: the one CLI change, §2, §3, §4, §5.
- "auto" otherwise unchanged. An approval never lets any agent merge the version PR. Posting the
  announcement stays the user's: §1.
- Both hosts' cards change together (they are shared files). No new CLI command.

## Out of scope

- Any other change under `skills/chantier/scripts/cli/src/`. This includes the `approvals unused:`
  label, which keeps its wording even after the Driver has run the approved steps, and any order
  that withdraws an approval.
- The CLI enforcing a held post-merge step: after the merge, `release go` keeps answering `go`.
- A procedure with no release PR (`order confirm`), the fixes grant, the budget.
- The "Released in" issue comments, which keep their own yes after `release published`.
- The second retro point of CR-366 (`handoff` printing `PR: none` for a merged release). It is a
  separate CR.
- CONTRIBUTING.md "Release", docs/release-process.md and docs/release-driver-texts.md. The project's
  procedure does not change, and the last of these already describes the owner's single
  "publish, or auto".
- `hooks/`, `types/`, the board.

## Host and default matrix

The cards and the CLI are the same on both hosts. Only the publication step's permission depends
on the host, and that is existing behaviour.

- Claude Code, no grant, the user said yes to the publication at the ready ask: the host's release
  rule is offered only under a grant, so `gh release create` may be refused or judged by the
  classifier. The existing route then applies, `handback blocked approval: publish: <exact
  command>`, and the user runs it. A real run proves whether one Driver goes to the end here.
  The scenario cannot.
- Claude Code, a live grant ("auto"): the steering session merges. Its merge go spends no
  approval (proved by §5's test and §4's scenario checks), and the post-merge steps go under the
  grant.
- Copilot, either case: the same card text and CLI. The run is **unproved** on Copilot, as the
  rest of the release path is.

## Evidence

- `just check` passes at the PR's head.
- `just test` holds §5's test, within the budget of AGENTS.md.
- `just eval-dry-run` passes in the worktree at the pushed head (owed: a change under `src/`).
- `just scenario` (the pipeline's `just scenario (ubuntu-latest)` job, green at the PR's head) runs
  the extended unit `release`. In the parallel release it runs §4's added check. In
  `release_on_stack` (section 14d) it runs the changed check at lines ~7088-7093, then, between
  the release PR's last `ready` and its `order merged`, with no grant live at that moment, six
  checks:
  1. A second `order approve <r>` (for `publish`) is accepted while the release PR is recorded and
     not merged, next to the `tag` one already there.
  2. `fm.turn()` then starts no Driver for the release. The release stays `ready`, with its PR
     recorded, and the orders are done.
  3. `release go <r> --note "merge the release PR <pr>"` still answers `merge` (exit 2).
  4. A redo before the merge (`release start <r>` for a new attempt) keeps both approvals:
     `handoff <r>` still prints them under `approvals unused:`.
  5. After `order merged <r>` and `fm.turn()`, the Driver started for the release (`fm.started[-1]`
     starts with `<r> merged:`) gets facts that carry `approvals unused: ` with both notes, and
     `release go` answers `go` for both steps.
  6. A "wait" after the merge: in a second release of the unit (or a second pass), `order merged
     <r>` then `order note <r> --note "wait: publish v1.8.0: user, <date>: 'wait'"` before
     `fm.turn()`. The note order is done with no take of its own, `fm.started[-1]` still starts
     with `<r> merged:`, and the CR's notes hold the `wait:` note after the `approved:` one.
     `approvals unused:` still lists the step: holding it is the Driver's judgement, by the card.
     Leave this check out if it needs more than the scripted Foreman's `BACK_NOTES` skip above.
- The cards' change is reviewed in the diff. No new test asserts card text. A "wait" written in
  `02-answers.md` before the merge is a card rule with no CLI part, so nothing scripts it.
- No `just mod` is owed (no `hooks/` or `types/` change). In the batch, the CR on top runs `chantier
  gate` locally, as AGENTS.md says.

## Open questions

None.
