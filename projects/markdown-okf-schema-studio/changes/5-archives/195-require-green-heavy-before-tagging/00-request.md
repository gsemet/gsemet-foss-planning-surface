# 195 — Require a green heavy run before tagging

Night batch 2026-10-28 (user request via the Chief of Staff). From origin/main, one PR.

Backlog intent (verbatim):

> # Require a green heavy run of the release commit before tagging
> 
> From the Pages reuse change (PR #192): the Pages deploy takes the fast path (reuse the e2e reports)
> only if a green heavy CI run of the exact tagged commit exists; otherwise it falls back to running
> the whole suite. Nothing enforces a green heavy run before tagging. Options: tag-release checks for
> one (and skips tagging with a clear message), or the release checklist / `just version` dispatches
> heavy and waits. Decide in the grill.
