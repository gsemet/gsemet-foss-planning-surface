# The board listens on all addresses with a key that never expires

From the Fable audit of 2026-11-21 (high, confirmed): the board listens on `0.0.0.0` by default, in clear HTTP (`board/address.py:21`); its key never expires, travels in the URL and then in a one-year cookie without `Secure` (`board/key.py:91`). Whoever reads it on the local network can write or rewrite a specification and move it to `3-ready`, which Drivers then run with their push rights. The key is also printed by each `chantier board` start, so it sits in 3 local transcripts (audit, low).

Wanted: the board is not exposed to the network unless the user asks, and its key can be revoked and stays out of the agents' output. The user reaches the board from a phone on the local network today.
