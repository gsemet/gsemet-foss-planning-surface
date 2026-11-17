# Behaviour change note: alert lazy continuation follows CommonMark

## GitHub's real rendering (cited)

Rendered through the GitHub Markdown API, `gh api markdown -f mode=gfm -f text=...`, on 2026-10-31.
Raw outputs: /private/tmp/claude-502/cr223-driver/gh-render.html, gh-render2.html, gh-edge-cases.txt.

| Input | GitHub |
| --- | --- |
| `> [!NOTE]` / `> Line one of a note.` / `lazy continuation line of the note.` | one Note alert; its paragraph holds both lines |
| `> [!TIP]` / `> first` / `Second` | one Tip alert; `Second` inside |
| `> [!NOTE]` / `lazy right after head` | inside the alert |
| `> [!NOTE]` / `> a` / `b` / `c` / `> d` | one alert, a b c d in one paragraph |
| `> [!NOTE]` / `> a` / `    indented lazy` | inside (paragraph continuation) |
| `> [!NOTE]` / `> a` / blank / `b` | `b` outside |
| `> [!NOTE]` / `> a` / `- item` | list outside (a list item cannot continue a paragraph) |
| `> [!NOTE]` / `> # head` / `b` | `b` outside (lazy needs an open paragraph) |
| `> [!NOTE]` / `> a` / `> [!WARNING]` / `> b` | ONE Note alert, `[!WARNING]` is literal text |

This is CommonMark 0.31.2 section 5.1 (Block quotes), "laziness" rule and examples 233-235, 238
(e.g. `> bar` / `baz` / `> foo` is one block quote with one paragraph); GitHub follows it for alerts.

## Today

The alert box stops at the last `>` line: the lazy line renders as a paragraph below the box, the
block editor covers the quoted lines only (data-end-line 2 for `> [!NOTE]\n> a\nb`). The palette sees
the lazy line as outside the alert: Alert on `Second` inserts `> [!NOTE]\n> Second` right under the
TIP alert, and picking WARNING then rewrites the TIP head: `> [!WARNING]\n> first\n> [!NOTE]\n> Second`.

## After

Like GitHub: a lazy line that continues the alert's open paragraph is inside the box and inside the
alert's block editor (data-end-line covers it). One shared "alert range" rule feeds the render pass
and the palette. In the palette, the caret on a lazy line is "in the alert" (Alert opens the type
list without an edit; a type changes the head of that alert, the one drawn around the line).
