# Verify CR-477 raw-text

Head: 39dcfc0fcdda7846d0c6002820dd9bfe2dfd362e

Verdict: VERIFIED.

Claims at 39dcfc0f:

1. Head and tree. `git rev-parse HEAD` = 39dcfc0fcdda7846d0c6002820dd9bfe2dfd362e; `git status --short` empty. PASS.
2. Rebase touched nothing. `git range-diff b54b414~13..b54b414 HEAD~13..HEAD`: commits shown as `=` (same patches). Claims 1 to 5 and the real-window proof of the b54b414 judgment are carried from b54b414: a clean rebase, same patch.
3. Removed code is gone. `grep -rnE "openingWatcher|putStudioInPlace|showDocumentInStudio" src test package.json` minus migration lines: no hit. PASS.
4. Gate. work/gates/pf2.log ends "ci-static: passed / exit 0" (local `just preflight`, Windows static stage). PASS (cited).
5. CI at 39dcfc0f: `gh run view 45338450523` success, headSha 39dcfc0f; heavy run 45338450342 (integration, stress) success, headSha 39dcfc0f. PASS.
6. PR description. Posted body (`gh pr view 493 --json body`) diffed against work/pr-body.md: only a trailing blank line differs. PR is draft, head 39dcfc0f. It renders, matches the diff (74 files), carries no image. Known gaps now has a bullet for the changelog `PR #0` (CHANGELOG.md line 13, filled by CR-478's references step) and for the VS Code opening limits. A declared, accepted gap, not a failure. PASS.
7. Before/after: not applicable (no UI change, PR says "No visual change"). Review box unchecked, claims nothing.

## Description pass at 39dcfc0fcdda7846d0c6002820dd9bfe2dfd362e

Command: `gh pr view 493 --repo gsemet/markdown-okf-schema-studio --json body` read against pr-template "The audit" and `git diff --stat origin/main...HEAD` (74 files).

- Sections Summary, Deliverables, Blast radius, Autonomous decisions, Known gaps visible in order; one Details fold with Changes, Impacts, Test plan, Internal references; blank lines around the fold; nothing after it. PASS.
- Known gaps present with the `PR #0` and opening-limit bullets. PASS. No role name as doer, CR name only in Internal references. PASS.
- SHA marks: "Verified at 39dcfc0", "CI green at 39dcfc0" match head; `gh run view 45338450342` success at 39dcfc0f. PASS.
- Test plan lacks the `Review: approved at <sha7>` item, which both the project template (.github/PULL_REQUEST_TEMPLATE.md, "Review") and the pr-template Test plan require, and lacks the Evidence item (or its "none, no visual change" line). The earlier note "Review box unchecked" does not match the posted body: there is no box. `$CHANTIER log 477` has one approved note only, at 1390620c (r3), none at 39dcfc0. FAIL.

Description verdict at 39dcfc0: NOT VERIFIED (fix: add the Review item, unchecked or citing a recorded pass, and the Evidence item to Test plan; re-post).

## Description pass 2 at 39dcfc0fcdda7846d0c6002820dd9bfe2dfd362e

Head: 39dcfc0fcdda7846d0c6002820dd9bfe2dfd362e

Command: `gh pr view 493 --repo gsemet/markdown-okf-schema-studio --json body`, read against `.github/PULL_REQUEST_TEMPLATE.md` (the project template ranks above pr-template and is used as written: Summary, Deliverables, Changes, Impacts, Blast radius, Test plan, optional Internal references; no Details fold), and `git diff --stat origin/main...HEAD` (74 files).

- Layout follows the project template; extra sections (Autonomous decisions, Known gaps, owner and release-note sections) are allowed. Renders: tables, mermaid, headings. PASS.
- Test plan now has `Review: approved at 39dcfc0 (carried from the round-3 approval at 1390620)`. `$CHANTIER log 477` line 68: "review: approved at 39dcfc0 (carried from 1390620c, the r3 inspector approval ...)", and line 17 records the r3 approval at 1390620c. Note SHA matches the box. PASS.
- Evidence item present: "no visual change; proof is real-window tests at 39dcfc0 (no before/after images)"; Impacts says "No visual change". PASS.
- Summary/Changes match the diff: removed openingWatcher.ts, studioPlacement.ts, openInStudio.ts, openingPolicy.ts and its tests, settings registry entries, reverse migration in associationMigration.ts, new SwRS LIFE-195, reverse-migration-suite.ts. PASS.
- Known gaps: PR #0 changelog placeholder and the opening limits. PASS. Role names: none; CR-477 only in Internal references. PASS.
- SHA marks: `gh run view 45338450342` success, headSha 39dcfc0f (workflow_dispatch heavy); `gh pr checks 493` pass at the PR run for 39dcfc0f; PR headRefOid 39dcfc0f. PASS.
- No image in the body. PASS.

Description verdict at 39dcfc0: VERIFIED
