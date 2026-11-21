## Summary

In edit mode, a list followed by blank lines could not be copied, cut, or pasted after: the host refused each request with "The preview is out of date. Refresh it and try again." because the renderer maps a list to the blank lines after it. Copy and cut now drop the blank lines at the end of the selected range, and paste accepts the blank line that ends a list.

## Deliverables

For `Para`, a blank line, `- a`, `- b`, two blank lines, `Next`:

| Action | Before | After |
| --- | --- | --- |
| Copy the list | Refused | Clipboard holds `- a\n- b`, document unchanged |
| Cut the list | Refused | Same clipboard; document is `Para`, blank line, `Next` (same as Delete block) |
| Paste `X` after the list | Refused | `Para`, blank, `- a`, `- b`, blank, `X`, blank, `Next`: one blank line on each side, none gained |

- Only real blank lines (spaces and tabs only) are dropped. A line holding only a no-break space is a paragraph in CommonMark, so it is still refused rather than silently left out.
- A blank line with no block above it, or right under the frontmatter, is still refused as an anchor for a paste.

## Blast radius

Grade: 2. Copy, cut, paste and file drop share these host paths, so every block selection is affected; the change only turns former refusals into accepted requests and leaves the other paths untouched. A plain `git revert` restores the previous behaviour.

## Autonomous decisions

- File drop and paste share the same planner, so a drop on a blank line under a block is now accepted by design, as any paste there. The existing test of that refusal moved to a line that is still refused (past the end), and was renamed.
- Two capture entries for the new scenario blocks are registered in `test/shared/captureRegistry.ts` and `test/site/captureRegistry.test.ts` (counts 128, 113 and 88), as every new capture requires.

## Known gaps

- The real VS Code scenario for the new steps runs only in the heavy CI run, not on the pull request.

<details><summary>Details</summary>

## Changes

- `src/core/edits/sourceEdits.ts`: new `withoutTrailingCommonMarkBlankLines`, used by `planBlocksCopyCut` before the copied text, the include check and the cut are planned.
- `src/core/mapping/blockRange.ts`: `planPaste` accepts a CommonMark-blank anchor under a body line and moves it up to the first blank line under that block.
- Requirements: the copy, cut, paste and refused-ranges requirements are updated, with a dated entry in the tiers log.
- `CHANGELOG.md`: one line under Unreleased.

## Human decisions

- A paste anchored on the blank line that ends a list is accepted, and the new block reuses the blank lines already there.
- Only real blank lines (spaces and tabs only) are dropped from a copy or cut range; a line with only a no-break space stays refused, so nothing is left out without the writer knowing.
- The paste rule is not list-specific: any blank anchor under a body line is accepted, which covers every block the renderer maps to its blank separator.

## Impacts

Edit-mode copy, cut and paste on a list followed by blank lines now work. No visual change besides the two new capture entries.

## Test plan

- [x] New or changed tests (they fail on the previous code): unit tests for copy and cut (LF, CR LF, lone CR), unit tests for paste, and two new real-input blocks in the block-selection scenario. One existing assertion changes on purpose: pasting after a blank line under a block used to be refused and now equals pasting after the block's last line.
- [x] Requirements: SwRS updated, markers in code and tests, `just requirements-update`
- [x] Changelog: one user-facing line under `## Unreleased`
- [x] Local gates: `just check`, `just requirements-lint`, `just requirements-update` (no diff left), `just preflight` (static stage on Windows), all passing at 15a0ef0
- [x] Review: approved at 15a0ef0
- [x] CI green: PR checks pass at 15a0ef0; the heavy run (real VS Code integration, stress, visual) also passes at 15a0ef0

## Internal references

- CR-447, batch-07
</details>
