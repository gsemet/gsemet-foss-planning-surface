# Review round 1: alert inside a colon container

Reviewed the uncommitted change in `markdown-okf-schema-studio-wt-177`: the `mystGithubAlerts.ts`
diff, the new test `test/core/render/alertInsideColonContainer.test.ts`, the GFM-009 scenario and
the CHANGELOG entry.

**Verdict: changes required** (one real tracking bug, one cheap robustness fix; the rest is minor).

## What runs

- `npm run compile`: ok.
- `npm run test:unit`: 3158 / 3158 pass (includes the new test, `alertSourceLines`, `crlfAlerts`,
  `mystFeatures`).
- `npm run test:contracts`: ok. `check:markers`, `check:limits`: ok.
- `UV_NO_CONFIG=1 uv run --group requirements okfreq validate --check-links --project-root .`:
  1065 requirements, 0 errors, 0 warnings.

The approach is right: a longer colon fence cannot work (a colon container closes at the first
colon-only line at least as long as its own), and a backtick directive is opaque to the enclosing
colon container. Line maps are unchanged in shape (same number of output lines; only the fence
text differs), so `sourceLines`, `alertSourceLines.test.ts` and `crlfAlerts.test.ts` stay exact.
CRLF renders identically to LF inside a card (probed).

## Required changes

### 1. Closing fences of four or more colons are counted as openers

`COLON_OPEN = /^\s*(:{3,})\s*\S/u` matches `::::` and `:::::`: the regex backtracks to three colons
and the fourth colon satisfies `\S`. Since `colonClose` is only tried when `colonOpen` fails, every
closing line of a tab set or grid pushes a phantom `3` onto the stack, and the stack never empties.

Probe (`expandGithubAlertsWithLines`):

```text
::::{grid}
:::{card}
x
:::
::::

> [!NOTE]
> a
```

gives ```` ````{note} ```` for the top-level alert. It still renders correctly (a backtick directive
works anywhere), but it contradicts the GFM-009 row "an alert outside every colon container is a
colon-fence admonition, as before" for every alert after the first tab set or grid of a document.

Fix: forbid a further colon after the captured run, e.g. `/^\s*(:{3,})(?!:)\s*\S/u` (or
`[^:\s]` right after the run). Add the case above to the "outside stays a colon fence" test (an
alert after a closed `::::{tab-set}` / `:::::{grid}`), so the test catches it.

### 2. Pick a backtick fence longer than any backtick run in the alert body

With a fixed ```` ```` ````, an alert body holding a four-backtick code block breaks the note:

```text
:::{card} T
> [!NOTE]
> ````md
> code
> ````

after
:::
```

renders the note with the code, then a stray code block swallowing `after` (probed through
`renderMyst`: `<pre><code data-line="5" data-end-line="7">after</code></pre>`). Three-backtick
code in the body is fine. This is cheap to avoid: before emitting the opener, scan the quoted
lines the inner loop is about to consume for `/^\s*(`{3,})/` after `stripQuote`, and use
`` "`".repeat(Math.max(4, longest + 1)) `` for both opener and closer. Add one test with a
four-backtick block in the alert body inside a card (`after` stays a paragraph in the card).

## Minor (non-blocking)

- `colonOpen && !GITHUB_BOLD_ALERT_MARKER.test(line)`: a bold marker starts with `>` and can never
  match `COLON_OPEN`, so the guard is dead code; drop it.
- `COLON_OPEN` / `COLON_CLOSE` accept any indentation; a `:::{card}` indented four spaces (indented
  code) is counted as an open container (probed). Over-counting is harmless (backtick directive),
  so this is acceptable; a `^ {0,3}` anchor would be more exact. Colons inside a code fence are
  correctly ignored (`advanceFence` runs first), and colon fences inside an alert body are consumed
  by the alert loop, not tracked, which is right (the backtick directive body is parsed apart).
- Test helper `innermostWith`: its doc says "and none of the others' text" but it returns the first
  match; fix the doc or the helper. In the tab test, `tab` is only asserted non-empty and otherwise
  unused.
- A few test lines exceed 120 characters (32, 69, 70, 100); no linter enforces it, cosmetic.
- GFM-009 "Criteria" line does not mention the new boundary (the text after an alert stays in the
  enclosing colon container); worth one clause so the criteria cover the new scenario.

## Tests quality

No existing assertion was weakened. The new tests check structure (text after the alert is inside
the card / the same tab panel, the text after the container is outside) and exact
`data-line` / `data-end-line` tuples for the card, tab set and nested grid cases. The gap is the
"outside" test, which only covers an alert after a three-colon card and so misses issue 1.

## SwRS and CHANGELOG

- GFM-009 scenario is clear and matches the behaviour, apart from row 3 being violated by issue 1.
  `tested_in_files` and the Method line are updated.
- CHANGELOG entry is user-facing, under Unreleased, wrapped at 100: fine.
