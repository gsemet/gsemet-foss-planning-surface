# Round 2 review: alert palette after a lazy continuation line

Verdict: **CHANGES REQUESTED** (one blocking finding, a one-line fix)

Reviewed worktree `markdown-okf-schema-studio-wt-223`: uncommitted changes on top of `origin/main`
0b4ede78. No worktree file was modified. To build an `origin/main` baseline, the two changed `src`
files were swapped to their originals, compiled into a copy of `out/`, then restored, and `out/` was
rebuilt from the restored sources. The checksum of `git diff` plus the three untracked files was
`e74bf049…` both before and after. Probe scripts and outputs are in
`/private/tmp/claude-502/cr223-driver/inspector2/` (`cmp.mjs`, `cmp1*.txt`, `norm-*.txt`, `check.txt`).

## Round-1 findings: status

All seven round-1 findings are fixed. Each repro was re-run against
`gh api markdown -f mode=gfm` with `cmp.mjs`, and our alert text, `data-line`/`data-end-line`
and the text outside the alert match GitHub:

1. Lazy `===`, `--` and `=` stay paragraph text and the title stays "Note". Fixed.
2. `2. x`, `-`, `*`, `+ b`, `1) b` and `- [ ] task` on a lazy line end the alert. A quoted
   `> 2. x` stays text. Fixed.
3. A quoted table closes the paragraph, so `foo` and a lazy `| 1 | 2 |` stay outside. A lazy
   delimiter row stays text. Fixed.
4. The HTML comment case puts `lazy` inside, and `# h` / `<custom-x>` puts `lazy` outside. Fixed.
5. The palette ignores alert heads inside fenced code, including inside a ```` ```` ```` fence that
   holds ```` ``` ````. Fixed.
6. The GFM-009 verification note is reworded. Fixed.
7. The colon-fence comment is back next to `let colons`. Fixed.

## Blocking

### 1. A lazy `+++` line after an alert now throws, so the whole document fails to render

- Where: `src/core/syntax/blockQuoteRange.ts:54-58` (`interruptsParagraph`) and `:97-100`
  (`lazyLineAsText`). Both let the MyST block break `+++` through as a lazy line, and
  `src/core/render/mystGithubAlerts.ts:113` writes it into the admonition body.
- Repro: `renderMyst("> [!NOTE]\n> a\n+++\nb\n")` throws
  `TypeError: Cannot read properties of undefined (reading 'length')` in
  `mdast-util-to-hast/lib/state.js:487`. `+++ {"a": 1}` throws the same way.
- On `origin/main`, the same input renders: an alert on lines 1 to 2, then the block break, then
  `b`.
- The root cause is older: `+++` inside any directive already throws
  (`:::{note}\na\n+++\nb\n:::` and a quoted `> +++` throw on origin too). The change makes a
  common unquoted line reach that path.
- GitHub keeps `+++` as text inside the alert.
- Fix (smallest): in `lazyLineAsText`, escape a leading `+++` (`\+++`) as well. That matches GitHub
  and avoids the crash. The other option is to treat `^ {0,3}\+{3}` as a line that starts a block in
  `interruptsParagraph`, which keeps the origin layout. Either way, add a `GITHUB_CASES` row and a
  GFM-009 row. Recording the older directive crash as a backlog item would be welcome.

## Non-blocking

### 2. Other MyST-only syntaxes on a lazy line become MyST blocks inside the alert

- Lazy `% comment`, `(lbl)=`, `[^1]: n` and `$$`…`$$` render as a MyST comment, a target, a
  footnote definition and display math inside the alert. GitHub shows them as paragraph text.
  Before the change, they rendered the same way, but outside the alert.
- None of these crashes, and nothing visible is lost: comments and targets are hidden, and the math
  case looks closer to github.com, which renders `$$` math on the client.
- Fine to leave, but GFM-009 says that a lazy line "stays paragraph text", which these cases don't
  quite meet. Either qualify the wording ("CommonMark/GFM block syntax") or record this as a known
  MyST divergence.

### 3. The build/export snapshot keeps the old "first unquoted line" rule

- `src/node-services/build/sourceTransforms.ts:22-56` has its own `expandGithubAlerts`, used by
  `snapshotWorkspace.ts:397`. It still ends the alert at the first unquoted line, so a built
  snapshot and the preview now disagree on lazy lines.
- This duplication already existed, and no requirement covers that file, so it is out of this CR's
  scope. Suggest a backlog item to make that path use `blockQuoteEnd`.

### 4. Readability of `blockQuoteRange.ts`

- The module is proportionate: 220 lines, one exported range rule plus two small helpers, every
  regex named and commented, and `check-boundaries` and `check-limits` pass. Nits:
  - `:136` uses an anonymous inline regex for "an empty list item". Name it next to `LIST_MARKER`,
    `LIST_ITEM_WITH_TEXT` (`:49-50`).
  - `:130` tests `HTML_BLOCK_START` and `HTML_BLOCK_7` again after `htmlBlockEnd`. It is correct
    (it catches a kind 1-5 block that closes on its own line), but the reason is not obvious, and a
    short comment would help.

### 5. Test diagnosability

- `GITHUB_CASES` (`test/core/render/alertLazyContinuation.test.ts:55-110`) holds about 45 rows in
  one test, which stops at the first failing row. The message names the source, so this is
  acceptable. A per-row `test()` would report every failing row at once.
- `"a lazy setext underline or delimiter row adds no heading or table"` (`:125`) passes on origin,
  because the lazy line was outside the alert there. It is a guard for the round-1 regression, not a
  pre-fix failure, and that is fine as long as it is understood that way.

### 6. For the owner: round-1 finding 8 is unchanged

- An alert inserted on a middle line of a paragraph (`Intro\nSecond\nThird`, caret on `Second`)
  still absorbs `Third` as a lazy line in the preview. The spec covers only the line above.

### 7. For the owner: a leading quoted heading becomes the admonition title

- I confirmed the Coder's open point: this happens on `origin/main` too, so it is not a regression.
  `> [!NOTE]\n> # h\n> b` gets the title "h", while GitHub shows "Note" and an `<h1>`.

