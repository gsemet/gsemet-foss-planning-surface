# Every Markdown file checks out as LF, whatever the git config

# Every Markdown file checks out as LF, whatever the git config and the OS

The user's request, relayed by the Studio Chief of Staff (2026-11-20): "tu passeras tous les md de
Chantier en LF et tu mettras les settings dans gitattributes pour que ca n'arrive plus quelque soit
la configuration de git et l'OS".

## Why

Studio 1.10.0 gets stuck on "Saving Markdown..." when a block of a CRLF file is left unchanged
(Studio's own fix is queued there as editor-stuck-saving). On the user's Windows checkout
(`core.autocrlf=true`), chantier's Markdown files check out as CRLF: `.gitattributes` forces
`eol=lf` only for a few paths, not for `*.md`.

## What is true today (2026-11-20)

- The index holds all 307 tracked `.md` files as LF (`git ls-files --eol`): the CRLF comes only
  from the checkout's `core.autocrlf=true`.
- `.gitattributes` has `eol=lf` rules for the board's web folder, a few JSON and YAML files and
  the dry-run patches. CR-411 (PR #384) moves the web folder to `clients/web` and edits that file.

## Asked

- A `.gitattributes` rule so every Markdown file is stored and checked out as LF on any OS and git
  configuration: `*.md text eol=lf` at least; the Driver judges whether a repository-wide
  `* text=auto eol=lf` is right, binaries kept binary (fonts, images, archives).
- `git add --renormalize .`, committing whatever it changes (expected: nothing for `.md`).
- Proof: a fresh checkout with `core.autocrlf=true` on Windows gives LF Markdown files
  (`git ls-files --eol` shows `w/lf`).
- Starts after CR-411 is merged (both edit `.gitattributes`).
- When merged, tell the Studio Chief of Staff in one line.

## On hold: the user doubts it (2026-11-20)

The user, after filing: "je ne suis pas sur que ce soit une bonne idee. Markdown studio doit
respecter le format original c'est dans son ADN." Studio must keep a file's line endings as they
are, CRLF included; that is Studio's own fix (editor-stuck-saving), not chantier's. This CR stays
in the inbox, not run, until the user decides.
