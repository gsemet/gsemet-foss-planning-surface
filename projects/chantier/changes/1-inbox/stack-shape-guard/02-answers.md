Short name: `stack-shape`

# Answers
1. stack-shape-Q1 (2026-11-21): **The guard on a per-CR ready ask in a stack batch.** D. "Refuse unless forced": `asks` refuses a per-CR `ready-to-merge` ask in a stack batch (a fix CR excepted), and an explicit flag lets it through.
2. stack-shape-Q2 (2026-11-21): **The shape line at each heartbeat.** A. One fixed line at each `status --refresh`, in stack batches only ("shape stack: next take stack; stack driver: none; native stack: absent").
3. stack-shape-Q3 (2026-11-21): **The reload's reread of the shape.** Not settled. The user's words: "I would say shape section but how do you « just read the shape section in the Md » if you do not have a Md per shape type ?" (foreman.md has no section per shape: its stack rules are spread over "The user's boundaries" and "Your means"). Asked again as Q5.
4. stack-shape-Q4 (2026-11-21): **The Chief of Staff's check of an ask.** A. One line in the CoS card: each Foreman ask is checked against the batch's shape (a stack batch: a stack ask and a native stack), not only rebased and green.
5. stack-shape-Q5 (2026-11-21, Q3 asked again): **What a stack batch's Foreman rereads after a compaction.** B. A separate card file, `foreman-stack.md`, read at the reload of a stack batch; foreman.md points to it (its stack rules move there).
6. stack-shape-Q6 (2026-11-21, after the full restatement): **Grilled enough.** A. Yes: the spec-writer, then the critic; destination the next batch (`3-ready`).
Spec v1 (2026-11-21): written; three open questions go to the user (Q7-Q9).
7. stack-shape-Q7 (2026-11-21, the spec's open question 1): **When the guard starts.** A. Only once the batch has made its first stack (a CR with `stacked`, merged or not); before that, per-CR asks stay allowed.
8. stack-shape-Q8 (2026-11-21, the spec's open question 2): **Who may use `--outside-stack`.** A. Only on a Chief of Staff order carrying the user's word (reason `O-<k>: …`).
9. stack-shape-Q9 (2026-11-21, the spec's open question 3): **A mismatched ask at the Chief of Staff.** A. It sends the ask back to the Foreman (`shape: through the stack`) and tells the user in one line ("CR-12 asked alone in a stack batch: sent back through the stack").
Spec critic: yes, it adds a CLI refusal, a status line, a card and a manifest action.
