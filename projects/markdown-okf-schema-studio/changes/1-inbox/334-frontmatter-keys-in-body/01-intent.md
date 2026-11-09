---
type: cr-intent
id: 334-frontmatter-keys-in-body
description: "Feature from an external user: render Dataview-style `=this.<field>` with the note's frontmatter values, as Obsidian does; scope still open."
generated: {by: "agent:claude-opus-5-5", at: "2026-11-09T14:30:00Z"}
sources: [{id: issue, resource: "https://github.com/gsemet/markdown-okf-schema-studio/issues/334", title: "Frontmatter keys display in body", author: "github:phansoks", last_modified: "2026-11-09"}]
---

# Show frontmatter values in the body (`=this.<field>`)

In Obsidian, an inline code span `` `=this.<key>` `` shows the value of `<key>` from the note's
frontmatter. Studio shows the code span as is. The user asks for the same rendering.

| Source | Studio today | Obsidian |
| --- | --- | --- |
| ![Source](intake/attachments/03-markdown-source-cf9bc8d2.png) | ![Studio](intake/attachments/01-studio-render-0f745592.png) | ![Obsidian](intake/attachments/02-obsidian-render-13d7b96b.png) |

## Known

- **It is the Dataview plugin, not core Obsidian.** Dataview also reads another note's field:
  `` `=[[Other note]].key` ``, which answers the owner's comment on the issue.
- **Studio has no Dataview support**; the frontmatter is shown only as the properties table at the
  top.

## Open

1. Scope: `this.<key>` only, or other notes, nested keys, expressions?
2. Syntax: Dataview's as is (same files in both tools), or a Studio/MyST one?
3. Always on, or behind a setting?

## Next

Grill with the owner; maybe ask the reporter what they need beyond `this.<key>`. A feature, not
automatable.
