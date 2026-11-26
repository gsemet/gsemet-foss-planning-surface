# CR-507 verification

Head: 0592dde49824cc0bb9fab3dbca07b6c0aaef2f20

Base: f9dc2c630b852635e8bffcd0b00b42cc886b293c. PR: https://github.com/gsemet/markdown-okf-schema-studio/pull/543
(open, draft). `<W>` is the CR worktree, `<F>` the CR folder, `<V>` is `<F>/work/verifier` (logs named below are
there). Previous judgment: `<V>/verify-6c5106e.md` (head `6c5106e4`, base `4e4eeb4`).

Result: the change does what the specification says (evidence items 1 to 6) at this head. The draft PR
description (`<F>/work/pr-body.md`, not posted yet) holds except one stated reason (D3, FAILED): it says the
files behind the screenshots did not change, and the Markdown renderer that draws three of them did. The
pictures themselves are unchanged.

## Head, move and scope

### C0. Head, tree, base, move and scope (judged at 0592dde)

- `git rev-parse HEAD`, `git status --porcelain`: `0592dde49824cc0bb9fab3dbca07b6c0aaef2f20`, empty (also at the end,
  after the probes, the site build and the removal of the base worktree).
- `gh pr view 543`: head `0592dde4...`, base `chantier/batch-09/cr-514-...`, draft, OPEN; `git ls-remote`: that base
  branch is `f9dc2c63...` (`h0592-images.log`).
- `git range-diff 4e4eeb4..6c5106e4 f9dc2c63..0592dde4`: `35cd6384 = 205123a3`, `6c5106e4 = 0592dde4`: both patches
  unchanged.
- `git diff --name-status 4e4eeb4 f9dc2c63` (what the new base brought) and `6c5106e4 0592dde4`: the same 15 files:
  `docs/user/editing.md`, `requirements/tiers/log.md`, four BLOCK SwRS and their index, `src/core/mapping/`
  (two files), `src/core/render/` (`mystBoxLines.ts`, `mystGithubAlerts.ts`, `mystRawHtml.ts`, `mystRenderer.ts`),
  `src/page/features/mappedBlocks.ts`, `test/session/boxBlockSourceLines.test.ts`.
- `git diff --shortstat f9dc2c63 0592dde4`: `17 files changed, 643 insertions(+), 23 deletions(-)`;
  `requirements/tiers/log.md` `4 0` (numstat). `git diff --stat f9dc2c63 0592dde4 -- src justfile package.json
  package-lock.json uv.lock .github requirements/config.yml CHANGELOG.md skills README.md AGENTS.md`: nothing.

## Evidence items of the specification

### E1a. `just check` passes with the new and changed tests (judged at 0592dde)

- Long gate cited: `<F>/work/gates/preflight-0592dde.log`, first line `CR-507
  chantier/batch-09/cr-507-how-we-test-a-docs-page-linking-test-lev 0592dde49824cc0bb9fab3dbca07b6c0aaef2f20 just preflight`;
  `$CHANTIER handoff CR-507`: note `gate: just preflight exit 0 at 0592dde4...`; its long-gate box is open because
  `chantier.yaml` names none.
- In that log: `check-no-merge-commits: passed (6 commits ...)`; `check-boundaries: passed (409 modules)`;
  `check-limits: passed (1384 files, ...)`; `check-markers: ... 459 in-force SwRS marked`; clip kit 56/56; unit
  `tests 5515, pass 5507, fail 0, skipped 8`; security 116/116; `296 passed`; `ci-static: passed`; last line
  `preflight exit 0 at 0592dde4...`.
- Own run: `just compile` (exit 0), then `node scripts/node-test.mjs unit` on the compiled `howWeTest`,
  `siteLinks`, `siteTheme`, `socialCard`, `requirementsViewer/pages` tests: `tests 49, pass 49, fail 0,
  skipped 0`, `exit 0` (`h0592-compile.log`, `h0592-five-files.log`).

