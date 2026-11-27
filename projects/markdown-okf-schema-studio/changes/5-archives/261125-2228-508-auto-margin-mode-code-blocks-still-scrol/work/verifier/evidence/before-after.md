# Before and after

Before: base `4a47151e8d055b7f096b69b1fca2d9bf9636f863` (a detached worktree of the base, removed
afterwards). After: head `09e8acf1a1581cb3803ad5f99b31a5c650f601cf`. No image shows a user name or
a home path (each one was opened and looked at).

## Pair 1: Auto width, visual harness page, cream theme, 1100 px pane, 688 px column

| Before (4a47151) | After (09e8acf) |
| --- | --- |
| ![before, Auto](base-auto-cream-1100.png) | ![after, Auto](head-auto-cream-1100.png) |

- Before: the numbered fence breaks out to 742 px and still scrolls by 2 px (`pre` 740/742). The
  captioned block stays at 688 px and scrolls (686/742).
- After: both break out to 744 px (742/742), no scroll bar, both centred on the column (centre
  542.5 px, as the column's), wider than the text column.

## Pair 2: Margin width, same page

| Before (4a47151) | After (09e8acf) |
| --- | --- |
| ![before, Margin](base-margin-cream-1100.png) | ![after, Margin](head-margin-cream-1100.png) |

Unchanged: both blocks keep the 688 px column and scroll (686/742). The two files are byte
identical (SHA-256 `e9eb1fd9...`).

## Pair 3: a real planning-surface page in a real VS Code preview, Auto width

| Before (4a47151) | After (09e8acf) |
| --- | --- |
| ![before, VS Code](base-vscode-auto-planning-page.png) | ![after, VS Code](head-vscode-auto-planning-page.png) |

Page: a copy of the backlog page `comment-failure-messages-and-lost-drafts/01-intent.md`. VS Code
1.147.0, own user-data and extensions folders, Studio editor, pane 902 px, column 702.7 px.

- Before: the top-level text block breaks out to 785.7 px and still scrolls (`pre` 784/785).
- After: it breaks out to 787.7 px (786/786), no scroll bar, centred.

In both widened states the longest line ends flush against the block's right border (the `pre`'s
right padding is not part of `scrollWidth`; see verify.md, "Observation").

## How to reproduce

The scripts are in `work/verifier/repro/`; they were run from `work/scratch/` (`e6.js` finds the
planning page relative to that folder).

1. Pairs 1 and 2: in the checkout (head, then base), after `npm run compile`:
   `node --import ./scripts/register-myst-patches.mjs <scratch>/probe.js <checkout> head|base <out folder>`
2. Pair 3: after `npm run compile` and `npm run bundle` in both checkouts:
   `node <scratch>/e6.js <head worktree> <checkout> head|base <out folder> <free port>`

Every pair the specification names (Evidence 5 and 6) was captured.
