# Board server notifies when a CR arrives by pull on the surface

Filed on the owner's words of 2026-11-23, relayed by the Chief of Staff of okf-schema. To grill later with the owner, not now.

The owner's words (French): "le serveur doit aussi detecter quand une CR est poussee sur la surface partagee (toi par exemple tu vas pousser une CR, qui va etre autosynchronisee sur le repo github, puis le serveur cote chantier, qui tourne sur mon PC a la main, va la recuperer. Donc il doit etre notifie qu'une nouvelle demande est arrivee en inbox ou backlog)."

In short: the board server must notice when a change request arrives in the shared planning surface from elsewhere, and tell its clients (the board, the watcher, the Chief of Staff).

The case: a Chief of Staff session files a CR in the surface; the autosync pushes it to the surface's remote; the board server, running by hand on the owner's machine, pulls the surface. Today the owner learns of the new inbox or backlog item only by looking. Wanted: when the surface's files change by a pull (a CR new in `1-inbox` or `2-backlog`, or moved), the server emits the same notification as a local board write: the board page updates, the watcher wakes the Chief of Staff with a line naming the CR and its stage.

Points to settle at the grill: how the server learns of a pull (file watch on the surface checkout, the remote's state, or both); whether the server itself fetches the surface on a timer; which stages notify (inbox, backlog, ready); no notification for the server's own writes.
