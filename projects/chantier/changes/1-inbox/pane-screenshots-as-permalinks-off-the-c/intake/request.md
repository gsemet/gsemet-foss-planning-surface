# Pane screenshots as permalinks off the CR branch

Retro of batch-30: a pane screenshot committed as a binary on a CR branch conflicts at every restack of a stack. Put it in the PR as a permalink to a file on the CR branch (or another path that a restack never rewrites), so a restack never conflicts on a binary.