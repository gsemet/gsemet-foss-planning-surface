# CR-507 verification

Head: 6c5106e4589592002f828b6feb3d545a442591aa

Base: 4e4eeb4eb548fc4a8f05838f6d0257b76d6b9f0e. PR: https://github.com/gsemet/markdown-okf-schema-studio/pull/543 (open, draft).
`<W>` is the CR worktree, `<F>` the CR folder, `<V>` is `<F>/work/verifier` (logs named below are there).
Every claim is judged at `6c5106e` unless it says otherwise. Nothing is carried from an earlier judgment.

Result: the change does what the specification says (evidence items 1 to 5, and item 6's list of
differences). The posted PR description fails on three points (claims P1 to P3).

## Head and scope

### C0. Head, tree, base and scope

- `git rev-parse HEAD`, `git status --porcelain`: `6c5106e4589592002f828b6feb3d545a442591aa`, empty.
- `gh pr view 543`: head `6c5106e...`, base `chantier/batch-09/cr-514-...`, draft, OPEN, updated 2026-11-26T14:44:12Z.
- `git rev-parse <rev>^{tree}`: HEAD and `166532f4` are both `e9e12e6af08cd9ca108c9cbb7f369b67e2220d27`;
  base `4e4eeb4` and `a5550c32` are both `43825577ca55366cfb0fac9a2596b99ca1744dd8`.
- `git log --oneline 4e4eeb4..HEAD`: `35cd6384` (the page), `6c5106e4` (both visual jobs).
- `git diff --shortstat 4e4eeb4..HEAD`: `17 files changed, 643 insertions(+), 23 deletions(-)`: docs, one SVG,
  guidelines, glossary, requirements (CORE-086, its index, `log.md` +4/-0), `test/site/`.
- Unchanged: `git diff --stat 4e4eeb4..HEAD -- src justfile package.json package-lock.json uv.lock .github
  requirements/config.yml CHANGELOG.md skills README.md AGENTS.md` prints nothing.

## Evidence items of the specification

### E1a. `just check` passes with the new and changed tests

- Long gate cited: `<F>/work/gates/preflight-6c5106e.log`, first line `CR-507
  chantier/batch-09/cr-507-how-we-test-a-docs-page-linking-test-lev 6c5106e4589592002f828b6feb3d545a442591aa just preflight`.
  `$CHANTIER handoff CR-507`: long gate "none in chantier.yaml"; its "PR head" still reads `fb5fb2f` (no
  ship recorded at this head, see the `ship` refusal in P3).
- In that log: `check-no-merge-commits: passed`; `check-boundaries: passed (408 modules)`; `check-limits:
  passed (1383 files...)`; `check-markers: ... 459 in-force SwRS marked`; clip kit 56/56; unit `tests 5443,
  pass 5435, fail 0, skipped 8`; security 116/116; `296 passed`; `ci-static: passed`; last line `preflight
  exit 0 at 6c5106e4589592002f828b6feb3d545a442591aa`.
- Own run: `just compile` (exit 0), then `node scripts/node-test.mjs unit` on the compiled `howWeTest`,
  `siteLinks`, `siteTheme`, `socialCard`, `requirementsViewer/pages` tests: `tests 49, pass 49, fail 0,
  skipped 0` (`head-compile.log`, `head-five-files.log`).

### E1b. On the code without the change, the drift test and the new header and card assertions fail

- Judged at base `4e4eeb4` in a detached worktree (since removed): the five test files of the head copied on
  the base, `npm run compile` (exit 0), the same test command: `tests 49, pass 36, fail 13, skipped 0`
  (`base-five-files.log`).
- Nine drift checks on shipped files fail (`ENOENT`, no page; the diagram check, no SVG): relative links and
  images; test folders; CI jobs; e2e groups; marker verbs; coverage mode; acceptance groups;
  `just requirements-lint` commands; diagram title, description and alternative text.
- Four more: "the site header links How we ship then How we test from root and nested pages"; "a viewer page
  brands and links the site relative to its own folder"; "a main page and a viewer page carry the same brand
  and the six links..."; "SIMPLE_CARDS covers the home, Contributing, How we ship and How we test pages".
