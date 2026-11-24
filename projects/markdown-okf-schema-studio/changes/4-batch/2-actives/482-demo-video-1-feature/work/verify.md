# Verify CR-482 feature-clip

Head: 0f52108f18ab5172ff131e0c426dd136447a3147

All claims below judged at 0f52108f18ab5172ff131e0c426dd136447a3147 (worktree batch-09-CR-482, `git rev-parse HEAD`), unless it says carried.

## Claims proved

1. E2 site unit tests (SHA 0f52108f). Command: `npm run compile` then
   `node --import ./scripts/register-myst-patches.mjs --test out/test/site/siteClips.test.js out/test/site/siteLinks.test.js`
   (the `.ts` files do not run directly: extensionless imports need the compiled `out/`).
   Output: `tests 16, pass 16, fail 0`, including: clip GIF with WebM and poster becomes the video; no poster; no WebM stays img;
   GIF outside clips folder or not named like its folder unchanged; copyClipMedia copies only webm/gif/poster; no clips folder
   no error; "the shipped settings page plays the raw copy clip as video"; "a clip's storyboard and stage documents are not
   site pages"; "a clip's WebM keeps its relative path from a docs page" (the siteLinks guard).
2. The shipped-page test fails on the previous code (SHA 0f52108f vs base). Command:
   `git cat-file -e origin/main:test/site/siteClips.ts` -> `fatal: path 'test/site/siteClips.ts' exists on disk, but not in 'origin/main'`
   (exit 128: no module on the base, so the test cannot pass there); `git diff origin/main...HEAD -- docs/user/settings.md`
   shows the single added image line under `preview.rawCopy.balanceEdges` (absent on the base). I did not run the test on a
   detached base worktree (the test file and module do not exist there).
3. Output files (SHA 0f52108f). Command: `ffprobe -show_entries stream=...,format=duration,size` on mp4 and webm.
   mp4: h264, 1920x1080, yuv420p, 30/1, duration 8.5, 952052 bytes, one stream (video only). webm: vp9, 1920x1080, yuv420p,
   30/1, 8.5 s, 574936 bytes, one stream (video only). These equal `check.json` (mp4 952052, webm 574936, GIF 1396686,
   SSIM 0.98855, passed: true, 20 checks all ok, playback rate 1.005, reading mode off, 0 paste widgets, VS Code 1.147.0
   pinned, extension source vsix, win32). GIF: `ls -la` 1396686 bytes, starts `GIF89a`; check.json loopCount 0, 960 px, 12 fps,
   128 colours, ladder step 0. All under the 10/3/3 MB budgets, duration inside 5 to 12 s.
4. `just clip raw-copy-balance-edges doctor` (SHA 0f52108f): exit 0; lines ok for Node 24.22.3, ffmpeg 9.1 and ffprobe, encoders
   libx264, libvpx-vp9, gif, playwright-core, @vscode/test-electron, scratch folder, Remotion install, VS Code 1.147.0 downloaded,
   `display: 3440x1392, device scale 1.75`.
5. Small-display matrix cell (SHA 0f52108f): `CLIP_DISPLAY_OVERRIDE=1280x720 just clip raw-copy-balance-edges doctor` -> exit 1,
   `FAIL display: The display is too small: no device scale fits. The take needs a work area of at least 1920x1080 physical
   pixels (1.5 times 1280x720); this one measures 1280x720 (CLIP_DISPLAY_OVERRIDE).` plus `fix:` line and `FAILED: doctor found problems`.
6. Badge platform refusal (SHA 0f52108f), proved at the function `storyboard.mjs` uses, not through a `render` run (that would
   need a clip.md edit and a take folder): `node -e` importing `wrongModifier`: `"⌘C" win32 -> ⌘ or Cmd`, `"Cmd+C" win32 ->
   ⌘ or Cmd`, `"Ctrl+C" win32 -> ok`, `"Ctrl+C" darwin -> Ctrl`, `"⌘C" darwin -> ok`. `buildStory` throws on a non-undefined result
   (read at lines in `lib/storyboard.mjs`). clip.md holds `Ctrl+C` and `Ctrl+V`.
