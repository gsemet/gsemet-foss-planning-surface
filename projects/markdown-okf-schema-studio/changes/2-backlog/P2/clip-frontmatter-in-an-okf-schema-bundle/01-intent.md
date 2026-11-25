# Feature clip: the frontmatter in an OKF Schema bundle

This clip shows what changes when a page lives in an OKF Schema bundle: its `type: note` finds
`_schema/note.schema.yaml`, and Studio shows the frontmatter as a schema table (a type icon and a
Description column per field), validates the values and flags a wrong one in red with a ✖ badge.
The page starts with the typo `status: publshed`. In edit mode a click on the value opens a typed
control, a select with the schema's values; the clip picks `published`, saves, and the error and
the badge go away while the page body shows the new value. A user sees that the schema guides and
checks the frontmatter, not only shows it.

It is made with the merged clip kit (`docs/demo-video/clip-kit/`) and the feature clip recipe
(`docs/demo-video/guidelines/feature-clip-process.guidelines.md`): two captions in turn, orange
marks, 1280x720 at 15 fps, no card, the logo top right, a loop, about 12 s (at most 12 s). The
clip lives in `docs/demo-video/clips/okf-schema-bundle-frontmatter/`.

It is the second of two sibling clips, after `okf-frontmatter`: the same page, the same `status`
field, the same click and save chord, the same caption voice and marks. Only `type: note` and the
`_schema/` folder are added, so what differs on screen is what the schema brings.

The storyboard draft is `work/storyboard/clip.md`, with the stage in `work/storyboard/stage/`. By
bundle-fm-Q3, the batch films the trial take from this draft, puts its pictures in the storyboard,
renders the clip and opens a draft PR with the clip watchable; the owner reviews the storyboard and
the clip in that draft PR.
