## Summary

In a real VS Code window the preview stopped answering the extension: opening a block editor stayed
on "Loading Markdown source..." and the palette never appeared. The page's sender check (added with
the recent page-hardening change) accepted window messages only from the parent frame, the page
itself or an event without a sender. VS Code posts from another frame of the webview host, which has
the page's own origin, so every host message was dropped.

## Deliverables

```ts
// before: parent | self | no sender
// after:  parent | self | no sender | same origin as the page, except window.opener
if (source === window) return origin === own || origin === "null" || origin === undefined;
return source !== window.opener && own !== undefined && own !== "null" && origin === own;
```

## Changes

- `src/page/hostTransport.ts`: `isTrustedMessageSender` also trusts a sender with the page's own
  origin that is not the opener; foreign origins and the opener stay refused.
- Unit test of the sender check updated (host frame accepted, same-origin opener and foreign
  windows dropped).
- SwRS TRUST-059 states the real behaviour; update log entry.

## Impacts

Editing and all host answers work again in real VS Code. No visual change. Security-relevant: the
origin check follows the earlier hardening and is loosened only to the webview's own origin.

## Blast radius

Grade: 2 (shared message path of the page; revert is possible, but would break the real window again).

## Test plan

- [x] New or changed tests (the sender test fails on the previous code)
- [x] Requirements: SwRS-MDOKFSTUDIO-TRUST-059 updated, `okfreq` validate/lint/update-coverage clean
- [x] Local gates: `just check`; `npm run test:unit` 2622 tests (one unrelated unit test failed once
      and passed on re-run)
- [x] Real VS Code `--reload-only` suite: 9/9 failing before the fix, 20/20 passing with it
- [ ] The slash-menu step of the real-input suite was not re-checked (the 20-round stress run did
      not finish)
- [ ] Review
- [ ] CI green

## Internal references

CR 085; origin check introduced by e757ef0.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
