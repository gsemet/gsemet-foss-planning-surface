# Verify CR-517 "A comment updates only its highlights and does not wait for Git (issue 547)", PR #550

Head: 44a2e9365a238ba8cd813dece5645b66665551e3
Base: aeefa1b00c5a6bb0cfbc64e67de3994c3e904053 (branch of the lower CR, PR #549, open draft)
Judged: 2026-11-27, batch-09. No earlier verify.md.

Notation: `<W>` the CR worktree, `<F>` the CR folder, `<L>` = `<F>/work/verifier` (my scripts),
`<E>` = `<L>/evidence` (saved outputs, user name removed), `<B>` = `aeefa1b00c5a6bb0cfbc64e67de3994c3e904053`.
Commands ran from `<W>`. Every claim is judged at 44a2e93 unless it says `carried from`.

Result: every "Done when" item holds, except the heavy CI run of the head, which has not run and is
covered later by owner order (see Gaps).

## 1. Head, base and pull request (44a2e93)

- `git rev-parse HEAD` -> `44a2e9365a238ba8cd813dece5645b66665551e3`; `git status --short --branch` -> branch line only
  (clean); `git ls-remote origin refs/heads/chantier/batch-09/cr-517-a-comment-updates-only-its-highlights-an`
  -> same SHA.
- `gh pr view 550 --json state,isDraft,mergeable,headRefOid,baseRefName,title,closingIssuesReferences` -> OPEN,
  isDraft true, MERGEABLE, headRefOid 44a2e93, base `chantier/batch-09/cr-516-...`, title
  "fix(render): redraw only the comment marks that changed", closingIssuesReferences [].
- `gh pr view 549 --json state,isDraft,headRefOid` -> OPEN, draft, headRefOid `<B>`.
- `git rev-list --merges --count aeefa1b0..HEAD` -> 0; `fnm exec -- just check-no-merge-commits <B>` ->
  "check-no-merge-commits: passed (3 commits since <B>, no merge commit)".
- `git log <B>..HEAD` -> 7d24547 "ci: measure the Git name wait and the comment thread index", 6c099bf
  "fix(render): redraw only the comment marks that changed", 44a2e93 "fix(render): measure again when a
  comment mark can move a block"; trailer of each: `Assisted-by: Claude:Sonnet-5.5`.
- `git diff --stat <B>..HEAD` -> 31 files changed, 1438 insertions(+), 338 deletions(-).

## 2. Gate: `just preflight` passed at the head (Done when, first half) (44a2e93)

- `<F>/work/gates/preflight-44a2e93.log`, first line: `head 44a2e9365a238ba8cd813dece5645b66665551e3 fnm exec -- just preflight, STUDIO_REQUIRE_CHROMIUM=1, Windows, started 2026-11-27T06:32:19+01:00`.
- Its end: "ci-static: passed", "preflight: visual, viewer-graph, integration, acceptance, report and gallery
  stages skipped on Windows; CI runs them", "exit 0", "head after 44a2e93...", "status done".
- Inside: node 56/56; 5568 tests, 5560 pass, 0 fail, 8 skipped (4 hang-watchdog `ps` tests, 3 POSIX process
  group tests, 1 without a requirements report); 116/116; pytest "298 passed" and "4 passed"; requirements
  "0 indexes would change", "0 files would change", errors 0.
- `chantier ... handoff CR-517 --batch batch-09` notes: "before second push at 44a2e93: fnm exec -- just
  preflight (STUDIO_REQUIRE_CHROMIUM=1, Windows static stage, includes just check): pass", "CI at 44a2e93:
  green (PR run 45947061700 ...)", "r4 approved at 6c099bf... committed as 44a2e93...", "r4 body re-inspection
  approved at 44a2e93...".

## 3. CI of the head (44a2e93)

- `gh pr checks 550` -> run 45947061700: static, static-windows, visual, visual-2, viewer-graph, report, checks
  pass; integration, acceptance, stress, perf-547, toc-loop, gallery, pages and release jobs skipping.
- `gh run list --branch <branch>` -> 45947061700 pull_request success @44a2e93; 45947065460, 45947068376,
  45947071021 workflow_dispatch success @44a2e93; 45928962519, 45928965278, 45928968671 workflow_dispatch
  success @7d24547.
- `gh run view <id> --json jobs` on the six dispatches and 45947061700 -> integration, acceptance and stress
  "skipped" in each; the dispatches ran perf-547 "success". No heavy run exists at this head. I dispatched none.

## 4. My own test run at the head (44a2e93)

- `fnm exec -- npm.cmd run compile` -> exit 0 (`<E>/compile.log`).
- `STUDIO_REQUIRE_CHROMIUM=1 fnm exec -- node scripts/node-test.mjs verifier517 <commentThreadsUpdate,
  commentRestyle, page/modules/comment*, build/perf547ThreadIndex, session/reviewReq*, commentAuthorResource,
  headBaselineUserName, core/preview/commentStyles, runtimeCommentsHidden, runtimeContentPatch,
  core/comments/*>` -> tests 281, pass 281, fail 0, skipped 0 (`<E>/tests-head.log`).

## 5. Done when: one added comment leaves the other highlights in place and reads `[data-line]` once (44a2e93)

- `<E>/update-tests-head.log` (esbuild bundle of `commentThreadsUpdate.test.ts`, head sources, `node --test`)
  -> tests 25, pass 25, including "adding one comment keeps the elements of the other threads and reads the
  mapped blocks once" (asserts reads == 1, same elements, same parents, no attribute written, other blocks keep
  their nodes) and "a reply, a resolve and a delete keep the elements of the threads that did not change".
