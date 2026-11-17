# Deep Analysis Review — Markdown OKF-Schema Studio

Date: 2026-10-08.
Subject: the VS Code extension in `src/markdown-okf-schema-studio` at commit `e1b4ad0`
(no uncommitted changes in that directory at review time).
Scope: security, performance, and stability of the shipped code paths.

## How to use this folder

Each rubric is a standalone work item. It restates its own context, cites file and line locations,
gives the evidence, the fix, the tests to add, and a "done when" criterion.
Pick one file, work it to completion, and update its findings in place.

| File | Rubric | Findings |
| --- | --- | --- |
| [01-security-process-execution-and-trust.md](01-security-process-execution-and-trust.md) | PlantUML process execution, settings, Workspace Trust | SEC-01 – SEC-04 |
| [02-security-webview-and-content.md](02-security-webview-and-content.md) | Webview CSP and sanitizer, content-driven reads, denial of service | SEC-05 – SEC-12 |
| [03-security-supply-chain-and-packaging.md](03-security-supply-chain-and-packaging.md) | Vulnerability scanning, VSIX content, stale evidence | SUP-02 – SUP-05 (SUP-01 excluded) |
| [04-performance-render-pipeline.md](04-performance-render-pipeline.md) | Main-thread rendering, HTML passes, PlantUML cost, memoisation | PERF-01 – PERF-04 |
| [05-performance-webview-lifecycle.md](05-performance-webview-lifecycle.md) | Webview reloads, Mermaid, scroll runtime, link discovery | PERF-05 – PERF-11 |
| [06-performance-frontmatter-and-filesystem.md](06-performance-frontmatter-and-filesystem.md) | Ajv leak, schema caching, stem index, watchers, sync I/O | PERF-12 – PERF-17 |
| [07-stability-and-correctness.md](07-stability-and-correctness.md) | Document corruption, edit locks, process errors, restore | STAB-01 – STAB-09 |
| [08-remediation-plan.md](08-remediation-plan.md) | Ordered increments, exit criteria, tracking metrics | all |
| [plan.md](plan.md) | Autonomous, sequential execution plan with sub-agents | all except SUP-01 |

## Summary

The extension has a sound security baseline for rendered content: a strict nonce-based CSP with no
network access, Mermaid and PlantUML output confined to `<img>` data URIs, KaTeX without `trust`,
alias-bomb protection on YAML, `realpath`-based containment for resources and navigation, and
careful escaping of the properties table. Raw HTML never reaches the page because `myst-to-html`
runs without `allowDangerousHtml`.

The material risks sit elsewhere.

1. **PlantUML is the one place where document content drives a process,** and it runs with
   PlantUML's default `LEGACY` profile (full file and URL access), the full extension-host
   environment, a workspace-relative `cwd`, and a JAR path that the repository's own settings can
   choose (SEC-01, SEC-02). It also runs for standalone files opened outside any workspace folder.
2. **A frontmatter edit can corrupt the document** when any value ends with `...` or `---`,
   because the fence pattern does not anchor the closing marker to a line start (STAB-01,
   reproduced).
3. **The session degrades over time:** the Ajv validator cache never hits and every compiled schema
   is retained, about 27 MB of heap per 1,000 analyses with a small schema at roughly three analyses
   per edit (PERF-12, reproduced); and an inline edit lock can survive a webview reload, after which
   no block can be edited (STAB-02).
4. **Every keystroke is expensive on the shared extension host:** three to six full webview document
   replacements (PERF-05), about 85 ms of synchronous rendering on the largest chapter (PERF-01,
   measured), several redundant HTML parse passes (PERF-02), one JVM per PlantUML diagram per render
   (PERF-03), and include expansion with no global budget, which reached 16 s at depth 5 of a
   ten-way fan-out (SEC-05, reproduced).
5. **The written evidence describes a retired Sphinx pipeline**, so reviewers reason about the wrong
   attack surface (SUP-04), and the manifest does not declare a Workspace Trust capability, which
   makes the extension's untrusted-mode code unreachable (SEC-03).

### Counts

