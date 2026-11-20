# CR-432 verification

Head: cb618b15a6eb668929001f964cb091aeb7511e05
Base: cdf286fe0ac649a300de63c789895092665cad86 (origin/main)
PR: https://github.com/gsemet/markdown-okf-schema-studio/pull/443 (draft, head cb618b15)

Verdict: VERIFIED (second pass at the same head: the code claims are carried from the first pass
at cb618b1, no move since; the posted PR description, which failed then, now holds; see the last
section).

Logs of my runs: `work/verifier/newtests.log`, `work/verifier/requirements-lint.log`,
`work/verifier/heavy-integration.log`, `work/verifier/heavy-visual.log`. Before/after:
`work/verifier/evidence/before-after.md`.

## Move and carry

- **Clean rebase, patch unchanged** (judged at cb618b1).
  `git show <c> | git patch-id --verbatim` on e788cff~2..e788cff and cdf286fe..HEAD:
  `6f3881b7... a4110666` = `6f3881b7... 834eee57`; `763298d0... e788cfff` = `763298d0... cb618b15`.
  `git diff --name-only 36240e0f cdf286fe` (old base to new base): `.agents/guidelines/release-process.guidelines.md`
  only, which no proof runs. CLI log: `driver carry head=cb618b15... base=cdf286fe... gate_from=e788cfff...`.
- **Long gate** (carried from e788cff: clean rebase, same patch-ids, base delta is one guideline
  file). Gate log `work/gates/20261120-151303.log`, first line:
  `gate CR-432 branch chantier/batch-06/cr-432-list-items-get-reorder-handles-on-the-le head e788cfffcf7c1c58d2731e3d953e0125082d5a82`,
  `$ just preflight`, last line `result: pass at e788cfffcf7c1c58d2731e3d953e0125082d5a82`
  (static stage on Windows; visual, integration run in CI below).

## Claims

1. **The text module moves an item, per spec A (markers, nesting, gaps, numbering, content column,
   quote prefix, CRLF, refusals)**: VERIFIED at cb618b1.
   `fnm exec -- npm.cmd run compile` (exit 0), then
   `fnm exec -- node --import ./scripts/register-myst-patches.mjs --test --test-reporter=spec out/test/page/modules/listItemMove.test.js out/test/page/runtimeListItemMove.test.js out/test/session/listItemRange.test.js out/test/core/preview/listItemHandleStyles.test.js`
   -> exit 0, `tests 28, pass 28, fail 0`. The module's 10 tests include
   `an ordered list keeps its numbers in order from its first number and each item its delimiter`,
   `a marker that grows from 9. to 10. indents the item's continuation lines; the nesting stays`,
   `a list in a quote keeps its prefix on every line, blank quote lines included`,
   `CRLF line endings and a source without a final line break are kept`,
   `a source that does not read as the rendered items, or a move out of range, is refused`.
2. **Precondition: list items in a quote, an alert and admonitions carry their lines; the list range
   is the list's own** (spec B): VERIFIED at cb618b1, same run:
   `✔ the items of a list in a quote, an alert and admonitions carry their lines and the list range is the list's own`.
3. **Page feature: handles (all items, none for one-item / included / properties lists), placement
   left of the outermost container, push, drag, drop refusals, Alt+Up/Down with ends and repeat,
   one open and one final save, busy refusals, click opens no editor, one box read per pass**:
   VERIFIED at cb618b1, same run, 13 tests of `runtimeListItemMove.test.js` all `✔` (names in
   `work/verifier/newtests.log`).
4. **Styles scoped to edit mode, push rule, theme colours** (spec C): VERIFIED at cb618b1, same run,
   4 tests of `listItemHandleStyles.test.js` all `✔`.
5. **Wiring as spec B** (refresh in `applyEditMode`, `reposition`, `receiveSource`, click skip,
   `listRange`, shared `quotePrefixOf`): VERIFIED at cb618b1.
   `git diff cdf286fe..HEAD -- src/page/features/editMode.ts src/page/features/blockSourceEditor.ts src/page/features/pageInput.ts src/page/runtime.ts src/page/modules/tableInContainer.ts src/page/features/mappedBlocks.ts`
   shows `rt.listItemMove.refresh();`, `rt.listItemMove?.reposition();`,
   `if (rt.listItemMove.receiveSource(message)) return;`,
   `|| event.target.closest("[data-okf-list-item-handle]")`, `function listRange(list: Element)`,
   `export function quotePrefixOf(text: string)`. Handle attributes in
   `src/page/features/listItemMove.ts`: `aria-label "Move list item"` (l.301),
   `title "Drag to move item (Alt+Up, Alt+Down)"` (l.302), class
   `okf-list-editor-handle okf-list-item-handle` (l.298), `MOVE_TIMEOUT_MS = 5000` (l.20).
