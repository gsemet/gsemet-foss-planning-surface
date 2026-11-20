## Summary

The surface server gets one published API, protocol 1, with one message shape on two transports: a WebSocket and, as the degraded case behind a proxy, HTTP (`/api/v1/call/<op>` and a long-poll). This is work in progress: the draft covers the HTTP binding, the op and topic tables, the push loop and the key rules; the WebSocket endpoint and the web client's port come in later commits of the same PR.

## Deliverables

None yet (a structural change: the module diagram is added when the WebSocket and the client port land).

## Blast radius

Medium: the board's server gains a new package and a dependency (`websockets`); the old routes stay in place until the client is ported, so rolling back is a revert.

## Autonomous decisions

- An extra `http.poll` schema in `protocol.json`, for the long-poll body.

## Known gaps

- The WebSocket endpoint, the web client's port, the removal of the old routes, the scenario and the docs are not in this commit yet.

<details><summary>Details</summary>

## Changes

- New package `board/api/` (protocol models and `protocol.json`, ops, topics, push loop, auth and CORS, HTTP binding, times).
- `websockets` added to the dependencies.

## Impacts

No visual change yet.

## Test plan

- [ ] `just check` in the worktree.

## Internal references

CR-406 server-api.

</details>