- The same head test bundled against `<B>` sources (`git archive <B> src test/probe/perf547Document.ts` into
  `<L>/base-tree`) -> tests 25, pass 21, fail 4: the two above ("10 !== 1" reads on the first) and "the host's
  threads do not measure the page when no block can have moved", shown and hidden ("1 !== 0")
  (`<E>/update-tests-base.log`). So the tests tell the old behaviour from the new one, and the PR's "25 tests;
  on the previous code 4 of them fail ... the 21 others" is exact.

## 6. Done when: in-place page equals the page from nothing; Fix 2, same result as today (44a2e93)

- The repository test compares the whole page dump (tags, attributes, every text node) after each list with a
  fresh page: named sequences (overlapping quotes, orphans, an orphan resolved, badge/highlight changes) and
  250 seeded random runs of 14 steps with create, delete, resolve, reply, re-anchor, reorder and hide
  (`test/page/modules/commentThreadsUpdate.test.ts` l.182-254, read); all pass in section 5 (fake DOM).
- My own differential, base comment module against head module (esbuild iife of each `commentThreads.ts`),
  same random thread lists on real renders in headless Chromium 156.0.8078.4, page scripts removed; DOM with
  text node boundaries, draft, popover and trace compared after each step:
  `RUNS=14 STEPS=40 SEED=517547 fnm exec -- node --import ./scripts/register-myst-patches.mjs <L>/differential.cjs <L>/ct-base.js <L>/ct-head.js`
  (rich, perf547, README, CONTRIBUTING; widths 420, 900) -> lists 5481, mismatches 0, popoverLists 1378,
  hiddenLists 1783, applies 136, maxMarks 10, maxBadges 9, maxOrphans 6; exit 0 (`<E>/differential.log`).
- With block replacement steps (content patch then `apply()`): `RUNS=7 STEPS=40 SEED=44936 ...
  <L>/differential-patch.cjs ...` (rich, readme, contributing) -> lists 2008, patches 375, mismatches 0
  (`<E>/differential-patch.log`).
- Sensitivity: a head bundle with `updateOrphans` skipped -> 6 mismatches reported; one whose `setThreads`
  answers false -> 4 "missed move" reported (`<E>/differential-mutants.log`).

## 7. Fix 1: the measure runs only when a block can have moved (44a2e93)

