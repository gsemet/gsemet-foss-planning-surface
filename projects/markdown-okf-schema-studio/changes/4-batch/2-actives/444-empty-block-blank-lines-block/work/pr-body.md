## Summary

Extra blank lines between blocks (hand edits, merges, older Studio versions) were invisible in edit mode, so a writer could not reach or remove them from Studio. In edit mode, every run of two or more blank lines between top-level blocks now shows as a small blank-lines block that the writer reaches with the arrows, clicks to type a block in its place, and removes with Delete, Backspace or its Delete block button, keeping one separator.

## Deliverables

The host finds the runs and appends one hidden list to the rendered content; the page, which has no source text, builds the blocks from that list only.

```mermaid
flowchart LR
  text[document text] --> runs[blankRuns]
  runs --> html[hidden data-okf-blank-runs element]
  html --> page[blankLines.refresh in edit mode]
  page --> block[blank-lines block]
  block -->|click, Enter| edit[previewEditOpen with replaceBlankRun]
  block -->|Delete, button| del[previewBlankRunDelete]
  del --> plan[planBlankRunRemoval]
  edit --> ins[planBlankRunInsertion]
```

```ts
// the new message of the page to the host
{ type: "previewBlankRunDelete", line, endLine }
// replaces the run when typing or pasting
replaceBlankRun?: { line: number; endLine: number }
```

## Changes

- `blankRuns` and `isCommonMarkBlank` find runs of spaces-and-tabs-only lines; a line holding a non-breaking space is a paragraph, not blank.
- The preview appends a hidden `data-okf-blank-runs` element; the page reads it only from the last child of the content, and the HTML export drops it.
- A blank-lines block is built by the page in edit mode only, skipped inside blocks and folded sections, kept across refreshes, and kept while its insertion editor is open.
- Arrows stop on it, Enter or a click opens an insertion editor in its place, Delete and Backspace on a selected one remove it, Ctrl/Cmd+V pastes in place of the run.
- The host checks the run again before every open, save, paste and removal (stale runs are refused), writes one edit (one undo step) and keeps line endings and the final line break.
- New and updated requirements, glossary terms, changelog line, unit, page, session and integration tests, and visual captures.

## Impacts

Edit mode only; reading mode and the HTML export are unchanged. Screenshots are added below once verified.

## Blast radius

Grade: 2. The change touches the shared render pipeline, the page-to-host protocol and the block selection keys; a revert is possible but the new requirements and tests go with it.

## Test plan

- [x] New or changed tests (they fail on the previous code)
- [x] Requirements: SwRS added and updated, markers in code and tests, `just requirements-update`
- [x] Changelog: one user-facing line under `## Unreleased` in `CHANGELOG.md`
- [ ] Local gates: `just preflight` (static stage on Windows)
- [ ] Review
- [ ] CI green

## Autonomous decisions

- The runs are found by the host and placed by the page through one hidden element; the page trusts only that element.
- A run next to a folded section, and runs inside lists or containers, show nothing (runs inside lists are a follow-up).
- Delete and Backspace act only on a selected blank-lines block; a block only focused takes Enter and its button.
- A blank-lines block hosting an open editor stays in place until the editor closes.
