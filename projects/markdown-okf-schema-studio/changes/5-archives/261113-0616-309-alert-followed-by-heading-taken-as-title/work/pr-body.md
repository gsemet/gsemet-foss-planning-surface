## Summary

A GitHub alert whose first line is a heading or a bold line lost its title in the preview:
`> [!NOTE]`, `> # h`, `> b` showed an admonition titled "h" with no heading in the body, while
GitHub shows the title "Note", then a real heading "h", then "b". The alert now behaves as on
GitHub.

## Deliverables

| Input | Before | After |
| --- | --- | --- |
| `> [!NOTE]`, `> # h`, `> b` | title "h", no heading | title "Note", heading `h`, paragraph `b` |
| `> [!NOTE]`, `> **Bold first**` | title "Bold first" | title "Note", bold paragraph in the body |
| `> [!WARNING] Read this`, `> ## h` | title "Read this" | unchanged, `h` stays a heading in the body |
| `:::{note}`, `# h` (MyST) | title "h" | unchanged |

## Changes

- `renderAdmonition` no longer infers a title from the first body line when the admonition comes
  from a GitHub alert (`> [!NOTE]` or the legacy `> **Note**`); the existing normalization pass
  adds the default title of the kind.
- MyST admonitions and Quarto callouts keep the leading-heading or bold-line title shortcut.
- New tests, including a comparison with committed HTML captured from GitHub's own renderer
  (no network call in tests).
- Requirements: new boundary scenario in the GitHub alerts requirement, boundary line in the MyST
  untitled-admonition requirement, changelog entry.

## Impacts

Rendered HTML for `> [!NOTE]`, `> # h`, `> b`:

- Before: `<p class="admonition-title">h</p><p data-line="3">b</p>` (the heading is swallowed into the title).
- After: `<p class="admonition-title">Note</p><h1 data-line="2" data-end-line="2">h</h1><p data-line="3">b</p>`.

The MyST `:::{note}` with a leading `# h` renders identically before and after (title "h"). No screenshot: the change is in the markup only.

No layout change beyond the alert content: only alerts starting with a heading or a bold line
change, and they now match GitHub. No visual fixture contains such an alert.

## Blast radius

Grade: 1. One condition in one function, limited to alerts; `git revert` restores the previous
behaviour.

## Test plan

- [x] New or changed tests (they fail on the previous code: 6 of 8 new tests fail without the fix; the other two keep today's behaviour by design)
- [x] Requirements: GFM-009 and MYST-001 updated, markers in code and tests, `just requirements-update`
- [x] Local gates: `just preflight` passed; unit suite 3887 pass, 0 fail
- [x] Review
- [x] CI green (static, Windows, visual; the real-window jobs run with the stack's heavy run)

## Autonomous decisions

- The spec's row "`[TOC]` lists Top and not Inside" does not hold: `[TOC]` lists headings inside
  any admonition, MyST ones included. The test asserts that the heading stays inside the
  `.admonition` aside (which the TOC column and sticky band exclude) instead.

## Internal references

CR-309 alert-followed-by-heading-taken-as-title.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
