# The board listens on all addresses with a key that never expires

From the Fable audit (2026-11-21, high): the board listens on 0.0.0.0 in clear HTTP, with a key that never expires and is printed into transcripts. Intent: no network exposure unless the user asks; a key the user can revoke, kept out of the agents' output; the phone access kept as a conscious choice.