- `git diff <B>..HEAD -- src/page/features/hostHandlers.ts` ->
  `if (parts.commentThreads.setThreads(message.threads)) rt.scroll.measure();`. `contentPatch.ts` still calls
  `commentThreads.apply()` then `measure()` (read).
- Soundness in real layout, same two runs: any geometry change of a mapped block or of one of its text line
  tops while `setThreads` answered false counts as missed: geometryMoved 77 and 36, missed 0 in both. The
  mutant of section 6 shows the check detects a miss.
- Repository tests S4 and S5 (measure on highlight or badge changes, none otherwise; shown and hidden) pass.

## 8. Done when: the lower CR's restyle test still passes (44a2e93)

- `git diff --stat <B>..HEAD` lists no `test/page/commentRestyle.test.ts` (unchanged). In my run it passes:
  "restyled 8 elements in 7 style passes (largest 2); the page has 3072 elements"; same line at
  `preflight-44a2e93.log` l.2626.

## 9. Done when: `threadIndex` for both documents, beside `commentCreate`, and the user actions (44a2e93)

- `gh run download <id> --name perf-547-attempt-1` then `node <L>/medians.cjs` (`<E>/evidence-medians.log`):
  published copies in `<F>/evidence/after/` identical to the artifacts. Medians (ms, 9 samples each, node
  v24.22.3), runs 45947065460 / 45947068376 / 45947071021:
  issue-size (464 lines, 64579 bytes, 9 threads) index 1.41 / 1.41 / 1.04, reanchor 1.96 / 1.74 / 1.35;
  four-times (1856 lines, 261223 bytes, 36 threads) index 5.62 / 5.48 / 4.20, reanchor 8.94 / 8.35 / 6.37;
  commentCreate 32.4 / 35.4 / 23.7. Recomputed medians equal the reported ones; the PR table matches.
- `<F>/evidence/after/runs.md` l.51-84 holds the same table and the user-action list; the PR body holds both.
- Read in code: `grep -rn "createDocumentIndex\|reanchorThreads" src` -> outside `core/comments/anchoring.ts`
  only `src/session/features/comments.ts` (l.211, 233, 340, 347). I followed their callers: the PR's table of
  user actions matches.

## 10. Fix 4: report only, default generator output unchanged (44a2e93)

- `fnm exec -- node <L>/generator.cjs <base perf547Document bundle>` -> `perf547Document()` and
  `perf547Document(1)`: 13 files identical to base (names, order, bytes) true; report.md 64579 bytes sha
  bea73f28631d98b4; all-files digest f1c010b1cce9f1a4 on both; scale 1: 464 lines, 22 tables, 21 blockquotes,
  11 images, 9 threads; scale 4: 1856, 88, 84, 44, 36 (`<E>/generator.log`).
- `fnm exec -- node out/test/probe/perf547ThreadIndex.js <copy of a report>` -> exit 0, issue-size index 1.09
  reanchor 1.30, four-times 4.30 / 6.66 (`<E>/thread-index-local.log`); with a missing report -> ENOENT, exit 1.
