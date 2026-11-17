# Behaviour note: radio choice lists, focus and write guards

Round 0 reproduced all four defects with headless tests that fail on origin/main 0b4ede78
(test/core/render/radioGroups.test.ts, test/page/runtimeRadioGroups.test.ts, test/session/radioChoice.test.ts).

## 1. Tab entry
- Today: the sanitizer gives every mapped block tabindex="0" (html-sanitizer.ts:502-504), so Tab from the label
  stops on ul, li, p, then the radio (4th stop).
- After: one Tab from the label lands on the selected option (else the first). The ul/ol, li and option p get
  tabindex="-1" (still focusable by click/script, out of the Tab order).
- Cost: Tab no longer stops on the list block itself. In edit mode the list stays reachable by the Up/Down block
  selection, then Enter opens its editor. In read mode, revealing the list's source by keyboard needs block selection.

## 2. Focus after a choice
- Today: the content patch replaces the option node; focus falls to BODY (contentMorph.ts:186).
- After: once the patch is applied, focus goes back to the option with the same source line and column
  (preventScroll). Same after a click. A choice from an external rewrite: restore only if the focused option existed before.

## 3. Click with a block editor open
- Today: mousedown moves focus, the editor's blur-commit closes an unchanged editor synchronously, then the click
  guard sees no editor and writes.
- After: a capture-phase mousedown guard on options: if an editor is open, prevent the mousedown (focus stays in the
  editor, no blur-commit) and the click is refused with the existing status "Save or cancel this edit before choosing
  an option." Nothing is written; the editor stays open.

## 4. Read-only file (files.readonlyInclude)
- Today: VS Code's editor.edit resolves true on a read-only editor without changing text; the host answers saved,
  the page keeps the new choice, says nothing.
- After (proposal): the host checks the document actually changed after an apply that resolved true; if not, it
  answers an error. The page restores the source selection and shows the reason next to the clicked option (~6 s,
  and as tooltip) with the text "This file is read-only in VS Code." The same safety net covers checkbox toggles
  (same path).
- Up-front disabling like Restricted Mode is not reliably possible: no stable VS Code API exposes files.readonlyInclude
  or "Set Active Editor Readonly in Session"; matching the setting globs ourselves would miss the session toggle.
  Proposed as a follow-up only if wanted.

## Requirements (all proposed, may change)
- SwRS-MDOKFSTUDIO-GFM-039: one-tab-stop row explicit for ul/li/p; Space/Enter row gains "focus stays on the chosen
  option"; refusal table gains the mousedown case and the read-only file row.
- SwRS-MDOKFSTUDIO-BLOCK-041: checkbox/radio row notes the guard runs before the editor's blur.
- SwRS-MDOKFSTUDIO-TRUST-005: unchanged scope (preview-level read-only); the read-only file refusal lives in GFM-039/GFM-021
  (GFM-021 proposed? to be checked by the Coder; if approved, wording goes to GFM-039 only).
