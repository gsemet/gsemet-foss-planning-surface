# show: resolve concept names given without the .md extension

Issue: https://github.com/gsemet/okf-schema/issues/56
Reporter: elmpp, 2026-11-06T08:42:59Z

## Summary

`okf-schema show` fails with "Concept not found" when the concept is given without the `.md` extension, which is exactly how the Getting Started tutorial tells users to call it.

## Steps to reproduce

Following [Getting Started → Inspect the bundle](https://github.com/gsemet/okf-schema/blob/main/docs/source/tutorials/getting-started.md#inspect-the-bundle), after creating `api/health-check` with `okf-schema new`:

```bash
okf-schema show --path my-knowledge-base/bundle api/health-check
```

## Expected

The document and its frontmatter are printed, as the tutorial says.

## Actual

```
Error: Concept not found: <cwd>/my-knowledge-base/bundle/api/health-check
```

Adding the extension works:

```bash
okf-schema show --path my-knowledge-base/bundle api/health-check.md
```

## Notes

- `okf-schema new --name api/health-check` accepts the name without an extension, so `show` not doing the same is inconsistent.
- `okf-schema list` prints `api/health-check.md`, so users can't tell which form is canonical.
- Suggested fix: have `show` try `<name>.md` when `<name>` doesn't exist (or fix the tutorial, if the extension is meant to be required).

## Environment

- okf-schema 0.17.0
- macOS (Darwin 24.6.0)


---

Comment by elmpp, 2026-11-06T08:53:24Z:

The [links and backlinks tutorial](https://github.com/gsemet/okf-schema/blob/main/docs/source/tutorials/knowledge-graph.md) hits the same bug: `okf-schema show --path my-knowledge-base/bundle runbooks/service-unavailable` fails with "Concept not found".

`okf-schema backlinks` already accepts names without the extension (`backlinks ... api/health-check` works), so `show` could resolve names the same way.
