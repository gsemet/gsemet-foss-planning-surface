# Competitive Analysis — Mark Sharp vs. `markdown-okf-schema-studio`

Date: 2026-09-25
Subject: <https://www.marksharp.co/> (VS Code extension `jonathan-yeung.mark-sharp`)
Scope: rendering and perceived performance only. Direct/WYSIWYG editing is explicitly out of scope.

---

## 1. What Mark Sharp actually is

**It is not written in Rust.** That hypothesis is disproved by the vendor's own
[acknowledgements.md](https://github.com/jonathanyeung/mark-sharp/blob/main/acknowledgements.md),
which lists the complete third-party dependency set. It is a **TypeScript + React webview bundled
with webpack**, and the speed comes entirely from its architecture, not from a native language.

Reconstructed stack, from the published acknowledgements:

| Layer | Library | Role |
|---|---|---|
| Editor core | **Lexical** (Meta) | Document model + incremental DOM reconciliation |
| UI | **React**, **Fluent UI**, `immer` | Chrome, menus, slash-command palette |
| Syntax highlighting | **Prism.js** | Per-code-block, client-side |
| Math | **KaTeX** | Client-side typesetting |
| Diagrams | **Mermaid JS** | Client-side rendering |
| Markdown / data | `yaml`, `luxon`, `diff`, `nunjucks`, `tinycolor2` | Frontmatter, dates, dirty-diffing, templating, theming |
| Build / DI | webpack, Babel, `ts-loader`, `tsyringe`, `reflect-metadata` | Bundling, dependency injection |
| Telemetry | `axios`, `web-vitals` | Usage + performance reporting |

Distribution: closed source. The public GitHub repo contains **only** `README.md`, `user-guide.md`,
`CHANGELOG.md`, `acknowledgements.md`, `licensing-and-activation.md`, `telemetry.md` — no `src/`.
Freemium: free tier is render + basic slash commands; a $12 perpetual licence unlocks tables,
Mermaid, images, theming, presentation mode, draggable blocks. 32,778 installs, 4.7★, 91 open
issues, single maintainer, v1.12.2.

### 1.1 Why it is fast — the real reason

Mark Sharp is a **single-pane WYSIWYG custom editor**. Markdown is parsed **once** when the
document is opened and serialized back **once** when it is saved. In between, the Lexical
`EditorState` *is* the document; a keystroke mutates a node and Lexical reconciles only the
affected DOM subtree.

Per keystroke, Mark Sharp does:

```
keystroke → Lexical command → EditorState transaction → reconcile changed nodes → paint
```

There is **no renderer**. No process spawn, no HTML generation, no document reload, no
serialize/parse round trip. The cost is a sub-millisecond DOM diff. Prism, KaTeX and Mermaid run
lazily, in-page, per changed block — they never re-process the whole document.

By contrast, our extension per keystroke does:

```
keystroke → 250 ms debounce → stage sources to disk → spawn `uv run sphinx-build`
          → full Sphinx build (~1.0–1.2 s) → read HTML → 3× parse5 parse/serialize
          → re-sanitize every stylesheet to disk → 3× full `panel.webview.html` reassignment
```

**The gap is architectural, not a matter of tuning.** Mark Sharp is fast because it renders an
*approximation* of Markdown from an in-memory model. We are slow because we render the *actual
build artifact* through the real toolchain.

### 1.2 What it deliberately cannot do

- **No MyST.** GFM only. No directives, no roles, no `{cite}`, no `{only}`, no `{include}`,
  no cross-references, no bibliography, no glossary, no Sphinx extensions.
- **It rewrites your file.** The user guide warns: *"your existing document layout may be
  altered… it is recommended to back up your documents with a version control system."* A
  round trip through Lexical normalizes list markers, table alignment, and line breaks.
- **No fidelity guarantee.** What you see is Mark Sharp's interpretation, not what CI will
  publish.

This is precisely the trade we must not make. Our value proposition is *fidelity to the book
build*. The goal is therefore **to keep Sphinx as the source of truth while removing its cost
from the interactive path** — not to replace it.

---

## 2. Feature comparison — rendering only

Legend: ✅ works · ⚠️ partial or degraded · ❌ absent or broken

| Capability | Mark Sharp | Ours today | Notes |
|---|---|---|---|
| Headings, lists, emphasis, links | ✅ | ✅ | |
| Tables | ✅ | ✅ | |
| Task lists, strikethrough | ✅ | ✅ | MyST `tasklist`, `strikethrough` |
| Footnotes | ✅ | ✅ | |
| Frontmatter | ✅ styled block, `title`/`created` promoted | ✅ plain field list | Cosmetic gap |
| **GitHub alerts** `> [!NOTE]` | ✅ icon + accent colour | ✅ | We pre-expand to `:::{note}` |
| **MyST admonitions** | ❌ | ✅ | **Our advantage** |
| **Admonition visual polish** | ✅ icons, tight spacing, themed accents | ⚠️ accent colours only, no icons | **Gap the user called out** |
| **Code blocks** | ✅ Prism, client-side, incremental | ✅ Pygments, server-side, whole-doc | Ours is more accurate, far slower |
| **Code block polish** | ✅ themed to VS Code, clean chrome | ⚠️ no language badge, copy button unverified | **Gap the user called out** |
| Math | ✅ KaTeX | ❌ **raw TeX shown as text** | MathJax CDN script stripped by CSP policy |
| Mermaid | ✅ client-side, themed from VS Code | ⚠️ `mmdc` CLI spawn per diagram per build | Very expensive; fails if `mmdc` absent |
| Images / figures | ✅ drag-drop | ✅ `{figure}`, `{image}`, `srcset`, `{include}` | Ours is richer |
| HTML blocks | ✅ rendered + editable | ⚠️ sanitized (scripts/styles stripped) | Intentional |
| Wikilinks | ✅ | ❌ | Not used by the book |
| **Outline panel** | ✅ native VS Code view + hover preview | ❌ (sidebar stripped by design) | Cheap win via `DocumentSymbolProvider` |
| Collapsible headers | ✅ synced with editor folds | ❌ | |
| **Presentation / reading mode** | ✅ (premium) | ❌ | |
| **Document width / font settings** | ✅ `letter` / `fullPage`, font size + family | ❌ | Cheap CSS-variable work |
| Theme fidelity to VS Code | ✅ (premium: full theme match) | ⚠️ partial via `--vscode-*` tokens | |
| `{cite}` + bibliography | ❌ | ✅ | **Our advantage** |
| `{only}` / conditional content | ❌ | ⚠️ **inverted** — `latex` tag wrongly set | One-line bug |
| `{animation}` directive | ❌ | ❌ **inert** — script stripped, no poster | Poster PNGs already exist |
| Cross-document `{ref}`/`{doc}` | ❌ | ⚠️ broken — only `index.md` is staged | Surfaces as xref warnings |
| Glossary / `{term}` | ❌ | ⚠️ glossary excluded by the `{only}` bug | |
| sphinx-design, copybutton, togglebutton | ❌ | ✅ | **Our advantage** |
| Scroll sync | ✅ single-pane, so N/A | ✅ server-anchored, block-granular | Ours is genuinely good |
| Scroll position survives a render | ✅ N/A | ⚠️ re-applied from stale state, can snap | |
| Flicker while typing | ✅ none | ❌ 3 document reloads per keystroke | **Dominant UX defect** |

---

## 3. Measured cost breakdown of our hot path

| Stage | Cost | Avoidable? |
|---|---|---|
| Debounce | 250 ms | Tunable, but it is hiding the build cost |
| `uv run` spawn + Python interpreter start | ~45 ms + interpreter | Yes — persistent worker |
| Import 12 Sphinx extensions (`revealjs`, `confluencebuilder`, `tippy`, `mermaid`, …) | large fixed cost | Yes — preview-only `conf.py` |
| `conf.py` side effects (read `release.yml`, `abstract.txt`, register 3 pybtex plugins) | per render | Yes — worker holds them warm |
| bibtex parse of `refs.bib` | per render, partially cached | Yes — worker |
| Doctree read/write, Shibuya template render, `_static` re-copy | per render | Partially |
| **Total Sphinx** | **~1.0–1.2 s** | → target < 200 ms with a worker |
| parse5 parse + walk + serialize ×3 | tens of ms | Yes — single pass |
| Re-read + re-sanitize + rewrite every stylesheet to disk | every render, uncached | Yes — mtime cache |
| **3× full `panel.webview.html` reassignment** | full document reload ×3 | **Yes — postMessage patch** |

Two independent problems are being conflated by users as "slow":

1. **Latency** — the ~1.2 s Sphinx build. Architectural; needs a worker process.
2. **Flicker / unresponsiveness** — three full webview document reloads per keystroke
   (`debouncing` → `building` → `ready`), each discarding and rebuilding the DOM and
   re-applying a possibly stale scroll position. **This is independent of Sphinx and is
   almost certainly what makes the preview feel broken compared to the stock Markdown
   preview.** It is also the cheapest thing to fix.

---

## 4. Strategic conclusion

We should not chase Mark Sharp's architecture. We should:

1. **Remove every non-Sphinx cost from the hot path** (webview reloads, CSS re-sanitization,
   redundant parse passes). This alone should close most of the perceived gap.
2. **Amortize Sphinx** via a preview-only configuration and a persistent worker, targeting
   sub-200 ms.
3. **Adopt Mark Sharp's *presentation* wins** — admonition icons, code-block polish, outline,
   reading mode, width/font controls — which are pure CSS and cheap.
4. **Fix the three outright rendering bugs** (math, `{only}` tags, `{animation}` poster) that
   currently make us *less* capable than a GFM-only competitor on documents we are supposed
   to own.

The detailed plan is in [01-improvement-proposal.md](./01-improvement-proposal.md).
