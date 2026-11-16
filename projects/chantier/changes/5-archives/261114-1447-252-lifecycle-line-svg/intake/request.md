A new, very simple SVG of a CR's life: one line of steps, no folders, no states.

The user (2026-11-14): "Je pense qu'il faut un autre SVG sur le lifecycle sans (on en a un avec les états / dossier) mais un plus simple avec juste : Intent -> grill -> spec -> spec critic -> driver -> verifier -... -> PR prête à merger"

Today `docs/cr-lifecycle.svg` and `docs/cr-lifecycle-simple.svg` both show the folders (1-inbox/ … 5-archives/) and the states; `cr-lifecycle-simple.svg` is used in README.md (lines ~126-145). This one is a single line: Intent → grill → spec → spec critic → driver → (coder, inspector, gate, CI) → verifier → … → PR ready to merge, in the words of CR-248 ready-wording (prête localement / PR en draft / prête à merger).

Depends on: the inbox item `spec-critic` (the step it draws; diagrams are the target, so it may be drawn first as the target) and CR-248 ready-wording (the end state's words). Where it goes (README, docs) is for the grill.