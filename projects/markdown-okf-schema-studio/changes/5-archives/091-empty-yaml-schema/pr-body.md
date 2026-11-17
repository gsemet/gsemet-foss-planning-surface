## Summary

A `.schema.yaml` file that is empty or holds only comments (typically a schema just created with
"New File") made the frontmatter analysis throw, so the properties table failed instead of showing.

## Deliverables

```text
before: Note.schema.yaml empty  -> TypeError, no table
after:  Note.schema.yaml empty  -> generic table + info row "schema file 'Note.schema.yaml' is empty"
        (0 errors / 0 warnings / 1 info; the type stays without schema until the file has content)
```

The wording is the one okf-schema uses for the same case.

## Changes

- `src/core/frontmatter/okfFrontmatter.ts`: a schema that parses to nothing is treated as "no schema
  content yet" and returns the generic table with that note.
- Requirements: Known issue lines removed, boundary scenario added, update log entry.

## Impacts

No visual change except that the failure no longer happens.

## Blast radius

Grade: 1. One early return in the frontmatter analysis; a plain `git revert` restores it.

## Test plan

- [x] New unit test with an empty, a whitespace-only and a comment-only YAML schema (fails on the previous code with a TypeError)
- [x] Requirements: SwRS updated, markers in code and tests, coverage regenerated
- [x] Local gates: `just check` unit 2640/2640, contracts 2/2, security 46/46, requirements validate and lint 1013 requirements 0 errors
- [ ] Review
- [ ] CI green

## Internal references

- CR 091 (empty-yaml-schema); okf-schema issue 41.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
