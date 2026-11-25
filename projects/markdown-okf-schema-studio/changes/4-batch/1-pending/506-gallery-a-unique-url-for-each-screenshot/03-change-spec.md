# Gallery: a stable link for each screenshot

Each screenshot of the published gallery (`gallery.html` on GitHub Pages) gets its own stable URL,
`gallery.html#<capture id>`. The URL opens that screenshot directly and changes as the reader moves
through the screenshots. Back and Forward step through what the reader saw, and the link can be
bookmarked, reloaded and shared. The gallery URLs published today keep working.

No tracker issue: the request was verbal.

## Goal, in the user's terms

Today a reader opens a screenshot of the gallery, moves with Previous and Next, and the address
never changes. A screenshot cannot be linked, bookmarked or reloaded, and Back leaves the gallery.
After the change:

- each screenshot has an address of its own, built from the scenario and step that took it, so the
  address stays the same from one CI run to the next;
- opening that address opens the gallery with that screenshot shown;
- moving to another screenshot changes the address; Back and Forward go through the screenshots
  seen, and through the grid;
- the address can be copied from the address bar or from the card ("Copy link address") and works
  for anyone who opens it;
- `gallery.html` with no fragment, the image URLs under `reports/e2e/screenshots/`, and the
  Markdown group pages under `reports/e2e/gallery/` keep the addresses they have today.

## What exists today (read-only investigation)

- `just ci-gallery` (justfile, CI job `gallery` in `.github/workflows/ci.yml`) and `just
  site-assemble` (used by `.github/workflows/pages.yml`, job `build-site`) run `just
  requirements-report`, `npm run site:gallery` (= `gallery:generate`: `scripts/generate-gallery.mjs`
  → `out/test/site/curateGallery.js` plus `scripts/generate-readme-images.py`, which curate the
  README images) and `npm run site` (`out/test/site/buildSite.js`).
- `test/site/buildSite.ts` writes `out/site/gallery.html` with `pageDocument("gallery",
  "gallery.html", buildGallery(), galleryPageCard)`. `buildGallery(screenshotRoot)` lists every
  png/jpg/jpeg/webp file under `out/reports/e2e/screenshots/` (`listCaptures`, in name order). Each
  file becomes a `<figure>` holding a `<button class="capture-open">`, the caption and a `<template
  class="capture-sidecar">`. One `<dialog class="capture-viewer">` holds the Previous and Next
  buttons, the position (`data-capture-position`), a close button, the sidecar panel and the image.
  An inline `<script>` opens the dialog at an index (`openCapture`) and handles ArrowLeft and
  ArrowRight, the close button and a backdrop click. **It never reads or writes the URL**: this is
  the defect.
- Capture paths under `out/reports/e2e/screenshots/`:
  - visual (mock host) captures: `visual/<scenario id>.png` and step images
    `visual/<scenario id>--<step>.png` (`test/visual/capture_support.py`). Scenario ids are
    `<group>/vNN-<slug>-<theme>-<width>` (`test/visual/scenarioIds.ts`); the groups come from
    `test/shared/e2eGroups.ts`.
  - real-window captures: `<run folder>/<group>/rNN-<slug>.png`. The run folder is
    `fs.mkdtempSync(<RUN_FOLDER_PREFIX[suite]>)` (`test/shared/evidenceStore.ts`), so it has a
    random suffix that changes on every run. `<group>/rNN-<slug>` is the permanent registry id of
    `test/shared/captureRegistry.ts` (`CAPTURES`, `RUN_FOLDER_PREFIX`).
  - any other path (legacy captures, other suites) is listed too.
- `test/site/gallery.test.ts` pins the gallery HTML (the counts, the sidecar, the navigation
  controls, the key handlers). `test/site/requirementsViewer/*.browser.test.ts` are the existing
  Chromium tests (playwright-core), run by `npm run test:viewer-graph` in `just ci-viewer-graph`
  with `STUDIO_REQUIRE_CHROMIUM=1`; elsewhere they skip, with a message, when no Chromium can start.
- The product-owner gallery (`test/site/poGallery.ts`, `npm run review:gallery`, the Markdown pages
  `out/reports/e2e/GALLERY.md` and `gallery/<group>.md`) is a separate set of Markdown pages, copied
  as raw files under `reports/`. It already has one stable file per group.
