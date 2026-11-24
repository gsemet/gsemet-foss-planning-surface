# Verify CR-477 raw-text

Head: b54b414c4ca0ca779bae36457f3e30ef9f082ab4

Verdict: NOT VERIFIED (one claim, cheap to fix).

Claims, all judged at b54b414c:

1. Removed code is gone. `grep -rnE "openingWatcher|openingDecision|putStudioInPlace|showDocumentInStudio|navigatesInStudio|StudioLineRequests|StudioOpenedTextEditors|StudioClosedTabs|searchResultsInStudio|opening watcher" src test docs skills package.json requirements CONTRIBUTING.md .agents/glossary`: the hits left are the reverse migration and its tests, history sentences in docs/user (open-studio.md, settings.md), and archived or superseded requirements and the log. The files openingWatcher.ts, studioPlacement.ts, openingPolicy.ts and studioNavigation.ts appear as deleted in `git diff --stat 0303eaf7 HEAD`. PASS.
2. Unit and host tests. `npm run compile`, then `node scripts/node-test.mjs unit "out/test/{core/configuration,session,host}/*.test.js"`: tests 569, pass 566, fail 0, skipped 3. `node scripts/node-test.mjs security "out/test/security/*.test.js"`: tests 106, pass 104, fail 0, skipped 2 (covers package-contract). PASS.
3. Settings schema. `just check-settings`: "check-settings: passed (20 settings)". `package.json` keeps `onLanguage:markdown` and `openAsText`, and has no `open.*` property. PASS.
4. Reverse migration, `just preflight` pass. work/gates/pf-final.log ends "ci-static: passed ... exit 0", and the Driver's note "just preflight: pass" is at b54b414c. PASS (cited, not re-run).
5. Real window. CI run 45249949581 at head b54b414c: success. Heavy run 45249961604 at head b54b414c: success, with integration, stress, static-windows and visual green. The integration log shows "STEP done: open-at-line" with the matrix lines (jump under the association studio=1 text=0 marks=0; file already open as text studio=1 text=1; Open as Text sourceLine=64 cursor=63) and "STEP done: reverse-migration-suite". `test/integration/reverse-migration-suite.ts` asserts the user `settings.json` and the `.code-workspace` file. PASS.
6. PR body as posted equals work/pr-body.md (diffed, SAME). It renders and is consistent with the diff (74 files: removals, studioSelections.ts rename, SwRS-195 added, tests listed). It carries no image. Its internal references line is one CR id. PASS.
7. CHANGELOG line. It is at `## Unreleased` and has all four required points, but it ends with "PR #0" instead of "PR #493". The Foreman note says CR-478 fixes this, but the PR body has no "Known gaps" section that names it. FAIL: a failed, accepted claim has no Known gaps bullet. Fix: set "PR #493" in the line, or add a Known gaps bullet saying PR #0 is carried by CR-478.

Carried: the before/after evidence is not applicable (no UI change; the PR declares "No visual change"). The Review box is unchecked, so it claims nothing.

Left alone: the untracked test/integration/fixtures/open-at-line-* dirs.
