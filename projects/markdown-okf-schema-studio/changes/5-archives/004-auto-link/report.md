# Report — auto-link

Status: **done** (P2 bug run, 2026-10-15, branch `dev/gsemet`).

## Delivered

| Task | Change | Commit |
| --- | --- | --- |
| T8 | 56 px top margin so the first block editor / "Start writing" clears the floating toolbar | `4abf94a` |
| T9 | Bare `http(s)://` and `www.` URLs are clickable | `a6d6d1a` |

## Proof of completion

- T9: review FIX-REQUIRED (quadratic trailing-`)` trim took 88 s on 100k characters), replaced by
  a linear scan; review then passed.
- Final run: 775 unit + 2 contract + 20 security tests pass; visual 119 scenarios green.
