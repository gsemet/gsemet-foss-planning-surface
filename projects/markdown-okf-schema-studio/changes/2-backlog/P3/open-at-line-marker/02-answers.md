# Answers

Short name: `open-at-line`

## Series 1, 2026-11-20

1. open-at-line-Q1: **How Studio gets the line.** A, Studio decides itself to open `.md` files: a Studio setting ("open Markdown files in Studio") replaces the VS Code `workbench.editorAssociations` entry; the text editor opens for a moment at the line, then Studio takes its place at that line, with the marker. (Context given: with the association, `resolveCustomTextEditor` receives no line; only a text editor gets it.)
2. open-at-line-Q2: **Entry points.** A, all of them, no closed list: whatever opens the text editor at a line (search, Quick Open `file.md:42`, Problems panel, terminal links, Ctrl+click, Outline...).
3. open-at-line-Q3: **File already open in Studio.** A, the same Studio tab scrolls to the new line and the marker moves; no new tab.
4. open-at-line-Q4: **Raw text asked on purpose.** A, Studio never replaces a text editor the user asked for on purpose ("Reopen Editor With > Text Editor", a Studio "open source" action): the text editor stays.

## Series 2, 2026-11-20

Retained mockup for the marker: `prototypes/01-arrow-marker/`, option A.

5. open-at-line-Q5: **The setting's default and the first-time notice.** Free answer (not A): the setting is **on by default**. The first time, a notification shows for a few seconds explaining that this behaviour can be changed in the settings. Owner's words: "allumé, la premiere fois une notification s'affiche pendant quelques secondes expliquant que cette association peut être changée dans les settings. met en place un systeme qui permet de reset ces notifications d'introduction de feature car je peux etre amener a en faire d'autres. par contre c'est qu'une fois, apres fermeture ou disparition, ca ne revient plus meme dans les prochaines sessions". So: a reusable "feature introduction" notice system (other features will use it), each notice shown once only, never again after it is closed or disappears, even in later sessions, and a way to reset these notices.
6. open-at-line-Q6: **The marker's look.** A, an arrow in the left margin at the exact height of the line, plus a light band on that line.
7. open-at-line-Q7: **When the marker goes away.** A, it stays until the user clicks in the page, starts an edit, or another line is requested; scrolling does not remove it.
8. open-at-line-Q8: **A line inside a block.** A, as precise as possible: the exact line in a paragraph or a code block, the targeted table row, a folded section or admonition is unfolded to show the line; otherwise the top of the block.

## Series 3, 2026-11-20 (not answered: the item was set aside)

