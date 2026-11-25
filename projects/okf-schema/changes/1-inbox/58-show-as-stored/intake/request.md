# show: stray trust line and reformatted frontmatter

Issue: https://github.com/gsemet/okf-schema/issues/58
Reporter: elmpp, 2026-11-06T08:53:53Z

## Summary

`okf-schema show` doesn't print the concept as stored. It adds a `trust: unverified` line after the closing `---`, where it reads as body text, and it re-serializes the frontmatter in a different style from the file on disk.

## Steps to reproduce

```bash
okf-schema new --path kb/bundle --name api/health-check --type "API Endpoint" --title "Health Check"
cat kb/bundle/api/health-check.md
okf-schema show --path kb/bundle api/health-check.md
```

## Actual

The file on disk:

```markdown
---
type: API Endpoint
title: Health Check
description: ''
tags: []
---
```

`show` output:

```markdown
---
type: API Endpoint
title: Health Check
description: ''
tags: []
---
trust: unverified
```

For a linted file, `show` also undoes the lint formatting. The file on disk has

```yaml
generated: {by: okf-enforcer/0.6, at: 2026-11-06T08:49:21Z}
links: [api/health-check.md]
```

but `show` prints

```yaml
generated:
  by: okf-enforcer/0.6
  at: '2026-11-06T08:49:21+00:00'
links:
- api/health-check.md
```

## Expected

`show` prints the frontmatter and body exactly as stored. If trust status is meant to be displayed, it should be clearly separated from the document, for example as a labelled header, a stderr line, or a `--trust` option, rather than inserted where it looks like body content.

## Impact

Users can't tell what is actually in the file. I first assumed a tool had written a stray `trust:` line into my documents, and later that `lint` had deleted it, when neither happened.

## Environment

- okf-schema 0.17.0
- macOS (Darwin 24.6.0)

