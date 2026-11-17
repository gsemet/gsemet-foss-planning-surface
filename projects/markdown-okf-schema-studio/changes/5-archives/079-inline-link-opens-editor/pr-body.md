## Summary

In edit mode, clicking a link inside a paragraph (or pressing Enter or Space on it) followed the
link and also opened the paragraph editor, and hovering the link outlined the whole paragraph.
The link is now only followed; the text around it still edits the paragraph.

## Deliverable showcase

| Edit mode, on a link inside a paragraph | Before | After |
| --- | --- | --- |
| click | link followed, paragraph editor opens | link followed only |
| Enter or Space | link followed, paragraph editor opens | link followed only |
| hover | paragraph outlined | no outline |
| click on the text beside the link | paragraph editor opens | unchanged |

```ts
// pageInput.ts: the click and keydown handlers now also test the event target
if (state.editMode && event.target.closest("a")) return; // follow the link, open nothing
```

## Changes

- `src/page/features/pageInput.ts`: the click and Enter/Space handlers skip the editor when the
  event target is inside a link, in edit mode.
- `src/page/features/editMode.ts`: the edit hover outline ignores a pointer over a link.
- Tests for click, keyboard and hover in `test/page/blockReq.requirements.test.ts` (replacing three
  tests that pinned the old behaviour).
- Requirements block-editing 014 and 017 gain a row each; their Known issue lines are removed.

## Impacts

Behaviour change in edit mode only; reading mode is untouched. No visual change beyond the missing
outline on a hovered link.

## Blast radius

Grade: 1. Three small guards in page input handlers; a plain `git revert` restores the old behaviour.

## Test plan

- [x] New or changed tests (3 fail on the previous code, pass now)
- [x] Requirements: SwRS-MDOKFSTUDIO-BLOCK-014 and BLOCK-017 updated, markers in tests,
      coverage regenerated (1011 requirements, 0 errors)
- [x] Local gates: `just check` green; `npm run test:unit` 2619 pass, 0 fail
- [ ] Review
- [ ] CI green

## Internal references

CR 079 (inline-link-opens-editor).

🤖 Generated with [Claude Code](https://claude.com/claude-code)
