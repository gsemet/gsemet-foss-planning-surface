Owner, 2026-11-20 (via the chantier Chief of Staff): "change markdown-lf-everywhere en juste une md
qui passe les md du projet Studio en LF + gitattributes, mais assure toi que les test soient bien
fait". And earlier: "Markdown studio doit respecter le format original c'est dans son ADN."

Checked by the Studio Chief of Staff, main dd89211d: `.gitattributes` already has
`* text=auto eol=lf` and the Studio Markdown files are LF. But the rule also turns the CRLF
fixture `.agents/skills/markdown-studio-exploratory-qa-claude/assets/synth/crlf-source.md` into LF
(`git ls-files --eol`: i/lf w/lf), so QA scenario ux-35 "crlf inline edit" tests an LF file and
proves nothing.

Done when:
- CRLF test fixtures stay CRLF whatever the git config and OS (a `.gitattributes` rule naming them
  `eol=crlf`), and a test fails if a CRLF fixture holds no `\r\n`;
- save tests on CRLF, LF and mixed documents keep every untouched byte and line ending, and never
  stay on "Saving Markdown...", each shown to fail before the fix.

Goes with `editor-stuck-saving` (P1): its end-to-end CRLF tests need these fixtures. Run them in
the same batch, this one first or as one stack.
