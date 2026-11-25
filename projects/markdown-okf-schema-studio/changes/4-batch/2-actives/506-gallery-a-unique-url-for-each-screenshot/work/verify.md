# CR-506 verification

Head: c715355c203d92df18200011749d1a73cead0ad9

Verdict: VERIFIED

Every product claim and the five evidence items of the specification pass at this head (claims 1
to 12), and the PR description as now posted passes (claim 13, judged again in a description-only
pass after the body was edited).

- Base: `4a47151e8d055b7f096b69b1fca2d9bf9636f863` (origin/main). `<worktree>` is the CR worktree,
  `<folder>` the CR folder. Logs are under `<folder>/work/gates/`, probe scripts under
  `<folder>/work/verifier/`, captures under `<folder>/work/verifier/evidence/`.
- Claims 1 to 12 were judged at `c715355c203d92df18200011749d1a73cead0ad9` by the earlier pass:
  carried from c715355 (same head, same base, no move; the body edit touches no code or proof),
  not run again, except the log reading of claim 12 and the checks that claim 13 cites.
- `git rev-parse HEAD` in `<worktree>`: `c715355c203d92df18200011749d1a73cead0ad9`.
  `git ls-remote origin "refs/heads/chantier/batch-09/cr-506*"`: the same SHA for the change
  branch (and `4abc9d62ba790cfb9b331dea20548900c7a0215a` for its `-assets` branch).
  `git ls-remote origin refs/heads/main`: `4a47151e8d055b7f096b69b1fca2d9bf9636f863`.
  `gh pr view 526`: head c715355, draft true, state OPEN.

## 1. Evidence 1: unit tests of the page and the ids (c715355c) VERIFIED

`node --test --test-reporter=spec out/test/site/gallery.test.js` after `npm run compile`
(log `verifier-gallery-unit-c715355.log`): `tests 8, pass 8, fail 0, skipped 0`, among them
visual scenario and step ids; one id and URL whatever the run folder suffix; any other path,
percent-encoded; two captures of one id stay unique; notice and history handling in the page; an id
holding HTML characters is escaped. On Windows the escaping test uses `a&'b`; the `<` and `"`
variant passed on Linux (CI run 45669698414, job static 139401313263:
"an id holding HTML characters is escaped in the page").

## 2. The new tests fail on the previous code (head tests on base 4a47151e) VERIFIED

Detached worktree of the base, the head's two test files copied in, with a shim
`test/site/galleryPage.ts` that re-exports the base `buildGallery` and `listCaptures` and throws
for the three new functions. `node --test --test-reporter=spec out/test/site/gallery.test.js
out/test/site/galleryLinks.browser.test.js` (log `verifier-newtests-on-base-4a47151.log`):
exit 1, `tests 18, pass 3, fail 15`: the 2 old unit tests pass and the 6 new ones fail; browser
steps 1 to 8 fail (and their parent test), only step 9 "no page error" passes.

## 3. Evidence 2: browser test of the links (c715355c) VERIFIED

- `just ci-viewer-graph` (log `verifier-ci-viewer-graph-c715355.log`): gallery steps 1 to 9 pass,
  `tests 16, pass 16, fail 0, skipped 0`, `ci-viewer-graph: passed`.
- `env STUDIO_REQUIRE_CHROMIUM=1 STUDIO_REQUIRE_REQUIREMENTS_REPORT=1 npm run test:viewer-graph`:
  16 of 16 pass, tree clean afterwards.
- Linux: CI run 45669698414, job viewer-graph 139401313367: steps 1 to 9 pass, 16 of 16, 0
  skipped, `ci-viewer-graph: passed`. Job static (no Chromium) reports the test skipped with
  "no Chromium can start here".
- Accepted deviation from the specification's step order: cards are in name order (legacy path 1,
  run folder 2, visuals 3 and 4), which D9 requires.

## 4. Evidence 3: the real site from a real CI artifact (c715355c) VERIFIED

Artifact `studio-reports-attempt-1` of run 45476952370, the latest green heavy run of main
(`63ef752bba38647ac0f95fa166855ec6e5970293`, integration and stress success; the newer run
45580228461 at the base failed). Name confirmed with `scripts/select_e2e_run.py
--reports-artifact-of`. `just site-assemble`: exit 0 (log
`verifier-site-assemble-c715355.log`; it rewrote tracked files under `images/`, restored with
`git checkout -- images`). Base site built from the same artifact.

