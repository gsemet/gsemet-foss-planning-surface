# CR-506 verification

Head: c715355c203d92df18200011749d1a73cead0ad9

Verdict: NOT VERIFIED

Every product claim and the five evidence items of the specification pass at this head. The one
failure is the PR description (claim 13); it is fixed by editing the body only, with no commit.

- Base: `4a47151e8d055b7f096b69b1fca2d9bf9636f863` (origin/main). `<worktree>` is the CR worktree,
  `<folder>` the CR folder. Logs are under `<folder>/work/gates/`, probe scripts under
  `<folder>/work/verifier/`, captures under `<folder>/work/verifier/evidence/`.
- Every claim below is judged at `c715355c203d92df18200011749d1a73cead0ad9`; none is carried.
- `git rev-parse HEAD` in `<worktree>`: `c715355c203d92df18200011749d1a73cead0ad9`.
  `git ls-remote origin "refs/heads/chantier/batch-09/cr-506*"`: the same SHA.
  `gh pr view 526`: head the same, draft true, state OPEN.

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

`chantier log CR-506`: `r3 inspector approved at c1037ae378629aa4455b1acf62ea9712f90e1ced
(CHANGELOG diff)` and `r3 approved at c1037ae..., committed as c715355c...`; the body cites
c1037ae committed as c715355.

## 13. The PR description (posted body, c715355c) NOT VERIFIED

Checked: `gh pr view 526 --json body` equals `<folder>/work/pr-body.md`
(`diff --strip-trailing-cr -B`, exit 0). The HTML GitHub renders (`gh api .../pulls/526`, accept
`application/vnd.github.html+json`) has the sections, the table and the task list; the Mermaid
block renders with the repository's mermaid and `#35;` shows as `#` (`pr-body-mermaid.png`). No
image attached, no username or home path. No `UNVERIFIED` claim and no `STALE` mark; the project
template has no Known gaps section and no fold.

Failures:

1. Impacts has neither the before/after nor "No visual change". The project rule
   (`.agents/guidelines/pull-request.guidelines.md`, and the template's Impacts comment) asks for
   screenshots of a visible change, and the guideline says the Verifier fails such a body. The
   change is visible (the notice; the address). Fix: push the pairs of
   `evidence/before-after.md` to the screenshot branch `<change branch>-assets` as the guideline's
   "Screenshots in the PR" says, and link `before-viewer-next` / `after-viewer-next` and
   `before-unknown-id` / `after-unknown-id` in Impacts, captioned before at `4a47151`, after at
   `c715355`. Note that the yellow address strip was added by the capture script.
2. Proofs without a SHA in Test plan. Write: "New or changed tests: at c715355; they fail on the
   previous code (4a47151)"; "`just requirements-update` clean at c715355"; "`just
   ci-viewer-graph` passes at c715355" in place of "passed on the same code before the commit"
   (claims 2, 10 and 3 prove them).
3. Delivered changes the body does not mention: the CONTRIBUTING.md paragraphs and the glossary
   term "Capture id" (and the `ci.yml` job comment). Fix: one Changes bullet, "CONTRIBUTING and
   the glossary describe the capture id and the link tests".

To tidy in the same edit, not failures: "CI green" is unchecked although `gh pr checks 526` is
green at c715355 (check it, "at c715355"); the body's hard-wrapped lines render as forced line
breaks on GitHub (one line per paragraph or bullet avoids it).

## Housekeeping

The base worktree `<worktree>/out/base` was removed. `<worktree>/out/reports` and
`<worktree>/out/site` (ignored build output) hold the artifact of run 45476952370.
`git status --porcelain` in `<worktree>`: empty.
