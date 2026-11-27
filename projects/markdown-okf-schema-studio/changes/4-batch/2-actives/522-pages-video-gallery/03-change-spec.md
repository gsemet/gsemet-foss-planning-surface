# A video gallery on the Pages site, and five clip GIFs in the README

## Goal

A visitor of the project's GitHub Pages site finds every video of the application in one place: a
new page, **Videos**, reached from its own link in the site header. It shows the feature clips and
the presentation video, each as a still picture that starts playing on a click. A reader of the
README sees five features in motion, as the clips' existing GIFs, in the section of each feature;
the one-minute demo video stays at the top of the README.

Facts read at `origin/main` `b9b29c5a`. This change request lands on top of CR-521 in the batch's
stack (CR-521 also edits `requirements/`, `requirements/tiers/log.md` and `CHANGELOG.md`): rebase on
it and take the next free requirement id at that point.

## Decisions (from `02-answers.md` and `intake/request.md`)

1. Priority P2 (owner, 2026-11-26); destination: the running batch, batch-11 (owner, 2026-11-27).
2. The gallery shows every feature clip (17 at `origin/main`) and the presentation video; a new clip
   enters it with no code change (`vidéos-Q1`, count corrected in "After the first specification").
3. It is a page of its own, with its own **Videos** link in the site header (`vidéos-Q2`).
4. A video shows a still picture and starts on a click (`vidéos-Q3`).
5. The README GIFs are part of this change request (`vidéos-Q4`).
6. The README shows the GIFs of `slash-menu-grid`, `table-anchors`, `figure-editor`,
   `diff-side-by-side` and `radio-buttons` (`vidéos-Q5`, `vidéos-Q6`): the existing files, none
   regenerated (`vidéos-Q7`).
7. The one-minute demo video stays at the top of the README: the project's current rule (feature
   clip guideline), stated in `vidéos-Q8`, not a separate owner decision.
8. Placement, decided by the Chief of Staff as a routine gap (`vidéos-Q8`): each GIF goes in the
   section of its feature, in place of the still picture that shows the same thing, else added to
   that section.
9. `table-anchors` goes in "Highest respect for the raw Markdown", a Chief of Staff decision
   (routine gap, "After the first specification"): the clip shows the raw table following the drag.

## Facts that shape the change

- `origin/main` has 17 clip folders under `docs/demo-video/clips/`, each with a `<clip>.webm` and a
  `poster.png` (frame 0). The gallery lists what the folder holds when the site is built.
- The presentation video is `docs/demo-video/short-demo-01/output/short-demo-01.mp4` (Git LFS,
  12 MB). It has no WebM and no poster file.
- The site is built by `test/site/buildSite.ts` (`npm run site`, `just site`, `just site-assemble`).
  `test/site/siteClips.ts` copies each clip's WebM, GIF and poster into the site (`copyClipMedia`)
  and turns a page image of a clip GIF into a looping, autoplaying `<video>` (`clipVideos`, SwRS
  CORE-095). The README is rendered as `index.html` by the same path, so the five README GIFs
  become autoplaying looping videos on the site's home page (CORE-095 behaviour). Click-to-play
  (decision 4) is decided for the gallery page.
- `.github/workflows/pages.yml` checks out with `lfs: true` and runs `git lfs pull`: the MP4, the
  WebMs and the posters reach the site build.
- `scripts/package-extension.mjs` passes `--baseImagesUrl https://media.githubusercontent.com/media/
  <repo>/v<version>/` to vsce. The packaged README then loads the GIFs from Git LFS through that
  host, and `.vscodeignore` keeps `docs/demo-video/**` out of the VSIX.
- `images/readme/showcase-diff-cream.png`, `radio-plan-cream.png` and `radio-plan-dark.png` are
  generated from visual scenarios (`README_BY_ID` in `test/visual/scenarioIds.ts`,
  `scripts/generate-readme-images.py`). The README is the only page that shows them.

## What changes

### The Videos page (`out/site/videos.html`)

- New module `test/site/videoGalleryPage.ts`, next to `galleryPage.ts`:
  - `listVideos(extensionRoot)`: the presentation video first, if
    `docs/demo-video/short-demo-01/output/short-demo-01.mp4` exists. Then one entry for each folder
    `docs/demo-video/clips/<clip>/` that holds `<clip>.webm`, in name order. The poster is
    `poster.png` when present. The title is the text of the clip's first `| Text 1 *(on screen)* |`
    row in `clip.md`, without `**`; with no such row, the title is the clip name. The clip name is
    the second line. A folder without a WebM is skipped (it cannot play). Nothing is hard-coded: a
    new clip folder appears on the next build.
  - `buildVideoGallery(videos)`: the page body, an `<h1>Videos</h1>`, a one-line intro and a
    `.gallery` grid of `<figure id="<clip>">` cards. Each card holds
    `<video controls preload="none" playsinline poster="...">` with the WebM (clips) or the MP4
    (presentation video) as source, then `<figcaption>` with the title (`h2`) and the second line
    (`p`). Clips carry `loop` and `muted` (they are silent and made to loop). The presentation video
    carries neither. No `autoplay` anywhere. The fallback content inside `<video>` is a link to the
    file. All text and attributes are escaped (`escapeHtml` of `socialCard.ts`).
  - The still picture is the `poster`. `preload="none"` means no video byte loads before the click.
    A click starts the video through the browser's native controls, with no script.
