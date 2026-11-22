# Markdown stored LF, CRLF fixtures kept CRLF and really tested

# Markdown files stored LF, CRLF fixtures kept CRLF and really tested

The user's request (2026-11-20), moved here from chantier's inbox: "change markdown-lf-everywhere en
juste une md qui passe les md du projet Studio en LF + gitattributes, mais assure toi que les test
soient bien fait". The user's rule stands: "Markdown studio doit respecter le format original c'est
dans son ADN": Studio keeps each file's line endings, CRLF included.

## What is true today (2026-11-20, read by the chantier Chief of Staff at Studio's main checkout)

- `.gitattributes` already starts with `* text=auto eol=lf`, and `git ls-files --eol` shows all
  1446 tracked `.md` files as `i/lf w/lf` (one empty file, `i/none`). The LF part is done.
- **The gap:** the same rule turns Studio's CRLF fixtures into LF.
  `.agents/skills/markdown-studio-exploratory-qa-claude/assets/synth/crlf-source.md` is
  `i/lf w/lf`, so scenario `ux-35-crlf-inline-edit-keeps-all-keys` edits an LF file and proves
  nothing about CRLF. `test/core/render/crlfAlerts.test.ts` is sound: it builds its CRLF text in
  memory (`replaceAll("\n", "\r\n")`).
- The bug that started this: Studio 1.10.0 stays on "Saving Markdown..." when a block of a CRLF
  file is left unchanged (Studio's editor-stuck-saving).

## Asked

- Keep the repository rule (`* text=auto eol=lf`): every Markdown file stored and checked out LF on
  any OS and git config; `git add --renormalize .` at the end, committing what it changes.
- Every CRLF fixture keeps its CRLF bytes whatever the checkout: a `.gitattributes` line for them
  (`-text`, or `eol=crlf`, placed after the general rule), the fixtures re-committed as CRLF, and a
  test that fails if a fixture named CRLF holds no `\r\n`.
- Tests that prove Studio keeps the original format, on a CRLF document: open, edit one block, leave
  another unchanged, save: the save ends (no stuck "Saving Markdown..."), the edited block is saved,
  every other byte is unchanged and every line ending stays CRLF; the same for LF and for a file
  with mixed endings. Each test is shown to fail on the code before the fix (or on a planted LF
  fixture).
- Scenario ux-35 rerun on a real CRLF file.
