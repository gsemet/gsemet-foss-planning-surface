# Verify CR-445

Head: f61ac3a920146b83d5b3deaa56a1e3472b564481

Verdict: VERIFIED (description pass at f61ac3a9 re-done; code claims below VERIFIED).

## Claims

1. Long gate pass at the head: VERIFIED at f61ac3a9. `work/gates/20261121-042413.log` first line: `gate CR-445 branch ... head f61ac3a920146b83d5b3deaa56a1e3472b564481`, last line `result: pass at f61ac3a920146b83d5b3deaa56a1e3472b564481` (`just preflight`, requirements errors 0).
2. Unit and security tests at the head: VERIFIED at f61ac3a9. `npm run compile` clean; `npm run test:unit` -> `tests 4264 pass 4249 fail 0 skipped 15`; `npm run test:security` -> `tests 102 pass 100 fail 0 skipped 2`.
3. Manifest (spec 4.3, 4.4, 4.5, 4.8): VERIFIED at f61ac3a9. Node read of package.json: activationEvents hold `onLanguage:markdown` (the only onLanguage); commands `openAsText` "Open as Text" and `showFeatureIntroductionsAgain` "Show Feature Introductions Again", category "Markdown OKF-Schema Studio"; `openAsText` in editor/title and commandPalette with `activeCustomEditorId == 'markdown-okf-schema-studio.editor'`; `open.searchResultsInStudio` default true (description 415 chars), `open.markdownFilesInStudio` default false (461 chars), both under 700.
4. CI at the head: VERIFIED. `gh pr checks 452`: static, static-windows, visual, report, checks pass; `gh run view 44860936230` (heavy, headSha f61ac3a9): success, jobs static, visual, static-windows, stress, integration, report, checks, gallery all success.
5. Real VS Code, Linux CI, at the head: VERIFIED (narrow). The heavy run's integration log shows `STEP start: open-at-line` ... `STEP done: open-at-line (3212 ms)`; `test/integration/openAtLine.test.ts` asserts, in a real window, a jump -> one Studio tab, no text tab, `.sphinx-preview-line-marker` present; search off -> text editor stays; files on plain opening -> Studio, no marker. Other trials (T3, T6, T7, T11, T13...) are not re-run at this head: UNVERIFIED here, carried as the Coder's trial logs in evidence/ (ta-*, tb-*, tc-*, td-*), not proof at this head.
6. Marker look and edit-mode arrow, at the head: VERIFIED. Visual job at f61ac3a9 passed the 12 lifecycle-sync scenarios; I opened v04, v10, v11 of artifact e2e-visual-attempt-1 (run 44860928294): arrow in left margin plus band on the exact code line; closed dropdown unfolded with the marker on the inner line; edit mode arrow clear of the list handles. Copied to `work/verifier/evidence/`, see before-after.md. No username or home folder visible.
7. Spec deviations declared in the body: confirmed. Watcher in `src/host-vscode/openingWatcher.ts` and `studioPlacement.ts` (diff stat); `test/integration/openAtLineCampaign.ts` absent (campaign cut, in Known gaps).
8. CHANGELOG, docs (`open-studio.md`, `settings.md`, `known-limitations.md`), glossary and requirements (StRS-LIFE-023, SwRS LIFE-174..185, changes to LIFE-001, 004, 149, 156, CORE-001, log.md) are in the diff against the base: VERIFIED at f61ac3a9 (`git diff --stat origin/<base>...HEAD`).
9. Review box: not checked here (Driver log has "r5 inspector approved at 28cf0ce2 ... committed as f61ac3a9"; the box is filled at closing).
10. PR description, as posted, re-checked at f61ac3a9: VERIFIED. Command: `gh pr view 452 --json body,headRefOid` -> headRefOid f61ac3a920146b83d5b3deaa56a1e3472b564481.
    - The stale "openAtLine.test.ts not run" claim is gone; Known gaps now says it ran in heavy run 44860936230 (step open-at-line, success), matching claim 5, and keeps its limited coverage and the **UNVERIFIED:** diffs bullet.
    - Narrow-pane edit-mode arrow bullet is present in Known gaps. Test plan boxes name `f61ac3a`, no sha7 placeholder left.
    - Review box "approved at f61ac3a": `chantier log CR-445` has "r5 approved at 28cf0ce2, committed as f61ac3a9" (and the inspector approval at 28cf0ce2 for the same tree): matches.
    - Images: three uploads fetched with `gh auth token`, HTTP 200 image/png; sha256 equal to work/verifier/evidence/v04 (light code line), v10 (closed dropdown, dark), v11 (edit mode list handle, dark), which I opened at claim 6: captions match, made-up fixture text, no username or home folder. Order and captions match the files.
    - Summary, Deliverables, Changes match the diff (claim 7, 8); Mermaid block and fold well formed; internal references only inside the folded section; footer is the attribution line the harness requires.
    - Test plan "Verified at f61ac3a" and "CI green" are backed by this file and claim 4.