`node compare-sites.mjs <worktree> <worktree>/out/base` (log `verifier-compare-sites-c715355.log`):

```text
screenshot files: 610
openers: 610 data-capture-id on openers: 610 unique: 610
figures with an id: 610 same ids and order as openers: true
ids by shape: real-window registry 113 visual 497 other 0
ids with a run folder prefix or a ~: []
```

`node probe-real-site.mjs <worktree> <worktree>/out/base <evidence>` (log
`verifier-probe-real-site-c715355.log`):

- Direct load and reload of `#block-editing/v08-insert-point-hover-light-900` (123 of 610),
  `...--hover` (122) and `#block-editing/r01-paragraph-blur-commit` (23, file under
  `real-input-t2pNgz/`): viewer open, right heading, title `<id> | gallery | Markdown OKF-Schema
  Studio`, image loaded.
- Base: open and Next keep the address `gallery.html`, title unchanged, Back leaves the gallery
  (`about:blank`); `#nope/r99-gone` shows no notice.
- The same site opened from disk (`file://`): direct load, Next, Escape and Back work.
- `page errors: []`.

Captures: see `evidence/before-after.md`; all 11 images opened: each shows what it names, legible,
no username and no home folder path.

## 5. History, title and focus, D6 and D8 (c715355c) VERIFIED

Same log, real site: click r01, Next (r02, `#...r02-mod-enter-commit`, 24 of 610), ArrowLeft,
Back three times (r02, r01, then the grid with focus on r01's card), Forward (r01). Escape: URL
`gallery.html`, page title restored, focus on the card, card in view; Back reopens. Close button
after three Next: grid, focus on the card of the screenshot closed (r04).

## 6. Unknown, malformed and markup fragments, escaping, D4 and D7 (c715355c) VERIFIED

- Real site: `#nope/r99-gone`, `#%E0%A4%A` and an encoded `<img onerror>` fragment: no viewer,
  notice "The screenshot <id> is not in this gallery: it may have been renamed or removed.", above
  the grid (bottom 279, grid top 295), 0 child elements in the notice, 0 alerts. Opening a card
  hides it, Back shows it again, an empty `#` hides it.
- `node probe-meta-and-escaping.mjs <worktree>` (log `verifier-probe-meta-escaping-c715355.log`),
  a file name holding `<img src=x onerror=alert(1)>&"` through the shipped `buildGallery` and
  `pageDocument`: no raw markup in the HTML, opener escaped, ids read back exactly, URL
  percent-encoded, no injected image, direct load opens it, 0 alerts.
- Search of `test/site/galleryPage.ts` for `innerHTML`: no match.

## 7. Cards are real links; modified clicks are the browser's, D5 (c715355c) VERIFIED

- Real site: Ctrl click and middle click open a new tab at `#<id>`, this page unchanged (0 history
  entries); the card's resolved `href` is `gallery.html#<id>`.
- Trusted and synthetic Meta, Ctrl, Shift and Alt clicks: `interceptedByPage: false`, viewer not
  open. Alt and Meta arrows: `defaultPrevented=false`.
- Observation, no failure: in Chromium on Windows, Meta is not a new-tab modifier, so a Meta click
  follows the link in the same tab and the viewer then opens through `hashchange`. The page does
  not intercept it.

## 8. What does not change, D9 and the kept addresses (c715355c) VERIFIED

compare-sites log: image `src` in order, captions, sidecar templates, viewer dialog, social card
meta, title and site header identical base and head (610 captures); site files base 2463, head
2464, only in base 0, only in head the new requirement's page; `reports/e2e/screenshots/` (1381
files) and `reports/e2e/gallery/` (16 files) same paths and bytes. Position counter reads the same
on base and head (24 of 610). Probe: at 1280 and 390 px, 36 boxes and computed styles identical,
grid screenshot bytes identical, focus outline identical (solid 3px, offset -3px), focused
screenshot bytes identical.

## 9. Code layout and files changed, D10 (c715355c) VERIFIED

