# Running this batch that way today: what refuses or contradicts it

The batch: a stack of about 15 CRs with a v0.9.0 release CR whose PR is the top of the stack,
started once every other CR is ready (not merged). Read on 2026-11-12 at `8c003ae`, CLI under
`skills/chantier/scripts/cli/src/chantier/`, cards under `skills/chantier/references/`. Nothing
was run: every line below is from reading the code and the cards.

Short answer: a CR of kind `release` cannot be started before the others are merged, and no
order changes that. The true shape needs this CR first. Three routes are at the end.

## The CLI

| # | Where | What it does today | Message | Without a code change |
| --- | --- | --- | --- | --- |
| 1 | `rails.py:112` (`waits_for`), `rails.py:203-206` (`check_take`) | For a release, a dependency is met only when merged or cancelled; `take` of the release is refused while any other CR is ready but not merged | `CR-n waits for CR-a ready, CR-b ready: it starts once each is merged or cancelled` (exit 2) | Cannot, needs the CR first |
| 2 | `commands.py:1114-1117` (`order confirm`) | The confirmation is refused while the release still waits, so it cannot be given in advance | `order confirm: CR-n still waits for CR-a ready: give the word once the others have ended` | Cannot. The user gives it after the merges |
| 3 | `rails.py:121-123`, `rails.py:212-214` | Once the others have ended, `take` is still refused without the confirmation | `CR-n needs the user's confirmation (`order confirm`): the Chief of Staff grills the version with the user once the others have ended, then gives it` | Cannot be skipped: a release that shares its batch always needs it |
| 4 | `commands.py:1002-1004` (`order after` on the release) | What the release waits for cannot be changed | `order after: CR-n is the release CR: the CLI keeps what it waits for (every other CR of the batch)` | Cannot |
| 5 | `commands.py:1464-1471` (`_chain`) | The stack leaves the release out: `take stack` does not list it, and the stack driver gets no base for it | none (silent) | Cannot. `stack <crs…>` (`commands.py:2041-2057`) accepts the release's id, but its place changes nothing: see 6 |
| 6 | `commands.py:1481-1485` (`_start_base`), `commands.py:1493-1500` (`_stack_base`), `commands.py:1545-1547` (`handoff`) | The release's start base and PR base are always the default branch; `take` and `handoff` print it, and `ship` records it | `after: … (a release starts from the default branch)` | Cannot. A Driver that opens the PR on another base goes against the base `take` printed (`driver.md:72-74`) |
| 7 | `commands.py:1696-1703` (`handback <release> ready`) | `ready` on a release means released: the CR goes to `3-done` as merged, with no PR check. A release PR that is open and waits for its merge can only be `blocked merge: <pr>` | none | Works, but the release reads as blocked in `status` and the reports |
| 8 | `commands.py:961-967` (`_check_release_open`) | Once the release has started, `order add` is refused for the whole batch | `order add: CR-n has started (…) and ships what was merged before it. Add a fix with `order add --fix-for CR-n`, or put the new work in the next batch` | Add every CR before the release starts |
| 9 | `rails.py:247-269` (`release_go`) | No rail ties an irreversible action to the merge: with an approval or a grant it answers `go` whatever the state of the other CRs. Safe today only because of 1 | none (a gap, not a refusal) | Nothing to do today; the CR must add the rail |
| 10 | `commands.py:2068-2069` (`release start/go/published`), `commands.py:908-912` (`order approve/grant/confirm`) | These work only on the CR of kind `release`. An ordinary CR that does the release's work gets no approval rail | `CR-n is not the batch's release CR`; `order approve names the batch's release CR (none)` | Matters for route B below: keep the tag and the publication in a real release CR |
| 11 | `commands.py:669-673` (`open`, the brief) | `open --mode stack --release N` is accepted, and the brief says the old rule | `(release: starts once every other CR is merged or cancelled, then on the user's confirmation)` | No refusal; the text is what the Foreman reads |

## The cards and the project's rules

