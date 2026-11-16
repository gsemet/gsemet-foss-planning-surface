# Reproducible eval campaigns on the sandbox

Second of two CRs (the user, 2026-11-12: "fais 1 puis 2"); it starts once `eval-sandbox-app`
has built the sandbox project and its reset. Its answers are in `02-answers.md` (2026-11-12).
After both: real-direct runs on the sandbox, then the release v0.9.0 (`release-v0-9-0`, in the
inbox, untouched here).

## The problem

The real campaigns (real-foreman, real-direct) take fresh inbox items on this repository and its
`main` of the day: two runs never measure the same thing, and their PRs are gone the next day.
Only the variable under test (the plugin) should change from one run to the next.

## What changes (option A, agreed by the user, ruled by the answers)

1. **A frozen project.** The campaigns run on the sandbox https://github.com/gsemet/chantier-eval-sandbox
   that `eval-sandbox-app` built: real `gh`, real GitHub Actions CI, the same start every time.
   Before each run the kit's reset command (from `eval-sandbox-app`) puts the sandbox back at the
   recorded initial SHA-1: `main` reset, open PRs closed, branches, tags and releases deleted.
   That command is the only force push, clearly named; no ad-hoc force push anywhere.
2. **Frozen CRs.** A set of already-specified CRs for the sandbox in the eval kit (request,
   intent, answers, specification for each), no grill to replay. Real coding, not long; their
   CI fast.
3. **A judge of the result.** Hidden tests per CR, kept in the kit and never pushed to the
   sandbox, run on each PR's head, so the audit says whether the work is right, not only
   whether the rails held.
4. **Comparable reports.** The report names the chantier version (and commit), the sandbox's base
   SHA-1, the campaign, the mode and the models: two reports compare line by line, costs
   included.
5. **Told-apart PRs.** Merged PRs may stay on the sandbox; every PR title a run opens carries the
   run's number, its date and the campaign type, so each run's PRs are told apart.
6. Dogfooding on this repository stays normal work, not an eval. `claude-planted` is unchanged
   (its fixture and local forge are already reproducible).

## The campaigns

- **full** (new): two batches, 4 slots, Foreman mode, and no human steps in: the operator plays
  the user (gos, merges, approvals, confirmations); nothing waits on the real user.
  - Batch 1: 8 feature CRs plus a release CR, which is the batch's last CR and depends on all the
    others, so it runs at the end. During the coding, a 10th CR is injected with `order add`; it
    lands between the 8 others and the release (the release waits for it too). Injection while
    the batch runs is not possible in direct mode: that is why full runs with a Foreman.
  - Batch 2: 2 feature CRs plus a release CR, the last, depending on both.
  - The PRs merge on the sandbox and both releases are made there by the sandbox's own release
    procedure; the next reset cleans them up.
- **real-foreman** and **real-direct** (rebuilt on the sandbox): one batch of 5 CRs, no release.
  The mode is chosen at launch (`--mode stack|parallel|series`); the same 5 CRs in every mode, so
  the modes compare. real-direct has never run: its first run follows this CR.
- **copilot** takes one of the frozen CRs.

## Decisions left to the Chief of Staff (Q3, Q4: "fais-en ce que tu veux")

- **Which CRs:** 11 feature CRs and 2 release CRs, written for the sandbox app: small features
  that each touch the backend, the hand-written HTML and the tests. Batch 1's 8 include the 5 of
  the quick campaigns; the injected 10th and batch 2's 2 are distinct. Some CRs touch the same
  files on purpose (so rebases after a merge happen); none depends on another unless the
  specification says why. Each runs in a few rounds at most.
- **The judge:** one hidden test file (or a few) per feature CR in the kit, run by the audit
  against the PR's head in a clean clone of the sandbox, with the project's own test command; a
  pass, a fail or "not run" per CR in the report. A release CR is judged by what the sandbox
  shows (the version, the tag, the GitHub release, the notes).

## Known constraints

- An eval's workspace is outside this repository and the main checkout does not change during an
  eval (AGENTS.md).
- Claude Desktop's 10-message limit between sessions: a Foreman batch of 10 CRs and a release
  sends more asks than that; the runbook says how the operator lives with it (the host's turn
  notes and `status`), as `evals/README.md` already says for long campaigns.
