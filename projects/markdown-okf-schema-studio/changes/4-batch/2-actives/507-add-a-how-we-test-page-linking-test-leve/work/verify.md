# CR-507 verification

Head: 0592dde49824cc0bb9fab3dbca07b6c0aaef2f20

Base: f9dc2c630b852635e8bffcd0b00b42cc886b293c. PR: https://github.com/gsemet/markdown-okf-schema-studio/pull/543
(open, draft). `<W>` is the CR worktree, `<F>` the CR folder, `<V>` is `<F>/work/verifier` (logs named below are
there). Earlier judgments: `<V>/verify-first-pass-0592dde.md` (same head: NOT VERIFIED on one reason in the draft
description) and `<V>/verify-6c5106e.md` (head `6c5106e4`, base `4e4eeb4`).

This pass judges the posted description of PR #543 alone. The code, test, site, probe and CI claims (E1a to C4) were
not run again: each is marked `carried from 0592dde: same head and base`. Where one of them already carried a part
from `6c5106e`, that mark stays.

Result: the change does what the specification says (evidence items 1 to 6) at this head, and the posted
description holds.

## Head, move and scope

### C0. Head, tree, base and move (judged at 0592dde, this pass)

- `<V>/desc3-move.log`: `git rev-parse HEAD` = `0592dde49824cc0bb9fab3dbca07b6c0aaef2f20`, `git status --porcelain`
  empty.
- `git ls-remote`: CR branch `0592dde4...`, base branch `f9dc2c63...`, assets branch `39842775...`.
- `gh pr view 543`: head `0592dde4...`, base `chantier/batch-09/cr-514-...` at `f9dc2c63...`, draft, OPEN, updated
  2026-11-26T20:34:16Z.
- `git range-diff 4e4eeb4..6c5106e4 f9dc2c63..0592dde4`: `35cd6384 = 205123a3`, `6c5106e4 = 0592dde4`: both patches
  unchanged.
- `git diff --name-status 6c5106e4 0592dde4` (what the new base brought): 15 files: `docs/user/editing.md`,
  `requirements/tiers/log.md`, four BLOCK SwRS and their index, `src/core/mapping/` (two files),
  `src/core/render/` (`mystBoxLines.ts`, `mystGithubAlerts.ts`, `mystRawHtml.ts`, `mystRenderer.ts`),
  `src/page/features/mappedBlocks.ts`, `test/session/boxBlockSourceLines.test.ts`.

### C0b. Scope of the diff against the base (carried from 0592dde: same head and base)

- `git diff --shortstat f9dc2c63 0592dde4`: `17 files changed, 643 insertions(+), 23 deletions(-)`;
  `requirements/tiers/log.md` `4 0` (numstat). `git diff --stat f9dc2c63 0592dde4 -- src justfile package.json
  package-lock.json uv.lock .github requirements/config.yml CHANGELOG.md skills README.md AGENTS.md`: nothing.

## Evidence items of the specification

### E1a. `just check` passes with the new and changed tests (carried from 0592dde: same head and base)

- Long gate cited: `<F>/work/gates/preflight-0592dde.log`, first line `CR-507
  chantier/batch-09/cr-507-how-we-test-a-docs-page-linking-test-lev 0592dde49824cc0bb9fab3dbca07b6c0aaef2f20 just preflight`;
  `$CHANTIER handoff CR-507`: note `gate: just preflight exit 0 at 0592dde4...`; its long-gate box is open because
  `chantier.yaml` names none.
- In that log: `check-no-merge-commits: passed (6 commits ...)`; `check-boundaries: passed (409 modules)`;
  `check-limits: passed (1384 files, ...)`; `check-markers: ... 459 in-force SwRS marked`; clip kit 56/56; unit
  `tests 5515, pass 5507, fail 0, skipped 8`; security 116/116; `296 passed`; `ci-static: passed`; last line
  `preflight exit 0 at 0592dde4...`.
- Verifier run: `just compile` (exit 0), then `node scripts/node-test.mjs unit` on the compiled `howWeTest`,
  `siteLinks`, `siteTheme`, `socialCard`, `requirementsViewer/pages` tests: `tests 49, pass 49, fail 0,
  skipped 0`, `exit 0` (`h0592-compile.log`, `h0592-five-files.log`).

### E1b. On the code without the change, the new tests fail (base f9dc2c6; carried from 0592dde: same head and base)

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

### E2. `just requirements-lint` passes (carried from 0592dde: same head and base)

- `h0592-requirements-lint.log`: `1228 requirements, 0 errors, 26 warnings`; `0 indexes would change`; `0
  requirement OKF projections would change`; `0 files would change`; `main paths: 96 StRS checked, 625 SwRS
  citations, all valid`; `use case diagrams: 94 StRS checked, all parse`; `exit 0`.

