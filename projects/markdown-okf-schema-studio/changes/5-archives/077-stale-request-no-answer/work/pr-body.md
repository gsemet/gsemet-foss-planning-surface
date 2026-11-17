## Summary

A request sent from a preview that is one render behind was dropped by the host without an answer.
The page then waited for its own timeout (6 seconds for a list, 10 minutes for a file dialog), an
arrow click stayed marked pending, and the blur commit stayed suspended. The host now always answers.

## Deliverable showcase

```text
before: page --previewBlockMove(rev 3)--> host (holds rev 4)   // dropped, page waits
after:  page --previewBlockMove(rev 3)--> host --previewBlockMoveResult ok:false,
        reason "The preview is out of date. Try again once it has refreshed."--> page
```

## Changes

- The render gate (`src/session/pageMessages.ts`) answers a stale request with its Result message
  (`ok: false` and the out-of-date reason): block move, block copy/cut/paste, thread reply/delete,
  label and citation lists, document and image pickers, image paste, HTML paste.
- A stale block-edit open and checkbox toggle are answered through the page-state stale path.
- History, view preference and palette mode messages are not requests and stay unanswered.
- One shared `STALE_REQUEST` constant replaces the repeated literal.

## Impacts

No visual change. The page clears its pending state at once. For a block-edit open only the pending
state is cleared: its reason is not visible yet, because the status line of the block editor is
attached to the frame only when the source arrives (a documented known issue).

## Blast radius

Grade: 1. Local to the host's page message gate; a plain `git revert` restores the dropped behaviour.

## Test plan

- [x] New or changed tests: stale-request test over 12 request kinds plus block open and checkbox toggle
- [x] Requirements: SwRS updated, Known issue lines removed, `okfreq` validate, lint and coverage clean
- [x] Local gates: `npm run test:unit` 2617 pass; `just check`
- [ ] Review
- [ ] CI green

## Internal references

CR 077 (stale-request-no-answer).

🤖 Generated with [Claude Code](https://claude.com/claude-code)