- `git diff --stat origin/main...HEAD`: 13 files, 760 insertions, 172 deletions: the glossary,
  the `ci.yml` comment, CHANGELOG, CONTRIBUTING, `package.json` (`test:viewer-graph`), four
  requirements files, `test/site/buildSite.ts`, `gallery.test.ts`, and the new
  `galleryPage.ts` and `galleryLinks.browser.test.ts`. None of the files the specification lists
  as not changed is in it.
- Search for `galleryPage` imports: only `test/site/buildSite.ts`, `gallery.test.ts` and
  `galleryLinks.browser.test.ts`. `RUN_FOLDER_PREFIX` is imported from
  `test/shared/captureRegistry`, not copied.
- Docs: the CONTRIBUTING paragraphs, the glossary term "Capture id", the `ci.yml` comment (comment
  only) and the CHANGELOG line ending `(CR-506 gallery-links, PR #526)` match the specification.

## 10. Evidence 4 and the requirement, D11 (c715355c) VERIFIED

- `just requirements-lint`: exit 0, `1227 requirements, 0 errors, 26 warnings`.
- `just requirements-update`: exit 0, 0 files, 0 indexes, 0 projections updated; tree clean.
- `just requirements-report`: exit 0; SwRS-MDOKFSTUDIO-CORE-096 covered, with its source file and
  both test files.
- `req_lifecycle: proposed`, derives from StRS-MDOKFSTUDIO-CORE-008, whose diff is the
  `derived_by` line and the generated link only; dated entry in `requirements/tiers/log.md`.
- Markers: `@implements_req` at `galleryPage.ts` lines 35 and 92; `@tests_req` on the six new unit
  tests and the browser test.
- Observation: lint warns W002 "body has no filled EARS expression" on CORE-096 (10 such warnings
  at head, 9 at base; other site requirements carry it; no guideline requires EARS).
- Observation for the restack: the CR log records that the CR-504 worktree also takes the id
  CORE-096. It is free at this base.

## 11. Evidence 5: preflight and CI (c715355c) VERIFIED

- `<folder>/work/gates/preflight-c715355.log`, first line `CR-506 chantier/batch-09/cr-506
  c715355c203d92df18200011749d1a73cead0ad9 just preflight`, last `exit 0 head c715355c...`:
  check-no-merge-commits passed, file sizes and unused exports ran (`no unused export in 401
  module(s)`), tests 5245 pass 5224 fail 0 skipped 21, requirements 0 errors, `ci-static:
  passed`; on Windows the other stages are skipped. This covers `just check`.
- `gh pr checks 526`: checks, report, static, static-windows, viewer-graph, visual pass;
  gallery, integration, stress, toc-loop, release-check, release, tag-release, pages skipping.
- `chantier.yaml` lists no long gate; none was run by this verification.

## 12. Review box (c715355c) VERIFIED

`chantier log CR-506` (read again in the description pass): `r3 inspector approved at
c1037ae378629aa4455b1acf62ea9712f90e1ced (CHANGELOG diff)` and `r3 approved at
c1037ae378629aa4455b1acf62ea9712f90e1ced, committed as
c715355c203d92df18200011749d1a73cead0ad9`; the body cites c1037ae committed as c715355.

## 13. The PR description (posted body, c715355c) VERIFIED

Judged again at c715355 on the body updated 2026-11-25T18:35:57Z (draft, head unchanged). Copy
read: `<folder>/work/verifier/pr-body-posted-pass2.log`.

Posted text and rendering:

- `gh pr view 526 --json body --jq .body | diff --strip-trailing-cr -B -
  <folder>/work/verifier/pr-body-posted-pass2.log`: exit 0; that copy compared the same way with
  `<folder>/work/pr-body.md`: exit 0.
- `gh api repos/gsemet/markdown-okf-schema-studio/pulls/526 -H "Accept:
  application/vnd.github.html+json" --jq .body_html` (`pr-body-rendered.log`): headings Summary,
  Deliverables, Changes, Impacts, Blast radius, Autonomous decisions, Test plan (the project
  template's sections in order, plus the project guideline's Autonomous decisions), both tables
  (the image table holds four `<img>`), six checked task items, one Mermaid section. The project
  template has no fold and no Known gaps section.