### E3. The site builds, with the page, the headers, the manifest and the picture (carried from 0592dde: same head and base)

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

### E4. The three drift probes fail as specified (carried from 0592dde: same head and base)

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

### E5. `just preflight` passes; CI (carried from 0592dde: same head and base)

- The gate of E1a: `preflight exit 0 at 0592dde4...` (static stage on Windows); `1228 requirements, 0 errors`,
  Sphinx `4 passed`, `found 0 vulnerabilities`.
- `gh pr checks 543` (run 45888567979, head `0592dde4...`): `static`, `static-windows`, `visual`, `visual-2`,
  `viewer-graph`, `report`, `checks` pass; `acceptance`, `integration`, `stress`, `toc-loop`, `gallery`, `pages`,
  release jobs `skipping` (not run on a pull request, not judged).

### E6. Captures and differences from the specification (carried from 0592dde: same head and base)

- `node <V>/capture.mjs <W> <W>/out/site <V>/recapture-0592dde after` (`h0592-capture.log`, `exit 0`): header with six
  links; click opens h1 "How we test"; diagram 1240x640 shown 880x454; table 880 of 880; no failed request.
- `cmp` of the five new captures with `<V>/evidence/after-*.png` (taken at `6c5106e4`): all five byte-identical.
- Differences from the specification listed in "Autonomous decisions": carried from 6c5106e: patch unchanged (C0).

## What the page and the diagram say

### C1. Owner's scenario steps 1 to 6 (carried from 0592dde: same head and base)

- Steps 1, 2: E3, E6. Steps 3 to 6 at 0592dde: `grep -n` on the page: line 159 ``Groups with acceptance files:
  `trust-security`.``, line 219 ``The StRS coverage mode is `linked-swrs-and-validation-test`.``; `git grep
  how-we-test`: `CONTRIBUTING.md:255`, `docs/how-we-ship.md:49`. The captures show the Acceptance row and the
  section "What is not enforced yet" as the specification says.
- Viewer home card labels: carried from 6c5106e: `test/site/requirementsViewer` shipped code unchanged (C0).

### C2. The page's statements match the repository (carried from 0592dde: same head and base)

- carried from 6c5106e: the page is unchanged, and the base move touches none of the facts it states (no CI job,
  test folder, group, marker verb, lint command, mode or trigger; its added markers are `@tests_req` on BLOCK
  SwRS only: `git diff -U0 4e4eeb4 f9dc2c63 -- test/session/boxBlockSourceLines.test.ts`). The counted facts are
  also held by the drift test, which passes at 0592dde (E1a).

### C3. The SVG is accessible and self-contained (carried from 0592dde: same head and base)

- carried from 6c5106e: `git diff --stat 6c5106e4 0592dde4 -- images` prints nothing.

### C4. The first commit alone fails the drift test, a stated known gap (carried from 0592dde: same head and base)

- carried from 6c5106e: `205123a3` is the same patch as `35cd6384` (C0) and the move changed no CI workflow, so it
  still lacks `visual-2`.

## The posted PR description (judged at 0592dde, this pass)

Judged: the body read from the forge, `gh pr view 543 --json body` (`<V>/desc3-posted-body.md`, sha256
`c84d95c3...3008061`, identical to `<F>/work/scratch/posted-0592dde.md`). `diff <F>/work/pr-body.md
<V>/desc3-posted-body.md`: one final empty line only.

### D1. What changed since the judged draft

- `diff <V>/h0592-draft-body.md <V>/desc3-posted-body.md` (`desc3-diff-from-draft.txt`): the paragraph "The four
  pictures that follow ..." added (lines 67 to 69), the reason removed from the header caption, "(carried from
  `6c5106e`)" removed from the three next captions, and one final empty line. Nothing else.

### D2. Rendering

- `gh api .../pulls/543 -H "Accept: application/vnd.github.full+json" --jq .body_html`
  (`desc3-posted-body.html`), parsed by `python -I <V>/desc3-render.py` (`desc3-render.log`): nine headings from
  "Summary" to "Internal references", 1 table (2 rows), 7 task boxes all checked, the Mermaid block (same markers as
  the body judged at `6c5106e`), 5 images with alt text, no literal Markdown left. The new paragraph renders as one
  paragraph, its two source line breaks shown as `<br>` as in the rest of the body, before "Header after, at
  0592dde:" (`desc3-paragraph.log`). Against the `6c5106e` HTML: `p` 23 to 24; headings, table, task boxes and images
  the same.

### D3. Images

