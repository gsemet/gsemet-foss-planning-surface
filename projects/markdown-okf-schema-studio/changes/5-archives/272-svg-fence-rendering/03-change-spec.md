---
title: "CR 272: render a svg fence and a block-level raw svg as a themed picture"
description: GitHub issue 336, SVG written straight into Markdown shows as a picture that follows the theme.
status: open
date: 2026-11-10
---

# CR 272: render a svg fence and a block-level raw svg as a themed picture

> [!NOTE]
> Source: GitHub issue [#336](https://github.com/gsemet/markdown-okf-schema-studio/issues/336).
> Intent: `01-intent.md`; owner's answers: `02-answers.md` (authoritative); the public plan and demo
> posted on the issue: `artifacts/svg-plan.md`, `artifacts/svg-theme-demo.html`. Base: `origin/main` at `da6d7b14`.

## What ships

Everything in `02-answers.md`, in one PR:

- A fenced block with the `svg` language and a raw `<svg>` that fills a whole block render as an inline
  picture. A `<svg>` inside a sentence stays dropped.
- A sanitizer (allow-list, never a deny-list) removes scripts, `foreignObject`, `on…` handlers, external
  links and `<style>`, and renames `id`s (and the `url(#…)` / `href="#…"` references to them) per picture.
- The theme vocabulary of `02-answers.md` is defined on the picture's scope from the existing
  `--studio-*` tokens of the three theme modes (and of the VS Code theme); an unknown `var()` with no
  fallback resolves to the text colour.
- Size: `viewBox` and declared width kept, capped at the column, eligible for the Auto breakout.
- Edit mode: a click opens the block's source editor, as for a Mermaid diagram.
- The writing skill `skills/writing-for-markdown-okf-schema-studio/` describes both forms, the variable
  list, what the sanitizer removes, and when a file with `{figure}` is still better; its "Raw SVG" and
  "Limits" parts change accordingly (constitution, section 6; its examples are rendered by a test).

## Requirements

New SwRS created `proposed` with `okfreq new`, under the closest StRS. `StRS-MDOKFSTUDIO-GFM-002`
(approved) lists the raw HTML subset and says active content is removed: the change must stay inside
its words (sanitized SVG is not active content). If the driver finds that an **approved** requirement
must change, it stops with `status: blocked` and the exact sentence to change; the owner decides.

## Issue link (owner, 2026-11-10)

The PR body says `Fixes #336`. The driver does **not** comment on the issue: the main session drafts
the comment with the PR link and posts it after the owner approves.

## Done when

- The issue's example renders as a rounded rectangle in the block colour with a border, in Cream, White
  and Dark, never black.
- Hostile SVG (script, `onload`, `foreignObject`, `<a href="https://…">`, `<style>`, `<use href="https://…">`,
  `javascript:` URLs, duplicate ids across two pictures) is neutralized; unit tests prove each case and fail
  on the unchanged code where the behaviour is new.
- A visual scenario shows a fence and a raw block in light and dark; before/after screenshots in the PR.
- `just check`, `just requirements-update`, a dated log entry, a `CHANGELOG.md` `## Unreleased` line.
