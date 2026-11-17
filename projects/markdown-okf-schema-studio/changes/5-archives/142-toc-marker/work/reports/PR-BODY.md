## Summary

A line containing only `[TOC]` or `[[_TOC_]]` (case-insensitive, outside code), or a MyST `{contents}` directive, now renders the document's headings as a nested, clickable table of contents in the preview. The list is generated, never written to the file, and follows heading changes. `[TOC]` is the syntax of GitLab, Markdown Preview Enhanced and Typora; GitHub shows it as literal text.

## Deliverables

- Read mode: a nested list whose entries link to the headings. `{contents}` accepts `:depth:` and `:local:`; the bracket markers take no options.
- Edit mode: the marker is a block titled with the literal marker (`[TOC]`, `[[_TOC_]]` or the `{contents}` line).
- A palette icon and the `/toc` slash command insert `[TOC]`.

| | Cream | Dark |
| --- | --- | --- |
| Before (read) | ![](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/c65e58d8ce04f4998e6e5d55b5ff0d1f7ad262ec/before-cream.png) | ![](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/c65e58d8ce04f4998e6e5d55b5ff0d1f7ad262ec/before-dark.png) |
| After (read) | ![](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/c65e58d8ce04f4998e6e5d55b5ff0d1f7ad262ec/after-cream.png) | ![](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/c65e58d8ce04f4998e6e5d55b5ff0d1f7ad262ec/after-dark.png) |
| Before (edit) | ![](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/c65e58d8ce04f4998e6e5d55b5ff0d1f7ad262ec/before-edit-cream.png) | ![](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/c65e58d8ce04f4998e6e5d55b5ff0d1f7ad262ec/before-edit-dark.png) |
| After (edit) | ![](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/c65e58d8ce04f4998e6e5d55b5ff0d1f7ad262ec/after-edit-cream.png) | ![](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/c65e58d8ce04f4998e6e5d55b5ff0d1f7ad262ec/after-edit-dark.png) |

## Changes

New renderer `src/core/render/mystToc.ts` and styles `src/core/preview/styles/tocStyles.ts`; `tocTagTitle` in `blockTagTitle.ts`; palette action `toc`; requirements, user guide, slash menu, toolbar docs and changelog updated.

## Impacts

Documents that contain a literal `[TOC]` line now show a table of contents instead of text. The file is never rewritten.

## Blast radius

1 (preview rendering and one palette action).

## Test plan

Unit tests for each syntax and `{contents}` options, palette action test, real-window scenario `toc` (fails on the base, passes here). Unit 2860 pass, 0 fail.
`just check` stops at the requirements coverage check on files unrelated to this change; the real-window CI job was not run.

## Autonomous decisions

- `:depth:` counts list nesting levels.
- Headings coming from `{include}` are not listed; heading text is taken as plain text.
- Only a paragraph that is solely the marker counts.
- The `{contents}` edit title shows the opening line only, not its options.
- The `[[toc]]` syntax of the first idea was dropped in favour of the established syntaxes, without alias.

## Internal references

Change request 142.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
