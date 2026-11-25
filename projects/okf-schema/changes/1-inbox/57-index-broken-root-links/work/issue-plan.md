# Plan: subdirectory summaries and link checks in `index.md`

## What changes for you

With `api/index.md` containing only a list of concepts:

| | Root `index.md` line |
| --- | --- |
| Today | `- [api](./api/) — [Health Check](health-check.md)  [API Endpoint]` |
| After the change | ``- [api](./api/) — Auto-generated index for concepts in `api`.`` |

If `api/index.md` has an introduction before its first list, that introduction is used instead, with its relative links rewritten to work from the root.

## Behaviour

- Summaries already damaged by the copy are recomputed by the next `okf-schema index`.
- The generic sentence is recomputed on each run, so an introduction added later reaches the root.
- Other summaries already written in an index are kept; schema summaries still take precedence.
- `okf-schema validate` reports W2 for broken links in every `index.md`.
- `#...` anchors are ignored when links are checked, in concepts and index files. The anchor itself is not verified.

## Compatibility

A bundle with broken links in an `index.md` gets new W2 warnings, so `validate --strict` can start failing until `okf-schema index` or a manual fix removes them.

## Limits

Concept descriptions edited after indexing are not refreshed in existing index entries (separate change).
