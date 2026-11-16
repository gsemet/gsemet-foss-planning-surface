# Eval kit: an end-to-end dry run as evidence

## The request

From the retro of batch-13 (2026-11-12): four blockers of the `full` campaign (the audit counted
the merged release PR as a stray merge, the reset's verify failed on `refs/pull/*`, a raw
`gh pr merge` the host may refuse, `uv.lock` missing from the release CRs) were found by an
independent review after CR-189 reproducible-evals merged, not by its Inspector or its Verifier.
Each of them judged one piece alone (the judge, the setup, the audit), and no one ran the pieces
together as a campaign does.

## What changes

- The eval kit (`evals/kit/`) gets a dry run of a campaign, end to end, that writes nothing to
  the real sandbox (https://github.com/gsemet/chantier-eval-sandbox) and spends no model call:
  a workspace set up as `setup.py` does, against a local bare repository standing for the
  sandbox's origin; a staged run that plays what a campaign leaves behind (the CRs' merged PRs,
  the release PR, its tag); then `audit.py --sandbox` and the judge on that result. It passes
  on a run that follows the rules and fails, naming the criterion, on a planted fault (at least
  the four of batch-13).
- The project's rules say that a change to the eval kit carries this dry run's output, at the
  pushed head, as its Verifier's evidence (CONTRIBUTING.md or `evals/README.md`, where the kit's
  rules live).
- `just check` runs the dry run (it must stay fast and portable: Linux, macOS, Windows).

## Out of scope

- A new review role or a mandatory second-model review before every merge: the retro's "the
  independent review runs before the merge" is kept as one line of guidance for eval-kit
  changes, not as a mechanism (the Chief of Staff's decision, below).
- Any write to the real sandbox, any paid campaign.
