---
title: Show front matter values in the body with this.<field>
description: GitHub issue 334, show the value of a front matter key of the current document inline, as Obsidian does.
status: inbox
date: 2026-11-10
---

# Show front matter values in the body with `this.<field>`

> [!NOTE]
> GitHub issue [#334](https://github.com/gsemet/markdown-okf-schema-studio/issues/334), opened
> 2026-11-09 by an external user, with screenshots from Studio and Obsidian.

## The request

In Obsidian the body can show the value of a front matter key of the document, with the syntax
`=this.<fieldname>` (Dataview inline query, written in inline code). Studio shows the raw text.

## Owner's decisions (2026-11-10)

- Yes, but only for the current document (`this`).
- No reference to another document and no wikilinks for now (the owner notes it would be useful in
  an OKF bundle later).

## For the grill

| Question | First recommendation |
| --- | --- |
| Exact syntax | The Dataview inline form `` `= this.field` `` (with or without the space); check the reporter's screenshot. |
| Missing key | Show the raw text with a warning style, never an empty string. |
| Value types | Strings and numbers as text, lists joined with commas, objects as their YAML on one line. |
| Edit mode | Rendered value in the page; the source keeps the expression; updates when the front matter changes. |
| Writing skill | A new rendered syntax: the skill changes in the same PR (constitution, section 6). |

## Issue link (owner, 2026-11-10)

The PR body says `Fixes #334` so GitHub links and closes the issue, and a comment on the issue links the PR when it opens.