### E1b. On the code without the change, the new tests fail (judged at 0592dde, base f9dc2c6)

- Detached worktree of `f9dc2c63` at `<W>/.artifacts/vbase` (removed since: `git worktree remove`, exit 0), the five
  test files of the head copied on it, `npm run compile` (exit 0), the same test command: `tests 49, pass 36,
  fail 13, skipped 0`, `exit 1` (`b0592-five-files.log`).
- Nine drift checks fail with `ENOENT` (`docs\how-we-test.md`; the diagram check on
  `images\how-we-test\test-levels.svg`).
- Four more: "the site header links How we ship then How we test from root and nested pages" (`index.html holds
  <a href="docs/how-we-ship.html">...`); "a viewer page brands and links the site relative to its own folder"
  (`the six links, in order`); "a main page and a viewer page carry the same brand and the six links..." (actual
  `Home, Contributing, How we ship, Gallery, Requirements`); "SIMPLE_CARDS covers the home, Contributing, How we
  ship and How we test pages" (missing `docs/how-we-test.md`).

### E2. `just requirements-lint` passes (judged at 0592dde)

- `h0592-requirements-lint.log`: `1228 requirements, 0 errors, 26 warnings`; `0 indexes would change`; `0
  requirement OKF projections would change`; `0 files would change`; `main paths: 96 StRS checked, 625 SwRS
  citations, all valid`; `use case diagrams: 94 StRS checked, all parse`; `exit 0`.

### E3. The site builds, with the page, the headers, the manifest and the picture (judged at 0592dde)

- `just site-from-run 45830014522` (`h0592-site-from-run.log`): `Built static site at <W>\out\site`, `exit 0`.
  `gh run view 45830014522`: `cd3b8e6a...`, `workflow_dispatch`, `success` (static, visual, integration, acceptance,
  stress included). `git rev-parse cd3b8e6a^{tree} 5f0746d7^{tree}`: both `e6f6894d...`; `git merge-base
  --is-ancestor 5f0746d7 HEAD`: yes.
- `just site-assemble` alone being refused without end-to-end reports: carried from 6c5106e: `justfile` and the
  gallery scripts did not change (C0).
- The 40 tracked pictures under `images/` were backed up and copied back: `cmp h0592-images-before.sha256
  h0592-images-after.sha256` identical, `git status --porcelain` empty.
- `node <V>/site-scan.mjs <W>/out/site` (`h0592-site-scan.log`, `exit 0`, `problems: 0`): page with 20 headings, one
  table of 10 rows header included, 6 cells each; diagram image and file present; `relative href and src: 11 in
  the whole page (9 unique), 2 inside <main>`, all resolve; the six links in order on `index.html`,
  `docs/how-we-ship.html`, the page and `requirements/index.html`; `pages with a site header: 643, without the six
  links in order: 0`; manifest `pages` and `cards` list the page and `og/how-we-test.png` (38674 bytes, 1200x630).

### E4. The three drift probes fail as specified (judged at 0592dde)

Each: file backed up, edited, `just unit`, restored by copy (`<V>/probe.sh`), sha256 equal after, tree clean. Logs in
`<V>/probes-0592dde/`.

- Every `stress` code span removed from the page (`probe-1-unit.log`): `tests 5515, pass 5507, fail 1, skipped 7`,
  exit 1: "How we test names every CI job", `actual: [ 'stress' ]`.
