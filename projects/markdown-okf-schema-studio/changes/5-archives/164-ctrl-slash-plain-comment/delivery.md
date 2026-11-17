# Report — ctrl-slash-plain-comment

Status: **done** (2026-10-28, branch `change-requests/164-ctrl-slash-plain-comment`,
PR [#176](https://github.com/gsemet/markdown-okf-schema-studio/pull/176), head `acfc6674 (merge of main added on GitHub; driver head 591cc0b4)`, merged as 2577039e).

## Delivered

| Task | Change | Commit |
| --- | --- | --- |
| T1 | Ctrl+/ (Cmd+/) toggles a plain `<!-- … -->` via a shortcut-only `comment` action; it removes only what it adds; TODO keeps its button and `/todo` without a shortcut; table cell editor unchanged; SwRS PALETTE-266 (proposed), REVIEW-160 and PALETTE-083 amended (proposed); CHANGELOG, docs/user/editing.md | `2577039e` |

## Proof of completion

- One round, reviewer APPROVE. `just check` green (3117 unit, 69 contract); `okfreq validate --check-links` 0 errors.
- CI: normal [40726229046](https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40726229046) pass on 591cc0b4. Heavy: never completed (merged before dispatch; run 40728302661 cancelled). The real-input `scenarioShortcuts` expectation change is unproven in a real window until main's heavy run.

## Open items

- Heavy proof of the real-input `scenarioShortcuts` change: next heavy run on main.
- Not removed yet: worktree `../markdown-okf-schema-studio-wt-164` and its branch.
