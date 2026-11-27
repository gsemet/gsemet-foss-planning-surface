# CR-522 verification

Head: 8541bedf7295b79a55d110b9b2117d18b1cda551

Result in one line: the product claims 1 to 6 hold at the head; claim 7 (the PR body) fails on four
points, all fixable in the body with no new commit.

Paths: `W` = the CR worktree, `CR` = the CR folder, `V` = `CR/work/verifier`, logs in `V/logs/`.
All claims judged at `8541bed`; none is carried.

## 0. Head, tree, PR, gate, CI (at 8541bed)

- `git rev-parse HEAD`; `git status --porcelain` -> `8541bedf7295b79a55d110b9b2117d18b1cda551`, empty
  (also empty after every build and test run below).
- `git log --oneline origin/main..HEAD` -> `8541bedf docs: name the pull request in the changelog
  line`, `5ed85509 feat: add a video gallery to the site and five clips to the README`; merge base
  `6b1dd90`.
- `gh pr view 555 --json isDraft,baseRefName,headRefOid,mergeable` -> draft true, base main, head
  8541bed, MERGEABLE.
- Completion gate: `CR/work/preflight-8541bed.log`, first line
  `head 8541bedf7295b79a55d110b9b2117d18b1cda551`; line 6007 `298 passed`; line 6011
  `1231 requirements, 0 errors, 26 warnings`; line 6106 `ci-static: passed`; line 6107
  `preflight: visual, viewer-graph, integration, acceptance, report and gallery stages skipped on
  Windows; CI runs them`. Not rerun by me. `chantier log CR-522` note: `short gate at 8541bed
  (completion gate, just preflight, static stage on Windows): pass`.
- `gh pr checks 555` -> pass: checks, report, static, static-windows, viewer-graph, visual, visual-2;
  skipping: acceptance, gallery, integration, pages, perf-547, release, release-check, stress,
  tag-release, toc-loop. The viewer-graph job log (job 140564758039) holds the two Videos page
  browser tests, `tests 18, pass 18, fail 0, skipped 0`.

## 1. PASS: the built videos.html holds 18 cards (8541bed)

- Build: `npm run site` in W -> `Built static site at ~\...\batch-11-CR-522\out\site`, exit 0
  (`site.log`). `just site-assemble` stops here at `Cannot curate E2E gallery: the final review
  report is missing` (`site-assemble.log`): it needs real VS Code reports; that script is not
  changed by the CR.
- `python -I V/static_checks.py W` (`static-checks.log`, `failures: 0`): 18 cards (found 18);
  `short-demo-01` first, then the 17 clip folders with a WebM in name order; every card `controls`,
  `preload=none`, `playsinline`, a poster, no `autoplay`; `loop`+`muted` on the 17 clips only;
  source and fallback link; site media byte-equal to the repository files; titles equal the clips'
  `Text 1`; `One-minute demo` for the presentation video; manifest lists `videos.html` and
  `og/videos.png` (a PNG); og description says `18 videos`.
- Boundary S4, the half no test runs: `node --import ./scripts/register-myst-patches.mjs -e
  <writeVideosAndManifest on an empty tree>` (`no-video-build.log`) -> exit 0, `<figure 0`,
  `<video 0`, h1 true, `pages index.html,videos.html`.
