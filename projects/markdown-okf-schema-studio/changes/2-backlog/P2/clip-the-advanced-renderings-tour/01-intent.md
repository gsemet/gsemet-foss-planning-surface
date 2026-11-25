# Feature clip: the advanced renderings tour

This clip shows in one page every advanced rendering Studio draws in its preview: a Mermaid
flowchart, a PlantUML sequence, a Vega-Lite chart, a full Vega chart, a display equation typeset by
KaTeX and an inline SVG drawing in the page colours. Each one gets an orange mark and a short
caption that names it. It matters to a user because it answers "what can I put in my document?" in
a few seconds, and because PlantUML draws with no Java and charts with no server: everything is
built in and works offline.

It is made with the merged clip kit (`docs/demo-video/clip-kit/`) and recipe
(`docs/demo-video/guidelines/feature-clip-process.guidelines.md`): orange marks in turn, 1280x720 at
15 fps, no card, the logo top right, a loop. It differs in two points the story needs: six captions
in turn (one per renderer) instead of two, and a length of 16 s, past the 12 s limit. The 16 s need
a small kit change in the same PR: the length bound raised to 30 s in the storyboard parser and in
`check`, and one sentence in the recipe. The clip lives in
`docs/demo-video/clips/advanced-renderings-tour/`.

The storyboard draft is `work/storyboard/clip.md`, with the stage in `work/storyboard/stage/`. The
batch films the trial take from the draft, puts its pictures in the storyboard, renders the clip and
opens the PR with the clip watchable (the GIF inline, the MP4 and the WebM linked at the PR's head).
The owner reviews the storyboard and the clip in that PR, which stays a draft until the owner
approves it.
