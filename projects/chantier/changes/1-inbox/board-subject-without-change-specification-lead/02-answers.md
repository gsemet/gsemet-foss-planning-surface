# Answers

- The request: user, 2026-11-20: "Dans la board, dans les items de la colonne Subject, je vois que
  chaque item commence par "Change Specification: ". ca prend de la place pour rien".
  The lead takes room for nothing: remove it from what the board shows.

## Settled by the Chief of Staff (2026-11-20, the user asks no questions)

1. Fix at the root: the CLI records a CR's title without the "Change Specification:" lead (any
   case, with an optional `#` and byte-order mark before it), so batch.json, STATUS.* and the
   pane get the plain subject. The board's display strip stays, as a guard for old records, and is
   applied in every board view: one shared function, case-insensitive.
2. Records already written are not rewritten.
3. The heading of `03-change-spec.md` itself stays as the cards prescribe
   (`# Change Specification: <subject>`).
4. A test in `tests/` covers the stripped title when a CR joins a batch; small and parametrized.
