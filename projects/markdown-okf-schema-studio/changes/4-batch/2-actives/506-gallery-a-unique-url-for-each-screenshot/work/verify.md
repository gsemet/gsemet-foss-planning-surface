# CR-506 verification (after the restack onto CR-508)

Head: c2f559388dc8fa276a66bc057005eaf1f61726a2

Verdict: VERIFIED

Delta assessment of the move `c715355..c2f5593` (rebase from base `4a47151e` onto CR-508
`09e8acf1`, conflicts in `package.json` and `requirements/tiers/log.md`). Claims the move touched
are judged again at c2f5593; the others are carried from the previous judgment, whose full text
(commands and outputs) is kept in `<folder>/work/verifier/verify-c715355.md`.

`<worktree>` is the CR worktree, `<folder>` the CR folder, logs are in `<folder>/work/gates/`.

## A. Head, base and patch (c2f55938) VERIFIED

- `git rev-parse HEAD`: `c2f559388dc8fa276a66bc057005eaf1f61726a2`; `git ls-remote origin`: the
  same for the change branch, `09e8acf1...` for the CR-508 branch, `4abc9d62...` (unchanged) for
  the `-assets` branch. `git status --porcelain` empty before and after every run below.
- `gh pr view 526`: head c2f5593, base the CR-508 branch at 09e8acf, draft, OPEN, MERGEABLE.
- `git range-diff 4a47151..c715355 09e8acf..c2f5593`: commit 2 `=`; commit 1 differs only in the
  context of `package.json` and `requirements/tiers/log.md`.
- `just check-no-merge-commits 09e8acf1`: `passed (2 commits since 09e8acf1, no merge commit)`.
- `git diff --name-only c715355c c2f55938`: CHANGELOG, `docs/user/wide-tables.md`,
  `package.json`, the log, two LAYOUT-023 requirement files, `src/page/modules/widthMode.ts`,
  three tests (all from the base). `git diff --stat c715355c c2f55938 -- test/site
  CONTRIBUTING.md .github .agents requirements/tiers/swrs/rendering-core requirements/tiers/strs`:
  empty, exit 0.

## B. Merged `package.json`, log and changelog (c2f55938) VERIFIED

- `git diff 09e8acf1..c2f55938 -- package.json`: one line, `test:viewer-graph` gains
  `out/test/site/galleryLinks.browser.test.js`; `test:breakout` is the base's, with
  `codeBlockBreakout.test.js`. Both scripts print so from `node -e "require('./package.json')"`.
- First bytes `7b 0a 20` (`package.json`) and `23 20 55` (log): no byte-order mark. `grep -nE
  "^(<<<<<<<|=======|>>>>>>>)"` on both and CHANGELOG: no match (exit 1).
- Log, `## 2026-11-25`: the CR-506 entry, then the CR-508 entry, both whole; `git diff
  09e8acf1..c2f55938` of the log and CHANGELOG adds lines only (the CR-506 ones).
- `uv run --no-sync python -m pytest test/build/test_workflows.py -q` (the base changed it):
  `81 passed`.

## C. Evidence 1: unit tests (c2f55938) VERIFIED

After the compile of D, `node --test --test-reporter=spec out/test/site/gallery.test.js`
(`verifier-gallery-unit-c2f5593.log`): exit 0, `tests 8, pass 8, fail 0, skipped 0`.

## D. Evidence 2: browser test of the links (c2f55938) VERIFIED

`just ci-viewer-graph` (`verifier-ci-viewer-graph-c2f5593.log`): exit 0, the merged
`test:viewer-graph` command lists the three files, gallery steps 1 to 9 pass, `tests 16, pass 16,
fail 0, skipped 0`, `ci-viewer-graph: passed` (the recipe sets `STUDIO_REQUIRE_CHROMIUM=1`).

## E. Evidence 4: requirements (c2f55938) VERIFIED

- `just requirements-lint` (`verifier-requirements-lint-c2f5593.log`): exit 0, `1227
  requirements, 0 errors, 26 warnings`; `94 StRS checked, all parse`.
- `just requirements-update`: `0 files updated, 0 indexes updated, 0 requirement OKF projections
  updated`; tree clean.
- `git grep -l SwRS-MDOKFSTUDIO-CORE-096`: the requirement, its index, StRS-CORE-008, the log,
  `galleryPage.ts` and the two tests; `git ls-tree -r 09e8acf1 requirements | grep -c CORE-096`:
  0, the id is free at the new base.

## F. Evidence 5: static gate and CI (c2f55938) VERIFIED

- `gh run view 45702562921`: headSha c2f5593, completed, success. `gh pr checks 526`: checks,
  report, static, static-windows, viewer-graph, visual pass; the others skipping.
- Job static-windows 139516174115 log, step `Run just ci-static` (the stage `just preflight` runs
  on Windows): `no unused export in 401 module(s)`, tests `5249 pass 5210 fail 0 skipped 39`,
  `ci-static: passed`.
- `just preflight` and `just check` were not run locally at c2f5593 by this pass (another long run
  was in progress; the brief asked for no heavy run). The local preflight pass stays at c715355
  and is not carried: the description may claim it at c2f5593 only after a run there.

## G. PR description (posted body) carried, one pending update

- `gh pr view 526 --json body` saved as `verifier/pr-body-posted-restack.log`; `diff
  --strip-trailing-cr -B` against `verifier/pr-body-posted-pass2.log` (the copy verified at
  c715355) and against `work/pr-body.md`: exit 0, unchanged. `grep -cE "UNVERIFIED|STALE"`: 0.
- `gh pr diff 526 --name-only`: the same 13 files as at c715355, so Summary, Deliverables,
  Changes, Impacts, Blast radius, Autonomous decisions and Known gaps stay consistent: carried
  from c715355: the CR's patch is unchanged but for merge context.
- The Test plan, the Review box and the image caption still name c715355 and c1037ae. The brief
  gives that update to the stack driver after this pass; not judged a failure here. For it: new
  tests, requirement, `ci-viewer-graph` and CI are proved at c2f5593 above; `just preflight` is
  not (F); the CR log notes `move c715355..c2f5593 (restack) inspector approved at c2f5593`.
- Images: asset branch still at 4abc9d6 (A); the four image proofs are carried from c715355.

## Carried claims

All carried from c715355: `test/site`, the docs of the change and the CR's requirement files are
byte-identical between c715355 and c2f5593 (A), and the base changes (code block width, its
tests, docs and requirement) are not exercised by these proofs.

| Claim (numbers of `verify-c715355.md`) | Judged at |
| --- | --- |
| 2: new tests fail on the previous code (base 4a47151) | c715355 |
| 4: real site from a real CI artifact | c715355 |
| 5: history, title and focus (D6, D8) | c715355 |
| 6: unknown, malformed and markup fragments, escaping (D4, D7) | c715355 |
| 7: cards are links, modified clicks (D5) | c715355 |
| 8: what does not change (D9), before/after captures | c715355 |
| 9: code layout and files changed (D10) | c715355 |
| 10: requirement content and markers (D11), lint figures renewed in E | c715355 |
| 12: review of the pre-move rounds | c715355 |

## Observation

SwRS-MDOKFSTUDIO-CORE-096 is also recorded in the CR log as taken by CR-504's worktree: the
second to land renumbers.