- The figure "13 of 49" of the PR body therefore holds at this base; the coder's
  `work/gates/parent-tests.log` shows the same counts.

### E2. `just requirements-lint` passes

- `just requirements-lint` (`head-requirements-lint.log`): `1228 requirements, 0 errors, 26 warnings`;
  `0 indexes would change`; `0 requirement OKF projections would change`; `0 files would change`;
  `main paths: 96 StRS checked, 625 SwRS citations, all valid`; `use case diagrams: 94 StRS checked, all parse`.

### E3. The site builds, with the page, the headers, the manifest and the picture

- `just site-assemble` alone is refused here (`head-site-assemble.log`): `Error: Cannot curate E2E gallery:
  the final review report is missing`, `recipe site-assemble failed on line 271 with exit code 1`.
- `just site-from-run 45830014522` (`head-site-from-run.log`): `Built static site at <W>\out\site`, `exit 0`.
  `gh run view 45830014522`: `workflow_dispatch`, `cd3b8e6a8f02...`, `success`. That commit is not an
  ancestor of the head; its tree `e6f6894de333c24969709306715c4f3c06d06418` is the tree of `223a8c49`, which is.
- The 40 tracked pictures under `images/` were backed up and copied back: `cmp images-before.sha256
  images-after.sha256` identical, `git status --porcelain` empty.
- `node <V>/site-scan.mjs <W>/out/site` (`head-site-scan.log`, `exit 0`, `problems: 0`):
  - `docs/how-we-test.html`: 20 headings (h1 "How we test" and the specified sections), one table of 10 rows
    header included, 6 cells each; image `../images/how-we-test/test-levels.svg` (alt of 214 characters),
    file present in `out/site/`;
  - `relative href and src: 11 in the whole page (9 unique), 2 inside <main>`, all resolve inside the site;
  - `index.html`, `docs/how-we-ship.html`, `docs/how-we-test.html`, `requirements/index.html`: `Home,
    Contributing, How we ship, How we test, Gallery, Requirements`, every target exists; `pages with a site
    header: 643, without the six links in order: 0` (viewer pages included);
  - manifest `pages` lists the page and `cards` lists `og/how-we-test.png`; the picture is 38674 bytes,
    1200x630 (opened).

### E4. The three drift probes fail as specified

Each: file backed up, edited, `just unit`, restored by copy (`<V>/probe.sh`), sha256 equal after, tree clean.

- P-stress, every `stress` code span removed from the page (`probe-1-unit.log`): `tests 5443, pass 5435,
  fail 1, skipped 7`, exit 1: "How we test names every CI job", `actual: [ 'stress' ]`.
