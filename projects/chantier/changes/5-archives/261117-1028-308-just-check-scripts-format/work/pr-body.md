## Summary

`just check` format-checked `skills/` but not the repository's own tooling scripts in `scripts/`, so an unformatted script was only found by hand. The `lint` recipe now format-checks `scripts` too, so an unformatted script fails the check locally and in CI. Three scripts failed that check, and they are formatted in the same change.

## Deliverables

The first line of the `lint` recipe in `justfile`:

```diff
-    uvx {{ruff}} format --check skills
+    uvx {{ruff}} format --check skills scripts
```

| Script | Before | After |
| --- | --- | --- |
| `scripts/copilot_models.py` | formatted | unchanged |
| `scripts/docs_screenshots.py` | formatted | unchanged |
| `scripts/mod.py` | would be reformatted | formatted |
| `scripts/release_notes.py` | would be reformatted | formatted |
| `scripts/version.py` | would be reformatted | formatted |

The pinned `ruff@0.17.5` formatter wrote the three files from the repository root (line length 100); the diffs are layout only.

## Blast radius

Grade: **1**

Only the format-check line of a lint recipe and the layout of three scripts change; a plain `git revert` restores the previous state.

## Autonomous decisions

None

## Known gaps

None

<details>
<summary>Details</summary>

## Changes

- `justfile`: `lint` runs `ruff format --check skills scripts`; the `ruff check` line, the pin and the other lines are unchanged.
- `scripts/mod.py`, `scripts/release_notes.py`, `scripts/version.py`: formatted by `uvx ruff@0.17.5 format scripts`, no hand edit.

## Impacts

No visual change. Contributors who edit a script now get a failing `just check` until it is formatted. `ruff check` (lint rules) and `mypy` still do not cover `scripts/`; that is out of scope here.

## Test plan

- [x] New or changed tests: No behaviour change
- [x] Local gates at `eb93500`: `just check`, `uvx ruff@0.17.5 format --check skills scripts`, `just version-show`, `uv run --script scripts/version.py --help`
- [x] Evidence: before at `3df17b9` (`just lint` fails naming the three scripts), after at `eb93500` (all files formatted)
- [x] Review: approved at `eb93500`
- [x] Verified at `eb93500`
- [x] CI green at `eb93500`

## Internal references

- CR-308 just-check-scripts-format
- Origin: the retro of batch-22

</details>
