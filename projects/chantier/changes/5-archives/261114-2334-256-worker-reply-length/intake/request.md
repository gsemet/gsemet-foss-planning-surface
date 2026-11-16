Worker replies keep their ten-line cap

Measured on batch-16's transcripts (by the spec-writer of driver-context-budget, 2026-11-13): worker.md
caps a worker's reply at ten lines (around line 20), yet Coder replies ran 93 to 105 lines and one
Verifier's 69. Each long reply lands in the Driver's context and pays for every later turn.

Wanted: workers keep the cap (details go to their work files, the reply names them), and the Driver
treats an over-long reply under the rule of worker-reply-contract (CR-230) or a lighter one; measure the
gain on the next batch.