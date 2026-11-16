**Eval run: do not merge.** The maintainer decides what happens to this PR.

## Change

- `skills/chantier/references/chief-of-staff.md`, section Releases: when the project's procedure
  has no long check on the exact head of the default branch before the version commit, the Chief
  of Staff asks the user whether to plan one, says why, and offers to write the answer in the
  project. The user's answer rules: chantier imposes no gate.
- `docs/use-cases.md`, section "Make a release": one sentence saying so.

The CLI, the agents and the Release driver's card do not change.

## Checks

- `just check` and `just scenario` pass at this head.
