# CR-516 verification

Head: aeefa1b00c5a6bb0cfbc64e67de3994c3e904053

Base: `origin/main` = merge base = remote `main` = `1953eaaf08b1dcc7c071018abd4b0259acb0020e`.
`<worktree>` is the CR's worktree, `<work>` this folder, `<ev>` = `<work>/verifier/evidence`.
All claims are judged at `aeefa1b0` unless a line says `carried from`.

## Head, gate, CI

- aeefa1b0. `git rev-parse HEAD origin/main; git status --short; git ls-remote origin refs/heads/main refs/heads/chantier/batch-09/cr-516-comment-creation-no-longer-restyles-the-`:
  HEAD and the remote branch `aeefa1b00c5a...`, `origin/main` and remote `main` `1953eaaf08b1...`, status empty (tree clean, also after the cleanup).
- aeefa1b0. Gate pass `<work>/gates/preflight-aeefa1b.log`, first line `head aeefa1b00c5a6bb0cfbc64e67de3994c3e904053`;
  tests 5538, pass 5530, fail 0, skipped 8; `298 passed`; okfreq `1229 requirements, 0 errors, 26 warnings`;
  ends `ci-static: passed`, `preflight: visual, viewer-graph, integration, acceptance, report and gallery stages skipped on Windows; CI runs them`, `exit 0`.
  `handoff CR-516`: `head aeefa1b`, `rounds: 6 of 6`; no long gate in chantier.yaml. No `gate` run by me.
- aeefa1b0. `gh run view 45920567951 --json headSha,conclusion,jobs`: `aeefa1b0 pull_request success`; success: checks, report,
  static, static-windows, viewer-graph, visual, visual-2 (7); skipped: the 10 others (integration, acceptance, stress and perf-547 among them).
- aeefa1b0. `fnm exec -- just check-no-merge-commits`: `passed (4 commits since origin/main, no merge commit)`.

## 1. Restyle test: fails on the old code, passes on the new

- aeefa1b0, new. `STUDIO_REQUIRE_CHROMIUM=1 fnm exec -- node --import ./scripts/register-myst-patches.mjs --test --test-reporter=spec out/test/page/commentRestyle.test.js out/test/page/alignedFloatLayout.test.js out/test/page/frameReadsInChromium.test.js`
  (`<ev>/new-head-chromium.log`): `restyled 26 elements in 7 style passes (largest 20); the page has 3072 elements`; tests 6, pass 6, fail 0, skipped 0.
- 1953eaaf, old (head tests over the base `src/`, 410 files with every blob equal; build in `<ev>/before-after.md`), same command plus
  hoverFrames, scrollSelection, codeCopy, commentCompose (`<ev>/new-tests-on-base-src.log`): tests 64, pass 51, fail 13;
  `AssertionError: one comment creation restyled 3125 elements, more than 100 (passes: 1, 2, 1, 1, 1, 0, 3119)`.
- aeefa1b0. The same numbers in `evidence/local/restyle-test-before.txt` (3125, fail 1) and `-after.txt` (26, pass 1).

## 2. Real VS Code window, three runs before and three after

- Before, 1fc95289 (`git diff 1953eaaf 1fc95289 -- src` empty: base code). `gh run view <id>`: 45895473044, 45895477080, 45896724578:
  `workflow_dispatch success`, perf-547 success, integration, acceptance, stress skipped.
- After, carried from e52cd28: `git diff --stat e52cd28 aeefa1b0` is only `CHANGELOG.md` (3 lines) and
  `test/page/modules/commentCompose.test.ts` (1 deleted blank line), no shipped code. 45918715713, 45918718450, 45918721402: same shape, success.
