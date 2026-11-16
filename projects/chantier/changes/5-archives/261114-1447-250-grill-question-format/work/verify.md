Head: 831ba06850a3672456daa45c89aad05f192bde92

All claims judged at 831ba06 (worktree HEAD, `git rev-parse HEAD` = 831ba06850a3672456daa45c89aad05f192bde92; PR 191 headRefOid the same).

1. Only the four cards changed; agents and CLI untouched. `git diff --name-only 894806a..831ba06` printed exactly chief-of-staff.md, griller.md, hosts/claude-code.md, hosts/copilot.md (under skills/chantier/references). `git diff --stat -- agents com.github.copilot src '*.py' hooks tests` printed nothing. HOLDS.
2. Decisions 1-14 in chief-of-staff.md "Asking the user: a series" (diff read in full): Who (1), reference `<short name>-Q<n>` never CR number (2), one item per call (3), independent questions (4), series size via host reference (5), no question tool "Q1 A, Q2 B" (6), record starts with reference (7), numbering across series (8), short name line at head of 02-answers.md (9), at most 4 options (10), A recommended "(recommended)" (11), one asker per item (12), "Grilled enough?" same format (13), text first every time incl. Remote Control, form is short mirror (14). HOLD.
3. No host figure in chief-of-staff.md: the only numbers are "never more than 5" (spec's own general cap) and "at most 4 options" (general rule); no "4 questions", Claude Code or Copilot figure; host reference is pointed to. HOLDS.
4. Worked example present (ready-wording, two questions, text and AskUserQuestion mirror). HOLDS.
5. "Shared understanding" points to the subsection (diff hunk @@ -249). HOLDS.
6. griller.md: one mention in "What you do" without copying the format; worktree sentence names the main checkout's 02-answers.md read, worktree copy written, short name picked if missing. HOLDS.
7. claude-code.md: diff is a single added Tools row (4 questions, 4 options, Other, Remote Control, mark: user's statements 2026-11-14, answers 5/11, trials, scrolling answer 17); `git diff ... | Select-String '^@@'` shows one hunk in the Tools table, so "Surfaces and options" is unchanged. HOLDS.
8. copilot.md: Tools row (5 questions, 4 options, name and free answer not recorded, mark and trial) and preamble exception for the 2026-11-14 statement (answer 10). HOLDS.
9. PR description (work/pr-body.md and as posted on the forge, body checked with gh): sections render, Summary/Deliverables/Changes match the diff (four files, worked example, host rows, preamble exception); Known gaps names the waived long gate, the unproved figures and Copilot's unrecorded tool name. The Verified/CI boxes are open placeholders for later steps, not claims. HOLDS.
10. Gates: no local long gate (user waiver, named in Known gaps); CI green at 831ba06 as reported by the caller. Not re-run.

VERIFIED
