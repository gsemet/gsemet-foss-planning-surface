# CR-507 verification

Head: 6c5106e4589592002f828b6feb3d545a442591aa

Base: 4e4eeb4eb548fc4a8f05838f6d0257b76d6b9f0e. PR: https://github.com/gsemet/markdown-okf-schema-studio/pull/543 (open, draft).
`<W>` is the CR worktree, `<F>` the CR folder, `<V>` is `<F>/work/verifier` (logs named below are there).
Two passes at this one head. The first (verdict 2026-11-26T15:15:02Z, NOT VERIFIED on the description
only; copy in `<V>/verify-first-pass-6c5106e.md`) judged C0 to C4 and E1a to E6. Those claims keep the SHA
`6c5106e`: carried from 6c5106e: same head and same base, not run again (what the second pass read again is
named in D1 to D7). The second pass judged the description posted since (claims D1 to D7).

Result: the change does what the specification says (evidence items 1 to 6), and the posted PR
description holds.

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
  ship recorded at this head: `$CHANTIER log CR-507`, 14:32:14Z, `ship` waits for the CR below).
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
  The body posted since holds them: see D2.
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

## The PR description (second pass, at `6c5106e`)

The body judged: `gh pr view 543 --json body -q .body`, sha256 `4e803065ca96c95d...d57fee664e`, saved as
`<V>/desc2-posted-body.md`; PR updated 2026-11-26T15:18:28Z, head `6c5106e4589592002f828b6feb3d545a442591aa`,
draft, OPEN, MERGEABLE (read again at 15:21Z, same hash). It equals `<F>/work/pr-body.md` but for one final
empty line. Its changes from the first body: `<V>/desc2-diff-from-first-body.txt`.

### D1. It renders

- `gh api repos/gsemet/markdown-okf-schema-studio/pulls/543` (HTML media type, `<V>/desc2-posted-body.html`):
  headings Summary, Deliverables, Changes, Impacts, Blast radius, Autonomous decisions, Known gaps, Test
  plan, Internal references; 1 table; 7 task boxes, all checked; 5 `img` tags, each with its alt text; one
  Mermaid block.
- The Mermaid block, put in a one-file bundle in the scratchpad, `node scripts/check-use-case-diagrams.mjs
  <bundle>`: `use case diagrams: 1 StRS checked, all parse (Mermaid 12.2.0)`, exit 0.

### D2. Impacts holds the before and after (former P1: fixed)

- `curl` of the five raw URLs at assets commit `398427751f944842a06fede7b6d18dc51560fc67`
  (`<V>/desc2-images.log`): each `200 image/png`, byte identical (`cmp`) to the file of the same name in
  `<V>/evidence/`. `git ls-remote`: that commit is the head of the CR branch's `-assets` side branch.
- The five downloaded images opened: header with five links (before), six with "How we test" between "How
  we ship" and "Gallery" (after), page top with introduction, two levels and diagram, the table, the
  section with four points. Captions and alt texts say that. No user name and no home folder in any.
- Captions: before at `4e4eeb4` (the base), after at `6c5106e`, as `<V>/evidence/before-after.md` says.
- "light theme only": `git grep` at the head: `test/site/siteTheme.ts:54` `color-scheme:light`, and
  `siteTheme.test.ts:45` forbids `prefers-color-scheme: dark`.

### D3. Each proof names its SHA and is proven (former P2: fixed)

`grep` of the body: each Test plan result, screenshot caption, "Built site" and "Drift probes" names
`6c5106e` or the base `4e4eeb4`, except the Changelog line (a statement about the diff, C0). No `STALE`, no
`UNVERIFIED`; `9d7e788` is gone.

- "13 of the 49 tests ... fail on the base `4e4eeb4`; all 49 pass": E1b and E1a. The list under it matches
  `<V>/base-five-files.log`: 9 failing drift checks (`ENOENT` on `docs/how-we-test.md`, the diagram one on
  `test-levels.svg`), then the four named tests with the messages quoted (`index.html holds <a ...>`, `the
  six links, in order`, actual `Home, Contributing, How we ship, Gallery, Requirements`, missing
  `docs/how-we-test.md`).
