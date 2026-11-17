# Answers

## eval-away-Q1: starting an eval away from the desk

2026-11-17, the user chose the recommended answer: one eval root folder the user trusts once at the desk; every run makes its workspace inside it, so no run asks for a new trust. The trust itself stays the user's act; chantier never edits a trust or security setting.

Spec critic: yes, it changes how evals start and touches the user's trust boundary.

## Spec questions (2026-11-17)

- eval-away-Q2 (how setup knows the root): a git-ignored local file names the eval root (e.g. `evals/kit/eval-root.local.json`); setup refuses a workspace outside it.
- eval-away-Q3 (campaigns away from the desk): only the campaigns with no Foreman start away from the desk; the README, the Prerequisites and the Foreman runbooks say plainly that the Foreman campaigns still need the desk to start the Foreman and type the go.
- eval-away-Q4 (the trial): yes, the trial checks that the session started from the phone is on the workspace's main checkout (`git rev-parse --git-dir` equals `--git-common-dir`, top level is the workspace); anything else is a Fail. It also records how the session was created from the phone.
