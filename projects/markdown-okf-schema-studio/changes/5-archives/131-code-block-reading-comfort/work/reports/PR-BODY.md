## Summary

Code blocks in the preview were hard to read: highlighting was weak and long blocks had no line
numbers. This PR replaces highlight.js with Shiki, which uses the same TextMate grammars and the
Dark+ colours as the VS Code editor, puts code blocks on a dark background in every preview
theme, and adds line numbers to multi-line blocks. Both new behaviours can be turned off in the
settings.

## Deliverables

- **Shiki highlighting** with the JavaScript regex engine (no WebAssembly), so Restricted Mode and
  the strict content security policy keep working. Common languages are bundled; an unknown
  language renders as plain text, never as an error.
- **Dark code background** (`markdownOkfSchemaStudio.preview.codeBlocks.darkBackground`, default
  on): Dark+ background in the cream and white themes too. Inline code is unchanged.
- **Line numbers** (`markdownOkfSchemaStudio.preview.codeBlocks.lineNumbers`, default on): only for
  blocks of two lines or more, and never copied (neither by the copy button nor by a mouse
  selection). MyST `:linenos:`, `:lineno-start:` and `:emphasize-lines:` on `{code-block}` /
  `{code}` win over the setting, block by block.
- Package size: VSIX 7.79 MB before, 8.37 MB after (+0.58 MB).

Before (cream theme) and after, in a real VS Code window:

| Before | After |
| --- | --- |
| ![before cream](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/42178dd59cb0bbb3e0a1bcbd0aa2a354e16da9bf/before-window-cream.png) | ![after cream](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/42178dd59cb0bbb3e0a1bcbd0aa2a354e16da9bf/after-window-cream.png) |
| ![before dark](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/42178dd59cb0bbb3e0a1bcbd0aa2a354e16da9bf/before-window-dark.png) | ![after dark](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/42178dd59cb0bbb3e0a1bcbd0aa2a354e16da9bf/after-window-dark.png) |

Code blocks, close up (white and cream themes, MyST options):

![after white blocks](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/42178dd59cb0bbb3e0a1bcbd0aa2a354e16da9bf/after-window-white-blocks.png)
![after cream blocks](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/42178dd59cb0bbb3e0a1bcbd0aa2a354e16da9bf/after-window-cream-blocks.png)

## Changes

- Shiki replaces highlight.js in the preview renderer; two new settings; styles for the dark code background and line numbers; requirements and tests.

## Impacts

VSIX grows by 0.58 MB. Existing code blocks look different (dark background, Dark+ colours, line numbers in blocks of two or more lines) unless the two settings are turned off.

## Blast radius

3 of 3: touches every rendered code block, adds a dependency and a bundle.

## Autonomous decisions

- The new dependency `shiki` is installed in its own `node_modules`; highlight.js is removed.
- Colours are emitted as CSS classes rather than inline styles, to keep the strict CSP.
- Comments are no longer italic (as in Dark+); diff blocks become padded rounded blocks on the
  dark background.
- `tsconfig.json` now lists the DOM lib, because highlight.js was the only source of DOM types.
- Requirements-lint could not run locally (installed `okfreq` lacks `--check-links`); the index
  entries for the two new requirements need `just requirements-update` with a newer `okfreq`.

## Test plan

Unit tests, visual scenarios (five new) and the real-window suite; the requirements lint is checked by CI.

## Internal references

Change request 131; requirements CODE-039, CODE-040 (new), CODE-001/005/007 and CORE-028 (updated).

🤖 Generated with [Claude Code](https://claude.com/claude-code)
