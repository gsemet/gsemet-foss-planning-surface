# T1 — Caution alerts: red accent and octagon icon

Repo /Users/az02065/Projects/DevTools/markdown-okf-schema-studio, branch `fix/caution-alert-style`
(from origin/main 9b5ac08). Read `00-request.md` (decisions) and `rules.md` first.

## Change

- `src/preview/previewStyles.ts`: `ICONS` (~line 80–100) gets an `octagon` icon (16×16 path, same
  style as `triangle`/`cross`: outlined shape + "!" bar and dot, evenodd-compatible like the others).
  In the accent rules (~line 3020) remove `.caution` from the warning group
  `:where(.warning, .attention, .caution, .versionchanged)` and give `.caution` its own rule:
  `--sphinx-preview-accent: var(--vscode-charts-red, #f14c4c); --sphinx-preview-icon: ${ICONS.octagon};`.
  Check every theme the stylesheet supports (current VS Code theme, light, dark, cream) still gets a
  readable red: look for theme blocks overriding the accents/charts colours.
- Check other places mapping caution to warning-like styling (grep -i caution in src/, e.g. palette
  alert menu icons in editActions.ts / editPalette, slash menu): if an alert picker shows a
  per-type colour/icon, make Caution match. Do not change the rendering of `{danger}`, `{error}`,
  `{warning}`, `{attention}`.

## Tests

- Unit `test/webview/previewStyles.test.ts`: the assertion near line 292 pins the warning group; update
  it to the new group (keep its intent: warning/attention/versionchanged stay yellow) and add tests:
  `.caution` uses `--vscode-charts-red` and `ICONS.octagon`, and is no longer in the yellow group.
  Write them first; record that they fail on the unchanged code.
- Visual e2e (`test/visual/scenarios.ts`, fixture `37-gfm-gallery`, ~line 1967 and the alert check ~227):
  add an assertion that the computed accent (border-inline-start colour or title colour) of the
  Caution alert differs from Warning and equals the Danger/red one (compare computed colours in the
  page, no hard-coded rgb), in light and dark. Make sure the scenario captures a screenshot of the
  five GFM alerts usable for the PR (light + dark); report the PNG paths under
  `out/reports/e2e/screenshots/`.
- If a test fixture with a MyST `{caution}` exists, check it renders red too (assertion if cheap).

## Docs

- CHANGELOG.md, Unreleased: one "Fixed"/"Changed" bullet in the file's style (GitHub `[!CAUTION]`
  and MyST `caution` callouts are red with a stop-sign icon, like GitHub, instead of Warning amber).
- README.md: only if it describes alert colours/icons.

## Gates (foreground, windowless only)

`npx tsc -p .` then `just check` and `just visual`. Do NOT run integration / `test:e2e` / anything
that opens VS Code windows (the user is using VS Code; CI runs the full preflight).
