# A live activity terminal client, proof of the server API

The user, 2026-11-20: "je veux oui une CLI en python, avec un rich ou mieux, de preuve qui permette de tracker d'activite en direct. Si tu t inspire de vercel board ca peut le faire."

- A Python terminal client (Rich, or better: Textual, built on Rich) that follows a surface's activity live, as a second client of the server's published API v1 (`server-api`, CR-406; after `web-client-out`, CR-411). It proves the protocol with a client other than the web UI.
- Inspired by Vercel Board's "swarm board" screen (shown by the user): a header with live counts (working, ready, held, done); a left column of channels (projects, batches) and agents (Drivers with what they hold); a centre "Flow" of events as they arrive (time, channel, who, text: journal lines, rounds, takes, handbacks, merges); a right "Tasks" column: working CRs with their Driver and lease time left (driver-leases, CR-403), then ready CRs with their age.
- Read-only: it watches; it writes nothing and messages no agent.
- Connects with the board's key, over the WebSocket, falling back to HTTP long-poll (the API's degraded case).

Open points for the grill: Textual or Rich alone; shipped in chantier's wheel as a command (`chantier watch --tui`? `chantier top`?) or as a separate example client under `clients/`; which topics it subscribes to; several surfaces at once.

Depends: server-api, web-client-out, driver-leases.
