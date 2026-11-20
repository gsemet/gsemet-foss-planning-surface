## Summary

Every change request's title started with "Change Specification: ", copied as written from the
specification's heading. It took room on the board's Subject column and said nothing. The CLI now
records the plain subject when a request joins a batch, and every place that shows a title strips
the lead too, so records written before this change also show plain.

## Deliverables

One shared function replaces the board's private, case-sensitive copy:

```python
LEAD = re.compile(r"^﻿?[#\s]*(?:change\s+specification\s*:\s*)?", re.I)

def subject(title: str) -> str: ...
```

| Title as written | Shown |
| --- | --- |
| `Change Specification: Fix it` | `Fix it` |
| `change specification : Fix it` | `Fix it` |
| `# Change Specification: Fix it` | `Fix it` |
| `Fix the Change Specification: lead` | unchanged |

Choices: the root is fixed (the recorded title, the branch name and the closed record are plain);
old records are shown plain but not rewritten; the board strips on the server and in the page (**UNVERIFIED:** the page's own stripping has had no hand check on a running board yet).

## Blast radius

Grade: **1**. Titles are display and naming only; a plain `git revert` restores the previous
behaviour. A new branch name no longer carries the `change-specification-` prefix; existing
branches are untouched.

## Autonomous decisions

- `board/crs.py` keeps its `subject(shown_title(...))` call, now importing from the shared module:
  harmless and allowed by the specification.

## Known gaps

- The page's JavaScript stripping (`title()` and the views that call it) is not covered by a test and was not rendered in a browser; its function was run under node on the lead, case, BOM and `#` cases, and the board's `/state` was checked for an old record.
- **UNVERIFIED:** no screenshot of the pane from a real session (the pane's title values change).

<details>
<summary>Details</summary>

## Changes

- `core/files.py`: `subject()`, case-insensitive; `board/backlog.py` imports it.
- `lifecycle/stages.py`: `prepared_cr` records `subject(markdown_title(text))`, else the folder name.
- `status/views.py`: `shown_title` and `_title` return the plain subject (STATUS files, pane, prompts).
- `board/prs.py`, `board/state.py`: server rows strip the lead.
- **UNVERIFIED:** `board/web/js/core/format.js` `title()`: case-insensitive, optional BOM and `#`; the PRs, home,
  batch card and overview views call it.

## Human decisions

- Fix at the root and keep the board's strip as a guard for old records.
- Records already written are not rewritten.
- The specification heading itself keeps its `Change Specification:` lead.

## Impacts

The Subject column and every title view lose the lead. No layout or style change.

## Test plan

- [ ] New or changed tests (title cases, join test, board rows)
- [ ] Local gates at `<sha7>`: `just check`
- [ ] Evidence: before at `<sha7>`, after at `<sha7>`
- [ ] Review: approved at `<sha7>`
- [ ] Verified at `<sha7>`
- [ ] CI green at `<sha7>`

## Internal references

- CR-395 board-subject-without-change-specification

</details>
