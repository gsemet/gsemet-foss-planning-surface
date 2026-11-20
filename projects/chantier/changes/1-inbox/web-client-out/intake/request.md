# The web client moves out of the server's package

Split off `server-api` (2026-11-20, its answer 1, settled by the Chief of Staff): once the server's API is published (protocol 1), the web UI moves to its own folder and `chantier board --ui <folder>|none` serves another UI or none, so other clients (native Android or iOS apps, other UIs) stand beside it. The user's words are planning-server-Q29. Its scope is the second part of server-api's 03-change-spec.md (the folder move and `--ui`). After server-api.
