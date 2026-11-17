# The Comments button hides the chips but leaves review threads highlighted and clickable

Severity Medium · Reproduced · Verdict Gap · Requirements: none found (SwRS-MDOKFSTUDIO-REVIEW-152 covers chips only) · Area Review comments · Side preview · c4-1 · Replay `scenarios/c4-1-comments-button-leaves-review-threads.json`

## Currently / Expected

| Currently | Expected |
| --- | --- |
| ![currently](../evidence/c4-1-currently.jpg) | No image: the expected state is the absence of the highlight. |
| The button reads "Show comments" (comments hidden), yet the quoted text of a review thread keeps its yellow highlight, and a click on it opens the thread popover. | With comments hidden, the thread highlights and badges are plain text again and do not open a popover (source: the button's label, and the gray and inline thread chips already vanish). |

## Why this is wrong

An author who presses "Hide comments" to read or screenshot the page cleanly still sees every
review-thread highlight and badge, and can open and edit threads while the button says comments
are hidden. The stylesheet hides only `.okf-comment` chips; `mark[data-okf-comment-thread]` and
the orphan badges are untouched. The page contradicts its own button label.

## Steps to reproduce

1. Fixture `docs/VISION.md` with a `docs/VISION.comments.json` holding three threads.
2. Open the preview to the side, expand the view controls, press the Comments button (aria-pressed false).
3. Observe the highlights; click one: the popover opens.

## Impact

Hide comments does not hide review comments; the toggle is unreliable for clean reading.

## Suggested direction

Extend the `html[data-sphinx-preview-comments="off"]` rules in `src/core/preview/styles/commentStyles.ts`
to the thread marks and badges, and close an open popover (it already closes). Uncheck to disagree: [x]

## Test to add

Real-input E2E: press Comments off, assert thread marks have no background and a click opens no popover. The replay scenario already checks it. Uncheck to disagree: [x]

## Requirement to write or change

Amend SwRS-MDOKFSTUDIO-REVIEW-152: the Comments button also hides review thread highlights and badges. Uncheck to disagree: [x]

## Done when

- [ ] With comments hidden no review thread highlight or badge shows and none opens a popover.
- [ ] The replay scenario passes.

## Also observed (Low, not filed)

- Failed save messages say "The comment was not saved: Error: EACCES: permission denied, open '<full path>'" even for Resolve/Reopen, and the raw error and path leak into the toast.
- A popover with a typed draft closes silently, draft lost, when the thread vanishes externally (thread removed, file deleted) or when Comments is toggled off.
- Held up: unreadable file, file dirty in an editor, rapid resolve/reply, external append, invalid JSON: no reply posted, draft kept, toast explains, errors 0.
