# Feature clips: a repeatable kit, then the balanced-edges copy clip

Short name: `feature-clip`. No tracker issue (origin: the owner, verbal, 2026-11-24). Destination:
the running batch, batch-09, stacked after CR-481 `copy-raw-edge-balancing` (short name
`copy-edges`, spec `changes/4-batch/2-actives/481-copy-raw-edge-balancing/03-change-spec.md`),
itself stacked on CR-480 `copy-selection-raw-markdown`. This CR's branch starts from CR-481's
branch: the clip films CR-481's feature, which is not released yet (answer 7).

It supersedes the P4 CR `record-demo-video` (answer 6): its useful parts are taken over in
section 6, and that CR is dropped with a pointer here.

## Goal

The owner, 2026-11-24: "On a déjà une demo video de présentation mais la l'idée c'est de faire des
vidéo démo direct d'une feature, que l'on pourra mettre dans la release notes. [...] Une vidéo dure
quelque seconde, doit être focus sur l'action et le résultat attendu. Et on la converti par exemple
en gif ou webm pour la mettre dans la doc et la publier sur tweeter par exemple."

A **feature clip** is a video of a few seconds that shows one feature: the action, then its result.
It has no title or end card, loops, and comes in three files: MP4 for X and the published GitHub
release, WebM for the published docs site, a light GIF for the release-note file in the repository
and the feature's docs page (not the README, answer 11). This CR:

1. turns the short-demo-01 kit (real VS Code window, CDP screencast, Remotion) into one shared,
   lighter **clip kit**, driven by a small per-clip scenario, that runs on Windows as well as
   macOS;
2. writes the process (a guideline) and adds a step to the release process;
3. makes the first clip: the raw copy with `markdownOkfSchemaStudio.preview.rawCopy.balanceEdges`
   on, a selection that crosses an admonition's edge, copied with Ctrl+C, pasted with Ctrl+V into a
   plain Markdown editor, the pasted text showing the added delimiter;
4. embeds that clip in the user docs and publishes it with the site.

No product code changes (`src/` is not touched). The published docs site changes (2.7): that part
is user-facing and gets a `feat` commit with its CHANGELOG line (answer 15, F2).

## Decisions carried from `02-answers.md`

| Q | Decision | Where it lands below |
| --- | --- | --- |
| feature-clip-Q1 | About 5 to 12 s, no title or end card, starts on the action, a small logo mark in a corner, loops cleanly as a GIF | 3.2, 4, 5 |
| feature-clip-Q2 | MP4 (X, which does not take WebM), WebM (docs and site), light GIF (release notes, README; the README is then left out by Q11) | 3.3, 2.6, 2.7 |
| feature-clip-Q3 | Reuse and lighten the short-demo-01 kit into one shared clip kit, driven by a small per-clip scenario; it also runs on Windows | 2.1, 3.1, 3.5 |
| feature-clip-Q4 | One short caption (the why), key badges for the shortcuts (Ctrl+C, Ctrl+V), a drawn cursor, one zoom on the result | 3.2, 4 |
| feature-clip-Q5 | One folder per clip under `docs/demo-video/clips/`, its scenario and its outputs in Git LFS; the release process gains a step: a visible feature may get a clip, a GIF in the release notes, the MP4 attached to the announcement post | 2.2, 2.4, 3.4 |
| feature-clip-Q6 | `record-demo-video` closed as superseded; its useful parts (engine, capture) taken into this spec | 6 |
| feature-clip-Q7 | In batch-09, stacked after CR-481, so the clip ships with the feature in the same release | Header, 3.1 (VSIX from the branch) |
| 8 (Chief of Staff routine) | The first clip: `balanceEdges` on, a selection crossing an admonition's or a list's edge, Ctrl+C, Ctrl+V into a plain Markdown editor, the added delimiters visible; the caption names the setting | 4 |
| feature-clip-Q9 | The clip's MP4 replaces the hero image in post 1 of the announcement thread and becomes its hook | 3.4 |
| feature-clip-Q10 | A brief orange outline around the added delimiter line during the zoom on the result | 3.2, 4.3, 4.4 |
| feature-clip-Q11 | No README change: the README keeps its presentation video; clips go to the feature's docs and the release note | 2.6, 7 |
| 12 (Chief of Staff routine) | The key badges show the keys of the platform the clip is filmed on (Ctrl+C on Windows and Linux, ⌘C on macOS); the first clip is filmed on Windows | 3.2, 4.4, 5.3 |
| feature-clip-Q12 | At publication the MP4 is uploaded into the GitHub release note, which plays it; the release-note file in the repository keeps the GIF; no CR for Studio rendering `<video>` | 2.6, 3.4, 7 |
| feature-clip-Q14 (spec critic F1) | A clip's GIF is not cropped: the release-process guideline gains an exception, and the zoom on the result stands in for the crop | 3.4 |
| 15 (Chief of Staff routine, spec critic F2 to F12) | F2 the site commit is a `feat` with its CHANGELOG line; F3 the publication checklist is a new owner-only release step after step 6, step 7 amended, MP4 budget 10 MB; F4 `doctor` fails when no device scale fits, Windows work area from PowerShell, display size in `check.json`; F5 no paste selector widget; F6 reading mode in `setup(t)`, the trial names the drag-select path; F7 the clips' Markdown is not rendered by the site; F8 VS Code version pinned; F9 `.cmd` trap covers npm and npx; F10 the fade ends one frame before frame 0; F11 `clipVideos` takes a file-exists callback; F12 CR-481's path | 2.1, 2.7, 3.1, 3.3, 3.4, 3.5, 4.2, 4.3, 5.1, 5.2, 5.4 |

The older ideas of `01-intent.md` and `work/` (horizontal and vertical series, presentation,
chapter showcase) are history and out of scope (section 7).

## 1. Where things live

```text
docs/demo-video/
├── guidelines/
│   ├── short-demo-process.guidelines.md      (gets a pointer to the clip process)
│   └── feature-clip-process.guidelines.md    (new: the clip process)
├── short-demo-01/                            (untouched)
├── clip-kit/                                 (new: the shared kit)
└── clips/
    └── raw-copy-balance-edges/               (new: the first clip)
        ├── clip.md                           the live storyboard: every on-screen text and time
        ├── scenario.mjs                      the actions, the stage, the settings, the expected result
        ├── stage/runbook.md                  the demo document
        ├── raw-copy-balance-edges.mp4        outputs, Git LFS
        ├── raw-copy-balance-edges.webm
        ├── raw-copy-balance-edges.gif
        ├── poster.png                        frame 0 (the X poster, the site poster)
        ├── contact-sheet.png                 evidence (section 5)
        ├── first-last.png
        ├── frames/01-selected.png, 02-pasted.png, 03-zoomed.png
        └── check.json                        the numbers of the last `check` step
```

