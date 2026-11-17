# CR 211 — Inspector review, round 2

Worktree: `markdown-okf-schema-studio-wt-211` (base `b9118506`). Scope: `git diff`, plus the
untracked `scripts/new-features.py`, `assets/synth/admon.md`, and the 28 campaign-210
scenario/synth files (c2-1 edited this round).

## Verdict: CHANGES REQUESTED

All 11 round-1 findings are addressed, and items 1–4, 6 and 7 are done. The owner requests (a)
`admon.md` and (b) c2-1 are done. One defect remains in the item-5 recovery path (finding 1): in
the default toolbar state the Back button is hidden, so "go back after a navigation" never works,
and the next kinds then run on the wrong document. The fix is small. Everything else is minor or
a nit and does not block.

## Round-1 findings: status

| # | Status | Note |
| --- | --- | --- |
| 1 | Fixed | `PICK_POINT` tests candidate points with `D.elementFromPoint(...).closest('a[href]')`; the dead `isLinkOnly` helper is gone |
| 2a | Fixed | `DOC_ID` reads `html[data-sphinx-preview-document-id]` (set in `src/page/runtime.ts:93`, a URI string), with the old mapped-block attribute as fallback; compared 500 ms after the click |
| 2b | Partly fixed | Uses `[data-sphinx-preview-back]` (exists: `src/core/preview/previewToolbar.ts:14`, wired in `src/page/modules/historyControls.ts:18`) with a real click, polls 5 s, then `setEditMode(ctx, true)`. But see finding 1 |
| 3 | Fixed | `assets/synth/admon.md` shipped; every scenario `file` resolves in a freshly built workspace |
| 4 | Fixed | `min(index Date, rev %cs) − 1 day`; warning at 200 PRs |
| 5 | Fixed | `Revision:` matches win; prose matches are used only when no index has one |
| 6 | Fixed | `NEWFEATURE` line in the charter return |
| 7 | Fixed | The replay window counts against the allowance; there is a no-sub-agent fallback |
| 8 | Fixed | E1/E3/E4 point at `fixtures-visual/07-frontmatter.md`, `08-okf-schema.md` (both exist) and synth files; A3 points at `docs/` |
| 9–11 | Fixed | 210 in `previous-campaigns`, `--dry-run` documented, vault rsync excludes first plus `--prune-empty-dirs` |

## Findings

1. **major**: `scripts/noop-sweep.mjs:120-129`, the way back after a navigation.
   (a) The Back button is in the toolbar's "more" rows (`previewToolbar.ts:46-50`), which the
   collapse button hides with `hidden`. **Without a stored preference the toolbar starts
   collapsed** (`src/page/modules/toolbarCollapse.ts`, `toolbarCollapsed !== false`), and `q launch`
   always creates a fresh `msq-*` profile. So `box([data-sphinx-preview-back])` returns
   `{w: 0, h: 0}` at the frame origin rather than `null`, and the sweep clicks the top-left corner
   of the preview. That stray click can land on content in edit mode. The id never comes back, so
   the recovery always fails. The button is also `disabled` until the host reports
   `canBack` (`historyControls.ts:21,41`).
   (b) After `Back did not return …; stopping ${kind}`, the `break` leaves only the current kind.
   The outer loop then sweeps `cells` and `fields` on the *navigated* document, while `buffer()`
   still compares the original file, so changes there would go unseen. Round-1 finding 2 asked
   not to continue on the wrong document.
   (c) A navigation slower than 500 ms (a large chapter) is missed by the single check, so the
   next targets come back "not found" (the 210 derail).
   **Fix:** before locating Back, if
   `D.querySelector('[data-sphinx-preview-toolbar-collapse][aria-expanded="false"]')` exists, click
   it through `box(...)` and wait about 600 ms. Wait until Back has `w > 0` and `!disabled`
   (poll), then click it. If the id still does not return, stop the **whole sweep**: set a flag and
   break the outer `for (const kind …)` loop too, and keep writing the report with the error. Also
   compare `DOC_ID` at the top of each target iteration (cheap; catches late navigations). Update
   the wording in `harness-pitfalls.md:88-91` and `SKILL.md:136-138` ("stops that kind" → "stops
   the sweep").
2. **minor**: `scripts/new-features.py:129-135`, drop rules 2 and 3 can hide a real new PR.
   Rule 2 (`mergedAt <= revision committer time`) is right only when the revision is a commit of
   the default branch. If a campaign tests a branch or a rebased commit, its committer date is
   later than PRs that are *not* in it, and those PRs are dropped. Rule 3 drops a PR whose title
   matches *any* older subject (`fix: typo`). Both errors go in the unsafe direction: a missing row
   means no gap. The timezone handling itself is correct (`%cI` and `mergedAt`, with `Z` replaced
   by `+00:00`, are both offset-aware). The script also fails safe when `git show` or `git log`
   fails: `cm.git` returns `""`, so `rev_time` stays `None` and the subjects set is empty.
   **Fix:** apply rule 2 only when `git merge-base --is-ancestor <rev> origin/<default>` succeeds
   (or `git branch -r --contains <rev>` lists the default branch). For rule 3, restrict the match
   to the `(#<number>)` form, or to subjects in `git log <rev> --since=<date>`.
3. **minor**: `scenarios/c2-1-comments-toggle-keeps-threads.json:8`. The selector is correct
   (`previewToolbar.ts:32`; `aria-expanded` is set to `"false"` when collapsed by
   `toolbarCollapse.ts` `apply()`), and the selector's double quotes are safe (`elementsJs` uses
   `JSON.stringify`). `engine.mjs:368-373` does honour `optional` (the run continues), but a failed
   optional step still runs `state.failed += 1` and prints `FAIL 4 step …`. When the toolbar is
   already expanded, the scenario ends with "N pass, 1 fail" even if the bug checks pass. `c7-1`,
   `c1-1` and `c1-2` share this, so it is not new, but the docs (`scenario-format.md:38`) say only
   "continue". **Fix (either):** in `runSteps`, give an optional step that fails an `..   n optional
   step skipped: …` note and do not count it, or state in `scenario-format.md` that an optional
   failure still counts.