- Poster of the presentation video (`poster.log`): ffmpeg PSNR of frame 0 against `poster.png`
  `inf`, 1920x1080; LFS pointer oid `673a8e63...` equals the file's sha256; `git -c
  lfs.storage=<empty dir> lfs fetch origin <head> --include poster.png` retrieved it, exit 0.

## 2. PASS: nothing loads before a click, a click plays (8541bed)

`node V/browser_checks.cjs W`, the built site served on 127.0.0.1 (`browser-checks.log`,
`failures: 0`), in Playwright Chromium 156.0.8078.4 and installed Chrome 158.0.8127.37, both
headless (Edge not installed):

- After load, a full scroll and 5 s: 18 videos paused, `readyState 0`, `server log [], page
  requests 0` for .webm/.mp4; 18 posters requested; no page error.
- Each of the 18 cards on a fresh page, real mouse click at the picture's middle: `requests before
  click 0`, then playing, only that card's file requested, `others touched 0`; second click pauses
  (one pause event), third plays.
- Space bar on an unloaded video plays then pauses; the native play button plays.
- Scripts disabled: a click on a picture requests nothing (the Known issue of CORE-098).
- Pause while loading: page error `The play() request was interrupted by a call to pause()` (the
  Known gap, reproduced).
- Home page: the five README clips are autoplay, loop, muted videos in README order and play once
  in view.

## 3. PASS: seven header links (8541bed)

`static_checks.py`: 650 html files, 649 with the site header (576 requirements pages), the one
without is the `requirements.html` redirect; every header holds `Home, Contributing, How we ship,
How we test, Gallery, Videos, Requirements` in order, each resolving to an existing file, 0 bad.
Before at `6b1dd90`: `GET videos.html 404`, six links (`before-after.log`).

## 4. PASS: README (8541bed)

`static_checks.py` section (4): exactly five GIFs, line 68 `table-anchors` (Highest respect for the
raw Markdown), 87 `slash-menu-grid` and 91 `figure-editor` (Edit MyST visually, right after the
editing still, each with a lead-in), 130 `diff-side-by-side` (See what changed since the last
commit), 161 `radio-buttons` (Decide in the page); real GIFs, alt = Text 1. Text 2; total 7239128
bytes. `showcase-diff-cream.png`, `radio-plan-cream.png`, `radio-plan-dark.png` unreferenced, files
and `README_BY_ID` entries kept (`test/visual/scenarioIds.ts:1007-1010`; no diff under `images`,
`test/visual`, `scripts`). Demo title and link on lines 22 and 24, before the first `## ` (line 30),
link unchanged. Line 7 links `videos.html` after the gallery link. No added prose line over 100
columns.

## 5. PASS: VSIX (8541bed)

`just package` -> `DONE Packaged: out/reports/package/markdown-okf-schema-studio.vsix (253 files,
8.93 MB)`, exit 0 (`package.log`). `static_checks.py` section (5): `extension/readme.md` points the
five GIFs to
`https://media.githubusercontent.com/media/gsemet/markdown-okf-schema-studio/v1.13.0/docs/demo-video/clips/<clip>/<clip>.gif`;
no relative demo-video link left; no `docs/demo-video` entry and no gif, webm or mp4 in the VSIX.

## 6. PASS: screenshots (8541bed, before at 6b1dd90)

- `node V/shots.cjs W CR/evidence` (`shots.log`): `18 videos, 18 paused and unloaded at capture;
  video requests 0`; each README section with its GIFs loaded, `failed none`.
- Mine, in `CR/evidence/`: `videos-page-top.png`, `videos-page.png`, `readme-raw-markdown.png`,
  `readme-edit-myst.png`, `readme-diff.png`, `readme-radio.png`. Not mine (earlier steps, not used
  as proof): `click-probe.txt`, `click-script-probe.txt`, `packaged-readme-gif-urls.txt`,
  `videos-page-checks.txt`, `short-demo-01-poster.png` (its sha256 equals the committed poster).
- Before and after pairs in `V/evidence/`, listed in `before-after.md` (`before_after.cjs`,
  `before-after.log`).
- I opened every picture in both folders (the `after-readme-*` and `after-videos-*` files are
  byte-identical, by sha256, to those in `CR/evidence/`): none shows the user name or the home
  folder. `grep -rIicE <user names> V CR/evidence` -> no match, after replacing home paths in my own
  logs with `~`.
- README pictures are a local markdown-it rendering, not GitHub's.

## 7. FAIL: the PR body against the diff (body read at 8541bed, updated 2026-11-27T14:29:57Z)

`gh pr view 555 --json body`; rendered HTML by `gh api repos/.../pulls/555 -H "Accept:
application/vnd.github.full+json"` (`pr-555.json`).

### Defects

1. **Deliverables table is wrong.** Row `Edit MyST visually | one still | the same still, then slash
   menu grid and figure editor GIFs`. `git show 6b1dd90:README.md` has three pictures in that
   section: line 81 `showcase-myst-edit.png`, line 90 `myst-cards-tabs-cream.png` and
   `myst-cards-tabs-dark.png`; all three remain at head (lines 83 and 100). Picture:
   `before-readme-edit-myst.png` (`3 images`). Fix: Before "three stills (the editing still and a
   Cream and Dark pair)", After "the same three, with the two GIFs after the editing still".
