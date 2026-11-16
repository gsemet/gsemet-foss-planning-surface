# Change Specification: a CR with a dependency starts once that dependency is ready, in a stack and in a parallel batch

## Goal

A CR that depends on another starts only once that dependency is ready, and the cards say so.
The user (2026-11-14), on the proposal to start a CR on an unready dependency: "je ne suis pas
d'accord, la dépendance est faite pile pour empêcher de commencer avant que l'autre soit prêt".
The rails are right; the card sentences that say otherwise are rewritten to say what the rails
do.

## Root cause

`skills/chantier/references/concepts.md`, "Words", the batch **modes** paragraph, has two
sentences that say every CR starts at once (line numbers on `main`; +2 once CR-233 and the CRs
under it in batch-17's stack are in):

- **Parallel** (lines 93-95): "every CR starts from the default branch at once and its PR is on
  the default branch;"
- **Stack** (lines 101-102): "every CR starts at once, on the default branch or on its last open
  dependency, and the stack driver puts the PRs each on the previous one"

The CLI does not do that. In
`skills/chantier/scripts/cli/src/chantier/rails.py`, `waits_for` (lines 123-137) counts a
dependency of a CR (not a release) as met only when it is `ready` or `merged`, in every mode, and
`check_take` (lines 198-236) refuses `take` on a queued CR with an unmet dependency:
`"<cr> waits for <ids>: it starts once each is ready or merged"`. So in a stack or a parallel
batch, a CR with an open dependency does not start "at once": it waits for the dependency to be
`ready`. The **Dependencies** paragraph of the same card (lines 160-169) already says it right
("`take` refuses a queued CR until each CR of its `after` is `ready` or `merged` … The CR starts
on the branch of its last dependency still open, in the order of `after`, else on the default
branch, in a stack too"); only the two mode sentences contradict it.

## Decisions carried (02-answers.md)

1. The CR was grilled and specified first, then joins batch-17's stack at its end (one native
   stack at the end; the budget raised to $210 is the batch's, not this CR's).
2. Grilled enough, on the restatement: the rails are right; `concepts.md`'s Stack sentence (~line
   101) is rewritten; `foreman.md` and `driver.md` are checked for the same wording; cards only.
3. The Parallel sentence (~line 94) is rewritten the same way in this CR: a CR with a dependency
   waits until it is ready, in a parallel batch too.

## What changes

Two sentences of one card. No CLI code, no scenario, no test, no agent file (`agents/`,
`com.github.copilot/agents/`), no docs.

### `skills/chantier/references/concepts.md`, the **Parallel** sentence

Replace

> **Parallel** (the default, when the user names none): every CR starts from the default branch
> at once and its PR is on the default branch;

with (the rest, from "the first one ready wins", unchanged):

> **Parallel** (the default, when the user names none): every CR with no open dependency starts
> from the default branch at once and its PR is on the default branch; a CR with a dependency
> starts only once that dependency is `ready` (`take` refuses it until then), on the branch of its
> last dependency still open, else on the default branch (see **Dependencies**), and its PR stays
> a draft on that branch until the dependency merges;

The draft clause is what `driver.md` (lines 389-392, `handback ready <link> draft on <base>:
waits for <cr>`) and `foreman.md` (lines 196-200, the rebase on `order merged`, "in every mode")
already do; it adds no behaviour.

### `skills/chantier/references/concepts.md`, the **Stack** sentence

Replace

> **Stack**: parallel, with a stack driver: every CR starts at once, on the default branch or on
> its last open dependency, and the stack driver puts the PRs each on the previous one

with (the rest of the sentence, from "(`stack` marks the CRs it orders; …", unchanged):

> **Stack**: parallel, with a stack driver: every CR with no open dependency starts at once, on
> the default branch; a CR with a dependency starts only once that dependency is `ready` (`take`
> refuses it until then), on the branch of its last dependency still open, else on the default
> branch (see **Dependencies**), and the stack driver puts the PRs each on the previous one

In both sentences "dependency" is any `after` of the CR: a `depends.json` one, a chain the
Foreman decided, or an `order after` the user's go approved, as **Dependencies** defines it; the
wording needs no more. The **Series** sentence is right already (the next CR starts once the
previous one is `ready`) and does not change.

### `foreman.md` and `driver.md`: checked, no change

The request asks to check them for the same wording. Checked on `main` and on CR-233's branch:

- `foreman.md` says "A queued CR that `status` shows `waits for …` is not yours to start" (line
  130) and handles a dependency that went back to a Driver after the CR started (lines 133-135):
  both agree with the rails. Nothing says a dependent CR starts at once.
- `driver.md` (lines 383-398, the `rebase: <cr> merged` paragraph and the `draft on <base>`
  hand-back) assumes the CR started on its dependency's branch once that one was ready: agrees.
- `chief-of-staff.md` (lines 300-303) already says "the waiting CR starts only once the other is
  ready": agrees.

So the Driver changes neither file; the PR's Test plan records this check (see Evidence).

## On top of batch-17's stack

This CR joins batch-17 at the top of its stack, after the CRs now in it. CR-233 (merge-any-time)
edits `concepts.md` in two places near these: **Ready to merge** (lines 9-16) and, in the
**Stack** sentence's continuation, "the user merges it in one action from the top PR" becomes
"… from the top PR, or one PR at a time from the bottom" (lines 106-107 on its branch). This CR
leaves both as CR-233 writes them and edits only the Parallel sentence's opening and the Stack
sentence's opening ("every CR starts at once, on the default branch or on its last open
dependency"), which no branch of batch-17 changes. CR-233's other card edits
(`chief-of-staff.md`, `foreman.md`, `driver.md`) are untouched. The Driver applies the
replacements above to the text as it stands at its start base; the line numbers move, the
sentences do not.

## Out of scope

- Any change to the rails or the CLI's texts (`waits_for`, `check_take`): they are right.
- The **Series** sentence: already right.
- The docs, README and SVGs; the eval kit.

## Evidence

- `just check` passes (Linux, macOS, Windows in CI).
- `just scenario` passes (AGENTS.md: a change to the cards passes it before its PR).
- A reading pass, recorded in the PR's Test plan:
  - `rg -n "last open dependency|every CR starts" skills/chantier/references` finds nothing;
  - the new **Parallel** and **Stack** sentences and **Dependencies** say the same: a dependent
    CR starts once its dependency is `ready`, on the branch of its last dependency still open,
    else on the default branch;
  - `foreman.md` and `driver.md` checked, no contradicting wording (named in the Test plan).
