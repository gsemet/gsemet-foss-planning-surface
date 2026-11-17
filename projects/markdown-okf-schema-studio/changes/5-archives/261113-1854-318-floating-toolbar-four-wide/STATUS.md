# CR-318 Change specification: the floating toolbar becomes a 4 × 4 grid

✅ merged · batch-04 · [PR](https://github.com/gsemet/markdown-okf-schema-studio/pull/390)

**Now:** Merged: https://github.com/gsemet/markdown-okf-schema-studio/pull/390.
**Next:** Nothing.

## Progress

- [x] Round 1: Implement spec 03-change-spec.md in full (sections 3.1-3.6)
- [x] Round 2: fix inspector item: TOOLBAR-130 scenario heading rows 2 to 4; test/visual/scenarios.ts:124 comment
- [x] Long gate fail: b9f7dc2b
- [x] Note: preflight at b9f7dc2b: static+visual pass; ci-integration failed only from the locked screen (accepted: heavy run on branch is the proof); report/gallery follow from it
- [x] Shipped: https://github.com/gsemet/markdown-okf-schema-studio/pull/390
- [x] Blocked: waits: PR 390 CI and heavy run 43476490855 still running; then Verifier screenshots and TOOLBAR-001 geometry
- [x] Round 3: CI visual: toolbar-float first paragraph check fails on CI at 393px after the shorter toolbar
- [x] Shipped: https://github.com/gsemet/markdown-okf-schema-studio/pull/390
- [x] Shipped: https://github.com/gsemet/markdown-okf-schema-studio/pull/390
- [x] Note: heavy run 43480001535: all pass except stress round 7/20 alert-dropdown timeout (editor flake, unrelated to toolbar); one re-run of the failed job started
- [x] Blocked: waits: heavy run 43483133215 at head 2ca565e1 still running; then gh pr ready 390
- [x] Note: heavy run 43483133215 at 2ca565e1 green; PR ready
- [x] Handed back
- [x] Merged: https://github.com/gsemet/markdown-okf-schema-studio/pull/390

## Documents

- [request](intake/request.md)
- [intent](01-intent.md)
- [answers](02-answers.md)
- [specification](03-change-spec.md)
- [pr-body](work/pr-body.md)
- [long gate log](work/gates/20261113-183515.log)
- [.agents/constitution.md](../../../constitution.md)
- [.agents/glossary/common.md](../../../glossary/common.md)
- [AGENTS.md](../../../../AGENTS.md)
- [CHANGELOG.md](../../../../CHANGELOG.md)
- [docs/user/README.md](../../../../docs/user/README.md)
- [docs/user/toolbar.md](../../../../docs/user/toolbar.md)
- [requirements/guidelines/project.guidelines.md](../../../../requirements/guidelines/project.guidelines.md)
- [requirements/guidelines/requirements.guidelines.md](../../../../requirements/guidelines/requirements.guidelines.md)
- [requirements/tiers/log.md](../../../../requirements/tiers/log.md)
- [requirements/tiers/strs/layout-width/StRS-MDOKFSTUDIO-LAYOUT-003.md](../../../../requirements/tiers/strs/layout-width/StRS-MDOKFSTUDIO-LAYOUT-003.md)
- [requirements/tiers/strs/toolbar-navigation/StRS-MDOKFSTUDIO-TOOLBAR-001.md](../../../../requirements/tiers/strs/toolbar-navigation/StRS-MDOKFSTUDIO-TOOLBAR-001.md)
- [requirements/tiers/swrs/lifecycle-sync/SwRS-MDOKFSTUDIO-LIFE-049.md](../../../../requirements/tiers/swrs/lifecycle-sync/SwRS-MDOKFSTUDIO-LIFE-049.md)
- [requirements/tiers/swrs/lifecycle-sync/SwRS-MDOKFSTUDIO-LIFE-170.md](../../../../requirements/tiers/swrs/lifecycle-sync/SwRS-MDOKFSTUDIO-LIFE-170.md)
- [requirements/tiers/swrs/review-annotations/SwRS-MDOKFSTUDIO-REVIEW-008.md](../../../../requirements/tiers/swrs/review-annotations/SwRS-MDOKFSTUDIO-REVIEW-008.md)
- [requirements/tiers/swrs/theme-zoom/SwRS-MDOKFSTUDIO-THEME-001.md](../../../../requirements/tiers/swrs/theme-zoom/SwRS-MDOKFSTUDIO-THEME-001.md)
- [requirements/tiers/swrs/toolbar-navigation/SwRS-MDOKFSTUDIO-TOOLBAR-001.md](../../../../requirements/tiers/swrs/toolbar-navigation/SwRS-MDOKFSTUDIO-TOOLBAR-001.md)
- [requirements/tiers/swrs/toolbar-navigation/SwRS-MDOKFSTUDIO-TOOLBAR-007.md](../../../../requirements/tiers/swrs/toolbar-navigation/SwRS-MDOKFSTUDIO-TOOLBAR-007.md)
- [requirements/tiers/swrs/trust-security/SwRS-MDOKFSTUDIO-TRUST-001.md](../../../../requirements/tiers/swrs/trust-security/SwRS-MDOKFSTUDIO-TRUST-001.md)

## Where

- Branch: `chantier/batch-04/cr-318-change-specification-the-floating-toolba`
- Worktree: `/Users/az02065/Projects/DevTools/markdown-okf-schema-studio.worktrees/batch-04-CR-318`
- Driver: `-`

## Decisions and open questions

- preflight at b9f7dc2b: static+visual pass; ci-integration failed only from the locked screen (accepted: heavy run on branch is the proof); report/gallery follow from it
- back to a Driver: fix: PR CI visual fails layout-width/v88-toolbar-float-first-lines-cream-393 (75-toolbar-float--light--sticky-3): first paragraph starts above the toolbar bottom edge; passes locally; round 3 is the last
- heavy run 43480001535: all pass except stress round 7/20 alert-dropdown timeout (editor flake, unrelated to toolbar); one re-run of the failed job started
- heavy run 43483133215 at 2ca565e1 green; PR ready
- back to a Driver: close-out: heavy run green at 2ca565e1, PR ready; only handback ready is left

## Cost

$4.14.
