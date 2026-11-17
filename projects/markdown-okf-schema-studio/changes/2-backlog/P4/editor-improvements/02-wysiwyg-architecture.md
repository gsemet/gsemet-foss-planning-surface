# Architecture Proposal — Single-Pane WYSIWYG MyST Editor

Date: 2026-09-25
Companions: [00-competitive-analysis.md](./00-competitive-analysis.md) ·
[01-improvement-proposal.md](./01-improvement-proposal.md)

Objective: an equivalent of Mark Sharp's single-pane WYSIWYG — React + Lexical + code
highlighting + KaTeX + Mermaid + a component library — **but for MyST, and without Mark Sharp's
fatal flaw of silently rewriting your files.**

This supersedes the "out of scope" note in
[01-improvement-proposal.md](./01-improvement-proposal.md#explicitly-out-of-scope).

---

## 1. The one thing that decides this project

Mark Sharp's user guide contains this warning:

> *"When you edit a markdown file with Mark Sharp, your existing document layout may be altered.
> It is recommended to back up your documents with a version control system."*

That is acceptable for personal notes. It is **not** acceptable for `book/chapters/*.md`, which
are git-tracked, reviewed in merge requests, and governed by a 100-character wrapping rule in
[AGENTS.md](../../../../AGENTS.md). A lossy round trip would turn every one-word fix into a
500-line diff.

So the central engineering problem is **not** the editor. It is **round-trip fidelity**. Everything
below is organised around it, and §7 proposes a cheap, decisive spike that must pass before any
editor code is written.

---

## 2. Stack

| Layer | Choice | Rationale |
|---|---|---|
| **Editor core** | **Lexical** (`lexical`, `@lexical/react`, `@lexical/rich-text`, `@lexical/list`, `@lexical/table`, `@lexical/link`, `@lexical/selection`, `@lexical/utils`) | Same as Mark Sharp. Immutable `EditorState`, transactional updates, incremental DOM reconciliation, first-class `DecoratorNode` for embedding React |
| **UI framework** | **React 18** | Required by `@lexical/react` and by decorator nodes |
| **Component library** | **Fluent UI v9** (`@fluentui/react-components`) | As requested; matches VS Code's visual idiom. See §2.1 for the caveat |
| **MyST parsing** | **`mystmd`** — `myst-parser`, `myst-transforms`, `myst-spec`, `myst-to-html` | ⭐ The critical enabler: a real TypeScript MyST implementation from the Executable Books team, producing a `myst-spec` AST (an mdast superset) with directive and role support |
| **Markdown serialization** | `mdast-util-to-markdown` + custom MyST directive/role handlers | Export side; must be configured to match our house style (§4.2) |
| **Syntax highlighting** | **Shiki** (`shiki`, `@shikijs/core`) with a **Prism** fallback | Shiki uses the *same TextMate grammars and themes as VS Code*, so code blocks match the editor exactly. Prism is lighter if bundle size bites |
| **Math** | **KaTeX** | Synchronous, small, no CDN — passes our CSP as a staged local asset |
| **Diagrams** | **Mermaid** (lazy chunk) | Replaces the `mmdc` CLI spawn entirely |
| **Frontmatter** | `yaml` | Same as Mark Sharp |
| **Bundler** | **esbuild** (recommended) or webpack 5 | See §2.2 |
| **Host integration** | `CustomTextEditorProvider` | See §3 — this is the single most important host-side decision |

All licences are MIT/Apache-2.0/ISC. No new legal review needed.

### 2.1 Caveat on Fluent UI

Fluent UI v9 is the closest match to Mark Sharp and to VS Code's idiom, but it adds roughly
300 KB gzipped and carries its own theming system, which must then be bridged to the `--vscode-*`
CSS custom properties we already rely on in
[previewStyles.ts](../../../../src/preview/previewStyles.ts).

Recommendation: use Fluent UI **only** for the genuinely complex chrome — the slash-command
palette, context menus, the table toolbar, dialogs. Render document content with plain semantic
HTML styled by `--vscode-*` tokens, exactly as the current preview does. This keeps the document
surface theme-faithful and lets Fluent UI be a lazily-loaded chunk.

### 2.2 Caveat on webpack

Mark Sharp uses webpack; it works. But our repo has no webpack anywhere today, and the extension
currently builds with a bare `tsc -p .` in well under a second. Introducing webpack means a new
config, new loaders, and a slow watch loop.

**Recommendation: esbuild.** One `build.mjs`, sub-second bundles, native TS/JSX, code splitting for
the Mermaid and Fluent UI chunks, and it keeps `just vscode-sphinx-liveview-dev` snappy. If a
webpack-specific feature is later required (module federation, an exotic loader), migrating is
mechanical. Webpack 5 remains an acceptable fallback if the team prefers the familiarity.

---

## 3. Host integration — use `CustomTextEditorProvider`

**This is the decision that prevents an entire class of bugs.**

`CustomTextEditorProvider` (as opposed to the binary `CustomEditorProvider`) keeps VS Code's
`TextDocument` as the single source of truth. We get, for free and correct:

- undo / redo (including across a mode switch),
- dirty state, save, save-as, hot exit,
- git integration, diff view, timeline,
- multi-editor consistency (the same file open in the text editor and the WYSIWYG stay in sync),
- `workspace.applyEdit` participation, so formatters and other extensions still work.

Data flow:

```
TextDocument ──onDidChangeTextDocument──► host ──postMessage{documentChanged}──► webview
                                                                                   │
                                                                          import / patch AST
                                                                                   │
                                                                          Lexical EditorState
                                                                                   ▼
                                                                                 paint

user types in webview
      │
Lexical update → dirty subtree → serialize → minimal text diff (`diff` / `fast-diff`)
      │
postMessage{edit: [{range, newText}]} → host → WorkspaceEdit.replace → TextDocument
```

Echo suppression uses the mechanism already proven in
[scrollSync.ts](../../../../src/webview/scrollSync.ts): tag each
host→webview change with the originating edit id and ignore our own round trip.

**Critically: we never write the whole file.** We compute a minimal diff from the *dirty subtree
only* (§4.3), so untouched regions are byte-for-byte preserved. This is what Mark Sharp does not
do, and it is why Mark Sharp has to warn its users.

---

## 4. Document model and round-trip fidelity

### 4.1 Import

```
markdown text
  └─ myst-parser  →  myst-spec AST (mdast + directives + roles), every node carrying `position`
      └─ myst-transforms (admonitions, math, cross-references, footnotes)
          └─ astToLexical()  →  Lexical node tree
```

Every Lexical node stores two extra fields:

| Field | Purpose |
|---|---|
| `sourceRange: {startOffset, endOffset}` | Exact byte span in the original document — drives minimal diffing and cursor mapping |
| `rawSource: string` | The verbatim original text for this node |

### 4.2 Export

`lexicalToAst()` → `mdast-util-to-markdown` with MyST directive/role handlers, configured for our
house style: `-` bullets, ATX headings, fenced code, and — non-negotiable —
**100-character prose wrapping at clause boundaries**, per
[documentation.guideline.md](../../../guidelines/documentation.guideline.md). This is not a
built-in option and will need a custom `join`/`handlers` layer or a post-serialization rewrap pass
reusing the logic behind the `rewrap-markdown` skill.

### 4.3 Dirty-subtree serialization — the core safety mechanism

On every edit:

1. Lexical reports which nodes changed (`editor.registerUpdateListener` → `dirtyElements`,
   `dirtyLeaves`).
2. Walk up to the nearest **block** ancestor with an intact `sourceRange`.
3. Serialize **only that block**.
4. Emit a `WorkspaceEdit` replacing exactly `sourceRange` with the new text.
5. Shift the `sourceRange` of all following siblings by the length delta.

Consequence: a node the user never touched is never re-serialized, so it cannot be reformatted.
The blast radius of any serializer imperfection is bounded to the paragraph being edited.

### 4.4 Unsupported constructs — the escape hatch

The MyST long tail is large: `{animation}`, `{bibliography}`, `sphinx-design` grids and dropdowns,
`{include}`, `{only}`, arbitrary Sphinx extensions. Rather than attempt full coverage:

- Any construct without a first-class Lexical node becomes a **`RawBlockNode`** — an atomic,
  non-editable `DecoratorNode` holding `rawSource` verbatim.
- It renders as a read-only card showing either a rendered preview (when the renderer knows how)
  or the source with a "edit in text mode" affordance.
- It serializes back as *exactly* `rawSource`. Zero mutation risk.

This lets us ship with partial coverage and expand node-by-node, and it guarantees that an unknown
directive can never be corrupted.

---

## 5. Rendering the MyST semantics Sphinx gives us today

The preview's real value is Sphinx's *semantic* resolution: citation labels, cross-reference
titles, glossary terms, figure numbering. None of that can run per keystroke. Solution: decouple
resolution from rendering via a **semantic index**.

```
book/refs.bib, book/chapters/*.md, book/glossary-definitions.yml
  └─ indexer (reuse the existing Python pipeline, or a light TS pass)
      └─ .vscode-myst-index.json   { citations, labels, terms, docTitles, figureNumbers }
```

- Built in the background on activation, then refreshed on save / file-watch / idle — **never on
  keystroke**.
- The webview resolves `{cite}`, `{ref}`, `{doc}`, `{term}`, `{numref}` against it in O(1).
- Unresolved references render with a muted dotted underline rather than a diagnostic banner —
  the fix already proposed as T2-6 in
  [01-improvement-proposal.md](./01-improvement-proposal.md#t2-6--cross-document-references).

### 5.1 Node inventory

| MyST construct | Lexical node type | Renderer |
|---|---|---|
| Paragraph, heading, list, quote, link, emphasis | Built-in Lexical nodes | Native |
| Table | `@lexical/table` | Native + Fluent UI toolbar |
| Code block | `CodeBlockNode` (Decorator) | Shiki, lazy language loading |
| Inline / block math | `MathNode` (Decorator) | KaTeX |
| Mermaid | `MermaidNode` (Decorator) | Mermaid, lazy chunk, theme from VS Code |
| Admonition / GitHub alert | `AdmonitionNode` (Element, editable children) | React + the CSS from T2-2 |
| `{figure}` / `{image}` | `FigureNode` (Decorator) | `asWebviewUri`, existing resource policy |
| `{cite}` / `{ref}` / `{term}` | `RoleNode` (Decorator, inline) | Semantic index lookup |
| Frontmatter | `FrontmatterNode` (Decorator) | Collapsed YAML card |
| Footnote | `FootnoteNode` | Native + a references section |
| **Anything else** | **`RawBlockNode`** | Read-only card (§4.4) |

---

## 6. Fidelity oracle — the feature Mark Sharp cannot have

The existing Sphinx pipeline does not get deleted. It is **repurposed as a verifier**.

On idle (or on save), run the real Sphinx build in the background — by then it is free, since it
is off the interactive path — and compare its structural output against what the WYSIWYG rendered:
heading tree, admonition types, resolved reference count, figure count, diagnostic set.

On divergence, show a status-bar badge: *"Preview differs from build — 2 unresolved references"*,
with a command to open the authoritative Sphinx render.

This converts our current liability (a slow, heavyweight renderer) into a differentiator: **a
WYSIWYG that tells you when it is lying.** With T1-3's persistent worker, the verification build
costs nothing the user can perceive.

---

## 7. Phasing — and the gate that must pass first

### Phase A — Fidelity spike ⭐ **do this before anything else** · Size: S

A standalone script, no editor, no UI:

```
for each book/chapters/*.md:
    parse with myst-parser → AST
    serialize with the configured mdast-util-to-markdown
    assert byte-identical to the original
```

**Gate: 100 % byte-identical across every chapter.** Report the per-construct failure histogram.

This is decisive. If the round trip mangles our real content, the honest answer is that a
full WYSIWYG is not viable for this repo and we stop — having spent very little. If it passes,
every subsequent phase rests on solid ground. There is no reason to write editor code before this
number is known.

### Phase B — Read-only Lexical renderer · Size: L

Render-only single pane: `myst-parser` → Lexical → React, no editing, no serialization, therefore
**zero write risk**. Replaces the Sphinx preview for documents whose constructs are fully covered;
falls back to the existing Sphinx preview otherwise (a one-line decision, since both live in the
same extension).

Instant, complete elimination of the latency problem for the common case — a keystroke becomes a
Lexical reconcile, exactly as in Mark Sharp. Ships the KaTeX, Shiki, Mermaid and admonition wins
from Tier 2 as a side effect.

### Phase C — Editing, safe subset · Size: L

Enable editing for text, emphasis, headings, lists, links, quotes. Everything else stays a
`RawBlockNode`. Dirty-subtree serialization (§4.3) active. Behind
`sphinxMystLiveview.experimental.editing`, default off.

### Phase D — Rich editing · Size: XL

Tables, slash commands, admonition insertion, image paste/drop, footnotes, drag handles,
collapsible headings, cursor-preserving mode switching (`sourceRange` makes this straightforward).
Fluent UI chrome lands here.

### Phase E — Consolidation · Size: M

Sphinx preview becomes the fidelity oracle and the export path only. Reading/presentation mode,
outline, width and font settings (T2-7, T2-8) land in the Lexical surface.

---

## 8. Relationship to the Tier 0 work

**Do not serialize these.** The Tier 0 items in
[01-improvement-proposal.md](./01-improvement-proposal.md#tier-0--stop-the-bleeding-no-architecture-change)
— killing the triple webview reload, the spawn timeout, the watcher scope — are a few days of work
and remove most of today's pain. Phase A is a spike that one person can run independently.

Recommended order:

1. **Ship Tier 0 now.** It is cheap, it is safe, and it fixes the extension people are using today.
2. **Run Phase A in parallel.** It is the decision gate.
3. **Fix the three rendering bugs** (math, `{only}`, `{animation}` — T2-1, T1-2, T2-5). They are
   worth doing regardless of which architecture wins, and math/Mermaid work is directly reusable
   in Phase B.
4. **Commit to Phase B only if Phase A passes.**

Committing to an XL editor rewrite before the fidelity number is known would be the single
riskiest thing we could do here.

---

## 9. Risk register

| Risk | Severity | Mitigation |
|---|---|---|
| **Round trip mutates git-tracked chapters** | **Critical** | Phase A gate; dirty-subtree serialization (§4.3); `RawBlockNode` escape hatch (§4.4); a pre-commit check that the WYSIWYG never touched bytes outside the edited range |
| JS MyST (`mystmd`) diverges from Python MyST (`myst-parser`) | High | The fidelity oracle (§6) surfaces divergence continuously; pin both and test the delta in CI |
| 100-char wrapping rule vs. serializer output | High | Custom rewrap pass reusing the `rewrap-markdown` logic; asserted in Phase A |
| MyST long tail never fully covered | Medium | `RawBlockNode` makes partial coverage safe and shippable; expand node types on demand |
| Bundle size / webview startup (React + Lexical + Shiki + Mermaid + Fluent UI) | Medium | Code splitting: Mermaid, Fluent UI and Shiki grammars as lazy chunks. Target < 400 KB gzipped for the initial chunk. `retainContextWhenHidden` already set |
| CSP vs. dynamic `import()` of chunks | Low | Chunks are local staged assets under `localResourceRoots`; `script-src ${cspSource} 'nonce-…'` already permits them. `connect-src 'none'` stays |
| Effort is XL and the team is small | High | Phases B–E are independently shippable and independently abandonable; Phase B alone justifies the work |
| Two renderers to maintain | Medium | Intentional and bounded — Sphinx becomes the oracle and the export path, not a second UI |

---

## 10. Recommendation

Build it — **but gate it on Phase A**, and ship Tier 0 first so that today's users stop suffering
while the spike runs.

The strategic case is strong: a single-pane MyST WYSIWYG with a build-accurate fidelity oracle is
something no one else ships. Mark Sharp cannot follow us into MyST, and the Sphinx ecosystem has
nothing resembling a WYSIWYG. But the value depends entirely on the editor being trustworthy with
a git-tracked book, and that is a measurable property we can determine cheaply, before committing.
