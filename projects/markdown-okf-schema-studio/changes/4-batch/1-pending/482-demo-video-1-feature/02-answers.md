# Grill answers

Short name: `feature-clip`.

1. feature-clip-Q1, length and dressing: A. A clip lasts about 5-12 s with no title or end card. It starts on the action, carries a small logo mark in a corner and loops cleanly as a GIF.
2. feature-clip-Q2, outputs: A. Each clip is rendered as MP4 (for X, which does not take WebM), WebM (for the Sphinx docs and site) and a light GIF (for the GitHub release notes and the README).
3. feature-clip-Q3, production: A. Reuse and lighten the short-demo-01 kit (a real VS Code window, CDP capture, Remotion) into one shared "feature clip" kit, driven by a small per-clip scenario. The kit also runs on Windows.
4. feature-clip-Q4, on-screen text: A. One short caption (the why) and key badges for the shortcuts (Ctrl+C, Ctrl+V), a drawn cursor and one zoom on the result.
5. feature-clip-Q5, where clips live: A. One folder per clip under `docs/demo-video/clips/`, holding its scenario and its outputs in Git LFS. The release-process guideline gains a step: a visible feature may get a clip, linked as a GIF in the release note and attached as MP4 to the announcement post.
6. feature-clip-Q6, the old P4 CR `record-demo-video`: A. Closed as superseded by this CR. Its useful parts (engine, capture) are taken into this spec, and it is dropped with a pointer here.
7. feature-clip-Q7, timing of the first clip: A. In the running batch batch-09, stacked after copy-raw-edge-balancing (CR-481), so the clip ships with the feature in the same release.
8. Chief of Staff routine (2026-11-24): the first clip shows the smart copy with the `balanceEdges` setting on: a selection crossing an admonition's or a list's edge is copied with Ctrl+C, pasted into a plain Markdown editor with Ctrl+V, and the pasted text shows the added delimiters. The caption names the setting. Grilled enough: specify now. Spec critic: yes (a new kit and a process step).
9. feature-clip-Q9 (2026-11-24, spec open question 1): **Which announcement post carries the MP4.** B, against the recommendation: the clip replaces the hero image in post 1 and becomes the thread's hook.
10. feature-clip-Q10 (spec open question 2): **Mark on the added delimiter.** A. A brief orange outline around the added delimiter line during the zoom on the result.
11. feature-clip-Q11 (spec open question 4): **README.** A. No. The README keeps its presentation video; clips go to the feature's docs and the release note.
12. Chief of Staff routine (spec open question 5): the key badges show the keys of the platform the clip is filmed on (Ctrl+C on Windows and Linux, ⌘C on macOS). The first clip is filmed on Windows.
13. feature-clip-Q12 (spec open question 3, after the owner asked whether GitHub renders video in Markdown; it plays only files uploaded through its UI, not a relative `.mp4` in the repository): A. At publication, the MP4 is uploaded into the GitHub release note, which plays it natively. The release-note file in the repository keeps the GIF. No CR for Studio rendering `<video>`.
14. feature-clip-Q14 (2026-11-24, spec critic F1): **A full-window clip GIF against the release-note crop rule.** A. The release-process guideline gains an exception: a clip's GIF is not cropped, and the zoom on the result stands in for the crop.
15. Chief of Staff routine (2026-11-24, spec critic F2-F12, all applied):
    - F2: the site commit is `feat: play feature clips as video on the published site`, with its CHANGELOG line. The kit stays `build`, the guidelines and the clip stay `docs`.
    - F3: the publication checklist becomes a new owner-only item after step 6, and line 7 is amended. The MP4 has a 10 MB budget, enforced by `check`.
    - F4: when no device scale fits, `doctor` fails and names the display it needs. The work area is read on Windows with a PowerShell `System.Windows.Forms.Screen` query. The measured display size goes into `check.json`.
    - F5: the profile sets `"editor.pasteAs.showPasteSelector": "never"`, and the frame checks include "no paste widget".
    - F6: `setup(t)` puts Studio in reading mode and checks it. The trial's proof names the mouse drag-select path.
    - F7: `docs/demo-video/clips/**/*.md` is excluded from the site rendering.
    - F8: the VS Code version is pinned in the kit default, with `DEMO_CODE` as the override.
    - F9: the `.cmd` trap row also covers npm and npx.
    - F10: the fade ends one frame before frame 0, and `first-last.png` asks the maintainer to judge the fade-out.
    - F11: `clipVideos` takes a repository root, or a file-exists callback.
    - F12: the CR-481 path becomes `4-batch/2-actives/481-copy-raw-edge-balancing/`.

Destination: running batch batch-09, after CR-481.
