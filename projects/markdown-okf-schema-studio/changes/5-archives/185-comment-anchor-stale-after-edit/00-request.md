# 185 — Comment anchor stale after an edit adds lines

Night batch 2026-10-28 (user request via the Chief of Staff). From origin/main, one PR.

Backlog intent (verbatim):

> # Comment thread below an edit that added lines is saved but not highlighted
> 
> Source: demo video track B, 2026-10-28 (observed while scripting, cause not proven).
> 
> After an in-preview edit that adds lines, creating a comment thread on a paragraph further down
> saves the thread but shows no highlight and no badge; Refresh does not help. A thread above the
> edit works. Suspected stale source-line mapping for blocks after the edit. Reproduce headless if
> possible, then real input.
