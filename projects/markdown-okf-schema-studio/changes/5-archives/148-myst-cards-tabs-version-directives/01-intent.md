# MyST cards, tabs and version directives render like MyST, and the README shows them

Type: feat · Priority: P1 · Reported 2026-10-27 by the user (overnight run)

## 1. Standalone cards (`{card}`)

The cards, dropdowns and tabs page of the MyST guide (<https://mystmd.org/guide/dropdowns-cards-and-tabs>)
documents `{card}` outside a grid, with `:header:` and `:footer:` options. Studio renders only
`{grid-item-card}` inside a `{grid}`. This user source does not render as a card:

````md
:::{card} Claude Code
:header: Since v2.1.154, published 2026-05-28

- Saved in `.claude/workflows/` or `~/.claude/workflows/`, run as `/<name>`.
- Runs in the CLI, the Desktop app, the IDE extensions, `claude -p` and the Agent SDK.
:::
````

Expected: a card with its title, the `:header:` line above it, the body, and `:footer:` when
given; the same options as `grid-item-card` where they apply (`:link:`, `:class-card:`, the
`^^^` / `+++` separators).

## 2. Tabs (`{tab-set}` / `{tab-item}`)

The user asked to check them: today there is no support (no code mentions `tab-set` or
`tab-item`). Expected: a tab bar with the `{tab-item}` titles, one panel shown at a time, keyboard
navigation (arrows, Home/End) and ARIA tabs roles, `:sync:` / `:selected:` options. In edit mode
each tab item is editable like any other block.

## 3. `versionadded` / `versionchanged` / `deprecated` title

![The admonition titled "Added in version :: 0.47:"](image-versionadded-title.png)

The user's screenshot came from a typo in their source (`:::{versionadded}:: 0.47`, an extra
`::`): **no lenient parsing for that** (user decision). Check only the valid form:

````md
:::{versionadded} 0.47
Added support for `.include` keyword.
:::
````

Expected title: `Added in version 0.47` (no trailing colon if Studio adds one today), same rule
for `versionchanged` ("Changed in version …") and `deprecated` ("Deprecated since version …").
If the valid form already renders correctly, record it in the report and keep only a test.

## 4. README

Add a README section with real-window screenshots (cream + one dark theme) that show these
"advanced" admonitions Studio supports: `versionadded` / `versionchanged` / `deprecated`, a card,
a tab set. Update `docs/user/` where the supported MyST directives are listed.

## Proof

Unit tests of the three renderings, a webview test for the tab keyboard behaviour, before/after
real-window screenshots for each.
