# Board server notifies when a CR arrives by pull on the surface

Short name: `pull-arrival`. Owner's words of 2026-11-23, relayed from okf-schema.

When the board server's writer pulls the shared planning surface and a CR is new in `1-inbox` or `2-backlog`, or moved between them, the server notifies like a local board write: the page updates, and the server appends one journal line, carried by the watcher to the Chief of Staff, naming the CR and its stage. No timer of its own: the arrival is seen after the writer's fetch and rebase. `3-ready` and `4-batch` notify nobody (the owning Chief of Staff's own doing; one Chief of Staff per project). The server's own writes notify nobody.