| # | Where | What it says today | Without a change |
| --- | --- | --- | --- |
| 12 | `concepts.md:95` | "A release CR and a fix CR sit outside a series and a stack, on the default branch." | Contradicts the shape; every role reads it |
| 13 | `concepts.md:145-147` | A Release driver runs the release "once every other CR of the batch is merged or cancelled … and, when it shares the batch, on the user's `order confirm`" | Same |
| 14 | `concepts.md:9-11`, `driver.md:63-64`, `driver.md:91`, `driver.md:319-320` | "A release PR is no draft: the Foreman merges it"; a Release driver opens its PR ready | On a base that is not the default branch this goes against "ready to merge" |
| 15 | `foreman.md:116-120`, `foreman.md:126` | The Foreman starts the Release driver once the others are merged and the user confirmed; "A release CR and a fix CR are outside" the stack | A Foreman that follows its card will not start it earlier |
| 16 | `driver.md:257-260` | Stack driver: "A release CR and a fix CR are not in the stack." It opens no PR and restacks only what `take stack` prints | The stack driver will not move a release PR |
| 17 | `driver.md:285-287` | A release attempt "starts on the fresh base" (the default branch), `git reset --hard <base>` | A Release driver that follows its card works from the default branch |
| 18 | `chief-of-staff.md:651-665` | "open it preferably alone with `--release 1`"; in a batch "once they have ended it starts only on the user's word"; the version is grilled "from what was merged" | The Chief of Staff's own card |
| 19 | `CONTRIBUTING.md:154-156` (a project rule: it ranks above the cards) | Release, step 1: "From an up-to-date `main` with green CI … on a new branch" | The project's written procedure starts the release branch from `main`, not from a stack. The user's word of 2026-11-12 covers the departure; say it to the user before acting |
| 20 | `CONTRIBUTING.md:173`, `scripts/version.py:107-113` (`just tag`) | The tag is refused unless `origin/main`'s head is the `release: vX.Y.Z` commit | Compatible with the shape if the version PR is the last merge and nothing merges after it. It is also the guard against a tag before the merge |
| 21 | `docs/release-process.md:28-38`, `docs/release-process.md:133-139` | The notes come from `git log vPREVIOUS..HEAD`; N is counted "on `main` before the version commit"; the release joins the batch by `order add --release` | The count is taken on the release branch instead; same number once merged by rebase |
| 22 | `docs/use-cases-foreman.md:111` | "Say "release v1.4.0" once the work is merged and validated." | Docs only |
| 23 | `docs/batch-pace.svg:3`, `:64-66`, `:119-124` | The `<desc>` says the release "runs last, alone"; a frame holds "every CR in here" and the release box is outside it | Docs only |
| 24 | `CONTRIBUTING.md:129-134` | "`full` and both quick campaigns before a release": the campaigns run the plugin from the main checkout | They cannot run on unmerged work. They run before the batch (as done on 2026-11-12), or after the merge of everything under the version PR and before the user merges it |

## Routes for this batch

**A. The CR first, in the same batch (the true shape).** `release-cr-in-batch` is the bottom of
the stack. When the stack is ready, the user merges that one PR; the main checkout is
fast-forwarded and the plugin reloaded (`/reload-plugins`); the release CR is then added
(`order add --release`) and starts on top of what remains. Needs: one merge by the user in the
middle of the batch and a wait for the release PR after it; the new CLI reading a batch opened
by the old one (the specification asks for it); brand-new lifecycle code used for its first real
release. Open question 1 of `02-answers.md` (the confirmation) decides whether the user must
also confirm before the release starts.

**B. No code change: the version PR as an ordinary CR on top, the release CR after the merge.**
Two CRs for one release:

1. An ordinary CR, "version PR for v0.9.0" (steps 1 to 3 of `CONTRIBUTING.md` "Release": the
   release folder, `just release minor`, the commit `release: v0.9.0`, which `driver.md:86-87`
   lets a CR Driver keep). Its `depends.json` names every other CR's slug, so `take` accepts it
   once each is ready or merged (`rails.py:112`, the ordinary rule) and `stack` refuses any order
   that puts it under one of them (`commands.py:2050-2053`). It passes the long gate and a
   Verifier like any CR, and its PR is the draft at the top of the stack.
   - Its start base is the branch of the last open CR of its `after`, in that order
     (`commands.py:1481-1484`), not the top of the stack. So the stack driver stacks the other
     CRs first, then `order after <cr> --note "<ids in stack order, the top one last>"` while the
     CR is still queued (`commands.py:998-1034`), then `take`.
   - `foreman.md:122-124` starts the stack driver "when its open CRs are all ready or blocked":
     this CR is queued then. An `order note` says to stack the others first; the CLI does not
     refuse `take stack` (`commands.py:1612-1624`).
   - A CR added later is not added to its `after` by the CLI (it is not a release): `order
     after` again while it is queued; once it has started, a note and a `take` to redo it.
   - The Chief of Staff writes `report.md` and `conversation.md` into this CR's folder before
     its `take` (the procedure writes them at `order confirm`, which comes too late here).
2. The real release CR, added with `order add --release` at any time. It waits for everything,
   the version PR included. The user merges the stack from the bottom up, the version PR last;
   then `order confirm`, and a Release driver does what is left of the procedure: `just tag`
   and `gh release create`, each after `release go` and the user's approval, then `release
   published`. Its specification says the version PR is merged and names it; `driver.md:323-326`
   already lets a Release driver go on from a release PR the user merged.

The user sees: two CRs for the release; the notes written by a Coder and judged by an Inspector
and a Verifier instead of a Release driver; a confirmation and two approvals after the merge.
All of it runs on paths the CLI and the cards already hold. It is a way around the missing
feature at the level of the plan, so it is said to the user as such before the batch opens.

**C. Today's supported path, no departure.** `order add --release` in the stack batch; the user
merges the whole stack; `order confirm`; the Release driver opens a version PR alone on `main`;
the steering session merges it on the user's approval; tag; publish. This is the shape the user
called an exception.

Advisor's recommendation: **B** when the user cannot be reached during the run (everything is
ready in one pass, the irreversible actions keep their rails, no new code is live), told to the
user in one line when the batch opens. **A** if the user can merge one PR mid-batch and prefers
the feature's first real run on v0.9.0. **C** only if the user refuses both.
