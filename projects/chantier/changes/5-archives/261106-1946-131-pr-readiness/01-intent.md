# Intent

The user sees on the forge itself when a PR or MR must not be merged yet, and cannot merge one into
anything but the default branch by accident. PR 55 and PR 57 were green and mergeable on another
CR's branch: neither CI nor `mergeable` covers that.

This CR also takes `stack-pr-base`, whose request is kept in `intake/stack-pr-base-request.md`:
7b64eec already starts CRs on the default branch unless they have a real dependency, and `take`
holds a CR until its dependency is ready, so its base has a PR. What stays open is who opens a PR
and what a PR on another base says.
