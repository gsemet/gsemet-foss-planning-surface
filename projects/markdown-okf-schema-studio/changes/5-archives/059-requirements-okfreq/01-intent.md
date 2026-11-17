# Add requirements layer

I need to lock the behavior of the VS Code extension in a requirements layer
anchored to the code.

To do that => use `okf-schema`, and its specific subset `okfreq`.
Load the `okfreq` skill to follow the process to declare the requirements layer in
`.agents/requirements/`, setup the guidelines in AGENTS.md and checks in the `justfile`.
