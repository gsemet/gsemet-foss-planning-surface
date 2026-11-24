Short name: `searched-line`

# Answers

1. searched-line-Q1 (2026-11-24): **Approach.** A. Proof first, in a real window: find what VS Code hands Studio under the `*.md` association (a `#L<n>` fragment, the search state, Quick Open's line); with a reliable signal Studio opens at the line; with none, fall back to an explicit gesture (the jump opens the text at the line, and a button or keybinding "Open in Studio at This Line" opens Studio there). No automatic replacement of a text tab.
2. searched-line-Q2 (2026-11-24): **Navigation inside Studio.** A. In scope: a link, Back or Next followed inside Studio opens the target at its line or anchor, and Back returns to the previous position.
3. searched-line-Q3 (2026-11-24): **The side preview's line marker under the association.** A. In scope, following Q1: with a signal the side preview marks the line; without one the limitation stays documented.
4. searched-line-Q4 (2026-11-24): **Real-window proofs.** A. Every common entry: a search result, Quick Open `file.md:42`, a link from another file, the Problems panel, Go to Symbol, Back and Next; each with and without the association, and with "Reopen Editor With > Text Editor" to prove the text is never replaced.