- `strs_test_coverage_mode: linked-swrs-and-acceptance-paths` (`probe-2-unit.log`): same counts, "How we test
  names the StRS coverage mode...": `the page names the coverage mode linked-swrs-and-validation-test,
  requirements/config.yml has linked-swrs-and-acceptance-paths` and `the page keeps "## What is not enforced yet"
  under the mode linked-swrs-and-acceptance-paths`.
- `group: [trust-security, gfm]` (`probe-3-unit.log`): same counts, "How we test lists the groups of the
  acceptance job": `groups of the acceptance job missing from the page: gfm`.
- Extra probes (new lint script, new CI job, group no longer named, broken link, new test folder, each `fail 1`;
  `<V>/probe-extra.log`): carried from 6c5106e: `git diff --stat 6c5106e4 0592dde4` on the drift test, the page, the
  picture, `test/`'s checked files, `justfile`, `.github`, `config.yml` and `sphinx` prints nothing, and the base adds
  no test folder (C0).

### E5. `just preflight` passes; CI (judged at 0592dde)

- The gate of E1a: `preflight exit 0 at 0592dde4...` (static stage on Windows); `1228 requirements, 0 errors`,
  Sphinx `4 passed`, `found 0 vulnerabilities`.
- `gh pr checks 543` (run 45888567979, head `0592dde4...`): `static`, `static-windows`, `visual`, `visual-2`,
  `viewer-graph`, `report`, `checks` pass; `acceptance`, `integration`, `stress`, `toc-loop`, `gallery`, `pages`,
  release jobs `skipping` (not run on a pull request, not judged).

### E6. Captures (judged at 0592dde) and differences from the specification

- `node <V>/capture.mjs <W> <W>/out/site <V>/recapture-0592dde after` (`h0592-capture.log`, `exit 0`): header with six
  links; click opens h1 "How we test"; diagram 1240x640 shown 880x454; table 880 of 880; no failed request.
- `cmp` of the five new captures with `<V>/evidence/after-*.png` (taken at `6c5106e4`): all five byte-identical.
  Four of them and `before-header.png` opened: they show what `before-after.md` says, no user name, no home folder.
- Differences from the specification listed in "Autonomous decisions": carried from 6c5106e: patch unchanged (C0).

## What the page and the diagram say

### C1. Owner's scenario steps 1 to 6

- Steps 1, 2: E3, E6. Steps 3 to 6 at 0592dde: `grep -n` on the page: line 159 ``Groups with acceptance files:
  `trust-security`.``, line 219 ``The StRS coverage mode is `linked-swrs-and-validation-test`.``; `git grep
  how-we-test`: `CONTRIBUTING.md:255`, `docs/how-we-ship.md:49`. The captures show the Acceptance row and the
  section "What is not enforced yet" as the specification says.
- Viewer home card labels: carried from 6c5106e: `test/site/requirementsViewer` shipped code unchanged (C0).

### C2. The page's statements match the repository

- carried from 6c5106e: the page is unchanged, and the base move touches none of the facts it states (no CI job,
  test folder, group, marker verb, lint command, mode or trigger; its added markers are `@tests_req` on BLOCK
  SwRS only: `git diff -U0 4e4eeb4 f9dc2c63 -- test/session/boxBlockSourceLines.test.ts`). The counted facts are
  also held by the drift test, which passes at 0592dde (E1a).

### C3. The SVG is accessible and self-contained

- carried from 6c5106e: `git diff --stat 6c5106e4 0592dde4 -- images` prints nothing.

### C4. The first commit alone fails the drift test (a stated known gap)

- carried from 6c5106e: `205123a3` is the same patch as `35cd6384` (C0) and the move changed no CI workflow, so it
  still lacks `visual-2`.

## The draft PR description (judged at 0592dde)

Judged: `<F>/work/pr-body.md`, sha256 `734726be6f9afb78...a92ef3d5` (copy `<V>/h0592-draft-body.md`). The forge still
holds the body of `6c5106e4`; posting is the Driver's, not judged.

### D1. Form

- `diff <V>/desc2-posted-body.md <F>/work/pr-body.md` (`h0592-body-diff.txt`): only SHAs, screenshot captions, test
  counts, the Review reason and the removed probe counts changed, plus one final empty line. Rendering (sections,
  table, task boxes, Mermaid block, 5 images with alt text): carried from 6c5106e: same structure.

### D2. Images

- `curl` of the five raw URLs at assets commit `398427751f944842a06fede7b6d18dc51560fc67` (`h0592-images.log`): each
  `200 image/png`, identical to `<V>/evidence/`; the four after pictures also identical to the captures at 0592dde.
  `git ls-remote`: that commit is the head of the `-assets` branch.
- "Header before, at `f9dc2c6` (carried from `4e4eeb4`: the files of the site header did not change between
  them)": holds. `git diff --stat 4e4eeb4 f9dc2c63 -- test/site images scripts package.json package-lock.json`
  prints nothing.

### D3. FAILED: the reason that carries the after screenshots is false

- Body, line 67: "Header after, at `0592dde` (carried from `6c5106e`: a clean rebase that left the files behind
  these pictures unchanged)"; the three next captions (page top, table, "What is not enforced yet") rest on it with
  "(carried from `6c5106e`)".
- `git diff --stat 6c5106e4 0592dde4 -- docs/how-we-test.md docs/how-we-ship.md images test/site src/core/render
  package.json package-lock.json scripts`: `mystBoxLines.ts | 248`, `mystGithubAlerts.ts | 3`, `mystRawHtml.ts | 3`,
  `mystRenderer.ts | 12`; `4 files changed, 255 insertions(+), 11 deletions(-)`.
- Those files draw the pictured page: `test/site/buildSite.ts:7` imports `renderMyst` from
  `../../src/core/render/mystRenderer` and calls it at line 135; `mystRenderer.ts` imports `mystBoxLines` and
  `mystRawHtml`, both changed.
- True and proven instead (E6, D2): the clean rebase left the page, the diagram and the site files unchanged, the
  renderer changed, and captures taken at `0592dde` are byte-identical to the posted pictures. A caption that says
  they were captured again at `0592dde` and are the same, byte for byte, as at `6c5106e` holds with this note; no
  new image or upload is needed.

### D4. The other proofs hold and name their SHA

- "13 of the 49 tests ... fail on the base `f9dc2c6`; all 49 pass at `0592dde`" and the list under it: E1b, E1a.
- Requirements line: E2. Changelog line: C0 (no CHANGELOG in the diff).
- Local gates line: E1a, E5: 5515/5507/0/8, 116/116, 296 passed, 0 errors, Sphinx 4, 0 vulnerabilities.
- "Review: approved at `0592dde` (carried from `166532f`...)": holds. `$CHANTIER log CR-507`, 14:30:52Z: `r3
  approved at bde4bd58..., committed as 166532f46b824ebad9659f696835f9254f1f961d`. `git range-diff
  a5550c32..166532f4 f9dc2c63..0592dde4`: both commits `=`; `git patch-id --verbatim`: `bde4bd58` = `205123a3`
  (`d848f4c5...`), `166532f4` = `0592dde4` (`211affb9...`).
- "Verified at `0592dde`: the tests against the base, requirements-lint, the site build and the drift probes": the
  four items hold in this run (E1b, E2, E3, E4).
- CI line: E5. "Built site" paragraph: E3 (every figure). "Drift probes" paragraph: E4.
- "light theme only" and the rest of Summary, Deliverables, Changes, Impacts' text, Blast radius, Autonomous
  decisions: carried from 6c5106e: patch unchanged (C0) and text unchanged (D1). "The rebases of this branch
  conflicted only in the requirements log": `<F>/work/conflicts.md` names `log.md` alone, both times; the later
  rebases are clean (C0).
- Known gaps: five bullets, unchanged, true (C2, C4, E6).
- `grep -nE 'STALE|UNVERIFIED|CR-?[0-9]|[Bb]atch|[Rr]ound|Driver|Coder|Inspector|Verifier|Foreman|\.agents/changes|O-[0-9]'`
  on the draft: one line, `- CR-507 how-we-test.`, under "Internal references".

## Verdict

Code, page, tests, requirements, site, probes, CI and pictures: verified at `0592dde`. PR description: fails on D3
alone.

NOT VERIFIED