- The justfile diff appends that step to `ci-perf-547`; its asserts check validity (sidecar errors, thread and
  orphan counts, report scenario), no time limit (`grep -n "assert\|limit" test/probe/perf547ThreadIndex.ts`
  and the file's header "It sets no limit").
- `git diff --stat <B>..HEAD -- src/core src/node-services src/host-api` -> only
  `src/core/preview/styles/commentStyles.ts`, whose diff is a CSS comment: indexing, anchoring and storage
  are unchanged.

## 11. Done when: the three runs against the lower CR's three "after" runs (44a2e93)

- `<L>/medians.cjs` on nine artifacts (head; 7d24547; lower CR 45918715713, 45918718450, 45918721402 at
  e52cd28, whose difference to `<B>` is one docs commit: `git diff --stat e52cd28 <B>` -> CHANGELOG.md and one
  removed test line). Environment of all: VS Code 1.148.0 linux, 671x799, 3114 elements, 464 lines, 9 to 21
  threads; head and 7d24547 folders are Git repositories with user "Lorem Reviewer", the lower CR's are not.

| ms (median per run) | head | lower CR | 7d24547 |
|---|---|---|---|
| commentCreate | 32.4 / 35.4 / 23.7 | 47.1 / 45.9 / 37.1 | 46.6 / 35.2 / 35.5 |
| selectionRelease | 16.9 / 16.65 / 3.6 | 18.2 / 17.65 / 18.05 | 17.45 / 17.8 / 18.05 |
| dragText longest task | 2.16 / 2.29 / 1.92 | 2.72 / 2.68 / 2.62 | 2.97 / 2.30 / 1.95 |
| dragCells longest task | 2.22 / 2.18 / 1.87 | 2.54 / 3.40 / 2.71 | 2.81 / 2.09 / 2.41 |
| releaseText longest task | 2.21 / 1.98 / 1.98 | 2.41 / 2.55 / 2.92 | 2.33 / 2.19 / 2.21 |
| releaseCells longest task | 2.28 / 2.44 / 2.10 | 2.73 / 2.92 / 2.91 | 2.68 / 2.48 / 2.32 |
| restyled elements | 4 / 4 / 4 | 41 / 41 / 41 | 41 / 41 / 41 |

  Every figure of the PR table and of `runs.md` matches. No median of runs of the head is above either compared
  set. selectionRelease samples cluster near 4 and 17 ms (head near4/near17 5/9, 4/10, 12/2). The largest drag
  or release long task of the head is 9.21 ms, so "no drag or release blocks for 50 ms" holds. "Against #549,
  comment creation and the four longest tasks are lower in every run" holds. "Not separable from runner noise"
  is said as such.

## 12. Fix 3 and "if the author wait is changed": nothing changed, and rightly (44a2e93)

- `git diff <B>..HEAD -- src/session` -> only `timedGitName` (times `host.vcs.userName`, keeps 50 samples on
  the probe as `authorWaitsMs`) and that probe field; `resolveAuthor` order unchanged, no cache.
- `<E>/evidence-medians.log`: head run medians 6.78 / 9.83 / 8.79, median of runs 8.79, pooled 36 samples 8.32
  (9 above 10 ms). 7d24547, on which the decision was taken: 10.74 / 8.69 / 6.79, median of runs 8.69, pooled
  9.635 (16 above 10 ms). All 12 samples of each run are listed in the PR body (head) and match.
- Judgment: the median is at or under 10 ms under both readings (median of run medians, pooled median), so
  "change nothing for the author and say so with the figures" applies; the PR says so, including that one
  7d24547 run measured 10.74 ms. The author tests of "Done when" and a change of REVIEW-065 do not apply. The
  pooled margin at 7d24547 is small (about 0.37 ms).

## 13. Done when: requirements (44a2e93)

- `git diff --name-only <B>..HEAD -- requirements` -> log.md, StRS REVIEW-001 and 003, SwRS REVIEW-017, 028,
  224 (new), SwRS index. `git diff <B>..HEAD -- requirements/tiers/strs` -> each StRS gains only the
  `derived_by` entry and the generated link to REVIEW-224: no StRS text changes.
- REVIEW-224 (proposed, derives StRS-REVIEW-001/003, scenarios S1 to S5) names `hostHandlers.ts` and
  `commentPlacements.ts` and the new test (read). `grep -rn SwRS-MDOKFSTUDIO-REVIEW-224 src test` ->
  `hostHandlers.ts:57`, `commentPlacements.ts:292`, `commentThreadsUpdate.test.ts` S1 to S5.
- `git for-each-ref` over `refs/heads` and `refs/remotes/origin` with `git ls-tree -r --name-only <ref> -- requirements`,
  and a look for the file in the sibling worktrees of `git worktree list`: REVIEW-224 exists on this branch only.
- Requirements lint and no pending update: section 2.

## 14. Done when: issue 547 referenced and not closed, nothing posted (44a2e93)

- PR body: "Part of https://github.com/gsemet/markdown-okf-schema-studio/issues/547", no closing keyword;
  closingIssuesReferences [] (section 1). The runs do not show both symptoms fixed (comment creation not
  separable from noise), and the body says why it does not close.
- `gh issue view 547 --json state,updatedAt,comments` -> OPEN, updatedAt 2026-11-26T15:23:55Z, 0 comments.

## 15. Other changed tests and files (44a2e93)

- `test/build/test_workflows.py`: the assertion is stricter (old command string plus
  `&& node out/test/probe/perf547ThreadIndex.js; then`, plus an is-file check).
- `test/core/preview/commentStyles.test.ts`: only the pinned length and digest (24826 to 24971 bytes), name and
  comment, for the corrected CSS comment; the PR body says so.
- CHANGELOG: one line under Unreleased, ending "(CR-517 perf-547-comment-update-and-author, PR #550, issue #547)".

## 16. PR description (44a2e93)

- `gh pr view 550 --json body` equals `<F>/work/pr-body.md` (trailing newline aside) and is unchanged at the end
  of this verification.
- `fnm exec -- node <L>/mermaid.cjs <L>/pr550-body.live.md` -> "diagram 1 of 1 rendered {"nodes":5,"edges":4}"
  (`<E>/mermaid.log`). The body carries no image.
- External reader, Deliverables, Impacts ("No visual change" with its reason), Autonomous decisions, Known gaps,
  draft rules: checked against `.agents/guidelines/pull-request.guidelines.md`; CR id only under Internal
  references; no stale mark.
- "Before: removed and created again, one or two reads per thread, measure every time": base test run of
  section 5 (10 reads for 9 threads, measure after an update that moves nothing) and the base code (read).
- Known gap, three lagging descriptions: confirmed at `commentStyles.ts:768` ("output is unchanged"),
  `commentThreads.ts:77` ("again from nothing") and the repeat-apply criterion of REVIEW-017 (read).
- Known gap, text nodes side by side, "the page code before this change does the same": hand-made page,
  `fnm exec -- node <L>/touching.cjs <L>/ct-base.js <L>/ct-head.js` -> in "highlight ends at the boundary, then a
  quote crosses it", list 3 DIFFERS from fresh identically for base and head (in place highlights "charlie",
  fresh shows a badge); every other list equals fresh for both (`<E>/touching.log`).
