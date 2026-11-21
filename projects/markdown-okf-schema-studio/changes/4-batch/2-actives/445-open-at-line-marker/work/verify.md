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


---

# Move re-judgment: f61ac3a9..207a550a (rebase onto the CR-444 branch, 5 conflict hunks)

Head: 207a550a3cbd7e801c02ff26e5ac390f73f97524

Verdict: VERIFIED at 207a550a.

M1. Long gate pass at the new head: VERIFIED at 207a550a. `work/gates/20261121-051438.log` first line `gate CR-445 branch ... head 207a550a3cbd7e801c02ff26e5ac390f73f97524`, last line `result: pass at 207a550a3cbd7e801c02ff26e5ac390f73f97524` (`just preflight`; visual, integration, report, gallery skipped on Windows, run by CI).
M2. Unit and security tests at the new head (the base brought changes to src/core/protocol, page runtime, tests): VERIFIED at 207a550a. `npm run compile` clean; `npm run test:unit` -> `tests 4385 pass 4370 fail 0 skipped 15`; `npm run test:security` -> `tests 102 pass 100 fail 0 skipped 2`.
M3. Files both the base move and the CR patch touch (git diff --name-only, intersection): glossary, release-process guideline, CHANGELOG, requirements log, hostToPage.ts, pageRuntime.ts, runtime.ts, trusted-suite.ts, runtimeHarness.ts, e2eGroups.ts, e2eGroups.test.ts, visual capture/scenario files. Conflict notes (`work/conflict-resolver/conflicts.md`) keep both sides in every hunk (counts 487+9=496, 34+1=35); both tests and the gate above pass, which covers the count tests.
M4. CI at the head: VERIFIED. `gh pr checks 452` (run 44864898286, head 207a550a per `gh pr view 452 --json headRefOid`): static, static-windows, visual, report, checks pass; the rest skipping on a PR.
M5. Review: `chantier log CR-445`: "move f61ac3a..207a550 (conflict) inspector approved at 207a550a3cbd7e801c02ff26e5ac390f73f97524".
M6. Evidence images: carried from f61ac3a9 (captured on Linux CI, opened then at claim 6, no username or home folder); the visual job at 207a550a is green, so the scenarios still render.
M7. PR description (work/pr-body.md): its SHAs read f61ac3a; expected, the driver updates them after this verdict, not a failure. Content (summary, deliverables, known gaps, images) carried from the description pass at f61ac3a9 (claim 10): the CR patch is unchanged except conflict hunks that kept both sides.
M8. Claims 3, 5, 7, 8 above: carried from f61ac3a9, the move only merged base text around them; the integration test open-at-line (real VS Code) last ran at f61ac3a9 in heavy run 44860936230 and is not re-run at 207a550a (CI heavy not run on this push): stays narrow, as stated in Known gaps.

---

# Description pass at 207a550a (SHA marks)

Head: 207a550a3cbd7e801c02ff26e5ac390f73f97524

D1. Posted body equals work/pr-body.md: VERIFIED at 207a550a. Command: `gh pr view 452 --json body,headRefOid,isDraft,baseRefName` compared to the file in node: headRefOid 207a550a..., isDraft true, base cr-444 branch, bodies equal, no placeholder or STALE mark.
D2. Line 24 (evidence carried to 207a550, visual job green at 207a550), lines 79-82: VERIFIED. Gate pass 20261121-051438.log at 207a550a (M1), `gh pr checks 452` visual/static/report pass (M4), inspector approval of the move at 207a550a in `chantier log` (M5), verdict VERIFIED at 207a550a (M1-M8).
D3. Line 83 (heavy run green at f61ac3a, before the rebase): VERIFIED, true and dated (heavy run 44860936230).
D4. Line 49 Known gaps: FAILED. It says `test/integration/openAtLine.test.ts` "ran in the real VS Code integration job on Linux CI at the head (heavy run 44860936230 ...)". That run is at f61ac3a, not at the head 207a550; M8 states the integration test is not re-run at 207a550. "at the head" is a stale claim. Fix: say "at f61ac3a, before the rebase onto the CR-444 branch (heavy run 44860936230 ...); not re-run at 207a550".

Verdict: NOT VERIFIED (description only; code verdict at 207a550a stands once the line is fixed).

---

# Description pass 2 at 207a550a (after the line 49 fix)

Head: 207a550a3cbd7e801c02ff26e5ac390f73f97524

E1. Posted body equals work/pr-body.md: VERIFIED at 207a550a. Command: `gh pr view 452 --json body -q .body` diffed against the file (CR stripped): identical except one trailing blank line; `gh pr view 452 --json headRefOid` -> 207a550a3cbd7e801c02ff26e5ac390f73f97524. No placeholder, no STALE mark.
E2. Known gaps line 49: VERIFIED. It now says the test ran at `f61ac3a`, before the rebase (heavy run 44860936230, step open-at-line, success), "not re-run at `207a550`", coverage limited to three cases; matches M8 and claim 5. The **UNVERIFIED:** diffs bullet is present; narrow-pane bullet present.
E3. Nothing else changed or stale: VERIFIED. Test plan and line 24 SHAs (207a550 for gate, review, verify, CI; f61ac3a for evidence and heavy run) match `chantier log CR-445` (gate pass at 207a550, "inspector approved at 207a550a...", driver note CI at 207a550) and `gh pr checks 452` (static, static-windows, visual, report, checks pass). Images carried from f61ac3a9 (claim 6, 10); visual job green at 207a550a.

Verdict: VERIFIED at 207a550a.
