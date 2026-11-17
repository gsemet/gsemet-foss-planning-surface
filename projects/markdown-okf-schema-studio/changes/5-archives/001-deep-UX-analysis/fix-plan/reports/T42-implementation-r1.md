# T42 implementation — round 1

STATUS: DONE

## Summary
Both commands now have `"category": "Markdown OKF-Schema Studio"` and short titles
("Open Preview to Side", "Refresh Preview"). Palette text is unchanged (category + title).

## Files changed
- package.json (contributes.commands only)
- test/security/package-contract.test.ts (commands entries, type gains `category?`)
- README.md untouched (line 138 already uses the short title; line 140 palette sentence unchanged).

## Tests written first (failing before the fix)
`contributes only opt-in Markdown OKF-Schema Studio commands` failed (deepEqual on commands) after the test update, before the package.json change.

## Tests added or changed
Same test: the two `commands` entries (see below).

## Existing assertions changed
`assert.deepEqual(packageJson.contributes.commands, …)`: old titles "Markdown OKF-Schema Studio: Open Preview to Side" / "…: Refresh Preview"; new titles "Open Preview to Side" / "Refresh Preview" plus `category: "Markdown OKF-Schema Studio"` on both. Required by D-20. Nothing else changed.

## Verification
Screen unlocked (ioreg printed nothing). `gate.sh T42-impl unit contracts full`: compile, unit, contracts-compile, contracts, full all PASS (full 223s; reload suite unchanged).

## Evidence for reviewers
`git diff package.json`: only title lines changed and category lines added; command IDs, icon, enablement, menus, keybindings untouched.

## Open points / STOP reason
None.
