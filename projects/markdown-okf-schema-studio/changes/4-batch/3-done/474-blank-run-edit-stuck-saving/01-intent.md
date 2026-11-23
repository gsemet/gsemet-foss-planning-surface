# Editing a blank-lines block gets stuck on Saving Markdown

issue: https://github.com/gsemet/markdown-okf-schema-studio/issues/485

In edit mode, a run of two or more blank lines shows as one blank-lines block (CR-444, PR #453).
Clicking that block and typing text leaves the editor stuck on "Saving Markdown…": the text is
written and renders below, but the editor never closes, and neither Done nor Cancel recovers it.

Intent: typing in a blank-lines block saves and returns to the rendered view like any other block,
and no edit can stay in "Saving…" for good. Tests cover blank-run segmentation, editing a blank-only
block (text in place of the run), and the save state always leaving "Saving…".