- "No rendered page checked holds such nodes": `... <L>/adjacent.cjs` on 20 static renders (rich, perf547,
  README, CONTRIBUTING, a 20000-word paragraph with a 128889-character text node, docs/*.md) -> pairs 0 in every
  one (`<E>/adjacent.log`; page scripts did not run).
- Autonomous decision "a highlight moved a list block by 4.19 px while the content size did not change":
  carried from 6c099bf: it states how the browser lays out a highlight, which the later commit 44a2e93 (measure
  after every added or removed highlight) does not change, and I did not rerun this probe.
  `<F>/evidence/local/moves-short-highlights-6c099bf.log`: "NOT MEASURED, highlight "after" L9, content size
  unchanged: ul.okf-html-block L9: height 4.19; p L14: top 4.19"; `moves-shortmarks-fix-r3.log` beside it:
  unmeasured 0 with the fix. My own soundness check at the head (section 7) found no missed move.

## Owner watch: review comment threads

Nothing to add beyond the PR body (index costs and the actions that run the index). Nothing disabled, no
storage changed.

## Conflicts to report (not failures)

- `pull-request.guidelines.md` l.107 ("GitHub issues") says the Summary ends with `Fixes #N`; the specification
  says close by keyword only if both symptoms are fixed or absent, and the PR says "Part of" instead. The PR
  follows the specification.
- `02-answers.md` item 7 (order O-204, shown by `handoff` at about 07:20) replaces item 6 / O-201 of my task: one heavy run
  at this CR's final head once verified, then PR #549 and #550 leave draft. The PR's Known gaps bullet "The real
  VS Code integration and acceptance jobs do not run at this pull request's head: they run once, at the last
  commit of the stack" was written under item 6. No heavy run exists at the head today, so it states no false
  result, but it must be rewritten with that run's outcome before the PR leaves draft.

## Gaps

- "A heavy CI run of the head is green": NOT PROVEN, no such run exists. Covered later by owner order (O-201 in
  my task: the stack's last commit; O-204 / item 7 now: this CR's final head after this verdict). I dispatched
  none. Real VS Code integration and acceptance have not run at this head.
- No VS Code window on this machine: real-window behaviour rests on the perf-547 runs (timings only).
- My differential and soundness checks run the comment module alone on real renders (page scripts removed).
- The author threshold: one 7d24547 run alone is above 10 ms (10.74); pooled 9.64.
- Older Chromium builds (older VS Code releases) not checked; the r4 coder's attempt was refused (text in
  `<F>/work/coder/r4.md`). I downloaded nothing and did not retry.
- `threadIndex` is plain Node, every thread anchoring at its stored place (as the PR's Known gaps says).

## Refused command, and files left behind

One command of mine was refused; it was not retried or rewritten, and nothing in it ran (its merge check was
run alone afterwards, section 1). User name replaced by `<user>`; otherwise exact:

```text
F="C:/Users/<user>/Projets/gsemet-foss-planning-surface/projects/markdown-okf-schema-studio/changes/4-batch/2-actives/517-perf-547-comment-update-and-author"; L="$F/work/verifier"; W="C:/Users/<user>/Projets/markdown-okf-schema-studio.worktrees/batch-09-CR-517"; cd "$W" && echo "merges in aeefa1b0..HEAD: $(git rev-list --merges --count aeefa1b0..HEAD)"; fnm exec -- just check-no-merge-commits aeefa1b00c5a6bb0cfbc64e67de3994c3e904053 2>&1 | tail -3; rm -rf "$L/base-tree" "$L/ct-base.js" "$L/ct-head.js" "$L/perf547Document.base.cjs" "$L/update-base.test.cjs" "$L/update-head.test.cjs" "$W/out/reports/verifier517"; rm "$L"/*.log; ls "$L" "$L/evidence"; git status --short
```

```text
Permission for this command was denied by a built-in Claude Code safety check, not by the user. The check stops removals that can delete far more than intended: a system, home or workspace directory, or a target it cannot resolve, such as a shell variable that, if unset or empty, turns this into `rm -rf /` or `rm -rf /*`. Only a person may approve such a removal, and no person did (the permission prompt timed out, or none was shown). The command was NOT run; do not claim it succeeded. Do not work around the check by splitting, scripting, or re-issuing the removal through another tool or shell: the check exists because a removal like this can destroy the user's data, and getting past it would not make it safe. If the text below suggests a safe rewrite, run that instead; it goes through the same check. Otherwise finish the rest of the task without this removal, tell the user what you wanted to delete and why, and leave the removal to them. What was flagged: Dangerous rm operation detected in `rm "$L"/*.log`. The target '"$L"/*.log' is a shell variable expansion: when $L is unset or empty it becomes `/`, `/*` or a top-level path. This requires explicit approval and cannot be auto-allowed by permission rules.

This check does not fire on a target that cannot expand to the filesystem root: rewrite it as `"${L:?}"/*.log`, which makes the shell stop with an error instead of running rm when $L is unset or empty, or use a literal absolute path.
```

It was meant to remove only files I made (build outputs and the first copies of the logs). They remain, for the
owner to delete if wanted: `<L>/base-tree/`, `<L>/ct-base.js`, `<L>/ct-head.js`, `<L>/perf547Document.base.cjs`,
`<L>/update-base.test.cjs`, `<L>/update-head.test.cjs`, `<L>/*.log`, `<W>/out/reports/verifier517/` (ignored by
git). One of those logs, `<L>/update-tests-base.log` (ignored by git), named the home folder; I replaced that
text in place with `<home>`. No file of `<L>` outside `base-tree/` holds the user name after that
(`grep -r -I -l -i <user>` -> no match; `base-tree/` -> 0 files).

VERIFIED
