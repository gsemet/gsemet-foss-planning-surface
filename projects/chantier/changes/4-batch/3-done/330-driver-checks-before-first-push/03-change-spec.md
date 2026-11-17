---
type: change-spec
description: Before its first push a Driver runs the fast gate again at the rebased head, plus any pre-push check the rules name, and the Coder's prompt carries the specification's file edits as a checklist the Coder marks.
---

# Change Specification: the fast gate again, and the rules' pre-push checks, before a Driver's first push; the specification's file edits as the Coder's checklist

Origin: verbal, the retro of batch-23 (`intake/request.md`;
`projects/chantier/changes/5-archives/batches/batch-23.md`, Retro). No issue.

## Goal

In batch-23, CR-317 ran six rounds. Two of its failures were found only after the first push,
each one costing a round:

- `just eval-dry-run` went red in CI, because the dry run paused a batch that now pauses itself.
- The Verifier found that the card edits the specification asked for were missing.

The CR's rebase onto CR-316 also pushed `rails.py` over the 400-line test of `just check`, but
that failure was found locally, before the first push.

Two things change so that such failures are caught before the first push:

1. Before the CR's first push, the Driver runs the project's fast gate again at the rebased head,
   plus any extra pre-push check the project's rules name. The card names no command: the
   project says which. chantier's own `AGENTS.md` names `just check` and, for a change to the
   CLI's code, `just eval-dry-run`.
2. The Coder's prompt carries, as a checklist, the list of file edits the specification gives,
   card edits included. The Coder marks each item done or open, so the Driver sees what is left.

## Decisions carried from `02-answers.md`

- batch-Q8: the six retro points of batch-23 join the next batch, with the four board CRs of
  2026-11-17. This CR is one of those six.
- checks-Q5 (the recommended answer): the Driver's card says to run the pre-PR checks the
  project's `AGENTS.md` names before the first push; chantier's own `AGENTS.md` names `just check`
  and `just eval-dry-run`. Nothing project-specific in the card. The Coder's round prompt also
  carries the specification's list of card edits as a checklist.
- Spec questions, round 1 (the two that still hold; round 2 replaced the third):
  - The checklist covers every file edit the specification lists (generic, for projects with no
    cards), not only card edits.
  - `coder.md` asks the Coder to mark each checklist item done or open in `r<n>.md`.
- Spec questions, round 2 (after the spec critic):
  - The checks before the first push are the project's fast gate, run again at the rebased head,
    plus any extra pre-push check the rules name. `docs/gates.md` and `init.md` say so. There is
    no third kind of check: the long gate stays as it is, run through `gate`.
  - `just eval-dry-run` is owed for a change under the CLI's `src/`, alongside `evals/kit/` as
    today, and not for a cards-only change. This replaces the round-1 settlement.
  - `just eval-dry-run` is proved on Windows: CR-317 r5 passed 17 of 17 on the user's machine
    (`5-archives/261117-1351-317-auto-pause-last-merge/work/coder/r5.md`). This CR's Driver
    confirms it at its own head. A failure is a round, with no exception.
- From the spec critic, carried with the round-2 settlements:
  - The checklist goes in the Coder's prompt only. The `--note` of `$CHANTIER round` stays the
    one-line brief: `driver.py` logs it as the round's step line.
  - The marks in `r<n>.md` are for the Driver, which reads that file. The Inspector does not read
    it: `inspector.md` never reads `r<n>.md`.

## What changes

### 1. The Driver's card (`skills/chantier/references/driver.md`)

**The checks before the first push.** In "Your means", next to the long-gate bullet (the one that
begins "The long gate, the project's command, before the first push and the PR"), add one bullet
with this content. The Coder chooses the wording, in the card's style:

- **Before the first push:** run the project's fast gate again, in the worktree, at the rebased
  committed head you are about to push, together with any extra pre-push check the project's
  rules name (`$CHANTIER rules`) for the kind of change the CR is.
  - The Coder already ran the fast gate during the round, but on the round's base: the rebase
    may have changed what it checks.
  - These are short gates. You run them yourself, one command per call, never through `gate`, as
    the card already says of short gates.
  - A failure is a round: a `coder` with the failing lines in its prompt, then the reviews, then
    these checks again at the new head before the push.
  - Record the result with `$CHANTIER note <cr> "before first push at <sha7>: <command>: pass"`,
    one note per command, or one note that names each command.
  - If the project's rules name no fast gate and no pre-push check, there is nothing to run and no
    note to write.
- The step holds whichever way the first push happens:
  - when the long gate runs through `gate`, these checks come before that run;
  - when the long gate is a pipeline job (the case "run no `gate`: push and open the PR after the
    approved round", which is chantier's own), they come before the push;
  - with the `ci: beside the long gate` line, they come before the push.

  It is not a third gate and does not change the long gate, which stays as it is.
- The new text names no project command: no `just`, no `eval-dry-run`.

Also update the one-line sequence in "CR driver" so that this step appears after the rebase and
before the long gate and the push. That is the line "record `note ...`, rebase, the long gate (a
failure is a round), push, the PR, `ship`, CI ...", together with its `ci: beside the long gate`
variant.

**The specification's file edits as a checklist in the Coder's prompt.** The card says what a
Coder's brief holds in two places:

- the "Whole, or by part" reading rule near the top: "The detail of 'What changes' is the Coder's
  and the Inspector's to read ... Read that detail when a brief or a judgment needs it";
- the round step: "Each round: a `coder` with the brief".

Add there:

