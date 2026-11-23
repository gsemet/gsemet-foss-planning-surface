Short name: `pull-arrival`

1. pull-arrival-Q1: **What is seen.** A. The page updates and the server adds a journal line that the watcher carries to the Chief of Staff, naming the CR and its stage.
2. pull-arrival-Q2: **A timer.** A. No: the arrival is seen after the writer's fetch and rebase; no extra timer.
3. pull-arrival-Q3: **Which stages notify.** Inbox and backlog only, not `3-ready`. The user's words: "Inbox et backlog. Normalement il ne peut pas y avoir 2 chief of staff actif sur le même projet (donc owner du batch)." So a CR reaching `3-ready` or `4-batch` by a pull is the owning Chief of Staff's own doing and notifies nobody.
4. pull-arrival-Q4: **A moved CR.** A. Yes: a new CR and a CR changed of stage (between inbox and backlog) both notify.
5. (rule from the request, no question) The server's own writes notify nobody.
6. pull-arrival-Q5: **Grilled enough.** A. Specify, for the running batch batch-31.

Destination: running batch batch-31.
Spec critic: yes, default model (it changes what the server does and what the user sees).
7. pull-arrival-Q6: **A move between backlog rows.** A. Yes: a pull that moves a CR from one backlog row to another (for example P2 to P1) notifies, as a move.
8. pull-arrival-Q7: **A CR back from `3-ready`.** A. Yes, with the mention that it comes back from `3-ready`. (A CR back from `4-batch`, the archives or the trash is for the spec to settle in line with Q3: it is the owning Chief of Staff's own doing.)
