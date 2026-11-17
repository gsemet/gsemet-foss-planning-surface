---
type: cr-answers
description: The user's answers to the grill of driver-checks-before-first-push.
---

# Answers

## Round 1 (2026-11-17)

### batch-Q8: in which batch

The user: the six retro points of batch-23 join the next batch, with the four board CRs of
2026-11-17.

### checks-Q5: the checks before a Driver's first push

The user chose the recommended answer: the Driver's card says to run the pre-PR checks the
project's AGENTS.md names before the first push; chantier's own AGENTS.md names `just check` and
`just eval-dry-run`. Nothing project-specific in the card. The Coder's round prompt also carries
the specification's list of card edits as a checklist.

## Spec questions (2026-11-17, settled by the Chief of Staff from checks-Q5)

- The checklist covers every file edit the specification lists (generic, for projects with no
  cards), not only card edits.
- `coder.md` asks the Coder to mark each checklist item done or open in `r<n>.md`.
- chantier's AGENTS.md owes `just eval-dry-run` for a change under the CLI's `src/` or the
  cards; that it runs on Windows is unproved, named as a known gap.
## Spec questions, round 2 (2026-11-17, settled by the Chief of Staff after the spec critic)

- Before the first push the Driver runs the project's fast gate again at the rebased head, plus
  any extra pre-push check the rules name; `docs/gates.md` and `init.md` say so. No third kind
  of check.
- `just eval-dry-run` is owed for a change under the CLI's `src/` (with `evals/kit/`, as
  today), not for a cards-only change, as the request said ("a CLI-behaviour change"). This
  replaces the earlier settlement.
- eval-dry-run on Windows is proved (CR-317 r5, 17 of 17 on the user's machine); this CR's
  Driver confirms it at its head; a failure is a round, with no exception.