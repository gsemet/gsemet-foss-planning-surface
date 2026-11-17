# Progress report: batch-03

Batch-03, direct mode (the Chief of Staff steers, no Foreman session), a stack of one change CR and
one release CR. Spent so far: $5.99, no budget.

| CR | State | PR |
| --- | --- | --- |
| CR-315 marketplace-trusted-publishing | merged by the owner, 2026-11-13 15:09Z (b1907e9f) | https://github.com/gsemet/markdown-okf-schema-studio/pull/387 |
| CR-316 release-v1-8-1 | confirmed, starting | - |

- CR-315: the release job publishes to the VS Code Marketplace with Trusted Publishing (GitHub
  OIDC, `vsce publish --oidc`, vsce 4.1.0) instead of the `VSCE_PAT` secret; `ci.yml`'s `release`
  job gains `id-token: write`. Two rounds; the inspector approved the second. The local real-window
  integration failed because another app had window focus; the owner accepted the branch heavy run
  (43445113627, green on the exact head) as the gate. Verifier: VERIFIED.
- Owner setup outside the repository: two Marketplace policies (`release.yml` and `ci.yml`, both
  environment `release`); Open VSX account, namespace claim and a hand publish of 1.8.0 (parked
  CR `publish-to-open-vsx`).
- Not proved yet: a real OIDC publish. 1.8.1 is that proof.
- Waiting for the pause: the floating toolbar in four columns (`floating-toolbar-four-wide`,
  specified), which a running direct batch cannot take.
