# 155 — Changed front matter fields show the change bar

Type: fix · Priority: P2 · From backlog: `02-backlog/P2/diff-line-not-shown-in-frontmatter`

## Intent

See [01-intent.md](../01-intent.md). When the diff with the last commit changes or adds a front matter
field, the properties table shows no change line in the left margin, unlike every other block.

## Autonomous decisions (orchestrator, 2026-10-28; list them in the PR body)

- Granularity: one bar per changed or added field row in the properties table (not one bar for the
  whole table); a removed field shows a deleted marker like a removed block, if the existing
  diff gutter has one, else the table-level bar. Use the same colours as body blocks.
- Stack position 2, above #166.