| Severity | Count | Findings |
| --- | --- | --- |
| High | 8 | SEC-01, SEC-02, PERF-01, PERF-03, PERF-05, PERF-12, STAB-01, STAB-02 |
| Medium | 18 | SEC-03 – SEC-06, SUP-02, PERF-02, PERF-06 – PERF-09, PERF-13 – PERF-16, STAB-03 – STAB-06 |
| Low | 13 | SEC-07 – SEC-10, SUP-03, SUP-04, PERF-04, PERF-10, PERF-11, PERF-17, STAB-07 – STAB-09 |
| Info | 3 | SEC-11, SEC-12, SUP-05 |
| Excluded | 1 | SUP-01 (owner decision, 2026-10-09) |

## All findings

| ID | Severity | Confidence | Title |
| --- | --- | --- | --- |
| [SEC-01](01-security-process-execution-and-trust.md#sec-01--plantuml-runs-with-full-file-and-network-access-on-any-previewed-document) | High | Code + vendor docs | PlantUML runs with full file and network access on any previewed document |
| [SEC-02](01-security-process-execution-and-trust.md#sec-02--plantumljarpath-is-workspace-overridable-and-resolved-against-the-workspace) | High | Code | `plantuml.jarPath` is workspace-overridable and resolved against the workspace |
| [SEC-03](01-security-process-execution-and-trust.md#sec-03--the-manifest-does-not-declare-a-workspace-trust-capability) | Medium | Code + vendor docs | The manifest does not declare a Workspace Trust capability |
| [SEC-04](01-security-process-execution-and-trust.md#sec-04--link-containment-settings-can-be-weakened-by-the-repository-itself) | Medium | Code | Link-containment settings can be weakened by the repository itself |
| [SEC-05](02-security-webview-and-content.md#sec-05--include-expansion-has-no-global-budget-exponential-fan-out) | Medium | Reproduced | Include expansion has no global budget (exponential fan-out) |
| [SEC-06](02-security-webview-and-content.md#sec-06--script-and-stylesheet-policy-relies-on-a-single-layer) | Medium | Code | Script and stylesheet policy relies on a single layer |
| [SEC-07](02-security-webview-and-content.md#sec-07--broad-resource-roots-and-recursive-watching-in-standalone-mode) | Low | Code | Broad resource roots and recursive watching in standalone mode |
| [SEC-08](02-security-webview-and-content.md#sec-08--schema-supplied-regular-expressions-can-hang-the-extension-host) | Low | Plausible | Schema-supplied regular expressions can hang the extension host |
| [SEC-09](02-security-webview-and-content.md#sec-09--unbounded-synchronous-file-reads-driven-by-content) | Low | Code | Unbounded synchronous file reads driven by content |
| [SEC-10](02-security-webview-and-content.md#sec-10--host-message-handling-missing-size-caps-and-an-unguarded-openexternal) | Low | Code | Host message handling: missing size caps and an unguarded `openExternal` |
| [SEC-11](02-security-webview-and-content.md#sec-11--absolute-filesystem-paths-are-exposed-in-the-preview) | Info | Code | Absolute filesystem paths are exposed in the preview |
| [SEC-12](02-security-webview-and-content.md#sec-12--generated-css-is-not-escaped) | Info | Code | Generated CSS is not escaped |
| [SUP-01](03-security-supply-chain-and-packaging.md#sup-01--tls-verification-is-disabled-for-the-package-registry) | Excluded (was Medium) | Config | TLS verification is disabled for the package registry |
| [SUP-02](03-security-supply-chain-and-packaging.md#sup-02--the-release-gate-does-not-scan-for-known-vulnerabilities) | Medium | Code | The release gate does not scan for known vulnerabilities |
| [SUP-03](03-security-supply-chain-and-packaging.md#sup-03--the-vsix-ships-files-that-are-not-part-of-the-runtime) | Low | VSIX listing | The VSIX ships files that are not part of the runtime |
| [SUP-04](03-security-supply-chain-and-packaging.md#sup-04--dead-sphinx-pipeline-code-and-stale-security-evidence) | Low | Import graph | Dead Sphinx pipeline code and stale security evidence |
| [SUP-05](03-security-supply-chain-and-packaging.md#sup-05--runtime-deprecation-warning-from-a-dependency) | Info | Observed | Runtime deprecation warning from a dependency |
| [PERF-01](04-performance-render-pipeline.md#perf-01--the-whole-render-runs-on-the-extension-host-main-thread) | High | Measured | The whole render runs on the extension host main thread |
| [PERF-02](04-performance-render-pipeline.md#perf-02--the-html-is-parsed-and-serialised-six-or-more-times-per-render) | Medium | Measured | The HTML is parsed and serialised six or more times per render |
| [PERF-03](04-performance-render-pipeline.md#perf-03--plantuml-spawns-one-jvm-per-diagram-on-every-render) | High | Code | PlantUML spawns one JVM per diagram on every render |
| [PERF-04](04-performance-render-pipeline.md#perf-04--code-highlighting-and-math-are-recomputed-for-every-block-on-every-render) | Low | Code | Code highlighting and math are recomputed for every block on every render |
| [PERF-05](05-performance-webview-lifecycle.md#perf-05--each-keystroke-replaces-the-webview-document-three-to-six-times) | High | Code | Each keystroke replaces the webview document three to six times |
| [PERF-06](05-performance-webview-lifecycle.md#perf-06--saving-the-active-document-triggers-a-redundant-full-render) | Medium | Code | Saving the active document triggers a redundant full render |
| [PERF-07](05-performance-webview-lifecycle.md#perf-07--the-5-mb-mermaid-bundle-is-reloaded-and-every-diagram-re-rendered-on-each-reload) | Medium | Code + size | The 5 MB Mermaid bundle is reloaded and every diagram re-rendered on each reload |
| [PERF-08](05-performance-webview-lifecycle.md#perf-08--scrolling-forces-synchronous-layout-several-times-per-frame) | Medium | Code | Scrolling forces synchronous layout several times per frame |
| [PERF-09](05-performance-webview-lifecycle.md#perf-09--link-discovery-is-repeated-on-every-reload-and-runs-uncached-findfiles) | Medium | Code | Link discovery is repeated on every reload and runs uncached `findFiles` |
| [PERF-10](05-performance-webview-lifecycle.md#perf-10--retaincontextwhenhidden-keeps-every-hidden-preview-alive) | Low | Code | `retainContextWhenHidden` keeps every hidden preview alive |
| [PERF-11](05-performance-webview-lifecycle.md#perf-11--the-runtime-script-and-css-are-inlined-in-every-page) | Low | Measured | The runtime script and CSS are inlined in every page |
| [PERF-12](06-performance-frontmatter-and-filesystem.md#perf-12--the-ajv-validator-cache-never-hits-and-every-compile-is-retained-memory-leak) | High | Reproduced | The Ajv validator cache never hits, and every compile is retained |
| [PERF-13](06-performance-frontmatter-and-filesystem.md#perf-13--schema-discovery-and-parsing-are-not-cached) | Medium | Code | Schema discovery and parsing are not cached |
| [PERF-14](06-performance-frontmatter-and-filesystem.md#perf-14--frontmatter-is-analysed-three-times-per-edit) | Medium | Code | Frontmatter is analysed three times per edit |
| [PERF-15](06-performance-frontmatter-and-filesystem.md#perf-15--any-markdown-save-invalidates-the-stem-index-and-forces-a-synchronous-rebuild) | Medium | Code | Any Markdown save invalidates the stem index (synchronous tree walk) |
| [PERF-16](06-performance-frontmatter-and-filesystem.md#perf-16--recursive-file-watchers-and-per-event-realpath-calls) | Medium | Code | Recursive file watchers and per-event `realpath` calls |
| [PERF-17](06-performance-frontmatter-and-filesystem.md#perf-17--per-keystroke-synchronous-filesystem-calls) | Low | Code | Per-keystroke synchronous filesystem calls |
| [STAB-01](07-stability-and-correctness.md#stab-01--frontmatter-fence-detection-truncates-the-block-and-table-edits-corrupt-the-file) | High | Reproduced | Frontmatter fence detection truncates the block and table edits corrupt the file |
| [STAB-02](07-stability-and-correctness.md#stab-02--the-inline-edit-lock-survives-a-webview-reload) | High | Code path | The inline-edit lock survives a webview reload |
| [STAB-03](07-stability-and-correctness.md#stab-03--any-reload-destroys-an-open-inline-editor) | Medium | Code path | Any reload destroys an open inline editor |
| [STAB-04](07-stability-and-correctness.md#stab-04--plantuml-child-process-handling-is-fragile) | Medium | Reproduced (EPIPE) | PlantUML child-process handling is fragile |
| [STAB-05](07-stability-and-correctness.md#stab-05--restoring-a-serialised-panel-orphans-the-previous-side-preview) | Medium | Code | Restoring a serialised panel orphans the previous side preview |
| [STAB-06](07-stability-and-correctness.md#stab-06--inline-block-edits-rely-on-absolute-offsets-and-can-be-dropped-silently) | Medium | Plausible | Inline block edits rely on absolute offsets and can be dropped silently |
| [STAB-07](07-stability-and-correctness.md#stab-07--github-alerts-are-not-recognised-in-crlf-documents) | Low | Reproduced | GitHub alerts are not recognised in CRLF documents |
| [STAB-08](07-stability-and-correctness.md#stab-08--inherited-object-keys-are-treated-as-frontmatter-fields) | Low | Code | Inherited object keys are treated as frontmatter fields |
| [STAB-09](07-stability-and-correctness.md#stab-09--per-document-state-grows-without-bound) | Low | Code | Per-document state grows without bound |

## Severity and confidence scales

**Severity** reflects impact on a realistic user of this repository, not worst-case theory.

| Level | Meaning |
| --- | --- |
| High | Code execution or data disclosure driven by content or repository settings; document corruption; leaks or blockages that degrade every session |
| Medium | Denial of service from content; defence-in-depth gaps one change away from exploitable; costs paid on every edit or save |
| Low | Bounded impact, narrow preconditions, or hygiene with a security or reliability angle |
| Info | Worth fixing opportunistically; no direct impact |

**Confidence** states how each finding was established.

| Label | Meaning |
| --- | --- |
| Reproduced | Demonstrated by running the compiled modules (`out/src`) against a crafted input |
| Measured | Timed or sized on real repository content |
| Code path / Code | Established by reading the call chain end to end; not executed in a running VS Code |
| Vendor docs | Behaviour of VS Code or PlantUML taken from their official documentation |
| Plausible | Mechanism is sound but depends on timing, platform, or inputs that were not reproduced |

## Method

- Manual review of the 30 live production modules under `src/` (about 14,700 lines including the
  dead ones), the manifest, `esbuild.mjs`, `.npmrc`, `.vscodeignore`, and the packaged VSIX listing.
  The three dead Sphinx modules (SUP-04) were only checked for imports, and the CSS-only
  `previewStyles.ts` was scanned for external URLs.
- Compilation with the project `tsconfig.json` into a scratch directory, then targeted probes of the
  compiled modules: Ajv cache growth and retained heap, frontmatter extraction and patching, include
  fan-out, CRLF alert rendering, PlantUML early-exit behaviour through the spawner test hook, and
  per-stage render timing on `book/chapters/08-research-plan-implement.md`.
- Vendor documentation checked: VS Code Workspace Trust extension guide, PlantUML security profiles.

## Limits of this review

- No probe ran inside a live VS Code instance; webview reload counts and lock behaviour are derived
  from the call chain, and the integration suites were not executed.
- No vulnerability database was queried for the dependency tree (the internal registry requires the
  corporate network); SUP-02 asks for this to become part of the release gate.
- Windows-specific behaviour (executable search order in SEC-02, CRLF defaults in STAB-07) was
  reasoned about on macOS and not executed on Windows.
- The test suites under `test/` were read only where needed to confirm which modules are dead; their
  coverage was not assessed.