2. **Impacts has no evidence.** `.agents/guidelines/pull-request.guidelines.md`: "Impacts holds the
   evidence of the change [...] or one line 'No visual change' [...]; the Verifier fails a body whose
   Impacts has neither." The body has neither (`img 0` in the rendered HTML). The specification
   ("Evidence") also asks the PR for the screenshots. Fix: attach the pairs of `V/evidence/`, with
   the SHAs.
3. **A requirements statement is false.** Test plan: "markers in code and tests [...] the header
   requirement: `test/site/siteHeader.ts` and the header link tests". `grep -nE
   'implements_req|SwRS|StRS' test/site/siteHeader.ts` -> no match; the frontmatter of CORE-086 has
   `implemented_in_files: - test/site/siteTheme.ts` only (marker at `siteTheme.ts:60`). The test
   half is true. Fix: name `siteTheme.ts` as the marked code file (unchanged here), or drop
   `siteHeader.ts` from the claim.
4. **A proof names a passed-over SHA.** "Local gates: `just check` (298 release tests among them) and
   `just preflight` [...] pass at 5ed8550". The head is 8541bed and the line says nothing of a carry
   (chantier `help verifier-description`). The proof at the head exists:
   `preflight-8541bed.log` runs `just check` (298 passed) inside `ci-static: passed`. Fix: "pass at
   8541bed".

### Statements that hold

- Summary, Deliverables diagram (parses with mermaid 12.2.0, names exist), other three table rows
  (`before-after.log`: 0, 1 and 2 pictures at the base).
- "17 short feature clips and a one-minute demo": 17 folders with a WebM; `ffprobe` duration
  57.515 s.
- Changes, all bullets: claims 1 to 4 above; `git diff --name-only origin/main..HEAD -- src` -> 0
  files. Not mentioned, minor: `package.json` adds the browser test to `test:viewer-graph`.
- Impacts text: claims 2, 4, 5. "About 7.3 MB" measures 7.24 MB (7239128 bytes).
- Blast radius: no file under `src/`.
- Test plan, "they fail on the previous code": head's seven changed or new test files copied onto
  `6b1dd90`, `npx tsc -p .`, `STUDIO_REQUIRE_CHROMIUM=1 node scripts/node-test.mjs verifier-base
  ...` (`tests-on-base.log`) -> `tests 42, pass 33, fail 9`: both new gallery files (`Cannot find
  module './videoGalleryPage'`), three README tests, four header assertions fail. Passing there, as
  expected of guards: the 100-column README test and the `pages.test.ts` tests. At head the same
  files (`tests-on-head.log`) -> `tests 48, pass 48, fail 0, skipped 0`.
- Requirements: ids CORE-098 (new), CORE-086, CORE-095, StRS CORE-008 are in the diff; CORE-098
  lists exactly the four files named, with markers; `requirements-lint` in the gate log, 0 errors
  (`update-coverage --check` included).
- Changelog: one bullet under Unreleased, ending `(CR-522 pages-video-gallery, PR #555)`.
- Review "approved at 8541bed": `chantier log CR-522`, `r3 approved at 5ed8550987..., committed as
  8541bedf`.
- Autonomous decisions: header order (code), titles (`videoGalleryPage.ts:49` and `Text 1`),
  placements (claim 4), 16:9 uncropped (CSS; posters 17x 1280x720, 1x 1920x1080), poster (claim 1),
  stills kept (claim 4).
- Known gaps: Chromium only (the test launches `chromium` only; I ran Chromium and Chrome only);
  unhandled rejection (claim 2); no test runs the build with no video (`videoGalleryPage.test.ts`,
  S4 calls only `listVideos` and `buildVideoGallery`; the build test adds a clip); no Pages dry run
  (`gh run list --branch <branch>` -> two CI `pull_request` runs only).
- "CI green" is unchecked: not a false claim; the seven checks that ran pass at the head.
- Rendering: nine sections, table, Mermaid block and six checkboxes render.

### Remarks, not failures

- Known gaps could name the scripts-disabled limit recorded in CORE-098.
- The body's hard-wrapped lines show as line breaks on GitHub (27 `<br>`).
- `test/site/siteHeader.ts` carries no requirement marker; it carried none before this CR.

NOT VERIFIED
