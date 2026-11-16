# Intent: README reorganisation

The user finds the repository's `README.md` too complicated. The intent is a README a newcomer
reads in one go: an introduction that says what a Change Request really is (a folder of any
content, fungible in the plan), that chantier works in batches rather than continuous delivery,
why one picks direct or Foreman mode, and that chantier respects the project's rules rather than
"zero configuration". The diagrams of "How chantier works" are reordered (detailed, Foreman,
direct). The detailed end of the README (the boards, the gates, your own agents, the models, the
planning folder's layout, the supported hosts, the costs) moves to pages under `docs/`, with a
link left in the README; nothing is lost.

A docs-only change. To run after the reproducible-evals work (batch-13).