- aeefa1b0. `gh run download <id> --name perf-547-attempt-1`, then `fnm exec -- node <work>/verifier/runs-check.cjs` (`<ev>/runs-check.log`):
  each of the six JSON copies in `evidence/before` and `evidence/after` is byte-equal to the forge artifact; same document in all
  (464 lines, 22 tables, 197 rows, 11 images, 9 threads before the run, 3114 elements). Medians, before | after:
  - restyled elements 3109, 3109, 3109 | 41, 41, 41
  - comment creation ms 53.4, 51, 53.9 | 47.1, 45.9, 37.1 (no overlap, faster)
  - selection release ms 17.8, 18.45, 17.75 | 18.2, 17.65, 18.05
  - drag text 2.65, 2.46, 2.66 | 2.72, 2.68, 2.62; drag cells 2.64, 2.62, 2.69 | 2.54, 3.4, 2.71
  - release text 2.28, 2.41, 2.17 | 2.41, 2.55, 2.92; release cells 2.62, 2.79, 2.6 | 2.73, 2.92, 2.91
  The PR table and `evidence/after/runs.md` give these values; the overlapping or touching sets read "not separable". No set is slower beyond the spread.
- aeefa1b0. Item 4 of the specification not triggered: largest drag or release sample before 12.26 ms (< 50 ms); after 4.9 ms.
- aeefa1b0. Heavy real-window run (integration, acceptance, stress): NOT RUN at this head and not claimed. Deferred to the last commit
  of the final stack by the user's night order (`02-answers.md` item 6, "fini par une pipeline long uniquement sur le dernier commit"; O-200).
  The PR's Known gaps says so. I dispatched no run.
- 1fc95289. A further dispatch, 45895468941, failed in perf-547 on `ETIMEDOUT` while resolving VS Code (`<work>/ci-45895468941-job.log`); not one of the three.

## 3. Layout unchanged, with and without an aligned float, switching, exported file

- aeefa1b0 against 1953eaaf. `fnm exec -- node --import ./scripts/register-myst-patches.mjs <work>/verifier/layout-compare.cjs <work>/scratch/<new folder>`
  (`<ev>/layout-old-new.log`, exit 0): 23 documents (none; image, figure, table right, left, centre; list table; raw HTML align and class
  variants; nested; float first and last), widths 900 and 420, on the page without script, the exported file, the runtime page, content
  patches walking all documents and runtime DOM changes: `256 comparisons, 0 with a difference`, no page error in either build.
  Compared: `::before`, clear, float, display, element rectangles, height. Mark present exactly with an aligned float.
- aeefa1b0. The new layout tests (page and export without script; first float added, last removed) pass, see 1.
- aeefa1b0. `git grep -nE '(#sphinx-myst-preview-content|\$\{CONTENT\})(:not\()?(\)?):has\(' HEAD -- src`: exit 1, no match; the same on
  `origin/main` finds 3 (contentBlockStyles.ts:19, contentLayoutStyles.ts:67 and :76).

## 4. Button, copy button, outline, scroll unchanged apart from once per frame; shortcut before the frame

- aeefa1b0 against 1953eaaf. `... <work>/verifier/behaviour-compare.cjs <work>/scratch/<new folder>` (`<ev>/behaviour-old-new.log`, exit 0):
  real mouse drag, wheel and keyboard, 31 steps, 3 passes (Comment button place, quote, shortcut in the same task as a new selection and
  right after its announcement, removed selection, click, copy button, hover outline, reported selection):
  `93 step comparisons, 0 with a difference`, no page error.
- aeefa1b0. `... --test out/test/page/hoverFrames.test.js out/test/page/scrollSelection.test.js out/test/page/modules/codeCopy.test.js out/test/page/modules/commentCompose.test.js out/test/page/modules/commentEditorBehaviour.test.js out/test/core/preview/alignedFloat.test.js out/test/page/linkEditModeClick.test.js`
  (`<ev>/new-head-unit.log`): tests 95, pass 95, fail 0, skipped 0.
- 1953eaaf. The 13 failures of the old build are the new behaviour only: 2 layout (mark), 1 restyle, once-per-frame selection, scroll,
  reread after a page change, hover outline (2), copy button (3), offset-0 search, scroll report text. The unchanged-behaviour tests pass
  there, the shortcut-before-frame test included. Edits to older tests add frame flushes and waits; no assertion is weakened.
- aeefa1b0. `STUDIO_REQUIRE_CHROMIUM=1 fnm exec -- npm run test:breakout` (`<ev>/head-test-breakout.log`): tests 20, pass 20, fail 0, skipped 0.

## 5. Requirements, perf-547 job, how-we-test, CHANGELOG