6. **The new tests fail on the previous code**: VERIFIED at cb618b1 (static). At the base:
   `git cat-file -e cdf286fe:src/page/modules/listItemMove.ts` -> absent;
   `...:src/page/features/listItemMove.ts` -> absent;
   `git grep -c -E 'listRange|LIST_ITEM_HANDLES_CSS|listItemMove' cdf286fe -- src` -> 0 files. The
   tests import `moveListItem`, call `blocks.listRange(...)` and read `LIST_ITEM_HANDLES_CSS`, which
   do not exist there. Not run at the base (no base worktree, see before-after.md).
7. **Real window (Linux)**: VERIFIED at cb618b1. `gh run view 44756125693 --json headSha,conclusion,event,jobs`
   -> `headSha cb618b15...`, `conclusion success`, `event workflow_dispatch`, `integration success`,
   `stress success`. Job log (`work/verifier/heavy-integration.log`, l.1457-1462):
   `PASS list item moves: an ordered item dragged, renumbered, one undo restores it`,
   `PASS list item moves: an item with a sub-list moves whole`,
   `PASS list item moves: an item of a GitHub alert keeps the alert's lines`,
   `PASS list item moves: a drop over another list moves nothing`,
   `PASS list item moves: Alt+Down on a handle, and the whole-list chord in an item editor`.
   **macOS (the Alt chord) not run**: `grep -n -i 'macos\|runs-on' .github/workflows/*.yml` lists only
   `ubuntu-latest` and `windows-latest`; the spec's "and macOS for the Alt chord" has no runner.
8. **Visual scenarios v36-v41 (light, dark, cream, 360 px push, held drag)**: VERIFIED at cb618b1.
   Visual job log of run 44756125693 (`work/verifier/heavy-visual.log`): `passed: block-editing/v36-list-item-handles-light-900`,
   `v37-...-dark-900`, `v38-...-cream-900`, `v39-list-item-handles-pushed-light-360`,
   `v40-list-item-drag-light-900`, `v41-list-item-drag-dark-900`, then `ci-visual: passed`.
   Images opened: handles left of markers, container handles left of the outermost box, the
   pushed 360 px page, the dimmed item and drop line; no path or username shows.
9. **PR checks green**: VERIFIED at cb618b1. `gh pr checks 443`: checks, report, static,
   static-windows, visual `pass`; the rest `skipping` by design. `gh pr view 443 --json headRefOid`
   -> `cb618b15a6eb668929001f964cb091aeb7511e05`.
10. **Requirements: SwRS-MDOKFSTUDIO-BLOCK-262 added, StRS-MDOKFSTUDIO-BLOCK-014 amended, markers**:
    VERIFIED at cb618b1. `just requirements-lint` -> exit 0, `1167 requirements, 0 errors, 26 warnings`
    (none on BLOCK-262: `grep -c BLOCK-262` on the log -> 0), `main paths: 92 StRS checked, 581 SwRS citations, all valid`,
    `use case diagrams: 93 StRS checked, all parse`; tree clean after (`git status --short` empty).
    `just check-markers` -> exit 0, `406 in-force SwRS marked`. Diff of StRS-014 adds the list-item
    intent, constraint and `Path 3: Move a list item` citing BLOCK-262; BLOCK-130 gains only the
    generated `tested_in_files: test/integration/listItemMoves.ts` line (its text unchanged).
11. **Docs, glossary, changelog** (spec E): VERIFIED at cb618b1, `git diff cdf286fe..HEAD -- CHANGELOG.md docs/user/editing.md .agents/glossary/common.md`:
    one line under `## Unreleased`, a paragraph in `docs/user/editing.md`, a "List item handle"
    entry in alphabetical order (after "List item editor").
12. **Before/after evidence**: captured at cdf286f / cb618b1, see `work/verifier/evidence/before-after.md`
    (two pairs, light and dark, plus five after-only captures). Not captured: the before of the new
    fixture (the base worktree failed on a Windows path length, exact error in before-after.md) and an
    ordered list before/after a move as a screenshot (no visual scenario does it).
