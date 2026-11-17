## Summary

In the rendered preview, tables with many columns squeezed some columns to a single character
per line ("do / cu / me / nt"). Table cells now keep a readable minimum width; a table that no
longer fits uses the existing wide-table behaviour (breaks out of the text column in Auto width,
scrolls horizontally otherwise).

## Deliverables

Rule added to the preview styles: `table:not(.okf-properties) :where(th, td) { min-width: 5em }`.
The frontmatter properties table is excluded. Edit mode keeps its own cell minimum (8em).

Before / after, cream theme:

| Before | After |
| --- | --- |
| ![before cream](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/cb29dfaf5c9e0e8b8ed9d75ad2e3afc6e60e8a0f/before-cream.png) | ![after cream](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/cb29dfaf5c9e0e8b8ed9d75ad2e3afc6e60e8a0f/after-cream.png) |

Before / after, dark theme:

| Before | After |
| --- | --- |
| ![before dark](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/cb29dfaf5c9e0e8b8ed9d75ad2e3afc6e60e8a0f/before-dark.png) | ![after dark](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/cb29dfaf5c9e0e8b8ed9d75ad2e3afc6e60e8a0f/after-dark.png) |

## Changes

- Preview styles: minimum cell width.
- Requirement LAYOUT-032 and the wide-tables user guide updated; changelog entry.
- Tests: a unit test on the style rule and a computed-style assertion in the GFM gallery visual scenario (fails without the rule).

## Impacts

Tables with many short columns now scroll sideways instead of squeezing.

## Blast radius

1 (preview CSS only).

## Test plan

Unit suite (2813 pass), GFM visual group (8/8), real-window before/after screenshots.

## Autonomous decisions

- The preview had no prior minimum, so "double" was not applicable: 5em was chosen.
- Edit mode does not share the rule.
- Inline code in dark-theme header cells is hard to read; it was already so and is untouched.

## Internal references

CR 138. Requirement coverage check (`okfreq update-coverage --check`) could not be validated locally with the pinned okfreq; CI should confirm.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
