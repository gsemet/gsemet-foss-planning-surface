Head: db4ba03eb86f943f6acf355e3052211213093f2c

Description pass on PR 320 (short pass), judged at db4ba03.

- Clean: sections in template order, fold with blank lines after summary and before details, nothing after details. No images. Judged at db4ba03 from `gh pr view 320 --json body`.
- Consistent with the diff: `git diff --stat origin/main...HEAD` lists 13 files (CONTRIBUTING.md, docs/boards.md, hooks/register.tsx and test, five reference cards, four agents/*-driver.md); every one is named in Changes or Deliverables. Four new tests in hooks/register.test.tsx, `worktreeOf` and `rootOf` exist in hooks/register.tsx. Judged at db4ba03.
- Role names: Driver and Foreman appear as product terms of cards and agent files the diff changes (pr-template, The rules); none as the doer of the work. Internal references holds the CR name only there. Judged at db4ba03.
- Review box: `chantier log 354` has "r1 inspector approved at bdd27e0f..." and "r1 approved at bdd27e0f, committed as db4ba03e", matching `approved at bdd27e0`, committed as `db4ba03`.
- Known gaps: states unproved host rows and accepted long lines; Autonomous decisions "None" consistent. Verified at db4ba03 matches the earlier verdict VERIFIED at that head in the log.
- No STALE mark. No image, so no username or home folder exposure.

VERIFIED
