## Summary

Reworks the `export-html` feature clip: a long report page in Cream and Auto width (wide table breaking out of the column, two diagrams, two charts) is scrolled in Studio, exported with Export, then opened in the Integrated Browser where it renders the same. 18 s, three captions, three marks. No behaviour of the extension changes.

## Deviation from the feature clip process

The storyboard review moved from before the take into this PR: the take was filmed from the draft storyboard. An on-screen row the owner changes is a render (`just clip export-html render`, then `check`); a filmed row is a retake. See `docs/demo-video/clips/export-html/clip.md`.

## Deliverables

Round 1 (static files): stage, scenario, storyboard draft, tests, docs. The take and render are not done yet.

## Known gaps

- The take is not filmed yet.
