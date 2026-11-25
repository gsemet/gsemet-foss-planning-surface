# index: keeps broken links in root summaries, validate misses them

Issue: https://github.com/gsemet/okf-schema/issues/57
Reporter: elmpp, 2026-11-06T08:49:09Z

## Summary

`okf-schema index` keeps the existing summary text of a root-index entry verbatim, even when that text contains links that only resolve from the subdirectory. The resulting root `index.md` has broken links, and `okf-schema validate` doesn't report them because it doesn't check links in `index.md` files.

## Steps to reproduce

```bash
okf-schema new --path kb/bundle --name api/health-check --type "API Endpoint" --title "Health Check"
okf-schema index --path kb/bundle

# Give the root entry a summary copied from api/index.md (links relative to api/)
printf -- '# bundle\n\n- [api](api/index.md) — [Health Check](health-check.md)  [API Endpoint]\n' > kb/bundle/index.md

okf-schema index --path kb/bundle
cat kb/bundle/index.md
okf-schema validate --path kb/bundle
```

## Actual

`index` reports `1 updated` and writes:

```markdown
# bundle

- [api](./api/) — [Health Check](health-check.md)  [API Endpoint]
```

`health-check.md` doesn't exist at the bundle root, since the file is `api/health-check.md`. `validate` reports no W2 for it, and the bundle is reported as conformant.

For comparison, a broken link in a concept is detected:

```
WARNING [W2] Broken cross-link 'nope.md' in '.../api/health-check.md'
```

## Expected

At least one of:

- `index` regenerates the root entry's summary, or rebases its relative links onto the subdirectory, instead of keeping text whose links don't resolve from the root.
- `validate` checks links in `index.md` files and reports W2 for broken ones.

## Context

In my real bundle the root `index.md` ended up as:

```markdown
- [_schema](./_schema/) — [_base.schema.yaml](_base.schema.yaml)
- [api](./api/) — [Health Check](health-check.md)  [API Endpoint]
```

I couldn't confirm whether `okf-schema` first wrote those summaries. Another tool in my setup also writes this file. On a fresh bundle, `index` writes `Auto-generated index for concepts in \`api\`.` instead. Either way, `index` keeps the broken links once they're present, and `validate` doesn't flag them.

## Environment

- okf-schema 0.17.0
- macOS (Darwin 24.6.0)

