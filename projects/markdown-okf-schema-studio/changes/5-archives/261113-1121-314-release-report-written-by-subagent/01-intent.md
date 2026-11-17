# Intent: name the release report with a number in the release CR

## Problem

Step 7 of the release-process guideline archives a release with a `report.md` in the release CR's
folder, written by the Release driver. For v1.8.0 (batch-02), the harness refused the Release
driver's Write of `.agents/changes/3-requests/batch-02/313-release-v1-8-0/report.md` with
"Subagents should return findings as text", while `retro.md` was accepted. Subagents cannot write
some Markdown file names, but a name with a number in front works (owner's finding).

The name also clashed with chantier's own `report.md` (the Chief of Staff's progress report,
written in the same folder before the release is confirmed): v1.7.1's `report.md` held both. The
owner says the chantier side is already fixed; this CR covers only the project.

## What the owner decided (2026-11-13)

- The project's release report is named with a number in front, in the release CR's folder, next
  to `01-intent.md`, `02-answers.md` and `03-change-spec.md`: `04-report.md`. The v1.8.0 report
  already uses that name (written by the Chief of Staff from the Release driver's relayed text).
- Update the release-process guideline (step 7 and every other mention of the release
  `report.md`) and anything in the project that names the file.

## Also

- Issue #336 (closed 2026-11-10) has no "Released in" comment, while #334 and #335 point to 1.6.0:
  find its release and post the comment per the guideline's issue rule.
