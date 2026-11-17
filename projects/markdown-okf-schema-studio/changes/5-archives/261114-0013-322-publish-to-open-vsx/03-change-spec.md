# Change Specification: publish to Open VSX with trusted publishing

Type: ci (plus docs). Automatable: the owner asked to be asked only on a user impact (02-answers.md,
2026-11-12); the user-facing parts (install links, README, user docs) are the owner's own words of
2026-11-14.
Sources: `01-intent.md`, `02-answers.md` (every entry up to "2026-11-14: scope added by the
owner"), `intake/advisor-grill.md` (section 3), the archived CR-315
(`4-archives/261113-1510-315-marketplace-trusted-publishing/03-change-spec.md`). Code read at
`origin/main` `f50b2059` (version 1.8.1; the local `main` is behind: cut the worktree from
`origin/main`).

## Goal

The owner's words: « Publish this extension to <https://open-vsx.org/search?q=Markdown> », then
« il y a moyen de ne pas faire de token », then (2026-11-14) « il faudra que le process de release
watch les 2 marketplaces pendant 10-15 min, et il faudra mettre les liens vers les 2 marketplace dans
la release notes et le README [...] met a jour les instructions d'install et les doc ».

1. The release job publishes the same VSIX to Open VSX with Open VSX trusted publishing (GitHub
   Actions OIDC). No `OVSX_PAT` secret exists or is read.
2. The release process watches both registries after the release job and reports each one's state.
3. The release notes, the README and the user documentation name both registries with their links.
4. A Cursor compatibility report is filed as a new inbox item (no fix).

## Already in place (outside this repository)

- Open VSX namespace `GaetanSemet` owned and `verified: true` (claim
  https://github.com/EclipseFdn/open-vsx.org/issues/15660, granted 2026-11-13).
- 1.8.0 published by hand and served: `GET https://open-vsx.org/api/GaetanSemet/markdown-okf-schema-studio/1.8.0`
  answers 200 (checked 2026-11-14); 1.8.1 is **not** on Open VSX (404). Nothing in this CR
  backfills it.
- Trusted publisher registered 2026-11-14 on open-vsx.org: provider GitHub, owner `gsemet`,
  repository `markdown-okf-schema-studio`, workflow `release.yml`, environment `release` (one
  trusted publisher per extension).
- The `release` environment, the job `package` of `release.yml` with `environment: release` and
  `permissions: contents: write, id-token: write`, and the caller job `release` of `ci.yml` with
  `contents: write, id-token: write`: all present since CR-315. Nothing to add there.
- The one-off "first publish" Open VSX token: kept by the owner for now (emergency path only; never
  stored in GitHub).

## Decisions carried from 02-answers.md and the brief

1. Trusted publishing, no `OVSX_PAT` (owner, 2026-11-13). The string `OVSX_PAT` must not appear in
   `.github/`: ovsx gives a PAT precedence over OIDC.
2. `ovsx` is a pinned devDependency, like `@vscode/vsce` 4.1.0 in CR-315 (constitution section 5:
   this specification allows that dependency, and only it).
3. The Open VSX step runs after the Marketplace step, so an Open VSX failure never blocks the
   Marketplace (02-answers, 2026-11-13).
4. `--skip-duplicate`, so a re-run or a dispatch with an existing tag is safe.
5. The first proof is the v1.9.0 release, the release CR right after this one in the same batch.

## Facts checked for this specification (ovsx on npm, 2026-11-14)

- `--trusted-publishing` first appears in **ovsx 1.2.0** (2026-09-10); 1.1.1 and older do not have
  it. 1.3.0 (2026-10-16) and 1.4.0 (2026-11-09) keep it.
- `ovsx publish` options used: `-i, --packagePath <paths...>`, `--skip-duplicate`,
  `--trusted-publishing` ("requires trusted publishing and fails if no ID token can be obtained";
  without the flag ovsx silently falls back to a PAT when one is present). On GitHub Actions the
  ID token is requested from the runner (needs `id-token: write`), nothing else to configure.
- 1.4.0 asks the registry for the expected OIDC audience (1.2.0 and 1.3.0 send the registry URL
  as audience), adds an inactivity timeout (`OVSX_TIMEOUT`, 30 s default, which also covers the ID
  token request) and `--registrationCode` (private repositories only; not needed here).
- ovsx 1.4.0: `engines.node >= 22` (`.nvmrc` is 24); depends on `@vscode/vsce ^4.0.0` (dedupes
  with our 4.1.0), `cross-keychain` (optional prebuilt `@napi-rs/keyring`, no install script, so
  `npm ci --ignore-scripts` is fine; the token store is not used by trusted publishing),
  `@inquirer/prompts`, `commander`, `semver`, `ci-info`, `yauzl-promise`.

## What changes

### 1. `package.json` and `package-lock.json`

- `fnm exec -- npm install --save-dev ovsx@1.4.0`: `devDependencies` gets `"ovsx": "^1.4.0"` (the
  repository's caret convention; the lock file pins), and the lock resolves exactly 1.4.0. Check
  `node_modules/ovsx/package.json` and the `node_modules/ovsx` lock entry both say `1.4.0`.
- `npm ls @vscode/vsce` shows a single 4.1.0 (deduped under `ovsx`). If npm nests a second vsce,
  say so in the PR body.
- Run a full `npm audit` (dev included). A new high or critical advisory reached through `ovsx`
  gets a floor in `overrides` with its line in the `//overrides` note, in the same style as
  `@azure/msal-node` and `qs`; a moderate one is named in the PR body only. Keep the existing
  `overrides` and the note unchanged otherwise.

### 2. `.github/workflows/release.yml`, job `package`

Add one step, **last** in the job, after "Attach VSIX and images to GitHub release":

```yaml
      # Open VSX trusted publishing: an OIDC token of this job, no stored token. Last, so an Open
      # VSX failure leaves the Marketplace publication and the GitHub release done.
      - name: Publish to Open VSX
        run: npx --no-install ovsx publish --trusted-publishing --skip-duplicate --packagePath out/reports/package/markdown-okf-schema-studio.vsix
```

- Exact step name "Publish to Open VSX" (the test looks it up by name).
- `npx --no-install`, as for vsce: the pinned devDependency, never a download in the job that
  holds publish rights.
- No `env:` block and no `continue-on-error`: a failure turns the job red so it is seen and
  recovered (section 4 below).
- Nothing else in the file changes: permissions, environment, order of the existing steps.

### 3. `test/build/test_workflows.py`

Add one test next to `test_release_publishes_to_the_marketplace_with_trusted_publishing`, without
a `@tests_req` marker (same reason as CR-315: release hardening, not an extension behaviour, no
SwRS covers publication), for example `test_release_publishes_to_open_vsx_with_trusted_publishing`:

- `_step("Publish to Open VSX")["run"]` contains `npx --no-install ovsx publish`,
  `--trusted-publishing`, `--skip-duplicate` and
  `--packagePath out/reports/package/markdown-okf-schema-studio.vsix`;
- the step has no `env` and no `continue-on-error`;
- `"OVSX_PAT" not in RELEASE.read_text()`;
- in the `package` job's step names, "Publish to VS Code Marketplace" and "Attach VSIX and images to
  GitHub release" both come before "Publish to Open VSX";
- `_release()["jobs"]["package"]["permissions"]["id-token"] == "write"` and
  `_release()["jobs"]["package"]["environment"] == "release"` (the trusted publisher pins both the
  file name and the environment).

### 4. `CONTRIBUTING.md`, "How to Release"

- Step 6: "publishes to Marketplace with trusted publishing (OIDC), and attaches ..." becomes
  "publishes to the VS Code Marketplace with trusted publishing (OIDC), attaches the VSIX, the
  notes and their images to a GitHub release, then publishes the same VSIX to Open VSX with
  trusted publishing". Add one sentence pointing to the release guideline's step 6 for watching
  both registries afterwards.
- "GitHub Configuration": the introduction says the workflow publishes to both registries with
  trusted publishing and reads no stored token. Add one bullet: the Open VSX trusted publisher on
  the `GaetanSemet/markdown-okf-schema-studio` extension (open-vsx.org, Settings, Trusted
  Publishers): provider GitHub, owner `gsemet`, repository `markdown-okf-schema-studio`, workflow
  `release.yml`, environment `release`; the namespace `GaetanSemet` must stay verified and equal
  to the `publisher` field of `package.json`; no `OVSX_PAT` secret exists. Extend the renaming
  bullet: renaming `release.yml` or the `release` environment breaks both publications until the
  Marketplace policy and the Open VSX trusted publisher are updated.
- "Recovery and Release Notes":
  - "Marketplace publication skips an already published version" becomes "Marketplace and Open
    VSX publications skip an already published version".
  - Add the Open VSX failure case: the step is last, so the Marketplace and the GitHub release are
    already done and the job is red. Fix the cause if any, then re-run the failed job or dispatch
    **Release VSIX** with the existing tag: the Marketplace step skips the duplicate, the GitHub
    release step rewrites the release body from the reviewed notes file (a hand edit made on GitHub
    in between is lost: redo it), and Open VSX is retried. In an emergency the owner publishes the
    VSIX of the GitHub release by hand with `npx ovsx publish <file.vsix> -p <token>` and a
    personal Open VSX token never stored in GitHub. There is no automatic fallback to a token.

### 5. `.agents/guidelines/release-process.guidelines.md`

No role names (`test_guideline_isolation.py`): keep "the agent that runs the release" style.

- Opening sentence ("Marketplace publication"): "Marketplace and Open VSX publication".
- Step 6, rewritten around the owner's 2026-11-14 words:
  - After the release job, watch **both** registries for 10 to 15 minutes (poll about once a
    minute) until each serves the new version, and report each one's state (served, at which
    minute, or not served after 15 minutes).
  - Checks of record, HTTP 200 each:
    - VS Code Marketplace: the existing `.../vsextensions/markdown-okf-schema-studio/X.Y.Z/vspackage`
      URL (unchanged text, listing lag sentence kept);
    - Open VSX: `https://open-vsx.org/api/GaetanSemet/markdown-okf-schema-studio/X.Y.Z` (for
      example the same `curl -sS -o /dev/null -w '%{http_code}' <url>`). The extension page
      `https://open-vsx.org/extension/GaetanSemet/markdown-okf-schema-studio` is not a gate.
  - A registry still not serving after 15 minutes: read the job log of its step; a red step is
    recovered as in "Recovery and Release Notes" of CONTRIBUTING.md; a green step whose version is
    not served yet is reported to the owner, not retried.
  - Keep the Marketplace trusted publishing sentences; add that the Open VSX publication uses the
    trusted publisher registered on open-vsx.org (no stored token). Leave the `VSCE_PAT` sentence
    as it is (not this CR's subject).
- "Release notes", item 2 **Links**: "Install from the Marketplace · Read the guide · Full
  changelog · 1.0 showcase" becomes, with the owner's exact texts and URLs:
  `[Install from VS Code Marketplace](https://marketplace.visualstudio.com/items?itemName=GaetanSemet.markdown-okf-schema-studio)`
  · `[Install from Open VSX](https://open-vsx.org/extension/GaetanSemet/markdown-okf-schema-studio)`
  · Read the guide · Full changelog (`blob/vX.Y.Z/CHANGELOG.md`) · 1.0 showcase.
- "Publishing" ("before the Marketplace publication"): "before the Marketplace and Open VSX
  publications".
- "Announcement thread", post 3: unchanged (still the Marketplace URL only; see open question 2).

Nothing generates or checks the install links today: `scripts/release_notes.py` validates the
images and the notes file, not the links line, and no test reads it. Do **not** add a links check
in this CR: `release-notes-check` validates the current version's notes (1.8.1), which have the old
line, so the check would fail `just check` on this branch. The v1.9.0 release CR writes its notes
with the new line from the guideline. Published notes of earlier versions are history: unchanged.

### 6. README and user documentation (owner, 2026-11-14)

Text on both registries: VS Code installs from the VS Code Marketplace; VSCodium, Cursor and other
compatible editors install from Open VSX. Links:
`https://marketplace.visualstudio.com/items?itemName=GaetanSemet.markdown-okf-schema-studio` and
`https://open-vsx.org/extension/GaetanSemet/markdown-okf-schema-studio`.

- `README.md` line 7 (the link row): `[VS Code Marketplace](...) | [Open VSX](...) | [Screenshot
  report/gallery](...) | [Requirements](...)`.
- `README.md` "## Install": name both registries as above, keep "or search for it in the
  Extensions view and select **Install**" (true in every one of these editors).
- `docs/user/open-studio.md` (top paragraph): the same two-registry sentence.
- `docs/user/README.md` line 5 ("Marketplace install, ..."): "install from the VS Code Marketplace
  or Open VSX, ...".
- `skills/writing-for-markdown-okf-schema-studio/SKILL.md` "## Install the extension": name both
  registries; keep `code --install-extension GaetanSemet.markdown-okf-schema-studio` and add that
  other editors install the same ID from Open VSX (their own CLI or Extensions view). Judgment: the
  owner asked for "the install instructions and the docs", and the skill holds an install
  instruction the agent repeats to users. Check the skill's own tests and sync rules (`just check`).
- Before writing, `git grep -n "marketplace.visualstudio.com/items?itemName=GaetanSemet"` on the
  worktree, excluding `docs/releases-notes/` and `CHANGELOG.md`: every other hit that is an install
  instruction gets Open VSX next to it; report any hit left alone and why.
- The README ships inside the VSIX: the link is already live (1.8.0 is on Open VSX).

### 7. Cursor compatibility report (scope of `01-intent.md`; not in the pull request)

`.agents/changes/` is ignored by git. Write a new inbox item in the **main checkout**:
`/Users/az02065/Projects/DevTools/markdown-okf-schema-studio/.agents/changes/1-inbox/cursor-compatibility/01-intent.md`
(type, owner's words from this CR's `01-intent.md`: « Then check what would be necessary to be
compatible with Cursor »). Content: what was checked from the code at `origin/main`, and what stays
open. Facts already checked for this specification (the coder re-checks them on the branch):

- `engines.vscode` `^1.95.0`; Cursor, VSCodium and Windsurf report their own VS Code engine
  version: compare with the current one of each (open, needs the editor's About box or release
  notes).
- No `enabledApiProposals`, no `extensionKind`, no `browser` entry, no `extensionDependencies`.
- Uses a custom text editor (`registerCustomEditorProvider`, view type
  `markdown-okf-schema-studio.editor`, priority `option`) and a webview panel with a serializer
  (`createWebviewPanel`, `registerWebviewPanelSerializer`): standard APIs, but webview behaviour in
  Cursor is unproven.
- `capabilities.agentsWindow.supported: true` (VS Code specific; ignored elsewhere, to confirm).
- Open: an install of the Open VSX build in Cursor and a smoke run (open a document, edit a block,
  the preview to the side). Nobody can prove it without Cursor installed.

No fix in this CR. Name the item in the PR body ("Cursor compatibility: filed in the inbox").

## Out of scope

- Publishing 1.8.1 (or any older version) to Open VSX by hand; v1.9.0 is the first automatic
  publication. The intent's "publish 1.3.0 by hand" is dropped (advisor, question 5).
- Deleting the owner's "first publish" token or `VSCE_PAT`.
- The v1.9.0 release itself (its own release CR, next in the stack).
- Marketplace publishing without `VSCE_PAT` changes, or `vsce --azure-credential` (separate idea of
  the owner).
- Requirements: no SwRS change (CI and docs; CR-315 precedent; CORE-078 is about the notes and
  stays true). Judgment against the advisor's question 8 (new SwRS): the release workflow is not an
  extension behaviour, and CR-315 shipped the same kind of step without one.
- `CHANGELOG.md`: no line (ci and docs commits get none, CONTRIBUTING step 2). The v1.9.0 release
  notes may still tell users that Studio is on Open VSX: that is the release CR's choice.

## Commits

Per [git-commit-message.guidelines.md](../../../guidelines/git-commit-message.guidelines.md) and
[git-commit-allowed-scopes.md](../../../guidelines/git-commit-allowed-scopes.md):

1. `ci: publish to Open VSX with trusted publishing` (`package.json`, `package-lock.json`,
   `release.yml`, `test_workflows.py`, CONTRIBUTING, the release guideline's step 6 and opening
   sentence).
2. `docs: name Open VSX in the install instructions and release notes links` (README, user docs,
   skill, the release guideline's "Links" item).

Never `feat:` (the batch's version is decided by the release CR). Pull request per
[pull-request.guidelines.md](../../../guidelines/pull-request.guidelines.md); the body says the first
proof is v1.9.0, there is no secret to add, the trusted publisher is already registered, and the
Cursor report is in the inbox.

## Evidence

Checks (local, in the worktree):

1. `npx --no-install ovsx --version` prints `1.4.0`; `npx --no-install ovsx publish --help` lists
   `--trusted-publishing`, `--skip-duplicate` and `--packagePath`.
2. `npm ls @vscode/vsce ovsx` shows vsce 4.1.0 once and ovsx 1.4.0.
3. `git grep -n OVSX_PAT -- .github/` prints nothing.
4. `npm ci --ignore-scripts` then `npx --no-install ovsx --version` works (the release job's
   install).
5. `just package` builds `out/reports/package/markdown-okf-schema-studio.vsix`.
6. `just check` passes (workflow tests, release-notes-check, guideline isolation, skill checks).
7. `just preflight` passes (completion gate, constitution section 4).

Scenario (not runnable before merge; for the v1.9.0 release CR):

1. The v1.9.0 version push runs `ci.yml`; `tag-release` tags; job `release` calls `release.yml`.
2. "Publish to VS Code Marketplace" succeeds, then "Attach VSIX and images to GitHub release",
   then "Publish to Open VSX" logs a publish with trusted publishing and no token.
3. Within 10 to 15 minutes both checks of record answer 200; the release report gives each
   registry's state.
4. On an Open VSX failure: the Marketplace and the GitHub release are done; recovery as in
   CONTRIBUTING "Recovery and Release Notes".

## Open questions

1. Reusable-workflow identity on Open VSX. The normal path is `ci.yml` calling `release.yml`; the
   OIDC token names the caller in `workflow_ref` and the called file in `job_workflow_ref`. The
   Marketplace matched `release.yml` (CR-316); Open VSX's documentation does not say which claim it
   matches, and one trusted publisher per extension means no second entry for `ci.yml`. If v1.9.0
   fails on this, recovery is a `workflow_dispatch` of `release.yml` with the tag (there the token
   names `release.yml` in both claims). Does not block this CR.
2. Announcement thread post 3 (USER-IMPACT, small): the owner asked for both links in the release
   notes and the README, not the thread. This spec leaves the thread with the Marketplace link
   only; the release CR may ask the owner whether post 3 names Open VSX too.
