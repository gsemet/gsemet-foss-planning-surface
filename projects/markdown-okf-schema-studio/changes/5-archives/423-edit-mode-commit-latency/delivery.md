# Delivery

- PR: https://github.com/gsemet/markdown-okf-schema-studio/pull/424, merged by rebase on
  2026-11-19 at the owner's request, head a0821ac5 (two commits: the fix and its changelog line).
  Refs #423; the issue stays open for the follow-ups.
- What landed: committing a block edit asks the build queue for an immediate render instead of
  waiting for the adaptive pause; the table row handles are placed in the next animation frame
  instead of during the page patch. SwRS-LIFE-039 normative change (immediate render after a
  commit), TABLE-002 verification line, requirements log entry, one new build queue test, three
  table row move tests flush the frame.
- Measured on chapter 08 in a clone of the reporter's environment: commit round trip
  1930/1134/590 ms → 543/394/391 ms.
- Gates: `just format` and `just ci-static` green locally (audit re-run through the proxy); PR CI
  green (static, static-windows, visual).
- Follow-ups not filed: a single read phase in `closeBlockEdit`, one HTML parse in the content
  patch and the properties table (~250 ms of patch left), the block editor opening time.