- The Driver reads the list of file edits the specification gives (in "What changes", each file
  it names with the change to make there, card edits included). It copies that list into each
  Coder's prompt as a checklist, one line per edit: the file and the change.
- The checklist goes in the prompt only. The `--note` of `$CHANTIER round` stays the one-line
  brief, which the CLI logs as the round's step line.
- From round 2 on, the prompt carries only the items that the previous rounds' `r<n>.md` mark
  open or leave unmarked, plus the items a review sent back.
- A specification that names no file gives no checklist.
- The Inspector and the Verifier keep reading the specification themselves, as they do today.

### 2. The Coder's card (`skills/chantier/references/coder.md`)

In "Your part", whose output today is "`r<n>.md`: what changed, the gates run with their results,
open points, a hand-over note for the next round", add one rule: when the prompt carries a
checklist, `r<n>.md` marks each of its items `done` or `open: <why>`, so the Driver sees what is
left. The reply template, its ten-line cap and its format checks stay unchanged. The checklist
goes in `r<n>.md` only, never in the reply.

### 3. The gates' docs (`docs/gates.md`) and the init tour (`skills/chantier/references/init.md`)

- `docs/gates.md`: in the fast gate's bullet ("what the Coder runs after every round, and the
  Inspector may run to check a claim"), add that the Driver also runs it once more before the
  CR's first push, at the rebased head. Add that the project may also name an extra pre-push
  check in its `AGENTS.md`, which runs at the same time and the same way (one command per item,
  never through `chantier gate`). Give one example line in the declaration block, for example
  "- Before the first push, for a change under `src/`: `<cmd>`.". Keep the two gates as the two
  kinds of check.
- `init.md`, step 5 "Getting started here" (the sentence "Check the two gates in particular:
  whether the project's rules declare a fast gate (run after every round) and a long gate ..."):
  say that the fast gate also runs before the first push, and that an extra pre-push check may be
  declared. Offer the exact line only when the project has a check that is too slow for every
  round and too important to leave to CI.

### 4. chantier's own rules (`AGENTS.md`, repository root)

Today the first bullet reads "Run `just check` before you hand back; it must pass on Linux, macOS
and Windows." Change it, or add one bullet beside it, so that it says, in the file's style:

- Before a CR's first push, its Driver runs `just check` in the worktree, at the rebased head it
  pushes.
- For a change under the CLI's `src/` (`skills/chantier/scripts/cli/src/`) or the eval kit
  (`evals/kit/`), the Driver also runs `just eval-dry-run` there, before that first push. A
  cards-only change does not owe it.

Keep "before you hand back" and the "Linux, macOS and Windows" requirement as they are. CI covers
the systems the local machine does not run.

### 5. `CONTRIBUTING.md` ("Daily work")

Keep the `just check` line ("run before any PR") and the eval-kit bullet ("A change to the eval
kit (`evals/kit/`) runs `just eval-dry-run`"). Add, matching `AGENTS.md`, that a change under the
CLI's `src/` also runs `just eval-dry-run` before its first push.

### Not touched

- The CLI (`skills/chantier/scripts/cli/`): no new command and no new refusal. `round --note`,
  `ship` and `handback ready` behave as today.
- The long gate and `gate`: unchanged.
- The Inspector's and the Verifier's cards: unchanged.
- The agent files (`agents/`, `com.github.copilot/agents/`): unchanged, so the two hosts stay
  identical.

## Out of scope

- Running these checks before later pushes (after a rebase, a restack, or a new round on an
  existing PR): the decision names the first push only.
- Any project-specific command in a card.
- The other five retro points of batch-23, each of which is its own CR.
- Making the CLI check that the checks ran.

## Evidence

- `just check` passes at the PR's head. The long gate is the pipeline's `just scenario
  (ubuntu-latest)` job, as `AGENTS.md` says; this CR changes the cards, so it passes that job
  before its PR.
- The Verifier runs these read checks at the head:
  - `driver.md` has the bullet for the checks before the first push (the fast gate again at the
    rebased head, plus the rules' pre-push checks, never through `gate`). The "CR driver"
    sequence places it after the rebase and before the long gate and the push.
    `rg -n "just |eval-dry-run" skills/chantier/references/driver.md` finds no project command in
    the new text.
  - `driver.md` puts the specification's file edits as a checklist in the Coder's prompt, not in
    `--note`, and carries the items still open to the next round.
  - `coder.md` asks for each checklist item to be marked `done` or `open: <why>` in `r<n>.md`,
    and its reply template is unchanged.
  - `docs/gates.md` and `init.md` say that the fast gate runs again before the first push and
    that a project may name an extra pre-push check. Neither names a third gate.
  - `AGENTS.md` names `just check` before the first push, and `just eval-dry-run` for a change
    under the CLI's `src/` or `evals/kit/` and not for a cards-only change. `CONTRIBUTING.md`
    agrees.
- This CR's own Driver applies the new rule to the CR itself (dogfooding):
  - Before its first push, it runs `just check` at the rebased head and records the note.
  - It also runs `just eval-dry-run` at its head on the user's Windows machine, to confirm the
    proof from CR-317 r5 (17 of 17), even though this CR touches no CLI `src/` and so does not owe
    it. A failure is a round, with no exception.
- Known gap in the PR, quoted in the ready line: the rule is not yet tested in a real batch (a
  trial). In the next batch, a Driver of a CR under the CLI's `src/` should run `just check` and
  `just eval-dry-run` before its first push, its log should show the note, and a red result
  should be a round before the push, not after CI.
