# Change Specification: batch-17 retro, card fixes

## Goal

The batch-17 retro (`5-archives/batches/batch-17.md`, "Retro") found nine slips that a card's text
can prevent. The user filed them as one CR on 2026-11-14 (ID-Q1, A): drafts 1, 2, 8, 9, 11, 12, 13,
14 and 15 of `.agents/changes/batch-17-issue-drafts.md`. Each point below says what happened, the
rule that prevents it, and where that rule goes. Card and doc text only: no CLI code, no hook, no
type, no test logic.

There is no `01-intent.md` or `02-answers.md`: the decisions are the nine points of
`intake/request.md`, which this specification carries one by one (table below). This CR has no
`issue:` line.

## Decisions carried (`intake/request.md`)

| # | Point (draft) | Where in this spec |
| --- | --- | --- |
| 1 | Drivers and conflict resolvers run every git command as `git -C <worktree>`; the main checkout is read-only except the post-merge fast-forward | Area 1 |
| 2 | The stack driver plans one restack pass right after each native stack merge, the siblings pushed at once | Area 2 |
| 8 | Tests and smoke runs of the board's write paths use a scratch planning folder, never the live record | Area 3 |
| 9 | `.git/info/exclude` is out of bounds for a Driver | Area 4 |
| 11 | The Inspector reviews the round's last commit | Area 5 |
| 12 | The Foreman's Driver brief always carries the Foreman's address | Area 6 |
| 13 | The spec critic flags a spec that bundles a refactor with a lint or type cleanup, or several views, and the grill splits it | Area 7 |
| 14 | The `stack-ready-to-merge` line carries each CR's open gaps; the Chief of Staff applies the gap and pane-screenshot rule to it before it offers the stack for merge | Area 8 |
| 15 | The Chief of Staff runs `asks --read A-<k>` in the turn it relays an ask or orders on it | Area 9 |

The other drafts (3 to 7, 10) need CLI code or are covered elsewhere: out of scope.

## What changes

All cards are under `skills/chantier/references/` and are read by both hosts: one edit serves
Claude Code and Copilot. The agent files (`agents/*.md`, `com.github.copilot/agents/*.agent.md`)
hold no contract and are **not touched**; if a Driver finds one that must change, it changes both
hosts' files together and keeps their bodies identical (`AGENTS.md`). Line numbers below are those
of `main` at `ce00ec3`, to find the place; the section names are the reference.

### Area 1: git only in the worktree (draft 1)

Evidence: CR-245's Driver ran a rebase in the main checkout instead of its worktree (aborted at
once).

`driver.md`, "Your means", the worktree bullet (lines 102-107) and the rebase bullet (108-113): add
one bullet, before the worktree bullet, that says:

- Every git command a Driver runs names its worktree: `git -C <worktree> <command>` (the CR's
  worktree as `take`/`handoff` printed it; for the stack driver, the worktree of the CR it moves;
  for the QA and Release drivers, their own worktree). A bare `git <command>` relies on the shell's
  current folder, which the host may reset between calls (the host's reference says so for Claude
  Code), and lands in the main checkout.
