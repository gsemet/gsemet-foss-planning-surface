## Summary

GitHub `[!CAUTION]` alerts and MyST `caution` callouts rendered exactly like Warning (amber,
triangle icon). They now use the danger red with a stop-sign (octagon) icon, as GitHub renders
them, in every preview theme. Warning, Attention, Danger and Error are unchanged.

Fixes known issue K4 from the visual campaign.

## Changes

- Preview stylesheet: a new octagon icon; `.caution` leaves the yellow warning group and gets the
  `--vscode-charts-red` accent.
- CHANGELOG: Unreleased bullet.

## Screenshots

| Light | Dark |
| --- | --- |
| ![Caution alert, light theme](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/6b984e3fe4ef3aaf4b0eb31bd8fcd070486a3def/caution-alerts-light.png) | ![Caution alert, dark theme](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/6b984e3fe4ef3aaf4b0eb31bd8fcd070486a3def/caution-alerts-dark.png) |

## Test plan

- [x] Unit: new test (fails on the old stylesheet) checks `.caution` is red with its own icon and
  out of the warning group; the warning-group assertion is updated with the same intent.
- [x] Visual e2e (`37-gfm-gallery`): the Caution title colour equals the computed
  `--vscode-charts-red` and differs from Warning.
- [x] Local: `just check` and `just visual` (255 scenarios) green; unit 1703/0.
- [ ] CI: full `just preflight` (integration under xvfb).

🤖 Generated with [Claude Code](https://claude.com/claude-code)
