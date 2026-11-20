# Release notes draft, for the version PR (not a release folder: no version is set by this CR)

- The server's API is published: protocol 1, over a WebSocket (`/api/v1/ws`) and over HTTP
  (`POST /api/v1/call/<op>`, a long-poll at `POST /api/v1/poll`) for a network where a WebSocket
  does not pass, behind a proxy for instance. 20 ops, 6 topics. Reference: `docs/server-api.md`;
  schema of record: `protocol.json`.
- The web board is one client of it, and updates live: the server pushes a change within a few
  seconds, with no polling by the page.
- A script, or a web page served elsewhere, uses the same API with the key in a header
  (`X-Chantier-Board-Key`); the cookie counts only for the board's own page.
- Breaking: the old `/api/...` routes are gone (use `/api/v1/call/<op>`). `GET /api/board` stays,
  with fewer fields, as the probe.
- A web page left open across the upgrade must be reloaded.
