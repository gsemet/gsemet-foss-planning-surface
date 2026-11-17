# 230 — A wide table keeps its horizontal scroll in Auto width

:::{important}
**Owner GO, via the Chief of Staff, 2026-10-31.** Fix now, inside the P1+P2 stack, under the wide-table Tab
change. One clean commit, one ready PR, never merge.
:::

The intent is in [backlog-item/01-intent.md](backlog-item/01-intent.md). The heavy CI run of 2026-10-31
reproduced it: in Auto width, after a wide table is scrolled sideways with no cell editor open, its
`scrollLeft` reads 0 on every following frame.

| | |
| --- | --- |
| Priority | P2 (raised from P3) |
| Behaviour gate | Required: the owner validates Today/After before any code. |
| Requirements | Approved requirements other than GFM-037 and REVIEW-152 are not changed: if needed, stop and ask. |

## Done when

- [ ] In Auto width, a wide table keeps the horizontal scroll the user gave it, with or without an open editor.
- [ ] A test fails before the fix; the wide-table real-input Auto pass works against the fix.
- [ ] Before/after screenshots; `just check` and `okfreq validate --check-links` green.
