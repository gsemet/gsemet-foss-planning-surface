# Diagrams show the surface server: board, hub, writer, watchers

The user (2026-11-22), after the Chief of Staff explained the server's role: "C'est très intéressant la description du rôle du serveur, tu peux mettre à jour le svg ?"

No diagram of docs/ shows the surface server today: how-chantier-works.svg draws the CLI as one box (CR lifecycle, Limits, Sync); planning-modes.svg names the writer in one line.

What to draw (from the explanation given to the user):
- The planning folder is the only truth: plain JSON and Markdown, edited by the CLI, the agents, git and the user. The server keeps no database.
- The server holds each project's state in memory, keyed by a fingerprint of the folder (a stat walk, no file opened): an unchanged project answers "unchanged" with no read.
- The OS tells the server of each change (watchfiles: inotify, FSEvents, ReadDirectoryChangesW); it walks a project once its files are quiet 1 s (at most 5 s); no timer walk while notifications work.
- Archives and trash: only their last folders are read.
- One process, several roles: the web board and its published API (WebSocket, and HTTP as the same protocol), behind a key; the forge hub (read-only forge reads, at most every 20 s, journal lines); the writer (commits, rebases and pushes the surface's published paths within 5 minutes); each session's watcher reads only its project's journal and wakes its session.
- Clients: the web client, the TUI (`live`), any client of the API.
- Where a cache could come later: closed batches never change, so the History and Dashboard pages can keep their summary in memory once; the forge reads cost the network, not the disk.

Docs items in the backlog (docs-sphinx-rtd, docs-style-guide) move and review the existing pages and images; neither draws the server. Keep each SVG's -texts.md source in step.