# Use WebCrypto instead of node:crypto in core

issue: https://github.com/gsemet/markdown-okf-schema-studio/issues/413

Part 1 of issue #413 (browser-capable host), the WEB_CRYPTO debt of `.dependency-cruiser.cjs`.

- `src/core/comments/commentStore.ts` (comment ids and text hashes) and `src/core/security/csp.ts`
  (CSP nonce) stop importing `node:crypto` and use `globalThis.crypto` (WebCrypto: `randomUUID`,
  `getRandomValues`, `subtle.digest` where a hash is needed), available in Node 24 and in browsers.
- If a hash is computed synchronously today and `subtle.digest` would force an async change, keep the
  behaviour (ids, hash values and their format unchanged, so stored comments still match) and say
  how in the PR.
- Remove both files from `NODE_DEBT` in `.dependency-cruiser.cjs`; `just check-boundaries` passes.
- No behaviour change: existing comments load and anchor as before; the CSP nonce stays random per
  page.