- `test/site/buildSite.ts` (`main`): writes `videos.html` with
  `pageDocument("videos", "videos.html", buildVideoGallery(listVideos(EXTENSION_ROOT)), videosCard)`.
  It copies the presentation video and its poster into the site at the same repository paths (clip
  media are already copied by `copyClipMedia`), adds `videos.html` to `site-manifest.json`, and draws
  a social picture `og/videos.png` with `simpleCard("Video gallery", "<n> videos", "Feature clips and
  the one-minute demo")`. The card description names the count. Card, wording and anchor ids are
  the spec-writer's choices, made so the page matches the other site pages.
- New file `docs/demo-video/short-demo-01/output/poster.png`: frame 0 of `short-demo-01.mp4`, the
  opening card (`short-demo-process.guidelines.md` makes frame 0 the poster), extracted once with
  ffmpeg and committed (Git LFS through `*.png`). Spec-writer's choice: the still picture of
  decision 4 needs a file, and the presentation video has none.
- `test/site/siteHeader.ts`: the links become Home, Contributing, How we ship, How we test, Gallery,
  **Videos** (`videos.html`), Requirements. The order is the spec-writer's choice: Videos sits next
  to the screenshot Gallery. Update the JSDoc.
- `pageDocument` styles: reuse `.gallery figure video` (it already exists). Add at most the rules
  the poster needs (`object-fit: contain` on the gallery page video if `cover` crops the poster).

### The README

