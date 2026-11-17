# Coverage note — C4 find and replace in the preview

Budget used: about 36 of 40 driver calls, 1 of 6 screenshots, session c4.

Exercised (all on `synth/tables.md`, `synth/find-mix.md`, small synthetic list fixtures, and
`book/chapters/06-guidelines-governance.md`):
- Cmd+F from the preview, match counting with and without Match case and Whole word, counts compared
  with grep on the source (they agree once matches only in hidden link URLs are discounted, 20/23/22
  on find-mix, 69/46/30 on chapter 06), Enter wraps around.
- Replace one and Replace all in tables (including `\|` cells), inline code, fenced code, GitHub
  alert, MyST note, grid card title and body, list, link text, heading, entity text; exact diff
  against mark; frontmatter match correctly refused. Regex option on a list-only query.
- Undo from the source editor reverts Replace all in one step and the preview follows.
- Bar open while edit mode is on (count kept, buffer unchanged), Replace one with edit mode on.
- No console error in any run.

Observed, not a finding: Cmd+Z with focus in the preview (not in a field) does nothing, so
"replace then undo" works from the source editor only.

Not exercised: invalid regex, Cmd+F while an inline editor field is open with typed text, replace in
MyST directive options/tabs, backslash and `$1` in the replacement, replace across a stale preview
(Refresh message), narrow preview layout, vault documents.
