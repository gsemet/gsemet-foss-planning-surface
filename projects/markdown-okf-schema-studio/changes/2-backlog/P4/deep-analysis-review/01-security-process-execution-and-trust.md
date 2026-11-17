# 01 — Security: Process Execution and Workspace Trust

Part of the [deep analysis review](00-index.md) of `src/markdown-okf-schema-studio`.
This file stands alone: it lists every finding about external processes, configuration
that controls them, and the Workspace Trust model, with the fix and the evidence needed to close it.

Paths below are relative to the repository root.
Line numbers refer to commit `e1b4ad0`.

## Context

The preview renders Markdown in-process with `myst-parser`, so the only external process left is
PlantUML. [`renderPlantUmlDiagrams`](../../../../src/render/plantUmlRenderer.ts#L245)
spawns either `java -jar <jarPath> -pipe -tsvg` or `plantuml -pipe -tsvg` once per diagram,
with `cwd` set to the preview resource root and the full extension-host environment inherited.
The only gate is `trusted: options.isWorkspaceTrusted()`
([renderPipeline.ts:201](../../../../src/render/renderPipeline.ts#L201)),
which is `vscode.workspace.isTrusted`.

Two facts frame the threat model:

- The manifest declares no `capabilities.untrustedWorkspaces`.
  The VS Code Workspace Trust guide states that such an extension is disabled in Restricted Mode.
  The extension therefore only runs in trusted windows, and `isTrusted` is effectively always true.
- Trust covers a *folder*, not every Markdown file the preview opens.
  The preview also renders files outside any workspace folder ("standalone" mode, `readOnly`),
  and empty windows are trusted by default (`security.workspace.trust.emptyWindow`).
  A Markdown file opened from `~/Downloads` therefore reaches the PlantUML spawn path.

## Findings

### SEC-01 — PlantUML runs with full file and network access on any previewed document

- **Severity**: High
- **Confidence**: Confirmed by code reading and PlantUML vendor documentation
- **Effort**: S
- **Location**:
  [plantUmlRenderer.ts:162-243](../../../../src/render/plantUmlRenderer.ts#L162),
  [plantUmlRenderer.ts:255-283](../../../../src/render/plantUmlRenderer.ts#L255),
  [renderPipeline.ts:196-211](../../../../src/render/renderPipeline.ts#L196)

**What happens.**
The child process is spawned without `PLANTUML_SECURITY_PROFILE`.
PlantUML documents `LEGACY` as the default profile, with "full access to local files and full
access to URL". The preprocessor can therefore `!include` arbitrary local files, fetch remote
URLs, and read environment variables (`%getenv`), all driven by the diagram text.
The spawn inherits `process.env` of the extension host, which typically holds tokens
(`GITLAB_TOKEN`, proxy credentials, cloud SDK variables).

**Scenario.**
A colleague shares a Markdown file, or a branch under review adds one.
Opening its preview renders a `plantuml` fence that includes `~/.ssh/config` into the SVG,
or builds an outbound URL from local data. The first variant only discloses data on screen;
the second is a plausible exfiltration path that has not been reproduced here.
The preview runs this automatically after every render, without any user action on the diagram.

**Fix.**

1. Pass an explicit, minimal environment to the child:
   `env: { PATH, JAVA_HOME?, PLANTUML_SECURITY_PROFILE: "SANDBOX" }`.
2. For the JAR form, also pass `-DPLANTUML_SECURITY_PROFILE=SANDBOX` before `-jar`, so the
   profile holds even if a wrapper script rewrites the environment.
3. Spawn with `cwd` set to a dedicated empty temporary directory rather than the workspace,
   so relative includes cannot resolve even if the profile were ignored.
4. Disable PlantUML for standalone (`readOnly`) previews, or require an explicit opt-in setting
   (`markdownOkfSchemaStudio.plantuml.enabled`, user scope, default `true` for workspace files
   only).
5. Add a hard timeout (see
   [STAB-04](07-stability-and-correctness.md#stab-04--plantuml-child-process-handling-is-fragile)).

**Tests to add.**
Unit test with the existing spawner hook (`setPlantUmlProcessSpawnerForTests`) asserting the
`env`, `cwd`, and JVM arguments. Integration test: a standalone `.md` outside the workspace
containing a PlantUML fence produces an "unavailable" placeholder and zero spawns.

**Done when.**
No spawn inherits `process.env`; every spawn carries `SANDBOX`; standalone previews never spawn.

### SEC-02 — `plantuml.jarPath` is workspace-overridable and resolved against the workspace

- **Severity**: High (in a trusted workspace this is arbitrary code execution chosen by the
  repository)
- **Confidence**: Confirmed by code reading
- **Effort**: S
- **Location**:
  [package.json:101](../../../../package.json#L101),
  [plantUmlRenderer.ts:118-138](../../../../src/render/plantUmlRenderer.ts#L118),
  [plantUmlRenderer.ts:179-183](../../../../src/render/plantUmlRenderer.ts#L179)

**What happens.**
The setting has no `scope`, so `.vscode/settings.json` in any repository can set it.
A relative value is resolved against `workspaceRoot` (`resolvedJarPath`), which is the workspace
folder, or the document directory in standalone mode. The extension then runs `java -jar` on it.
A repository can therefore ship `tools/diagram.jar` plus a settings file and obtain code execution
as soon as a contributor previews a document containing a PlantUML fence.
Workspace Trust is the only barrier, and trust prompts are routinely accepted for internal repos.

The default command path has a related weakness.
`plantuml` and `java` are bare names resolved by `child_process.spawn` with `cwd` set to the
workspace. On Windows, the libuv search order looks in the working directory before `PATH`,
so a `plantuml.exe` or `java.exe` committed at the repository root could be executed instead.
This second variant is **plausible** and was not reproduced (the review ran on macOS).

**Fix.**

1. Declare `"scope": "machine"` on `markdownOkfSchemaStudio.plantuml.jarPath` so only user or
   machine settings apply.
2. Require an absolute path; reject relative values with a diagnostic instead of resolving them.
3. Resolve `java` and `plantuml` to absolute paths by scanning `PATH` explicitly, skipping
   empty entries and `.`; refuse a match located inside a workspace folder.
4. Use a temporary directory as `cwd` (shared with SEC-01).
5. List the setting in `capabilities.untrustedWorkspaces.restrictedConfigurations` (SEC-03).

**Tests to add.**
Configuration unit test: a relative `jarPath` yields an error diagnostic and no spawn.
Manifest test: `contributes.configuration` declares `scope: machine` for the setting.

**Done when.**
A workspace-level `jarPath` has no effect, and no executable is ever resolved from the workspace.

### SEC-03 — The manifest does not declare a Workspace Trust capability

- **Severity**: Medium
- **Confidence**: Confirmed by manifest reading and VS Code documentation
- **Effort**: M
- **Location**:
  [package.json:15](../../../../package.json#L15),
  [extension.ts:1942](../../../../src/extension.ts#L1942),
  [renderPipeline.ts:134](../../../../src/render/renderPipeline.ts#L134)

**What happens.**
Without `capabilities.untrustedWorkspaces`, VS Code disables the extension in Restricted Mode. The
code nevertheless contains a full untrusted design: `readOnly` previews, `allowUntrusted`, "Editing
requires a trusted workspace", and "PlantUML preview is disabled in an untrusted workspace". Those
branches are unreachable in practice, so the tests that exercise them prove behaviour that users
never get, and the real security boundary is "the user never trusts a hostile folder".

**Fix.**
Pick one model explicitly and make the code match it.

- **Recommended**: declare
  `"capabilities": { "untrustedWorkspaces": { "supported": "limited", "description": "...",
  "restrictedConfigurations": ["markdownOkfSchemaStudio.plantuml.jarPath",
  "markdownOkfSchemaStudio.frontmatter.bundleRoot",
  "markdownOkfSchemaStudio.frontmatter.projectRoot",
  "markdownOkfSchemaStudio.frontmatter.allowOutsideWorkspaceLinks"] } }`.
  In Restricted Mode, render read-only, skip PlantUML, skip includes outside the document directory,
  and skip schema resolution, which the existing `readOnly` branches already implement.
  Subscribe to `vscode.workspace.onDidGrantWorkspaceTrust` to upgrade open previews.
- **Alternative**: keep the extension disabled in Restricted Mode, delete the unreachable branches,
  and state the model in the README and `docs/security-evidence.md`.

**Tests to add.**
Integration run with `security.workspace.trust.enabled: true` and an untrusted folder, asserting
the preview opens read-only and PlantUML reports "unavailable".

**Done when.**
The manifest, the README, and the trust-dependent code paths describe the same behaviour.

### SEC-04 — Link-containment settings can be weakened by the repository itself

- **Severity**: Medium
- **Confidence**: Confirmed by code reading
- **Effort**: S
- **Location**:
  [package.json:116-130](../../../../package.json#L116),
  [fileLinks.ts:432-446](../../../../src/frontmatter/fileLinks.ts#L432),
  [fileLinks.ts:347-383](../../../../src/frontmatter/fileLinks.ts#L347),
  [previewNavigation.ts:180-199](../../../../src/navigation/previewNavigation.ts#L180)

**What happens.**
`allowOutsideWorkspaceLinks`, `bundleRoot`, and `projectRoot` are workspace-scoped.
`bundleRoot` and `projectRoot` accept absolute paths anywhere on disk (`configuredRoot`).
When a repository sets them, frontmatter links resolve outside the workspace.
Link enrichment then reads the target file (`linkedFileDetails`) and renders selected
frontmatter fields of that file in the preview, and a click opens it in an editor.
The data stays local, so the impact is limited to disclosure on screen and confusing navigation,
but it defeats requirement R4 of [spec.md](../../../../spec.md).

**Fix.**
Declare `allowOutsideWorkspaceLinks` with `"scope": "application"` (or `machine`).
Accept workspace-level `bundleRoot`/`projectRoot` only when they resolve inside a workspace folder;
keep the absolute escape hatch for user-level values. Add the three settings to
`restrictedConfigurations` (SEC-03).

**Tests to add.**
Unit test for `resolveFrontmatterLinkRoots`: a workspace-level root outside every workspace folder
is ignored, and a user-level one is honoured.

**Done when.**
No workspace setting can make the preview read or open a file outside the workspace folders.

## Related findings in other rubrics

- Process lifecycle defects of the same spawn path (EPIPE, timeout, encoding):
  [STAB-04](07-stability-and-correctness.md#stab-04--plantuml-child-process-handling-is-fragile).
- PlantUML cost (one JVM per diagram per render, no cache):
  [PERF-03](04-performance-render-pipeline.md#perf-03--plantuml-spawns-one-jvm-per-diagram-on-every-render).
- Supply chain and stale security evidence that still claims "untrusted host spawn count is zero":
  [SUP-04](03-security-supply-chain-and-packaging.md#sup-04--dead-sphinx-pipeline-code-and-stale-security-evidence).
