# index: keeps broken links in root summaries, validate misses them

issue: https://github.com/gsemet/okf-schema/issues/57

## Intent (grilled 2026-11-25, see 02-answers.md)

`okf-schema index` itself writes broken links in the root `index.md`: without a schema or
existing summary, it copies the first non-heading line of a subdirectory's `index.md`, list
entries included, then preserves it forever. `okf-schema validate` checks no link in any
`index.md`.

`index` must write only the subdirectory's introduction (links rewritten from the root) or the
generic text, recompute the damaged summaries and the generic text, and `validate` must report W2
for broken links in index files, ignoring `#...` anchors.
