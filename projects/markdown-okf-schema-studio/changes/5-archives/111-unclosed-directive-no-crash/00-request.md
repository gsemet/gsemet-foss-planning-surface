# 111 — Unclosed directives render as raw text instead of crashing

Type: fix · Priority: P1 · From backlog: `02-backlog/P1/bug-crash-extension`

## Intent (user)

When a document contain the opening of a list-table but not the close

````md

```{list-table}

````

it crashs instead of just printing the raw line

---

Same with this

````md

(label-name

:::{table} Caption

:::

)=
````

more generally, syntax error should be much better tested !

## Autonomous decisions

- Decided by the main session on 2026-10-26 under the user's instruction "pas de questions, full autonome". List these in the PR body under "Autonomous decisions".
- Any unclosed fence or directive (```` ```{list-table} ````, `:::{table}`), dangling label `(name` / `)=`, renders the raw source lines as a paragraph or code block; the preview never crashes and the rest of the document renders.
- Add a syntax-error test suite (parser unit tests plus one preview e2e) covering at least: unclosed backtick directive, unclosed colon directive, unclosed label, label without target, nested unclosed directive, empty directive at end of file. Use the item's example.md as a fixture.
- A visible hint is out of scope; raw text is enough.
