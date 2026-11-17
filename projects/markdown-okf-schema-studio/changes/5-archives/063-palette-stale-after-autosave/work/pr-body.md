## Summary

After the block editor saved anything (autosave after typing, or a palette button), the Reference,
Citation, Document link and Image buttons and the figure form's Browse answered "The preview is
out of date. Try again once it has refreshed." until the editor was closed. The advice could not
come true, because the preview only refreshes when the editor closes. These buttons now keep
working while the editor is open.

## Deliverable showcase

```text
type text in a paragraph -> autosave (document moves to revision 4, preview still shows render 3)
press Reference
  before: "The preview is out of date. Try again once it has refreshed."
  after:  the list of labels opens
```

The host accepts the request when a block editor is open on exactly the render the request names
(same document, same revision, still the shown render). With no editor open, or an editor open on
another render, the out-of-date answer is unchanged.

## Changes

- `src/session/sessionDocuments.ts`: new `currentPaletteDocument`, which wraps
  `currentPreviewDocument` and also accepts the document revision produced by the open editor's
  own saves.
- `src/session/features/hostRequests.ts`: the label, citation, document picker and image picker
  requests use it.
- Requirements: the Known issue is removed from the page-message gate requirement and from the
  Image, Reference, Document link and figure requirements; the gate requirement states the new
  accepted case.

## Impacts

No visual change. Pasting an image or rich text was already unaffected.

## Blast radius

Grade: 1. Four request handlers use a more permissive revision check, only while a block editor is
open; a plain `git revert` restores the previous behaviour.

## Test plan

- [x] New or changed tests (they fail on the previous code): one test in
      `test/session/paletteReq.requirements.test.ts` (14 pass; it failed before the change)
- [x] Requirements: SwRS updated, markers in code and tests, coverage regenerated
- [x] Local gates: `okfreq validate --prose --check-links` (1010 requirements, 0 errors), `lint
      --check`, `update-coverage --check`, `just check` all green. No real-window run: verified by
      code reading and the unit test.
- [ ] Review
- [ ] CI green

## Internal references

- CR 063 (palette-stale-after-autosave). The unanswered older-render request is out of scope.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

🤖 Generated with [Claude Code](https://claude.com/claude-code)
