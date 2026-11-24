## Summary

Feature announcements need a few seconds of video: the action, then its result. The existing demo video is a long presentation. This adds a repeatable "feature clip" kit (a real VS Code window filmed over CDP, composed with Remotion, Node.js and ffmpeg only, so it runs on Windows as well as macOS), the process that goes with it, the first clip (raw copy with `balanceEdges` on, pasted into a plain Markdown editor), and the docs site change that plays a clip's WebM where a page shows its GIF.

## Deliverables

The first clip (8.5 s, looping), as the GIF the release notes and docs use:

![Raw copy with balanceEdges on: select across an admonition's edge, Ctrl+C, Ctrl+V, the opening line is added](https://media.githubusercontent.com/media/gsemet/markdown-okf-schema-studio/HEADSHA/docs/demo-video/clips/raw-copy-balance-edges/raw-copy-balance-edges.gif)

Its contact sheet (12 frames across the MP4), filmed at HEADSHA7:

![Contact sheet](https://media.githubusercontent.com/media/gsemet/markdown-okf-schema-studio/HEADSHA/docs/demo-video/clips/raw-copy-balance-edges/contact-sheet.png)

MP4 (for X and the GitHub release): [raw-copy-balance-edges.mp4](https://media.githubusercontent.com/media/gsemet/markdown-okf-schema-studio/HEADSHA/docs/demo-video/clips/raw-copy-balance-edges/raw-copy-balance-edges.mp4)

A clip is one folder under `docs/demo-video/clips/<name>/` with its scenario, storyboard (`clip.md`) and outputs:

```text
docs/demo-video/
├── guidelines/feature-clip-process.guidelines.md   (new)
├── clip-kit/                                       (new: clip.mjs, lib/*.mjs, remotion/)
└── clips/raw-copy-balance-edges/                   (new: clip.md, scenario.mjs, stage/, outputs, evidence)
```

Run with `just clip <name> [doctor|setup|take|render|check|all] [--vsix <path>]`.

The docs site turns `![…](…/clips/<clip>/<clip>.gif)` into a looping muted `<video>` of the WebM with the GIF as fallback (`test/site/siteClips.ts`: `clipVideos`, `copyClipMedia`, `isClipSource`, tested in `test/site/siteClips.test.ts`). Studio and GitHub keep showing the GIF. New requirement `SwRS-MDOKFSTUDIO-CORE-095` (derived from `StRS-MDOKFSTUDIO-CORE-008`) covers it.

Numbers of the last `check` (`check.json`): MP4 952 KB, 1920x1080, 30 fps, H.264 yuv420p, no audio; WebM 575 KB (VP9); GIF 1.40 MB, 960 px, 12 fps, 128 colours, loop count 0; loop seam SSIM 0.98855; playback rate 1.005; 0 paste widgets; reading mode off at start. Filmed on Windows 11, VS Code 1.147.0 (pinned), extension from the branch VSIX, device scale 1.75.

Host and default matrix:

| Host | Setting `balanceEdges` | Result |
| --- | --- | --- |
| Windows 11, pinned VS Code | on | full take passes, pasted text equals the expected text |
| Windows 11, `DEMO_CODE` local install | on | `doctor` and `setup` resolve it |
| Windows 11, display too small (`CLIP_DISPLAY_OVERRIDE=1280x720`) | on | `doctor` fails and names the needed display |
| Windows 11, `⌘C` badge | on | `render` refuses it |
| Windows 11 | off (shipped default) | not filmed: the clip shows the setting on |
| macOS | on | **not proved** (no macOS machine) |

Choices: no title or end card, one caption naming the setting, key badges of the filming platform, a drawn cursor, one zoom on the result with a brief orange outline on the added delimiter line, loop seam one frame short of frame 0.

## Blast radius

Grade: 1. Nothing under `src/` changes and the kit is outside the build, `just check` and CI. The site change is limited to pages that show a clip GIF (only `docs/user/settings.md`). Rollback is `git revert`.

## Autonomous decisions

- Windows `npm` is spawned unquoted with `shell: true` in the kit (a quoted bare `npm` breaks the `.cmd` shim).
- The Studio preview in the take is opened as the custom editor through `workbench.editorAssociations`, because "Open Preview to Side" follows the active editor and would show `notes.md`.
- The kit's host record is copied at take time, so a later `setup` cannot rewrite what a take filmed.

## Known gaps

- macOS is not proved: no macOS machine was available; the first macOS run of the kit proves it.
- Motion, rhythm and the loop as watched are for the maintainer to judge; the raw screencast is about 5 fps, retimed to 30 fps, so cursor motion is stepped.

<details>
<summary>Details</summary>

## Changes

- `docs/demo-video/clip-kit/`: Node-only port of the short-demo kit, lighter (platform, profile, take, prepare, storyboard, encode, check, Remotion composition).
- `docs/demo-video/clips/raw-copy-balance-edges/`: the first clip and its evidence files.
- `justfile` recipe `clip`; `AGENTS.md`, glossary entry, new guideline, pointer in the short-demo guideline, release process steps (clips row, announcement video line, owner-only publish step, GIF crop exception).
- `docs/user/settings.md`: the GIF under the `preview.rawCopy.balanceEdges` entry.
- `test/site/siteClips.ts` and tests, wired in `buildSite.ts`; new SwRS CORE-095; changelog line.

## Human decisions

- The badges show the keys of the platform the clip is filmed on (Ctrl+C on Windows and Linux, ⌘C on macOS); the first clip is filmed on Windows.
- A clip's GIF is not cropped: the clip's one zoom on the result stands in for the crop.
- At a release with a clip, its MP4 replaces the hero image in the announcement thread's first post; the owner uploads it into the GitHub release note.
- The README is not changed; Studio does not render `<video>`: docs embed the GIF and the site turns it into the WebM.
- One shared clip kit, Node.js only, replaces the idea of a separate demo engine; the earlier recording CR is superseded.

## Impacts

The published docs page for the setting plays the clip. No change to the extension.

## Test plan

- [ ] New or changed tests (they fail on the previous code): `test/site/siteClips.test.ts` and a guard in `test/site/siteLinks.test.ts`
- [ ] Requirements: SwRS-MDOKFSTUDIO-CORE-095 added, markers in code and tests, `just requirements-update` and `just requirements-lint` pass
- [ ] Changelog: one user-facing line under `## Unreleased`
- [ ] Local gates: `just check`, site tests (16 passed), `just package`, full clip take; `just preflight` pending
- [ ] Review: approved at (pending)
- [ ] Verified at (pending)
- [ ] CI green at (pending)

## Internal references

CR-482 feature-clip.

</details>
