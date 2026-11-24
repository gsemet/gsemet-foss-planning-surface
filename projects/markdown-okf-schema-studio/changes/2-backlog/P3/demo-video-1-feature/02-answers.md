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

Destination: running batch batch-09, after CR-481.
