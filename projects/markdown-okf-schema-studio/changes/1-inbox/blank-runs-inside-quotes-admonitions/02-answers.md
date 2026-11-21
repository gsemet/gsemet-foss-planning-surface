
## Owner's answers, 2026-11-21

- bq-Q1 Scope. Owner: "Tout d'un coup": quotes (`>`), GitHub alerts, MyST admonitions (every directive kind that holds Markdown content), definition lists and footnote definition bodies, all in this CR, with the same blank-lines block as CR-444 / CR-448.
- bq-Q2 Inside a quote. Owner: "Reste dans la citation": Delete keeps one empty `>` line (the quote stays one quote); a block typed or pasted in place of the run gets the quote's `>` prefix (and the item/content indent when nested, as CR-448 br-Q5), so it stays in the quote.
- Owner, 2026-11-21: "mets tous les inbox dans le batch en cours" then "Griller puis batch": once specified, this CR joins the running batch-07 (stack shape).

## Settled by the Chief of Staff

- Markdown keeps its original format (Studio's DNA): only the removed lines change in the file; prefixes and indents of the surrounding lines are untouched.
- Inside an admonition, a definition or a footnote, a typed block takes the content indent of that container (the same rule as br-Q5 for list items).
