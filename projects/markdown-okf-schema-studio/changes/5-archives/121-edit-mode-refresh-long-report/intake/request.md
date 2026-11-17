# 121 — Edit mode on a long report: no refresh glitch

Type: fix · Priority: P1 · From backlog: `02-backlog/P1/edit-mode-refresh-long-report`

## Intent (user)

# Refresh bug in edit mode on a long Markdown report

User report (2026-10-26): opening `.agents/changes/rapport-cout-orchestration.md` in the Studio
shows a "refresh bug". It appears **in edit mode only**; the plain preview of the same file is fine.
Seen on the build installed from `main` at eb812ad (version 0.3.1, after the 19-PR stack merge).
Not reproduced yet: the exact symptom (flicker, scroll jump, stale content, refresh loop) still has
to be observed.

Priority P1 set by the user (2026-10-26).

## Repro to run first

1. Use `repro-document.md` in this folder: a copy of the report as the user opened it, about 300
   lines of French text with many GFM tables, bold text, lists, inline code and one fenced code
   block, no frontmatter. Work on a copy in a QA workspace (`setup-workspace.sh` from the
   exploratory QA skill), never on the original.
2. Open it with the Studio (Open With, and preview beside the text editor), then switch to **edit
   mode** (Edit toolbar button).
3. Watch for a few seconds without input, then scroll, click a block to open its editor, type one
   character, and press Done. Also rewrite the file on disk while it is open in edit mode: the
   original was rewritten by a tool while it was open.
4. Measure with the QA probes (`flicker-probe.mjs`, `filmstrip.mjs`, `observe.mjs`): renders and
   DOM replacements per second, scroll position before and after, and whether the open block
   editor survives.
5. If it reproduces, cut the document down to the smallest version that still shows it (tables,
   their number or width, length, the code fence).

## Leads, not verified

- Things that differ in edit mode: the edit affordances on every block, the "+" insert bars, the
  table row handles added last night (#89, outside the table and shifting full-width tables), and
  the block editor open and save flow (#82: open the clicked block after the save).
- The file is under `.agents/changes/`, which is git-ignored: check the change bar and "diff since
  last commit" path for an untracked file.

## Expected

Edit mode renders once and stays stable: no flicker, no scroll jump, no lost block editor, and an
external rewrite refreshes the page once.

## Done when

- The symptom is reproduced in a real window, with the cause at `file:line`.
- The bug is fixed, with a real-window test.
- The SwRS is updated in the same change.
- Heavy CI is green.

## Autonomous decisions

- Decided by the main session on 2026-10-26 under the user's instruction "pas de questions, full autonome". List these in the PR body under "Autonomous decisions".
- Round 1 is a reproduction with the attached repro-document.md in edit mode (real window test or scripted e2e). Leads: the row handles, open-after-save, the change bar of a git-ignored file.
- If round 1 cannot reproduce, the driver sets status: blocked with the findings and the question for the user instead of guessing a fix.
- Placed on top of the stack because the cause is unknown.