- P-mode, `strs_test_coverage_mode: linked-swrs-and-acceptance-paths` (`probe-2-unit.log`): same counts, "How
  we test names the StRS coverage mode...": `the page names the coverage mode
  linked-swrs-and-validation-test, requirements/config.yml has linked-swrs-and-acceptance-paths` and `the page
  keeps "## What is not enforced yet" under the mode linked-swrs-and-acceptance-paths`.
- P-group, `group: [trust-security, gfm]` (`probe-3-unit.log`): same counts, "How we test lists the groups of
  the acceptance job": `groups of the acceptance job missing from the page: gfm`.
- Extra, drift test alone (`probe-extra.sh`, `probe-extra.log`), each `tests 12, pass 11, fail 1`: new
  requirements-lint script (`scripts/check_new_probe.py`); new CI job (`zzz-probe`); `gfm` no longer named;
  broken link (`line 320: ../test/zzz-missing.ts`); new folder (`test/zzz-probe`). Files restored, tree clean.

### E5. `just preflight` passes; CI

- The gate of E1a: `preflight exit 0 at 6c5106e...` (static stage on Windows); `requirements, 0 errors`,
  Sphinx `4 passed`, `found 0 vulnerabilities`.
- `gh pr checks 543` (run 45839932538, `pull_request`, head `6c5106e...`, `success`): `static`,
  `static-windows`, `visual`, `visual-2`, `viewer-graph`, `report`, `checks` pass; `acceptance`,
  `integration`, `stress`, `toc-loop`, `gallery`, `pages`, release jobs `skipping` (not run on a PR, not judged).

### E6. Captures, and the facts written differently from the specification

- Captures taken: `<V>/evidence/` (`before-after.md`): header before and after, page top with the diagram,
  table, "What is not enforced yet", diagram at its own size. `head-capture.log`: clicking "How we test" opens
  h1 "How we test"; diagram 1240x640 shown 880x454; table not clipped (880 of 880); no failed request.
  The posted PR body does not hold them yet: see P1.
- Differences from the specification are listed in the body's "Autonomous decisions" (two commits instead of
  one included). One small refinement is not listed (the page calls the e2e groups "the first part of the
  visual scenario ids, the folders of their captures", the spec "the folders of the visual scenarios"): not
  judged a failure.

## What the page and the diagram say

### C1. Owner's scenario steps 1 to 6

- Steps 1, 2: header and click, E3 and E6. `after-diagram-native.png` (opened): three lanes, the requirement
  stack (StRS, SwRS, `src/`) on the right, arrows labelled `@tests_req` and `@accepts_req`.
- Step 3: `grep -n '^| Acceptance' docs/how-we-test.md`: `just ci-acceptance [GROUP]`, job `acceptance`, push
  to `main` and heavy dispatch, `StRS path accepted`, `@accepts_req <StRS-ID>#S<n>`; line 159 `Groups with
  acceptance files: trust-security.`; `ls test/integration/acceptance`: only `trust-security.*` files.
- Step 4: line 219 `The StRS coverage mode is linked-swrs-and-validation-test.`; the built viewer home holds
  the labels "StRS paths tested", "StRS paths accepted", "StRS covered", "SwRS scenarios tested", "Paths
  tested", "Paths accepted" (`head-viewer-labels.log`).
- Step 5: the section says no check fails on an untested SwRS scenario or an unaccepted StRS path, with no date.
- Step 6: `grep -n how-we-test`: `CONTRIBUTING.md:255` and `docs/how-we-ship.md:49` link the page.

### C2. The page's statements match the repository

Read against the files at the head (`head-facts.log`, plus reads of the named files):

- `git ls-files 'test/core/render/*.contract.ts' | wc -l` 0; no `@tests_req`/`@accepts_req` under `sphinx/`.
- The example: TRUST-001 S1 has its `@accepts_req` in `trust-security.restricted.acceptance.ts:36`; TRUST-005
  derives from it and has `@tests_req ...#S1` under `test/session/`.
- The 16 groups, in the order of `GROUPS`; test folders, recipes and CI jobs and their triggers as in
  `justfile` and `ci.yml` (`ci-static`, `ci-visual` parts, `ci-viewer-graph`, `ci-acceptance`, `ci-stress`
  trusted then Restricted Mode with `STUDIO_STRESS_SCENARIOS`, `mutation-core` second phase and its report).
- Chromium unit tests outside `test:breakout` and `test:viewer-graph` carry markers and run in no CI job
  (skip reason `no Chromium can start here` in the CI log, `ci-static-skips.log`); `tableBreakout.test.ts`
  width assertions only on Windows.
- `check_main_paths.py`, `check-use-case-diagrams.mjs`, `check-marker-companions.mjs` rules, and okfreq 0.18.1's
  counting under the current coverage mode, as the page states them.

### C3. The SVG is accessible and self-contained

- `head-svg.log`: `role="img" aria-labelledby="t d"` (title and description), `viewBox="0 0 1240 640"`, the
  font family of `release-1-6-1.svg`; `script|image|foreignObject|style tags: 0`; `href/data: attributes: 0`;
  the only URL is the SVG namespace; `url()` only internal markers. No non-ASCII character in the page.

### C4. The first commit alone fails the drift test (a stated known gap)

- At `35cd6384`, drift test alone (`first-commit-drift.log`): `tests 12, pass 11, fail 1`, "How we test names
  every CI job", `actual: [ 'visual-2' ]`.

