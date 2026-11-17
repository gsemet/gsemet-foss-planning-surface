## Summary

Under a dark VS Code colour theme, blockquotes on light preview themes (Cream, White) showed a
near-black box, because VS Code's default webview stylesheet paints `blockquote` with the host
colour and the preview never set its own background. Blockquotes now get a tinted background from
the active preview theme (on Cream, a cream a step darker than the page), in light and dark. The
left rule is kept.

## Deliverables

Blockquote rule in the preview stylesheet (`contentBlockStyles.ts`):

```css
#sphinx-myst-preview-content blockquote {
  padding: 0.25em 1em;
  border-radius: 0 4px 4px 0;
  background: var(--studio-textBlockQuote-background, rgba(128, 128, 128, 0.08));
}
```

The theme token `--studio-textBlockQuote-background` already exists per theme (cream: `#efe9dd` on a
`#f5f1e8` page). A unit test pins the rule and fails without it; the rendering requirement gains a
scenario for it.

Before / after, in a real VS Code window (Default Dark Modern host theme, `> toto` / `> tata` and
inline code in a quote):

| Preview theme | Before | After |
| --- | --- | --- |
| Cream | ![before cream](SCREENSHOT_BASE/before-vscode-dark-cream.png) | ![after cream](SCREENSHOT_BASE/after-vscode-dark-cream.png) |
| White | ![before white](SCREENSHOT_BASE/before-vscode-dark-white.png) | ![after white](SCREENSHOT_BASE/after-vscode-dark-white.png) |

## Autonomous decisions

- Root cause: VS Code injects `blockquote { background: var(--vscode-textBlockQuote-background) }`
  in `@layer vscode-default`; the preview rule is unlayered with an id selector, so it wins. A unit
  test models that host rule and fails without the preview rule. Inline code in a quote only looked
  dark because of the quote behind it; its own tint is unchanged.
- Audit of other elements against VS Code webview defaults: `code`, `pre`, `table`, `th`/`td`, `hr`
  and body are overridden by the preview. `kbd` is not: its default light-grey text is barely
  legible on Cream and White under a dark host. Not fixed here (scope); worth a follow-up. Link
  colour was not measured.

- Cream theme: cream background a step darker than the page, existing left rule kept.
- Other themes reuse their own tokens through one CSS variable, with a neutral grey fallback.
- Small vertical padding and rounded outer corners added so the tint does not touch the text.
- Nested quotes stack the tint; accepted for now.

## Internal references

Screenshots source: `.agents/changes/03-requests/107-blockquote-theme-background/reports/shots/`
(to be pushed to the `-assets` branch by the stack driver; replace `SCREENSHOT_BASE`).

🤖 Generated with [Claude Code](https://claude.com/claude-code)