## Regression hunt (no differences found)

- Normal alerts without lazy lines: 21 inputs, rendered by `origin/main` and by the worktree, give
  byte-identical HTML (`norm-orig.txt` vs `norm-new.txt`). The inputs covered:
  - EOF without a final newline, titled alerts, bold markers, backtick and tilde fences inside the
    alert;
  - an alert in a list item, a grid card or a tab item, and context tags;
  - CRLF, frontmatter, an alert marker inside a fence, a nested quote, consecutive alerts;
  - an alert followed by a heading, a list or a fence.
- Lazy lines with the new code all match GitHub:
  - titled and bold-marker alerts with a lazy line, and a lazy line after a quoted fence;
  - two alerts each with a lazy line, and `> [!TIP]` after lazy lines (literal text, as on GitHub);
  - an indented `    ===`, `=== b`, ` -- `, `|-|`, `| x |`, `\===`;
  - `---`, `- - -`, `___` (thematic break outside), a list continuation inside the alert, a link
    reference definition, `<span>`, `<details>`.
- The escape does not leak:
  - The rendered text shows `===` and `| - | - |`, never the backslash.
  - The block editor text comes from the document lines (`src/session/features/blockEdits.ts`
    `currentSourceEdit` → `document.getText()`), not from the rewritten body.
  - `expandGithubAlertsWithLines` has only render callers.
- Palette probes:
  - The caret on a lazy line in a `:::{card}`, or in a list-item alert, changes that head.
  - A selection keeps its range and shifts with the head length.
  - A caret on a non-alert quote under an alert inserts the new alert after a blank line.
  - The caret after a quoted `# h` is outside the alert.
- Requirements:
  - GFM-009 and PALETTE-115 are `proposed`, and their wording matches the behaviour, except
    finding 2.
  - The index is regenerated, the log entry is present, and GFM-037 and the approved requirements
    are untouched.
- Screenshots: `after-alert-lazy-{cream,dark}.png` show the lazy line inside the Note in both
  themes, where `before-*` shows it as a paragraph below the box. Plain quotes are unchanged.

## Tests fail on the original code (spot-checked)

- Setup: the new tests ran against `origin/main`'s `mystGithubAlerts.ts` and `blockEditActions.ts`
  (with `blockQuoteRange.ts` present). The three test files ran 30 tests, and 13 failed.
- The failures are:
  - all 4 lazy render tests except the setext guard (finding 5);
  - the rewritten `alertSourceLines` lazy test;
  - all 8 palette tests, the fence-aware one included.
- The changed `alertSourceLines` assertion is the owner-approved behaviour, and the list-item case
  is kept as a new test.

## Gate results

- `just check`: green (exit 0).
  - Format, compile, boundaries (314 modules), limits (905 files), exports, markers and settings
    pass.
  - Unit 3334/3334, contracts, security 71/71, pytest 153 passed.
  - requirements-lint: 1072 requirements, 0 errors.
  - No flakes this run.
- `UV_NO_CONFIG=1 uv run --group requirements okfreq validate --check-links --project-root .`:
  1072 requirements, 0 errors, 21 warnings (the existing PALETTE-264 cross-link warnings).
- GitHub comparison: `gh api markdown -f mode=gfm` on 50 inputs (`cmp1.txt`, `cmp1b.txt`).
