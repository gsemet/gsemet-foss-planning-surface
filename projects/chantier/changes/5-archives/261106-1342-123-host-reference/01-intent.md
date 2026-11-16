# Intent

chantier gets one reference per coding agent in its skill: what the host does with sessions, how
to classify the session a role runs in, and what follows for each class. Its first use is the step
only the user can do: when the host refuses to start a session, the user gets exact instructions
and a text to copy and paste, even from a remote device.

Why now: batch-06's Foreman was started from a remote client. The session runs in a worktree, the
Write tool refuses the main checkout from there, and `.agents/changes/` lives in the main checkout.
Nobody knew until Drivers were blocked: the user could not tell from the picker that a worktree
would be used, and the card only said "the user can start it and paste this prompt".
