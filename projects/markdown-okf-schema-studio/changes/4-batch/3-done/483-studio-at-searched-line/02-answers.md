Short name: `searched-line`

# Answers

1. searched-line-Q1 (2026-11-24): **Approach.** A. Proof first, in a real window: find what VS Code hands Studio under the `*.md` association (a `#L<n>` fragment, the search state, Quick Open's line); with a reliable signal Studio opens at the line; with none, fall back to an explicit gesture (the jump opens the text at the line, and a button or keybinding "Open in Studio at This Line" opens Studio there). No automatic replacement of a text tab.
2. searched-line-Q2 (2026-11-24): **Navigation inside Studio.** A. In scope: a link, Back or Next followed inside Studio opens the target at its line or anchor, and Back returns to the previous position.
3. searched-line-Q3 (2026-11-24): **The side preview's line marker under the association.** A. In scope, following Q1: with a signal the side preview marks the line; without one the limitation stays documented.
4. searched-line-Q4 (2026-11-24): **Real-window proofs.** A. Every common entry: a search result, Quick Open `file.md:42`, a link from another file, the Problems panel, Go to Symbol, Back and Next; each with and without the association, and with "Reopen Editor With > Text Editor" to prove the text is never replaced.
5. searched-line-Q5 (2026-11-24): **Grilled enough?** A. Specify, for the next batch (3-ready). Spec critic: yes (host behaviour and what the owner sees at opening).

6. searched-line-Q6 (2026-11-24, spec open question 1): **"Open in Studio at This Line" from a text tab.** A. The text tab stays; a Studio tab opens in the same group, at the line.
7. searched-line-Q7 (2026-11-24, spec open question 2): **Default keybinding.** A. None: the editor title menu and the palette only.
8. searched-line-Q8 (2026-11-24, spec open question 3): **Under the association, an entry with no signal.** A. Accepted: Studio opens at the top, the limitation is documented, the command is the fallback.
9. searched-line-Q9 (2026-11-24, spec open question 4): **VS Code's Go Back / Go Forward between Studio tabs.** A. Prove it too, in a real window: Go Back returns to the Studio tab left, at its position; Go Forward redoes the jump.

10. searched-line-Q10 (2026-11-24, spec critic F1): **A link to another file in a preview that does not follow the editor (TOOLBAR-059).** A. Studio tabs (the custom editor) record it; fixed previews restored by VS Code keep today's rule; TOOLBAR-059, its test (toolbarReq.requirements.test.ts:306) and the links.ts:291 comment are amended in this CR.
11. searched-line-Q11 (2026-11-24, spec critic F2): **Back or Next to a file whose Studio tab is open in another group.** A. Reveal the existing Studio tab in its own group, at the line; proved in a real window (a row in 7.3).
12. searched-line-Q12 (2026-11-24, spec critic F3): **A link reveals a Studio tab already open with its own history.** A. Only a Studio tab the link creates shares the source's history; an existing tab keeps its own and the move is appended to it.
13. searched-line-Q13 (2026-11-24, spec critic F4): **Default settings, a link in a Studio tab opens the target as text.** A. Not recorded: a Studio tab records a link to another file only when the target opens in a Studio tab; the default stays as today.
14. Chief of Staff routine (2026-11-24, spec critic F5-F6, no user question): F5 the palette clause is `resourceExtname == .md && !activeCustomEditorId`, and the title-menu placement drops "next to Open as Text" (it shows on Studio tabs only); F6 the pending line is taken whenever it is delivered, by `resolve` or to a live session, with that case in the 7.2 unit tests.

15. searched-line-Q15 (2026-11-24, spec open question after the rerun): **A link (not Back or Next) to a file whose Studio tab is open in another group.** A. Reveal that tab in its own group, at the line, the same rule as Q11: no second Studio tab.

16. Chief of Staff routine (2026-11-24, reading of Q11 and Q15): the reveal rule does not depend on the `*.md` association: with default settings too, a link from a Studio tab to a file whose Studio tab is already open reveals that tab rather than opening the text.

Destination: next batch (3-ready).