7. Evidence images (SHA 0f52108f, files unchanged since 8a916a8d: `git diff --stat 8a916a8d HEAD` is CHANGELOG.md only).
   Opened contact-sheet.png, frames/01-selected.png, 02-pasted.png, 03-zoomed.png. Show: runbook in Studio left, empty notes.md right,
   caption pill and logo throughout; drag selection from "database" across the admonition edge to the following paragraph;
   Ctrl+C and Ctrl+V keycaps; pasted text starting with `:::{important} Before you deploy`, `database migrations first, ...`, `:::`,
   blank, `The deploy script ...`; orange outline on the first line in the zoom (03) and in contact frames at 4.958 to 5.667 s;
   no paste widget; zoom out at 7.8 s. Window title reads "workspace"; no username, home folder or personal path visible.
   Observation, not a failure: 01-selected.png shows the selection ending at "schema" without the final period (the drag is not
   finished in that frame), while the page selection at the chord ends with the period (verify passed; contact frame 2.833 s
   shows the full selection). Motion, rhythm and the loop as watched were not judged.
8. Release and docs content (SHA 0f52108f): diff holds the glossary entry, the AGENTS.md target and guideline pointer, the CHANGELOG
   line `... (PR #501)`, the feat commit `5858108e`, build `b112dec3`, docs `8a916a8d`, SwRS CORE-095 and its index/log entries.
   `just requirements-lint` exit 0 (`use case diagrams: 94 StRS checked`). CI at 0f52108f (`gh pr view 501`): static,
   static-windows, visual, viewer-graph, report, checks SUCCESS; heavy jobs (integration, stress, gallery) SKIPPED.
9. Preflight (carried from 8a916a8): gate log `work/gates/preflight.log` ends `ci-static: passed` and `preflight: ... stages skipped on
   Windows`; head moved 8a916a8d -> 0f52108f by CHANGELOG.md only, which the Driver's log records. Caveat: the log's first line is
   `rm -rf out .artifacts`, not a CR-and-SHA line, so the log does not itself name its SHA; the Driver note (`just preflight: pass` at
   8a916a8) is the only link. No `chantier gate` pass exists at the head (the ship event says so).
10. PR description (SHA 0f52108f; body is `pr-body.md`, fetched from the PR page not re-read): sections render; the three images
    use `media.githubusercontent.com/media/.../8a916a8d.../raw-copy-balance-edges.gif`, `contact-sheet.png` and the mp4; the same
    paths at head 0f52108f return HTTP 200 with size 1396686 (GIF), 389697 (contact sheet), 380977 (poster), equal to the local
    files (assets identical between 8a916a8d and head). Summary, Deliverables and Changes match the diff; Known gaps lists macOS and
    motion. No image shows a username or home path (item 7). Items for the Driver to fill, not failures yet: Test plan lines
    "just preflight pending", "Review: approved at (pending)", "Verified at (pending)", "CI green at (pending)" (log shows r3 approved
    at 8a916a8, carried to 0f52108f; CI green at 0f52108f; preflight passed at 8a916a8); the matrix row "`render` refuses it"
    for the ⌘C badge is proved here only at `wrongModifier` (item 6).

## Not proved, stated plainly

- E3 full take and the `DEMO_CODE` matrix cell: not re-run (instructed); the take's numbers are `check.json` as committed, the ffprobe
  of item 3 agrees. `DEMO_CODE` doctor/setup run not re-proved.
- E4 site build: not proved. `just site-assemble` not run (instructed). No heavy dispatch exists for this branch (`gh run list`
  shows only the two `pull_request` runs; `gallery` SKIPPED), so `out/site/...settings.html` holding the `<video>`, the WebM, GIF and
  poster in `out/site/docs/demo-video/clips/raw-copy-balance-edges/`, and no `clip.html`, is covered only by the unit tests of item 1.
- E5 GitHub's view of the GIF in `docs/user/settings.md`: not opened visually. Only that the LFS file at the head resolves on
  `media.githubusercontent.com` (item 10).
- macOS: not provable here; the PR already says so.
- Scenario motion, loop rhythm as watched, and a phone view of the MP4: the maintainer's.

VERIFIED
