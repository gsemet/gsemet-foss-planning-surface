# CR-301 Change Specification: every use case (StRS) states its main paths

✅ merged · batch-01 · [PR](https://github.com/gsemet/markdown-okf-schema-studio/pull/372)

**Now:** Merged: https://github.com/gsemet/markdown-okf-schema-studio/pull/372.
**Next:** Nothing.

## Progress

- [x] Round 1: Round 1: check script, its test, justfile wiring, project guideline section (spec sections 1 and 3)
- [x] Round 2: Round 2: Main paths written in the 80 active StRS by 4 parallel coders on disjoint scopes
- [x] Long gate fail: 040e40a1
- [x] Long gate fail: 040e40a1
- [x] Long gate fail: 040e40a1
- [x] Note: Gate: ci-static and ci-visual pass; ci-integration fails twice on the same real-window step (real-input, Warning type change timeout), a docs-only diff, so environmental. PR opened as draft.
- [x] Shipped: https://github.com/gsemet/markdown-okf-schema-studio/pull/372
- [x] Handed back
- [x] Merged: https://github.com/gsemet/markdown-okf-schema-studio/pull/372

## Documents

- [intent](01-intent.md)
- [answers](02-answers.md)
- [specification](03-change-spec.md)
- [pr-body](work/pr-body.md)
- [long gate log](work/gates/20261112-130807.log)
- [.agents/constitution.md](../../../constitution.md)
- [.agents/guidelines/git-commit-message.guidelines.md](../../../guidelines/git-commit-message.guidelines.md)
- [.agents/skills/okfreq/SKILL.md](../../../skills/okfreq/SKILL.md)
- [AGENTS.md](../../../../AGENTS.md)
- [requirements/guidelines/project.guidelines.md](../../../../requirements/guidelines/project.guidelines.md)
- [requirements/guidelines/requirements.guidelines.md](../../../../requirements/guidelines/requirements.guidelines.md)
- [requirements/tiers/log.md](../../../../requirements/tiers/log.md)
- [requirements/tiers/strs/diagrams/StRS-MDOKFSTUDIO-DIAG-001.md](../../../../requirements/tiers/strs/diagrams/StRS-MDOKFSTUDIO-DIAG-001.md)

## Where

- Branch: `chantier/batch-01/cr-301-change-specification-every-use-case-strs`
- Worktree: `/Users/az02065/Projects/DevTools/markdown-okf-schema-studio.worktrees/batch-01-CR-301`
- Driver: `-`

## Decisions and open questions

- Gate: ci-static and ci-visual pass; ci-integration fails twice on the same real-window step (real-input, Warning type change timeout), a docs-only diff, so environmental. PR opened as draft.
- answer: owner says rebase PR #372 on main (BEHIND since #371 merged), then it is mergeable for them; restack CR-302 on top after the rebase
- back to a Driver: rebase: owner order O-2 — rebase PR #372 on main (BEHIND since #371 merged); keep it ready, push with --force-with-lease, re-check CI, hand back ready. CR-302 will be restacked on top afterwards.

## Cost

$5.04.
