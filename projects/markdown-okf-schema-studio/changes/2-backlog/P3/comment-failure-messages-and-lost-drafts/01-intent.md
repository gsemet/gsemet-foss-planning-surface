# Comment threads: raw error text on a failed save, and a typed draft lost silently

Severity Low · Reproduced · Verdict Gap · Requirements: none found · Area Review comments · Side preview · QA215-09 · P3

```text
Currently: a failed save says "The comment was not saved: Error: EACCES: permission denied,
           open '<full path>'", also for Resolve and Reopen. A popover holding a typed draft closes
           silently, draft lost, when its thread vanishes (thread removed, file deleted) or Comments
           is toggled off.
Expected:  a plain message naming the action ("Could not resolve the thread: the comments file is
           read-only"), no raw error or full path; a draft is kept, or the author is told it was dropped.
```

**Why this is wrong.** The toast leaks a stack-style error and a full local path into the UI and
names the wrong action for Resolve and Reopen. Losing a typed reply without a word costs the author
their text; it stays Low because it needs an outside change or the Comments toggle while typing.

**Fix.** Map file errors to short messages per action; keep the draft in memory and offer it back, or
warn before closing. Uncheck to disagree: [x]
**Test.** No test: message wording; the draft path is covered once the fix is chosen. Uncheck to disagree: [x]

Source: "Also observed" in sheet
[QA215-06](../../../5-archives/215-qa-campaign-2026-10-31/work/03-review-comments/c4-1-comments-button-leaves-review-threads.md).
