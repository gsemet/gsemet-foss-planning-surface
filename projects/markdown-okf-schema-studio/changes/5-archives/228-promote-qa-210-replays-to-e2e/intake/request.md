# 228 — Promote the passing QA replays to real-input E2E tests

:::{important}
**Owner GO, via the Chief of Staff, 2026-10-31.** Batch "all P1 and P2" as one tested stack. One clean
commit, one ready PR, never merge.
:::

The full intent is in [backlog-item/01-intent.md](../work/backlog-item/intent.md). Its sections still ticked
`Uncheck to disagree: [x]` are the scope; skip any unticked section.

| | |
| --- | --- |
| Priority | P2 |
| Notes | LAST in the stack, on top of every other CR of this batch. By then the fixed bugs' replays should pass: promote only those; for the others, record which bug still blocks them. No user-facing change: no behaviour gate. |
| Behaviour gate | No user-facing change: this CR skips the behaviour gate. |
| Requirements | Approved requirements other than GFM-037 and REVIEW-152 are not changed: if the fix needs it, stop and ask. |

## Done when

- [ ] The ticked sections of the intent are done, with their tests (failing before the fix).
- [ ] Before/after screenshots for every visible change.
- [ ] `just check` and `okfreq validate --check-links` green.
