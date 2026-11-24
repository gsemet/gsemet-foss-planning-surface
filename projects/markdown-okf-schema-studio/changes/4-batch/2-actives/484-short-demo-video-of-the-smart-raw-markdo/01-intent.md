# Storyboard and two captions for the raw copy feature clip

The raw copy feature (Ctrl+C / ⌘C on a selection copies the raw Markdown under it, PR #498) and its
`markdownOkfSchemaStudio.preview.rawCopy.balanceEdges` setting (PR #499) already have a feature clip:
`docs/demo-video/clips/raw-copy-balance-edges/`. CR-482 (PR #501) made it with the clip kit
(`docs/demo-video/clip-kit/`) and the recipe `docs/demo-video/guidelines/feature-clip-process.guidelines.md`.
The owner likes the clip as it is, one continuous shot: the copy on the left, then a zoom on the
pasted text on the right.

This change gives the clip, and every later feature clip, a storyboard the owner reviews and edits
as easily as the main video's `01-storyboard.md`. That storyboard is Markdown with a section per
beat, its time, its filmed shot, its picture and its on-screen texts, and it stays the clip's live
source. The recipe gains the owner's review of the storyboard before the take and before a render.
The clip shows two captions in turn, one during the action and one during the zoom, with texts
the owner sets. Its key badges read "Ctrl+C / ⌘C" and "Ctrl+V / ⌘V", whatever the platform filmed.
The size and the frame rate become storyboard fields the kit reads: this clip is 1280x720 at 15 fps.

The scene changes, so the clip needs a new stage document and a new take: the selection starts
inside an untitled admonition, in the middle of bold text, crosses a small table and a thematic
break (`---`), and ends inside another admonition, and
the clip shows the characters the setting adds, the closing ones included. An orange mark outlines
each added part in turn (the opening line, the opening `**`, the closing `:::`), so the kit learns
to show several marks in one clip.

The storyboard draft, reviewed and edited by the owner, is in `work/storyboard/clip.md` of this
folder, with the new stage in `work/storyboard/stage/`. The batch brings them into the repository,
changes the kit and the recipe, films the new take, renders the clip again and opens the PR.