- Requirements line: E2 (`just requirements-lint`, 0 errors, `0 files would change`); `git diff
  4e4eeb4..HEAD -- test/site/siteLinks.test.ts`: the added `#S1` marker on the header test.
- Local gates line: `<F>/work/gates/preflight-6c5106e.log` read again: unit 5443/5435/0/8, security 116/116,
  `296 passed`, `1228 requirements, 0 errors`, Sphinx `4 passed`, `found 0 vulnerabilities`, `preflight exit
  0 at 6c5106e...`.
- "Verified at `6c5106e`: the tests against the base, requirements-lint, the site build and the drift
  probes": E1b, E2, E3, E4.
- CI line: `gh pr checks 543` run again: `static`, `static-windows`, `visual`, `visual-2`, `viewer-graph`,
  `report`, `checks` pass; the others `skipping`.
- "Built site" paragraph: `<V>/head-site-scan.log` and `<V>/site-scan.mjs`: 20 headings, one table of 10
  rows, 11 relative `href` and `src` of the page all resolved (`problems: 0`), 643 pages with a header and 0
  without the six links, manifest page and card. `gh run view 45830014522`: `success`, static, visual,
  integration, acceptance and stress jobs included; `git rev-parse cd3b8e6a^{tree} 223a8c49^{tree}`: both
  `e6f6894d...`; `223a8c49` is an ancestor of the head.
- "Drift probes" paragraph: `<V>/probe.sh` (probe 1 removes every `stress` code span) and
  `probe-{1,2,3}-unit.log`: each `tests 5443, pass 5435, fail 1, skipped 7`, with the messages quoted.

### D4. The Review box (former P3: fixed)

- Body: "Review: approved at `6c5106e` (carried from `166532f`: a clean rebase after the last review left
  the files unchanged)".
- `$CHANTIER log CR-507`, 14:30:52Z: `r3 approved at bde4bd58..., committed as
  166532f46b824ebad9659f696835f9254f1f961d`.
- `git rev-parse HEAD^{tree} 166532f4^{tree}`: both `e9e12e6af08cd9ca108c9cbb7f369b67e2220d27`.

### D5. It is consistent with the diff

- Outside Impacts and Test plan the text changed in one place (`desc2-diff-from-first-body.txt`): the e2e
  groups are "described as the first part of the visual scenario ids, which are the folders of their
  captures": `docs/how-we-test.md` lines 202-205; `test/shared/e2eGroups.ts` (ids "used in scenario ids
  (`<group>/vNN-...`) and folder names"), `test/visual/scenarios.ts:329`. This also lists the refinement E6
  noted as unlisted.
- The rest is the text the first pass compared with `git diff 4e4eeb4..HEAD` (same head; `git ls-remote`: the
  base branch is still `4e4eeb4`). Also read now: CORE-086 `implemented_in_files` is
  `test/site/siteTheme.ts` (not in the diff), `tested_in_files` the three test files Changes names.

### D6. Known gaps

- Visible, five bullets, unchanged text, each true (C2, E6 with `<V>/head-capture.log`: 1240 shown 880, C4).
  No `UNVERIFIED` claim. `before-after.md` names no capture that failed: its "none" entries are views of a
  page the base does not have (`base-capture.log`: `not in this site`).

### D7. No internal reference or role outside the last section

- `grep -nE 'STALE|UNVERIFIED|CR-?[0-9]|[Bb]atch|[Rr]ound|Driver|Coder|Inspector|Verifier|Foreman|\.agents/changes|O-[0-9]'`
  on the body: one line, `- CR-507 how-we-test.`, under "Internal references". "the last review" and "a
  maintainer decision" name no agent role.

## Verdict

Code, page, tests, requirements, site and probes: verified at `6c5106e` (first pass). PR description:
verified at `6c5106e` (D1 to D7; P1 to P3 of the first pass are fixed).

VERIFIED
