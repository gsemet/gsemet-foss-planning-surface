# Transparent sync with Confluence

URL to confluence in frontmatter

```md
type: confluence_sync
url: 'https://confluence.dt.renault.com/pages/viewpage.action?pageId=275319589'
title: tttt
---

This is the content of Confluence page converted to Markdown with key extensions.
```

## Real difficulties:

- ensure bijection when converting from/to confluence., **without** losing data
- put unsupported confluence blocks into specific directive (section/columns,...). User will request to expand supported syntax later.
- Goal is to 2-way, non-destructive, asynchronous (multiuser) mapping of confluence features to Markdown OKF-Schema Studio
- For instance inline comments can be mapped to the feature 'inline-comment-thread'
- include attachments
- only 1 page edition.
- connexion to confluence is external (an MCP, CLI,...).
  - Import/export are out of the business of this tool
  - but the convertion from/to the intermediate format (Confluence Wiki + json + attachment) in a working folder is

## Goal:

- confluence page acts like a share surface
- I have my copy in local, converted in Markdown, agent can work on it

## Antipattern

- expose all local markdown as "Markdown Macro" in confluence
