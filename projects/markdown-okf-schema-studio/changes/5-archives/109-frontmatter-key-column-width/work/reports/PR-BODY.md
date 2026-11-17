## Summary

In the front-matter properties table of the Markdown preview, the key column was so narrow that
keys wrapped letter by letter ("na/me", "des/cri/pti/on"). The key column now keeps each key on one
line and is wide enough for its keys.

## Deliverables

The key column fits the longest key, capped at 40% of the table. Longer keys end with an ellipsis
and show the full key as a tooltip. The value column takes the remaining width and wraps normally.

```css
/* key cell */ white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
/* name cell */ max-width: 40cqw;  /* section: container-type: inline-size */
```

The collapse happens when a long value sits next to short keys: the table shares its width by
content, so a long description squeezed the key column to about 40 px and short keys such as
"name" broke letter by letter. A header "Names" that is wider than every key now also stays on one
line.

Before / after on front matter like a skill file (long description, metadata block):

| | Cream | Dark |
| --- | --- | --- |
| Before | ![before cream](shots/before-r2-cream.png) | ![before dark](shots/before-r2-dark.png) |
| After | ![after cream](shots/after-r2-cream.png) | ![after dark](shots/after-r2-dark.png) |

Short keys only (header "Names" kept whole):

![after short keys](shots/after-r2-short-keys-dark.png)

## Changes

- Properties table styles and key markup (tooltip on keys over 24 characters).
- Requirement for the front-matter table updated; unit tests and four visual scenarios added.

## Impacts

Preview front-matter table only. Screenshots above.

## Blast radius

1: CSS and markup of one table.

## Test plan

`just check` (2687 unit tests) and the 368 visual scenarios pass.

## Autonomous decisions

- The key never wraps inside a word; the width is fitted to the longest key and capped at 40%.
- Over-long keys ellipsize with the full key as tooltip; the value column wraps normally.

## Internal references

CR 109, backlog item bug-squized-frontmatter.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
