# Grill advisor report: batch of nine change requests, ending with release 1.7.2

Date: 2026-11-12. Read-only review. Code read at `origin/main` (`cb968299 chore: version 1.7.1`).

## Facts to know before the batch starts

- The local `main` checkout is **4 commits behind `origin/main`** (it still says version 1.7.0;
  `origin/main` is 1.7.1). Every worktree must be cut from `origin/main`, and the guidelines read
  there.
- The version is computed by Commitizen (`just bump-version`): a single `feat:` commit in the batch
  gives **1.8.0**, not 1.7.2. For 1.7.2 every commit must be `fix:`, `ci:`, `docs:`, `test:` or
  `chore:`, or the release uses `just version 1.7.2`.
- Probes: I compiled a copy of `origin/main` in the scratchpad and ran the render pipeline and the
  HTML export builder on small inputs. Results are quoted in the CRs below. Nothing was run in the
  repository, and nothing was run in a real VS Code window.
- No GitHub issue is open, so no CR of this batch closes one (`gh issue list` returned nothing).

## Premise check, in short

| CR | Premise | Verdict |
| --- | --- | --- |
| changelog-line-in-each-pr | three doc gaps | True. No guideline or template asks a PR for its changelog line today. |
| ci-integration-locked-screen | no lock check before the run | True. The lock state is only read for failure messages (`test/integration/macWindow.ts:45`). |
| publish-to-open-vsx | no Open VSX step | True. `ovsx` is not a dependency; `release.yml` publishes to the Marketplace only. One stale line: "publish 1.3.0 by hand". |
| export-html-drops-block-being-edited | "the block being edited is missing" | **Partly wrong.** A block under the block editor is exported (its last rendered state). The content that is lost is the **table cell** under the cell editor. |
| cmd-s-from-preview-focus | Cmd+S does nothing in the preview | Plausible from the code (no key binding, `documents.save` port never called). Not reproduced in a window. |
| alert-followed-by-heading-taken-as-title | heading becomes the title | True, reproduced. The same happens with a lone bold first line. |
| card-in-blockquote-line-offset | "every" line one too early | **Narrower than written.** Reproduced only for a quoted grid whose body starts with a blank `>` line. A quoted `{card}` alone maps correctly. |
| sticky-heading-long-title-wraps | long title wraps | True, and wrapping is the specified behaviour today (SwRS TOOLBAR-025, visual scenario v05). The CR changes a requirement, it does not fix a deviation. |
| ci-report-object-object-message | `[object Object]` | True on main. PR 321 (the eval) is **closed, not merged**; its diff is a ready model. |

No CR is already fixed on main. No CR should be dropped. Two need their intent rewritten before the
specification (export, card).

---

## 1. changelog-line-in-each-pr

Decisions already taken (02-answers): one CR for the three fixes; the changelog line is required by
the documents (lifecycle guideline and a PR template checkbox), not by a CI check.

