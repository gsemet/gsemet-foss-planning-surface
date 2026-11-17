Verdict: VERIFIED

Head 8512191a, test file test/core/render/gridCardTitleSourceLine.test.ts (22 tests).
1. At head (node --import ./scripts/register-myst-patches.mjs --test): 22 pass, 0 fail.
2. On a detached worktree of origin/main with the test file copied in (removed after): 18 pass, 4 fail.
   Failing on main: quoted grid with blank first line; doubly quoted grid with blank first line;
   quoted backtick card with blank first body line; quoted card with an option line.
   Deviation from plan: the plan expected 3 failures; "a quoted card with an option line"
   also fails on main (the spec table listed it as Correct). Same prefix-stripping cause; fixed at head.
   All other rows pass on both.
3. BLOCK-258 boundary scenario "A grid card inside a quote", log.md entry and CHANGELOG line exist in the diff.
Heavy CI 43317287276 green (reported by caller, not rechecked).
