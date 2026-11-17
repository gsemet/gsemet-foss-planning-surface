## Summary

In edit mode, an opened HTML comment now shows its literal syntax as the block title, in code font:
`<!-- -->` for a plain comment and `<!-- TODO -->` for a TODO comment, instead of a bare word.
TODO detection follows one rule: an HTML comment whose text starts with `TODO` (case-insensitive,
colon optional, single or multi-line). Lower-case `todo` comments were previously missed.

## Deliverables

Before (title is the word "TODO") and after (title is the literal tag), cream theme:

| Before | After |
| --- | --- |
| ![before cream](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/dbde87396f1604ccedf8621c059781883ab69644/before-cream.png) | ![after cream](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/dbde87396f1604ccedf8621c059781883ab69644/after-cream.png) |

Dark theme:

| Before | After |
| --- | --- |
| ![before dark](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/dbde87396f1604ccedf8621c059781883ab69644/before-dark.png) | ![after dark](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/dbde87396f1604ccedf8621c059781883ab69644/after-dark.png) |

A helper, `openingTagTitle` (`src/core/render/blockTagTitle.ts`), computes the shortened opening
tag of an HTML block (`<div align="center">`, with `…` when long). It is unit-tested and not wired
yet: the edit-mode renderer currently drops raw `<div>`, `<p>` and `<picture>` blocks, so there is
nothing to title; the follow-up change that renders such HTML will use it.

## Changes

- Comment title rendering and styles; TODO detection fix; new requirement and widened existing one.
- User guide updated; changelog entry.

## Impacts

Edit-mode comment blocks only. Read mode and the Markdown source are unchanged.

## Blast radius

1

## Test plan

- Unit tests for the title helper, comment markers and styles.
- A real VS Code window scenario that fails on the old code and passes now.
- `just check` green (the requirements coverage check reports churn on a stale baseline; unrelated).

## Autonomous decisions

- HTML block titles are not wired because no such edit-mode block exists yet; the tested helper is shipped for the follow-up.
- `[[toc]]` has no marker in this code base, so nothing was titled.

## Internal references

CR 140 (edit-mode-tag-in-block-title).

🤖 Generated with [Claude Code](https://claude.com/claude-code)
