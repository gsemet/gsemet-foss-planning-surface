# The Chief of Staff asks for a long check before a release

## Change

- `skills/chantier/references/chief-of-staff.md`, section Releases: when the project's procedure
  has no long check on the exact head of the default branch before the version commit, the Chief
  of Staff asks the user whether to plan one, says why (per-CR gates miss what CRs break together
  and any check skipped on a PR), and offers to write the answer in the project. The user's answer
  rules: chantier imposes no gate.
- `docs/use-cases.md`, section "Make a release": one sentence saying so.
- The CLI, the agents and the Release driver's card do not change.

## Done when

- `just check` and `just scenario` pass, and CI is green at the PR's head.

## This PR is never merged

This CR is an eval of chantier with the real tools. It stops at an open PR.

- Open the PR as a draft.
- The first line of its body is exactly: `**Eval run: do not merge.** The maintainer decides what happens to this PR.`
- Nobody merges it, marks it ready, or enables auto-merge: not a Driver, not the Foreman.