Code and rules read: `.agents/guidelines/release-process.guidelines.md` (steps 2, 6, 8),
`.agents/guidelines/change-requests-lifecycle.guidelines.md` (lifecycle table step 8, "Release
driver"), `.github/PULL_REQUEST_TEMPLATE.md`, CONTRIBUTING "How to Release" step 2,
`test/build/test_guideline_isolation.py`, the v1.7.1 retro.

| # | Question | Tag | Recommended answer | Reason |
| --- | --- | --- | --- | --- |
| 1 | Which PRs owe a line? | INTERNAL | Every PR with a `feat` or `fix` commit; `test`, `ci`, `build`, `docs`, `chore` PRs tick the box with "No user-facing change". | Same rule as CONTRIBUTING step 2 ("one user-facing line for every `feat` and `fix` commit ... test, CI, build and documentation commits get none"). |
| 2 | Where does the template ask for it? | INTERNAL | One checkbox in "Test plan": `- [ ] Changelog: one user-facing line under ## Unreleased <!-- or "No user-facing change" -->`. No new section. | CI rule 10 lists the template sections by name; a checkbox keeps that list true. |
| 3 | Where does the lifecycle guideline ask for it? | INTERNAL | Step 5 (the coder writes the line with the change), step 6 (the Inspector checks it), step 8 (the PR body check). | The line belongs to the round's diff so the Inspector sees it; step 8 already holds the body check. |
| 4 | Does CONTRIBUTING step 2 change? | INTERNAL | Keep it as the release's safety net; change "add the missing ones in the release branch" to say a missing line is a gap of its PR, added by a fix PR before the version commit. | Release step 2 already says the lines are in `main` before the heavy run. |
| 5 | Where does the line go in `## Unreleased`? | INTERNAL | Appended at the end of the list. A conflict on it keeps both lines. | Every PR of a stack touches the same block; one rule makes the conflict mechanical. |
| 6 | Step 6: what is the check of record? | INTERNAL | HTTP 200 on `https://marketplace.visualstudio.com/_apis/public/gallery/publishers/GaetanSemet/vsextensions/markdown-okf-schema-studio/X.Y.Z/vspackage`. The listing page is not checked. | Retro: the gallery served 1.7.1 while the listing still showed 1.7.0. |
| 7 | Step 6: what delay is written? | INTERNAL | "The listing page can lag by several minutes (more than 3 seen in 1.7.1); it is not a gate." No fixed number. | The retro has one data point, "still 1.7.0 after three minutes". |
| 8 | Step 8: wording for an empty list | INTERNAL | "No issue closed by this release: write that line in `report.md`; the step ends, no approval is asked." Mirror it in the lifecycle guideline's "Release driver" bullet "Lists". | Both documents describe step 8; one would contradict the other. |
| 9 | Role names in the release guideline | INTERNAL | None. Keep "the agent that runs the release" style. | `test_guideline_isolation.py` fails on "driver", "Foreman", "Chief of Staff" in a project guideline. |
| 10 | Does this batch follow the new rule? | INTERNAL | Yes. This CR goes first in the stack, and the eight others add their line in their own PR. | Otherwise 1.7.2 repeats the 1.7.1 deviation. |

- Files: `.agents/guidelines/release-process.guidelines.md`,
  `.agents/guidelines/change-requests-lifecycle.guidelines.md`, `.github/PULL_REQUEST_TEMPLATE.md`,
  `CONTRIBUTING.md` (step 2).
- Requirements: none (documents only; "No behaviour change").
- Size: S. Fits a quick batch.
- Risks: `test_guideline_isolation.py`; `just check` runs the Markdown format check on the guidelines.
- Depends on: nothing. The CRs 2 and 3 edit the same two release documents: stack them after it.

## 2. ci-integration-locked-screen

Decisions already taken: macOS only; `ci-integration` checks before the run and stops with the cause
and the two ways out; in `preflight`, `ci-report` and `ci-gallery` say they are skipped because
integration did not run; the release procedure says to dispatch the branch heavy run at once.

Code read: `justfile` (`ci-integration` 272, `ci-stress` 316, `preflight` 386),
`test/integration/macWindow.ts:45` (the lock test already exists:
`ioreg -n Root -d1` matched against `"CGSSessionScreenIsLocked" = Yes`),
`test/build/test_workflows.py:214` (text test of the `preflight` recipe),
`.agents/guidelines/local-worktree.guidelines.md` ("app-window tests then fail fast", which is not
true today), CI rules 7 and 8.

| # | Question | Tag | Recommended answer | Reason |
| --- | --- | --- | --- | --- |
| 1 | How is the lock detected? | INTERNAL | The same `ioreg` test as `macWindow.ts`, in a private justfile recipe (`_require-unlocked-screen`), no new dependency. | One existing, proven probe; a justfile recipe keeps CI rule 2 (the target runs locally as in CI). |
| 2 | Where in `ci-integration`? | INTERNAL | First line, before `e2e-campaign.mjs begin integration`. | `begin` deletes the previous integration manifest, `review.json` and `e2e-manifest.json`; a refused run must not erase evidence. |
| 3 | How does `preflight` know the cause? | INTERNAL | `ci-integration` exits with a dedicated code (3) on a locked screen. `preflight` then prints "ci-report: skipped, integration did not run (screen locked)" and the same for `ci-gallery`, runs neither, and still exits 1. | Constitution 4: a change is complete only when preflight passes, so a locked screen cannot turn preflight green. |
| 4 | Does `ci-stress` get the check? | INTERNAL | Yes, same recipe. `just integration` and `just e2e` too if it costs one line each. | Same failure, same 20 minutes lost. |
| 5 | Early notice in `preflight`? | INTERNAL | Yes: one warning line at the start when the screen is already locked, without stopping. | Static and visual take minutes before integration; the developer can unlock meanwhile. |
| 6 | How is it tested? | INTERNAL | An override `STUDIO_SCREEN_LOCKED=1` read by the recipe on any OS; a test in `test/build/test_workflows.py` runs `just ci-integration` with it and asserts exit code 3, the cause, both ways out, and that no campaign file was written. Plus a text test of the `preflight` skip lines. | The CI runners are Linux; without the override the path is never run in CI (constitution 3). |
| 7 | A screen that locks during the run | INTERNAL | Out of scope: the message names `caffeinate` as in the worktree guideline. | The guideline already covers it. |
| 8 | Requirement | INTERNAL | None: developer tooling, not extension behaviour. Write "No behaviour change" in the PR. | No SwRS covers `preflight` or the `ci-*` targets (`grep` on `requirements/tiers` finds only log entries). |
| 9 | Which documents change? | INTERNAL | Release guideline step 5 and CONTRIBUTING step 4 (locked screen: dispatch `gh workflow run ci.yml --ref <branch> -f heavy=true` at once and go on); the worktree guideline sentence stays, now true. | Decision 2 of the answers. |

- Files: `justfile`, `test/build/test_workflows.py`,
  `.agents/guidelines/release-process.guidelines.md`, `CONTRIBUTING.md`; maybe
  `.agents/guidelines/ci.guidelines.md` (one line under rule 8).
- Requirements: none.
- Size: S to M. Fits.
- Risks: `just format` rewrites the justfile; the Windows branch of `preflight` and its test must
  stay as they are; the exit code 3 must not leak into the CI job (Linux never takes the path).
- Depends on: CR 1 (same two release documents). No overlap with CR 9 if `e2e-campaign.mjs` is left
  alone, as recommended.

## 3. publish-to-open-vsx

Code read: `.github/workflows/release.yml` (steps "Verify Marketplace token", "Publish to VS Code
Marketplace" with `npx --no-install vsce publish --skip-duplicate`, then "Attach VSIX and images"),
`test/build/test_workflows.py:197` (order assertions, tagged SwRS CORE-078), CONTRIBUTING "GitHub
Configuration" and "Recovery", `package.json` (`publisher: GaetanSemet`, `engines.vscode ^1.95.0`,
no `enabledApiProposals`, `@vscode/vsce` is a devDependency, no `ovsx`).

| # | Question | Tag | Recommended answer | Reason |
| --- | --- | --- | --- | --- |
| 1 | Is the owner's setup done before the release CR starts? (Eclipse account, signed Publisher Agreement, `ovsx create-namespace GaetanSemet`, token, `OVSX_PAT` secret in the `release` environment) | **USER-IMPACT** | Ask the owner now. Without it, 1.7.2 is not on Open VSX, and the notes must not announce it. | Only the owner can create the account, sign the agreement and store the secret. `ovsx publish` fails on an unknown namespace. |
| 2 | Missing `OVSX_PAT`: fail or skip? | **USER-IMPACT** | Skip with a `::warning::` and a line in the job summary. A failed `ovsx publish` with the secret present fails the job. | The step must not block a release while the owner's setup is pending; a present secret means the owner expects the publication. |
| 3 | Where is the step? | INTERNAL | Last, after "Attach VSIX and images to GitHub release". | The intent says "after the Marketplace step". After the GitHub release, an Open VSX outage cannot leave a tag without its release. A re-run is safe: `vsce --skip-duplicate`, `ovsx --skip-duplicate`. |
| 4 | Which tool? | INTERNAL | `ovsx` as a pinned devDependency, run as `npx --no-install ovsx publish --skip-duplicate --packagePath <the same VSIX>` with the token in the `OVSX_PAT` environment variable. No third-party action. | Same pattern as `vsce`; the job holds publish secrets and runs `npm ci --ignore-scripts`. Constitution 5: the specification must say the dependency is allowed. |
| 5 | Which versions appear on Open VSX? | **USER-IMPACT** | 1.7.2 is the first. No backfill of older versions. Drop the "publish 1.3.0 by hand" line of the intent. | Open VSX users get the current version; a backfill needs the owner's token on a workstation for no user gain. |
| 6 | Does the README or the release notes name Open VSX? | **USER-IMPACT** | Release notes and thread of 1.7.2: yes, one line, only if question 1 is "done". README: one install line in a follow-up after the listing exists. | A README line ships inside the VSIX; if the first publication fails it points to a missing page. |
| 7 | Cursor compatibility report: where? | INTERNAL | A new backlog item written by this CR (`cursor-compatibility`), with what was checked from the code: `engines.vscode ^1.95.0`, no proposed API, a webview panel plus a custom text editor. An install test in Cursor is listed there as open. No fix in this CR. | The intent says "report the gaps; do not fix them in this CR". Nobody can prove Cursor behaviour without Cursor installed. |
| 8 | Requirement | INTERNAL | A new SwRS with `okfreq new` in `rendering-core`, next to CORE-076 and CORE-078, with the same annotation exemption; tests in `test_workflows.py` (step order, `--skip-duplicate`, secret only in `env`, skip when the secret is empty). | CORE-078 already pins the release job's step order; the release workflow is specified there. |
| 9 | Release procedure | INTERNAL | Release guideline step 6 and CONTRIBUTING step 6, "GitHub Configuration" and "Recovery" name the step, the secret, and the check of record `https://open-vsx.org/api/GaetanSemet/markdown-okf-schema-studio/X.Y.Z`. | The intent asks for CONTRIBUTING; step 6 is where the release is monitored. |
| 10 | Commit type | INTERNAL | `ci:`. | `feat:` would make the release 1.8.0. |

- Files: `.github/workflows/release.yml`, `package.json`, `package-lock.json`,
  `test/build/test_workflows.py`, `CONTRIBUTING.md`,
  `.agents/guidelines/release-process.guidelines.md`, a new SwRS and the generated
  `requirements/tiers/swrs/rendering-core/index.md`, `requirements/tiers/log.md`, a new backlog item.
- Size: M. Fits, with one condition: the workflow change cannot be proven before the release itself
  (the step runs only on a tag). The first real run is 1.7.2.
- Risks: `just audit` and the security floors on the new dependency tree (`package.json`
  `overrides`); the Open VSX namespace must equal the `publisher` field; a red release job on the
  first run (the release rule then re-runs once and calls the owner).
- Depends on: CR 1 and CR 2 for the shared documents. Independent of the product CRs.

## 4. export-html-drops-block-being-edited

Code read: `src/page/modules/exportSnapshot.ts` (`takeExportSnapshot` clones the content),
`src/core/export/exportContent.ts` (`REMOVED_BY_ATTRIBUTE`, `stripAttributes`),
`src/page/features/blockEditor.ts:270-292`, `src/page/features/editorChrome.ts:99-112`,
`SwRS-MDOKFSTUDIO-TOOLBAR-137` line 59 (the Known issue row), the CR 288 Inspector note
(`4-archives/288-export-single-html/work/inspector/T1-r1.md:85`).

What the code does:

- A block under the block editor stays in the page as a sibling of the editor frame, hidden by
  `data-sphinx-preview-editing="true"`. The export removes the frame and strips that attribute.
  Probe on `origin/main`:
  `<p data-sphinx-preview-editing="true">EDITED BLOCK</p>` + editor host exports as
  `<p>before</p><p>EDITED BLOCK</p><p>after</p>`. The block is **not** missing.
- The Inspector of CR 288 wrote that the frame host "wraps the block being edited". It wraps the
  editor frame (`edit.element`), not the block.
- A table cell under the cell editor is different: its content is moved into
  `<span data-sphinx-table-cell-content="true" aria-hidden="true">`, the export keeps that span and
  its attribute, and the exported style sheet still holds the rule
  `[data-sphinx-table-cell-content="true"] { height: 0; visibility: hidden }`. Probe: the cell is in
  the file but invisible.

| # | Question | Tag | Recommended answer | Reason |
| --- | --- | --- | --- | --- |
| 1 | First step | INTERNAL | Reproduce before any fix: a page-level test (`test/page/modules/exportSnapshot.test.ts`, real block editor and real cell editor open) fed to `buildHtmlExport`. Rewrite the intent from what it shows. | The recorded Known issue does not match the code for a block editor. |
| 2 | What does the file show for a block or cell being edited? | **USER-IMPACT** | The last rendered state, which is the text already autosaved to the document (about 400 ms behind the typing). The editor stays open and the export does not close or commit it. | The intent allows "its rendered content (or its last saved state)". Closing the editor on export would move the caret and the layout under the user. |
| 3 | Fix for the cell | INTERNAL | In `removeChrome` (host side, `exportContent.ts`): unwrap the `data-sphinx-table-cell-content` span, as find marks are unwrapped. | The rule "editing chrome is left out" lives there; the page snapshot stays a plain clone. |
| 4 | Other editors to check in the same test | INTERNAL | Front matter value editor, a block editor opened inside a card, a `{list-table}` edited as raw Markdown (`blockSourceEditor.ts:119`). | Each hides its target in its own way. |
| 5 | Requirement | INTERNAL | TOOLBAR-137: replace the Known issue row by the real behaviour (block and cell exported in their last rendered state), update the verification notes; log entry. If the block case is confirmed never broken, the log says the Known issue was wrong for blocks. | Constitution 1: the requirement describes what the code does. |
| 6 | Visual scenario | INTERNAL | One scenario in `test/visual/exportHtmlScenarios.ts` with a cell editor open. | The loss is visual (hidden by CSS), a DOM-only test would pass with the bug. |

- Files: `src/core/export/exportContent.ts`, `test/core/export/htmlExport.test.ts`,
  `test/page/modules/exportSnapshot.test.ts`, `test/visual/exportHtmlScenarios.ts`,
  `requirements/tiers/swrs/toolbar-navigation/SwRS-MDOKFSTUDIO-TOOLBAR-137.md`, `log.md`,
  `CHANGELOG.md`.
- Requirements: SwRS-MDOKFSTUDIO-TOOLBAR-137 (StRS-MDOKFSTUDIO-TOOLBAR-014 unchanged).
- Size: S to M. Fits.
- Risks: my probe used hand-written DOM, not a real page; the reproduction may show a third case.
- Depends on: nothing.

## 5. cmd-s-from-preview-focus

Code read: `package.json` `contributes.keybindings` (no save binding; the find binding shows the
`when` pattern `activeWebviewPanelId == 'markdown-okf-schema-studio.preview'`),
`src/host-vscode/activation.ts` (two hosts: the side panel `PANEL_VIEW_TYPE` and the custom text
editor `EDITOR_VIEW_TYPE`), `src/host-api/documentStore.ts:107` and
`src/host-vscode/documents.ts:156` (`save(document)` exists and nothing calls it),
`src/session/previewManager.ts:214` (`runEditCommand`, the model for a command routed to the focused
preview), `src/page/features/blockEditor.ts:400` (`flushPendingAutosave`), SwRS BLOCK-003 (keys that
reach VS Code from the preview).

| # | Question | Tag | Recommended answer | Reason |
| --- | --- | --- | --- | --- |
| 1 | What does Cmd+S (Ctrl+S) do with the focus in the preview? | **USER-IMPACT** | It saves the Markdown document the preview shows, as in the source editor. | The preview edits that document; a second, hidden step to save it is the defect reported. |
| 2 | What happens to an open block or cell editor? | **USER-IMPACT** | It stays open with its caret; the text typed so far is written to the document first, then the document is saved. | Same as Cmd+S in a text editor: save does not end the editing. |
| 3 | Is the command in the Command Palette? | **USER-IMPACT** | No (hidden, like `editUndo`). The key binding can be rebound in Keyboard Shortcuts. | "File: Save" already exists in the palette; a second save command would confuse. |
| 4 | Which previews? | INTERNAL | The side panel (`activeWebviewPanelId`). The custom editor is checked in a real window first: VS Code saves a custom text editor natively; bind it only if the test shows it does not. | `resolveCustomTextEditor` gives VS Code the document; a second binding could save twice. |
| 5 | Order of operations | INTERNAL | Host command, message to the page, the page flushes its pending autosave, the page asks the host to save, the host calls `documents.save`. | A direct host save would run before the 400 ms autosave and leave the document dirty again. |
| 6 | Format on save and other save participants | INTERNAL | They run, as with any save; the preview takes the result as an external change, as today. State it in the SwRS. | `TextDocument.save()` runs the participants; nothing to add. |
| 7 | Untitled document | INTERNAL | `save()` opens VS Code's Save As dialog; nothing special. | VS Code behaviour. |
| 8 | Requirement | INTERNAL | A new SwRS with `okfreq new`, scope `lifecycle-sync`, citing BLOCK-003 for the key path; `@implements_req` at the command and the page handler. | No SwRS covers saving today. |
| 9 | Proof | INTERNAL | Unit and session tests on the memory host for the order of question 5, plus one real-window scenario (the key reaches the binding and the dirty mark goes). | A key binding with a `when` clause cannot be proven outside a window (BLOCK-003 is proven the same way). |
| 10 | Commit type | INTERNAL | `fix:`. | The save key was expected to work; `feat:` would give 1.8.0. |

- Files: `package.json`, `src/host-vscode/activation.ts`, `src/session/previewManager.ts` and the
  session of a preview, `src/host-api/` (message types), `src/page/features/hostHandlers.ts`,
  `src/page/features/blockEditor.ts`, tests in `test/session`, `test/page`, `test/integration`, a new
  SwRS, `log.md`, `CHANGELOG.md`.
- Size: M. It is the largest product CR of the batch and the only one that needs a real-window test;
  the pull request runs only the simulated jobs, so its proof is an on-demand heavy run on the branch.
- Risks: the binding must not fire in the find field in a harmful way (it should still save); a
  double save in the custom editor; `check-settings` and the unused-export check on the new command.
- Depends on: nothing. Put it last in the stack so it can be left out without restacking.

## 6. alert-followed-by-heading-taken-as-title

Code read: `src/core/render/mystGithubAlerts.ts` (the alert becomes `:::{note}` + `:class: simple`,
and `alertLines` records where), `src/core/directives/admonition.ts:40-48` and
`src/core/render/mystNode.ts:115` (`takeAdmonitionTitle`: a leading heading **or a lone bold
paragraph** becomes the title when the directive has no argument), SwRS MYST-005 and MYST-001
(this shortcut is specified for MyST admonitions), SwRS GFM-009 (alerts).

Probe on `origin/main`: `> [!NOTE]`, `> # h`, `> b` gives one admonition, lines 1-3, with no
heading in the body; `> [!NOTE]`, `> **Bold first**`, blank, `> b` behaves the same.

| # | Question | Tag | Recommended answer | Reason |
| --- | --- | --- | --- | --- |
| 1 | Keep the title shortcut on GitHub alerts, or match GitHub? | **USER-IMPACT** | Match GitHub for alerts written as `> [!NOTE]`: the title is the default ("Note"), or the text after the marker (`> [!NOTE] My title`, which stays); the heading stays a heading in the body. | An alert is GitHub syntax and the document is also read on GitHub; the alert has its own title form already. |
| 2 | Does the same apply to a lone bold first line (`> **Bold**`)? | **USER-IMPACT** | Yes: it stays a bold paragraph in the body. | Same code path, same difference with GitHub; fixing only the heading leaves half the gap. |
| 3 | MyST admonitions (`:::{note}`) and Quarto callouts | **USER-IMPACT** | Unchanged: a leading heading or bold line is still the title. | Specified in MYST-005 and MYST-001; it is a MyST habit, not a GitHub one. |
| 4 | Legacy `> **Note**` bold-marker alerts | INTERNAL | Same rule as `[!NOTE]` alerts. | Both go through `expandGithubAlertsWithLines`. |
| 5 | How does the renderer tell an alert from a directive? | INTERNAL | Mark the admonition nodes that come from an alert (the pass that maps `alertLines` back to the document) and skip `takeAdmonitionTitle` for them. | `alertLines` already identifies them; no change to the rewritten text, so the line mapping of GFM-009 is untouched. |
| 6 | The heading inside the alert: TOC, sticky band, folding | INTERNAL | Like any heading inside an admonition today: out of the TOC and the band (`BAND_EXCLUDED` in `stickyHeadings.ts`). Assert it in the test. | No new rule; the case exists with `:::{note} Title` + heading. |
| 7 | Is that heading editable as a block with the right line? | INTERNAL | Assert `data-line` of the heading (line 2 in the probe input). | A new mapped block appears where there was none. |
| 8 | Requirement and writing skill | INTERNAL | GFM-009: new scenario (leading heading, leading bold line). MYST-005: one boundary line saying alerts are excluded. The skill: check `SKILL.md` and `references/examples.md`; no example uses the shortcut in an alert, so probably no change, but the test that renders the examples decides. | Constitution 1 and 6. |
| 9 | Proof against GitHub | INTERNAL | A committed fixture of GitHub's HTML for the input, not a `gh api markdown` call in the test. | Tests do not use the network. |

- Files: `src/core/render/mystGithubAlerts.ts` or the tree pass that uses it,
  `src/core/directives/admonition.ts`, `test/core/render/mystFeatures.test.ts` (or a new alert test),
  `requirements/tiers/swrs/gfm/SwRS-MDOKFSTUDIO-GFM-009.md`,
  `requirements/tiers/swrs/myst/SwRS-MDOKFSTUDIO-MYST-005.md`, `log.md`, `CHANGELOG.md`.
- Size: S. Fits.
- Risks: a document that used the shortcut in an alert changes look (a heading appears inside the
  alert); visual baselines that contain such an alert.
- Depends on: nothing. Same area as CR 7 but different files.

## 7. card-in-blockquote-line-offset

Code read: `src/core/render/mystGridToctree.ts:90-101` (`rawBody`): when the source lines of the
directive are not plain fence lines, which is the case behind a `>` prefix, it falls back to
`node.value` and assumes the body starts on the line after the opener.

Probes on `origin/main`:

| Input | Result |
| --- | --- |
| `> :::{card} T` + body (colon or backtick fence, options, `^^^`/`+++`, nested quote, quote in a list, blank first body line) | Correct lines |
| `> ::::{grid} 2`, cards on the next line | Correct lines |
| `> ::::{grid} 2`, then a blank `>` line, then the cards | **Card, title and body one line too early** (card on source lines 3-5 is mapped 2-4) |
| The same grid unquoted | Correct |
| `> ::::{grid} 2`, `> :gutter: 2`, blank `>`, cards | Correct |

So the trigger is a quoted grid whose body starts with a blank quoted line: the parsed `value`
drops that line and the fallback does not know.

| # | Question | Tag | Recommended answer | Reason |
| --- | --- | --- | --- | --- |
| 1 | Scope | INTERNAL | Rewrite the intent to the reproduced case; the test table above becomes the render-level test, in `test/core/render/gridCardTitleSourceLine.test.ts`. | The intent says "every source line"; most cases are right. |
| 2 | Fix | INTERNAL | In `rawBody`: read the source lines through the quote prefix (strip the container's `>` prefix before the fence test), so the quoted case takes the same path as the unquoted one. | The unquoted path is right because it cuts the body from the source text. |
| 3 | Other containers with a prefix (a grid in a list item, a grid in an alert) | INTERNAL | Add them to the test; fix only what the same change covers. | Same fallback. |
| 4 | Requirement | INTERNAL | SwRS BLOCK-258 (source line of a card title) or BLOCK-257: one boundary row for the quoted grid. | The existing test file carries `@tests_req SwRS-MDOKFSTUDIO-BLOCK-258`. |
| 5 | What the user sees | INTERNAL | A click on such a card opens the editor on the card, not on the line above. One changelog line. | Bug fix with no choice to make. |

Found on the way, **not** for this batch: a `::::{grid}` inside a `> [!NOTE]` alert is cut. The
alert is rewritten as a three-colon `:::{note}` and the grid's inner `:::` closes it; the last `:::`
is shown as code. To file in the inbox.

- Files: `src/core/render/mystGridToctree.ts`, `test/core/render/gridCardTitleSourceLine.test.ts`,
  one SwRS of `block-editing`, `log.md`, `CHANGELOG.md`.
- Size: S. Fits.
- Risks: `mystGridToctree.ts` is 26.7 KB; check the 800-line ratchet before adding code.
- Depends on: nothing.

## 8. sticky-heading-long-title-wraps

Code read: `src/core/preview/styles/pageChromeStyles.ts:561-588` (the band: `white-space: pre-wrap;
overflow-wrap: anywhere; pointer-events: none`), `src/page/features/stickyHeadings.ts` (the band is
one text node, one line per level joined by `\n`; `refreshReadingOffset` takes the larger of an
allowance of `depth` lines and the tallest band seen), SwRS TOOLBAR-025 ("wrapping a long heading
path onto more lines", scenario "Long heading path wraps", scenario "Pointer"), SwRS TOOLBAR-030,
visual scenario `preview-sticky-headings-natural-growth` (v05) and fixture `10-sticky-heading-wrap`.

| # | Question | Tag | Recommended answer | Reason |
| --- | --- | --- | --- | --- |
| 1 | One line per level with an ellipsis, or keep wrapping and move the scroll offset? | **USER-IMPACT** | One line per heading level, cut with an ellipsis. The band is then never taller than the configured depth. | The reading-offset allowance is already computed as `depth` lines (`anchorPolicy.readingOffset(depth, lineHeight, 5)`): one line per level is what the scroll logic assumes. The other option touches the three-pass measure loop and the scroll stability rules of TOOLBAR-030. |
| 2 | Full title on hover? | **USER-IMPACT** | No. | The band ignores the pointer so clicks reach the text under it (TOOLBAR-025 "Pointer"); a tooltip needs the opposite. The full title is the heading itself and the table of contents. |
| 3 | How | INTERNAL | CSS only: `white-space: pre; overflow: hidden; text-overflow: ellipsis` on the band; the text node and its `\n` stay. | `text-overflow` cuts each line of a `pre` block; every test that reads the band text keeps working. |
| 4 | Existing assertions that change | INTERNAL | TOOLBAR-025 (normative sentence and the scenario "Long heading path wraps"), `test/core/preview/previewStyles.test.ts` (asserts `pre-wrap`), the v05 visual scenario (`expectStickyGrowth`) and its baseline. The PR says why each changes. | Constitution 3: say why when an assertion changes. |
| 5 | New visual test | INTERNAL | Depth 1, a long H1, 160 % zoom, Cream: the band is one line and the first line of the section is visible under it. Use an own fixture, not the demo branch file. | The intent's acceptance file lives on another branch. |
| 6 | Requirement | INTERNAL | TOOLBAR-025 changed in the same change; TOOLBAR-030 unchanged. Log entry. | Constitution 1. |

- Files: `src/core/preview/styles/pageChromeStyles.ts`, `test/core/preview/previewStyles.test.ts`,
  `test/visual/scenarioDefinitions2.ts`, one fixture, `test/visual/capture_final_checks.py` if it
  measures the band height from its lines,
  `requirements/tiers/swrs/toolbar-navigation/SwRS-MDOKFSTUDIO-TOOLBAR-025.md`, `log.md`,
  `CHANGELOG.md`.
- Size: S with the recommended answer. With "keep wrapping and move the offset" it is M to L and
  does not fit a quick batch.
- Risks: it reverses a behaviour that was specified and tested on purpose (v05 "natural growth"), so
  the owner's answer is needed; RTL headings and the ellipsis side.
- Depends on: nothing.

## 9. ci-report-object-object-message

Code read: `scripts/e2e-campaign.mjs` `stageFrom` (`manifest.failures.join("; ")`),
`test/visual/capture.py` (`Failure(scenario['page'], detail)`: objects with `page` and `detail`),
`test/site/e2eCampaign.test.ts`, SwRS CORE-076, PR 321.

PR 321 is closed and not merged; `origin/main` still has the bug. Its diff (a `failureText` helper,
one test, one boundary row in CORE-076) is correct against today's code and conflicts only because
CORE-076 moved.

| # | Question | Tag | Recommended answer | Reason |
| --- | --- | --- | --- | --- |
| 1 | Reuse PR 321? | INTERNAL | Redo it on a fresh branch from `origin/main` with the same three edits; do not reopen the eval branch. | The PR is closed, conflicting and titled as a test. |
| 2 | Format of one reason | INTERNAL | `<page>: <detail>`, joined with `; `; a string stays as it is; anything else is `JSON.stringify`. | The fields `capture.py` writes; the intent's "scenario, check, message" are inside `page` and `detail` (`check_name: error`). |
| 3 | JUnit | INTERNAL | Nothing more: `writeJUnit` writes `stage.error`, which gets the new text. | Same value. |
| 4 | Requirement | INTERNAL | The boundary row of PR 321 in CORE-076. | The script is covered there by the annotation exemption. |
| 5 | Changelog line | INTERNAL | None ("No user-facing change"); commit type `ci:` or `fix(ci)` per the allowed scopes. | Not visible to an extension user. |

- Files: `scripts/e2e-campaign.mjs`, `test/site/e2eCampaign.test.ts`,
  `requirements/tiers/swrs/rendering-core/SwRS-MDOKFSTUDIO-CORE-076.md`, `log.md`.
- Size: S. Fits.
- Risks: none of note.
- Depends on: nothing; shares `rendering-core/index.md` with CR 3 through the generated index.

---

## Batch view

### Files touched by more than one CR

| File | CRs |
| --- | --- |
| `.agents/guidelines/release-process.guidelines.md` | 1, 2, 3 |
| `CONTRIBUTING.md` ("How to Release", "GitHub Configuration") | 1, 2, 3 |
| `test/build/test_workflows.py` | 2, 3 |
| `requirements/tiers/swrs/rendering-core/` (CORE-076, generated index) | 3, 9 |
| `package.json` | 3 (devDependency), 5 (key binding and command) |
| `test/core/render/` | 6, 7 (different files) |
| `requirements/tiers/log.md`, generated indexes | 3, 4, 5, 6, 7, 8, 9 |
| `CHANGELOG.md` `## Unreleased` | 4, 5, 6, 7, 8 (and 3 if the owner wants a line) |

`log.md`, the indexes and the changelog conflict for every pair, so the batch ships as one stack.

### Suggested order of the stack

1. changelog-line-in-each-pr (sets the rule the others follow)
2. ci-report-object-object-message
3. ci-integration-locked-screen
4. publish-to-open-vsx
5. card-in-blockquote-line-offset
6. alert-followed-by-heading-taken-as-title
7. export-html-drops-block-being-edited
8. sticky-heading-long-title-wraps
9. cmd-s-from-preview-focus (largest, needs a real-window proof; on top so it can be left out)

Then the release CR. Process and CI first: they need no owner answer except the Open VSX setup. The
product CRs wait for the owner's answers of CRs 4, 5, 6 and 8.

### Fit for a quick batch

- Small and ready: 1, 2 (locked screen), 7 (card), 9 (ci-report).
- Small once the owner has answered: 6 (alert), 8 (sticky, with the recommended answer).
- Medium: 3 (Open VSX, first real run is the release itself), 4 (export, starts with a
  reproduction), 5 (Cmd+S, real-window test).
- The release cannot be 1.7.2 if any commit is typed `feat:`.

### What a user of 1.7.2 would notice

- Cmd+S (Ctrl+S) saves the document when the focus is in the preview.
- Export to HTML keeps the content of a table cell that is being edited.
- A click on a card of a grid written inside a quote opens the editor on the right line.
- A GitHub alert that starts with a heading or a bold line keeps its default title, as on GitHub
  (if the owner picks that answer).
- A long title in the sticky heading band stays on one line with an ellipsis (if the owner picks
  that answer).
- The extension is on Open VSX, for VSCodium, Cursor and Windsurf (if the owner's setup is done).

For contributors: a changelog line in each pull request, a locked screen named before the real
VS Code tests start, and `ci-report` naming each failed visual check.
