# One blank-line block per extra blank line

Part C of the split of `blank-run-edit-stuck-saving` (issue #485, owner's answer blank-save-Q8). The
issue's reporter expected each empty line to be its own block; today a run of blank lines shows as
one blank-lines block (CR-444, PR #453).

Intent: in edit mode, each blank line beyond the one Markdown needs as a separator is a block of its
own, at the top level and inside containers; typing in one replaces that line, deleting one removes
that line.
