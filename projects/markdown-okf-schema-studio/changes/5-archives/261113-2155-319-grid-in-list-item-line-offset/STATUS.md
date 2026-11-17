# CR-319 Change Specification: a grid inside a list item maps its cards one line too early

✅ merged · batch-04 · [PR](https://github.com/gsemet/markdown-okf-schema-studio/pull/392)

**Now:** Merged: https://github.com/gsemet/markdown-okf-schema-studio/pull/392.
**Next:** Nothing.

## Progress

- [x] Round 1: Implement the change specification in full: failing tests first, fix, requirement scenario, log, changelog, requirements-update. Do not commit.
- [x] Note: Round 1 approved, committed; running long gate
- [x] Long gate fail: fc21e5e5
- [x] Note: Local preflight: static and visual passed; integration failed on tall-block-scroll toolbar clearance (real VS Code, unrelated to line mapping), so report/gallery failed. Running heavy CI on the branch as proof.
- [x] Shipped: https://github.com/gsemet/markdown-okf-schema-studio/pull/392
- [x] Note: Rebased onto main after CR-320 merged (log.md conflict only); just check green; pushed force-with-lease; heavy CI rerun
- [x] Shipped: https://github.com/gsemet/markdown-okf-schema-studio/pull/392
- [x] Blocked: waits: heavy CI run 43501134204 on head 00569bd (PR 392, draft); resume: read gh run view 43501134204, if green + Verifier then gh pr ready 392 and handback ready
- [x] Note: Verifier VERIFIED at 00569bd; evidence in PR Impacts; PR ready
- [x] Handed back
- [x] Merged: https://github.com/gsemet/markdown-okf-schema-studio/pull/392

## Documents

- [request](intake/request.md)
- [intent](01-intent.md)
- [answers](02-answers.md)
- [specification](03-change-spec.md)
- [pr-body](work/pr-body.md)
- [long gate log](work/gates/20261113-203150.log)
- [.agents/constitution.md](../../../constitution.md)
- [AGENTS.md](../../../../AGENTS.md)
- [CHANGELOG.md](../../../../CHANGELOG.md)
- [requirements/tiers/log.md](../../../../requirements/tiers/log.md)
- [requirements/tiers/swrs/block-editing/SwRS-MDOKFSTUDIO-BLOCK-258.md](../../../../requirements/tiers/swrs/block-editing/SwRS-MDOKFSTUDIO-BLOCK-258.md)

## Where

- Branch: `chantier/batch-04/cr-319-change-specification-a-grid-inside-a-lis`
- Worktree: `/Users/az02065/Projects/DevTools/markdown-okf-schema-studio.worktrees/batch-04-CR-319`
- Driver: `-`

## Decisions and open questions

- Round 1 approved, committed; running long gate
- Local preflight: static and visual passed; integration failed on tall-block-scroll toolbar clearance (real VS Code, unrelated to line mapping), so report/gallery failed. Running heavy CI on the branch as proof.
- Rebased onto main after CR-320 merged (log.md conflict only); just check green; pushed force-with-lease; heavy CI rerun
- back to a Driver: resume: heavy run green at 00569bd; Verifier, PR body Impacts, gh pr ready, handback ready
- Verifier VERIFIED at 00569bd; evidence in PR Impacts; PR ready

## Cost

$1.84.
