# The `:header:` and `:footer:` options of a grid card are hidden with no hint

Severity Low · Observed once · Verdict Gap · Requirements: SwRS-MDOKFSTUDIO-MYST-053 (header via `^^^` only), MYST-100 (options for standalone `{card}`) · Area Grid cards · Side preview ·
c3-3 · Replay none (fixture `fixtures-visual/73-grid-card-editing.md`)

## Currently / Expected

No visual: the header text "okf-schema, okfreq, okfkb" of the first card in `fixtures-visual/73-grid-card-editing.md` appears nowhere in the preview (measured: 0 `.myst-grid-card-option`, text absent).

## Why this is wrong

A standalone `{card}` shows `:header:`; a `{grid-item-card}` with the same option drops it silently, in a repository fixture meant to show card editing. The author sees text vanish and cannot click it to edit it. Either render it, as the docs imply ("like a grid-item-card"), or show the line as a muted unsupported option.

**Steps.** Open fixture 73 in the preview, edit mode on.
**Fix.** Render or flag the option. Uncheck to disagree: [x]
**Test.** No test: depends on the choice; a render test pins it. Uncheck to disagree: [x]
**Requirement.** State in MYST-053 whether the option is supported. Uncheck to disagree: [x]
