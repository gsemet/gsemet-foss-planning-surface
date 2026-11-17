# 217 — In edit mode a click on a link opens the editor; Cmd/Ctrl+click follows it

:::{important}
**Owner GO, via the Chief of Staff, 2026-10-31.** Batch "all P1 and P2" as one tested stack. One clean
commit, one ready PR, never merge.
:::

The full intent is in [backlog-item/01-intent.md](backlog-item/01-intent.md). Its sections still ticked
`Uncheck to disagree: [x]` are the scope; skip any unticked section.

| | |
| --- | --- |
| Priority | P1 |
| Notes | P1, first in the stack. Owner rule (2026-10-31): in edit mode a click, Enter or Space on any link opens the block editor; Cmd/Ctrl+click and Cmd/Ctrl+Enter follow it; reading mode unchanged. BLOCK-014 is proposed (no approval needed). |
| Behaviour gate | User-facing change: the Driver stops after its analysis and sends a **Behaviour change** note (Today, After, Requirements touched, choices the item left open). Code starts only after the owner answers. |
| Requirements | Approved requirements other than GFM-037 and REVIEW-152 are not changed: if the fix needs it, stop and ask. |

## Done when

- [ ] The ticked sections of the intent are done, with their tests (failing before the fix).
- [ ] Before/after screenshots for every visible change.
- [ ] `just check` and `okfreq validate --check-links` green.
