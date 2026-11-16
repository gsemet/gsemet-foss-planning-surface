# Conflicts: CR-202 restacked on CR-201 (dce25c9)

`git rebase --onto dce25c92 origin/main`; one commit (756a362, now 97d5125). One conflict, in `docs/boards.md`.

## Hunk 1: section "The CR board (Claude Code)" (whole section body)

- CR-201 side (HEAD): the section rewritten into sub-sections (What it is, How to open it, How to read it, pictures, two facts, guard of a worker's writes).
- CR-202 side: the old one-paragraph section, extended with the 15 s check, the "checked 3s ago, every 15 s" header and the Refresh button.
- Choice: keep CR-201's structure and wording whole, drop the old paragraph, carry CR-202's intents into it:
  - "How to read it": header example changed from `read 0s ago` to `checked 3s ago, every 15 s`, with a clause saying it is when the pane last checked and its period.
  - Same paragraph: "refreshes every 15 seconds" replaced by "checks every 15 seconds ... reads a file again only when it changed", plus the Refresh button sentence (every view, reads files again even unchanged, looks for planning folders again, keeps page and folds, does not refresh cost or record).
  - Facts already in CR-201's "What it is" (read only, git rev-parse, Copilot, Remote Control issue, slots, open on skill load) kept once, not duplicated.

Other files (hooks/register.tsx, its test, types/index.d.ts) merged cleanly. `just check`: 58 passed, release-notes ok. Nothing pushed.