13. **Known flake**: `test/session/previewManager.test.ts:162` was not seen in my runs (I ran only
    the CR's tests, not the full unit suite).

## The PR description, first pass (superseded by the second pass below)

- **Impacts**: FAILED at cb618b1. It reads "Before and after screenshots: to come from the visual
  run." The project rule (pull-request.guidelines.md, "Impacts holds the evidence of the change ...
  the Verifier fails a body whose Impacts has neither") needs the screenshots or "No visual change".
  The captures are in `work/verifier/evidence/` (push them as the guideline's "Screenshots in the PR" says).
- **Known gaps**: FAILED at cb618b1. The bullet "The visual and real-window scenarios have not run
  yet ..." is stale: both ran and passed at cb618b1 (claims 7 and 8). Missing bullets: the macOS
  real-window run of the Alt chord did not run (no macOS runner, claim 7); the screenshots of an
  ordered list before and after a move, and the "before" of lists in alerts and admonitions, were
  not captured (before-after.md, "Not captured").
- **Proof SHAs**: FAILED at cb618b1. The Test plan's "Local gates: `just check` (4138 tests ...),
  `just requirements-lint` ..., `just check-markers` ..." names no SHA (they ran at cb618b1, logs
  `work/gates/prepush2-*.log`; the long gate is at cb618b1 carried from e788cff).
- Summary, Deliverables (flowchart and `moveListItem` sketch: names exist in the diff), Changes and
  Blast radius match the diff at cb618b1: no claimed change missing, no delivered source change
  unmentioned (the visual and integration test files are named in the Test plan). No internal
  reference outside the body text's allowed places; no image attached yet. The zero-padded
  ordered-list gap is a stated gap, not a claim.
- Review box: unchecked "Review", no SHA claimed; the CLI log has `r2 approved at a41106664..., committed as e788cfff...`,
  so the box can cite `e788cff` carried to cb618b1.

## Second pass at cb618b1: the PR description only

No move: `git rev-parse HEAD` in the worktree -> `cb618b15a6eb668929001f964cb091aeb7511e05`, and
`gh pr view 443 --json headRefOid` -> the same SHA. Claims 1-13 above are carried from cb618b1
(same head, nothing re-run: only `work/pr-body.md` and the posted body changed). Judged again: the
three failed items of the first pass, and the body as a whole.

- **Posted body = work/pr-body.md**: `gh pr view 443 --json body -q .body` diffed against
  `work/pr-body.md` (CR stripped) -> one difference only, `125a126 > ` (a final blank line).
  `grep -c -i -E` for the machine's login name, `C:\Users` and `/Users/` on the posted body -> `0`.
- **Impacts**: VERIFIED at cb618b1. It now holds the before/after table (before `cdf286f`, after
  `cb618b1`), the after-only table of the new test page and the 360 px capture: nine images at
  `https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/327ba52eaedec90c78c0e84feeae287b61b52d21/<name>.png`.
  `curl -s -o /dev/null -w '%{http_code} %{content_type} %{size_download}'` on each ->
  all nine `200 image/png` (before-bullet-list-light-900-cdf286f 300991, after-bullet-list-light-900-cb618b1 301690,
  before-ordered-list-dark-460-cdf286f 140379, after-ordered-list-dark-460-cb618b1 141436,
  after-handles-containers-light-900-cb618b1 123979, after-handles-containers-dark-900-cb618b1 125756,
  after-drag-held-light-900-cb618b1 127406, after-drag-held-dark-900-cb618b1 128352,
  after-handles-pushed-light-360-cb618b1 111357).
  Same images as captured: `git fetch origin chantier/batch-06/cr-432-list-items-get-reorder-handles-on-the-le-assets`,
  `git rev-parse FETCH_HEAD` -> `327ba52eaedec90c78c0e84feeae287b61b52d21`; `git ls-tree FETCH_HEAD`
  blob ids equal `git hash-object --no-filters` of each file of `work/verifier/evidence/` (9 of 9,
  e.g. `ba2e9e03...` after-bullet-list-light, `4349a57d...` before-ordered-list-dark), so each
  image is the one captured at the SHA its name gives (before-after.md: CI runs 44752621641 at
  cdf286f and 44756125693 at cb618b1).
  The look, all nine opened: each shows what its alt text and caption say (no handle before;
  six-dot handles left of each item after; the ordered "Run order" list with handles while an item
  editor stays as it was; bullet, ordered from 3 with nested sub-list, task, alert and nested
  admonition lists with the container handles left of the outermost box, light and dark; the held
  drag with the dimmed dashed item and the drop line under the third item, light and dark; the
  360 px pane with every handle inside). No local path, username or home folder shows in any.
- **Known gaps**: VERIFIED at cb618b1. The stale "have not run yet" bullet is gone; the bullets now
  are: the zero-padded ordered list; the macOS Alt+Up/Down run (no macOS runner, claim 7); no
  ordered-list before/after a move screenshot (before-after.md "Not captured"); no "before" of the
  new test page, which holds the lists in an alert and in admonitions (before-after.md "Not
  captured"). Every gap of claims 7 and 12 has its bullet; no `UNVERIFIED` claim, no `STALE` mark.
- **Proof SHAs**: VERIFIED at cb618b1. Test plan: "Local gates at `cb618b1`: `just check` (4138
  tests, 0 fail; site 101, 0 fail)" matches `work/gates/prepush2-check.log` (`tests 4138`,
  `fail 0`; `tests 101`, `fail 0`); "`just requirements-lint` (0 changes, 581 main path citations
  valid)" matches `prepush2-lint.log` (`0 files would change`, `581 SwRS citations, all valid`);
  "`just check-markers` (406 in-force SwRS marked)" matches `prepush2-markers.log`. These logs ran
  at cb618b1 per the CLI log note `before push at cb618b1: just check, just requirements-lint,
  just check-markers` (14:41:21Z, the carry to cb618b1 at 14:42:56Z). "`just preflight` at `cb618b1`
  (carried from `e788cff`)" matches the carry and gate above. "CI green at `cb618b1`" matches
  claims 7, 8 and 9.
