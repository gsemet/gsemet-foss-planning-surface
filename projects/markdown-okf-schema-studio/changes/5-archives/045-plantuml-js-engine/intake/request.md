# 045 — plantuml-js-engine

From backlog `P3/plantuml-js-renderer` (`01-analysis.md` here: the spec basis, option (b)).

## Problem

PlantUML needs Java + plantuml.jar and one JVM per diagram per render (slow, security findings
SEC-01/SEC-02/STAB-04/PERF-03). The official JavaScript engine (`@plantuml/core`, MIT) removes it.

## Decisions (user grill, 2026-10-23)

1. Built-in JavaScript engine by default, bundled into the webview like Mermaid (esbuild),
   following the analysis section 5. Adding the npm dependency `@plantuml/core` is ALLOWED for
   this CR (pinned exact version, lockfile updated; that is the only install allowed).
2. A checkbox setting chooses the jar: boolean, e.g. `markdownOkfSchemaStudio.plantuml.useJar`,
   default `false` = built-in engine. `true` = the existing jar/PATH pipeline (`jarPath`
   unchanged). Main-session interpretation: existing `jarPath` users get the built-in engine until
   they tick the box; say it clearly in CHANGELOG and README (user may correct).
3. Restricted Mode (untrusted workspace): the built-in engine is ENABLED there (no local file
   `!include`, no network); the jar stays disabled there.
4. No network by default (no `connect-src` to plantuml servers); unsupported features show a clear
   message with a hint to tick the jar option. CSP changes kept minimal and documented.
5. Tests: unit (setting resolution, untrusted), visual scenarios for a rendered diagram with the
   built-in engine (light + dark) and the unsupported-feature message; existing jar tests keep
   passing unchanged.
6. Speed: Opus everywhere, reviewer on the round diff, ready when `checks` is green. Rounds: 3.
7. PR written for an external reader.

## Decisions 8–10 (user, 2026-10-23 ~17:00, after reading PR #39) — scope added to the same PR

8. Support `{uml} path/to/diagram.puml` (sphinxcontrib-plantuml form, MyST directive whose argument
   is the diagram file; also accept `{plantuml} path.puml` if the directive body is empty). The
   file is read by the extension host under the same rules as `{include}` (workspace / document
   bounded, size cap, reuse the existing include budget and resource policy), rendered by the
   active engine (built-in or JAR). The preview re-renders when that file changes on disk (like
   `{include}` dependencies). Clear message for a missing file or a path outside the bounds.
9. Support local `!include` / `!include_many` / `!include_once` / `!includesub` (file paths) in the
   built-in engine: the webview's `PLANTUML_FILE_LOADER` asks the host for the file through a
   message; the host applies the same bounds and cap; nested includes resolve relative to the
   including file; a depth/count limit stops cycles. In Restricted Mode only files in the open
   document's folder (and below) are served. Dependencies are watched for re-render.
10. Still refused in the built-in engine (message keeps pointing to `useJar`): URL includes
    (`!includeurl`, `!include http…`), the standard library (`!include <…>`), `!import`, and
    `!theme … from`. No network, CSP unchanged.
Tests: unit (path resolution, bounds, Restricted Mode, cycle limit, message protocol), visual
scenarios for `{uml} file.puml` and a diagram with a local `!include` (light + dark), the
unsupported message now for a URL/stdlib include only. Docs: README PlantUML section with both
syntaxes; PR body updated (Summary, Changes, screenshots). This is round 2 of 3.

## Decision 11 (user, 2026-10-23 ~17:30)

"rebase et merge quand ce sera fini CR 045": once round 2 is reviewed (APPROVE), rebased on
origin/main and the required `checks` is green, the MAIN SESSION merges PR #39 (rebase merge).
The user authorised this merge only. Then rebase every remaining CR and open their PRs.
