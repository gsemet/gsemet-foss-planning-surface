## Summary

`just check` linted `skills/` with ruff's rules but only format-checked the repository's own tooling scripts in `scripts/`, so a script that broke a rule was found by hand. The lint now covers `scripts/` too, with the same rules, and the nine findings ruff reported there are fixed with no change in what any script does.

## Deliverables

The `lint` recipe of the `justfile`, before and after:

```diff
-    uvx {{ruff}} check skills
+    uvx {{ruff}} check skills scripts
```

The nine findings fixed in the code (no `# noqa` added, `pyproject.toml` unchanged):

| File | Rule | Fix |
|---|---|---|
| `scripts/copilot_models.py` | RUF100 | unused `# noqa: S310` deleted |
| `scripts/docs_screenshots.py` | PLC0207 | `url.split("#", 1)[0]` |
| `scripts/docs_screenshots.py` | E501 | comment rewrapped |
| `scripts/mod.py` | E501 | docstring's first line shortened |
| `scripts/release_notes.py` | B905 | `zip(..., strict=False)`, same pairing |
| `scripts/release_notes.py` | PLR2004 | constant `MIN_IDENTITY_LENGTH = 3` |
| `scripts/release_notes.py` | RUF005 | `[*images(notes), thread_image]` |
| `scripts/version.py` | PLW1510 | `subprocess.run(..., check=False)` |
| `scripts/version.py` | PLR0911 | `check-tag` moved into `check_tag(version) -> int` |

## Blast radius

**1**: tooling scripts and a lint line only; a plain `git revert` restores the previous state.

Grade: 1

## Autonomous decisions

- Two cosmetic review remarks accepted as they are: the new `CONTRIBUTING.md` sentence's first line is a little over 100 characters, and `MIN_IDENTITY_LENGTH` sits between two version constants.

## Known gaps

None

<details>
<summary>Details</summary>

## Changes

- `justfile`: `lint` runs `ruff check` on `scripts` as well as `skills`.
- The five scripts above: the nine findings fixed; messages and exit codes unchanged.
- `CONTRIBUTING.md`, "Code standards": one sentence saying the tooling scripts meet the Style target through `just lint`.

## Impacts

No visual change. A contributor's `just check` now fails on a ruff finding in `scripts/`.

## Test plan

- [x] No behaviour change in the scripts (Verified at `c0bb193`)
- [x] Local gates at `c0bb193`: `just check` pass (635 tests, release notes ok); `uvx ruff@0.17.5 check skills scripts` and `format --check` pass
- [x] Evidence: none beyond the gates above
- [x] Review: approved at `c0bb193`
- [x] Verified at `c0bb193`
- [x] CI green at `c0bb193`

## Internal references

CR-371 ruff-check-scripts.

</details>
