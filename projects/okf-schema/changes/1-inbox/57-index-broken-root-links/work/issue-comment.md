Thanks for the report. This is accepted, and we reproduced it.

To your question: these summaries are written by `okf-schema index` itself. When the root `index.md` has no summary for a subdirectory yet, it copies the first non-heading line of that subdirectory's `index.md`, often a list entry whose relative link only works from there.

- `index` will only take the introduction written before the first list of the subdirectory's `index.md` (links rewritten to work from the root), otherwise a generic sentence. Never a list entry.
- Running `index` will repair the summaries already damaged this way, and will refresh the generic sentence.
- Other summaries already written in an index are kept, and schema summaries still take precedence.
- `validate` will report W2 for broken links in `index.md` files too, so `--strict` will fail on them.
- `#...` anchors will be ignored when links are checked (today `page.md#part` is reported as broken).

Not part of this change: concept descriptions edited after indexing are not refreshed in existing index entries; that is tracked separately.

No date yet; the pull request will be linked here.
