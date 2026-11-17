## Summary

A `{doc}` or `{download}` role written without a label rendered a link with no text, so the
reference disappeared from the preview. It now shows the written target as the link text.

## Deliverables

| Source | Before | After |
|--------|--------|-------|
| ``{doc}`other/page` `` | empty link | link text `other/page` |
| ``{download}`schema/m.json` `` | empty link | link text `m.json` |
| ``{doc}`Label <other/page>` `` | `Label` | `Label` (unchanged) |

## Changes

- New tree pass `labelLinkRoles` in `src/core/render/mystBlockTransforms.ts`, run from
  `mystRenderer.ts`: a label-less link role gets its target (file name for downloads) as text.
- The render test covers both roles with and without a label.
- Out of scope: checking that targets exist, and `{numref}` (stays an inert placeholder).

## Impacts

No visual change except that previously invisible links are now visible.

## Blast radius

The pass only touches `doc` and `download` roles that have no text; a `git revert` restores the
previous behaviour.

Grade: 1

## Test plan

- [x] New or changed tests (they fail on the previous code): the doc/download render test now
      expects text for label-less roles. Its intent for the label-less case changed on purpose:
      it asserted the empty link, which was the documented bug.
- [x] Requirements: the myst "inline roles" SwRS updated (scenario, Known issue line removed),
      markers kept, requirements log entry added, `okfreq` validate, lint and coverage clean
- [x] Local gates: `just check` (2639 unit tests, 46 and 2 contract and security tests pass)
- [ ] Review
- [ ] CI green

## Internal references

- CR 087 (doc-download-empty-link); SwRS-MDOKFSTUDIO-MYST-017 (formerly MYST-095)

🤖 Generated with [Claude Code](https://claude.com/claude-code)
