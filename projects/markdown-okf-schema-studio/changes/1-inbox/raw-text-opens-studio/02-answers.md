Short name: `raw-text`

Grilled with the owner on 2026-11-23 (bug day, batch-09).

1. raw-text-Q1 (gesture): **"Open With... > Text Editor"** (or another editor) on a Markdown file;
   Studio takes its place at once.
2. raw-text-Q2 (version): **the published 1.12.0**.
3. raw-text-Q3 (expected): **always the text.** An explicit request for the raw text (Open as Text,
   Open With / Reopen Editor With > Text Editor) opens the text and is never replaced by Studio, even
   with a line.
4. raw-text-Q4 (design): **the native association.** "Every Markdown file in Studio" goes back
   to VS Code's `workbench.editorAssociations`, where Open With > Text Editor works natively.
5. raw-text-Q5 (jumps under the native association): **open at the line** (Studio finds the
   line by another means, proved in a real window, else opens at the top and says so). The owner then
   split this out: it is the P1 CR `studio-at-searched-line`, not this one.
6. raw-text-Q6 (delivery): **two CRs.** This one does the revert, at once, and is released
   (1.12.1); a second CR, P1, finds a satisfying design for opening Studio at a searched line ("une
   feature intéressante mais moins importante").
7. raw-text-Q7 (scope): **remove the whole watcher.** No text tab is ever replaced by Studio:
   neither the jump to a line nor every `.md` file. Both `open.searchResultsInStudio` and
   `open.markdownFilesInStudio` go; opening goes back to the native association as in 1.11. The side
   preview's line marker on a jump (dfc07437) and the "Open as Text" command stay.
8. raw-text-Q8 (migration): **put the association back.** On the first activation of 1.12.1, a user
   whose `open.markdownFilesInStudio` is on gets the `*.md` → Studio entry back in
   `workbench.editorAssociations`, and the setting is removed, without a question.
9. raw-text-Q9 (release path): **everything in 1.12.1.** The batch's release waits for CR-475 and
   CR-476 and ships the three CRs together, later today; this CR joins batch-09's stack, released
   with them. The release CR is `release-1-12-1`.
10. raw-text-Q10 (spec open question 1): **strict removal.** A link, Back or Next followed inside a
    Studio tab opens the target in Studio at the top, without the line, as in 1.10, until
    `studio-at-searched-line`.
11. raw-text-Q11 (spec open question 2): **keep the feature introductions mechanism** and its
    command "Show Feature Introductions Again" (and SwRS LIFE-176), for future introductions, even if
    it shows nothing today.
12. Chief of Staff, routine (spec open questions 3-5): the reverse migration's edges take the spec's
    proposals (another editor's `*.md` entry is left and the setting still removed; leftover
    `searchResultsInStudio` or an explicit false are removed; user on + workspace off is accepted and
    said in the notes; removing an undeclared key is proved in a real window, fallback: keep both
    keys declared for one version with a `deprecationMessage`). The texts say "since 1.11.0" (fact
    from git). The 1.12.1 notes file belongs to the release CR; this PR adds the CHANGELOG line only.
