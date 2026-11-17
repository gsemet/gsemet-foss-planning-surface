# Coverage note C6 (front matter and properties)

Exercised (synth/frontmatter-edge.md, synth/broken.md, synth/vault-props.md, ws-c6 copy): number,
text with trailing comment, folded `>-` and literal `|` block edits (diff is one scalar's lines; the
folded value is rewritten on one line), checkbox toggle, enum/date/list/object editors opening and
Escape, custom-key add (plain and `a: b`, quoted correctly), remove field, x-okf-link list edit,
invalid-YAML display and live recovery by typing `]`, schema-less Obsidian-style properties table.

Not exercised: field rename (no such feature in `src/page/features`), successful enum/date/object
commits, OKF requirement files and `fixtures-visual` OKF fixtures, real vault notes, marker line
navigation and tooltips of x-okf-link, required-field removal.

Note: after the first rejected commit the editor is stranded (c6-1), so scenarios must re-click.