- aeefa1b0. `git diff origin/main HEAD -- requirements/tiers/strs`: one StRS file, 2 added lines, both the generated `derived_by` entry and
  link for SwRS REVIEW-223 (REVIEW-003 stays `req_lifecycle: approved`, text and approval unchanged): no StRS is changed in meaning.
- aeefa1b0. Changed SwRS BLOCK-017, CODE-017, LAYOUT-043, LIFE-108, CORE-076, REVIEW-038, REVIEW-049 and new REVIEW-223: all
  `req_lifecycle: proposed`. `requirements/tiers/log.md`, 2026-11-26, section "Comment creation no longer restyles the whole document".
- aeefa1b0. `git grep` finds `@tests_req` for REVIEW-223#S1, REVIEW-038#S7-S10, CODE-017#S10, BLOCK-017#S8, LIFE-108#S11,
  LAYOUT-043#S6-S8 and `@implements_req` in src for REVIEW-223, REVIEW-038, REVIEW-049, CODE-017, BLOCK-017, LIFE-108, LAYOUT-043.
- aeefa1b0. `uv run --no-sync --group requirements okfreq validate`: exit 0 (`1229 requirements, 0 errors, 26 warnings`, as in the gate log).
- aeefa1b0. `ci.yml`: input `perf_547` (line 41), job `perf-547` (line 545) `if: ... github.event_name == 'workflow_dispatch' && inputs.perf_547`,
  job timeout 5, step timeout 4, hang dump, artifact `perf-547-attempt-<n>`, in no job's `needs`; skipped in the pull_request run.
  `justfile:475` `ci-perf-547`, "sets no limit"; `test/integration/perf547.ts` writes samples and medians to `out/reports/probe/perf-547.json`;
  rule 13 paragraph at `ci.guidelines.md:114-116`; listed in `docs/how-we-test.md:196-199`; also CONTRIBUTING.md.
- aeefa1b0. `uv run --no-sync python -m pytest test/build/test_workflows.py -q`: `111 passed`.
- aeefa1b0. `git diff origin/main HEAD -- CHANGELOG.md`: one user-facing entry ending `(CR-516 comment-restyle, PR #549, issue #547)`.

## 6. Pull request 549 and issue 547

- aeefa1b0. `gh pr view 549`: OPEN, draft, base main, head aeefa1b0, title `fix(render): save a comment without restyling a whole large document`,
  closing references 0, comments 0, reviews 0. `gh issue view 547`: OPEN, comments 0, closing pull requests 0. No closing keyword in the
  title, body or the four commit messages (96331f0f, 1fc95289, e52cd28a, aeefa1b0); the changelog line references the issue. Body unchanged
  since my full read (`diff` exit 0).
- aeefa1b0. Impacts and Test plan hold: no visual change (3), table and run links (2), gate numbers (gate log), 7 CI checks, 11 SVG images
  (`perf547Document.ts`), mermaid block draws (`mermaid-check.cjs`: 6 nodes, 7 links), job time limits and the unthrottled pointer-move
  listener as described. Known gaps names both missing runs. No image, no stale mark, no role name as doer. "Review: approved at aeefa1b"
  matches the notes of `handoff` (approved on e52cd28, committed as aeefa1b0).
- aeefa1b0. "20 of 20 browser tests": rerun, 20/20 (4).
- carried from e52cd28: the other carried local claims of the Test plan, read in the earlier rounds' logs, not rerun by me (run on the
  uncommitted tree later committed as e52cd28; no later change to shipped code): `evidence/local/r4-stability.txt` (10 of 10 alone, and
  beside `just check`), `r5-visual-stage.txt` (524 passed, 6 failed), `visual-stage.txt` (the same 6 fail on the unchanged head).
- aeefa1b0. The PR says the comment shortcut test was not run on the previous code; my run in 4 shows it passes there, which does not contradict it.

## Housekeeping

- Removed: `<worktree>/out/vbase`, my scratch probe folders and one partial log of a first probe run. Kept: the downloaded artifacts under
  `<work>/scratch/artifacts-<run id>-verifier`. No removal was refused.
- A first layout probe run hung (no animation frame in a page without script) and stayed as my background shell; I did not stop a process;
  the host ends it with this run. Its fixed rerun is the cited log.
- No home path or user name in `<work>/verifier` (searched before writing).

VERIFIED
