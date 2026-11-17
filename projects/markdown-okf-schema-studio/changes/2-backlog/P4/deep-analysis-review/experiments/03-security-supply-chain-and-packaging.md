# 03 — Security: Supply Chain, Packaging, and Security Evidence

Part of the [deep analysis review](00-index.md) of `src/markdown-okf-schema-studio`.
This file covers how dependencies are fetched, what the VSIX ships, and whether the written
security evidence still matches the code. Paths are relative to the repository root;
lines refer to `e1b4ad0`.

## Context

Dependencies resolve exclusively through the internal Artifactory (584 lockfile entries, all on
`artifactory.tls.renault.fr`, all with an `integrity` hash). The release gate runs
[`test/release/audit-lockfile.mjs`](../../../../test/release/audit-lockfile.mjs),
which checks resolved hosts and credential leakage. Runtime dependencies are bundled by esbuild into
`out/bundle/extension.js` (1.6 MB) and `out/bundle/mermaidPreview.js` (5.0 MB).

## Findings

### SUP-01 — TLS verification is disabled for the package registry

- **Status**: Excluded on 2026-10-09 by the repository owner. No change is planned; the finding is
  kept for the record and is not part of [plan.md](plan.md).
- **Severity**: Medium
- **Confidence**: Confirmed by configuration reading
- **Effort**: S
- **Location**: [.npmrc:2](../../../../.npmrc#L2)

**What happens.**
`strict-ssl=false` turns off certificate validation for every npm request in this package.
`npm ci` still verifies the lockfile `integrity` hashes, which protects a clean install from a
tampered tarball. The protection disappears for every command that writes the lockfile:
`npm install <pkg>`, `npm update`, Dependabot-style bumps, and `npm audit` itself, because the
metadata (versions, tarball URLs, and the new integrity values) is accepted from an unauthenticated
connection. Anyone able to intercept traffic on the corporate network or VPN can then plant a
package that the next lockfile update records as legitimate.

**Fix.**
Install the Renault root CA and reference it instead of disabling verification:
`cafile=/path/to/renault-root-ca.pem` in `.npmrc`, or `NODE_EXTRA_CA_CERTS` in the developer
environment and CI image. Remove `strict-ssl=false`.
Document the CA setup in `CONTRIBUTING.md` so the change does not block onboarding.

**Done when.**
`npm ci` and `npm install` succeed with `strict-ssl=true` on a developer machine and in CI.

### SUP-02 — The release gate does not scan for known vulnerabilities

- **Severity**: Medium
- **Confidence**: Confirmed by reading the gate
- **Effort**: S
- **Location**:
  [audit-lockfile.mjs](../../../../test/release/audit-lockfile.mjs),
  root `justfile` target `vscode-markdown-okf-schema-studio-release-check`

**What happens.**
The lockfile audit is a provenance check, not a vulnerability check. The bundle embeds parsers that
process untrusted text (`parse5`, `yaml`, `ajv`, `katex`, `highlight.js`, the unified/micromark
stack behind `myst-parser`) and `mermaid@12.0.0`, a fresh major release with a history of XSS
advisories. `docs/security-evidence.md` reports "zero reported vulnerabilities" from a single past
run, which does not protect later releases.

**Fix.**
Add `npm audit --omit=dev --audit-level=high` (if Artifactory proxies the audit endpoint) or
`osv-scanner --lockfile package-lock.json` to the release gate, and fail on high or critical runtime
advisories. Generate a CycloneDX SBOM (`npm sbom --sbom-format cyclonedx`) next to the VSIX so a
later advisory can be matched to shipped versions.

**Done when.**
The release gate fails on a known high-severity advisory in a runtime dependency.

### SUP-03 — The VSIX ships files that are not part of the runtime

- **Severity**: Low
- **Confidence**: Confirmed by listing `.artifacts/markdown-okf-schema-studio.vsix`
- **Effort**: XS
- **Location**: [.vscodeignore](../../../../.vscodeignore)

**What happens.**
The packaged extension contains, besides the bundles:

- `.playwright-cli/` page snapshots and console logs from local debugging sessions
  (git-ignored, but `vsce` packages the working directory);
- `package.json.orig` (git-ignored backup), `spec.md`, and the whole `docs/` folder;
- `out/bundle/extension.js.map` (5.6 MB), which reconstructs the full TypeScript source.

None of the inspected files contained local paths, but the next debugging session may write some.
The source map also roughly doubles the installed size.

**Fix.**
Switch `.vscodeignore` to an allowlist: ignore `**`, then re-include `out/bundle/extension.js`,
`out/bundle/mermaidPreview.js`, `out/bundle/katex/**`, `package.json`, `README.md`, `CHANGELOG.md`,
and `LICENSE`. Keep source maps out of the VSIX, or ship them only in a separate debug build.
Add a release-gate assertion on the VSIX file list.

**Done when.**
The VSIX listing contains only runtime files, and the gate fails if anything else appears.

### SUP-04 — Dead Sphinx pipeline code and stale security evidence

- **Severity**: Low (governance; misleads reviewers about the real attack surface)
- **Confidence**: Confirmed by import graph and document reading
- **Effort**: S
- **Location**:
  [src/build/sphinxBuild.ts](../../../../src/build/sphinxBuild.ts),
  [src/build/snapshotWorkspace.ts](../../../../src/build/snapshotWorkspace.ts),
  [src/build/sourceTransforms.ts](../../../../src/build/sourceTransforms.ts),
  [html-sanitizer.ts:445-482](../../../../src/security/html-sanitizer.ts#L445),
  [docs/security-evidence.md](../../../../docs/security-evidence.md),
  [docs/known-limitations.md](../../../../docs/known-limitations.md),
  [AGENTS.md:236-246](../../../../AGENTS.md#L236)

**What happens.**
No production module imports `sphinxBuild`, `snapshotWorkspace`, or `sourceTransforms`; only their
tests do. `sanitizeCss` and the external-script branch of the sanitizer also only made sense for
Sphinx output. Meanwhile, the written evidence describes that retired pipeline:

- `security-evidence.md` asserts "untrusted host spawn count is zero" and Sphinx staging isolation,
  while the shipped code now spawns PlantUML processes.
- `known-limitations.md` describes "an opt-in, read-only preview" with no "rendered-block editing",
  while the preview now edits blocks, table cells, and frontmatter.
- `AGENTS.md` documents `sphinx-build` (~1.2 s per render) and a 250 ms debounce; the code renders
  in-process with a 40 ms debounce.

Reviewers and coding agents read these documents first and will reason about the wrong system.

**Fix.**
Delete the three modules and their tests (or move them under `test/legacy/` with a note),
remove `sanitizeCss` and the external-script handling once SEC-06 lands, and rewrite the three
documents to describe the in-process MyST pipeline, the PlantUML process, and preview editing.

**Done when.**
Every security claim in `docs/` can be traced to a test that exercises the shipped code path.

### SUP-05 — Runtime deprecation warning from a dependency

- **Severity**: Info
- **Confidence**: Confirmed by running the renderer
- **Effort**: XS

**What happens.**
Rendering emits Node's `DEP0040` warning (the built-in `punycode` module), pulled in through the
Markdown parsing stack. It is harmless today but will become an error in a future Node release
used by VS Code's extension host.

**Fix.**
Identify the importing package with `node --trace-deprecation`, and alias `punycode` to the
userland `punycode/` package in esbuild (`alias: { punycode: "punycode/" }`).
