---
title: "CR 273: show a front matter value in the body with `= this.field`"
description: GitHub issue 334, inline code `= this.field` shows the value of a front matter key of the current document.
status: open
date: 2026-11-10
---

# CR 273: show a front matter value in the body with `= this.field`

> [!NOTE]
> Source: GitHub issue [#334](https://github.com/gsemet/markdown-okf-schema-studio/issues/334).
> Intent: `01-intent.md`; owner's answers: `02-answers.md` (authoritative). Base: `origin/main` at
> `5d2f13cf` (after CR 272, PR #340).

## What ships

Everything in `02-answers.md`, in one PR:

- Inline code whose whole text is `= this.<field>` or `=this.<field>` renders as the value of the key
  `<field>` of the current document's front matter. Only `this`: no other document, no wikilinks.
  A dotted path into a nested object (`this.a.b`) follows the object only if the driver finds it
  natural; otherwise it is out of scope and says so in the PR.
- Strings and numbers show as text, booleans as `true` / `false`, lists joined with `, `, objects as
  their YAML on one line. The value is text, never parsed as Markdown or HTML (no injection path).
- A missing key, or a document without front matter: the raw inline code stays visible with a warning
  style, never an empty string, and the render emits a warning diagnostic.
- Edit mode: the page shows the value; the source keeps the expression; the value updates when the
  front matter changes (front matter edit in the page or in the text editor).
- Inline code in a fenced block, or any inline code that is not exactly the form above, is unchanged.
- The writing skill `skills/writing-for-markdown-okf-schema-studio/` describes the syntax, the value
  formatting and the missing-key style (constitution, section 6; its examples are rendered by a test).

## Requirements

New SwRS created `proposed` with `okfreq new`, under the closest StRS (front matter or rendering). If
the driver finds that an **approved** requirement must change, it stops with `status: blocked` and the
exact sentence to change; the owner decides.

## Issue link (owner, 2026-11-10)

The PR body says `Fixes #334`. The driver does **not** comment on the issue: the main session drafts
the comment with the PR link and posts it after the owner approves.

## Done when

- `` `= this.title` `` in a document with `title: Hello` shows `Hello`; a list key shows its items
  joined with commas; an object key shows one line of YAML; a missing key shows the raw text in the
  warning style. Unit tests prove each case and fail on the unchanged code.
- A value holding `<script>` or Markdown shows as plain text.
- Changing the front matter value updates the rendered value (unit or visual test).
- A visual scenario shows a value and a missing key, light and dark; before/after screenshots in the PR.
- `just check`, `just requirements-update`, a dated log entry, a `CHANGELOG.md` `## Unreleased` line.
