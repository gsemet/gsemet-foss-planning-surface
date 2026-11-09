---
id: 334-frontmatter-keys-in-body
project: markdown-okf-schema-studio
stage: inbox
kind: feature
source:
  forge: github
  repository: gsemet/markdown-okf-schema-studio
  issue: 334
  url: https://github.com/gsemet/markdown-okf-schema-studio/issues/334
  title: "Frontmatter keys display in body"
  state: open
  reporter: phansoks
  reporter_role: external user
  opened: 2026-11-09T11:58:06Z
  comments: 1
  labels: []
  synced: 2026-11-09
area: rendering, frontmatter
requirements: []
code:
  - src/core/frontmatter/propertiesTable.ts
  - src/core/render/renderPipeline.ts
priority: null
understanding: partial
reproduced: true
open_questions: 5
attachments:
  - path: intake/attachments/01-studio-render-0f745592.png
    shows: Studio renders `=this.<field>` as literal inline code
  - path: intake/attachments/02-obsidian-render-13d7b96b.png
    shows: Obsidian replaces each `=this.<field>` with the frontmatter value
  - path: intake/attachments/03-markdown-source-cf9bc8d2.png
    shows: the Markdown source, inline code spans `=this.<field>`
---

# Show frontmatter values in the body (`=this.<field>`)

## The request

A user (phansoks) writes notes in Obsidian, where an inline code span `` `=this.<field>` `` is
replaced by the value of that key in the note's own frontmatter. They ask Studio to do the same.

Source of the note: a section with a NOTE callout and a list, each item ending in an inline code
span `=this.stars_github`, `=this.contributeurs_actifs`, `=this.derniere_activite`,
`=this.licence`, and `=this.type_signal` in the callout.

![Markdown source](intake/attachments/03-markdown-source-cf9bc8d2.png)

| Studio today | Obsidian |
| --- | --- |
| ![Studio: literal code spans](intake/attachments/01-studio-render-0f745592.png) | ![Obsidian: values](intake/attachments/02-obsidian-render-13d7b96b.png) |

Studio shows the code spans as they are; Obsidian shows `Dépôt de code`, `12800+`, `500+`,
`2026`, `Apache-2.0`.

## What we know

- **This is not core Obsidian, it is the Dataview plugin**: `` `= expr` `` is a Dataview inline
  expression (DQL), and `this` is the current note. Dataview also has `` `$= …` `` (DataviewJS)
  and `[[Other note]].field` for another note's field.
- **The owner's comment** (2026-11-09): "syntax look like `=this.<fieldname>`. Does it work for
  external document?" Asked of the reporter, no answer yet. With Dataview, yes:
  `` `=[[Other note]].field` ``.
- **Studio today:** no Dataview support anywhere in the code. The frontmatter is shown as a
  properties table at the top (FMSCHEMA requirements, `propertiesTable.ts`), never inside the
  body.
- The visible part of the request is only `this.<key>` for a scalar key. Everything beyond is
  open.

## Open questions

1. **Scope:** only `` `=this.<key>` `` (the current file's frontmatter), or also another file's
   keys (`[[Other]].key`), nested keys (`this.a.b`), lists, and Dataview expressions
   (`=this.a + 1`, functions)?
2. **Name and compatibility:** reuse Dataview's syntax as is (Obsidian files render the same in
   both tools), or a Studio/OKF syntax (a MyST role like `` {field}`key` ``)? Dataview syntax is
   the cheaper adoption path.
3. **A missing key:** show the code span as today, an empty value, or a marked "unknown key"?
4. **Editing:** clicking the value opens the block's source as usual, or edits the frontmatter
   key?
5. **Opt-in:** always on, or behind a setting, since a literal `` `=this.x` `` code span becomes
   a value?

## Next step

Grill with the owner (questions 1, 2 and 5 shape the feature), maybe ask the reporter what they
need beyond `this.<key>`. Then a specification, with new SwRS requirements. A feature, not
automatable.