Questions asked, not answered: open-at-line-Q9 (remove the user's own `workbench.editorAssociations` entry that names Studio; recommended A, Studio removes it and the notice says so), open-at-line-Q10 (how to reset the feature-introduction notices; recommended A, a palette command), open-at-line-Q11 (edit mode; recommended A, same marker, no block editor opened on its own), open-at-line-Q12 (side preview; recommended A, same marker on a jump, not on every cursor move).

Owner's clarifying question before answering: "attent tu veux dire que je peux pas avoir les deux, l'association md automatique avec studio comme maintenant ET l'ouverture a la ligne lors d'une recherche ?" Answer given: yes, both, but the automatic opening must be done by Studio itself (its own setting) instead of the VS Code association, which loses the line; the text editor may show for a short moment before Studio replaces it (to be measured by trials).

9. **Decision: set aside in P3**, 2026-11-20. Owner's words: "met la de coté en P3 avec le drawback que l'ouverture du text brute risque de tjs boucler sur studio". The drawback to keep in mind when the item is taken up again: with Studio taking over every `.md` opened in a text editor, opening the raw text on purpose risks always looping back to Studio (open-at-line-Q4 asked that a text editor opened on purpose stays, but how to tell it apart reliably is unproved). The grill resumes at open-at-line-Q9.

10. **A setting "open searches in Studio", on by default**, 2026-11-20 (given after the item was set aside). Owner's words: "il faudra un settings \"ouvrir les recherche dans studio\", on par defaut." Open at the resumption: whether this setting replaces the general "open Markdown files in Studio" setting of open-at-line-Q1/Q5 (only an opening at a line, from a search or another jump, goes to Studio, which would avoid the raw-text loop) or comes in addition to it.

## Merge of `vscode-diff-view`, 2026-11-20

11. **The diff-view item merged into this CR, P3, with a big caveat**, 2026-11-20 (recorded by
    the Griller of `vscode-diff-view`). Owner's words: "ok on laisse tomber en P3 avec un gros
    caveat, que ca implique de remplacer l'editeur de text pour les md et ca risque de poser des
    pbl. a tester en meme temps que la CR sur l'ouverture a la ligne. merge d'ailleur les 2
    demandes dans le meme CR. met aussi tous tes resultat d'analyse dans le dossier". So: the
    behaviour of Studio in VS Code's diff views (search-and-replace preview, Git diff, Source
    Control, timeline, Compare with Saved, two-file compare) is part of this CR and tested with
    it; the risk is that Studio taking over the text editor for `.md` breaks those diffs, which
    are all plain text diffs today. The diff-view questions asked and not answered (diff-view-Q1
    to Q4: keep the text diff and fix the side preview's gaps, scroll sync from a diff, "Open
    Preview to Side" from the replace preview, Studio's button on a diff; all recommended A) are
    open for the resumption. Findings: `work/diff-view-findings.md`; evidence:
    `evidence/diff-view/`; scripts: `experiments/0N-diff-view-*`.

## Series 4, 2026-11-20 night: decided by the Griller under the owner's autonomy rule

Source: the Chief of Staff relayed the owner's words of the evening: "tu es maintenant autonome. plus de question. tu grilles tout seul avec un fable et tu me livres a la fin de la nuit une stack mergeable." Each answer below is decided by the Griller under the owner's autonomy rule, not by the owner; the owner may change any of them at review. The priority (P3) is unchanged by this pass.

12. open-at-line-Q9: **The user's own association `*.md → markdown-okf-schema-studio.editor`.** Decided by the Griller under the owner's autonomy rule: A, with a migration. When Studio finds, at activation, a `workbench.editorAssociations` entry for `*.md` whose value is Studio's editor (in the user or the workspace scope), it removes that entry from that scope and turns on the Studio setting "Open Markdown files in Studio" in the same scope, so the user keeps every `.md` opening in Studio, now at the line; the introduction notice says so. An entry naming another editor is never touched. Why: it is the only way the owner keeps today's experience and gains the line (decision 1), and Studio touches only an entry that names itself.
13. **Decision 10's open point (one setting or two).** Decided by the Griller under the owner's autonomy rule: two settings. "Open search results in Studio" (on by default, decision 10): a `.md` opened in a plain text editor at a line by a jump (search, Quick Open `:line`, Problems, links, Ctrl+click, Outline...) is replaced by the Studio tab at that line, with the marker; a plain opening (no line) stays a text editor. "Open Markdown files in Studio" (off by default, on after the migration of decision 12): every `.md` opened in a plain text editor is replaced by the Studio tab, at the line when there is one. Why: the search setting alone has no raw-text loop and no diff risk, so it can be on for everyone (decision 10); the general takeover carries the drawback of decision 9, so it is on only for users who already chose Studio as their default. This reads open-at-line-Q5's "on by default" as applying to the search setting, which decision 10 named after Q5.
14. **The raw-text loop (decision 9) and the diffs (decision 11).** Decided by the Griller under the owner's autonomy rule: Studio never replaces a diff (either side of any diff editor: Git, Source Control, timeline, Compare with Saved, two-file compare, the search-and-replace preview), a text editor the user reopened as text on purpose ("Reopen Editor With > Text Editor", open-at-line-Q4), or a text editor Studio itself opened (its own reveals, e.g. double click to switch to the editor). Each of these is proved in real VS Code before the CR is ready. diff-view-Q1 (keep VS Code's text diff): A, as above.
15. open-at-line-Q10: **Resetting the feature introductions.** Decided by the Griller under the owner's autonomy rule: A, a palette command ("Markdown OKF-Schema Studio: Show Feature Introductions Again"); each introduction then shows once more.
16. open-at-line-Q11: **Edit mode.** Decided by the Griller under the owner's autonomy rule: A, the same arrow and band, placed without covering the list item handle or the block actions; no block editor opens on its own; a click on the block opens it as usual and removes the marker.
17. open-at-line-Q12 and diff-view-Q2 to Q4: **Split off** by the Griller under the owner's autonomy rule (the Chief of Staff asked for one CR that can ship tonight): the marker in the side preview on a jump (Q12) and the side preview's gaps next to a diff (scroll sync from a diff, "Open Preview to Side" from the replace preview, Studio's title button on a diff) go to new inbox items. This CR changes nothing in the side preview.
18. **Grilled enough, specify.** Decided by the Griller under the owner's autonomy rule (the Chief of Staff's relay asked to specify tonight). Spec critic: yes, on Fable (claude-fable-5-2, asked by the owner's relayed words), because it changes what the user sees on every `.md` opening, edits the user's VS Code settings (decision 12) and touches the host's editor lifecycle.
