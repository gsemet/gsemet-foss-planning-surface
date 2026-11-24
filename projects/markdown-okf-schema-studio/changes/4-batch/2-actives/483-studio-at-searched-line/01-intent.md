# Open Studio at a searched line, never replacing an explicit text tab

Owner, 2026-11-23 (split of raw-text-opens-studio, CR-477, answer raw-text-Q6): after the revert of the 1.12.0 opening watcher (released as 1.12.1), find a satisfying design for opening Studio at the line of a search result, a link or Quick Open `file.md:42`, including when every Markdown file opens in Studio through VS Code's native editor association (a custom editor receives no selection). Hard constraint: an explicit request for the raw text (Open as Text, Open With or Reopen Editor With > Text Editor) is never replaced by Studio. Owner: "une feature intéressante mais moins importante".

Known state after 1.12.1: with default settings a jump opens the text editor at the line; with the `*.md` association a jump opens Studio at the top, and the side preview marks no line (CR-477's known limitation, raw-text-Q13); a link, Back or Next inside Studio opens the target at the top (raw-text-Q10).
