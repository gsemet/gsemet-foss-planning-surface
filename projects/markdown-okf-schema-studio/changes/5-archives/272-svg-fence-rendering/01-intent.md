---
title: Render a svg fence (and maybe inline svg) as a picture
description: GitHub issue 336, agents write SVG straight into Markdown and Studio shows the XML.
status: inbox
date: 2026-11-10
---

# Render a svg fence (and maybe inline svg) as a picture

> [!NOTE]
> GitHub issue [#336](https://github.com/gsemet/markdown-okf-schema-studio/issues/336), opened
> 2026-11-09 by an external user, no comment yet.

## The request

Some harnesses teach their model to write SVG inside the Markdown it produces. Studio shows the XML
instead of the picture. The reporter asks to render it ("rasterize the svg instead of displaying the
xml"). Their example is a fenced block with the `svg` language:

````markdown
```svg
<svg viewBox="0 0 960 320" xmlns="http://www.w3.org/2000/svg" font-family="sans-serif" font-size="13">
  <rect x="15" y="15" width="450" height="290" rx="8" fill="var(--surface)" stroke="var(--border)" stroke-width="1.5"/>
</svg>
```
````

## What Studio does today (origin/main)

- A `svg` fence is a highlighted code block.
- Raw `<svg>` in the Markdown is dropped (the writing skill says so; `SwRS-MDOKFSTUDIO-PALETTE-229`
  lists `svg` among the elements dropped on paste). The skill tells agents to write the SVG to a file
  and show it with `{figure}` or `![]()`.
- The CSP already allows `data:` images (`src/core/security/csp.ts`).

## Questions for the grill (first thoughts, not decided)

| Question | First recommendation |
| --- | --- |
| Scope | The `svg` fence only, like `mermaid` and `plantuml`; raw `<svg>` stays dropped. |
| How | Sanitize (no script, `foreignObject`, event handler, external `href`), then show it as an `<img>` with a `data:` URI: an image never runs scripts. A toggle shows the source, as for other diagrams. |
| `var(--surface)` and other CSS variables | They do not resolve inside an `<img>`. Either map the common ones to the theme colours, or inline the sanitized SVG in the page (more risk). Needs a decision. |
| Writing skill | Must change in the same PR (constitution, section 6): the svg fence becomes a third way to draw. |
| Size | Rendered with its `viewBox`, capped at the column, eligible for the Auto breakout. |

## Owner's decisions

- 2026-11-10: render both the `svg` fence and raw `<svg>` in the Markdown (raw `<svg>` is no longer
  dropped at render; check what this means for the paste rule of `PALETTE-229`).
- CSS variables (2026-11-10): option B. The sanitized SVG is inlined in the page, and Studio defines the common variable names (`--surface`, `--border`, `--text`...) from its theme colours, so the picture follows Cream, White and Dark. An unknown variable uses its `var()` fallback, else the text colour. The sanitizer removes scripts, `foreignObject`, `on...` handlers, external links and `<style>`, and scopes or renames `id`s.
- Writing skill (2026-11-10): `skills/writing-for-markdown-okf-schema-studio/` describes what is possible: the `svg` fence and raw `<svg>`, the variable names it can use and their meaning, what the sanitizer removes, and when a file with `{figure}` is still the better choice.
