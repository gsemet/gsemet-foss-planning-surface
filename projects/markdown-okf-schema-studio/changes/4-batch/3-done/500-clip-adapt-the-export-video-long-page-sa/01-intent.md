# Feature clip: export a long page, same render in the browser

This clip reworks the merged `export-html` clip with a stronger story. Studio shows a long report
page in its default Cream theme, with card grids, tables, Mermaid diagrams, a Vega-Lite chart and a Vega chart,
and one table so wide that it breaks out of the centred text column (the Auto width mode). The clip
scrolls through that page, exports it with the Export button, then opens the exported file in a
browser: the same page, the wide table still breaking out, the diagrams and charts drawn. A reader
with no editor gets the page exactly as the writer sees it; that is what the clip sells.

The browser is VS Code's Integrated Browser inside the filmed window, on the exported file served
by a small local server started off camera, as in the merged clip (the kit films the VS Code window
only). The story has three beats (scroll, export, the same page in the browser), so it needs about
18 s, past the recipe's former 12 s cap. The 30 s limit comes from the CR
`clip-the-advanced-renderings-tour`, which raises the kit's maximum length for the whole round;
this CR is built after it and makes no kit change of its own.

It is made with the merged clip kit (`docs/demo-video/clip-kit/`) and the feature clip recipe
(`docs/demo-video/guidelines/feature-clip-process.guidelines.md`): captions in turn (three here),
orange marks in turn, 1280x720 at 15 fps, no card, the logo top right, a loop. It replaces the
storyboard, scenario and stage of `docs/demo-video/clips/export-html/` in place (same clip folder,
same file names for the outputs), and updates what points at the old clip.

The storyboard draft is `work/storyboard/clip.md`, with the stage in `work/storyboard/stage/`. The
batch films the trial take from this draft, puts its pictures in the storyboard, renders the clip
and opens the PR with the clip watchable (the GIF inline, the MP4 and the WebM linked at the PR's
head). The owner reviews the storyboard and the clip in that PR, which stays a draft until the
owner approves (Q3).
