# CR-311 Change Specification: a long heading in the sticky band stays on one line

✅ merged · batch-02 · [PR](https://github.com/gsemet/markdown-okf-schema-studio/pull/382)

**Now:** Merged: https://github.com/gsemet/markdown-okf-schema-studio/pull/382.
**Next:** Nothing.

## Progress

- [x] Round 1: Implement the whole specification
- [x] Long gate fail: 3a3aacf7
- [x] Shipped: https://github.com/gsemet/markdown-okf-schema-studio/pull/382
- [x] Note: Local preflight: static+visual passed; integration real-input flaked (focus under load) and pytest tmp PermissionError; heavy run dispatched as proof
- [x] Shipped: https://github.com/gsemet/markdown-okf-schema-studio/pull/382
- [x] Note: Fixed overlap check clamp; CI green on 352077d (pr + heavy run 43337013395 integration/stress green); first run's v30 failure not reproduced locally (full visual 474 passed)
- [x] Handed back
- [x] Shipped: https://github.com/gsemet/markdown-okf-schema-studio/pull/382
- [x] Note: Restack: scenario id renumbered v44->v45 (CR-310 took v44); PR body alt text updated.
- [x] Merged: https://github.com/gsemet/markdown-okf-schema-studio/pull/382

## Documents

- [intent](01-intent.md)
- [answers](02-answers.md)
- [specification](03-change-spec.md)
- [conflicts](work/conflicts.md)
- [pr-body](work/pr-body.md)
- [long gate log](work/gates/20261113-002252.log)
- [.agents/guidelines/git-commit-allowed-scopes.md](../../../guidelines/git-commit-allowed-scopes.md)
- [AGENTS.md](../../../../AGENTS.md)
- [CHANGELOG.md](../../../../CHANGELOG.md)
- [requirements/tiers/log.md](../../../../requirements/tiers/log.md)
- [requirements/tiers/strs/toolbar-navigation/StRS-MDOKFSTUDIO-TOOLBAR-004.md](../../../../requirements/tiers/strs/toolbar-navigation/StRS-MDOKFSTUDIO-TOOLBAR-004.md)
- [requirements/tiers/swrs/toolbar-navigation/SwRS-MDOKFSTUDIO-TOOLBAR-025.md](../../../../requirements/tiers/swrs/toolbar-navigation/SwRS-MDOKFSTUDIO-TOOLBAR-025.md)

## Where

- Branch: `chantier/batch-02/cr-311-change-specification-a-long-heading-in-t`
- Worktree: `/Users/az02065/Projects/DevTools/markdown-okf-schema-studio.worktrees/batch-02-CR-311`
- Driver: `-`

## Decisions and open questions

- Local preflight: static+visual passed; integration real-input flaked (focus under load) and pytest tmp PermissionError; heavy run dispatched as proof
- Fixed overlap check clamp; CI green on 352077d (pr + heavy run 43337013395 integration/stress green); first run's v30 failure not reproduced locally (full visual 474 passed)
- Restack: scenario id renumbered v44->v45 (CR-310 took v44); PR body alt text updated.

## Cost

$3.05.
