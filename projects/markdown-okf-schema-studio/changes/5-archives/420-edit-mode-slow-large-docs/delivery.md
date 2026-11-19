# Delivery

- PR: https://github.com/gsemet/markdown-okf-schema-studio/pull/421, merged by the owner on
  2026-11-19T12:00:30Z, merge commit 1d5db15b (one commit). Closes #420.
- What landed: the row handle placement, the wide-table flags and the caret reveal batch their
  layout reads; the width-mode observer skips the re-measure when a block that cannot break out is
  edited. Three regression tests, each failing on the previous code (table box reads 45 → 6 for
  14 handles). SwRS-LAYOUT-023, PALETTE-021 and TABLE-002: verification lines, no normative change.
- Local gates: `just check` green; `just preflight` green except the real-window integration
  stage (screen locked), left to the heavy CI run.
- Follow-ups not filed: the anchor read after the editor is inserted, the sticky palette and
  textarea resize ordering, lazy insert bars, `content-visibility`, the `:has()` rules, caching the
  top-level block list, debouncing the layout stabilisation.
