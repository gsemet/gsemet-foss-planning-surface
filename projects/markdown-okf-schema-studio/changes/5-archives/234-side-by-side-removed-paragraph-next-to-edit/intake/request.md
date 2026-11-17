# 234-side-by-side-removed-paragraph-next-to-edit

Priority: P1 (stack #275 blocker). Owner GATE approved on 2026-11-01, via the CoS.

## Today

The side-by-side diff, which compares with the last commit, misreads a paragraph deleted right before an edited one:
- the untouched paragraph is shown as rewritten into the edited text;
- the edited paragraph is shown as deleted.

The behaviour is deterministic. The line diff (Myers) pairs the wrong lines, because blank lines match on both sides.
- Unit repro: /private/tmp/claude-502/sbs-debug/repro.ts
- Prototype: /private/tmp/claude-502/sbs-debug/proto.ts

The real-input test in test/integration/realWindowGaps.ts (sideBySideSteps, "empty right side") fails on heavy run
41246660286.

## After (approved)

1. src/core/mapping/lineDiff.ts, `lineHunks`: merge a pure removal or a pure addition with the neighbouring hunk when
   only blank lines separate them on both sides. Never merge across headings or any other non-blank line.
2. src/page/modules/sideBySide.ts, render: inside one hunk, keep on the left only the last-commit block most similar to
   the current block. Similarity is the shared-word ratio, using the existing word diff in src/core/mapping/wordDiff.ts.
   The other last-commit blocks become "removed" cards (empty right side), placed in source order.
3. Unit tests for both. The real-input test stays unchanged.
4. SwRS REVIEW-010 and REVIEW-009 (both proposed) gain rows for these rules.

Any other user-visible change needs a new GATE.