## The PR description

`gh pr view 543 --json body`, and GitHub's rendering of it (`gh api repos/.../pulls/543` with the HTML media
type, `pr-body-html.log`).

Holds:

- Renders: the nine `##` sections as headings, one table, the Mermaid block, seven task boxes (read from the
  rendered HTML; the diagram was not looked at in a browser). `img` tags: 0, so no image can show a user name.
- Consistent with the diff: Summary, Deliverables, Changes (compared with `git diff 4e4eeb4..HEAD`: header
  link, card entry, test updates, the CORE-086 source and tests, the marker, guideline and glossary lines),
  Blast radius, Autonomous decisions (checked one by one, C2 and C0), Known gaps (five bullets, each true: C2,
  E6, C4).
- Impacts' text claim (such changes fail the unit tests): E4 and its extra probes.
- "Changelog: no user-facing change" (C0: no `src/`, no `CHANGELOG.md`); "Local gates at `6c5106e`" and its
  counts (E1a, E5); "CI green at `6c5106e`" (E5).
- Unchecked "New or changed tests", "Requirements", "Verified": claim nothing.
- No `STALE` mark, no `UNVERIFIED` mark; no role name outside Internal references.

Fails:

### P1. Impacts holds neither the before/after nor "No visual change"

- `gh pr view 543 --json body`, section `## Impacts`: three sentences of text; no image link, no "No visual
  change" line (rendered HTML: `img` 0).
- Project rule (`.agents/guidelines/pull-request.guidelines.md`, lines 37-39): "Impacts holds the evidence of
  the change: the before/after the Verifier produced ..., or one line "No visual change" with the reason ...
  the Verifier fails a body whose Impacts has neither." The change is visible (site header, new page), and
  evidence item 6 asks for captures of the page in the body.
- By the same guideline ("Screenshots in the PR"), the PR opener pushes the captures of `<V>/evidence/` to the
  assets side branch, links them in Impacts, and a verification pass on the posted body follows. Until then
  the posted body fails.

### P2. Proofs without the head's SHA or a `carried from`

- "The new and changed tests against the code without this change, measured at `9d7e788`, an earlier commit
  below this branch: 13 of 49 fail.": neither the base or head of this PR nor a carry. `git merge-base
  --is-ancestor 9d7e788 HEAD`: no (its tree equals that of `5672ca63`, which is below). The branch was rebased
  with conflicts since, and `6c5106e4` changed `siteLinks.test.ts`. The figure is true at `4e4eeb4` (E1b).
- The "Built site ..." paragraph and the "Drift probes ..." paragraph name no SHA (`grep -nE '[0-9a-f]{7,40}'`
  on the body: only the four Test plan lines with `6c5106e` or `9d7e788`). Both results are true at
  `6c5106e` (E3, E4).
- Rule (`pr-template.md`, and the description check): each proof names the head, or `carried from <sha7>`.

### P3. The Review box cites a SHA no recorded pass approved

- Body: "[x] Review: approved at `6c5106e` (the last round was reviewed before a clean rebase that left the
  files unchanged)".
- `$CHANTIER log CR-507`: approved passes name `9d7e788` (r2), `fb5fb2f` (move), `bde4bd5` (move
  `fb5fb2f..bde4bd5`, and r3 `approved at bde4bd5..., committed as 166532f46b824ebad9659f696835f9254f1f961d`).
  No approved-pass note names `6c5106e`; the 14:32:14Z note records the push, and that `ship` answered
  `error: CR-507: CR-514's branch moved since its last ship (a5550c3 -> 4e4eeb4): it ships first, then ship
  again; nothing recorded`.
- The files are the approved ones (C0: same tree as `166532f4`), but the box's SHA is not proven by a note.
  Remedy: record the clean move once `ship` takes it, or write the box in the carried form `at 6c5106e
  (carried from 166532f)`, the SHA the r3 note names.

## Verdict

Code, page, tests, requirements, site and probes: verified at `6c5106e`. PR description: P1, P2 and P3 fail.

NOT VERIFIED
