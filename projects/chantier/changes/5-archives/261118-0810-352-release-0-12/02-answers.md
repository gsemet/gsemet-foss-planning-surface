Short name: `release-0-12`

# Answers

1. Q: Make a release? User, 2026-11-18: "Enchaîne tout seul les dix puis tu feras une release
   sans evals." This means: run batch-24's six retro CRs on their own, then release.
2. Q: The eval campaigns that CONTRIBUTING.md asks for before a release? User, same words: none.
   No campaign and no new run. The claims file `evals/results/claims-v0.12.0.md` marks each claim
   `scenario only` (proved by a named check of `just scenario` or `just test`) or `not exercised`.
   The notes' "For contributors" bullet lists them, and the PR says no eval ran.

## Settled by the Chief of Staff (the user is away)
- Version: v0.12.0, minor. There is new behaviour since v0.11.0 (the board's design system, the
  Batch view's tabs, the PRs page, forge links, the CR pane following the seat, the round-one host
  matrix), and nothing breaks a user's setup.
- Batch: batch-24, the batch whose work it ships (docs/release-process.md). It is added with
  `--release`, so it runs last, after the six retro CRs, from an up-to-date `main`.
- Notes cover everything since v0.11.0 on `main`: every `feat:` and `fix:` commit exactly once.
- Images come from batch-24's real run: the merged PRs' evidence screenshots and
  `docs/web-board/*.png`, anonymised as docs/release-process.md says. None invented. No docs SVG
  diagram.
- Grant: the user merges the version PR. Each irreversible step after that (tag, forge release)
  waits for the user's approval.
