# No edit stays on Saving Markdown for good

Part B of the split of `blank-run-edit-stuck-saving` (issue #485, owner's answer blank-save-Q8). That
CR fixes the one hang the issue found; this one makes sure no edit, of any block kind, can hang the
same way again.

Intent: every final save, of a block, a table cell or a frontmatter field, ends in success or in an
error shown to the writer, and Cancel always closes the editor. Tests prove it for every save path;
a hang they find is a bug fixed here. No time limit and no timeout message (owner, save-guard-Q9).
