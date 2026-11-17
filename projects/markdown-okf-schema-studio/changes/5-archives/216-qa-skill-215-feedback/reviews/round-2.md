# CR 216 review, round 2 (Inspector)

Verdict: CHANGES REQUESTED

Worktree `markdown-okf-schema-studio-wt-216`, base `origin/main` 18c4f020, uncommitted change.

## What was checked

- **Round-1 finding 1 (`asExpression` / `asPageExpression`).** Scratch checks in
  `/private/tmp/claude-502/cr216-driver/inspector-r2/t.mjs` pass each output through a copy of the
  `wv` wrapper in `qa.mjs:386-390` (`return (${body}\n);`) and, for the page, through Playwright's
  own path: `normalizeEvaluationExpression` then `globalThis.eval`, as found in
  `node_modules/playwright-core/lib/coreBundle.js:20638,25682`.
  The page path is correct. Text that compiles as a script is sent unchanged, so it behaves as on
  `main`: `document.title;` gives `T`, `var a=1; a+1` gives 2, `let x = 5; x` gives 5, `{a:1}` gives 1
  (a block, as on `main`), `({a:1})` gives the object, and `() => 1` / `function f(){}` give a function,
  the same as on `main`. Only text with a top-level `return` gets wrapped. The webview path is still
  wrong for a trailing `;` (finding 1 below).
- **Round-1 finding 2 (`editorMatches`).** It is fixed. The rule `rel === wanted ||
  wanted === basename(root)/rel` is right, and the reviewer's round-1 suggestion was wrong, as the
  coder said. I ran 13 cases. The absolute path, `ws/book/x.md`, `./book/x.md`, `book/x.md` and
  `x.md` under root `/q/ws/book` (also with a trailing `/`), and `%20` decoding all match. `ook/x.md`,
  `other/book/x.md`, `fixtures-visual/README.md` for `ws/README.md`, `ws/x.md` under `/q/ws/book`,
  a `null` uri and a missing root all give the expected result. The plain suffix rule still matches
  any path-boundary tail, which is intended.
- **Round-1 finding 3 (IDs).** It is fixed. I checked the 7 promoted replays against the
  campaign-215 `00-index.md` findings table. c3-1 is QA215-01, 215-c1-1 is QA215-02, 215-c2-1 is
  QA215-03 (its third check, "one tab stop", is QA215-02, which is right because c2-2 was merged
  into QA215-02), c7-1 is QA215-04, c7-2 is QA215-05, c4-1 is QA215-06 and c3-2 is QA215-07.
  File names are unchanged.
- **Round-1 findings 4 and 5 (SKILL.md).** Both are fixed. `run` is no longer alone on its line.
  §1 now says the script "carries forward the previous index's rows left at TODO or "not run"".
- **Whole diff, read again.** I found nothing new apart from finding 1. The other changes from
  round 1 are unchanged: `comment` step, `--frame`/`pickFrame`, `clicksel` 0×0 guard, doctor
  observer poll, `listWindows`/`sessions`, first-`=` split, repeatable `--var`. No current
  scenario has a trailing `;` in `expr`/`eval`/`waitFor`, so no shipped replay breaks.
- **Gates.** `node --check` passes on all `scripts/*.mjs`. All 30 `scenarios/*.json` parse.
  `py_compile` and `bash -n setup-workspace.sh` pass. The coder's scratch test passes 14/14.
  `just check` in the worktree exits 0; the only W2 warnings are the existing broken links in the
  requirements.

## Findings

1. **minor**: `scripts/engine.mjs:166` (`asExpression`), and the doc that describes it at
   `references/scenario-format.md:100`. The trailing `;` is stripped only for the expression test.
   The function then returns the original text, and `wv` puts it inside `return (…\n);`. Scratch
   check: `asExpression("D.title;")` returns `"D.title;"`, and the webview gets
   `return (D.title;\n);`, which gives `SyntaxError: Unexpected token ';'`. The same happens with
   `"D.querySelectorAll('x').length;"`. This hits `feval` (CLI `qa.mjs:572`, check
   `engine.mjs:351`), the `eval` step (`engine.mjs:300`) and `waitFor` (`engine.mjs:285`).
   `waitFor` is worse: `waitUntil` keeps retrying until its timeout, and the cause is never shown.
   The doc says "One trailing `;` is ignored", which is false in the webview. It is true only in the
   workbench page, where `vm.Script` accepts the text first. This gives no false PASS, but the
   round-2 claim "asExpression strips one trailing `;`" does not hold for what gets sent.
   Fix: return the stripped text when the expression test passes, for example
   `const expr = text.replace(/;\s*$/, ""); if (parses(\`return (${expr}\n);\`)) return expr;`.
   Then add a scratch case that runs the output inside the `wv` wrapper, not just a check of the
   returned string. The coder's test currently asserts `asExpression("D.title;") === "D.title;"`,
   which is exactly the failing case.
2. **nit**: `scripts/engine.mjs:172-175` (`asPageExpression`). An expression that uses `await`
   (`await Promise.resolve(3)`) does not compile with `vm.Script`. `asExpression` still accepts it as
   an expression (it parses inside an `AsyncFunction`) and returns it unchanged, so the page gets a
   bare `await` and fails with `await is only valid in async functions`. This is the same as on
   `main`, so it is not a regression. Either wrap it when `vm.Script` fails
   (`(async () => (${expr}\n))()`), or add one line to `scenario-format.md` saying that `peval` needs
   `return await …` for promises.

Finding 1 is a one-line fix plus its test. After that the round can be approved: findings 2–5 from
round 1 are closed, and nothing else regressed.
