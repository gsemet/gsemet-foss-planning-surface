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

---

# Move re-judgment at 711a4dd5 (rebase onto CR-444 head 5e42c5f6, scenario headings, glossary line)

Head: 711a4dd5ae9902368cf57ff408f0b03624191355

N1. Long gate pass at the head: VERIFIED at 711a4dd5. `work/gates/20261121-062021.log` first line `gate CR-445 ... head 711a4dd5ae9902368cf57ff408f0b03624191355`, last line `result: pass at 711a4dd5ae9902368cf57ff408f0b03624191355` (`just preflight`; visual, integration, report, gallery skipped on Windows, run by CI).
N2. Delta since 207a550a: `git log 207a550a..711a4dd5` shows the base's CR-444 and site commits plus the CR's commits replayed; the CR-only changes after the last verdict are `467dd197` (8 files, LIFE-178..185 scenario headings, 16 lines) and `711a4dd5` (`.agents/glossary/common.md`, 1 line), per `git show --stat`. Product code unchanged; the gate (N1) re-runs unit, contract and security tests at this head.
N3. CI at the head: VERIFIED. `gh pr checks 452` (run 44870407656): checks, report, static, static-windows, visual pass; others skipping on a PR. `gh pr view 452` headRefOid 711a4dd5ae9902368cf57ff408f0b03624191355.
N4. Review: `chantier log CR-445`: "round 6 inspector APPROVE at 711a4dd5 (glossary Line marker); just check pass"; box says "approved at 711a4dd": matches.
N5. Claims 3, 5, 7, 8 and the evidence images: carried from f61ac3a9/207a550a: the move touched only requirements headings and a glossary line and replayed commits (gate green); the integration test last ran at f61ac3a (heavy run 44860936230), stated as such in Known gaps.
N6. PR description, as posted (`gh pr view 452 --json body,headRefOid,isDraft`), at 711a4dd5: VERIFIED. SHAs: 711a4dd for gate, review, verify, CI; f61ac3a only for evidence and the heavy run, both labelled historical and matching claim 4/5 and N3. Known gaps carries the UNVERIFIED diffs bullet, the narrow-pane bullet and the not-re-run-at-711a4dd integration note. No placeholder, no STALE mark; Mermaid block and fold well formed; internal references only in the folded section. Images: three uploads fetched with `gh auth token` (HTTP 200 image/png), sha256 equal to work/verifier/evidence v04, v10, v11 (opened earlier at claim 6: made-up fixture text, no username or home folder). Summary, Deliverables and Changes match the diff (claims 7, 8).

Verdict: VERIFIED at 711a4dd5.

---

# Description-only pass at df3722061 (clean restack of 711a4dd5 onto CR-444 7635816)

Head: df3722061ad5ea3f06ca047d229edcd8917682ff

D1. Head: `git rev-parse HEAD` in the worktree and `gh pr view 452 --json headRefOid` both give df3722061ad5ea3f06ca047d229edcd8917682ff. `chantier log CR-445` holds a `carry` event at that head (gate_from and verdict_from 711a4dd5).
D2. CI at df37220: `gh pr checks 452` (run 44876601900): checks, report, static, static-windows, viewer-graph, visual pass; others skipping on a PR. Matches the body's "CI green at df37220".
D3. Heavy run claim: `gh run view 44860936230` exists (workflow_dispatch); body states it was before the rebases and not re-run at df37220. Stated honestly; Known gaps repeats it.
D4. Rendering and consistency: body has Summary, Deliverables (Mermaid), Blast radius, Autonomous decisions, Known gaps, folded Details; no STALE mark, no placeholder. Changes list matches `git diff --stat <base>...HEAD` (90 files: openingPolicy, openingWatcher, studioPlacement, migration, introductions, lineMarker, hostToPage, links/history, requirements, docs). Known gaps carries the UNVERIFIED diffs bullet.
D5. Images: three uploads fetched (HTTP 200, PNG 1800x2000), opened: arrow and band on a code line (light), closed dropdown unfolded (dark), edit-mode list with arrow clear of handles (dark). Made-up fixture text, no username, no home folder. They show what the body claims.
D6. Review box: body says "Review: approved at `df37220` (carried from `711a4dd`, move re-inspected)". `chantier log CR-445` has the approved note at 711a4dd5 ("round 6 inspector APPROVE at 711a4dd5") and the earlier "move f61ac3a..207a550 ... inspector approved at 207a550". It has NO note of an inspection of the move to df37220 (the restack note only says "restack: on CR-444 7635816, head df37220"; the move is a `carry`). "move re-inspected" is stated as fact for this head with no proof in the log. FAILED: reword to "approved at 711a4dd, carried to df37220 (clean restack)" or add the re-inspection note.

Verdict: NOT VERIFIED (description, D6 only; all other description claims verified).

## Description-only pass 2 (head df3722061ad5ea3f06ca047d229edcd8917682ff)

Head: df3722061ad5ea3f06ca047d229edcd8917682ff

D7. Review box, re-read at df37220 with `gh pr view 452 --json body`: "Review: approved at `711a4dd`, carried to `df37220` (clean restack)". `chantier log CR-445` has "round 6 inspector APPROVE at 711a4dd5" and the `carry head=df37220 ... verdict_from=711a4dd` event (clean restack). The note names the SHA the box cites: proved.
D8. Rest of the description: unchanged from pass 1 except the box and SHA wording; D1-D5 carried from pass 1 (images fetched HTTP 200 there; unauthenticated curl now gives 403, same upload URLs, body text unchanged). Test-plan lines name df37220 or carry from 711a4dd with the reason; no STALE mark; Known gaps keeps the UNVERIFIED bullet.

Verdict: VERIFIED (description only)
