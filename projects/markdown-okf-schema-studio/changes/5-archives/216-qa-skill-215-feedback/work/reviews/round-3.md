# CR 216 review, round 3 (Inspector)

Verdict: APPROVE

Worktree `markdown-okf-schema-studio-wt-216`, base `origin/main` 18c4f020, uncommitted change.

## What was checked

- **Round-2 finding 1 (trailing `;` in the webview).** It is fixed. `asExpression`
  (`scripts/engine.mjs:164-169`) now returns the stripped text when it parses as an expression.
  Scratch check `/private/tmp/claude-502/cr216-driver/inspector-r3/t.mjs` runs every output inside a
  copy of the real `wv` wrapper (`qa.mjs:386-390`, `return (${body}\n);`). `D.title;` gives `T`,
  `D.title ;  ` gives `T`, `D.querySelectorAll('x').length;` gives 2, `await Promise.resolve(8);`
  gives 8. Statement bodies are still wrapped in the async IIFE: `const n = 1; return n + 1` gives 2,
  `if (true) { return 4 }` gives 4, `return await …` gives 9. Text with no `return` gives
  `undefined`, as the doc says. `({a:1})`, `{a:1}`, `() => 1` and `function f(){}` behave as on
  `main`.
- **Round-2 finding 2 (bare `await` in the page).** It is fixed. `asPageExpression`
  (`engine.mjs:173-180`) wraps a bare top-level `await x` (with or without a trailing `;`, and
  `await a + await b`) as `(async () => (expr\n))()`. Through Playwright's
  `normalizeEvaluationExpression` + `globalThis.eval` emulation it gives 3, 3 and 3.
  `return await x` and `const v = await …; return v` keep the statement wrap and give 4 and 5.
- **No regression on the page path.** Text that compiles as a script is still sent unchanged:
  `document.title;` gives `T`, `var a=1; a+1` gives 2, `let x = 5; x` gives 5, `a; b` gives 2,
  `{a:1}` gives 1 (a block, as on `main`), `({a:1})` gives the object, function and async function
  expressions give a function. Text that does not compile is sent unchanged, so the page reports
  its own `SyntaxError`.
- **`editorMatches`** gives the same results as in round 2. One case in my round-2 table is marked
  BAD, `x.md` against `/q/wsx/book/x.md`, but my own expectation was wrong there: the plain suffix
  rule matches it on purpose.
- **Doc.** `references/scenario-format.md:100-102` now says what the code does.
- **Whole diff, read once more.** Nothing new. The diff stat is the same 10 modified files plus the
  new synth fixtures and 8 scenarios.
- **Gates.** `node --check` passes on all `scripts/*.mjs`. All 30 `scenarios/*.json` parse. The
  coder's scratch test passes 21/21. `just check` in the worktree exits 0
  (log: `/private/tmp/claude-502/cr216-driver/inspector-r3/just-check.log`). The only W2 warnings
  are the broken links that were already in the requirements. The `HANG DUMP` lines come from the
  CR 173 watchdog tests, and those tests pass.

## Findings

1. **nit**: `scripts/engine.mjs:167`. In the webview, a trailing `;` followed by a comment
   (`x; // c`) is not stripped, so the text gets the statement wrap and gives `undefined`.
   This is an edge case and not a regression. No fix is needed.
2. **nit**: `scripts/engine.mjs:178`. The `!out.startsWith("(async")` guard misses text that itself
   starts with `(async` and contains a bare `await` (`(async () => 1)() + await x`). That text is
   sent unchanged and fails in the page. This is very unlikely, and it is not a regression.
3. **nit**: `references/scenario-format.md:100,102`. These lines are 121 and 202 characters long.
   The file already had 12 lines over 100 characters on `main`, so this follows the file's style.
   Wrapping is optional.

No blockers or majors. Both round-2 findings are closed, and the round-1 findings stay closed.
