## Summary

Feature announcements need a few seconds of video: the action, then its result. The existing demo video is a long presentation. This adds a repeatable "feature clip" kit (a real VS Code window filmed over CDP, composed with Remotion, Node.js and ffmpeg only, so it runs on Windows as well as macOS), the process that goes with it, the first clip (raw copy with `balanceEdges` on, pasted into a plain Markdown editor), and the docs site change that plays a clip's WebM where a page shows its GIF.

## Deliverables

A clip is one folder under `docs/demo-video/clips/<name>/` with its scenario, storyboard (`clip.md`) and outputs (MP4 for X and the GitHub release, WebM for the site, a light GIF for the release notes and docs):

```text
docs/demo-video/
├── guidelines/feature-clip-process.guidelines.md   (new)
├── clip-kit/                                       (new: clip.mjs, lib/*.mjs, remotion/)
└── clips/raw-copy-balance-edges/                   (new: clip.md, scenario.mjs, stage/, outputs, evidence)
```

Run with `just clip <name> [doctor|setup|take|render|check|all] [--vsix <path>]`.

The docs site turns `![…](…/clips/<clip>/<clip>.gif)` into a looping muted `<video>` of the WebM with the GIF as fallback (`test/site/siteClips.ts`: `clipVideos`, `copyClipMedia`, `isClipSource`). Studio and GitHub keep showing the GIF.

Choices: 8.5 s clip, no title or end card, one caption naming the setting, key badges, a drawn cursor, one zoom on the result with a brief orange outline on the added delimiter line, loop seam one frame short of frame 0.

Clip pictures (GIF, contact sheet) are added to the PR description at the head: see the Test plan evidence once the branch is pushed.

## Blast radius

Grade: 1. Nothing under `src/` changes and the kit is outside the build, `just check` and CI. The site change is limited to pages that show a clip GIF (only `docs/user/settings.md`). Rollback is `git revert`.

## Autonomous decisions

- Windows `npm` is spawned unquoted with `shell: true` in the kit (a quoted bare `npm` breaks the `.cmd` shim).
- The Studio preview in the take is opened as the custom editor through `workbench.editorAssociations`, because "Open Preview to Side" follows the active editor and would show `notes.md`.

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

## Impacts

The published docs page for the setting plays the clip. No change to the extension.

## Test plan

- [ ] New or changed tests (they fail on the previous code)
- [ ] Local gates
- [ ] Evidence
- [ ] Review: approved at (pending)
- [ ] Verified
- [ ] CI green

## Internal references

CR-482 feature-clip.

</details>
