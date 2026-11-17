# Audit: performance, security and maintainability of the extension

Type: chore · Priority: P3 · Audit 2026-10-27

## Goal

Give the maintainer a verified, ranked list of improvements to the extension's performance
under load (many previews, very large documents, fast typing), its security (webview, message
channel, file access, supply chain) and its modularity and maintainability, each with evidence
(file:line or a measurement), an effort estimate and a way to prove the change. The findings are
in [report.md](report.md); the scripts and raw numbers in [measurements/](measurements).
The audit was read-only: nothing in the repository was changed.

## Executive summary (top 10, ranked by impact over effort)

1. **Re-check the link scheme on the parsed URI before `openExternal`** (security, high, S).
   `[x](https%3A/../../path)` is classified "external" because the scheme is checked on the
   decoded path but the raw string is opened; `vscode.Uri.parse` turns it into a `file:` URI, so
   one click can open a local file or app, Restricted Mode included
   (`src/core/navigation/previewNavigation.ts:134-141`, `src/host-vscode/vscodeHost.ts:226`).
2. **Patch `computeBlockTightness` of `markdown-it-myst`** (performance, high, S). It splits the
   whole source for every directive fence: 48.6% of the CPU of a 50k-line render. Pre-split the
   lines once (postinstall patch, like `scripts/patch-myst-imports.mjs`, and an upstream PR).
3. **Remove the redundant full-page parse5 cycles of the page assembly** (performance, high,
   S-M). `annotateSourceMappings` (644 ms at 50k lines) duplicates the sanitizer's
   `injectSourceMappings`; `injectContentSecurityPolicy`, `applyTableAlignments`,
   `renderMathHtml` and `planContentPatch` (which re-parses the previous page) each parse and
   serialise the whole page again.
4. **Render only visible previews, once per document, and stop retaining hidden webviews**
   (performance and memory, high, M). Every session renders on its own queue, hidden panels are
   patched too, and `retainContextWhenHidden: true` keeps a 5 MB Mermaid or 3.4 MB PlantUML
   runtime alive per hidden preview (`src/host-vscode/activation.ts:74,194`).
5. **Take the render off the extension-host thread and make it cancellable** (performance,
   high, L). A render is one synchronous block (418 ms per keystroke at 10k lines, 3.5 s at 50k,
   13.5 s at 100k, measured) that no abort interrupts; typing produces back-to-back renders.
   A `worker_threads` renderer plus an adaptive debounce removes the freezes.
6. **Content-addressed caches for the per-block work** (performance, medium, S each):
   highlight.js, KaTeX, `statSync`+`realpathSync` per image, toctree file reads, and an SVG cache
   plus a concurrency limit for the PlantUML JAR (one JVM per diagram per render today).
7. **Harden the sanitizer** (security and robustness, medium, S): quadratic `removeNode`
   (50k removed siblings take 39 s), stack overflow at nesting depth 5,000, `<script src>` kept
   with the page nonce in trusted mode and `nonce` in the attribute allowlist, unescaped KaTeX
   style declarations.
8. **Close the local-file exposure paths** (security, medium, S each): the resource and include
   root is the document's folder when there is no workspace folder or in Restricted Mode (a note
   in `$HOME` can `{include} .ssh/id_rsa`); the PlantUML JAR runs without
   `PLANTUML_SECURITY_PROFILE`; the comments sidecar write follows a dangling symlink; the
   frontmatter path settings are not in `restrictedConfigurations`.
9. **Cut the per-keystroke and per-event fan-out across sessions** (performance, medium, S-M):
   one recursive `**/*` watcher per preview, `onDocumentChanged` doing synchronous `realpathSync`
   for every session on every edit of any file, the stem index invalidated on every `.md` change,
   `findFiles` without excludes, uncapped and unshared linked-target watchers.
10. **Maintainability pack** (medium, S-M): a `Logger` port and a `fireAndForget` helper (8
    `console.error`, 74 `void` calls with 12 `.catch`); one copy each of the fence regex (5
    divergent copies), the front-matter range (5 copies), `escapeHtml` (3) and `escapeRegExp`
    (2); retire the session to node-services debt and the `fileLinks` <-> `okfFrontmatter` cycle;
    split `test/integration/realInput.test.ts` (4,580 lines, 92 scenarios); de-risk the
    postinstall patch; stop shipping the 6.5 MB source map with `sourcesContent`, `docs/` and
    `.claude/` in the VSIX.

What is already good and should stay: `default-src 'none'` CSP with a 144-bit nonce on every
script and style, typed and gated message validation on both sides, realpath-checked include
policy, bounded caches on the host, lazy activation (50 ms to load the bundle), keyed DOM morph
that keeps Mermaid and image nodes, LRU diagram caches on the page, dependency-cruiser layering
with a shrinking exception list, and a file-size ratchet with a single remaining exception.

## Split out

- 2026-10-27: S-01 and S-02 filed as P1 items (`security-link-scheme-open-external`,
  `security-read-only-root-home`) at the user's request, then opened as CRs 132 and 133.
