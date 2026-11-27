# Evidence plan (CR Driver; no investigator: the specification names every edit)

Host and default matrix: none (the rule depends on no host and no setting value).
Screenshots: none (no user-visible change; the PR body says "No visual change" with the reason).

Base of the CR: chantier/batch-09/cr-509-reliable-heavy-ci-split-the-trusted-laun.
Every command runs in the worktree at the pushed head.

1. `uv run --no-sync --group requirements okfreq validate --check-links --project-root .` passes.
2. `just check-markers` passes; S8 and S9 of SwRS-MDOKFSTUDIO-LAYOUT-023 each keep a `@tests_req`.
3. `just requirements-update` leaves no diff (`git status --porcelain` empty); the coverage output
   lists SwRS-MDOKFSTUDIO-LAYOUT-023#S9 with test/page/runtimePageControls.test.ts and
   test/page/codeBlockBreakout.test.ts. `just requirements-lint` passes.
4. The unit test `T10b: a wide block nested in a container is not measured` passes, and fails when
   `wrapperOf` (src/page/modules/widthMode.ts) accepts any element (in the Verifier's own detached
   worktree, or from the Coder's recorded run).
5. test/page/codeBlockBreakout.test.ts passes; its diff against the base adds marker lines only.
6. `git diff <base>...HEAD --stat -- src/` is empty (the CR's own diff; lower stack PRs excluded).
7. `just preflight` passes (Windows: static stage; CI runs the others).
8. The PR body's Tests section names SwRS-MDOKFSTUDIO-LAYOUT-023 (changed, scenario S9 added) with
   src/page/modules/widthMode.ts and its test files.
9. The SwRS text: description equals the normative statement, both restrict widening to top-level
   elements; S9 declared with its heading; list-item row gone from S8; Known issue line gone, the
   two others kept; StRS files untouched; a log entry dated in requirements/tiers/log.md.
