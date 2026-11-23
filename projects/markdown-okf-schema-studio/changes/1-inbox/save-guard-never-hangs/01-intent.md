# No edit stays on Saving Markdown for good

Part B of the split of `blank-run-edit-stuck-saving` (issue #485, owner's answer blank-save-Q8). That
CR fixes the one hang the issue found; this one makes sure no edit, of any block kind, can hang the
same way again.

Intent: every final save ends in success or in an error shown to the writer, after a time limit at
most; the frontmatter editor's "Saved. Refreshing preview…" wait is bounded too; Cancel always
closes the editor. Tests cover the save state always leaving "Saving…".
