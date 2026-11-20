# Answers: server-api

The request comes from planning-server-Q29 (`2-backlog/P3/planning-server/02-answers.md`). The
answers below settle the sixteen open questions of this CR's first specification (§16).

## 2026-11-20, settled by the Chief of Staff (the user asks no questions)

All sixteen take the specification's recommended answer, on which it is written:

1. Two CRs: this one, then `1-inbox/web-client-out` (the folder move and `--ui`), filed now.
2. One JSON message shape on both transports; today's route answers unchanged as each op's data.
3. A push carries the whole value, never a diff; an `events` topic streams the typed journal
   lines with a `seq` cursor.
4. Protocol 1 changes only by addition; a breaking change is protocol 2 under `/api/v2/`; another
   protocol is refused with close code 4426.
5. `protocol.json` covers the message types and each op's and topic's arguments; results are
   documented by example in `docs/server-api.md`.
6. HTTP degraded mode: call plus long-poll (held up to 20 s).
7. Auth: the cookie counts only from the server's own origin; the header key or the key in the
   WebSocket's first message works from any origin; CORS open with no credentials.
8. Proxy: plain HTTP, TLS at the proxy; `X-Forwarded-Host` and https origins accepted; the key
   exchange redirects with a relative `Location`.
9. The UI in `chantier/clients/web/`, in the one wheel; `board --ui <folder>|none`.
10. No build step, no framework.
11. Clients shipped: the web client and the CLI's probe and seat call; no SDK; two examples in
    the doc.
12. `websockets` (wheels for Linux, macOS and Windows), not `wsproto`.
13. The command stays `chantier board`.
14. Old routes removed at once; `/api/board` kept as the probe with its identity fields only.
15. The footer adds " (HTTP)" only in degraded mode.
16. The AGENTS.md edits of §11.2 are approved as written.

## 2026-11-20, the spec critic's first pass (15 points), settled by the Chief of Staff

Ten text fixes (5 to 10, 12 to 15) go to the writer without a question; for 13, the Part 2 text
is marked "not in this CR: web-client-out" and copied into that CR's own specification by its
spec-writer. The five that touch behaviour, each the critic's recommended answer:

1. **The cookie's same-origin rule** applies only to `/api/v1/` and the WebSocket upgrade;
   opening `/` and the static files keep today's cookie check (a bookmark or a link from a chat
   app still opens the page).
2. **A path prefix behind a proxy** is supported only on a host or origin of its own;
   `docs/server-api.md` says so.
3. **A web UI from another origin:** CORS stays; "UI from another origin: unproved in a real
   browser" goes in the PR's Known gaps unless one Chromium check from another origin proves it.
4. **Sockets with no key yet:** only sockets past `welcome` count toward the 64; sockets still
   waiting for `hello` have a small separate cap and a short wait.
11. **The page's CSP:** §8 names `HTML_POLICY`; the Chromium check and the phone check confirm
    the socket opens under it; a phone the Driver cannot reach goes to Known gaps.
- The writer's numbers for point 4 (at most 16 sockets waiting for `hello`, `HELLO_S` 5 s) are accepted.
