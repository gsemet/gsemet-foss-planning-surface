# Investigation, 2026-11-20 (main 1.10.0, no fix)

## What happens
- "+" then Done with nothing typed: nothing is written (insertionText returns "" for empty text,
  src/core/mapping/insertion.ts:51-53, SwRS-MDOKFSTUDIO-BLOCK-094).
- The owner's case is most likely: open an EXISTING block, erase all its text, Done. The page
  sends "\n" (src/page/features/blockEditor.ts:382), the host writes it as a plain replacement
  (src/session/features/blockEdits.ts:320-341, planBlockTextEdit in src/core/edits/sourceEdits.ts:301).
  Result: "# Title\n\n\n\nSecond paragraph.\n", 3 blank lines.
- Same runs from: a new block starting with Enters (insertion.ts:55 keeps leading blank lines),
  an existing block with trailing Enters typed.

## Why it cannot be reached
- markdown-okf makes no token for blank lines: no DOM node, no source map entry.
- Insert points sit after a block's end line (src/page/features/insertPoints.ts:171-180).
- The host refuses an editor range starting on a blank line (SwRS-MDOKFSTUDIO-BLOCK-256).
- No Delete action on a block; only Cut (planCut, src/core/mapping/blockRange.ts:97-134,
  SwRS-MDOKFSTUDIO-BLOCK-169), which removes the block with its separator.

## Options
1. Recommended. An existing block emptied then Done is deleted with one blank separator, like
   planCut, in one undo step (final save only; autosaves keep the "\n" placeholder). Also trim
   leading blank lines of a new block and trailing blank lines of a final block edit.
2. For runs already in the file (hand edits, merges): a "Remove extra blank lines" action on the
   insert point of a block followed by a run of 2+ blank lines; collapses the run in one host edit.
   No editor on blank lines (keeps BLOCK-256).
3. Not recommended: collapse all blank-line runs on save (breaks BLOCK-025/042, noisy diffs,
   blank lines matter in code/HTML/MyST).

## Requirements
SwRS BLOCK-094, 047, 042, 053, 169, 256, 087, 109, 117; StRS BLOCK-011, 025. No SwRS covers an
existing block emptied and committed today.
