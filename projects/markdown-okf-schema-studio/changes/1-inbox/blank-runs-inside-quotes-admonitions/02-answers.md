
## Owner's answers, 2026-11-21

- bq-Q1 Scope. Owner: "Tout d'un coup": quotes (`>`), GitHub alerts, MyST admonitions (every directive kind that holds Markdown content), definition lists and footnote definition bodies, all in this CR, with the same blank-lines block as CR-444 / CR-448.
- bq-Q2 Inside a quote. Owner: "Reste dans la citation": Delete keeps one empty `>` line (the quote stays one quote); a block typed or pasted in place of the run gets the quote's `>` prefix (and the item/content indent when nested, as CR-448 br-Q5), so it stays in the quote.
- Owner, 2026-11-21: "mets tous les inbox dans le batch en cours" then "Griller puis batch": once specified, this CR joins the running batch-07 (stack shape).

## Settled by the Chief of Staff

- Markdown keeps its original format (Studio's DNA): only the removed lines change in the file; prefixes and indents of the surrounding lines are untouched.
- Inside an admonition, a definition or a footnote, a typed block takes the content indent of that container (the same rule as br-Q5 for list items).

## Owner's answers, 2026-11-21 (spec critic's questions)

- bq-Q3 Context-tag panels (`<example>` and the like). Owner: "Oui, les montrer": in scope; container line = the opening tag line, typed block takes that line's leading whitespace.
- bq-Q4 Closed dropdown. Owner: "Quand il est ouvert": the block shows only while the dropdown is open (refresh on `toggle`); an editor already open stays if the writer closes it.
- bq-Q5 New entry typed between two definition entries. Owner: "Nouvelle entrée": a term followed by a `:` line typed in a run between two entries is written at the list's indent (a sibling entry); any other text takes the definition's content indent. Same rule for a `[^x]:` definition typed in a run between two footnote definitions.
- bq-Q6 `{epigraph}`, `{pull-quote}`, `{blockquote}`. Owner: "Oui, l'afficher dedans": give their quote its end line so the block shows inside it.

## Settled by the Chief of Staff (spec critic, 2026-11-21)

- Tab items: nothing shown (their bodies are unmapped and edited whole).
- Footnote label line alone (`[^b]:` then a run then the indented body): a footnote run, 4-space indent (critic F2: column 0 would turn the body into a code block). A run between two footnote definitions keeps the top-level rule, except bq-Q5.
- Critic findings F1 (equal-line order and delete target), F3 (final line break), F4 (footnote DOM order: `aboveOf` by largest line, delete target by holder), F5 (any non-container holder in the chain shows nothing), F6 (forged container line accepted as in CR-448; tab after `>` keeps columns) are fixed in the spec.
