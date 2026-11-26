# StRS acceptance tests: the remaining groups, then the mode switch

Follow-up of CR-505 (strs-acceptance, https://github.com/gsemet/markdown-okf-schema-studio/pull/532), for the batch after batch-09: accept the remaining use case paths, then switch the requirements coverage mode.

CR-505 delivers the bench and the trust-security group (5 of its 8 paths accepted; across all groups 134 of 156 paths are not accepted and 702 of 2638 scenarios have no marker, at its pull request's head).

Wanted, as the owner decided on 2026-11-26:
- One change per e2e group with no acceptance file yet: rendering-core, code-blocks, gfm, myst, diagrams, frontmatter-schema, frontmatter-editing, layout-width, theme-zoom, toolbar-navigation, block-editing, palette-slash, table-editing, review-annotations, lifecycle-sync. Each carries the SwRS scenario tests and marker repairs of its group, as CR-505 does for trust-security.
- The three trust-security paths left out (TRUST-012 S1 and S2, TRUST-014 S1) get another kind of test (driving the real window, a real install); the strict marker rule is unchanged.
- The coverage-mode switch and its gate come last.
- Split this item into those changes when that batch is prepared; CR-505's specification is the design.