Git LFS needs no change: `.gitattributes` already sends `*.mp4`, `*.webm`, `*.gif` and `*.png` to
LFS, and every CI checkout runs `git lfs pull` and `git lfs fsck`. `.vscodeignore` already excludes
`docs/demo-video/**`, so nothing of this CR enters the VSIX. The kit adds no dependency to the
extension's `package.json` or `pyproject.toml`.

## 2. What changes, area by area

### 2.1 The clip kit: `docs/demo-video/clip-kit/` (new)

A port of `docs/demo-video/short-demo-01/kit/`, lighter (no cards, no music, no panels) and
portable. **Node.js and ffmpeg only**: the Python steps (`prepare.py`, `story.py`, `panels.py`) and
`render.sh` are ported to Node so the kit runs the same from PowerShell, Git Bash and a macOS
shell. `short-demo-01/kit/` stays as it is: it is the record of the published video.

| File | Content | Ported from |
| --- | --- | --- |
| `clip.mjs` | Entry point: `node docs/demo-video/clip-kit/clip.mjs <clip folder> <step>`, steps `doctor`, `setup`, `take`, `render`, `check`, `all` (= setup, take, render, check). Prints what it does and stops at the first failure with a non-zero exit | new |
| `lib/platform.mjs` | Host differences (3.5): scratch folder, VS Code executable and CLI, kill of the process tree, file URLs, the modifier key | `setup.mjs`, `capture.mjs` |
| `lib/profile.mjs` | The throwaway profile and workspace (the settings of `setup.mjs`, plus the clip's own settings from `scenario.mjs`, plus `files.eol: "\n"`); installs the extension from a VSIX or the Marketplace | `setup.mjs` |
| `lib/take.mjs` | Launches the window with the debugging port, connects with `playwright-core` (resolved from the repository's `node_modules`, as `DEMO_NODE_ROOT` did), starts `Page.startScreencast`, records events, gives the scenario its helpers (3.1), writes `frames.json` and `events.json` | `capture.mjs` |
| `lib/prepare.mjs` | Frames to a 30 fps `clip.mp4` (ffmpeg concat with per-frame durations) and the timing data `take.json` | `prepare.py` |
| `lib/storyboard.mjs` | Reads `clip.md` into `story.json` and validates it (3.2) | `story.py` |
| `lib/encode.mjs` | From the Remotion master: the final MP4, WebM, GIF, poster, contact sheet, first-last sheet, named frames (3.3, 5) | `panels.py` |
| `lib/check.mjs` | Probes every output and writes `check.json` (5.2) | new |
| `remotion/` | `package.json` (name only, as today), `remotion.config.ts`, `src/index.ts`, `src/Clip.tsx`: the composition of section 4, lightened from `short-demo-01/kit/remotion/src/Root.tsx` (its cursor, ripple, zoom and caption pill kept; cards, callouts, audio, panels and crossfades between panels removed) | `remotion/` |
| `.gitignore` | `remotion/node_modules`, `remotion/public/`, `remotion/src/story.json`, `remotion/src/take.json` | `short-demo-01/.gitignore` |

Remotion stays out of `package.json`: `setup` installs `remotion@4.0.539 @remotion/cli@4.0.539
react@19 react-dom@19` (the versions of the current guideline) into `<scratch>/remotion/` when they
are absent, from the official npm registry. `render` copies `clip-kit/remotion/` (sources and
config) and the public assets (`clip.mp4`, `images/logo.png`) into `<scratch>/remotion/` and renders
there, so no `node_modules` link is ever made inside the repository (no `ln -s`, which Windows
refuses without developer mode).

VS Code: `setup` downloads a **pinned** VS Code version into `<scratch>/vscode/<version>/` with
`downloadAndUnzipVSCode({ version })` of `@vscode/test-electron` (already a devDependency, used by
`test/integration/run-tests.ts`), and installs the extension with the CLI that
`resolveCliArgsFromVSCodeExecutablePath` gives. The version is one constant, `DEFAULT_CODE_VERSION`
in `lib/platform.mjs`, set to the current stable release when the kit is written and moved by hand
when a clip is remade on a newer one (answer 15, F8), so two takes of the same clip film the same
VS Code. `DEMO_CODE` overrides the executable with a local install. The VS Code version used is
written in `check.json`.

The extension: `--vsix <path>` installs a packaged VSIX; without it, the published
`GaetanSemet.markdown-okf-schema-studio` from the Marketplace (the current guideline's rule). A clip
of a feature not yet released uses the VSIX packaged from the branch (`just package` writes
`out/reports/package/markdown-okf-schema-studio.vsix`); the first clip does so (answer 7).

`doctor` checks, and says how to fix each: Node.js 24, `ffmpeg` and `ffprobe` on `PATH` (or
`FFMPEG` / `FFPROBE`) with the `libx264`, `libvpx-vp9` and `gif` encoders (`scoop install ffmpeg`
on Windows, `brew install ffmpeg` on macOS), the repository's `node_modules` (`just dev`), the
scratch folder writable, the Remotion install, the VS Code download, and the display: the primary
display's work area must hold the take's window (1280x720 logical pixels) at one of the device
scales of 3.5. On Windows the work area is read with a PowerShell query,
`powershell -NoProfile -Command "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.Screen]::PrimaryScreen.WorkingArea | ConvertTo-Json"`
(physical pixels); on macOS with
`osascript -e 'tell application "Finder" to get bounds of window of desktop'`. When no scale fits,
`doctor` fails and names the display it needs (a work area of at least 1920x1080 physical pixels,
the smallest scale 1.5 times 1280x720) and the one it measured (answer 15, F4). `setup` and `take`
run the same display check first.

The kit is not part of the build, of `just check` or of `just preflight`, and has no CI job (section
7). It lives outside `tsconfig.json` (`src/**`, `test/**` only), like `short-demo-01/kit/`; if a
`just check` stage picks a kit file up, the folder is excluded the way `short-demo-01/` is.

### 2.2 The first clip: `docs/demo-video/clips/raw-copy-balance-edges/` (new)

`clip.md`, `scenario.mjs` and `stage/runbook.md` as section 4 gives them, and the outputs of the
last accepted run (section 1 tree). Section 4 is the clip's full description.

### 2.3 justfile and `AGENTS.md`

- `justfile`: one recipe, formatted with `just format`:

  ```just
  # Make or remake a feature clip (docs/demo-video/clips/NAME); STEP: doctor, setup, take, render, check or all.
  clip NAME STEP="all" *ARGS:
      fnm exec -- node docs/demo-video/clip-kit/clip.mjs docs/demo-video/clips/{{ NAME }} {{ STEP }} {{ ARGS }}
  ```

  (`ARGS` carries `--vsix <path>`.) It is not a dependency of any other recipe.
- `AGENTS.md`, "Main targets": `Feature clip (manual, a real VS Code window, not in check or
  preflight): just clip NAME [STEP]`. "Guidelines": `When making a feature clip (a few seconds, one
  feature) or adding one to a release:
  [feature-clip-process.guidelines.md](docs/demo-video/guidelines/feature-clip-process.guidelines.md)`.

### 2.4 Guidelines

- New `docs/demo-video/guidelines/feature-clip-process.guidelines.md`, written for an agent that
  makes a clip with the maintainer, in the style of `short-demo-process.guidelines.md` (rules with
  their reason). Its content is section 3. It names no process role and links to no process
  document: `test/build/test_guideline_isolation.py` scans `docs/demo-video/guidelines/` and fails
  on "Chief of Staff", "Foreman", "driver", "Inspector", "coder" or "orchestrator" (write
  "maintainer" and "agent", as the short-demo guideline does; never "VS Code driver").
- `short-demo-process.guidelines.md`: one sentence after its opening paragraph: a video of a few
  seconds on one feature is a feature clip and follows `feature-clip-process.guidelines.md`; its
  identity table stays the source of the colours, type, caption pill, cursor and zoom rules that
  clips reuse.
- `.agents/guidelines/release-process.guidelines.md`: section 3.4.

### 2.5 Glossary

`.agents/glossary/common.md`: **Feature clip**: a video of 5 to 12 seconds on one feature, with no
card, that loops; one caption, key badges, a drawn cursor, one zoom on the result; made with the
clip kit (`docs/demo-video/clip-kit/`), one folder per clip under `docs/demo-video/clips/`, in MP4,
WebM and GIF.

### 2.6 User docs: the clip in `docs/user/settings.md`

Studio's renderer does not render `<video>`: the README-style raw HTML pass
(`src/core/render/mystRawHtml.ts`, `BLOCK_TAGS` and `PHRASING_TAGS`) has no `video` tag, so a
`<video>` element written in a docs page is dropped, in Studio and in the site, which renders the
docs with the same `renderMyst`. GitHub's file view drops a `<video>` with a repository path too.
So a docs page embeds a clip as **its GIF, with a plain Markdown image**, and the site build turns
that image into the WebM video (2.7):

- under the `preview.rawCopy.balanceEdges` entry that CR-481 adds to `docs/user/settings.md`, an
  indented line:

  ```markdown
    ![A selection from inside an admonition to the next paragraph is copied with Ctrl+C and pasted with Ctrl+V: the admonition's opening line is added](../demo-video/clips/raw-copy-balance-edges/raw-copy-balance-edges.gif)
  ```

- Studio and GitHub show the GIF; the published site plays the WebM. Studio does not gain a
  `<video>` rendering, now or in a follow-up CR (answer 13). The README is not changed: it keeps its
  presentation video (answer 11).

The docs here are the `docs/` pages that `test/site/buildSite.ts` publishes on GitHub Pages: the
project has no Sphinx documentation build (`sphinx/` is the preview's source-mapping extension).

### 2.7 Site: a clip's GIF becomes its WebM video

New `test/site/siteClips.ts` (kept out of `buildSite.ts`, which is long already), called from
`buildSite.ts`:

- `clipVideos(html, sourcePage, fileExists)`: in a page's rendered HTML (parse5, as
  `rewriteRenderedLinks`), an `<img>` whose `src` resolves, from the source page, to
  `docs/demo-video/clips/<clip>/<clip>.gif`, with `<clip>.webm` beside it, is replaced by the video
  below. `fileExists(repoRelativePath)` is the callback that says whether a file is in the
  repository (answer 15, F11): `buildSite.ts` passes one bound to `EXTENSION_ROOT`
  (`fs.existsSync(path.join(EXTENSION_ROOT, p))`), the unit tests pass a set of paths. The
  replacement:

  ```html
  <video src="…/<clip>.webm" poster="…/poster.png" autoplay loop muted playsinline controls
         aria-label="<the image's alt>"><img src="…/<clip>.gif" alt="<the image's alt>"></video>
  ```

  `poster` only when `poster.png` exists. Any other `<img>` is unchanged. It runs in
  `renderMarkdown` before `rewriteRenderedLinks`, so `src` and `poster` go through
  `rewriteLinkTarget` like every other link (a docs path stays relative, as the site mirrors
  `docs/`). The site page is written by the builder after the sanitizer, so `playsinline` stays.
- `copyClipMedia(extensionRoot, siteRoot)`: for each folder of `docs/demo-video/clips/`, copies
  `<clip>.webm`, `<clip>.gif` and `poster.png` (those that exist) to
  `out/site/docs/demo-video/clips/<clip>/`. Not the MP4, the scenario, the stage or the evidence
  files. No clips folder: nothing, no error. Called in `main()` next to the `images/` copy.
- A CSS rule in the page stylesheet of `pageDocument`: `video { max-width: 100%; height: auto; }`,
  next to the `img` rule.
- The clips' own Markdown is not published (answer 15, F7): `buildSite.ts` leaves
  `docs/demo-video/clips/**/*.md` (`clip.md`, `stage/*.md`) out of the files it renders (the list
  built from `walkMarkdown(path.join(EXTENSION_ROOT, "docs"))`), through an exported filter in
  `siteClips.ts`, `isClipSource(repoRelativePath)`. A clip's storyboard and stage document are
  production files, not docs pages.

This is a site behaviour: a new SwRS (section 3.6 of the evidence, "Requirements").

## 3. The process (content of `feature-clip-process.guidelines.md`)

### 3.1 The kit and a take

```bash
just clip <name> doctor                 # what is missing, and how to get it
just clip <name> all --vsix <path>      # setup, take, render, check
just clip <name> render                 # after a text or time change in clip.md: no new take
just clip <name> check
```

- `setup`: throwaway `--user-data-dir` and `--extensions-dir` in the scratch folder, never the
  maintainer's profile; the profile settings of `short-demo-01/kit/setup.mjs` (theme, hidden
  chrome, `workbench.hover.delay` high, sash hover transparent, `editor.occurrencesHighlight` off,
  `comments.authorName` "Reviewer", `files.autoSave` afterDelay) plus the clip's settings
  (`scenario.mjs`), plus `files.eol: "\n"` and `"editor.pasteAs.showPasteSelector": "never"` (no
  paste-options widget after a paste, answer 15, F5); a neutral workspace holding the clip's
  `stage/`.
- `take`: before it starts, it deletes the previous take and `clip.mp4`, so a failed take can never
  be rendered as if it were new (the short-demo trap "a cut from a failed take is not a new cut").
  It opens the window, sets the layout up **before** the screencast starts (what happens there is
  not in the clip), starts the screencast, runs `scenario.run(t)`, stops, and runs the scenario's
  check (`scenario.verify(t)`): a failed check fails the take.
- `scenario.mjs` exports: `stage` (files copied to the workspace), `settings` (added to the
  profile), `setup(t)` (the layout, off camera), `run(t)` (the filmed action), `verify(t)` (the
  expected result, read from disk). The helpers `t` gives, from `capture.mjs`: `moveTo(x, y, dur)`
  (eased, logged), `click()`, `selectText(frame, from, to)` (a mouse drag from the left edge of the
  first character of `from` to the right edge of the last character of `to`, located with a DOM
  `Range`, non-breaking spaces normalised), `press(chord, badgeId)` (the key chord through CDP,
  `ControlOrMeta` for the platform modifier, logged with the badge id), `zoom(id, rect)`,
  `unzoom(id)`, `mark(id, rect)`, `unmark(id)`, `sleep(ms)`, `frameOf()` (the preview frame),
  `workspaceFile(name)` (read a workspace file from disk).
- Pacing defaults (from `record-demo-video`, Q19): cursor moves 600 to 900 ms, eased; 400 ms pause
  before a click or a chord; zoom in and out over 600 ms (20 frames at 30 fps), at most 2x.
- A trial first (the short-demo step 6, and `record-demo-video`'s go/no-go spike): the first take of
  a new kit or a new host proves (a) the preview webview is in the screencast frames, (b) the
  selection is made the way the clip shows it, a CDP mouse drag (`Input.dispatchMouseEvent`
  pressed, moved, released, through `selectText`) in Studio's reading mode, and the page's
  `getSelection()` holds the expected text (answer 15, F6), (c) the chord reaches the page (the
  scenario's check passes), (d) at least 30 frames per second after retiming (`prepare` prints
  it). If (b) fails, stop and report: a selection made by script (`Selection.addRange`) is not what
  the clip shows. If (a) fails, a `Page.captureScreenshot` loop replaces the screencast; if
  (c) fails, `Input.dispatchKeyEvent` with its `commands` field (`copy`, `paste`) replaces the plain
  key press; if either still fails, stop and report. Never an OS-level screen capture or OS-level
  input.
- A take opens a real VS Code window: it does not run while another change runs app-window tests on
  the same machine (`local-worktree.guidelines.md`), and the screen stays unlocked. It overwrites
  the system clipboard.

### 3.2 The live storyboard: `clip.md`

The short-demo rule holds: **one file, the clip reads every on-screen text and time from it, every
change lands in it in the same step, re-read before each render**. Its contract:

- front matter `title`, `status`, `date`; one table `| Field | Content |`;
- fields: `Length` (seconds, 5 to 12), `Caption` (one line; `**bold**` takes the accent colour),
  `Badge <id>` (the keycap text of each `press(…, id)`, for example `Badge copy | Ctrl+C`),
  `Zoom` (the id of the one zoom and its hold, for example `result, hold to 7.6 s`), `Logo`
  (`top right` by default), `Mark <id>` (optional, `-` for none: a brief orange outline, during the
  zoom, around what the feature changed, answer 10);
- badges show the keys of the platform the clip is filmed on (answer 12): `Ctrl+C` on Windows and
  Linux, `⌘C` on macOS. `clip.md` holds one text per badge; `storyboard.mjs` refuses a badge that
  names the other platform's modifier (`Ctrl` in a take filmed on macOS, `⌘` or `Cmd` in one filmed
  on Windows or Linux), read from the take's platform;
- `storyboard.mjs` refuses a clip.md with no caption, a length outside 5 to 12 s, more than one zoom,
  more than one mark, a badge id the take did not log, or a playback rate outside 0.77 to 1.3 of the filmed length
  (the short-demo pace rule).

### 3.3 Outputs and how the GIF stays light

Every output comes from one Remotion master (`--codec=h264 --pixel-format=yuv420p --crf=18
--muted`), 1920x1080, 30 fps. Then ffmpeg:

| File | Settings | Budget (the `check` step fails above it) |
| --- | --- | --- |
| `<clip>.mp4` | the master remuxed with `-movflags +faststart`, no audio stream, H.264 `yuv420p` (what X takes and what the GitHub release editor plays) | 10 MB (answer 15, F3); over it, the master is re-encoded at `-crf 20`, then 22, reported in `check.json`; still over: `check` fails |
| `<clip>.webm` | VP9: `-c:v libvpx-vp9 -crf 34 -b:v 0 -row-mt 1 -deadline good -cpu-used 2 -pix_fmt yuv420p -an`, 1920x1080, 30 fps | 3 MB |
| `<clip>.gif` | one filter graph: `fps=12,scale=960:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=128:stats_mode=diff[p];[b][p]paletteuse=dither=bayer:bayer_scale=5:diff_mode=rectangle`, `-loop 0` | 3 MB |
| `poster.png` | frame 0, 1920x1080 | - |

Why the GIF stays light, and what the guideline says about it:

- **Its own palette, built from the clip** (`palettegen`), not the default 256-colour web palette:
  VS Code and the cream page are a few flat colours, so 128 colours are enough and keep the LZW
  stream short. `stats_mode=diff` weighs the palette towards what moves (the selection, the pasted
  text), so the moving parts get the exact colours.
- **Ordered dithering** (`bayer`, scale 5) instead of error diffusion: error diffusion sprinkles
  noise on flat areas, which changes pixels from frame to frame and defeats the frame-difference
  compression.
- **Only changed rectangles re-encoded** (`diff_mode=rectangle`): a screen clip changes a small area
  per frame, except during the zoom.
- **12 fps**: enough for a cursor and a paste; 30 fps in the MP4 and WebM.
- **960 px wide** (half the master): the width of a GitHub release body and of a docs page column.
  Text stays readable because the take films a window at 1280x720 logical pixels and the clip zooms
  on the result.
- **A ladder when over budget**, stopping at the first that fits, reported in `check.json`: 10 fps,
  then 800 px wide, then 96 colours. None fits: the `check` step fails, and the clip is shortened
  (back to `clip.md`), never shipped heavier.

### 3.4 Release step (in `.agents/guidelines/release-process.guidelines.md`)

- "The release folder" table, a row: `Clips` | the GIF and the MP4 of a feature clip, copied from
  `docs/demo-video/clips/<clip>/` into the folder (Git LFS stores one object for both copies).
- "The steps of a release", step 3 gains: a visible feature may get a feature clip
  (`docs/demo-video/guidelines/feature-clip-process.guidelines.md`); the maintainer decides which
  feature gets one, and the clip is made in the change of the feature or right after it, before the
  version pull request, so it ships with the feature. Its GIF is the picture of that feature's
  highlight in `release-notes.md` (linked by file name, so the existing check of
  `scripts/release_notes.py` and the release's asset upload take it as they take a PNG). The
  release-note file in the repository keeps the GIF, never a video link (answer 13).
- "Announcement thread": when the release has a clip, **its MP4 replaces the hero image in post 1**
  and is the thread's hook (answer 9). Post 1 carries a `Video: <clip>.mp4` line instead of its
  `Image:` line (X takes one video or up to four images per post, never both); no other post
  changes. A release without a clip keeps the hero image in post 1. Only the owner posts and
  uploads. The "Hero image" section says that, when the release has a clip, the hero image is still
  made for the release folder but is not posted in the thread.
- "The version PR body": the `rewrite` function gains
  `-e "s#^Video: ([^ /]+\.mp4)\$#Video: [\1]($base/\1)#"`, so the owner can open the MP4 from the
  PR page (the GIF is already covered by the `gif` alternative of the image expression).
- "Release notes", "Writing": the crop rule gains an exception (answer 14): **a feature clip's GIF
  is not cropped**. It shows the whole filmed window, and the clip's one zoom on the result stands
  in for the crop. The rest of the rule holds for every still picture.
- "The steps of a release" gains a new **owner-only step 7, after step 6** (answer 15, F3), for a
  release with a clip; the current step 7 (the archive) becomes step 8 and is amended:
  - New step 7, "Publish the clip" (owner only, after the GitHub release exists and the version is
    served):
    1. In the GitHub release editor, the owner drags `<clip>.mp4` (at most 10 MB, 3.3) from the
       release folder into the release body at the clip's highlight, in place of its GIF line
       (GitHub plays only a video uploaded through its UI, not a relative `.mp4` in the repository,
       answer 13). `release-notes.md` in the repository is not changed: it keeps the GIF.
    2. The owner opens the published release page: the video plays at the highlight, and the
       highlight does not show both the video and the GIF.
    3. Post 1 of the announcement thread is posted with `<clip>.mp4` attached (its `Video:` line),
       with `poster.png` as the cover when X asks for one.
  - Step 8 (was 7): `04-report.md` also records, for a release with a clip, the clip's name and
    whether step 7 was done (the release body plays the MP4, post 1 carries it), as the owner
    reports it; the agent does not do step 7.
  - Step 8 (was 8) becomes step 9; the other references to step numbers in the guideline follow.
### 3.5 Windows and macOS

The traps of the short-demo guideline all still hold. The guideline adds these, each with its rule:

| Trap | Rule |
| --- | --- |
| VS Code is installed in different places | The kit downloads the pinned `DEFAULT_CODE_VERSION` with `@vscode/test-electron` into the scratch folder; `DEMO_CODE` overrides it |
| The VS Code CLI, `npm` and `npx` are `.cmd` files on Windows | Spawn them with `shell: true` on Windows only (the VS Code CLI from `resolveCliArgsFromVSCodeExecutablePath`, `npm` for the Remotion install, `npx remotion render`), with every argument quoted (answer 15, F9) |
| macOS's temporary folder is long and the debugging port fails | Scratch: `CLIP_SCRATCH`, else `/private/tmp/okfclip` on macOS, else `<os.tmpdir()>/okfclip` |
| `file://${path}` is wrong with a drive letter | `pathToFileURL(path).href` for every URI in `storage.json` |
| `Meta+…` chords do nothing on Windows | `ControlOrMeta` in every chord; the scenario never names `Meta` or `Control` for the platform modifier |
| Killing VS Code leaves its helpers running on Windows | `taskkill /PID <pid> /T /F` on Windows; `process.kill` on macOS |
| A pasted file gets CRLF on Windows and the check fails | `files.eol: "\n"` in the profile |
| A window at device scale 2 is larger than a 1080p screen | The kit sizes the window so its physical size fits the primary display's work area, at scale 2 when it fits, else the largest of 1.75 and 1.5 that fits, and writes the scale and the measured work area in `check.json`; no scale fits: `doctor` (and `setup`, `take`) fails and names the display it needs (answer 15, F4); the master is 1920x1080 whatever the scale |
| A backslash path in the ffmpeg concat list | Forward slashes and `-safe 0` |
| `ln -s` needs developer mode on Windows | No link: `render` copies the composition into the scratch Remotion folder |
| Python is `python3` on macOS and absent or `py` on Windows | The kit is Node.js only |

### 3.6 Self-check, review and commit

- The `check` step (section 5.2) and the evidence files (5.1), then the agent looks at every frame
  of the contact sheet and the three named frames: wrong framing, a missed selection, the result
  not visible at the zoom, a tooltip, a personal name or path, a dirty tab. It says what it did not
  check: motion, rhythm and the loop as watched are the maintainer's to judge.
- The maintainer watches the MP4 (on a phone) and the GIF. A caption, a badge or a time: they edit
  `clip.md` (or the agent does), `just clip <name> render` then `check`, about two minutes. A new
  action or a changed document: a new take.
- The outputs, the poster and the evidence files are committed together with `clip.md`, so the
  storyboard, the clip and its pictures always match (the short-demo rule for panel pictures).
- No personal data in any frame; the version shown is the one the clip says (the Marketplace
  version, or the branch's VSIX for a feature not yet released).

## 4. The first clip: `raw-copy-balance-edges`

### 4.1 Stage: `stage/runbook.md`

A short release runbook an agent would write (the short-demo step 4 rule: real sentences, no
personal data), with the admonition the selection starts in:

```markdown
# Release runbook: payments service

Deploy on a weekday morning, with the on-call engineer in the channel.

:::{important} Before you deploy
Run the database migrations first, then restart the workers one at a time.
:::

The deploy script checks the migration version and refuses to start the workers on an old schema.

## Rollback

Redeploy the previous tag. The migrations are backward compatible for one release.
```

The workspace also holds an empty `notes.md`: the plain Markdown editor the text is pasted into is
VS Code's built-in text editor on that file.

### 4.2 Settings and layout

- `settings`: `"markdownOkfSchemaStudio.preview.rawCopy.balanceEdges": true` (a startup setting
  read when the page boots, CR-481 2.2, so it is in the profile before the window opens).
- `setup(t)`, off camera: Studio shows `runbook.md` in one editor group, the built-in text editor
  shows the empty `notes.md` in the other, side by side, the text editor of `runbook.md` closed;
  window 1280x720 logical pixels (3.5). Studio is in **reading mode** (answer 15, F6): `setup(t)`
  reads `data-sphinx-preview-edit-mode` on the page's root element in the preview frame and, when
  it is `on`, clicks the edit-mode toggle (`[data-sphinx-preview-edit-toggle]`) and waits for `off`;
  the take fails if the attribute is not `off` when the screencast starts. In reading mode a drag
  selects text and opens no block editor.
- Extension: the VSIX packaged from this CR's branch (`just package`), which holds CR-480 and CR-481.

### 4.3 The action (`run(t)`), and the times of `clip.md`

| Time in the clip | What happens |
| --- | --- |
| 0.0 s | Frame 0, the poster: the runbook in Studio, the empty `notes.md`, the caption whole, the logo. No entrance animation on frame 0 |
| 0.4 to 2.2 s | The cursor drags from "database" in the admonition's body to the end of "old schema." in the paragraph after it; the selection is shown |
| 2.6 s | `press("ControlOrMeta+C", "copy")`: the `Ctrl+C` badge |
| 2.8 to 3.8 s | The cursor moves to `notes.md` and clicks in it |
| 4.2 s | `press("ControlOrMeta+V", "paste")`: the `Ctrl+V` badge; the text appears |
| 4.4 to 5.0 s | The one zoom, on the pasted lines in `notes.md` (at most 2x, no line cut: the editor wraps) |
| 5.0 to 7.6 s | Hold on the result: the added `:::{important} Before you deploy` line above the copied text. The orange outline (`mark("delimiter", rect)`, the rect of that first line in `notes.md`) fades in at 5.2 s and out at 6.8 s, brief and inside the hold (answer 10) |
| 7.6 to 8.2 s | Zoom out; the cursor back to its frame-0 place |
| 8.2 to 8.5 s | The last 8 frames cross-fade towards frame 0 and end **one frame before it** (the last frame is the fade's step just short of frame 0, never a copy of it), so the loop neither jumps nor shows frame 0 twice (answer 15, F10) |

Length 8.5 s (inside 5 to 12). The times are the proposal of `clip.md`; the clip plays the filmed
action at those times within the 0.77 to 1.3 rate (3.2).

### 4.4 On screen (answer 4), from `clip.md`

- Caption, bottom centre, the short-demo green pill, whole from frame 0 to the end (it is the
  poster's text and the loop must not blink): proposal `**balanceEdges** on: a copy stays valid
  Markdown`. It names the setting (answer 8); the owner may reword it in `clip.md`.
- Badges: `Ctrl+C` and `Ctrl+V` (the clip is filmed on Windows, answer 12), keycaps (white, dark text, a thin border, rounded), centred just
  above the caption pill, each springing in at its chord's event and fading out after 1.2 s.
- Cursor: drawn over the footage from the logged track, with the orange ripple on each click (the
  short-demo composition's).
- One zoom: on the result, as 4.3.
- Logo: `images/logo.png`, 56 px, top right, 24 px from the edges, 85 % opacity, whole clip.
- Mark: the short-demo orange outline (rounded, no fill) around the added
  `:::{important} Before you deploy` line, from 5.2 s to 6.8 s, fading in and out over 6 frames;
  `clip.md` field `Mark delimiter | added opening line, 5.2 to 6.8 s` (answer 10).
- No title card, no end card, no callout, no music.

### 4.5 The expected result (`verify(t)`)

The selection crosses the admonition's boundary at its start only (the end is in a top-level
paragraph), so CR-481's container rule applies (its 3.4, "start in admonition A, end after A": A's
opening lines, then the cut). `verify(t)` reads `notes.md` from disk (auto-save on) and requires it
to equal, byte for byte:

```markdown
:::{important} Before you deploy
database migrations first, then restart the workers one at a time.
:::

The deploy script checks the migration version and refuses to start the workers on an old schema.
```

Before the chord, the take also checks that the page selection's text
(`getSelection().toString()` in the preview frame) starts with "database" and ends with "old
schema.". A pasted text that differs from this expected value is not "fixed" in the scenario: it is
a finding against CR-481 (or CR-480), reported with the pasted text, and the clip waits.

## 5. Evidence

### 5.1 What proves the clip to the owner

Written by `encode`/`check` into the clip folder and committed:

| File | What the owner sees |
| --- | --- |
| `contact-sheet.png` | 12 frames evenly spaced across the MP4, 4x3, each 480 px wide, with its time |
| `frames/01-selected.png` | The frame just before the `copy` chord: the selection across the admonition's edge |
| `frames/02-pasted.png` | The frame 0.3 s after the `paste` chord: the pasted text, unzoomed, and no paste-options widget next to it (answer 15, F5) |
| `frames/03-zoomed.png` | The frame in the middle of the hold: the added opening line readable, inside its orange outline |
| `first-last.png` | Frame 0 and the last frame side by side: the loop seam. Its caption asks the maintainer to judge the fade-out as watched, which the SSIM number does not prove (answer 15, F10) |
| `poster.png` | Frame 0: the X poster and the site poster |
| `check.json` | The numbers of 5.2; no absolute path, no user name |

The pull request body shows the GIF and the contact sheet through
`https://media.githubusercontent.com/media/gsemet/markdown-okf-schema-studio/<head sha>/docs/demo-video/clips/raw-copy-balance-edges/<file>`
(LFS files: a `raw.githubusercontent.com` link shows the pointer), and links the MP4 the same way.

### 5.2 The `check` step

`check` fails (non-zero) unless every line holds; it writes each measured value in `check.json`:

- MP4: duration 5 to 12 s and equal to `clip.md`'s `Length` within one frame; 1920x1080; 30 fps;
  `h264`, `yuv420p`; no audio stream; `faststart` (the `moov` atom before `mdat`); at most 10 MB
  (answer 15, F3), with the CRF step used.
- WebM: `vp9`, same size, fps and duration; no audio stream; at most 3 MB.
- GIF: 960 px wide or the ladder's width, 12 fps or the ladder's, at most 3 MB, a NETSCAPE2.0 loop
  extension with a count of 0 (read from the file's bytes); the ladder step used.
- Loop seam: SSIM between frame 0 and the last frame of the MP4 (ffmpeg `ssim` filter) at least
  0.98 and below 1.0 (the last frame is not a copy of frame 0, F10).
- Paste widget: in `frames/02-pasted.png` and the hold frames, no paste-options widget; `take`
  also asserts, right after the paste chord, that the workbench shows no element of the paste
  selector widget (`.post-edit-widget`) (answer 15, F5).
- The take: the scenario's `verify` passed (stored by `take` in the scratch take folder, read by
  `check`); frames per second after retiming at least 30; the playback rate inside 0.77 to 1.3.
- The host: VS Code version (and whether it is `DEFAULT_CODE_VERSION` or `DEMO_CODE`), extension
  version (from the VSIX or the Marketplace), device scale, the measured display work area
  (answer 15, F4), platform (`win32`, `darwin`); the reading mode at the start of the take.

### 5.3 Host and default matrix

The kit depends on the host, and the clip on a configured value of a setting whose shipped default
is off. One line per cell:

| Host | VS Code | Setting `balanceEdges` | Expected | Proved by |
| --- | --- | --- | --- | --- |
| Windows 11 (the batch's machine) | `DEFAULT_CODE_VERSION`, downloaded by the kit (`DEMO_CODE` unset) | on, in the profile | `just clip raw-copy-balance-edges all --vsix out/reports/package/markdown-okf-schema-studio.vsix` passes; `verify` holds the 4.5 text | E3 |
| Windows 11 | `DEMO_CODE` set to the local install | on | `doctor` and `setup` resolve and use it | E3, one `doctor` and `setup` run with it set |
| Windows 11 | `DEFAULT_CODE_VERSION` | off (shipped default) | not filmed: the clip shows the setting on only (answer 8) | - |
| Windows 11, a display too small for every scale | `DEFAULT_CODE_VERSION` | on | `doctor` fails and names the display it needs and the one measured | E3: one `doctor` run with `CLIP_DISPLAY_OVERRIDE=1280x720` (a test hook of `lib/platform.mjs` that replaces the measured work area) |
| Windows 11 (badges) | `DEFAULT_CODE_VERSION` | on | the badges read `Ctrl+C`, `Ctrl+V`; `storyboard.mjs` refuses a `⌘` badge on a `win32` take | E3, plus one `render` with a `⌘C` badge text that must fail, then reverted |
| macOS | `DEFAULT_CODE_VERSION`, downloaded by the kit | on | the kit's macOS paths and chords are kept from short-demo-01 and the new code takes the macOS branch; a clip filmed there shows `⌘C`, `⌘V` badges (answer 12) | **Not proved in this CR** (no macOS machine in the batch); the first macOS run of the kit proves it, and the PR says so |

### 5.4 Checks and scenario steps

- **E1. Static gates.** `just check` passes (formatting, TypeScript, boundaries, sizes, unused
  exports, markers, release tests with `test/build/test_guideline_isolation.py` scanning the new
  guideline). `just format` was run on the justfile. `just requirements-lint` and
  `just requirements-update` pass. `just preflight` passes (on Windows its static stage; CI runs
  the others), constitution section 4.
- **E2. Site unit tests: new `test/site/siteClips.test.ts`**, each with `@tests_req` of the new
  SwRS:
  - `clipVideos`: an `<img>` of `docs/demo-video/clips/x/x.gif` with `x.webm` and `poster.png`
    beside it becomes the `<video>` of 2.7 with every attribute, the
    alt in `aria-label`, and the `<img>` fallback inside; without `poster.png`, no `poster`; without
    `x.webm`, the `<img>` is unchanged; a GIF outside `docs/demo-video/clips/` and a GIF whose name
    is not its folder's are unchanged.
  - `copyClipMedia`: copies `x.webm`, `x.gif`, `poster.png` to `out/site/docs/demo-video/clips/x/`,
    and not `x.mp4`, `scenario.mjs`, `stage/`, `contact-sheet.png`; no clips folder: no error, no
    output folder.
  - The shipped page: reads `docs/user/settings.md` from the repository at the head under test,
    renders it with `renderMyst` and runs `clipVideos` on it: the output holds the `<video>` whose
    `src` is the shipped `docs/demo-video/clips/raw-copy-balance-edges/raw-copy-balance-edges.webm`,
    and that file, the GIF and `poster.png` exist in the repository (the callback bound to the
    repository root). This test fails on the previous
    code (no module, no image line), as constitution section 3 asks.
  - `clipVideos` is given its `fileExists` callback as a set of paths in these cases, so no
    temporary tree is needed (F11).
  - `isClipSource`: `docs/demo-video/clips/x/clip.md` and `docs/demo-video/clips/x/stage/runbook.md`
    are clip sources, `docs/user/settings.md` and `docs/demo-video/guidelines/x.md` are not; and
    the list of files `buildSite.ts` renders, built from the shipped `docs/` tree, holds no path
    under `docs/demo-video/clips/` (F7).
  - `test/site/siteLinks.test.ts` gains a guard: `rewriteLinkTarget` of
    `../demo-video/clips/x/x.webm` from `docs/user/settings.md` to `docs/user/settings.html` stays
    `../demo-video/clips/x/x.webm`.
- **E3. The clip, on Windows** (the Windows lines of the matrix): `just package`, then
  `just clip raw-copy-balance-edges doctor`, then
  `just clip raw-copy-balance-edges all --vsix out/reports/package/markdown-okf-schema-studio.vsix`
  passes: the trial's four proofs (3.1), reading mode at the start, `verify` (4.5), `check`
  (5.2); the matrix's `DEMO_CODE` and small-display lines are run too. The agent then reads every
  evidence file of 5.1 and reports what it saw frame by frame, and what it did not check.
- **E4. Site build.** `just site-assemble` locally when the host runs it (it needs the
  requirements report; on Windows it may not), else the `gallery` job of a heavy dispatch
  (`gh workflow run ci.yml --ref <branch> -f heavy=true`) builds the site with LFS objects pulled;
  either way, `out/site/docs/user/settings.html` holds the `<video>` and
  `out/site/docs/demo-video/clips/raw-copy-balance-edges/` holds the WebM, the GIF and the poster,
  and no `clip.html` or `stage/runbook.html` (F7).
  The CI job is unchanged (its checkout already pulls LFS objects); this is the only difference from
  the local machine that the job's run proves (Linux, a fresh checkout, LFS pulled).
- **E5. GitHub's view.** On the pushed branch, `docs/user/settings.md` opened on github.com shows
  the GIF under the setting's entry (an LFS GIF in a repository Markdown file); the PR says it was
  looked at.
- **E6. Pull request.** Body per `.github/PULL_REQUEST_TEMPLATE.md` and
  `.agents/guidelines/pull-request.guidelines.md`, stacked on CR-481's PR per
  `.agents/guidelines/stacked-prs.guidelines.md`: the GIF and the contact sheet (5.1), the MP4 link,
  the `check.json` numbers, the matrix with the macOS line marked not proved, the new SwRS with its
  source and test files. Commits per `.agents/guidelines/git-commit-message.guidelines.md`, with no
  scope (answer 15, F2):
  - the site change (2.7, its SwRS, its tests): `feat: play feature clips as video on the published
    site`, with its line under `## Unreleased` of `CHANGELOG.md`, in the file's style, for example
    "The published docs site now plays a feature clip as a looping video where a page shows its
    GIF; the first one shows the raw copy with `balanceEdges` on" (the commit, CR and PR references
    are added by `just changelog-refs` at the release). The template's "No user-facing change" box
    is not ticked;
  - `build` for the kit and the `clip` recipe;
  - `docs` for the guidelines, the glossary, `AGENTS.md`, the clip and `settings.md`.

### 5.5 Requirements (okfreq)

Rules: `requirements/guidelines/requirements.guidelines.md`, the okfreq baseline it links to and
`requirements/guidelines/project.guidelines.md` ("During a change"); okfreq as
`uv run --no-sync --group requirements okfreq`.

- One new SwRS, scope `rendering-core` (token CORE), `okfreq new … --lifecycle proposed`, deriving
  from `StRS-MDOKFSTUDIO-CORE-008` ("A reviewer reads the published site and its requirements",
  proposed): "When a maintainer builds the Pages site, an image of a page that shows a feature
  clip's GIF (`docs/demo-video/clips/<clip>/<clip>.gif` with `<clip>.webm` beside it) SHALL become
  a looping, muted, autoplaying video of the WebM with the poster and the GIF as fallback, and the
  site SHALL carry the clip's WebM, GIF and poster." Scenarios: the nominal page; no WebM beside
  the GIF (the image stays); a GIF outside the clips folder (unchanged); no clips folder (the build
  passes).
- `@implements_req` on `clipVideos` and `copyClipMedia` in `test/site/siteClips.ts`;
  `@tests_req` in `test/site/siteClips.test.ts`; at most 3 IDs per marker block.
- No `approved` requirement is touched. The kit, the clip and the guidelines are not product
  behaviour and carry no requirement.
- `just requirements-update`, then a dated entry in `requirements/tiers/log.md` under the day of the
  change, in a `### Site: feature clips play as video` sub-heading.

## 6. Taken over from `record-demo-video` (answer 6)

| From `record-demo-video` | Here |
| --- | --- |
| Deterministic replay of an authored scenario | `scenario.mjs` and `clip.md`; the agent authors, the kit replays (3.1, 3.2) |
| A demo engine separate from the QA engine | The clip kit, outside `test/` and the build (2.1) |
| Pinned VS Code from `@vscode/test-electron`, isolated profile, no other extensions, telemetry off | `setup` (2.1, 3.1) |
| Input through CDP, the cursor path and clicks recorded in a timeline, the cursor drawn at composition | `take.mjs` events, `take.json`, `Clip.tsx` (3.1, 4.4) |
| `Page.startScreencast`, frames retimed at composition | `take.mjs`, `prepare.mjs` |
| Spike as go/no-go, CDP screenshot loop the only fallback, no OS capture | The trial (3.1), with the CDP key-command fallback added |
| Explicit zoom, at most 2x, 600 ms; pacing defaults | One zoom per clip (answer 4); 3.1 |
| Caption pill, drawn cursor, click ripple | 4.4, from the short-demo identity |
| Review loop: lint, contact sheet, size check, human approval before commit | `storyboard.mjs` validation, 5.1, 5.2, 3.6 |
| Palette-based GIF, 3 MB budget | 3.3 |
| Recording outside `just preflight`; zero impact on the extension's dependencies and VSIX | 2.1, section 1 |
| Remotion, individual licence | Kept: Remotion as in the short-demo kit |

Not taken: the nested `demos/` npm package and `just demo-install` (Remotion stays in the scratch
folder, the current guideline's way), `images/demos/` and a gitignored MP4 (replaced by the clip
folder in LFS, answer 5), the 1080p overview video, the `record-demo-video` agent skill and its
entry points (not asked), schema validation in `just check`.

## 7. Out of scope

- Any change to `src/`, and so the writing skill. Studio rendering `<video>` is not wanted, in this
  CR or another (answer 13).
- `docs/demo-video/short-demo-01/` and its kit: unchanged.
- A CI job for the kit or the clip; the kit in `just check` or `just preflight`.
- Cropping a clip's GIF for the release notes (answer 14: the zoom stands in for the crop).
- The README: it keeps its presentation video; clips go to the feature's docs and the release note
  (answer 11).
- The release notes, the GitHub release and the announcement of the release that ships CR-481: the
  step and the publication checklist of 3.4 apply at that release, not in this CR.
- Music, voice, title and end cards, vertical formats, the older series of `work/` (horizontal,
  vertical, presentation, chapter showcase).
- Clips of other features.

## Open questions

None. The five questions of the first draft are settled by answers 9 to 13.
