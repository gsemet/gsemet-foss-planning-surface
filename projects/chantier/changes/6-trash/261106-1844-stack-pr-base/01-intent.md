# Intent

In a stack, every PR stands on a base that exists on the forge and has its own PR, or on the
default branch, and the user cannot merge a PR into anything else by accident.

Who opens a CR's PR while a parallel stack is not ordered yet must be stated once, in the cards,
so that a CR Driver and the stack driver do not each do half of it.

Open questions for the grill:

- Does a CR Driver stop at a pushed, gated head and leave the PR to the stack driver, or open its
  PR on the default branch until the stack is ordered?
- Who refuses a PR on a base with no PR: the card (the Driver judges), or `ship` (`rails.py`)?
- Does the Chief of Staff's report flag a PR whose base is not the default branch before a merge?
