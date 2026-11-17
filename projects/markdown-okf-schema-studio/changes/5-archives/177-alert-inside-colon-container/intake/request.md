# 177 — GitHub alert inside a ::: container closes it early

Night batch 2026-10-28 (user request via the Chief of Staff). From origin/main, one PR.

Backlog intent (verbatim):

> # A GitHub alert inside a `:::` container closes the container early
> 
> From PR #185 review: the alert rewrite emits a closing `:::`, which ends an enclosing
> `:::{card}` / `:::{tab-item}`. Fix: emit a longer colon fence for alerts. Pre-existing. Related:
> alerts inside backtick-fenced directives are not converted; nested `> > [!TIP]` stays a quote.