- The main checkout is read-only for a Driver: its branch, index and files never change by a
  Driver's command (no `checkout`, `switch`, `rebase`, `merge`, `reset`, `commit`, `stash`, `pull`
  there). The two commands that name it are the worktree's creation, `git -C <main checkout> fetch
  <remote> <default branch>` and `git -C <main checkout> worktree add …` (with a planning surface,
  `git -C <clone>`, as today), which change neither its branch nor its files. The one move of the
  main checkout is the steering session's post-merge fast-forward ([concepts](https://github.com/gsemet/chantier/blob/main/skills/chantier/references/concepts.md), rule 8;
  `foreman.md`, "The main checkout after a merge"), never a Driver's.
- A git command run in the wrong place by mistake: stop, undo only what is safe to undo
  (`git -C <main checkout> rebase --abort`, `merge --abort`), and `note` it; anything else left in
  the main checkout goes to the steering session as it is, by an `anomaly` (stack driver) or a
  `blocked question:` hand-back, never cleaned by force.

Update the command examples of `driver.md` that show a bare `git` in a worktree context to the
`git -C <worktree>` form where the place matters: the rebase bullet (`git -C <worktree> fetch`,
`git -C <worktree> rebase <base>`), the Push bullet (both forms; the `-C` forms already have allow
rules, `hosts/claude-code.md`, "Allow rules"), the CR driver's commit (`git -C <worktree> add --
<paths>`), the stack driver's "Removing a dropped CR" `rebase --onto` lines and "A conflict that
needs code" (`git -C <worktree> rebase --abort`). The forge commands (`gh`, `glab`) are unchanged.

`worker.md`, "Conflict resolver" (lines 158-167): add one sentence: every git command it runs is
`git -C <worktree>` (the worktree of its prompt's `writes:` line); it never runs git in the main
checkout.

### Area 2: one restack pass after a native stack merge (draft 2)

Evidence: GitHub's native stack merge rewrote the branches above the merged PR, so every child
needed a restack and fresh CI.

`driver.md`, "Stack driver", the paragraph that starts "The stack is what your prompt gives" and
its "After a partial merge" text (lines 569-586), and "A merge during a take" (547-550): the
restack after a merge becomes one planned pass, in this order, stated as such:

1. `git -C <main checkout or clone> fetch <remote>` once, then `$CHANTIER stack` once (the old
   heads), before any rebase. The forge may have rewritten the remote branches above the merged PR
   (GitHub's native stack merge did in batch-17): the local branches stay the source of each CR's
   commits, and a `--force-with-lease` push after this fetch replaces the forge's rewrite.
2. Rebase every remaining CR with no live Driver, bottom up, each on the one under it (the first on
   `origin/<default branch>`), all before any push. A conflict goes the usual way
   (`conflict-resolver`, or "A conflict that needs code").
3. Push every moved branch right after the last rebase, back to back, one command per branch
   (never a loop or a script), so the forge starts every PR's CI at once; then `ship` each one.
4. One CI wait for all of them (heavy CI at the top, as today), the proofs each move touched
   judged again (as today), then one `$CHANTIER forge-stack rebuild`, read back.

The text says that pushing a branch and waiting for its CI before rebasing the next one is what
this pass avoids. The rest stays: the restack is silent (no `stack-ready-to-merge` follows), a
working CR's branch is its Driver's (`rebase:` note from the Foreman), and the Foreman's side is
unchanged (`foreman.md` already sends `note merged:` or `take stack` at once on a merge).

The claim "a lease push after the fetch replaces the forge's rewrite" is marked **unproved; trial:
the next native stack merge on GitHub, the restack's pushes accepted and `forge-stack show` exit
0**.

### Area 3: board write paths tested on a scratch planning folder (draft 8)

Evidence: CR-226's smoke test wrote a self-nesting tree inside the live planning record
(`.agents/changes`).

`worker.md`, "Coder" and "Verifier" (and "Debugger", which probes): one sentence each, or one shared
sentence in the card's preamble that all three read: a test, a smoke run or a probe of the board's
write paths (`chantier board`'s edits of the backlog, and the role-free CLI commands it calls)
points at a scratch planning folder (a fresh temporary folder, or one under the worktree's test
fixtures), never at the project's live planning folder (`.agents/changes/`, or the planning
surface's), and removes it at its end.

`driver.md`, "CR driver": one sentence: a CR that touches the board's write paths carries that rule
in each Coder's and Verifier's brief, and the evidence plan names the scratch folder its runs use.

### Area 4: `.git/info/exclude` out of bounds (draft 9)

Evidence: CR-248's Driver wrote to the repository's `.git/info/exclude`, outside both the planning
folder and its worktree.

`driver.md`, "Your means", next to the `writes:` sentence (lines 31-36): a Driver and its workers
write nothing in the repository's git folder (`.git/info/exclude` named, and `.git/config`,
`.git/hooks`), by any tool or shell command; git's own commands write there as git does. A file to
ignore is ignored by the worktree's own files (a `.gitignore` change goes through a `coder`, in a
round, as any project file) or not at all; a file that should not be committed is simply not
staged (staging is by name already).

### Area 5: the Inspector reviews the round's commit (draft 11)

Evidence: CR-228's round-4 Inspector approved at 073cfc5, then the round's commit 6860065 was
pushed, so only the Verifier saw the final head.

**AMENDED (2026-11-14, `02-answers.md` point 1; this replaces everything else in this Area).** The
order stays as the diagrams say: `coder`, `pr-body.md`, `inspector` on the uncommitted diff, then
the commit. What is added is a check that the commit holds exactly what was reviewed. `driver.md`,
"CR driver", the round paragraph and the "Every APPROVE is recorded at once" paragraph: before the
round's commit, `git -C <worktree> status --porcelain` and `git -C <worktree> diff` (or `diff
--stat`) show nothing changed since the review (the files the Inspector reviewed, same contents; a
file touched after the review means a new `inspector` on the new state before the commit); stage by
name, commit, then check `git -C <worktree> diff --stat <commit> -- <paths>` is empty against the
reviewed state and the tree is clean; the note stays `r<n> approved at <head>, committed as <sha>`.
The Inspector's card, the Verifier's Review-box paragraph, and the docs texts and SVGs are **not
changed** (drop every bullet of this Area below, except the `git -C` forms that Area 1 already
gives).

Superseded text, kept for the record only:

Today a round is: `coder`, `pr-body.md`, `inspector` on the uncommitted diff, then the commit, with
the note `r<n> approved at <head>, committed as <sha>`. It becomes: `coder`, then the round's commit,
then `pr-body.md`, then `inspector` on the committed head, so the `head` of the approval is the
commit that is pushed.

- `driver.md`, "CR driver", the round paragraph (lines 371-396): after the `coder`, commit the
  round (files by name, `git -C <worktree> add -- <paths>`, a message as "Commits" says), check the
  tree is clean, then write or update `pr-body.md`, then the `inspector` on the branch against the
  base at that commit and `pr-body.md`, then each review step of `Team:`. `APPROVE`: record `note
  <cr> "r<n> inspector approved at <head from the JSON>"`; the head must be the worktree's head
  (`git -C <worktree> rev-parse HEAD`): another head, or a dirty tree, is a reply that covers
  nothing, and a new `inspector` runs at the head. `FIX-REQUIRED` on the code: the next round's
  commit is added on top (or folded into the round's commit before the branch's first push, by the
  "Commits" fold rule, then inspected again at the folded head). Any commit after an approval and
  before the push, other than a move (rebase, restack, conflict resolution, which keep their own
  rule), needs a new `inspector` at the new head before the push. The body-only re-inspection stays
  as it is (the body is not committed).
- `driver.md`, the "Every `APPROVE` is recorded at once" paragraph (lines 426-438): drop the
  `committed as <sha>` note and the sentence that the Inspector's head predates the commit; the
  Review box cites the approval's `head`, which is the reviewed commit.
- `driver.md`, the dirty-worktree rule after a failed coder (lines 360-368) stays: a failed coder's
  leftovers are never committed as the round's commit before a new coder deals with them.
- `worker.md`, "Inspector" (lines 47-61): review the round's commit (the worktree's head against
  its base); the tree is clean at the review; `head` is that commit; a dirty tree is
  `FIX-REQUIRED` with one blocking item saying the round is not committed. The move review is
  unchanged.
- `worker.md`, "Verifier", the Review box paragraph (lines 131-137): the note that proves the box
  is the approval whose `head` is the SHA the box cites (or the move's head, or `carried from`);
  drop "the round's `committed as <sha>`".
- `docs/how-chantier-works-texts.md`, `docs/how-chantier-works-simple-direct-texts.md`,
  `docs/how-chantier-works-simple-foreman-texts.md` and the three matching SVGs
  (`docs/how-chantier-works.svg`, `docs/how-chantier-works-simple-direct.svg`,
  `docs/how-chantier-works-simple-foreman.svg`): the phrase "Inspector, which reads the diff before
  the commit" becomes "Inspector, which reads the round's commit", in the text files and in the
  SVGs' text alike (the SVG's layout unchanged; the line must still fit its box).

### Area 6: the Driver brief carries the steering session's address (draft 12)

Evidence: CR-252's Driver's first message to the Foreman was lost because its brief gave no
Foreman address.

- `concepts.md`, "Starting an agent", the prompt template (lines 336-348): a Driver's prompt (CR,
  stack, release, QA driver) gets one line, `Steering: <who steers> <how to reach it>`, with the
  steering session (the Foreman, or the Chief of Staff in direct mode) and the means of the host's
  reference row "A Driver messages its steering session", written out: on Claude Code `SendMessage
  to main` and, for the record, the steering session's id (`$CLAUDE_CODE_SESSION_ID`); on Copilot
  "your final answer", as its reference says. Workers get no such line (they answer their Driver).
- `foreman.md`, "Your means", the `take` bullet (line 121, next to the `writes:` sentence): every
  Driver's prompt the Foreman writes holds that `Steering:` line, for each start and restart,
  whatever the Driver kind.
- `chief-of-staff.md`, "Steering a batch yourself": the same line in a Driver's prompt in direct
  mode (one sentence pointing to the template).
- `driver.md`, the card's opening paragraph: a Driver sends every line to the steering session by
  the `Steering:` line of its prompt; a prompt without it is a `Needs:`-like gap: `note` it and use
  the host's reference row.

Sending to the session id instead of `main` is not introduced: the session id is in the line for
the record only (from a Driver to its own parent session by id is unproved).

### Area 7: the spec critic flags a bundle (draft 13)

Evidence: CR-221 ($23.27, 6 rounds) bundled inline dependencies with a ruff/mypy cleanup; CR-225
($21.77, 4 rounds) bundled several board views; the median CR cost about $4.

- `spec-critic.md`, "What you look for": "Only these three" becomes four, adding:
  4. **A bundle:** the specification joins work that would ship more cheaply as separate CRs: a
     refactor or a feature together with a lint, format or type cleanup across files the change does
     not otherwise need; or several views, screens or commands that each deliver alone. Name the
     parts and the cut.
  A bundle always touches behaviour (scope): its draft question offers the split first (the parts
  named), then keeping it whole.
- `spec-critic.md`, "Reply": the kinds become intent, inconsistency, claim or bundle.
- `chief-of-staff.md`, "The spec critic" (lines 368-372): the summary of what it looks for names the
  bundle; step 3 says a bundle finding is always a question for the user, the split recommended. On
  the user's split: the parts split off are filed as new inbox items (`$CHANTIER file`, one per
  part, the raw request naming the CR they come from), the answer is recorded in `02-answers.md`,
  and the spec-writer's next run narrows the specification to what stays. The Griller follows the
  same steps (`griller.md` already points to "Backlog and grill"; no change there).

### Area 8: the stack's merge line carries each CR's gaps (draft 14)

Evidence: PR #197 (CR-248) changed what the board pane draws and merged as the bottom of stack
#200 with its Known gap "no screenshot of the pane from a real session" still open. Today only the
complete `stack-ready-to-merge` carries gaps; the partial one does not.

- `foreman.md`, the stack hand-back bullets (lines 207-211): the partial ask also carries each
  mergeable CR's gaps after its link: `stack-ready-to-merge <stack link> partial stack mergeable
  below <sha7> <cr>=<link> gaps: …… to come: …`, from the `gaps:` note recorded at its hand-back
  (lines 233-235; `none` gives no `gaps:` text). Lines 233-235 drop "in the complete" so the gaps
  are quoted in both forms. The ask's format list (line 262) shows `<cr>=<link>[ gaps: …]…`.
- `chief-of-staff.md`, the stack batch bullet (lines 952-968): on any `stack-ready-to-merge` ask,
  partial or complete, before telling the user the stack is mergeable, apply the plain ask's gap
  rule (lines 930-938) to each CR of the mergeable part: quote its gaps next to its link, in the
  user's language; where the project's rules ask for a screenshot of the board pane and a gap names
  it as missing, ask the user for that screenshot in the same message, naming the PR, before the
  sentence that says the stack can be merged, and say which PRs are below and above it. The
  evidence route stays (`order note <cr> --note "evidence: <path>"`). Lines 966-968 ("its gaps are
  quoted with the complete `stack-ready-to-merge`") follow.
- `status-layout.md`: no change unless it describes the partial-stack line's gaps differently; if
  so, align it.

Whether an open pane-screenshot gap holds the offer of the stack is the open question below; this
specification writes the default "quote, ask, the user decides", which is today's rule for a plain
`ready-to-merge`.

### Area 9: asks marked read as the Chief of Staff acts (draft 15)

Evidence: 45 asks were left unread, so CR-228's blocked ask (A-44) looked like the rest and was
found through `status`.

`chief-of-staff.md`, "Asks" (lines 1058-1060): `asks --read A-<k>` runs in the same turn the Chief
of Staff relays that ask to the user or acts on it (an `order`, an answer to the Foreman), not
later; `--read all` only after every unread ask listed has been relayed or acted on, never to clear
the list. An ask that waits for the user stays unread until the user has heard it. At each report,
`$CHANTIER asks` lists what is still unread: each one is relayed or acted on in that turn.

## Out of scope

- Any CLI, hook, type or test logic change; drafts 3, 4, 5, 6, 7 and 10 of the drafts file.
- The agent files of both hosts (not touched, see "What changes").
- `hosts/claude-code.md` and `hosts/copilot.md`: no row changes (the `-C` push rules exist; the
  steering means is unchanged).
- The project points of the retro (stale screenshots, release notes, `batch-pace.svg`).
- Other workers' git (Coder, Debugger, Verifier, Investigator): Area 1 names the Drivers and the
  conflict resolver, as the request does.

## Evidence

- `just check` passes (Linux, macOS, Windows in CI), including the docs and structure tests.
- `just scenario` passes: a change to the cards (`AGENTS.md`).
- `just mod`: not due (no `hooks/` or `types/` change).
- A Grep on `skills/chantier/references/` after the change shows: no `committed as` left; no
  "reads the diff before the commit" in `docs/`; `git -C <worktree>` in the Conflict resolver
  section; `.git/info/exclude` in `driver.md`; `Steering:` in the `concepts.md` template and in
  `foreman.md`; "bundle" in `spec-critic.md` and `chief-of-staff.md`; the partial
  `stack-ready-to-merge` form with `gaps:` in `foreman.md`; `asks --read A-<k>` with "same turn" in
  `chief-of-staff.md`.
- The three SVGs render (open each; the changed phrase fits its box): one screenshot each, before
  and after, in the PR's Deliverables.
- No agent file changed (`git diff --name-only` shows none under `agents/` or
  `com.github.copilot/agents/`); if one did, both hosts' bodies are identical (the structure test).

## Open questions for the user

1. **Area 5, the diagrams:** the docs diagrams (the target) say the Inspector "reads the diff
   before the commit". Draft 11 inverts it: commit first, then the Inspector at that commit. This
   specification updates the diagrams' text with it. Confirm, or keep the review before the commit
   and only check that the commit holds exactly what was reviewed (no diagram change, a weaker
   proof)?
2. **Area 8, hold or quote:** a CR in the mergeable part whose gap names the missing pane
   screenshot: (A, written) quote it and ask for the screenshot, the user decides to merge or not;
   (B) the Chief of Staff offers the stack mergeable only below that PR until the screenshot lands;
   (C) the stack driver keeps that PR a draft until the evidence is attached.
3. **Area 3, breadth:** the rule names the board's write paths, as the request does. Widen it to
   every test or smoke run of a CLI command that writes a planning folder (`file`, `triage`,
   `summary set`…)?
4. **Area 7, without a critic:** the critic runs only on a CR judged impactful. Should the grill's
   restatement also name a bundle when no critic runs, or is the critic the only check?
