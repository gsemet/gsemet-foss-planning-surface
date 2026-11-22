# Privacy pass, CR-447, head 4c99436

Verdict: CLEAN.

- PNGs: 37 under docs/web-board/ (the 33 changed plus the rest of the folder) scanned for chunks with a python -I script: every file has only IHDR, IDAT, IEND. No tEXt, iTXt, zTXt, eXIf, no other ancillary chunk. Nothing non-trivial.
- Viewed: home-pc, writer-pc, config-pc, picker-pc, panel-pc, help-pc, project-pc, editor-pc, costs-pc, new-pc, batch-graph-pc, home-phone, writer-phone. All show the synthetic demo data (planning-surface, shop-api, mobile-app, docs-portal; path /home/demo/planning-surface; upstream github.com/demo/planning-surface; CR-14x). No Windows path, no real username, no email, no ?k= link or key text, no token. The other PNGs come from the same demo app and were not each opened (not viewed: the remaining phone and pc variants).
- SVGs: grep of docs/*.svg (including surface-server.svg and the 5 changed others) for gaeta, Users/, C:\, emails, ?k=, token, secret, /home/, password: no match.
