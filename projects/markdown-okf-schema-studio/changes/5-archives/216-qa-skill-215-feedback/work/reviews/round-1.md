# CR 216 review, round 1 (Inspector)

Verdict: APPROVE

Worktree `markdown-okf-schema-studio-wt-216`, base `origin/main` 18c4f020, uncommitted change.

## What was checked

- **Scope.** Only files under `.agents/skills/markdown-studio-exploratory-qa-claude/` changed
  (SKILL.md, 3 references, 6 scripts, 8 scenarios, 2 synth fixtures). Nothing under `src/` or
  `test/`.
- **33 rows, checked in the files, not in the report.**
  F1 `new-features.py` `carried_rows` (run on the real 215 `00-index.md`: carries exactly #223,
  "not run"). F2 three new `AREAS` rows. F3 doctor polls 3 s. F4 `listWindows`/`q sessions`, doctor
  window count. F5 SKILL §2 and pitfalls. A1 `comment` step. A2 `asExpression`. A3 `export
  QA_SESSION`, `\rm -f`, `>|`. A4/A5/A6 pitfalls plus `--frame`, `pickFrame`, id matching. A7/A17
  pitfalls and command table. A8/B9 `clicksel` 0×0 error (engine and CLI) plus docs, `D` vs
  `document`. A9/A10 fixtures promoted, `--clone` refresh, crlf naming explained. A11, A13, A14,
  A15, A16 documented. A12 `peval` step, `maxLines` per side. B1 `CONTROLS` in `noop-sweep.mjs`.
  B2 `open-side-preview-edit.json`. B3 `--from/--limit` mandatory. B4 `editorMatches`. B5
  first-`=` split and repeatable `--var` (the old `split("=", 2)` dropped the value of
  `--var=t=…`, which explains the row). B6 stated as unsupported in harness-pitfalls. B7, B8, B10,
  B11 documented. All present.
- **Scripts.** `bash -n`, `node --check` (all `.mjs`), `py_compile` pass. Scratch checks under
  `/private/tmp/claude-502/cr216-driver/inspector/t.mjs`: `asExpression` on 11 inputs, `editorMatches`
  on 8 cases with two roots, `args`/`varPairs` (`--var 't=3. Quoted'`, `--var=a=b=c`, `--frame 1`),
  `listWindows` with no window (0). `--frame` absent leaves `which` at 0 as before; cells keep the
  same first click point in `noop-sweep.mjs`, so the sweep is unchanged apart from controls.
  `setup-workspace.sh --clone` only copies over `ws/synth` and deletes nothing but
  `crlf-source.md`, which it regenerates.
- **Scenarios.** 30 parse. The 7 promoted replays match the archive's `replay/scenarios/` except
  for the documented additions (comment steps, c7-1 setup, c4-1 moved to `synth/review-threads.md`).
  `radio-c1.md` is byte-identical to the archive. Every referenced fixture exists in the skill
  or in `test/visual/fixtures`. `c3-cards.md` matches the c3-2 sheet (numbered grid card plus a
  standalone `{card}` with a bold title; both render through `buildCard` with
  `.myst-grid-card-title`). File names do not collide.
- **Docs.** New lines wrap at 100 characters (the lines over 100 already existed). Relative links
  resolve. No private paths added. SKILL.md went from 314 to 332 lines.
- **`just check`** in the worktree: exit 0. The W2 broken-link warnings come from the requirements
  and already exist on main.

## Findings

1. **minor**: `scripts/engine.mjs:41-45` (`asExpression`), used for `page.evaluate` in
   `engine.mjs:277,290,340` and `qa.mjs:573`. Playwright evaluates a string with `global.eval`
   (checked in `playwright-core` `UtilityScript.evaluate`), so `q peval 'a; b'` and
   `q peval 'document.title;'` used to return the completion value. Now they are wrapped in an async
   IIFE and return `undefined`. A trailing `;` in `feval` or a webview `eval` also gives `undefined`
   silently. Checks fail rather than pass, so this does not give a false PASS.
   Fix: strip one trailing `;` and whitespace before the expression test. For the `page.evaluate`
   paths, send the text unchanged when it compiles as a script (`new vm.Script(text)` from
   `node:vm`), and wrap it only when it does not (a top-level `return`). Keep the current wrapping
   for the webview paths.
2. **minor**: `scripts/engine.mjs:56-58` (`editorMatches`, root-relative rule).
   `wanted.endsWith('/' + rel)` matches any longer `want` whose tail is the file's path relative to
   the root. Scratch check: root `/q/ws`, active `ws/book/x.md`, want `other/book/x.md` gives
   `true`. Likewise, an open `ws/README.md` matches want `fixtures-visual/README.md`, which is a
   false PASS of an oracle. Fix: allow one leading folder segment only, for example
   `rel === wanted || wanted.slice(wanted.indexOf("/") + 1) === rel`, and add that case to the doc
   comment.
3. **nit**: the promoted replays `scenarios/c3-1-…`, `c3-2-…`, `c4-1-…`, `c7-1-…`, `c7-2-…` and
   `215-c*-…` still use the provisional IDs in their check labels. `scenario-format.md` asks for the
   finding ID there, and `c3-1`/`c4-1`/`c7-1` already name campaign-210 replays. Fix: keep the file
   names, because the archived sheets link to them. Put the final ID in each label, for example
   `"label": "QA215-07 numbered grid-card title renders *card* as emphasis"`.
4. **nit**: `SKILL.md` §3, the mission sentence before the code block, ends with the single word
   `run` on its own line. Fix: rewrap the sentence so that `run` joins the line before it.
5. **nit**: `SKILL.md` §1 calls `new-features.py` and describes it as "PRs merged since the last
   campaign". The new carry-forward of TODO and "not run" rows (F1) is described only in the
   script's docstring and output. Fix: add a few words to that comment or to the following paragraph,
   for example "plus the previous index's rows that were never covered".

No blocker or major. Window-level behaviour (sweep on `74-radio-plan.md`, `q frames` with two
webviews, `q sessions`) was not re-run here. The coder ran it once in a window, and this review
relies on that run.
