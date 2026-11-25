# Feature clip: edit the standard OKF frontmatter in place

This clip shows what Studio does with the standard OKF frontmatter of a page (`title`,
`description`, `status`, `date`, `tags`) when no schema applies: it shows the fields as a plain
Names and Values table above the page, and in edit mode a click on a value opens it for editing.
The clip changes `status` from `draft` to `published`, saves, and the table and the page body
(which shows the field with `= this.status`) both show the new value. A user sees that the
frontmatter is part of the page, not hidden YAML to edit by hand.

It is made with the merged clip kit (`docs/demo-video/clip-kit/`) and the feature clip recipe
(`docs/demo-video/guidelines/feature-clip-process.guidelines.md`): two captions in turn, orange
marks, 1280x720 at 15 fps, no card, the logo top right, a loop, about 11.5 s (at most 12 s). The
clip lives in `docs/demo-video/clips/okf-frontmatter/`.

It is the first of two sibling clips: `okf-schema-bundle-frontmatter` films the same page inside an
OKF Schema bundle, so the viewer sees what a schema adds. Both use the same page, the same field,
the same gesture and the same caption voice.

The storyboard draft is `work/storyboard/clip.md`, with the stage in `work/storyboard/stage/`. By
okf-fm-Q3, the batch films the trial take from this draft, puts its pictures in the storyboard,
renders the clip and opens a draft PR with the clip watchable; the owner reviews the storyboard and
the clip in that draft PR.
