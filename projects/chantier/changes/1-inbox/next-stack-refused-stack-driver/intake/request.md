# next stack refused for a stack driver; cards swapped mid-batch

Priority P2. A stack driver's card command `next stack --lease <n>` is refused, and a running batch
met new cards under an older prompt. Filed on 2026-11-26 from the Chief of Staff session of
markdown-okf-schema-studio, on the owner's word.

The owner, verbatim: "Pardon, oui, il faut mettre dans l'inbox du projet chantier en P2."

Facts, from the events of that project's batch-09 (chantier 0.15.1, shape stack, Foreman mode):

- Ask A-50 (2026-11-26 14:15Z), the stack driver: its prompt names `references/startup-core.md` and
  `startup-manifest.json`, neither in the chantier checkout at 266b784f (it read `stack-driver.md`
  whole and the help topics instead); and `chantier next stack --lease 32` exits 1 with
  `error: unknown CR stack in batch batch-09` (it took the steps from `help stack-joins` and
  `help stack-make`).
- Ask A-51 (14:24Z), again after the next restack: `next stack --lease 33` is refused with the same
  error; it went on from the card and the help topics.
- `skills/chantier/references/stack-driver.md` line 3 names that command: "`$CHANTIER next stack
  --lease <n>` and the `next:` lines give the steps".
- The checkout the batch runs from (plugin root) was fast-forwarded to 266b784f at 15:06:28 +0100,
  while the batch ran (its reflog). The range holds 7714288e, "feat(cards)!: swap in the new role
  cards and remove the old set". The Chief of Staff of that batch also found its earlier cards gone
  at its next read.

Effect seen: both stack drivers finished from the cards and the help topics; the stack was delivered.

Not examined: whether `next` is meant to accept the unit `stack` in this version, and whether a
running batch should keep the cards it started with.
