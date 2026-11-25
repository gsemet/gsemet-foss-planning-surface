# Plan: `okf-schema show` and concept names

## What changes for you

| Command | Today | After the change |
| --- | --- | --- |
| `show --path bundle api/health-check` | "Concept not found" | prints `api/health-check.md` |
| `show --path bundle api/health-check.md` | prints the concept | unchanged |
| `show --path bundle api` (a directory, no `api.md`) | Python traceback | "Concept not found", exit code 2 |
| `show --path bundle ../notes.md` | reads the file outside the bundle | refused, exit code 2 |

- A directory is never a concept: `api` resolves to `api.md` when that file exists, even if `api/` exists too.
- A symlink inside the bundle whose target is outside it is refused.
- An absolute path that points inside the bundle stays accepted.
- Python API: `show_bundle` follows the same rules and raises `FileNotFoundError` with an explicit message.

## Limits

- Only `show` and `show_bundle` change. The outside-symlink rule for `validate`, `list`, `index`, `backlinks` and `lint` is a separate change.
- The output format of `show` is handled in #58.

## Compatibility

A script that relied on `show` reading a file outside the bundle, or through a symlink that leaves it, will now get an error.

## Documentation

The command reference, the tutorials' command examples and the packaged agent skill will state that `.md` is optional and describe the refusals.