- **Review box**: VERIFIED at cb618b1. "approved at `cb618b1` (carried from `e788cff`)":
  `$CHANTIER log CR-432` -> `r2 approved at a41106664..., committed as e788cfffcf7c1c58d2731e3d953e0125082d5a82`
  and `driver carry head=cb618b15... gate_from=e788cfff...` (clean rebase, same patch-ids, above).
- **Rest of the body**: carried from the first pass at cb618b1 (Summary, Deliverables, Changes and
  Blast radius match the diff; unchanged text). The screenshot branch name appears only under
  Internal references; no CR number elsewhere in the body text.

## Description pass at cb618b1 (closing step 2)

No move: `git rev-parse HEAD` in the worktree and `gh pr view 443 --json headRefOid` ->
`cb618b15a6eb668929001f964cb091aeb7511e05`. Code claims 1-13 carried from cb618b1 (same head, not
re-run). Posted body saved to `work/verifier/posted-body-desc-pass.log`.

- **Body unchanged since the second pass**: VERIFIED at cb618b1. `diff` of `work/pr-body.md`
  (CR stripped) against the posted body -> only `125a126 > ` (a final blank line).
- **Renders**: VERIFIED at cb618b1. `grep -c '^```'` -> 4 (two balanced fences: mermaid, ts);
  sections Summary .. Internal references in order, tables well formed; no fold used.
  The nine image URLs (assets commit `327ba52`, immutable) re-fetched with `curl -s -o /dev/null -w
  '%{http_code} %{content_type} %{size_download}'` -> all `200 image/png`, sizes equal to the second
  pass (300991 .. 111357), so the same blobs already matched to `work/verifier/evidence/` and given
  the look there (carried from the second pass at cb618b1: same commit, same bytes).
- **Matches the diff at cb618b1**: VERIFIED. `git diff --stat origin/main...HEAD` (34 files): every
  source file is named in Changes; tests and visual files in the Test plan; requirements (BLOCK-262
  new, StRS-014 amended, BLOCK-130 gains only the generated `tested_in_files` line, `log.md`) under
  Requirements and `just requirements-update`; docs, glossary, changelog named. Nothing claimed is
  missing from the diff.
- **Proof SHAs, Review box, Known gaps**: VERIFIED at cb618b1, unchanged text, judged in the second
  pass: Review `approved at cb618b1 (carried from e788cff)` against `$CHANTIER log CR-432`
  (`r2 approved at a41106664..., committed as e788cfff...`; `driver carry head=cb618b15...
  gate_from=e788cfff...`); Known gaps holds the four gaps of claims 7, 12 and before-after.md
  "Not captured"; no UNVERIFIED, no STALE.
- **No username or home folder; internal references**: VERIFIED at cb618b1.
  `grep -c -i -E "<login>|C:\Users|/Users/|/home/"` on the posted body -> `0`.
  `grep -n -i -E "CR-?[0-9]|chantier|driver|verifier|inspector|coder|foreman|batch"` -> lines 124
  and 125 only, both under `## Internal references`.

Verdict of the description pass: VERIFIED at cb618b15a6eb668929001f964cb091aeb7511e05.
