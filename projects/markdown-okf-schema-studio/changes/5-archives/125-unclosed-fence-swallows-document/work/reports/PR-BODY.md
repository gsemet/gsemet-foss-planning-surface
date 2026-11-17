## Summary

A code fence (backticks or colons, with or without a directive name) that is opened but never
closed used to swallow the rest of the document: the preview showed nothing after it, not even
the opening line. Now the opening line is shown as a raw code block, a warning
("unclosed fence") is reported on it, and every later section renders normally. The source file
is never changed.

## Deliverables

Before: the preview stops at the heading, the later sections are gone.
After: the raw line is visible and the document continues.

| Before (cream) | After (cream) |
| --- | --- |
| ![before](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/53ac425e43b732dcdb87a7dfc6d5c171fa354f70/before-cream.png) | ![after](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/53ac425e43b732dcdb87a7dfc6d5c171fa354f70/after-cream.png) |
| ![before dark](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/53ac425e43b732dcdb87a7dfc6d5c171fa354f70/before-dark.png) | ![after dark](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/53ac425e43b732dcdb87a7dfc6d5c171fa354f70/after-dark.png) |


A new tree pass, `src/core/render/mystUnclosedFences.ts`, runs in the renderer and cuts an
unclosed fence at the next heading.

## Changes

- New pass for unclosed backtick and colon fences, including nested ones.
- Requirement and changelog updated; unit tests plus a new visual scenario with a fixture.

## Impacts

Preview rendering only. A fence with no heading after it still runs to the end of the file.
The warning is a diagnostic; it is not drawn on the raw block.

## Blast radius

1

## Test plan

- `just check` passes (unit, contracts, security, release).
- Three of four new unit tests and two new visual scenarios fail on the previous code.
- Not run: the requirements lint (installed tool too old) and a real VS Code window; screenshots
  come from a static browser capture.

## Autonomous decisions

- An unclosed fence is cut at the next heading and departs from Markdown (which runs to the end
  of the file) in the preview only.
- The source is never modified.

## Internal references

CR 125 (backlog: unclosed fence swallows document).

🤖 Generated with [Claude Code](https://claude.com/claude-code)
