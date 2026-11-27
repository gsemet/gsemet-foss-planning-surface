# CR-522 verification

Head: 8541bedf7295b79a55d110b9b2117d18b1cda551

Result in one line: the product claims 1 to 6 hold at the head (carried), and the PR body posted at
2026-11-27T15:09:23Z passes claim 7: the four earlier defects are fixed.

Paths: `W` = the CR worktree, `CR` = the CR folder, `V` = `CR/work/verifier`, logs in `V/logs/`.
Claims 1 to 6 are carried from the earlier pass at the same head. Sections 0 and 7 are judged in the
description pass.

## 0. Head, tree, PR, gate, CI (at 8541bed)

- `git rev-parse HEAD`; `git status --porcelain` -> `8541bedf7295b79a55d110b9b2117d18b1cda551`, empty
  (checked again after the one probe of claim 7). `git ls-remote origin <branch>` -> 8541bed.
- `git merge-base origin/main HEAD` and `git rev-parse origin/main` -> `6b1dd90`. Two commits above
  it: `5ed85509 feat: add a video gallery to the site and five clips to the README`, `8541bedf docs:
  name the pull request in the changelog line`.
- `gh pr view 555` -> draft true, base main, head 8541bed, title `feat: add a video gallery to the
  site and five clips to the README`.
- Completion gate: `CR/work/preflight-8541bed.log`, first line
  `head 8541bedf7295b79a55d110b9b2117d18b1cda551`; line 6007 `298 passed`; line 6106
  `ci-static: passed`; line 6107 `preflight: visual, viewer-graph, integration, acceptance, report
  and gallery stages skipped on Windows; CI runs them`. Not rerun by me. `chantier log CR-522`:
  `short gate at 8541bed (completion gate, just preflight, static stage on Windows): pass`.
- `gh pr checks 555` -> pass: checks, report, static, static-windows, viewer-graph, visual, visual-2;
  skipping: acceptance, gallery, integration, pages, perf-547, release, release-check, stress,
  tag-release, toc-loop. The viewer-graph job log (job 140564758039) holds the two Videos page
  browser tests, `tests 18, pass 18, fail 0, skipped 0` (carried from 8541bed: same run).

## 1. PASS: the built videos.html holds 18 cards (carried from 8541bed: same head, no new commit)

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

## 2. PASS: nothing loads before a click, a click plays (carried from 8541bed: same head)

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

## 3. PASS: seven header links (carried from 8541bed: same head)

`static_checks.py`: 650 html files, 649 with the site header (576 requirements pages), the one
without is the `requirements.html` redirect; every header holds `Home, Contributing, How we ship,
How we test, Gallery, Videos, Requirements` in order, each resolving to an existing file, 0 bad.
Before at `6b1dd90`: `GET videos.html 404`, six links (`before-after.log`).

## 4. PASS: README (carried from 8541bed: same head)

`static_checks.py` section (4): exactly five GIFs, line 68 `table-anchors` (Highest respect for the
raw Markdown), 87 `slash-menu-grid` and 91 `figure-editor` (Edit MyST visually, right after the
editing still, each with a lead-in), 130 `diff-side-by-side` (See what changed since the last
commit), 161 `radio-buttons` (Decide in the page); real GIFs, alt = Text 1. Text 2; total 7239128
bytes. `showcase-diff-cream.png`, `radio-plan-cream.png`, `radio-plan-dark.png` unreferenced, files
and `README_BY_ID` entries kept (`test/visual/scenarioIds.ts:1007-1010`; no diff under `images`,
`test/visual`, `scripts`). Demo title and link on lines 22 and 24, before the first `## ` (line 30),
link unchanged. Line 7 links `videos.html` after the gallery link. No added prose line over 100
columns.

## 5. PASS: VSIX (carried from 8541bed: same head)

`just package` -> `DONE Packaged: out/reports/package/markdown-okf-schema-studio.vsix (253 files,
8.93 MB)`, exit 0 (`package.log`). `static_checks.py` section (5): `extension/readme.md` points the
five GIFs to
`https://media.githubusercontent.com/media/gsemet/markdown-okf-schema-studio/v1.13.0/docs/demo-video/clips/<clip>/<clip>.gif`;
no relative demo-video link left; no `docs/demo-video` entry and no gif, webm or mp4 in the VSIX.

## 6. PASS: screenshots (carried from 8541bed: same head; before at 6b1dd90)

- `node V/shots.cjs W CR/evidence` (`shots.log`): `18 videos, 18 paused and unloaded at capture;
  video requests 0`; each README section with its GIFs loaded, `failed none`.
- In `CR/evidence/`: `videos-page-top.png`, `videos-page.png`, `readme-raw-markdown.png`,
  `readme-edit-myst.png`, `readme-diff.png`, `readme-radio.png`. Other files there are from earlier
  steps.
- Before and after pairs in `V/evidence/`, listed in `before-after.md` (`before_after.cjs`,
  `before-after.log`).
- Every picture in both folders was opened: none shows the user name or the home folder.
- README pictures are a local markdown-it rendering, not GitHub's.

## 7. PASS: the PR description, judged whole (at 8541bed, body updated 2026-11-27T15:09:23Z)

`gh pr view 555 --json body,updatedAt,headRefOid` -> body equal to `CR/work/pr-body-posted.md`
(`equals pr-body-posted.md True`). `gh api repos/.../pulls/555 -H "Accept:
application/vnd.github.full+json"` for the rendered HTML
(`CR/work/scratch/attachments-8541bed/meta/pr-555-full.json`).

