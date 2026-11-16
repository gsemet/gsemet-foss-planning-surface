# Intent

On batch 05, auto mode refused `git push --force-with-lease` to a Driver (ask A-2). A stack needs
that push at each restack. The cards answer a `refused` by asking the user to type a line in the
Foreman's session, so the stack stops until they do, and that line may not lift the refusal at all.

The user wants the request to go up by itself: Driver, Foreman, Chief of Staff, who runs the push.
