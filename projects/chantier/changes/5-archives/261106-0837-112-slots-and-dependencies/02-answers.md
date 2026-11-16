# Answers

Given by the user on 2026-11-06, in the Chief of Staff's session.

- **Dependencies:** declared, in an optional JSON file placed in the CR's folder. The CLI refuses
  a `take` until they are met, and the order of the stack follows from them.
- **Start:** a dependent CR starts once its dependency is ready, and stacks on it; it does not
  wait for the merge.
- **Slot:** a running Driver, as today: a `ready` or `blocked` CR holds none. A QA driver counts
  too.
- **When:** after `batch-folder`, which it builds on; priority P1.
- **Specification:** the user asked for no more questions and to finalize it, on 2026-11-06.