- `node render-mermaid.mjs <worktree> <body copy> pr-body-mermaid-2.png`: `mermaid blocks: 1`,
  eight messages drawn, `#35;` shows as `#`; image opened.

Images (project rule: screenshot branch, linked in Impacts):

- `curl` of the four URLs at `4abc9d62ba790cfb9b331dea20548900c7a0215a`: each `http=200
  type=image/png` (87922, 89075, 107768 and 104081 bytes).
- `cmp` of each with `evidence/<name>.png`: identical; `git hash-object --no-filters` equals the
  blob of `gh api .../git/trees/4abc9d6...`: before-viewer-next `ebaec18e`, after-viewer-next
  `d9ebb2d6`, before-unknown-id `c0d03907`, after-unknown-id `a8efba2d`. They are the captures of
  `before-after.md` (before at 4a47151, after at c715355), the SHAs the caption names.
- All four opened: Next with the address `gallery.html` (before) and
  `gallery.html#block-editing/r02-mod-enter-commit` (after), 24 of 610; `#nope/r99-gone` with
  nothing said (before) and the notice above the grid (after); the yellow strip the caption
  describes; legible; no username, no home folder path (addresses are `127.0.0.1`).

Text searches on the body copy:

- `grep -nEi "CR[- ]?[0-9]{2,}|batch|\bround\b|\.agents/changes|planning|<chantier role names>"`:
  no match (exit 1).
- `grep -nEi "<login name>|C:[\\/]Users|/home/|/Users/"`, and the login name alone: no match.
- `grep -nE "UNVERIFIED|STALE|carried"`: no match.

Consistency with the diff at c715355 (`git diff origin/main...HEAD`, `galleryPage.ts` read):

- Summary and Impacts: claims 4 (base behaviour, direct load, reload), 5, 8.
- Deliverables: the id table matches `captureId` (lines 36 to 41) and claim 1; the sequence
  diagram matches claims 4 and 5.
- Changes: links (claim 7), page script (lines 195 to 270, claim 5), notice (claim 6), duplicate
  ids (`assignCaptureIds`, claim 1), module move and browser test in `viewer-graph` with its
  comment (`package.json`, `ci.yml`), CONTRIBUTING and the glossary term. CHANGELOG and the
  requirement are named in Test plan. No delivered change is left out.
- Blast radius: grade 1; the diff touches no file under `src/`.
- Autonomous decisions: claims 8 (social card), 7 and lines 240 and 248 (modified clicks and
  arrows), 5 (close adds an entry), 10 (proposed).
- Test plan proofs and their SHA: new tests at c715355 failing on 4a47151 (claim 2; `git diff` of
  `gallery.test.ts` changes only the import of the two older tests); requirement and
  `requirements-update` at c715355 (claim 10); changelog line (diff: one entry under
  `## Unreleased`); preflight and `ci-viewer-graph` at c715355 (claims 11 and 3); review (claim
  12); CI green at c715355 (`gh pr checks 526`: checks, report, static, static-windows,
  viewer-graph, visual pass, the others skipping; `gh run view 45669698414`: headSha c715355,
  conclusion success).
- Known gaps: no `UNVERIFIED` claim, no pair `before-after.md` says was not captured (its
  after-only files have the before already shown by `before-unknown-id.png`), no failed claim
  accepted: nothing needs a bullet.

The three failures of the earlier pass are fixed: Impacts holds the before/after, the Test plan
proofs name their SHA, CONTRIBUTING, the glossary and the `ci.yml` comment are mentioned.

Observations, not failures: the hard-wrapped source lines render as forced line breaks on GitHub;
"sets the tab title to the capture id" is short for the title `<id> | gallery | Markdown
OKF-Schema Studio` (claim 4); "Local gates" gives results without test counts, which the project
template's comment suggests.

## Housekeeping

The base worktree `<worktree>/out/base` was removed. `<worktree>/out/reports` and
`<worktree>/out/site` (ignored build output) hold the artifact of run 45476952370. The images
downloaded by the description pass under `work/scratch/` were removed after the comparison.
`git status --porcelain` in `<worktree>`: empty.
