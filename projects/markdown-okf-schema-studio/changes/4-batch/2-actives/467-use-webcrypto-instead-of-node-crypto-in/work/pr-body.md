## Summary

The comment store and the CSP nonce imported `node:crypto`, which blocks a browser build of the core. They now use WebCrypto (`globalThis.crypto`), available in Node 24 and in browsers. Part of #413.

## Deliverables

None (internal refactor).

## Changes

- `src/core/security/csp.ts`: the nonce is 18 bytes from `getRandomValues`, base64url-encoded with `btoa` (still 24 characters, random per page).
- `src/core/comments/commentStore.ts`: comment ids and the temporary-file suffix use `getRandomValues` (ids keep the `t_`/`c_` + 8 hex format).
- `hashText` is called synchronously, and `subtle.digest` is async. To keep the callers and the hash values unchanged, a small pure synchronous SHA-256 lives in `src/core/comments/sha256.ts`. A unit test compares it with `node:crypto` on empty, ASCII, multibyte and long inputs and on every length around the block boundaries, so stored comments still match.
- `.dependency-cruiser.cjs`: both files leave `NODE_DEBT`; `just check-boundaries` passes.

## Impacts

No visual change; no behaviour change.

## Blast radius

Grade: 1. Local to two core files; a plain `git revert` restores the previous code.

## Test plan

- [ ] New or changed tests (they fail on the previous code): SHA-256 equivalence test added; the existing nonce and comment tests pass unchanged
- [ ] Requirements: No behaviour change (`just requirements-update` run; test added to REVIEW-054 coverage)
- [ ] Changelog: No user-facing change
- [ ] Local gates: `just check` passed
- [ ] Review
- [ ] CI green
