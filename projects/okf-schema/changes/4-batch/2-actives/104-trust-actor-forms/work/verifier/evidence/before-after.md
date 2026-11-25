# CR-104: before and after

- Before: base `2f09cef3e786d1696e42b5cb305d4a55111e7725`, detached worktree, `src/` and `tests/` checked out.
- After: pushed head `7a33d920b46188821c4ebf73d008fbc12dcdf750`, the CR's worktree.
- Technique: the specification's "Evidence" section, items 1 to 6 (text outputs; no UI, no screenshot).

## How to reproduce

Copy `../probe.py` into a folder under the CR's `work/scratch/` (it writes its scratch files beside
itself; the base worktree is its `b/` subfolder), then, with the worktree's environment:

```console
uv --directory <worktree> run --no-sync -- python <scratch>/probe.py <scratch>/b/src
uv --directory <worktree> run --no-sync -- python <scratch>/probe.py <worktree>/src
```

## Pairs

| Pair | Before (`before-2f09cef.txt`) | After (`after-7a33d92.txt`) |
|---|---|---|
| Tier of `reference_agent/gemini-2.5-pro`, `langchain.agents/0.3`, `acme.ci:nightly` | unverified, W10 | machine-confirmed, no W10 |
| Tier of `alice`, `Alice`, `human:` | unverified, W10 | machine-confirmed, W10 |
| `process:nightly-check`, `bot:okf-schema`, `human:alice`, `Human:alice` | machine-confirmed, machine-confirmed, human-reviewed, machine-confirmed; no W10 | unchanged |
| Not a string, or empty (`42`, `True`, list, mapping, `0`, `""`, `None`) | unverified; W10 or E9 | unchanged |
| W10 message for entry 1 | ends with a literal `[{i}]`, teaches `bot:ci` | the specification's exact text, index printed |
| `show_bundle(...).trust_tier`, `okf-schema show` | unverified | machine-confirmed |
| `validate-md --strict`, producer/version actor | exit 1, one W10 | exit 0, no warning |
| `validate-md --strict`, `by: alice` | exit 1, W10 ending `[{i}]` | exit 1, W10 naming `verified entry [0]` twice |
| `validate-md --strict`, `generated.by: alice`, `sources[].author: alice` | exit 0 | exit 0 (still unchecked) |

Tests: the head's four changed test files run against the base source give 13 failed, 280 passed;
at the head the same files and `test_project_contract.py` give 295 passed (commands in `verify.md`).
