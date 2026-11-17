# Intent: Studio in VS Code diff views

Status: **parked, waiting for the public VS Code API** (2026-10-29). Priority P2.

## Problem

When VS Code opens a diff of a Markdown file (Source Control, a chat or agent edit, a link to a
diff, "Open Changes"), the editor picker offers "Text Diff Editor" and the built-in "Markdown
Editor". The built-in editor renders the file with a change bar on the left of each changed block.
Studio is not offered there, or opens as two unrelated panels, so the user loses Studio's rendering
while reviewing a change.

## Intent (user decision)

Reuse Studio's existing diff mode, with two changes. The diff mode is the incoming-changes marks
(`preview.showIncomingChanges` and the Diff toolbar toggle), implemented in
`src/session/features/incomingChanges.ts` and styled in `src/core/preview/styles/commentStyles.ts`.

- The baseline is the **original side of the VS Code diff** instead of the file at Git HEAD.
- The left bar is **blue** instead of green, so a diff-view mark is not mistaken for a "changed since
  last commit" mark.

The panel shows the modified side with these blue bars, like the built-in Markdown editor in a
diff.

## Platform facts (checked against VS Code main, 1.144)

- The proposed API `customEditorDiffs` (`src/vscode-dts/vscode.proposed.customEditorDiffs.d.ts`)
  has two methods:
  - `resolveCustomTextEditorInlineDiff(documents {original, modified}, webviewPanel, token)` gives
    one webview both documents.
  - `resolveCustomTextEditorSideBySideDiff` gives two panels.
- The built-in `markdown-language-features` extension enables it in `enabledApiProposals`.
- A proposed API cannot ship on the Marketplace: `vsce` refuses to publish, and stable VS Code
  blocks it for extensions that are not on its allow list. Inline mode becomes possible for Studio
  only once the API is finalized.
- Without the API, VS Code falls back to `createDiffEditorInput` in `customEditors.ts`. It opens a
  `DiffEditorInput` of two plain `CustomEditorInput`s, the original on the left and the modified on
  the right. Each is resolved by `resolveCustomTextEditor`, so neither panel knows it belongs to a
  diff.
- Diff-only defaults come from `workbench.diffEditorAssociations` ("Set Default (Diff Only)").

## Open questions (for the grill)

1. Today, with the fallback: can the modified panel detect that it is the right side of a diff and
   find the original URI, through the tab API (`TabInputTextDiff` or the custom diff tab input)? If
   so, it can apply the blue marks. Should the original panel stay plain and read-only?
2. Later, once the API is finalized: implement `resolveCustomTextEditorInlineDiff`, drop the
   fallback handling, and bump `engines.vscode`.
3. The original side can use other schemes (`git:`, chat editing snapshots, `untitled:`). Read it
   through `vscode.workspace.openTextDocument`, never the file system.
4. Why was Studio missing from the diff picker in the user's screenshot? Two possible causes: the
   window was the Agents window, where Studio is disabled until it declares support, or a scheme
   filter excluded it.
5. Does the Diff toggle switch between the diff-view baseline and HEAD, or only show or hide the
   marks?
6. How does this relate to the parked P3 item `147-rich-diff-side-by-side` (draft #155)? Reuse it,
   or supersede it.

## Decision (2026-10-29): wait for the public API

Asked to implement, then stopped by the user: "arrête et note-le dans le CR pour que je puisse
attendre l'API publique".

- Wait until `customEditorDiffs` is finalized in `vscode.d.ts` (stable, publishable). Check each
  VS Code release notes and `src/vscode-dts/vscode.d.ts` for `resolveCustomTextEditorInlineDiff`.
- Then implement `resolveCustomTextEditorInlineDiff` only: **one Studio panel** showing the modified
  side, existing diff mode with baseline = `documents.original`, **blue** left bar. No side-by-side
  method. Bump `engines.vscode` to the release that finalizes the API.
- Rejected meanwhile:
  - heuristic pairing of the two fallback panels: fragile;
  - a dedicated "Open Changes in Studio" command: needs an extra click;
  - a dev-only build on the proposed API: not publishable.
- Why the fallback cannot work: VS Code exposes a diff made of two custom editor panels as
  `TabInputUnknown` (`mainThreadEditorTabs.ts`, `DiffEditorInput` with `CustomEditorInput` sides),
  so a panel cannot know it is part of a diff nor find the original URI.
- Answered: Q1 (no, see above), Q2 (yes, inline only), "hide" layout (single panel).