4. **nit**: `scripts/noop-sweep.mjs:8-9` and `SKILL.md:280` say link-only blocks "are skipped". With
   point picking, a wide `<p>` holding only a link usually has a free point right of the link, so
   it is clicked (safely, off the link) and not skipped. `SKILL.md:134-136` and the pitfalls entry
   describe it correctly. Align the header and the script list with "skipped only when every
   candidate point is on a link".
5. **nit**: `references/bug-sheet-template.md:13`, "starts with the block above": the block is
   *below*, in the templates. Write "the Currently / Expected block of the templates below".
6. **nit**: prose lines over 100 characters: `SKILL.md:51` (104), `:145` (101), `:190` (103), and
   the `new-features.py` docstring `:12` (123). The `bug-sheet-template.md:8` link line is
   unbreakable and acceptable. Rewrap the others.
7. **nit**: `scripts/__pycache__/coverage-map.cpython-312.pyc` (git-ignored, dated 09:47:11, before
   this review's runs) sits in the worktree. It does not ship. Delete it before the commit for a
   clean tree.

Checked and fine:
- `PICK_POINT` coordinate space: `D` is the `active-frame` document. `getBoundingClientRect()` and
  `D.elementFromPoint` both use that frame's viewport. The returned point adds the same `BASE` as
  `box()` (`qa.mjs:246-247`), so it is in window coordinates for `page.mouse.click`. The block is
  scrolled to the centre first. `el.contains(hit)` rejects points covered by the toolbar or the
  sticky headings. A `null` result is counted as skipped and not tried.
- Re-enter edit mode: `setEditMode(ctx, true)` after the return. The baseline is untouched, which
  is right: a navigation does not change the buffer.
- `coverage-map.py`: `Revision:` precedence and the fallback order are correct, and a non-ancestor
  sha is reported and skipped.
- Item 6: the Currently / Expected block is in both templates, with rules for an image, an
  annotated shot, a diff pair, and "no visual". The limit is 2 JPEGs at about 1000 px in
  `SKILL.md:189-191`, `charters.md` and the template. No "1 JPEG", "one JPEG" or "one evidence"
  is left. The triage copy into `01-intent.md` is in `SKILL.md:162-164` and the template `:26-27`.
  The charter prompt asks for both shots, and both FINDING return formats carry the two paths.
- Item 7: the `[!NOTE]` in `bug-sheet-template.md:6-9`. The link
  `../../../../skills/writing-for-markdown-okf-schema-studio/SKILL.md` resolves. There is one line
  in SKILL.md Report.
- (a) `admon.md` holds the NOTE alert with its lazy line, a blank line, then a plain blockquote with
  the same lazy line, matching the archived c3-1 fixture text.
- The docs match the script flags: coverage-map `--since/--campaign`, new-features
  `--since/--campaign/--repo/--json-file/--dry-run`, setup-workspace env vars, `--force` and
  `--clone`. Relative links resolve.
- Scope: `git status` shows changes only under `.agents/skills/markdown-studio-exploratory-qa-claude/`.

## Gates (re-run by the Inspector)

| Gate | Result |
| --- | --- |
| `bash -n scripts/setup-workspace.sh` | OK |
| `PYTHONPYCACHEPREFIX=… python3 -m py_compile` coverage-map.py, new-features.py, fmt-probe.py, assets/synth/ux25-export.py | OK |
| `node --check` qa, engine, noop-sweep, flicker-probe, probe-blocks, filmstrip, latency-probe, observe `.mjs`, spy/extension.js | all OK |
| JSON parse of `scenarios/*.json` | 22/22 OK |
| Scenario `file` fields against a freshly built workspace | all resolve |
| noop-sweep live run | Not run (VS Code not allowed); finding 1 comes from the source |

## Dry-run outputs (verbatim)

`python3 scripts/coverage-map.py --campaign <main>/.agents/changes/04-archives/210-qa-campaign-2026-10-31`
(from the Baseline line on):

```text
## Baseline: b9118506 from /Users/az02065/Projects/DevTools/markdown-okf-schema-studio/.agents/changes/04-archives/210-qa-campaign-2026-10-31 (--campaign)
## Changes since b9118506 (0 commits)
product sources: unchanged
areas without product changes (lower priority unless never explored): A1 A2 A3 A4 A5 B1 B2 B3 B4 B6 C1 C2 C3 C4 D1 D2 D3 D4 D5 D6 D7 E1 E2 E3 E4 E5 F1 F2 F3
```

`python3 scripts/new-features.py --campaign <same>` (rc 0):

```text
<!-- baseline: 2026-10-30, revision b9118506, source: /Users/az02065/Projects/DevTools/markdown-okf-schema-studio/.agents/changes/04-archives/210-qa-campaign-2026-10-31 (--campaign) -->
<!-- already in b9118506: #236 (merge commit is an ancestor); #234 (merge commit is an ancestor); #233 (merge commit is an ancestor); #232 (merge commit is an ancestor); #231 (merge commit is an ancestor); #230 (merge commit is an ancestor); #228 (merged before the revision was committed) -->

### New-feature coverage (0 PR(s) merged since 2026-10-30)

| PR | Feature | Charter | Result |
| --- | --- | --- | --- |
| (none) | | | |

Charter: charter ID, or `automated: <test>`. Result: PASS / finding IDs / not run.
A user-facing PR left at TODO is a gap: list it under Limits; status cannot be `completed`.
```

`QA_ROOT=/private/tmp/claude-502/cr211-driver/insp2 bash scripts/setup-workspace.sh` (VAULT_DIR
unset, rc 0; `insp2` deleted afterwards):

```text
Corpora:
  book: /Users/az02065/Projects/Nestor/agentic-coding-white-paper/book -> book/
  visual: /Users/az02065/Projects/DevTools/markdown-okf-schema-studio-wt-211/test/visual/fixtures -> fixtures-visual/
  docs: /Users/az02065/Projects/DevTools/markdown-okf-schema-studio-wt-211/docs -> docs/
  fixtures-qa: /Users/az02065/Projects/DevTools/markdown-okf-schema-studio-wt-211/.agents/skills/markdown-studio-exploratory-qa/assets/fixtures -> fixtures-qa/
  synth: /Users/az02065/Projects/DevTools/markdown-okf-schema-studio-wt-211/.agents/skills/markdown-studio-exploratory-qa-claude/assets/synth -> synth/
  vault: skipped (not set)
Workspace ready: /private/tmp/claude-502/cr211-driver/insp2/ws (193 Markdown files)
```

The Inspector added no file to the worktree. The pre-existing ignored `__pycache__` is left as
found (finding 7).
