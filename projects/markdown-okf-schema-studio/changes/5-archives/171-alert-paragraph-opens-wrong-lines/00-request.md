# 171 — Clicking a paragraph inside a GFM alert opens the block editor on the wrong lines (HOTFIX)

Type: fix · Priority: P1 · Target 1.0.0 (escalated: data-loss risk confirmed; user decision 2026-10-28, merges before #182) · Approved by
the user via the Chief of Staff, 2026-10-28 · From `origin/main` (after #184), one PR, not stacked.
Runs in the background; must not block #182 (release/1.0.0).

## User report (real VS Code, user's own window)

- File: the repository README.md (working copy with uncommitted user work — never edit it; the
  snapshot taken at CR open is `reports/README-snapshot-*.md`).
- Click on the paragraph inside the `> [!NOTE]` alert, README lines 40–41 ("> The Markdown rendering
  and editing experience of Obsidian is nice, but I hate having to work / > through a "vault" ...").
  The alert follows another blockquote/alert that ends on line 38.
- The block editor opened with "Lines 42–43": the blank line 42 and `### Edit MyST visually` (line
  43). Offset +2.
- Screenshots: `reports/user-click.png` (click), `reports/user-editor-opened.png` (editor).

Context: just before, README.md was rewritten on disk outside the preview (lines 16–41: a 3-line
`::: {card}` wrapper removed, blank lines collapsed, so the line count changed), and the user was
typing in the same file.

## Leads to reproduce, and state which one it is

1. Stale source map after an external on-disk edit that changes the line count (block line ranges
   not refreshed in the open preview).
2. Line mapping of an alert (blockquote with `[!NOTE]`) that follows another blockquote/alert.

## Data-loss check (first)

An editor opened on the wrong lines and confirmed with Done would overwrite those lines. Determine
early whether Done/autosave writes to the stale range, or whether a guard (source text check)
refuses it. If it can overwrite the wrong lines, report at once (possible 1.0.0 escalation).

## Done means

- Reproduced first with a failing test (unit or headless), then fixed.
- Regression test for the exact case: two consecutive alerts/blockquotes, click in the second; plus
  an external on-disk edit changing the line count while the preview is open, if that is the cause.
- Heavy CI green; before/after proof in the PR.
- No weakened assertion, no retry loop. SwRS / markers / log entry if behaviour changes (new
  requirements `--lifecycle proposed`).
