## Summary

The comment store and the CSP nonce imported `node:crypto`, which blocks a browser build of the core. They now use WebCrypto (`globalThis.crypto`), available in Node 24 and in browsers.

## Issues References

Part of #413 (first step only: it must not close the issue).

## Deliverables

Target set: the core no longer depends on Node for randomness or hashing, so it can run in a browser.

| | Before | After |
|---|---|---|
| `csp.ts` nonce | `node:crypto` `randomBytes` | `crypto.getRandomValues` + `btoa` |
| `commentStore.ts` ids, temp suffix | `node:crypto` `randomBytes` | `crypto.getRandomValues` |
| `commentStore.ts` text hash | `node:crypto` `createHash` | synchronous `sha256.ts` (same hashes) |
| `.dependency-cruiser.cjs` `NODE_DEBT` | lists both files | both removed |

No visual change, so no screenshots.

## Blast radius

Grade: 1. Local to two core files; a plain `git revert` restores the previous code.

## Autonomous decisions

- The issue is referenced with `Part of`, not `Fixes`, because this is only the first step of it and merging must not close it.
- A small pure synchronous SHA-256 replaces `node:crypto` hashing, because `hashText` is called synchronously and `subtle.digest` is async; this keeps callers and stored hash values unchanged.

## Known gaps

- None.

<details>
<summary>Details</summary>

## Changes

- `src/core/security/csp.ts`: the nonce is 18 bytes from `getRandomValues`, base64url-encoded with `btoa` (still 24 characters, random per page).
- `src/core/comments/commentStore.ts`: comment ids and the temporary-file suffix use `getRandomValues` (ids keep the `t_`/`c_` + 8 hex format).
- `src/core/comments/sha256.ts`: synchronous SHA-256. A unit test compares it with `node:crypto` on empty, ASCII, multibyte and long inputs and on every length around the block boundaries, so stored comments still match.
- `.dependency-cruiser.cjs`: both files leave `NODE_DEBT`; `just check-boundaries` passes.

## Impacts

No visual change; no behaviour change.

## Test plan

- [x] New or changed tests (they fail on the previous code): SHA-256 equivalence test added; the existing nonce and comment tests pass unchanged
- [x] Local gates at `faba0c4`: `just check` passed
- [x] Evidence: none, internal refactor with no visual change
- [x] Review: approved at `116f39d` (committed as `faba0c4`)
- [x] Verified at `faba0c4`
- [x] CI green at `faba0c4`: static, static-windows, visual, viewer-graph pass; heavy VS Code jobs are skipped on pull requests by the project's rules

## Internal references

- CR-467 use-webcrypto-instead-of-node-crypto-in
- Requirements: no behaviour change; `just requirements-update` run, test added to REVIEW-054 coverage.

</details>
