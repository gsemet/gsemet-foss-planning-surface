# Feature clip: export the page to one HTML file

Studio has a feature clip kit (`docs/demo-video/clip-kit/`, CR-482, PR #501) and a recipe
(`docs/demo-video/guidelines/feature-clip-process.guidelines.md`). The CR `short-demo-video-of-the-smart-raw-markdo`
gives them a Markdown storyboard the owner reviews, two captions in turn, several marks in turn,
combined key badges and a PR whose review plays the clip. This CR makes one more clip with the kit and
the recipe as that CR leaves them.

Clip: Export writes one HTML file; opened in a browser, it shows the same themed page with its
diagrams and working tabs. One continuous shot: run the export command from the page, then open the
written file in a browser and click a tab.

The clip lives in `docs/demo-video/clips/export-html/` with its storyboard `clip.md`, its stage
document and its scenario; the batch films the take, renders the GIF, MP4 and WebM, and opens the PR.
