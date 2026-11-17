## Summary

Three small preview lifecycle limitations are fixed, and a setting that never did anything useful is
removed. Open Preview to Side no longer refuses to work from a Studio Open With tab. A render-engine
load that failed once at start-up is retried by the first render instead of failing forever. The
`preview.doubleClickToSwitchToEditor` setting is removed: a single click in the preview already
reveals the matching source line, so the setting added nothing.

## Deliverables

```text
Before                                          After
Open With tab active, Open Preview to Side  ->  previews that tab's file
engine load fails once at start-up          ->  next render loads it again
preview.doubleClickToSwitchToEditor         ->  setting removed; single click still reveals
```

Setting removal: users who still have `markdownOkfSchemaStudio.preview.doubleClickToSwitchToEditor`
in their `settings.json` will see VS Code's unknown-setting hint and can delete the line. Nothing
else changes for them: double-click never had a visible effect beyond the clicks it is made of.

## Changes

- `src/host-vscode/activation.ts`: with no active text editor, the command falls back to the
  document of the active tab when that tab is a Studio Open With editor; other custom editors are
  still refused.
- `src/core/render/mystEngine.ts`: the engine loader forgets a failed import (a loaded engine is
  still shared).
- Removed the setting from the settings registry, the generated `package.json` schema
  (`just generate-settings`), the page double-click listener, the host gate, the `double-click`
  reveal activation, the user documentation and the requirements (now a removal note in the
  changelog).
- Requirements: Known issue lines removed from the Open Preview and engine warm-up SwRS; the
  panes-follow-each-other SwRS now covers two settings and states that a double click has no
  behaviour of its own; the dependent SwRS and the use case drop the setting.
- Not fixed: a change by another tool to the document of the active text editor still counts as
  typing and does not glow. VS Code does not say where a change comes from and the host only knows
  the cursor line, so any heuristic would make the preview glow while the writer types. It stays an
  explicit Known issue of its SwRS.

## Impacts

No visual change. The removed setting disappears from the Settings editor.

Changed assertions: the tests that checked a double-click reveal with the setting off/on, and the
package-contract test that checked the setting's text, now assert that a double click posts nothing
beyond its clicks and that the setting is not contributed. The settings-registry, boot-context and
configuration tests no longer list the setting.

## Blast radius

Grade: 2. Touches the settings registry, the page boot context and the generated settings schema,
plus the command entry point and the engine loader. Revert restores everything; a user setting
value left in `settings.json` is simply ignored either way.

## Test plan

- [ ] New or changed tests (they fail on the previous code): Open With tab command, failed engine
      load retried, package contract, double click posts nothing
- [ ] Requirements: SwRS updated, markers in code and tests, `okfreq` validate/lint/coverage
      clean
- [ ] Local gates: `just check` green (2661 unit, 2 contract, 47 security tests; okfreq validate, lint and coverage clean); window suites not needed
- [ ] Review
- [ ] CI green

## Internal references

- Change request 100 (lifecycle-small-fixes); SwRS LIFE-010, LIFE-094 (unchanged), LIFE-097,
  CORE-001 / CORE-027.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