### The four earlier defects

1. Fixed. Row `Edit MyST visually` reads three stills before, the same three plus the two GIFs after.
   `git show 6b1dd90:README.md` has pictures on lines 81 and 90 (two on line 90) in that section;
   `git diff origin/main..HEAD -- README.md` only adds there. Pictures 07 and 08 show it.
2. Fixed. Impacts holds 12 pictures (see below).
3. Fixed. `grep -rnE SwRS-MDOKFSTUDIO-CORE-086 test` -> `implements_req` at
   `test/site/siteTheme.ts:60`, `tests_req` in `write.test.ts`, `siteLinks.test.ts`,
   `siteTheme.test.ts`; `siteTheme.ts` is not in `git diff --stat origin/main..HEAD`. The body says
   exactly that.
4. Fixed. "passes at 8541bed": the gate log of section 0; `justfile:528-535` (preflight runs
   `ci-static`, stops there on Windows), `:313` (`ci-static` runs `just check`), `:179` (`check`
   runs `release-tests`: 298 passed).

### Pictures

- `python -I V/body_pass.py <pr json> <download dir> V/evidence` (`body-pass.log`): 12 markdown
  images, 12 distinct `user-attachments` URLs, each HTTP 200 `image/png` without credentials; each
  download equals one evidence file by sha256, under the matching alt text and table cell;
  `evidence pictures 12 attached and matched 12 unused []`.
- Rendered HTML: `img 12`, nine `h2` sections, 2 tables, Mermaid present, `checkboxes 6 checked 6`,
  `br 0`, `literal ![ 0`, `relative evidence paths 0`; the 12 rendered sources answer 200.
- I opened the 12 downloads: none shows the user name or the home folder (`~/.claude/workflows/` is
  text of the demo page). Each shows what its caption says: the Videos page with posters and nothing
  playing; six then seven header links; the four README pairs.
- Captions name their SHAs: `before at 6b1dd90, after at 8541bed`. The Videos page has no before
  (404 at the base), and the body says it did not exist.

### Statements

- Summary, Deliverables (diagram names exist; four table rows), Changes: `git diff --stat` (27
  files, none under `src/`), diffs of `package.json` (browser test added to `test:viewer-graph`),
  `ci.yml` (comment only), `how-we-test.md`, `CONTRIBUTING.md`, glossary, README; the click script
  read at `test/site/videoGalleryPage.ts:72-82`. No delivered change is left unmentioned.
- Impacts: claims 2, 4, 5. "the browser's controls and the space bar work as usual":
  `browser-checks.log` (play button, space) and `CR/evidence/click-script-probe.txt` (timeline, full
  screen, mute; on an unloaded video the other controls load nothing, the native behaviour).
- Blast radius: no file under `src/`.
- Test plan: new tests fail on the old code (carried from 8541bed: `tests-on-base.log`, 42 tests,
  9 fail; `tests-on-head.log`, 48 pass); requirements (defect 3 above, CORE-098 files carried);
  changelog diff, one bullet under Unreleased; local gates (defect 4); `Review: approved at 8541bed`
  against `chantier log CR-522`, `r3 approved at 5ed8550987..., committed as 8541bedf`; CI line equal
  to `gh pr checks 555` (section 0). No `STALE` or `UNVERIFIED` mark; the body's only short SHAs are
  `6b1dd90` and `8541bed`.
- Autonomous decisions: match `02-answers.md` (routine gaps) and the coder notes; claims 1 and 4.
- Known gaps, each bullet:
  - Chromium and Chrome only: claim 2; `click-script-probe.txt` (`msedge ... cannot launch`).
  - Scripts disabled: `node V/nojs_play.cjs W` on the built page (`nojs-play.log`, `failures: 0`),
    Chromium 156 and Chrome 158, `javaScriptEnabled: false`: picture click requests `[]`, then the
    play button requests the clip, `paused=false t=1.52` / `t=1.46`.
  - Unhandled rejection on pause while loading: claim 2.
  - No test of the build with no video: carried from 8541bed (`videoGalleryPage.test.ts` S4).
  - Full gallery build not run locally: `site-assemble.log` fails for the missing report. No Pages
    dry run: `gh run list --branch <branch>` -> two CI `pull_request` runs only.
  - Real VS Code jobs skipped: `gh pr checks 555`.
- No internal reference before "Internal references" (regex scan: none), no role name anywhere, no
  user name or home path (`Grep` on the posted body: 0).

### Remarks, not failures

- Summary, "the README showed its features only as still pictures": true of the feature sections; the
  base README also has the "One-minute demo" video link near the top (`6b1dd90:README.md` lines
  22-24), which the same sentence counts among the videos.
- "about 7.3 MB" measures 7.24 MB (7239128 bytes).
- Internal references names `CR-522` without its slug `pages-video-gallery`.
- No "Human decisions" section, though the owner's grill answers shape the change. The project's PR
  template has none; the chantier template would add it where the project is silent.
- Pictures were attached with `gh pr edit --attach`, while `pull-request.guidelines.md`
  ("Screenshots in the PR") says side-branch blobs. The project rule ranks higher; the conflict is
  noted in the CR log. The attachments resolve publicly.

## Conduct

One no-op shell command of mine created an empty file `unused` in the user's temp folder, outside
`writes:`; its creation time showed it was new, and I removed it at once. No build, gate or test was
run in this pass; the one browser probe is `nojs_play.cjs`.

VERIFIED
