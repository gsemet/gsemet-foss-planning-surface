# Plan: `show` prints the stored file

## What changes for you

For a concept whose file reads:

```markdown
---
generated: {by: okf-enforcer/0.6, at: 2026-11-06T08:49:21Z}
---
# Health Check
```

| | Output of `okf-schema show` |
| --- | --- |
| Today | the frontmatter re-written in another style, then a `trust: ...` line before the body |
| After the change | the file above, as stored |

## Behaviour

- Nothing is added to or removed from the file: style, quoting and YAML comments are kept.
- No `trust:` or `stale: true` line.
- No validation: a file without frontmatter, or with invalid YAML, is printed as it is.
- `show_bundle` (Python API) also returns the exact stored text; its current fields are unchanged.

## Compatibility

A script that read the `trust:` or `stale: true` lines of `show` no longer finds them. The `verified` field of the file stays visible, `list` keeps its `[STALE]` marker, and the API keeps `trust_tier` and `stale`.

## Limits

The trust tier is displayed by no command.