- `curl` of the five raw URLs at assets commit `398427751f944842a06fede7b6d18dc51560fc67` (`desc3-images.log`): each
  `200 image/png`. `cmp`: the four after pictures = `<V>/evidence/after-*.png` (taken at `6c5106e4`) =
  `<V>/recapture-0592dde/`; `before-header.png` = `<V>/evidence/before-header.png`.
- All five opened (`<V>/desc3-images/`): the header with five links; the header with six; the top of the page with
  its diagram; the table; "What is not enforced yet" with four points. Each matches its caption and alt text. No
  user name, home folder, path or address bar.
- "Header before, at `f9dc2c6` (carried from `4e4eeb4`: ...)": carried from 0592dde: same head and base, same text
  (D1). Its proof: `git diff --stat 4e4eeb4 f9dc2c63 -- test/site images scripts package.json package-lock.json`
  prints nothing.

### D4. The changed sentences hold (the failed claim of the first pass at this head is fixed)

- "The four pictures that follow": four pictures follow (after-header, after-page-top, after-table,
  after-not-enforced; D2, D3).
- "were captured again at `0592dde`": `h0592-capture.log` first line `captures of the head site at
  0592dde49824...`, `exit 0`; files in `<V>/recapture-0592dde/` (E6).
- "after a clean rebase": C0 range-diff, both patches `=`.
- "that left the page, the diagram and the site files unchanged": `git diff --stat 6c5106e4 0592dde4 --
  docs/how-we-test.md docs/how-we-ship.md images test/site scripts package.json package-lock.json` prints nothing
  (`desc3-move.log`). "Site files" is read as the site's own sources, `test/site`, as in the body's "Changes" ("Site:
  ... `test/site/siteHeader.ts` ... `test/site/buildSite.ts`"). The rebase did change one user guide page that the
  site also publishes, `docs/user/editing.md` (`git diff --stat 6c5106e4 0592dde4 -- docs images test/site`:
  that file only, `desc3-images.log`); none of the pictures shows it (D3).
- "and changed the Markdown renderer": `git diff --stat 6c5106e4 0592dde4 -- src/core/render`: 4 files, 255
  insertions, 11 deletions (`desc3-move.log`).
- "each is the same, byte for byte, as its picture taken at `6c5106e`": the `cmp` of D3; `head-capture.log`:
  `captures of the head site at 6c5106e4...`.
- The four captions "..., at `0592dde`:" name the head, and each picture equals the capture made there (D3).

### D5. The other proofs hold and name their SHA (carried from 0592dde: same head and base; text unchanged, D1)

- "13 of the 49 tests ... fail on the base `f9dc2c6`; all 49 pass at `0592dde`" and the list under it: E1b, E1a.
- Requirements line: E2. Changelog line: C0b (no CHANGELOG in the diff).
- Local gates line: E1a, E5: 5515/5507/0/8, 116/116, 296 passed, 0 errors, Sphinx 4, 0 vulnerabilities.
- "Review: approved at `0592dde` (carried from `166532f`...)": `$CHANTIER log CR-507`, 14:30:52Z: `r3 approved at
  bde4bd58..., committed as 166532f46b824ebad9659f696835f9254f1f961d`. `git range-diff a5550c32..166532f4
  f9dc2c63..0592dde4`: both commits `=`; `git patch-id --verbatim`: `bde4bd58` = `205123a3` (`d848f4c5...`),
  `166532f4` = `0592dde4` (`211affb9...`).
- "Verified at `0592dde`: the tests against the base, requirements-lint, the site build and the drift probes": E1b,
  E2, E3, E4.
- CI line: E5. "Built site" paragraph: E3 (every figure). "Drift probes" paragraph: E4.
- "light theme only" and the rest of Summary, Deliverables, Changes, Impacts' text, Blast radius, Autonomous
  decisions: carried from 6c5106e: patch unchanged (C0). "The rebases of this branch conflicted only in the
  requirements log": `<F>/work/conflicts.md` names `log.md` alone, both times; the later rebases are clean (C0).
- Known gaps: five bullets, true (C2, C4, E6).

### D6. No leftover mark, no role as doer (judged at 0592dde, this pass)

- `desc3-scan.log`: `grep -nE 'STALE|UNVERIFIED|CR-?[0-9]|[Bb]atch|[Rr]ound|Driver|Coder|Inspector|Verifier|Foreman|\.agents/changes|O-[0-9]'`
  on the posted body: one line, 196, `- CR-507 how-we-test.`, under "Internal references". `grep -niE
  'gaeta|C:[\/]|/Users/|/home/|@gmail'`: nothing.

## Verdict

Code, page, tests, requirements, site, probes and CI: verified at `0592dde` (carried). Posted PR description:
holds at `0592dde`.

VERIFIED
