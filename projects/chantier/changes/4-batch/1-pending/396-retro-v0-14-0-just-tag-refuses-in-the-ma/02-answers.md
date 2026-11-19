# Answers

## Settled by the Chief of Staff (2026-11-20, the user asks no questions)
- Grilled enough: the intent is the grill. The user's go, 2026-11-20: "relance un foreman avec les inbox et les p1"; this CR joins batch-29 (factory, stack) once specified.

## Settled by the Chief of Staff (2026-11-20, the user asks no questions): the fix
1. The release procedure fast-forwards the main checkout (`git fetch` then `git merge --ff-only origin/main`, refusing with a clear message if the checkout is dirty or not on main) before `just tag`, so `just tag` runs from the main checkout as CONTRIBUTING.md says. The fast-forward goes in the `tag` recipe itself (or a step it calls) so no agent has to remember it; check-tag keeps reading the local version, which then equals origin/main's.
2. Never a forced update of the main checkout; a refusal stops the step and says what to do.
3. Update CONTRIBUTING.md "Release" and the release-driver card if they name the steps.
4. Must work on Linux, macOS and Windows (just recipes stay portable).

## Settled by the Chief of Staff (2026-11-20, the user asks no questions): who runs `just tag`
- Keep the read-only rule whole: no Driver moves the main checkout. The Release driver hands `just tag` to the steering session (the Foreman, or the Chief of Staff in direct mode). That session already fast-forwards the main checkout after a merge, and it runs `just tag` there; ff-main inside the recipe stays as the guard. Neither driver.md nor concepts.md rule 8 gets an exception. The hand-off goes in the Release driver section and in the steering cards (foreman.md, chief-of-staff.md direct mode), where the release steps are.
