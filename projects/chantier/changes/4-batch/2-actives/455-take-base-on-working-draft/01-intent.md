# Intent

Split, 2026-11-20, by the Chief of Staff out of `take-base-from-forge` (its answer Q5). Priority
P3. Written 2026-11-21 by the spec writer from `intake/request.md` and the archived answers; no
grill was held (the user delegated the night's spec questions to an advisor: "plus de question").

## The rule today

In a stack batch, `take` starts a new CR (no open dependency, neither a fix nor a release) on the
nearest earlier CR of the batch that has a PR, whatever that CR's status (`working`, `blocked`,
`ready`) and its PR's draft state, else on the default branch, recorded on the CR as `start_on` at
its first take. It leaves out a CR whose PR the forge shows merged (a `merged@1` line of the
journal). Sources:

- The user's answer stack-Q4, 2026-11-17 (`5-archives/261117-2134-333-take-base-nearest-pr/02-answers.md`):
  "`take` bases a CR on the nearest earlier CR of the batch that already has a PR, else on main;
  one stack-driver run, at the batch's end, owns the final order of the stack (one linear stack on
  the forge)". Its goal: no tree of PRs, no branch with no PR as a base (batch-23's restacks).
- `take-base-from-forge`'s answer Q5, settled by the Chief of Staff on 2026-11-20
  (`5-archives/261121-0330-422-take-base-from-forge/02-answers.md`): CR-429's case leaves the rule
  unchanged, "the nearest earlier CR with a PR, whatever its status and draft state"; changing it
  is a new decision for the user, filed apart: this CR.

## What happened

Studio's batch-06: CR-429 was given the branch of CR-424, a working CR with an open draft PR and
several rounds still to come (the takeover of an external PR). The Foreman's take note sent CR-429
to `origin/main` instead, and the batch's retro counts the printed base as wrong.

## The decision asked

Keep the rule as it is; or start a new CR on another CR's branch only when that CR is handed back
ready, else on the default branch; or let the Foreman name the base at the take. Open as
take-draft-Q1 in `03-change-spec.md`.