- Requirements: `StRS-MDOKFSTUDIO-CORE-008` ("A reviewer reads the published site and its
  requirements", `req_lifecycle: proposed`) covers the e2e gallery on GitHub Pages; no SwRS
  specifies the gallery viewer today.

## Decisions (answer Q1 of `02-answers.md`, carried in full)

Q1 says: one stable static URL per screenshot page, on GitHub Pages with no server rewrite, built
from the stable ids of the scenario and step; Back and a direct link work; the current URLs keep
working; the spec-writer picks the mechanism and names it. The decisions below carry it out.

- **D1. Mechanism: a URL fragment that opens the screenshot, not a static page per screenshot.**
  The URL is `gallery.html#<capture id>`. It is static: GitHub Pages serves the same
  `gallery.html` file, and the page script reads the fragment. No server rewrite and no new file
  per screenshot are needed. `gallery.html` stays the one page and URL it is today, and a link
  works on the downloaded site opened from disk as well. Rejected: one HTML page per screenshot
  (several hundred files per deploy, a second rendering path for the sidecar, and a new Open Graph
  card per screenshot, which is outside this request).
- **D2. The capture id, built from the stable ids of the scenario and step.** It is a pure function
  `captureId(relativePath)` of the path relative to the screenshot root (posix, file extension
  removed):
  1. `visual/<rest>` → `<rest>`. This is the scenario id, for example
     `block-editing/v01-paragraph-light-900`, or the scenario id plus `--<step>` for a step image.
  2. First segment starting with one of the `RUN_FOLDER_PREFIX` values of
     `test/shared/captureRegistry.ts` (imported, not copied) → the path without that segment. This
     is the registry id `<group>/rNN-<slug>`, the same for every run whatever the random suffix of
     the run folder.
  3. Any other path → the path itself (for example `real run/checkpoint`): stable as long as the
     file keeps its name.
- **D3. Ids are unique on a page.** When two captures get the same id (only when two runs of one
  suite sit under the screenshot root, which happens locally; the published site comes from one
  CI run's artifact), the first one in gallery order (name order, as today) keeps the short id.
  Each other one takes rule 3, its full path. If that is still taken, `~2`, `~3`… is appended, in
  gallery order. `buildGallery` assigns the ids, so the page and the tests see the same ones.
- **D4. Fragment encoding.** The fragment is the id with each `/`-separated segment encoded by
  `encodeURIComponent` and the `/` kept (`#block-editing/v01-paragraph-light-900`;
  `#real%20run/checkpoint`). The script decodes with `decodeURIComponent` inside `try`/`catch`; a
  fragment that does not decode counts as an unknown id (D7). The id is only ever written with
  `textContent`, an attribute value set through the DOM, or the escaped attribute of the
  generated HTML (`escapeHtml`). It never goes into `innerHTML`.
- **D5. Each card is a real link.** The `.capture-open` opener becomes `<a class="capture-open"
  href="#<encoded id>" data-capture-id="<id>" aria-label="Inspect <relative path>">`, with the
  same image inside. The `<figure>` also carries `data-capture-id`. A plain left click is
  intercepted (`preventDefault`) and opens the viewer as today. A middle click, or a click with
  Ctrl, Meta or Shift, is left to the browser, so "open in new tab" and "Copy link address" give
  the screenshot's URL. The styles of `.capture-open` keep the card look of the button
  (`display: block`, same focus outline); the cards look unchanged.
- **D6. History.**
  - Opening a screenshot from the grid, Previous, Next, ArrowLeft and ArrowRight each **push** a
    history entry whose URL is `#<id>` (`history.pushState`). Each screenshot is a page, so Back
    returns to the previous screenshot seen.
  - Closing the viewer (close button, backdrop click, Escape, handled on the dialog's `close`
    event) **pushes** the URL without a fragment (`location.pathname + location.search`). Back
    after a close reopens the screenshot just closed.
  - On `popstate` and `hashchange`, one idempotent `syncFromUrl()` shows the screenshot the
    fragment names (rendered, with `showModal` when the dialog is closed). With no fragment it
    closes the viewer. It never pushes: a close that `syncFromUrl` causes must not push a new
    entry.
  - On page load, `syncFromUrl()` runs once: `gallery.html#<id>` opens that screenshot. Reload
    keeps it open.
- **D7. Unknown id.** A fragment that names no capture (a screenshot renamed or removed since the
  link was shared) opens no viewer. A notice above the grid, `<p class="status" role="status"
  data-capture-missing>`, hidden otherwise, says: `The screenshot <id> is not in this gallery: it
  may have been renamed or removed.` (the id inserted as text). The grid shows as usual. Opening
  any screenshot or going back to a URL with no fragment hides the notice.
- **D8. Title and focus.** While a screenshot is shown, `document.title` is `<id> | gallery |
  Markdown OKF-Schema Studio`, so a bookmark carries the screenshot's name. On close it goes back
  to the page title. On close, the card of the last screenshot shown is scrolled into view
  (`block: "nearest"`) and its link gets focus.
- **D9. What does not change.** The order of the screenshots and Previous/Next (name order of
  `listCaptures`), the position text (`n of N`), the sidecar panel and the keyboard keys stay as
  they are. So do the grid at `gallery.html`, the social card of `gallery.html` (a shared
  `#<id>` link shows the gallery card) and the site header link. The `pages.yml` and `ci.yml` jobs
  that build the site do not change either.
- **D10. Code layout.** The gallery page code moves from `test/site/buildSite.ts` to a new
  `test/site/galleryPage.ts`: `listCaptures`, `buildGallery`, the new `captureId` and
  `assignCaptureIds`, and the inline script. `buildSite.ts` imports `buildGallery` and
  `listCaptures` from it and keeps the gallery CSS in `pageDocument` (the new rules for the
  `<a>` opener and the notice go there). Reasons: `buildSite.ts` is already long, and batch-09 CRs
  touch it too (CR-482 adds `siteClips.ts` beside it). The browser test can also import the page
  code without the site's main. `test/site/gallery.test.ts` then imports from `./galleryPage`.
  No other import of these names exists outside `test/site/`; `just check` (unused exports)
  confirms it.
- **D11. Requirement.** A new SwRS in `rendering-core`, `proposed`, `derives_from:
  [StRS-MDOKFSTUDIO-CORE-008]`. Its number is the next free `SwRS-MDOKFSTUDIO-CORE-NNN` at the
  base of the stack when the Driver creates it with `okfreq new … --lifecycle proposed` (CORE-095
  is already taken by batch-09 CRs; do not hard-code a number). Title: "Each screenshot of the site
  gallery has its own stable link". Normative text: each screenshot of the gallery SHALL have the
  URL `gallery.html#<capture id>`. The capture id SHALL be built from the scenario and step ids
  (D2, D3). Opening it SHALL show that screenshot. Moving to another screenshot SHALL change it.
  Back and Forward SHALL show the screenshots seen, and an unknown id SHALL show the notice and
  no viewer. Scenarios: nominal (direct link opens; Next changes the URL; Back returns), boundary
  (an id from a run folder with another random suffix gives the same URL; two runs of one suite
  give unique ids), refusal (unknown or malformed fragment: notice, no viewer).
  `implemented_in_files: test/site/galleryPage.ts`; `tested_in_files: test/site/gallery.test.ts,
  test/site/galleryLinks.browser.test.ts`. Markers `// @implements_req` on `captureId` and on the
  script builder in `galleryPage.ts`, `// @tests_req` on the tests below. StRS-CORE-008 stays
  `proposed`, not approved: no owner re-approval is needed. Its Main paths are not changed (the new
  SwRS "also serves this need"). Only its generated `derived_by` and Links change, through `just
  requirements-update`. A dated entry goes in `requirements/tiers/log.md`.

## What changes, file by file

- `test/site/galleryPage.ts` (new): `listCaptures` (moved, unchanged), `captureId(relative:
  string): string` (D2), `assignCaptureIds(relatives: readonly string[]): string[]` (D3),
  `captureHref(id)` (D4), `buildGallery(screenshotRoot)` (moved). Every figure and opener now
  carries the id and the `href` (D5). The output adds the `data-capture-missing` notice (D7) and
  the script is extended with `syncFromUrl`, the pushes, `popstate`/`hashchange`, the `close`
  listener, the title and focus (D6, D8). The JavaScript stays an inline `<script>` in the page,
  as today, so the page works opened from disk.
- `test/site/buildSite.ts`: imports from `./galleryPage`. Adds the CSS rules for `a.capture-open`
  (the card look of today's button: block, no underline, `cursor: zoom-in`, same `:focus-visible`
  outline) and for `[data-capture-missing][hidden]`. `main()` is otherwise unchanged.
- `test/site/gallery.test.ts`: imports from `./galleryPage`; existing assertions kept (the
  `class="capture-open"` count still holds), new unit tests below.
- `test/site/galleryLinks.browser.test.ts` (new): the Chromium test below.
- `package.json`: `test:viewer-graph` also runs `out/test/site/galleryLinks.browser.test.js`.
- `.github/workflows/ci.yml`: only the comment above the `viewer-graph` job, which now names the
  gallery link tests too. The job's steps stay the same.
- `CONTRIBUTING.md`: in the paragraph on `out/site/gallery.html` ("Selecting an image opens the full
  sidecar…"), add that each screenshot has the URL `gallery.html#<capture id>` and how the id is
  built (D2), and that Back and Forward step through the screenshots. In the CI paragraph,
  `ci-viewer-graph` also runs the gallery link tests in Chromium.
- `.agents/glossary/common.md`: new term **Capture id** (the id of D2/D3, and the URL fragment of
  a gallery screenshot).
- `CHANGELOG.md`: one user-facing line under `## Unreleased`, per "CHANGELOG line" in
  `.agents/guidelines/pull-request.guidelines.md`.
- `requirements/`: the new SwRS (D11), `just requirements-update`, the `log.md` entry.
- Not changed: `scripts/generate-gallery.mjs`, `test/site/curateGallery.ts`, `test/site/poGallery*.ts`,
  `.github/workflows/pages.yml`, the justfile, `README.md` (its link to `gallery.html` stays
  valid), the writing skill (no rendered syntax changes).

Commit type: `feat:` with no scope (the allowed scopes `vscode`, `render`, `editor`,
`frontmatter` do not cover the site), for example `feat: give each gallery screenshot its own
link`.

## CI job touched: `viewer-graph`

The job gets one more test file. Its environment does not change: `ubuntu-latest`, Node from
`.nvmrc`, `just dev-ci visual` (Chromium from Playwright, Ubuntu packages restored from the archive
cache the `visual` job saves), `STUDIO_REQUIRE_CHROMIUM=1`, so a Chromium that cannot start fails
the test there. The test needs nothing the job lacks: no network beyond `127.0.0.1`, no fonts
(it measures no geometry), no credentials, no e2e reports (it builds its own fixture screenshot
root). The `static` jobs (Linux and Windows) have no Chromium, so the test skips there with a
message, like the existing browser tests. Before the push it is proved by a local `just
ci-viewer-graph` on the Driver's machine (Windows, Chromium installed by `just dev`). Only the
job's first CI run proves the Linux runner (Chromium from the restored cache, headless,
`ubuntu-latest`).

No host and default matrix: the behaviour depends on neither a host (Claude Code or Copilot) nor a
configured value.

## Evidence

Each command runs at the pushed head; its output goes in the evidence.

1. Unit tests, `test/site/gallery.test.ts` (`npm run test:unit`, inside `just check`), on
   `buildGallery` and `captureId` as shipped, from a temporary screenshot root:
   - `visual/block-editing/v01-x-light-900.png` → `block-editing/v01-x-light-900`;
     `visual/block-editing/v01-x-light-900--typed.png` → `block-editing/v01-x-light-900--typed`.
   - for each suite of `SUITES`: `<RUN_FOLDER_PREFIX[suite]>AbC123/gfm/r01-task.png` →
     `gfm/r01-task`; the same file under a run folder with another suffix gives the same id and
     the same `href`.
   - `real run/checkpoint.png` → `real run/checkpoint`, with `href="#real%20run/checkpoint"`.
   - two run folders of one suite holding the same capture: the first in name order gets
     `gfm/r01-task`, the other its full path; every `data-capture-id` on the page is unique, and
     there are as many ids as `class="capture-open"` openers and as `listCaptures` entries.
   - the HTML holds the `data-capture-missing` notice (hidden), `history.pushState`, `popstate`,
     `hashchange` and the `close` listener. An id holding `<`, `&` or `"` appears escaped in
     the HTML.
2. Browser test, `test/site/galleryLinks.browser.test.ts` (playwright-core Chromium, the pattern of
   `test/site/requirementsViewer/idLayout.browser.test.ts`). It writes the page with the shipped
   `pageDocument` and `buildGallery`, from a temporary screenshot root that holds four small real
   PNGs (two visual, one real-window run folder, one legacy path) with JSON sidecars. It serves the
   folder with a `node:http` static file server on `127.0.0.1` (files only, no rewrite, as on
   GitHub Pages). It checks, each as its own step:
   1. `gallery.html` (no fragment): no dialog open, four cards, notice hidden. The current URL
      still works.
   2. Plain click on card 1: dialog open, URL ends `#<id 1>`, heading and `document.title` hold
      id 1, position `1 of 4`.
   3. Next, then ArrowRight: URL `#<id 2>`, then `#<id 3>`.
   4. `goBack()`: id 2 shown, URL `#<id 2>`. `goBack()` twice: URL with no fragment, dialog
      closed. `goForward()`: id 1 shown.
   5. Escape: dialog closed, URL with no fragment, focus on card 1's link. `goBack()`: id 1 shown
      again.
   6. A new page opened directly on `gallery.html#<id 3>` (the run-folder capture, its registry
      id): dialog open on it, position `3 of 4`. `reload()`: still open on it.
   7. A direct load of `gallery.html#nope/r99-gone`: no dialog, notice visible with `nope/r99-gone`
      as text. Same for a malformed fragment `#%E0%A4%A`: notice, no viewer, no page error. Then
      changing the hash to a known id opens it and hides the notice.
   8. The `href` of card 4 (legacy path with a space), resolved by the browser, is
      `<origin>/gallery.html#real%20run/checkpoint`, and loading it opens that screenshot.
   9. No `pageerror` event during the whole test.
   Command: `STUDIO_REQUIRE_CHROMIUM=1 npm run test:viewer-graph` and `just ci-viewer-graph`
   (output with `ci-viewer-graph: passed`). Without `STUDIO_REQUIRE_CHROMIUM`, when no Chromium
   starts, the test skips with a message, like the other browser tests.
3. The real site, from a real CI artifact. Download the reports artifact of the latest green heavy
   run of `main` (`gh run download <run id> -n <reports artifact> -D out/reports/`), run `just
   site-assemble` and serve `out/site` with a static file server. Then:
   - count the `data-capture-id` values in `out/site/gallery.html` and check they are all unique
     and as many as the screenshots (a one-line `node -e` script, output kept);
   - open `gallery.html#<a real visual scenario id>`, `gallery.html#<a real visual step id>` and
     `gallery.html#<a real registry id, for example block-editing/r01-paragraph-blur-commit>`:
     each opens that screenshot. Capture one screenshot of the open viewer with the address bar
     or the URL shown, for the PR's before/after (before: `main`'s page, where Next leaves the URL
     unchanged).
4. `just requirements-lint` and `just requirements-update` clean, with the new SwRS listed with
   its source and test markers; `just check` passes (markers, unused exports, file size limits).
5. `just preflight` (on Windows the static stage; CI runs the other stages, and `viewer-graph`
   runs the new test on Linux).

The guarded file is the shipped page code. Every check above builds the page with the shipped
`test/site/galleryPage.ts` and `pageDocument` at the head under test, never a copy of the script.
The temporary screenshot roots hold only input data (fixture PNGs and sidecars).

## Out of scope

- One HTML page or one social card per screenshot (D1).
- Stable links inside the product-owner Markdown gallery (`GALLERY.md`, `gallery/<group>.md`).
- A "copy link" button: the address bar and the card's link already give the URL (D5).
- Changing the order, grouping or filtering of the screenshots, and changing which captures the
  site lists (historical captures stay listed, as today).
- Any change to `pages.yml`, to the CI jobs that build the site, or to how reports are selected.

## Open questions

None. The owner asked for no questions; every gap is decided above (D1 to D11).
