# Image-paste test diagnostics can crash and hide the real failure

Found in review of the pasted-image fix ([PR #53](https://github.com/gsemet/markdown-okf-schema-studio/pull/53)).
The diagnostics added to the image-paste real-window test (`test/integration/realWindowGaps.ts`
around line 272) list the image folder and stat each file. If the hidden `.partial` file is
renamed or deleted between the listing and the `stat`, the diagnostics throw `ENOENT`, and that
error replaces the real assertion message.

## Expected

- Diagnostics never throw: stat with `throwIfNoEntry: false` (or catch per entry) and report a
  vanished file as "gone during listing".
- A unit test for the diagnostics helper with a file that disappears.

Test code only. Needs PR #53 merged first.