- Top link line: add `| [Videos](https://gsemet.github.io/markdown-okf-schema-studio/videos.html)`
  after the screenshot gallery link (spec-writer's choice, so the README reaches the new page).
- Each GIF is a plain Markdown image, `![<alt>](docs/demo-video/clips/<clip>/<clip>.gif)`. The alt
  text is built from the clip's on-screen texts (Text 1 and Text 2 of its `clip.md`). Placement
  follows decision 8:
  - `diff-side-by-side`, in "See what changed since the last commit": **replaces**
    `images/readme/showcase-diff-cream.png`, which shows the same change marks.
  - `radio-buttons`, in "Decide in the page: choices in your plans": **replaces** the Cream/Dark
    table of `radio-plan-cream.png` and `radio-plan-dark.png`, which shows the same radio groups.
    The Markdown example stays above it.
  - `slash-menu-grid` and `figure-editor`, in "Edit MyST visually" (the section that names grids
    and figures): **added** after the existing still, which shows an admonition being edited, not
    the same thing. Each GIF gets a one-line lead-in sentence. The still stays.
  - `table-anchors`, in "Highest respect for the raw Markdown" (decision 9): **added**; the section
    has no picture, and the clip shows its claim (the raw table follows the drag and each cell keeps
    its spacing).
- The one-minute demo link and its place before "Example of complex Markdown rendering" do not
  change. README lines outside tables and images stay within 100 columns.
- The three replaced stills stay in `images/readme/`, and their `README_BY_ID` entries stay
  (spec-writer's choice: the same table already feeds images that the README does not show, such as
  `showcase-hero.png`). No visual scenario changes.

### Requirements

New and changed requirements are `proposed`. The ones this change touches (CORE-086, CORE-095,
StRS CORE-008) are all `proposed`, and no `approved` requirement changes (checked: no approved
requirement covers the site, its header or the README pictures). Add markers (`@implements_req`,
`@tests_req` with the scenario fragment), run `just requirements-update`, and add a dated entry in
`requirements/tiers/log.md`.

- New SwRS (rendering-core, next free `SwRS-MDOKFSTUDIO-CORE-NNN` after the stack base), derived
  from StRS CORE-008, title "The published site has a video gallery". When a maintainer builds the
  Pages site, it SHALL write `videos.html` with the presentation video first, then one card per clip
  folder that holds `<clip>.webm`. Each card is a video with its poster, `controls` and
  `preload="none"`, and no `autoplay`. Scenarios:
  - S1 (nominal): two clips and the presentation video give three cards in that order, with poster,
    source, title from `Text 1` and no autoplay.
  - S2 (nominal): a new clip folder appears with no code change.
  - S3 (boundary): a folder without a WebM is skipped; a clip without a `Text 1` row is titled with
    its name.
  - S4 (boundary): no clips folder and no presentation video gives a page with no card, and the
    build passes.
  - S5 (nominal): in a browser, no video file is requested before a click, and a click on a card
    requests its file.
  `implemented_in_files`: `test/site/videoGalleryPage.ts`, `test/site/buildSite.ts`.
- SwRS CORE-086: the description, the normative statement, S1, S2 and the criteria name seven links,
  with Videos between Gallery and Requirements. S1's GIVEN adds the Videos page.
- SwRS CORE-095: unchanged in meaning. S1's "a docs page" is true of every rendered Markdown page,
  the README included. Make the GIVEN "a page written from Markdown (a docs page or the README)" so
  the home page videos are covered.
- StRS CORE-008: add "and the videos" to the description, the normative statement and `user_need`
  ("... coverage, the e2e gallery and the videos ..."). The new SwRS joins `derived_by` through
  `just requirements-update`.

### Documentation and guidelines

- `docs/demo-video/guidelines/feature-clip-process.guidelines.md`:
  - the sentence "The README is not changed: it keeps its presentation video." becomes: the README
    keeps its presentation video at the top; a clip's GIF may illustrate its feature in the
    README's section of that feature, by the maintainer's choice;
  - section 4 gains a bullet: every clip with a WebM appears on the site's Videos page
    (`videos.html`), with its poster, playing on a click, with no edit needed.
- `CONTRIBUTING.md`, the site paragraph after `just site`: one or two sentences on
  `out/site/videos.html` (the presentation video and every clip with a WebM, posters, play on a
  click).
- `.agents/glossary/common.md`: "Site header" lists Videos. New term **Video gallery**: the Videos
  page of the site, `videos.html`, written by `buildVideoGallery` in `test/site/videoGalleryPage.ts`.
- `CHANGELOG.md` "Unreleased": one line (the site has a Videos page with every feature clip and the
  presentation video, playing on a click; the README shows five features as GIFs).
- The writing skill `skills/writing-for-markdown-okf-schema-studio/` is not affected: no rendered
  syntax changes.

## Evidence

- `test/site/videoGalleryPage.test.ts` (new, `@tests_req` S1 to S4): `listVideos` and
  `buildVideoGallery` over a temporary fixture tree. A further test reads the **shipped**
  `docs/demo-video/clips/` and `docs/demo-video/short-demo-01/output/` at the head under test. It
  asserts one card per clip folder that holds a WebM, the presentation video first, and every card
  with `poster`, `controls`, `preload="none"` and no `autoplay`.
- `test/site/videoGallery.browser.test.ts` (new, `@tests_req` S5, in the style of
  `galleryLinks.browser.test.ts`): it serves the page built by `pageDocument` and
  `buildVideoGallery` over fixture files on 127.0.0.1, and checks that no `.webm` or `.mp4` request
  happens on load, that every video is paused, and that a click on a card's video requests its
  file. It is skipped when no Chromium can start, unless `STUDIO_REQUIRE_CHROMIUM=1`. Add it to
  `test:viewer-graph` in `package.json` (the `ci-viewer-graph` job; see `ci.guidelines.md`).
- `test/site/siteLinks.test.ts`, `test/site/siteTheme.test.ts`,
  `test/site/requirementsViewer/write.test.ts`, `test/site/requirementsViewer/pages.test.ts`: the
  seven header links in order; `videos.html` is a site page.
- `test/build/readmeClipGifs.test.ts` (new) reads `README.md` at the head under test. It checks the
  five GIF images, each inside its named section, and that each file exists. It checks that
  `showcase-diff-cream.png`, `radio-plan-cream.png` and `radio-plan-dark.png` are no longer
  referenced, that the one-minute demo link still comes before the first `## ` heading, and that
  the top line links `videos.html`. It checks no GIF size: a checkout without LFS holds pointers.
- `just package`, then read `extension/readme.md` inside the VSIX: the five GIFs point to
  `https://media.githubusercontent.com/media/.../v<version>/docs/demo-video/clips/...`.
- The pull request shows a screenshot of the built `videos.html` (posters, no video playing) and
  the README sections with their GIFs, per `pull-request.guidelines.md`.
- `just requirements-lint`, `just requirements-update`, `just check`, `just preflight`. A Pages dry
  run (`gh workflow run pages.yml --ref <branch> -f dry_run=true`) shows the page built in CI with
  the LFS media; it is optional and the Driver decides.

## Out of scope

- Making, regenerating or cropping any GIF, WebM or poster of a clip; a lighter GIF.
- A WebM of the presentation video; replacing the README's one-minute demo.
- The release-notes MP4 copy (`docs/releases-notes/2026-11-27-v1.13.0/raw-copy-balance-edges.mp4`):
  it is not a clip folder and not the presentation video.
- Autoplay, playlists, filters or a viewer dialog on the Videos page; deep-link behaviour beyond the
  plain `id` anchors.
- Removing the three replaced stills or their visual scenarios.
- Videos in `docs/user/` pages (CORE-095 already plays a clip GIF placed there).
