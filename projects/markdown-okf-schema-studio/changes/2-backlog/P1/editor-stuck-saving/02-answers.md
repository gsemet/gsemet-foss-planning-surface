Short name: `stuck-saving`

1. stuck-saving-Q1: **Fix approved (owner, 2026-11-20).** "je suis d'accord pour le fix. il faut
   respected le format utilisé par le fichier. il faudra que tu tests bien ces cas en e2e"
   - Studio keeps the file's own line endings (CRLF stays CRLF, LF stays LF) on every edit path:
     the page compares and posts text in the file's line ending; the host always answers a final
     save or cancel, even when nothing is written.
   - The cases are tested end to end (real VS Code window), on CRLF and LF files: a multi-line
     paragraph, a list item with nested items, a list's last item, left unchanged by Done,
     Ctrl+Enter, a click on another block, arrow past the edge, and type-then-delete; plus a real
     change in a CRLF file that must stay CRLF.
2. stuck-saving-Q2: **Chantier's own files (owner, same message).** "puis tu passeras tous les md de
   Chantier en LF et tu mettras les settings dans gitattributes pour que ca n'arrive plus quelque
   soit la configuration de git et l'OS". Not part of this Studio CR: sent to the chantier Chief of
   Staff (convert chantier's Markdown files to LF, add an `eol=lf` rule in its `.gitattributes`).
3. stuck-saving-Q3: **Chantier's LF change on hold (owner, via the chantier Chief of Staff,
   2026-11-20).** "Markdown studio doit respecter le format original c'est dans son ADN." Chantier
   keeps its CRLF checkouts; its CR markdown-lf-everywhere waits in its inbox. This CR must handle
   CRLF files fully and leave their line endings unchanged; the e2e tests above are the proof.
