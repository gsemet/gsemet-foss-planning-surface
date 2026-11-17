# A GitHub alert inside a `:::` container closes the container early

From PR #185 review: the alert rewrite emits a closing `:::`, which ends an enclosing
`:::{card}` / `:::{tab-item}`. Fix: emit a longer colon fence for alerts. Pre-existing. Related:
alerts inside backtick-fenced directives are not converted; nested `> > [!TIP]` stays a quote.
